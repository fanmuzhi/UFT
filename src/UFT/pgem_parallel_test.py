#!/usr/bin/env python
# encoding: utf-8
"""Description: pgem parallel test on UFT test fixture. Currently supports 4 duts in parallel.
"""

__version__ = "0.1"
__author__ = "@boqiling"
__all__ = [""]

from UFT.fsm import IFunc, StateMachine, States
from UFT import models
import logging


class PGEMStates(States):
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


class PGEMFunc(IFunc):
    def __init__(self, mode=models.PGEMBase):
        pass

    def init(self):
        raise NotImplementedError

    def idle(self):
        raise NotImplementedError

    def work(self):
        raise NotImplementedError

    def error(self):
        raise NotImplementedError

    def exit(self):
        raise NotImplementedError

    def empty(self):
        for i in range(self.queue.qsize()):
            self.queue.get()
