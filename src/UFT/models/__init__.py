#!/usr/bin/env python
# encoding: utf-8
"""description: Cororado PGEM models
"""
__version__ = "0.1"
__author__ = "@fanmuzhi, @boqiling"
__all__ = ["PGEMBase", "DUT", "DUT_STATUS", "Cycle"]

from base import PGEMBase, Diamond4
from dut import DUT, DUT_STATUS, Cycle


class Crystal(PGEMBase):
    pass


class Saphire(PGEMBase):
    PGEM_ID = {"name": "INITIALCAP", "addr": 0x077, "length": 1, "type": "int"}

    def write_pgemid(self):
        # write to VPD
        self.device.slave_addr = 0x53
        #
        self.device.write_reg(i, buffebf[i])
        self.device.sleep(5)


# class Diamond4(PGEMBase):
# """
#     PGEM with LTC3350 Charge IC used instead of BQ24707 class.
#     """
#     def charge(self, status=True, **kvargs):
#         """
#         Charge IC LTC3350 used instead of BQ24707.
#         :param kvargs: option dict of charge option, charge voltage, etc.
#         :param status: status=True, start charge; status=False, stop charge.
#         """
#         BCAPFB_DAC = 0x05
#         VSHUNT = 0x06
#         CTL_REG = 0x17
#         NUM_CAPS = 0x1A
#         CHRG_STATUS = 0x1B
#
#         # check IC
#         logger.debug("LTC3350 Charge IC used instead of BQ24707, unknown ID")
#         if status:
#             self.write_ltc3350(BCAPFB_DAC, 0xF)
#             self.write_ltc3350(VSHUNT, 0x3998)
#         else:
#             # stop charge
#             self.write_ltc3350(VSHUNT, 0x0000)


