#!/usr/bin/env python
# encoding: utf-8
"""Description: pgem parallel test on UFT test fixture.
Currently supports 4 duts in parallel.
"""

__version__ = "0.1"
__author__ = "@boqiling"
__all__ = ["Channel"]

from UFT.fsm import IFunc, StateMachine, States
from UFT.devices import pwr, load, multimeter, aardvark
from UFT.models import DUT_STATUS
from UFT.backend import load_config, load_test_item
from UFT.config import *
import logging
logger = logging.getLogger(__name__)


class ChannelStates(States):
    HARDWARE_INIT = 0x0A
    POWER_ON = 0x0B
    LOAD_DISCHARGE = 0x0C
    CHECK_POWER_FAIL = 0x0D
    CHARGE = 0x0E
    PROGRAM_VPD = 0x0F
    CHECK_LED = 0x1A
    CHECK_ENCRYPTED_IC = 0x1B
    CHECK_TEMP = 0x1C
    AUTO_DISCHARGE = 0x1D
    SELF_DISCHARGE = 0x1E
    LOAD_DISCHARGE = 0x1F


class Channel(IFunc):
    def __init__(self, barcode_list):
        """
        :param barcode_list: barcode list, if no dut, barcode = ""
        :return: None
        """
        # aardvark
        self.adk = aardvark.Adapter()
        self.adk.open(portnum=ADK_PORT)

        # setup dut_list
        self.dut_list = []
        self.config_list = []
        for s in self.get_dut_sensor():
            i = 0
            if s:
                # dut is present
                dut = PGEM_MODEL(device=self.adk,
                                 slot=i,
                                 barcode=barcode_list[i])
                dut.status = DUT_STATUS.Idle
                self.dut_list.append(dut)

                dut_config = load_config(CONFIG_DB,
                                         dut.partnumber, dut.revision)
                self.config_list.append(dut_config)
            else:
                # dut is not loaded on fixture
                self.dut_list.append(None)
                self.config_list.append(None)
            i += 1

        # setup load

        # setup main power supply

        # setup database


        super(Channel, self).__init__()
        pass

    def init(self):
        pass

    def idle(self):
        pass

    def work(self):
        pass

    def error(self):
        pass

    def exit(self):
        pass

    def get_dut_sensor(self):
        """
        get sensor status of each DUT present.
        :return: list of 1 and 0, 1 for present, 0 for not.
        """
        return [1, 0, 0, 0]


if __name__ == "__main__":
    channel = Channel()
    f = StateMachine(channel)
    f.en_queue(ChannelStates.INIT)
    f.run()
