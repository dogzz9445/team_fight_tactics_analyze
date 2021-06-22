import pandas as pd

from lolchess.model.match import GameType, Match
from lolchess.model.participant import Participant
from lolchess.model.analyze_set5 import AnalyzeSet5
from lolchess.model.analyzed import Analyzed
from lolchess.DatabaseManager import DatabaseManager, PostgresDatabaseManager
from lolchess.StaticDataManager import StaticDataManager

from sqlalchemy import exists, and_, or_

class Reader:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.postgres_db_manager = PostgresDatabaseManager()

    def read_data(self, start_time, end_time, limit=None):
        # ----------------------------------------------------
        #
        # Read match information by participants
        #
        # ----------------------------------------------------
        if limit == None:
            df_match_info = pd.read_sql(self.db_manager.session.query(Match) \
                    .filter(Match.setnumber == 5) \
                    .filter(and_(Match.matched_at <= end_time, Match.matched_at >= start_time)).statement, \
                self.db_manager.session.bind)
            df_read = pd.read_sql(self.db_manager.session.query(AnalyzeSet5, Participant) \
                    .join(Participant) \
                    .join(Match) \
                    .filter(Participant.is_analyzed == True) \
                    .filter(Match.setnumber == 5) \
                    .filter(and_(Match.matched_at <= end_time, Match.matched_at >= start_time)).statement, \
                self.db_manager.session.bind)
        else:
            df_match_info = pd.read_sql(self.db_manager.session.query(Match) \
                    .filter(Match.setnumber == 5) \
                    .filter(and_(Match.matched_at <= end_time, Match.matched_at >= start_time)).limit(limit).statement, \
                self.db_manager.session.bind)
            df_read = pd.read_sql(self.db_manager.session.query(AnalyzeSet5, Participant) \
                    .join(Participant) \
                    .join(Match) \
                    .filter(Participant.is_analyzed == True) \
                    .filter(Match.setnumber == 5) \
                    .filter(and_(Match.matched_at <= end_time, Match.matched_at >= start_time)).limit(limit).statement, \
                self.db_manager.session.bind)
        df_for_cluster = df_read.drop(['id', 
                                  'last_round', 
                                  'level', 
                                  'placement', 
                                  'players_eliminated', 
                                  'time_eliminated', 
                                  'total_damage_to_players', 
                                  'traits', 
                                  'champions', 
                                  'is_analyzed', 
                                  'match_id', 
                                  'participant_id', 
                                  'id_1', 
                                  'gold_left'], axis=1)
        return (df_match_info, df_read, df_for_cluster)