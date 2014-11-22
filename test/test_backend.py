#!/usr/bin/env python
# encoding: utf-8
"""Description:
"""

__version__ = "0.1"
__author__ = "@boqiling"

from UFT.backend import load_config, sync_config
test_uri = "sqlite:///pgem_config.db"

sync_config(test_uri, "./")

config = load_config(test_uri, partnumber="AGIGA9601-002BCA", revision="04")
for item in config.testitems:
    if(item.name == "Charge"):
        Charge_Option = item
print Charge_Option.max
print Charge_Option.misc
