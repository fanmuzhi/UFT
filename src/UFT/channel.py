#!/usr/bin/env python
# encoding: utf-8
"""Description: pgem parallel test on UFT test fixture.
Currently supports 4 duts in parallel.
"""

__version__ = "0.1"
__author__ = "@boqiling"
__all__ = ["Channel", "ChannelStates"]

from UFT.devices import pwr, load, aardvark
from UFT.models import DUT_STATUS, DUT, Cycle
from UFT.backend import load_config, load_test_item
from UFT.backend.session import SessionManager
from UFT.config import *
import threading
from Queue import Queue
import logging
import time
logger = logging.getLogger(__name__)


def get_sensor_status():
    """
    get sensor status of each DUT present.
    :return: list of 1 and 0, 1 for present, 0 for not.
    """
    #TODO
    return [1, 0, 0, 0]


class ChannelStates(object):
    EXIT = -1
    INIT = 0x0A
    POWER_ON = 0x0B
    LOAD_DISCHARGE = 0x0C
    CHARGE = 0x0E
    PROGRAM_VPD = 0x0F
    CHECK_LED = 0x1A
    CHECK_ENCRYPTED_IC = 0x1B
    CHECK_TEMP = 0x1C
    AUTO_DISCHARGE = 0x1D
    SELF_DISCHARGE = 0x1E


