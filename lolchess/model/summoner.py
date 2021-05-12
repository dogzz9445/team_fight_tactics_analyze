from sqlalchemy import Column, String, Numeric, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class Summoner(Base):
    __tablename__ = 'summoners'

    id = Column(Integer, primary_key=True)
    summoner_id = Column(String(65))
    summoner_puuid = Column(String(80))

    def __init__(self, summoner_id, summoner_puuid):
        self.summoner_id = summoner_id
        self.summoner_puuid = summoner_puuid