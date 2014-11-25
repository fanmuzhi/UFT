#!/usr/bin/env python
# encoding: utf-8
"""event-driven state machine
2014.11, changed from multiprocessing to threading.
got Ctype pointer issue in pickle using multiprocessing
"""
#from multiprocessing import Process, Queue, Value
from exceptions import NotImplementedError
import threading
from Queue import Queue


class States(object):
    INIT = 0
    IDLE = 1
    WORK = 2
    ERROR = 3
    EXIT = 4


class IFunc(object):
    """Interface Class for functions in different states.
    """
    def __init__(self):
        self.queue = Queue()

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


class StateMachine(object):
    """finite state machine class
    """
    def __init__(self, ifunc):
        self.mf = ifunc
        self.q = ifunc.queue
        #self.status = Value('d', 0)
        self.status = 0
        self.is_alive = True

    def en_queue(self, state):
        self.q.put(state)

    def run(self):
        #p = Process(target=self.loop, args=(self.status, ))
        #p.start()
        t = threading.Thread(target=self.loop, args=(self.status,))
        t.start()

    def quit(self):
        self.q.put(States.EXIT)
        self.is_alive = False

    def loop(self, s):
        while(self.is_alive):
            #s.value = self.q.get()
            s = self.q.get()
            if(s == States.INIT):
                self.mf.init()
            elif(s == States.IDLE):
                self.mf.idle()
            elif(s == States.ERROR):
                self.mf.error()
            elif(s == States.EXIT):
                self.mf.exit()
                self.is_alive = False
            else:
                self.mf.work(s)
