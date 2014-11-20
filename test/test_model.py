#!/usr/bin/env python
# encoding: utf-8
"""description:
"""
__version__ = "0.1"
__author__ = "@boqiling"

from UFT.models import Crystal
from UFT.devices import aardvark


adk = aardvark.Adapter()
crystal = Crystal(device=adk)
