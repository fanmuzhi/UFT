"""test sqlalchemy orm
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
import datetime
SQLBase = declarative_base()


class DUT_STATUS(object):
    Blank = 0   # empty, not loaded on fixture
    Pass = 1    # pass the test
    Idle = 2    # wait to test
    Fail = 3    # fail in test
    Charging = 4
    Charged = 5
    Discharging = 6
    Discharged = 7


class DUT(SQLBase):
    __tablename__ = "dut"

    id = Column(Integer, primary_key=True)
    barcode = Column(String(30), nullable=False)
    partnumber = Column(String(30), nullable=False)

    temphist = Column(Integer)
    caphist = Column(Integer)
    charger = Column(Integer)
    capacitance = Column(Integer)
    chargevol = Column(Integer)
    chgmaxval = Column(Integer)
    powerdet = Column(Integer)
    chargecur = Column(Integer)
    hwver = Column(String(5))
    cappn = Column(String(20))
    pcbver = Column(String(5))
    sn = Column(String(10))
    mfdate = Column(String(10))
    endusr = Column(String(5))
    pca = Column(String(20))
    initialcap = Column(Integer)

    slotnum = Column(Integer)
    archieved = Column(Integer)   # 0 for running and 1 for archieved.
    status = Column(Integer, nullable=False)
    errormessage = Column(String(20))
    testdate = Column(DateTime, default=datetime.datetime.utcnow)

    #DUT is one to many class refer to Cycles
    cycles = relationship("Cycle")


class Cycle(SQLBase):
    __tablename__ = "cycle"

    id = Column(Integer, primary_key=True)
    temp = Column(Float)
    vin = Column(Float)
    vcap = Column(Float)
    time = Column(Integer)
    dutid = Column(Integer, ForeignKey("dut.id"))


if __name__ == "__main__":
    from UFT.backend.session import SessionManager
    sm = SessionManager()
    session = sm.get_session("sqlite:///pgem.db")
    sm.prepare_db("sqlite:///pgem.db", [DUT, Cycle])

    dut = DUT()
    dut.sn = "888888"
    dut.partnumber = "crystal"
    dut.status = DUT_STATUS.Blank

    session.add(dut)
    session.commit()

    try:
        dut = session.query(DUT).filter(DUT.partnumber == "crystal").first()

        print dut.sn

        #dut.__dict__.update({"sn": "12345", "slotnum": 7})
        d = {"status": DUT_STATUS.Idle, "slotnum": 2}
        for k, v in d.items():
            setattr(dut, k, v)

        cycle = Cycle()
        c = {"vin": 47, "vcap": 43, "temp": 20}
        for k, v in c.items():
            setattr(cycle, k, v)
        dut.cycles.append(cycle)

        session.commit()
    except Exception as e:
        print e
        session.rollback()
