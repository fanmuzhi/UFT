#!/usr/bin/env python
# encoding: utf-8
"""Description: pgem parallel test on UFT test fixture.
Currently supports 4 duts in parallel.
"""

__version__ = "0.1"
__author__ = "@boqiling"
__all__ = ["Channel", "ChannelStates"]

from UFT.fsm import IFunc, StateMachine, States
from UFT.devices import pwr, load, multimeter, aardvark
from UFT.models import DUT_STATUS
from UFT.backend import load_config, load_test_item
from UFT.backend.session import SessionManager
from UFT.config import *
import logging
import time
logger = logging.getLogger(__name__)


def get_sensor_status(self):
    """
    get sensor status of each DUT present.
    :return: list of 1 and 0, 1 for present, 0 for not.
    """
    return [1, 0, 0, 0]


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
    def __init__(self, channel_id=0):
        """
        :param channel: channel ID, from 0 to 7
        :return: None
        """
        # channel number for mother board.
        # 8 mother boards can be stacked from 0 to 7.
        # use 1 motherboard in default.
        self.channel = channel_id

        # aardvark
        self.adk = aardvark.Adapter()
        self.adk.open(portnum=ADK_PORT)

        # setup dut_list
        self.dut_list = []
        self.config_list = []

        # setup load
        self.ld = load.DCLoad(port=LD_PORT, timeout=LD_DELAY)

        # setup main power supply
        self.ps = pwr.PowerSupply()

        # setup database
        # db should be prepared in cli.py
        self.session = SessionManager().get_session(RESULT_DB)

        # progress bar, 0 to 100
        self.progressbar = 0

        super(Channel, self).__init__()

    def init(self, barcode_list):
        # setup dut_list
        for s in get_sensor_status():
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
        time.sleep(1)
        volt = self.ps.measureVolt()
        curr = self.ps.measureCurr()
        assert (PS_VOLT-1) < volt < (PS_VOLT+1)
        assert curr >= 0

        # clear progress bar
        self.progressbar = 0

    def idle(self):
        pass

    def work(self):
        pass

    def error(self):
        pass

    def exit(self):
        pass

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

        self.device.slave_addr = 0x20 + chnum
        REG_INPUT = 0x00
        REG_OUTPUT = 0x02
        REG_CONFIG = 0x06

        # config PIO-0 to output and PIO-1 to input
        # first PIO-0 then PIO-1
        wdata = [REG_CONFIG, 0x00, 0xFF]
        self.device.write(wdata)

        # read current status
        val = self.device.read_reg(REG_INPUT, length=2)
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
        self.device.write(wdata)

        # read status back
        val = self.device.read_reg(REG_INPUT, length=2)
        val = val[0]    # only need port 0 value
        val = (val & (0x01 << slot)) >> slot
        assert val == IO

    def switch_to_dut(self, slot):
        """switch I2C ports by PCA9548A, only 1 channel is enabled.
        chnum(channel number): 0~7
        slotnum(slot number): 0~7
        """
        chnum = self.channel
        self.device.slave_addr = 0x70 + chnum    # 0111 0000
        wdata = [0x01 << slot]

        # Switch I2C connection to current PGEM
        # Need call this function every time before communicate with PGEM
        self.device.write(wdata)

    def switch_to_mb(self):
        """switch I2C ports back to mother board
           chnum(channel number): 0~7
        """
        chnum = self.channel
        self.device.slave_addr = 0x70 + chnum    # 0111 0000
        wdata = 0x00

        # Switch I2C connection to mother board
        # Need call this function every time before communicate with
        # mother board
        self.device.write(wdata)

    def check_power_fail(self, slot):
        """check power_fail_int signal on TCA9555 on mother board
        return true if power failed.
        """
        chnum = self.channel

        self.device.slave_addr = 0x20 + chnum
        REG_INPUT = 0x00
        #REG_OUTPUT = 0x02
        REG_CONFIG = 0x06

        # config PIO-0 to output and PIO-1 to input
        # first PIO-0 then PIO-1
        wdata = [REG_CONFIG, 0x00, 0xFF]
        self.device.write(wdata)

        # read reg_input
        val = self.device.read_reg(REG_INPUT, length=2)
        val = val[1]    # only need port 1 value

        # check current slot
        val = (val & (0x01 << slot)) >> slot
        return val != 0


if __name__ == "__main__":
    channel = Channel()
    f = StateMachine(channel)
    f.en_queue(ChannelStates.INIT)
    f.run()
