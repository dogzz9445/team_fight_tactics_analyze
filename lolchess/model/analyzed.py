from sqlalchemy import Column, String, Numeric, Integer, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

from datetime import datetime

from .base import Base

class Analyzed(Base):
    __tablename__ = 'analyzed'

    id = Column(Integer, primary_key=True)
    version = Column(Integer)
    analyze_period = Column(Integer)
    target_start_date = Column(DateTime)
    target_end_date = Column(DateTime)
    target_date = Column(DateTime)
    json_result = Column(JSON)

    def __init__(self, 
        version: int, 
        analyze_period: int,
        target_start_date: datetime, 
        target_end_date: datetime, 
        target_date: datetime,
        json_result: dict
        ):
        self.version = version
        self.analyze_period = analyze_period
        self.target_start_date = target_start_date
        self.target_end_date = target_end_date
        self.target_date = target_date
        self.json_result = json_result