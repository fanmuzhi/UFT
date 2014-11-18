#!/usr/bin/env python
# encoding: utf-8
"""PGEM test configuration model.
Default connect to configuration.db which save the test items settings.
"""

__version__ = "0.1"
__author__ = "@boqiling"
__all__ = ["Configuration", "TestItem"]

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

SQLBase = declarative_base()


class Configuration(SQLBase):
    __tablename__ = "configuration"

    ID = Column(Integer, primary_key=True)
    PARTNUMBER = Column(String(20), nullable=False)
    DESCRIPTION = Column(String(50))
    REVISION = Column(String(5), nullable=False)

    TESTITEMS = relationship("TestItem", backref="configuration")

    def to_dict(self):
        items_list = []
        for items in self.TESTITEMS:
            items_list.append(items.to_dict())
        return {"PARTNUMBER": self.PARTNUMBER,
                "DESCRIPTION": self.DESCRIPTION,
                "REVISION": self.REVISION,
                "TESTITEMS": items_list}


class TestItem(SQLBase):
    __tablename__ = "test_item"

    ID = Column(Integer, primary_key=True)
    CONFIGID = Column(Integer, ForeignKey("configuration.ID", ondelete="CASCADE"))

    NAME = Column(String(10), unique=True, nullable=False)
    DESCRIPTION = Column(String(30))
    ENABLE = Column(Boolean, nullable=False)
    MIN = Column(Float)
    MAX = Column(Float)
    STOPONFAIL = Column(Boolean, default=True)
    MISC = Column(String(50))

    def to_dict(self):
        return {"NAME": self.NAME,
                "DESCRIPTION": self.DESCRIPTION,
                "ENABLE": self.ENABLE,
                "MIN": self.MIN,
                "MAX": self.MAX,
                "STOPONFAIL": self.STOPONFAIL,
                "MISC": self.MISC}


if __name__ == "__main__":
    from session import SessionManager
    dburi = "sqlite:///configuration.db"
    sm = SessionManager()
    session = sm.get_session(dburi)
    sm.prepare_db(dburi, [Configuration, TestItem])

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

    try:
        CrystalConfig.TESTITEMS.append(CheckTemp)
        CrystalConfig.TESTITEMS.append(Charge)
        session.add(CrystalConfig)
        session.commit()
    except Exception as e:
        print e
        session.rollback()

    # Query Example
    crystal = session.query(Configuration).filter(
        Configuration.PARTNUMBER == "AGIGA9601-002BCA",
        Configuration.REVISION == "04").first()
    for testitem in crystal.TESTITEMS:
        if testitem.NAME == "Charge":
            print testitem.NAME
            print testitem.DESCRIPTION
            print testitem.MAX

    print crystal.to_dict()
