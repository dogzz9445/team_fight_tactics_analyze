import pandas as pd
import json

from lolchess.model.match import Match
from lolchess.model.participant import Participant
from lolchess.model.analyze_set5 import AnalyzeSet5

from lolchess.DatabaseManager import DatabaseManager

from sqlalchemy import exists, and_, or_

from Configuration import *

class Preprocessor():
    def __init__(self):
        self.db = DatabaseManager()
        self.analyze_column_name = set5_analyzed_cloumn_names

    def preprocess(self):
        df_read = pd.read_sql(self.db.session.query(Participant) \
                    .join(Match) \
                    .filter(Participant.is_analyzed == False) \
                    .filter(Match.setnumber == 5).statement, self.db.session.bind)
        df_preprocessing = df_read
        df_preprocessing, dropped_idx = self.preprocessing_trash_rows(df_preprocessing)
        for idx in dropped_idx:
            if self.db.session.query(exists().where(Participant.id == idx)).scalar():
                self.db.session.query(Participant).filter_by(id=idx).update({"is_analyzed": True})

        pre_idx = 0
        for idx in self.myRange(0, len(df_preprocessing), 10000):
            df = df_preprocessing[pre_idx:idx].copy()
            df = self.preprocessing_split_traits_champions(df)
            for idx_row, row in df.iterrows():
                anaset5 = AnalyzeSet5()
                anaset5.fromDataFrame(row[set5_analyzed_cloumn_names])
                if not self.db.session.query(exists().where(AnalyzeSet5.participant_id == anaset5.participant_id)).scalar():
                    self.db.session.add(anaset5)
                    if self.db.session.query(exists().where(Participant.id == anaset5.participant_id)).scalar():
                        self.db.session.query(Participant).filter_by(id=anaset5.participant_id).update({"is_analyzed": True})
            pre_idx = idx
            self.db.session.commit()

    def run(self):
        self.preprocess()

    def preprocessing_trash_rows(self, df):
        # 1. 6레벨 이하
        dropped_idx = list(df[df['level'] <=  6].index)
        # 2. 넣은 데미지 6이하
        dropped_idx.extend(df[(df['gold_left'] >= 50) & (df['placement'] >= 7)].index)
        # 3. 50골드 이상 7등 이하
        dropped_idx.extend(df[df['total_damage_to_players'] <=  6].index)
        dropped_idx = sorted(list(set(dropped_idx)))
        df = df.drop(dropped_idx)
        df = df.reset_index().drop('index', axis=1)
        return df, dropped_idx

    def preprocessing_split_traits_champions(self, df_p1, json_convert=True):
        if json_convert == True:
            df_p1['traits'] = df_p1['traits'].apply(lambda x: json.loads(x.replace("'", '"')))
            df_p1['champions'] = df_p1['champions'].apply(lambda x: json.loads(x.replace("'", '"')))
        for idx, row in df_p1.iterrows():
            for trait in row['traits']:
                df_p1.loc[idx, trait['name'] + '_num_units'] = trait['num_units']
                df_p1.loc[idx, trait['name'] + '_tier_current'] = trait['tier_current']
            for champion in row['champions']:
                if champion['name'] + '_exits' in df_p1.columns:
                    if df_p1.loc[idx, champion['name'] + '_exits'] == 1:
                        if df_p1.loc[idx, champion['name'] + '_tier'] < champion['tier']:
                            df_p1.loc[idx, champion['name'] + '_tier'] = champion['tier']
                else:
                    df_p1.loc[idx, champion['character_id'] + '_tier'] = champion['tier']
                    df_p1.loc[idx, champion['character_id'] + '_exits'] = 1
        df_p1.fillna(0, inplace=True)
        return df_p1

    def myRange(start,end,step):
        i = start
        while i < end:
            yield i
            i += step
        yield end

if __name__ == '__main__':
    preprocessor = Preprocessor()
    preprocessor.run()
