#!/usr/bin/env python
# encoding: utf-8
"""Base Model for Cororado PGEM I2C functions
2 functions are on the mother board, check_power_fail() and auto_discharge().
other functions are on the dut board.
"""
__version__ = "0.1"
__author__ = "@boqiling"
__all__ = ["PGEMBase"]

import logging
import struct
import re
from dut import DUT

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

BARCODE_PATTERN = re.compile(r'(?P<SN>(?P<PN>AGIGA\d{4}-\d{3}\w{3})(?P<VV>\d{2})(?P<YY>[1-2][0-9])(?P<WW>[0-4][0-9]|5[0-3])(?P<ID>\d{8})-(?P<RR>\d{2}))')


class PGEMException(Exception):
    pass


class PGEMBase(DUT):

    def __init__(self, device, barcode, **kvargs):
        # slot number for dut on fixture location.
        # from 0 to 3, totally 4 slots in UFT
        self.slot = kvargs.get("slot", 0)

        # channel number for mother board.
        # 8 mother boards can be stacked from 0 to 7.
        # use 1 motherboard in default.
        self.channel = kvargs.get("channel", 0)

        # I2C adapter device
        self.device = device
        r = BARCODE_PATTERN.search(barcode)
        if r:
            self.sn = r.groupdict()
        else:
            raise PGEMException("Unvalide barcode.")

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
        # Need call this function every time before communicate with
        # mother board
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
            reg_name = eep["name"].lower()
            dut.update({reg_name: self.read_vpd_byname(reg_name)})

        #TODO not tested
        # import change:
        # set self.values to write to database later.
        for k, v in dut:
            setattr(self, k, v)

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

    def write_vpd(self, path):
        """method to write barcode information to PGEM EEPROM
        barcode is a dict of 2D barcode information
        path is the ebf file location.
        """
        buffebf = self.load_bin_file(path)
        #[ord(x) for x in string]
        id = [ord(x) for x in self.sn['ID']]
        yyww = [ord(x) for x in (self.sn['YY'] + self.sn['WW'])]
        vv = [ord(x) for x in self.sn['VV']]

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
        # can be start with 0x41, 0x00 for ensurance.
        for i in range(0x00, len(buffebf)):
            self.device.write_reg(i, buffebf[i])
            self.device.sleep(5)

        # readback to check
        assert self.sn["ID"] == self.read_vpd_byname("SN")
        assert (self.sn["YY"] + self.sn["WW"]) == self.read_vpd_byname("MFDATE")
        assert self.sn["VV"] == self.read_vpd_byname("ENDUSR")

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
        """return True for valid data.
        """
        val = self.device.read_reg(0x00, length=128)
        # valid data in 0x00 to 0x80 (address 0 to 127)
        # 0xFF in 0x80 to 0xFF (address 128 to 256)
        try:
            for v in val:
                assert v == 255
        except AssertionError:
            # good
            return True
        return False

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

    def charge(self, option, status=True):
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
        charge_option = option["charge_option"]    # 0x1990
        if status:
            # start charge
            charge_option &= ~(0x01)    # clear last bit
        else:
            # stop charge
            charge_option |= 0x01   # set last bit
        self.write_bq24707(CHG_OPT_ADDR, charge_option)
        self.write_bq24707(CHG_CUR_ADDR, option["charge_current"])   # 0x01C0
        self.write_bq24707(CHG_VOL_ADDR, option["charge_voltage"])   # 0x1200
        self.write_bq24707(INPUT_CUR_ADDR, option["input_current"])  # 0x0400

        # read back to check if written successfully
        assert self.read_bq24707(CHG_OPT_ADDR) == charge_option
        assert self.read_bq24707(CHG_CUR_ADDR) == option["charge_current"]
        assert self.read_bq24707(CHG_VOL_ADDR) == option["charge_voltage"]
        assert self.read_bq24707(INPUT_CUR_ADDR) == option["input_current"]

    def load_discharge(self):
        # the agilent load code should not be here.
        # delete this function.
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
        assert val == IO

    def check_power_fail(self):
        """check power_fail_int signal on TCA9555 on mother board
        return true if power failed.
        """
        chnum = self.channel

        self.device.slave_addr = 0x20 + chnum
        REG_INPUT = 0x00
        #REG_OUTPUT = 0x02
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
        return val != 0

    @staticmethod
    def _calc_temp(temp):
        # method to caculate the temp sensor value of chip SE97BTP
        if(int(temp) & (0x01 << 12)):
            # check 12 bit, 1 for negative , 0 for positive
            result = (~(int(temp) >> 1) & 0xFFF) * 0.125
            # 0.125 for resolution
            result += 0.125     # since FFFF = -0.125, not 0.
            result = -result
        else:
            result = ((int(temp) >> 1) & 0xFFF) * 0.125
            # 0.125 for resolution
        return result

    def check_temp(self):
        self.device.slave_addr = 0x1B
        # check device id
        val = self.device.read_reg(0x07, length=2)
        val = (val[0] << 8) + val[1]
        logger.debug("temp sensor id: " + hex(val))
        assert val == 0xA203

        # check temp value
        val = self.device.read_reg(0x05, length=2)
        val = (val[0] << 8) + val[1]
        logger.debug("temp value: " + hex(val))

        return self._calc_temp(val)


if __name__ == "__main__":
    import time
    logging.basicConfig(level=logging.DEBUG)

    from UFT.devices.aardvark import pyaardvark
    adk = pyaardvark.Adapter()
    adk.open(portnum=0)

    barcode = "AGIGA9811-001BCA02143500000002-01"

    bq24704_option = {"charge_option": 0x1990,
                      "charge_current": 0x01C0,
                      "charge_voltage": 0x1200,
                      "input_current": 0x0400}

    dut = PGEMBase(device=adk, slot=0, barcode=barcode)
    dut.switch_back()
    print DUT.check_power_fail()

    dut.switch()
    dut.charge(option=bq24704_option, status=True)

    dut.switch_back()
    while(dut.check_power_fail()):
        time.sleep(10)
        pass

    dut.switch()
    print dut.read_vpd()
    dut.control_led(status="on")

    path = "./101-40028-01-Rev02 Crystal2 VPD.ebf"
    dut.write_vpd(path)

    print dut.read_vpd()
    print dut.check_temp()
    #dut.self_discharge(False)
    #dut.charge(option=bq24704_option, status=False)

    #dut.switch_back()
    #print dut.check_power_fail()
    #dut.auto_discharge(True)

    adk.close()
