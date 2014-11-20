#!/usr/bin/env python
# encoding: utf-8
"""Description: pgem parallel test on UFT test fixture.
Currently supports 4 duts in parallel.
"""

__version__ = "0.1"
__author__ = "@boqiling"
__all__ = ["ChannelFunc"]

from UFT.fsm import IFunc, StateMachine, States
from UFT import models
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


class ChannelFunc(IFunc):
    def __init__(self, mode=models.PGEMBase):
        super(ChannelFunc, self).__init__()
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


if __name__ == "__main__":
    channel = ChannelFunc()
    f = StateMachine(channel)
    f.en_queue(ChannelStates.INIT)
    f.run()
