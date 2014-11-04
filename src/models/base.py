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


class Base(object):

    def __init__(self):
        pass

    def write_VPD(self):
        pass

    def read_VPD(self):
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
