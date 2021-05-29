from sqlalchemy import create_engine, exists
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

from .model.base import Base
from .model.summoner import Summoner
from .model.match import GameType, Match
from .model.participant import Participant

from .secret import *

mysql_engine = create_engine('mysql+pymysql://dmjang:'+MYSQL_PASSWORD+'@tzfamily.duckdns.org:33306/lolchess', pool_pre_ping=True)
mysql_session = scoped_session(sessionmaker(bind=mysql_engine))

postgres_engine = create_engine('postgresql://postgres:'+POSTGRES_PASSWORD+'@database-tft.ce5q9qmucrjo.ap-northeast-2.rds.amazonaws.com:5432/postgres', pool_pre_ping=True)
postgres_session = scoped_session(sessionmaker(bind=postgres_engine))

class DatabaseManager():
    def __init__(self):
        self.session = mysql_session

    def __del__(self):
        pass

    def commit(self):
        self.session.commit()

    def run(self):
        pass

class PostgresDatabaseManager():
    def __init__(self):
        self.session = postgres_session

    def __del__(self):
        pass

    def commit(self):
        self.session.commit()

    def run(self):
        pass

if __name__ == '__main__':
    mysqlSession = mysql_session
    print(mysqlSession.is_active)
    postgresSession = postgres_session
    print(postgresSession.is_active)

    #   INSERT
    # if not session.query(exists().where(GameType.gametype == 'test')).scalar():
    #     gt = GameType(gametype = 'test')
    #     session.add(gt)
    #     session.commit()

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

    # if session.query(exists().where(GameType.gametype == 'test')).scalar():
    #     session.query(GameType).filter_by(gametype='test').delete()
    #     session.commit()