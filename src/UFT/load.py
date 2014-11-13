#!/usr/bin/env python
# encoding: utf-8
"""API program for Agilent N3300A DC electronic Load.
RS232 communication based.
"""
__version__ = "0.0.1"
__author__ = "@boqiling"
__all__ = ["DCLoad"]

import serial
import re
import logging
import time

logger = logging.getLogger(__name__)


class DCLoadException(Exception):
    pass


class DCLoad(object):
    ModeCURR = "CURR"
    ModeVolt = "VOLT"
    ModeRes = "RES"
    DELAY = 0.1

    def __init__(self, port='COM0', baudrate=9600, **kvargs):
        timeout = kvargs.get('timeout', 5)
        parity = kvargs.get('parity', serial.PARITY_NONE)
        bytesize = kvargs.get('bytesize', serial.SEVENBITS)
        stopbits = kvargs.get('stopbits', serial.STOPBITS_ONE)
        self.ser = serial.Serial(port=port, baudrate=baudrate)
        if(not self.ser.isOpen()):
            self.ser.close()
            self.ser.open()

        # check IDN
        self._write("*IDN?")
        idn = self._read()
        if(re.match(r"Agilent\sTechnologies,N3300A", idn)):
            logger.info("DC Load found: " + idn)
        else:
            logger.debug("unknown device found: " + idn)

        # clean error
        self._write("SYST:ERR?")
        errmsg = self._read()
        while(not re.match(r"\+0,\"No\serror\"", errmsg)):
            logger.debug("DC Load Error: " + errmsg)
            self._write("SYST:ERR?")
            errmsg = self._read()

    def __del__(self):
        try:
            self.ser.close()
        except Exception:
            pass

    def _write(self, msg):
        self.ser.write(msg + "\n")

    def _read(self):
        time.sleep(self.DELAY)       # wait for response
        buff = ''
        while(self.ser.inWaiting() > 0):
            buff += self.ser.read(1)
        return buff

    def _check_error(self):
        self._write("SYST:ERR?")
        errmsg = self._read()
        if(not re.match(r"\+0,\"No\serror\"", errmsg)):
            logging.error("DC Load Error: " + errmsg)
            raise DCLoadException(errmsg)

    def select_channel(self, chnum):
        if(chnum in range(1, 5)):
            self._write("CHAN " + str(chnum))
        else:
            raise DCLoadException("Invalid channel number")
        self._check_error()

    def change_func(self, mode):
        if(mode in [self.ModeCURR, self.ModeRes, self.ModeVolt]):
            self._write("FUNC " + mode)
        self._check_error()

    def set_curr(self, curr):
        self._write("CURR:RANG MIN")    # select min range
        self._write("CURR " + str(curr))
        self._check_error()

    def read_curr(self):
        self._write("MEAS:CURR?")
        result = self._read()
        self._check_error()
        return float(result)

    def set_res(self, resistance):
        # 2 Amps and 1 second protection
        self._write("CURR:PROT:LEV 2;DEL 0.1")
        self._write("CURR:PROT:STAT ON")
        self._write("RES " + str(resistance))
        self._check_error()

    def read_volt(self):
        self._write("MEAS:VOLT?")
        result = self._read()
        self._check_error()
        return float(result)

    def input_on(self):
        self._write("INP ON")
        self._check_error()

    def input_off(self):
        self._write("INP OFF")
        self._check_error()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    load = DCLoad(port="COM3", timeout=3)

    load.select_channel(1)
    load.input_off()

    load.change_func(DCLoad.ModeCURR)
    load.set_curr(0.5)

    load.input_on()

    print load.read_curr()
    print load.read_volt()

    print "finish."
