#!/usr/bin/env python
# encoding: utf-8
"""Description: test base.check_power_fail function
"""

__version__ = "0.1"
__author__ = "@boqiling"
__all__ = [""]

from UFT.models import base
from UFT.devices.aardvark import pyaardvark

adk = pyaardvark.Adapter()
adk.open(portnum=0)

barcode = "AGIGA9811-001BCA02143500000002-01"
dut = base.PGEMBase(device=adk, barcode=barcode, slot=1)

dut.switch_back()
print dut.check_power_fail()

adk.close()