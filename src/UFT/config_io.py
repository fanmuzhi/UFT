#!/usr/bin/env python
# encoding: utf-8
"""Description: sync the configuration db with single xml files.
load configuration from xml file, insert to db.
or load configuration from db, save to xml file.
"""

__version__ = "0.1"
__author__ = "@boqiling"
__all__ = [""]

from simplexml import loads, dumps

def save_config(config, filepath):
    result = dumps(config, "entity")
    print result
    with open(filepath, "wb") as f:
        f.truncate()
        f.write(result)


def load_config(filepath):
    with open(filepath) as f:
        result = loads(f.read())
        print result


if __name__ == "__main__":
    from configuration import Configuration, TestItem

    # Insert Example
    CrystalConfig = Configuration()
    CrystalConfig.PARTNUMBER = "AGIGA9601-002BCA"
    CrystalConfig.DESCRIPTION = "Crystal"
    CrystalConfig.REVISION = "04"

    CheckTemp = TestItem()
    CheckTemp.NAME = "Check_Temp"
    CheckTemp.DESCRIPTION = "Check Temperature on chip SE97BTP, data in degree"
    CheckTemp.ENABLE = True
    CheckTemp.MIN = 5.0
    CheckTemp.MAX = 30.0
    CheckTemp.STOPONFAIL = False

    Charge = TestItem()
    Charge.NAME = "Charge"
    Charge.DESCRIPTION = "Charge DUT with BQ24707, limition in seconds"
    Charge.ENABLE = True
    Charge.MIN = 30.0
    Charge.MAX = 120.0
    Charge.STOPONFAIL = True

    CrystalConfig.TESTITEMS.append(CheckTemp)
    CrystalConfig.TESTITEMS.append(Charge)

    save_config(CrystalConfig.to_dict(), "./crystal.xml")
    load_config("./crystal.xml")
