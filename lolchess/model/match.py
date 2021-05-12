from sqlalchemy import Column, String, Numeric, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

import datetime

class GameType(Base):
    __tablename__ = 'gametype'

    id = Column(Integer, primary_key=True)
    gametype = Column(String(15))

    def __init(self, gametype):
        self.gametype = gametype

class Match(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    match_region = Column(Integer)
    match_str = Column(Integer)
    setnumber = Column(Integer)
    matched_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    gametype_id = Column(Integer, ForeignKey('gametype.id'))
    #gametype = relationship('GameType', back_populates='Match')

    def __init__(self, match_region, match_str, setnumber, matched_at, gametpye_id):
        self.match_region = match_region
        self.match_str = match_str
        self.setnumber = setnumber
        self.matched_at = datetime.datetime.utcfromtimestamp(matched_at / 1000)
        self.gametpye_id = gametpye_id