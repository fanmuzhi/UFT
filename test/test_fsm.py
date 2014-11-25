#!/usr/bin/env python
# encoding: utf-8
"""Description:
"""

__version__ = "0.1"
__author__ = "@boqiling"

from UFT.fsm import IFunc, States, StateMachine

class MainFunc(IFunc):
    def init(self):
        print "init"

    def idle(self):
        print "idle"

    def work(self):
        print "work"

    def error(self):
        print "error"

    def exit(self):
        print "exit"

if __name__ == "__main__":
    m = MainFunc()

    f = StateMachine(m)
    f.en_queue(States.INIT)
    f.run()

    f.en_queue(States.EXIT)
