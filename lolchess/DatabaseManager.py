from sqlalchemy import create_engine, exists
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String

from model.base import Session, Base
from model.match import GameType, Match
from model.participant import Participant

Session = Session
Base = Base
GameType = GameType
Match = Match
Participant = Participant

class DatabaseManager():
    def __init__(self):
        pass

    def __del__(self):
        pass

    def run(self):
        pass
        

if __name__ == '__main__':
    session = Session()
    #   INSERT
    if not session.query(exists().where(GameType.gametype == 'test')).scalar():
        gt = GameType(gametype = 'test')
        session.add(gt)
        session.commit()

    #   SELECT
    # if session.query(exists().where(Address.city == 'City WTF')).scalar():
    #     a2 = session.query(Address).filter_by(city='City WTF').first()
    #     print a2.city

    # if bool(session.query(Address).filter_by(city='City WTF').count()):
    #     a2 = session.query(Address).filter_by(city='City WTF').first()
    #     print a2.city


    # #   UPDATE
    # if session.query(exists().where(User.email == 'test@example.net')).scalar():
    #     session.query(User).filter_by(email='test@example.net').update({"nick": "a"})
    #     session.commit()

    # if session.query(exists().where(User.email == 'test@example.net')).scalar():
    #     u = session.query(User).filter_by(email='test@example.net').first()
    #     u.nick = "b"
    #     session.commit()


    # #   DELETE
    # if session.query(exists().where(User.email == 'test@example.net')).scalar():
    #     session.query(User).filter_by(email='test@example.net').delete()
    #     session.commit()

    if session.query(exists().where(GameType.gametype == 'test')).scalar():
        session.query(GameType).filter_by(gametype='test').delete()
        session.commit()