#!/usr/bin/env python
# encoding: utf-8


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
           {"name": "SN", "addr": 0x05E, "length": 8, "type": "str"},
           {"name": "PCBVER", "addr": 0x064, "length": 2, "type": "str"},
           {"name": "MFDATE", "addr": 0x066, "length": 4, "type": "str"},
           {"name": "ENDUSR", "addr": 0x06A, "length": 2, "type": "str"},
           {"name": "PCA", "addr": 0x06C, "length": 11, "type": "str"},
           {"name": "INITIALCAP", "addr": 0x077, "length": 1, "type": "int"}]


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

        # Switch I2C connection to current PGEM
        # Need call this function every time before communicate with PGEM
        self.switch()

    def switch(self):
        """switch I2C ports by PCA9548A, only 1 channel is enabled.
        chnum(channel number): 0~7
        slotnum(slot number): 0~7
        """
        chnum = self.channel
        slot = self.slot
        self.device.slave_addr = 0x70 + chnum    # 0111 0000
        wdata = [0x01 << slot]
        self.device.write(wdata)

    def _query_map(self, mymap, **kvargs):
        """method to search the map (the list of dict, [{}, {}])
        params: mymap:  the map to search
                kvargs: query conditon key=value, key should be in the dict.
        return: the dict match the query contdtion or None.
        """
        r = mymap
        for k, v in kvargs.items():
            r = filter(lambda row: row[k] == v,  r)
        return r

    def read_VPD_byname(self, reg_name):
        """method to read eep_data according to eep_name
        eep is one dict in eep_map, for example:
        {"name": "CINT", "addr": 0x02B3, "length": 1, "type": "int"}
        """
        eep = self._query_map(EEP_MAP, name=reg_name)[0]
        start = eep["addr"]                 # start_address
        length = eep["length"]              # length
        typ = eep["type"]                   # type
        datas = self.device.read_reg(start, length)
        if(typ == "word"):
            val = datas[0] + (datas[1] << 8)
            return val
        if(typ == "str"):
            return ''.join(chr(i) for i in datas)
        if(typ == "int"):
            return datas[0]

    def read_VPD(self):
        """method to read out EEPROM info from dut
        return a dict.
        """
        self.device.slave_addr = 0x53
        dut = {}
        for eep in EEP_MAP:
            reg_name = eep["name"]
            dut.update({reg_name: self.read_VPD_byname(reg_name)})
        return dut

    def write_VPD(self):
        pass

    def control_LED(self):
        pass

    def self_discharge(self):
        # Controlled by I/O expander IC, address 0x41
        # When IO=0, discharge;
        # When IO=1, not discharge.
        pass

    def encrypted_IC(self):
        pass

    def charge(self):
        pass

    def load_discharge(self):
        pass

    def auto_discharge(self):
        # Controlled by Present I/O
        # When IO=0, discharge;
        # When IO=1, not discharge.
        pass

    def check_power_fail(self):
        pass

    def check_temp(self):
        pass

if __name__ == "__main__":

    from pyaardvark import Adapter
    adk = Adapter()
    adk.open(portnum=0)
    DUT = PGEMBase(device=adk)
    print DUT.read_VPD()
    adk.close()

