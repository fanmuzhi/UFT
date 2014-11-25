#!/usr/bin/env python
# encoding: utf-8
"""Description:
"""

__version__ = "0.1"
__author__ = "@boqiling"

from UFT.fsm import IFunc, States, StateMachine
from UFT.devices import aardvark
import logging

TestStates = 0xA0


class MainFunc(IFunc):
    def init(self):
        self.device = aardvark.Adapter()
        print "init"

    def idle(self):
        print "idle"

    def work(self, states):
        if(states == TestStates):
            self.device.sleep(5)
            print "work"

    def error(self):
        print "error"

    def exit(self):
        print "exit"

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    m = MainFunc()

    f = StateMachine(m)
    f.en_queue(States.INIT)
    f.run()

    f.en_queue(TestStates)
    f.en_queue(States.EXIT)
