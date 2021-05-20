from sqlalchemy import Column, String, Numeric, Integer, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship

from .base import Base

class Participant(Base):
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True)
    gold_left = Column(Integer)
    last_round = Column(Integer)
    level = Column(Integer)
    placement = Column(Integer)
    players_eliminated = Column(Integer)
    time_eliminated = Column(Integer)
    total_damage_to_players = Column(Integer)
    traits = Column(Text)
    champions = Column(Text)
    is_analyzed = Column(Boolean)
    match_id = Column(Integer, ForeignKey('matches.id'))
    #match = relationship('Match', back_populates='participants')

    def __init__(self, 
        gold_left, 
        last_round, 
        level, 
        placement, 
        players_eliminated, 
        time_eliminated, 
        total_damage_to_players, 
        champions, 
        traits,
        match_id,
        is_analyzed = False
        ):
        self.gold_left = gold_left
        self.last_round = last_round
        self.level = level
        self.placement = placement
        self.players_eliminated = players_eliminated
        self.time_eliminated = time_eliminated
        self.total_damage_to_players = total_damage_to_players
        self.champions = champions
        self.traits = traits
        self.match_id = match_id
        self.is_analyzed = is_analyzed