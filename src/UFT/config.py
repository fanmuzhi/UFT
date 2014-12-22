#!/usr/bin/env python
# encoding: utf-8
"""Description: Configuration for UFT program.
"""

__version__ = "0.1"
__author__ = "@boqiling"

# total slot number for one channel,
# should be 4, 1 for debug
TOTAL_SLOTNUM = 4

# seconds to delay in charging and discharging,
# increase value to reduce the data in database.
# more data, more accurate test result.
INTERVAL = 2

# DUT will discharge to start voltage before testing
START_VOLT = 1.0

# power supply settings
# node address and channel
PS_ADDR = 5
PS_CHAN = 1
# output
PS_VOLT = 12.0
PS_OVP = 13.0
PS_CURR = 2.0
PS_OCP = 3.0

# aardvark settings
# port number
ADK_PORT = 0

# load Settings
# load RS232 port
LD_PORT = "COM5"
LD_DELAY = 3

# self discharge counter
SD_COUNTER = 10

# database settings
# database for dut test result
#RESULT_DB = "sqlite:////home/qibo/pyprojects/UFT/test/pgem.db"
#RESULT_DB = "sqlite:///C:\\UFT\\db\\pgem.db"
RESULT_DB = "C:\\UFT\\db\\pgem.db"
# database for dut configuration
#CONFIG_DB = "sqlite:////home/qibo/pyprojects/UFT/test/pgem_config.db"
#CONFIG_DB = "sqlite:///C:\\UFT\\db\\pgem_config.db"
CONFIG_DB = "C:\\UFT\\db\\pgem_config.db"

# Location to save xml log
RESULT_LOG = "C:\\UFT\\logs\\"
