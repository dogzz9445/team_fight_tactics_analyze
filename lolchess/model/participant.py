from sqlalchemy import Column, String, Numeric, Integer, ForeignKey

from .base import Base

class Participant(Base):
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('matches.id'))
    gold_left = Column(Integer)
    last_round = Column(Integer)
    level = Column(Integer)
    placement = Column(Integer)
    players_eliminated = Column(Integer)
    time_eliminated = Column(Integer)
    total_damage_to_players = Column(Integer)
    champions = Column(String)
    traits = Column(String)

    def __init__(self, model, number, owner):
        self.model = model
        self.number = number
        self.owner = owner