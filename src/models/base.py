#!/usr/bin/env python
# encoding: utf-8
import logging
import struct

logger = logging.getLogger(__name__)

EEP_MAP = [{"name": "TEMPHIST", "addr": 0x000, "length": 2, "type": "int"},
           {"name": "CAPHIST", "addr": 0x021, "length": 32, "type": "int"},
           {"name": "CHARGER", "addr": 0x041, "length": 1, "type": "int"},
           {"name": "CAPACITANCE", "addr": 0x042, "length": 1, "type": "int"},
           {"name": "CHARGEVOL", "addr": 0x043, "length": 2, "type": "int"},
           {"name": "CHGMAXVAL", "addr": 0x045, "length": 2, "type": "int"},
           {"name": "POWERDET", "addr": 0x047, "length": 1, "type": "int"},
           {"name": "CHARGECUR", "addr": 0x048, "length": 2, "type": "int"},
           {"name": "HWVER", "addr": 0x04A, "length": 2, "type": "str"},
           {"name": "CAPPN", "addr": 0x04C, "length": 16, "type": "str"},
           {"name": "SN", "addr": 0x05E, "length": 8, "type": "str"},       # need program, id
           {"name": "PCBVER", "addr": 0x064, "length": 2, "type": "str"},
           {"name": "MFDATE", "addr": 0x066, "length": 4, "type": "str"},   # need program, yyww
           {"name": "ENDUSR", "addr": 0x06A, "length": 2, "type": "str"},   # need program, vv
           {"name": "PCA", "addr": 0x06C, "length": 11, "type": "str"},     # need program, default all 0
           {"name": "INITIALCAP", "addr": 0x077, "length": 1, "type": "int"}]


class PGEMException(Exception):
    pass


