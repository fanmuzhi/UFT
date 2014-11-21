#!/usr/bin/env python
# encoding: utf-8
"""test code for UFT test process
"""
__version__ = "0.1"
__author__ = "@boqiling"

from UFT.models import PGEMBase, DUT_STATUS, DUT, Cycle
from UFT.backend.session import SessionManager
from UFT.devices import pwr
from UFT.devices import load
from UFT.devices import aardvark
from UFT.config import *
import time

# barcode list for test purpose only
barcode_list = ["AGIGA9811-001BCA02143500000001-01",
                "AGIGA9811-001BCA02143500000002-01",
                "AGIGA9811-001BCA02143500000003-01",
                "AGIGA9811-001BCA02143500000004-01"]

bq24704_option = {"charge_option": 0x1990,
                  "charge_current": 0x01C0,
                  "charge_voltage": 0x1200,
                  "input_current": 0x0400}

VCAP_HIGH_THRESHHOLD = 4.6
VCAP_LOW_THRESHHOLD = 0.2

VPD_PATH = r"C:\Users\qibo\Documents\UFT\test\101-40028-01-Rev02 Crystal2 VPD.ebf"

def run():

    # setup load
    ld = load.DCLoad(port=LD_PORT, timeout=LD_DELAY)
    for slot in range(TOTAL_SLOTNUM):
        ld.select_channel(slot)
        ld.input_off()
        ld.protect_on()
        ld.change_func(load.DCLoad.ModeCURR)
        ld.set_curr(0.8)    # discharge current, should be in dut config.

    # setup main power 12V
    ps = pwr.PowerSupply()
    ps.selectChannel(node=PS_ADDR, ch=PS_CHAN)

    setting = {"volt": PS_VOLT, "curr": PS_CURR,
               "ovp": PS_OVP, "ocp": PS_OCP}
    ps.set(setting)
    ps.activateOutput()
    time.sleep(1)
    volt = ps.measureVolt()
    curr = ps.measureCurr()
    assert 11 < volt < 13
    assert curr >= 0

    # aardvark
    adk = aardvark.Adapter()
    adk.open(portnum=ADK_PORT)

    # setup dut_list
    dut_list = []
    for slot in range(TOTAL_SLOTNUM):
        dut = PGEMBase(device=adk, slot=slot, barcode=barcode_list[slot])
        dut.partnumber = "Crystal"
        dut.status = DUT_STATUS.Idle
        dut_list.append(dut)

    # setup database
    sm = SessionManager()
    my_session = sm.get_session(RESULT_DB)
    sm.prepare_db(RESULT_DB, [DUT, Cycle])

    # charging
    #TODO add time out gauge here.

    counter = 0     # counter for whole charging and discharging

    for slot in range(TOTAL_SLOTNUM):
        dut_list[slot].switch()   # to dut
        dut_list[slot].charge(option=bq24704_option, status=True)

    all_charged = False
    while(not all_charged):
        all_charged = True
        for slot in range(TOTAL_SLOTNUM):
            this_cycle = Cycle()
            this_cycle.vin = ps.measureVolt()
            this_cycle.temp = dut_list[slot].check_temp()
            this_cycle.time = counter
            counter += 1

            ld.select_channel(slot)
            this_cycle.vcap = ld.read_volt()

            if(this_cycle.vcap > VCAP_HIGH_THRESHHOLD):
                all_charged &= True
                dut_list[slot].status = DUT_STATUS.Charged
            else:
                all_charged &= False
            dut_list[slot].cycles.append(this_cycle)
        time.sleep(INTERVAL)

    # programming
    for dut in dut_list:
        dut.write_vpd(VPD_PATH)
        dut.read_vpd()

    # discharging
    #TODO add time out gauge here.
    for slot in range(TOTAL_SLOTNUM):
        dut_list[slot].switch()   # to dut
        dut_list[slot].charge(option=bq24704_option, status=False)

        ld.select_channel(slot)
        ld.input_on()

    all_discharged = False
    while(not all_discharged):
        all_discharged = True
        for slot in range(TOTAL_SLOTNUM):
            this_cycle = Cycle()
            this_cycle.vin = ps.measureVolt()
            this_cycle.temp = dut_list[slot].check_temp()
            this_cycle.time = counter
            counter += 1

            ld.select_channel(slot)
            this_cycle.vcap = ld.read_volt()

            if(this_cycle.vcap <= VCAP_LOW_THRESHHOLD):
                all_discharged &= True
                dut_list[slot].status = DUT_STATUS.Discharged
            else:
                all_discharged &= False
            dut_list[slot].cycles.append(this_cycle)
        time.sleep(INTERVAL)

    # save to database
    for dut in dut_list:
        my_session.add(dut)
        my_session.commit()


if __name__ == "__main__":
    run()
