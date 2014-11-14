#!/usr/bin/env python
# encoding: utf-8
"""test code for UFT test process
"""
__version__ = "0.1"
__author__ = "@boqiling"

from UFT.models import base
from UFT.devices import pwr
from UFT.devices import load
from UFT.devices import aardvark
import time


def main():

    # setup load
    ld = load.DCLoad(port="COM3", timeout=3)
    for ch in range(1, 2):
        ld.select_channel(ch)
        ld.input_off()
        ld.protect_on()
        ld.change_func(load.DCLoad.ModeCURR)
        ld.set_curr(0.8)

    # setup main power 12V
    ps = pwr.PowerSupply()
    ps.selectChannel(node=5, ch=1)

    try:
        setting = {"volt": 12.0, "curr": 2, "ovp": 13.0, "ocp": 3.0}
        ps.set(setting)
        ps.activateOutput()
        time.sleep(1)

        volt = ps.measureVolt()
        curr = ps.measureCurr()

        assert 11 < volt < 13
        assert curr >= 0

        # base
        adk = aardvark.Adapter()
        adk.open(portnum=0)

        crystal1 = base.PGEMBase(device=adk, slot=0)
        crystal1.switch()   # to dut
        crystal1.charge(True)

        v = ld.read_volt()
        while(v < 4.6):
            v = ld.read_volt()
            print v
    except Exception:
        print Exception.args
        print Exception.message
    finally:
        # end, cleanup
        ld.input_on()
        ps.deactivateOutput()


if __name__ == "__main__":
    main()