class PGEMBase(object):

    def __init__(self, device,  **kvargs):
        # slot number for dut on fixture location.
        # from 0 to 3, totally 4 slots in UFT
        self.slot = kvargs.get("slot", 0)

        # channel number for mother board.
        # 8 mother boards can be stacked from 0 to 7.
        # use 1 motherboard in default.
        self.channel = kvargs.get("channel", 0)

        # I2C adapter device
        self.device = device

    def switch(self):
        """switch I2C ports by PCA9548A, only 1 channel is enabled.
        chnum(channel number): 0~7
        slotnum(slot number): 0~7
        """
        chnum = self.channel
        slot = self.slot
        self.device.slave_addr = 0x70 + chnum    # 0111 0000
        wdata = [0x01 << slot]

        # Switch I2C connection to current PGEM
        # Need call this function every time before communicate with PGEM
        self.device.write(wdata)

    def switch_back(self):
        """switch I2C ports back to mother board
           chnum(channel number): 0~7
        """
        chnum = self.channel
        self.device.slave_addr = 0x70 + chnum    # 0111 0000
        wdata = 0x00

        # Switch I2C connection to mother board
        # Need call this function every time before communicate with mother board
        self.device.write(wdata)

    @staticmethod
    def _query_map(mymap, **kvargs):
        """method to search the map (the list of dict, [{}, {}])
        params: mymap:  the map to search
                kvargs: query conditon key=value, key should be in the dict.
        return: the dict match the query contdtion or None.
        """
        r = mymap
        for k, v in kvargs.items():
            r = filter(lambda row: row[k] == v,  r)
        return r

    def read_vpd_byname(self, reg_name):
        """method to read eep_data according to eep_name
        eep is one dict in eep_map, for example:
        {"name": "CINT", "addr": 0x02B3, "length": 1, "type": "int"}
        """
        eep = self._query_map(EEP_MAP, name=reg_name)[0]
        start = eep["addr"]                 # start_address
        length = eep["length"]              # length
        typ = eep["type"]                   # type

        self.device.slave_addr = 0x53
        datas = self.device.read_reg(start, length)

        if(typ == "word"):
            val = datas[0] + (datas[1] << 8)
            return val
        if(typ == "str"):
            return ''.join(chr(i) for i in datas)
        if(typ == "int"):
            return datas[0]

    def read_vpd(self):
        """method to read out EEPROM info from dut
        return a dict.
        """
        dut = {}
        for eep in EEP_MAP:
            reg_name = eep["name"]
            dut.update({reg_name: self.read_vpd_byname(reg_name)})
        return dut

    @staticmethod
    def load_bin_file(path):
        """read a file and transfer to a binary list
        """
        datas = []
        f = open(path, 'rb')
        s = f.read()
        for x in s:
            rdata = struct.unpack("B", x)[0]
            datas.append(rdata)
        return datas

    def write_vpd(self, barcode, path):
        """method to write barcode information to PGEM EEPROM
        barcode is a dict of 2D barcode information
        path is the ebf file location.
        """
        buffebf = self.load_bin_file(path)
        #[ord(x) for x in string]
        id = [ord(x) for x in barcode['ID']]
        yyww = [ord(x) for x in (barcode['YY'] + barcode['WW'])]
        vv = [ord(x) for x in barcode['VV']]

        # id == SN == Product Serial Number
        eep = self._query_map(EEP_MAP, name="SN")[0]
        buffebf[eep["addr"]: eep["addr"] + eep["length"]] = id

        # yyww == MFDATE == Manufacture Date YY WW
        eep = self._query_map(EEP_MAP, name="MFDATE")[0]
        buffebf[eep["addr"]: eep["addr"] + eep["length"]] = yyww

        # vv == ENDUSR == Manufacturer Name
        eep = self._query_map(EEP_MAP, name="ENDUSR")[0]
        buffebf[eep["addr"]: eep["addr"] + eep["length"]] = vv

        # write to VPD
        self.device.slave_addr = 0x53
        for i in range(0x00, len(buffebf)):      # can be start with 0x41, 0x00 for ensurance.
            self.device.write_reg(i, buffebf[i])
            self.device.sleep(5)

        # readback to check
        assert barcode["ID"] == self.read_vpd_byname("SN")
        assert (barcode["YY"] + barcode["WW"]) == self.read_vpd_byname("MFDATE")
        assert barcode["VV"] == self.read_vpd_byname("ENDUSR")

    def control_led(self, status="off"):
        """method to control the LED on DUT chip PCA9536DP
           status=1, LED off, default.
           staus=0, LED on.
        """
        LOGIC = {"on": 0, "off": 1}
        status = LOGIC.get(status)
        if(status is None):
            raise PGEMException("wrong LED status is set")

        self.device.slave_addr = 0x41
        REG_OUTPUT = 0x01
        REG_CONFIG = 0x03

        # config PIO to output
        wdata = [REG_CONFIG, 0x00]
        self.device.write(wdata)

        # set LED status
        out = status << 1
        wdata = [REG_OUTPUT, out]
        self.device.write(wdata)

    def self_discharge(self, status=False):
        """Controlled by I/O expander IC, address 0x41
           when IO=0, not discharge;
           when IO=1, discharge.
        """
        if(status):
            IO = 1
        else:
            IO = 0

        self.device.slave_addr = 0x41
        REG_OUTPUT = 0x01
        REG_CONFIG = 0x03

        # config PIO to output
        wdata = [REG_CONFIG, 0x00]
        self.device.write(wdata)

        # set IO status
        wdata = [REG_OUTPUT, IO]
        self.device.write(wdata)

    def encrypted_ic(self):
        pass

    def write_bq24707(self, reg_addr, wata):
        """
        write regsiter value to charge IC BQ24707
        """
        self.device.slave_addr = 0x09

        # write first low 8bits, then high 8bits
        self.device.write_reg(reg_addr, [wata & 0x00FF, wata >> 8])

    def read_bq24707(self, reg_addr):
        """
        read register value from charge IC BQ24707
        """
        self.device.slave_addr = 0x09
        ata_in = self.device.read_reg(reg_addr, length=2)

        # first low 8bits then high 8bits
        val = (ata_in[1] << 8) + ata_in[0]
        return val

    def charge(self, status=True):
        """
        Send charge option to charge IC to start the charge.
        Charge IC BQ24707 is used as default.
        Override this function is use other IC instead.
        """
        # BQ24707 register address
        CHG_OPT_ADDR = 0x12
        CHG_CUR_ADDR = 0x14
        CHG_VOL_ADDR = 0x15
        INPUT_CUR_ADDR = 0x3F
        MAN_ID_ADDR = 0xFE
        DEV_ID_ADDR = 0xFF

        # check IC
        logger.debug(self.read_bq24707(MAN_ID_ADDR))
        logger.debug(self.read_bq24707(DEV_ID_ADDR))

        # write options
        charge_option = 0x1990
        if status:
            # start charge
            charge_option &= ~(0x01)    # clear last bit
        else:
            # stop charge
            charge_option |= 0x01   # set last bit
        self.write_bq24707(CHG_OPT_ADDR, charge_option)
        self.write_bq24707(CHG_CUR_ADDR, 0x01C0)
        self.write_bq24707(CHG_VOL_ADDR, 0x1200)
        self.write_bq24707(INPUT_CUR_ADDR, 0x0400)

        # read back to check if written successfully
        assert self.read_bq24707(CHG_OPT_ADDR) == charge_option
        assert self.read_bq24707(CHG_CUR_ADDR) == 0x01C0
        assert self.read_bq24707(CHG_VOL_ADDR) == 0x1200
        assert self.read_bq24707(INPUT_CUR_ADDR) == 0x0400

    def load_discharge(self):
        pass

    def auto_discharge(self, status=False):
        """output PRESENT/AUTO_DISCH signal on TCA9555 on mother board.
           When IO=0, discharge;
           When IO=1, not discharge.
        """
        if(status):
            IO = 0
        else:
            IO = 1

        chnum = self.channel

        self.device.slave_addr = 0x20 + chnum
        REG_INPUT = 0x00
        REG_OUTPUT = 0x02
        REG_CONFIG = 0x06

        # config PIO-0 to output and PIO-1 to input
        # first PIO-0 then PIO-1
        wdata = [REG_CONFIG, 0x00, 0xFF]
        self.device.write(wdata)

        # read current status
        val = self.device.read_reg(REG_INPUT, length=2)
        val = val[0]    # only need port 0 value

        # set current slot
        if(IO == 1):
            # set bit
            val |= (IO << self.slot)
        else:
            # clear bit
            val &= ~(0X01 << self.slot)

        # output
        # first PIO-0, then PIO-1
        wdata = [REG_OUTPUT, val, 0xFF]
        self.device.write(wdata)

        # read status back
        val = self.device.read_reg(REG_INPUT, length=2)
        val = val[0]    # only need port 0 value
        val = (val & (0x01 << self.slot)) >> self.slot
        assert val == 0

    def check_power_fail(self):
        """check power_fail_int signal on TCA9555 on mother board
        return true is power failed.
        """
        chnum = self.channel

        self.device.slave_addr = 0x20 + chnum
        REG_INPUT = 0x00
        REG_OUTPUT = 0x02
        REG_CONFIG = 0x06

        # config PIO-0 to output and PIO-1 to input
        # first PIO-0 then PIO-1
        wdata = [REG_CONFIG, 0x00, 0xFF]
        self.device.write(wdata)

        # read reg_input
        val = self.device.read_reg(REG_INPUT, length=2)
        val = val[1]    # only need port 1 value

        # check current slot
        val = (val & (0x01 << self.slot)) >> self.slot
        if(val == 0):
            # PWR_OK
            return False
        else:
            # PWR_FAIL
            return True

    def check_temp(self):
        pass

if __name__ == "__main__":
    logging.basicConfig()

    from pyaardvark import Adapter
    adk = Adapter()
    adk.open(portnum=0)

    DUT = PGEMBase(device=adk, slot=1)
    DUT.switch()
    print DUT.read_vpd()
    #DUT.control_led(status="off")

    barcode = {
        'PN': 'AGIGA8601-400BCA',
        'RR': '10',
        'VV': '02',
        'YY': '14',
        'WW': '41',
        'ID': '88888888'
    }
    path = "./101-40028-01-Rev02 Crystal2 VPD.ebf"
    DUT.write_vpd(barcode, path)

    print DUT.read_vpd()
    #DUT.charge(True)
    #DUT.self_discharge(False)

    #DUT.switch_back()
    #print DUT.check_power_fail()
    #DUT.auto_discharge(False)

    adk.close()
