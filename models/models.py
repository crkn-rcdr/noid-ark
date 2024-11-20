from sqlalchemy.orm import declarative_base
from sqlalchemy import Column,Integer

Base = declarative_base()

class Counter(Base):
    __tablename__ = "counter"
    id = Column(Integer,primary_key=True,index=True)
    current = Column(Integer,nullable=False,default=0)