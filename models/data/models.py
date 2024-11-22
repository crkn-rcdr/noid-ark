from sqlalchemy.orm import declarative_base
from sqlalchemy import Column,Integer,String,DateTime,func

Base = declarative_base()

class Counter(Base):
    __tablename__ = "counter"

    id = Column(Integer,primary_key=True,index=True)
    current = Column(Integer,nullable=False,default=0)

class Noid(Base):
    __tablename__ = "noid"

    noid = Column(String,primary_key=True)
    schema_ = Column(String,nullable=False,comment="Scheme prefix for the NOID, e.g., 'ark:/'")
    naan = Column(String,nullable=False,comment="NAAN (Name Assigning Authority Number) for the NOID")
    create_time = Column(DateTime,server_default=func.now(),comment="Time when the NOID was created")