class Channel(threading.Thread):
    def __init__(self, name, barcode_list, channel_id=0):
        """initialize channel
        :param name: thread name
        :param barcode_list: list of 2D barcode of dut.
        :param channel_id: channel ID, from 0 to 7
        :return: None
        """
        # channel number for mother board.
        # 8 mother boards can be stacked from 0 to 7.
        # use 1 motherboard in default.
        self.channel = channel_id

        # aardvark
        self.adk = aardvark.Adapter()

        # setup dut_list
        self.dut_list = []
        self.config_list = []
        self.barcode_list = barcode_list

        # setup load
        self.ld = load.DCLoad(port=LD_PORT, timeout=LD_DELAY)

        # setup main power supply
        self.ps = pwr.PowerSupply()

        # setup database
        # db should be prepared in cli.py
        sm = SessionManager()
        sm.prepare_db(RESULT_DB, [DUT, Cycle])
        self.session = sm.get_session(RESULT_DB)

        # progress bar, 0 to 100
        self.progressbar = 0

        # counter, to calculate charge and discharge time based on interval
        self.counter = 0

        # discharge current, default to 0.5A
        self.current = 0.5

        # exit flag and queue for threading
        self.exit = False
        self.queue = Queue()

        super(Channel, self).__init__(name=name)

    def init(self):
        # open aardvark
        self.adk.open(portnum=ADK_PORT)

        # setup dut_list
        for s in get_sensor_status():
            i = 0
            if s:
                # dut is present
                dut = PGEM_MODEL(device=self.adk,
                                 slot=i,
                                 barcode=self.barcode_list[i])
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
        for slot in range(TOTAL_SLOTNUM):
            self.ld.select_channel(slot)
            self.ld.input_off()
            self.ld.protect_on()
            self.ld.change_func(load.DCLoad.ModeCURR)

        # setup power supply
        self.ps.selectChannel(node=PS_ADDR, ch=PS_CHAN)

        setting = {"volt": PS_VOLT, "curr": PS_CURR,
                   "ovp": PS_OVP, "ocp": PS_OCP}
        self.ps.set(setting)
        self.ps.activateOutput()
        time.sleep(1.5)
        volt = self.ps.measureVolt()
        curr = self.ps.measureCurr()
        assert (PS_VOLT-1) < volt < (PS_VOLT+1)
        assert curr >= 0

        # reset DUT
        self.reset_dut()

        # clear progress bar
        self.progressbar = 0

    def reset_dut(self):
        """disable all charge and self-discharge, enable auto-discharge.
        just like the dut is not present.
        :return: None
        """
        for dut in self.dut_list:
            if dut is not None:
                self.switch_to_dut(dut.slotnum)
                try:
                    # disable self discharge
                    dut.self_discharge(status=False)
                except:
                    #maybe dut has no power, doesn't response
                    pass

                # disable charge
                charge_config = load_test_item(self.config_list[dut.slotnum],
                                               "Charge")
                dut.charge(charge_config, status=False)

                # enable auto discharge
                self.switch_to_mb()
                self.auto_discharge(slot=dut.slotnum, status=True)

                # empty the dut, one by one
                self.ld.select_channel(dut.slotnum)
                val = self.ld.read_volt()
                if(val > 0.2):
                    self.ld.set_curr(0.5)
                    self.ld.input_on()
                while(val > 0.2):
                    val = self.ld.read_volt()
                    time.sleep(INTERVAL)
                self.ld.input_off()

                self.switch_to_mb()
                if(not self.check_power_fail(dut.slotnum)):
                    dut.status = DUT_STATUS.Fail
                    dut.errormessage = "Power Int Test Fail"

    def charge_dut(self):
        """charge
        """
        for dut in self.dut_list:
            if dut is None:
                continue
            if dut.status != DUT_STATUS.Idle:
                continue
            # disable auto discharge
            self.switch_to_mb()
            self.auto_discharge(slot=dut.slotnum, status=False)
            self.switch_to_dut(dut.slotnum)
            try:
                # disable self discharge
                dut.self_discharge(status=False)
            except:
                #maybe dut has no power, doesn't response
                pass
            # start charge
            charge_config = load_test_item(self.config_list[dut.slotnum],
                                           "Charge")
            dut.charge(option=charge_config, status=True)
            dut.status = DUT_STATUS.Charging

        all_charged = False
        while(not all_charged):
            all_charged = True
            for dut in self.dut_list:
                if dut is None:
                    continue
                if dut.status != DUT_STATUS.Charging:
                    continue
                charge_config = load_test_item(self.config_list[dut.slotnum],
                                               "Charge")
                this_cycle = Cycle()
                this_cycle.vin = self.ps.measureVolt()
                this_cycle.time = self.counter
                try:
                    temperature = dut.check_temp()
                except aardvark.USBI2CAdapterException:
                    # temp ic not ready
                    temperature = 0
                this_cycle.temp = temperature
                this_cycle.state = "charge"
                self.counter += 1

                self.ld.select_channel(dut.slotnum)
                this_cycle.vcap = self.ld.read_volt()

                threshold = float(charge_config["Threshold"].strip("aAvV"))
                max_chargetime = charge_config["max"]
                min_chargetime = charge_config["min"]

                if(this_cycle.vcap > threshold):
                    all_charged &= True
                    if((self.counter * INTERVAL) < min_chargetime):
                        dut.status = DUT_STATUS.Fail
                        dut.errormessage = "Charge Time Too Short."
                    else:
                        dut.status = DUT_STATUS.Idle
                    dut.charge(option=charge_config, status=False)
                elif((self.counter * INTERVAL) > max_chargetime):
                    all_charged &= True
                    dut.status = DUT_STATUS.Fail
                    dut.errormessage = "Charge Time Too Long."
                    dut.charge(option=charge_config, status=False)
                else:
                    all_charged &= False
                dut.cycles.append(this_cycle)
                logger.info("dut: {0} status: {1} message: {2}".format(
                    dut.slotnum, dut.status, dut.errormessage))
            time.sleep(INTERVAL)

    def discharge_dut(self):
        """discharge
        """
        for dut in self.dut_list:
            if dut is None:
                continue
            if dut.status != DUT_STATUS.Idle:
                continue
            # disable auto discharge
            self.switch_to_mb()
            self.auto_discharge(slot=dut.slotnum, status=False)
            # disable self discharge
            self.switch_to_dut(dut.slotnum)
            dut.self_discharge(status=False)
            # disable charge
            charge_config = load_test_item(self.config_list[dut.slotnum],
                                           "Charge")
            dut.charge(option=charge_config, status=False)

            self.ld.select_channel(dut.slotnum)

            discharge_config = load_test_item(self.config_list[dut.slotnum],
                                              "Discharge")

            self.current = float(discharge_config["Current"].strip("aAvV"))
            self.ld.set_curr(self.current)  # set discharge current
            self.ld.input_on()

            dut.status = DUT_STATUS.Discharging

        all_discharged = False
        while(not all_discharged):
            all_discharged = True
            for dut in self.dut_list:
                if dut is None:
                    continue
                if dut.status != DUT_STATUS.Discharging:
                    continue

                this_cycle = Cycle()
                this_cycle.vin = self.ps.measureVolt()
                try:
                    temperature = dut.check_temp()
                except aardvark.USBI2CAdapterException:
                    # temp ic not ready
                    temperature = 0
                this_cycle.temp = temperature
                this_cycle.time = self.counter
                this_cycle.state = "discharge"
                self.counter += 1

                self.ld.select_channel(dut.slotnum)
                this_cycle.vcap = self.ld.read_volt()

                threshold = float(discharge_config["Threshold"].strip("aAvV"))
                max_dischargetime = discharge_config["max"]
                min_dischargetime = discharge_config["min"]

                if(this_cycle.vcap < threshold):
                    all_discharged &= True
                    if((self.counter * INTERVAL) < min_dischargetime):
                        dut.status = DUT_STATUS.Fail
                        dut.errormessage = "Discharge Time Too Short."
                    else:
                        dut.status = DUT_STATUS.Idle
                elif((self.counter * INTERVAL) > max_dischargetime):
                    all_discharged &= True
                    dut.status = DUT_STATUS.Fail
                    dut.errormessage = "Discharge Time Too Long."
                else:
                    all_discharged &= False
                dut.cycles.append(this_cycle)
                logger.info("dut: {0} status: {1} message: {2}".format(
                    dut.slotnum, dut.status, dut.errormessage))
            time.sleep(INTERVAL)
        self.calculate_capacitance()

    def calculate_capacitance(self):
        for dut in self.dut_list:
            if dut is None:
                continue
            cap_list = []
            pre_vcap, pre_time = None, None
            for cycle in dut.cycles:
                if cycle.state == "discharge":
                    if pre_vcap is None:
                        pre_vcap = cycle.vcap
                        pre_time = cycle.time
                    else:
                        cur_vcap = cycle.vcap
                        cur_time = cycle.time
                        cap = (self.current * (cur_time - pre_time) *
                               INTERVAL) / (pre_vcap - cur_vcap)
                        cap_list.append(cap)
            print cap_list
            capacitor = sum(cap_list) / float(len(cap_list))
            dut.capacitance_measured = capacitor

    def auto_discharge(self, slot, status=False):
        """output PRESENT/AUTO_DISCH signal on TCA9555 on mother board.
           When status=True, discharge;
           When status=False, not discharge.
        """
        if(status):
            IO = 0
        else:
            IO = 1

        chnum = self.channel

        self.adk.slave_addr = 0x20 + chnum
        REG_INPUT = 0x00
        REG_OUTPUT = 0x02
        REG_CONFIG = 0x06

        # config PIO-0 to output and PIO-1 to input
        # first PIO-0 then PIO-1
        wdata = [REG_CONFIG, 0x00, 0xFF]
        self.adk.write(wdata)

        # read current status
        val = self.adk.read_reg(REG_INPUT, length=2)
        val = val[0]    # only need port 0 value

        # set current slot
        if(IO == 1):
            # set bit
            val |= (IO << slot)
        else:
            # clear bit
            val &= ~(0X01 << slot)

        # output
        # first PIO-0, then PIO-1
        wdata = [REG_OUTPUT, val, 0xFF]
        self.adk.write(wdata)

        # read status back
        val = self.adk.read_reg(REG_INPUT, length=2)
        val = val[0]    # only need port 0 value
        val = (val & (0x01 << slot)) >> slot
        assert val == IO

    def switch_to_dut(self, slot):
        """switch I2C ports by PCA9548A, only 1 channel is enabled.
        chnum(channel number): 0~7
        slotnum(slot number): 0~7
        """
        chnum = self.channel
        self.adk.slave_addr = 0x70 + chnum    # 0111 0000
        wdata = [0x01 << slot]

        # Switch I2C connection to current PGEM
        # Need call this function every time before communicate with PGEM
        self.adk.write(wdata)

    def switch_to_mb(self):
        """switch I2C ports back to mother board
           chnum(channel number): 0~7
        """
        chnum = self.channel
        self.adk.slave_addr = 0x70 + chnum    # 0111 0000
        wdata = 0x00

        # Switch I2C connection to mother board
        # Need call this function every time before communicate with
        # mother board
        self.adk.write(wdata)

    def check_power_fail(self, slot):
        """check power_fail_int signal on TCA9555 on mother board
        return true if power failed.
        """
        chnum = self.channel

        self.adk.slave_addr = 0x20 + chnum
        REG_INPUT = 0x00
        #REG_OUTPUT = 0x02
        REG_CONFIG = 0x06

        # config PIO-0 to output and PIO-1 to input
        # first PIO-0 then PIO-1
        wdata = [REG_CONFIG, 0x00, 0xFF]
        self.adk.write(wdata)

        # read reg_input
        val = self.adk.read_reg(REG_INPUT, length=2)
        val = val[1]    # only need port 1 value

        # check current slot
        val = (val & (0x01 << slot)) >> slot
        return val != 0

    def program_dut(self):
        for dut in self.dut_list:
            if dut is None:
                continue
            program_config = load_test_item(self.config_list[dut.slotnum],
                                            "Program_VPD")
            # power should be OK.
            self.switch_to_mb()
            if(self.check_power_fail(dut.slotnum)):
                dut.status = DUT_STATUS.Fail
                dut.errormessage = "Power Int Test Fail"

            self.switch_to_dut(dut.slotnum)
            try:
                dut.write_vpd(program_config["File"])
                dut.read_vpd()
            except AssertionError:
                dut.status = DUT_STATUS.Fail
                dut.errormessage = "Programming VPD Fail"

    def check_encryptedic_dut(self):
        for dut in self.dut_list:
            if dut is None:
                continue
            if(not dut.encrypted_ic()):
                dut.status = DUT_STATUS.Fail
                dut.errormessage = "Check I2C on Encrypted IC Fail."

    def prepare_to_exit(self):
        """
        cleanup and save to database before exit.
        :return: None
        """
        for dut in self.dut_list:
            if dut is None:
                continue
            if(dut.status == DUT_STATUS.Idle):
                dut.status = DUT_STATUS.Pass

            for pre_dut in self.session.query(DUT).filter(
                            DUT.barcode == dut.barcode).all():
                pre_dut.archived = 1
                self.session.add(pre_dut)
                self.session.commit()
            dut.archived = 0
            self.session.add(dut)
            self.session.commit()

    def run(self):
        """ override thread.run()
        :return: None
        """
        while(not self.exit):
            state = self.queue.get()
            if(state == ChannelStates.EXIT):
                self.prepare_to_exit()
                self.exit = True
            elif(state == ChannelStates.INIT):
                self.progressbar += 10
                self.init()
            elif(state == ChannelStates.CHARGE):
                self.progressbar += 30
                self.charge_dut()
            elif(state == ChannelStates.LOAD_DISCHARGE):
                self.progressbar += 30
                self.discharge_dut()
            elif(state == ChannelStates.AUTO_DISCHARGE):
                pass
            elif(state == ChannelStates.SELF_DISCHARGE):
                pass
            elif(state == ChannelStates.PROGRAM_VPD):
                self.progressbar += 10
                self.program_dut()
            elif(state == ChannelStates.CHECK_ENCRYPTED_IC):
                self.progressbar += 10
                self.check_encryptedic_dut()
            elif(state == ChannelStates.CHECK_LED):
                pass
            else:
                logging.debug("unknown dut state, exit...")
                self.queue.put(ChannelStates.EXIT)

    def empty(self):
        for i in range(self.queue.qsize()):
            self.queue.get()

    def error(self):
        pass

    def quit(self):
        self.empty()
        self.queue.put(ChannelStates.EXIT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)    # quiet

    barcode = "AGIGA9601-002BCA02143500000002-04"
    ch = Channel(barcode_list=[barcode, "", "", ""], channel_id=0,
                 name="UFT_CHANNEL")
    ch.start()

    ch.queue.put(ChannelStates.INIT)
    ch.queue.put(ChannelStates.CHARGE)
    ch.queue.put(ChannelStates.PROGRAM_VPD)
    ch.queue.put(ChannelStates.CHECK_ENCRYPTED_IC)
    ch.queue.put(ChannelStates.LOAD_DISCHARGE)
    ch.queue.put(ChannelStates.EXIT)

    while(ch.is_alive()):
        print "progress bar: {0}".format(ch.progressbar)
        time.sleep(5)
