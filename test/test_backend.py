#!/usr/bin/env python
# encoding: utf-8
"""Description:
"""

__version__ = "0.1"
__author__ = "@boqiling"
__all__ = [""]

from UFT.backend import load_config, sync_config
test_uri = "sqlite:///configuration.db"

config = load_config(test_uri, partnumber="AGIGA9601-002BCA", revision="04")
print config

sync_config(test_uri, "./")

