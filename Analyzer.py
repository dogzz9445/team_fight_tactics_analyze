import pandas as pd
import numpy as np
import json
import copy
from datetime import datetime, timedelta

from sqlalchemy.sql.functions import current_time

from lolchess.model.match import GameType, Match
from lolchess.model.participant import Participant
from lolchess.model.analyze_set5 import AnalyzeSet5
from lolchess.model.analyzed import Analyzed
from lolchess.DatabaseManager import DatabaseManager, PostgresDatabaseManager
from lolchess.StaticDataManager import StaticDataManager

from sqlalchemy import exists, and_, or_

from sklearn.cluster import DBSCAN
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from Configuration import *

class Analyzer:
    def __init__(self):
        self.tft_clustering_version = 1
        self.db_manager = DatabaseManager()
        self.postgres_db_manager = PostgresDatabaseManager()
        self.staticdata_manager = StaticDataManager()

    def duration_datetime(self, start_time, end_time, period_delta):
        previous_time = start_time
        current_time = start_time + period_delta
        while not current_time > end_time:
            yield previous_time, current_time
            previous_time = current_time
            current_time = current_time + period_delta

    '''
    cluster_tft_matches:
        클러스터링 분석
    params:
        start_time -> datetime: 분석 시작 날짜 및 시간
        end_time -> datetime: 분석 끝 날짜 및 시간
        period_win_rate -> int: hour 기본
    returns:
        result -> json: 
    '''
    def cluster_tft_matches(self, start_time: datetime, end_time: datetime, period_win_rate: int):
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
        df_clustering = df_read.drop(['id', 
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
        df_db = df_clustering
        df_db = StandardScaler().fit_transform(df_db)
        db_model = DBSCAN(eps=7.142, min_samples=30).fit(df_db)
        X_db_fit_pca = PCA(n_components=3).fit_transform(df_db)

        # Compute DBSCAN
        db_labels = db_model.labels_

        # Number of clusters in labels, ignoring noise if present.
        db_n_clusters_ = len(set(db_labels)) - (1 if -1 in db_labels else 0)
        db_n_noise_ = list(db_labels).count(-1)

        print('Estimated number of clusters: %d' % db_n_clusters_)
        print('Estimated number of noise points: %d' % db_n_noise_)

        count_db_labels = []
        unique, counts = np.unique(db_labels, return_counts=True)
        for u, c in zip(unique, counts):
            print('label ' + str(u) + ": " + str(c))
            count_db_labels.append(dict({'label': u, 'counts': c}))

        df_db_result = pd.DataFrame(X_db_fit_pca)
        df_db_result['label'] = pd.Series(db_labels, name='label')
        df_read['label'] = pd.Series(db_labels, name='label')
        df_db_result['id'] = df_read['id']
        
        period_timedelta = timedelta(hours=period_win_rate)
        daily_timedelta = timedelta(days=1)
        json_champions = None
        json_traits = None
        df_db_labels = pd.DataFrame(count_db_labels)
        df_matchtime_gametype = pd.merge(df_read[['placement','match_id', 'label']], df_match_info[['id','matched_at', 'gametype_id']], how='left', left_on='match_id', right_on='id')

        for dic in count_db_labels:
            dic_label = dic['label']
            index_label = dic['label'] + 1

            mean_result = df_db_result[df_db_result.label == dic_label].mean()
            df_db_labels.loc[index_label, 'centroid_x'] = mean_result[0]
            df_db_labels.loc[index_label, 'centroid_y'] = mean_result[1]
            df_db_labels.loc[index_label, 'centroid_z'] = mean_result[2]

            cur_label = df_db_labels[df_db_labels.label == dic_label]
            min_distance_id = -1
            min_distance_value = 1000
            for idx, row in df_db_result[df_db_result.label == dic_label].iterrows():
                if np.sum((np.array(cur_label[['centroid_x', 'centroid_y', 'centroid_z']]) - np.array(row[[0,1,2]])), axis=1) ** 2 < min_distance_value:
                    min_distance_value = np.sum((np.array(cur_label[['centroid_x', 'centroid_y', 'centroid_z']]) - np.array(row[[0,1,2]])), axis=1) ** 2
                    min_distance_id = idx
            if min_distance_id > -1:
                json_champions = json.loads(df_read.loc[min_distance_id, "champions"].replace("'", '"'))
                json_traits = json.loads(df_read.loc[min_distance_id, "traits"].replace("'", '"'))
                names = [self.staticdata_manager.GetChampionKoreanName(champion['character_id']) for champion in json_champions]
                df_db_labels.loc[index_label, 'champions'] = str(names)
                names.clear()
                for trait in json_traits:
                    if trait['tier_current'] > 0:
                        names.append(self.staticdata_manager.GetTraitKoreanName(trait['name']))
                df_db_labels.loc[index_label, 'traits'] = str(names)

            if len(df_read[df_read.label == dic_label].index) == 0:
                df_db_labels.loc[index_label, 'win_rate'] = 0.00
                df_db_labels.loc[index_label, 'defence_rate'] = 0.00
            else:
                df_db_labels.loc[index_label, 'win_rate'] = round(len(df_read[(df_read.label == dic['label']) & 
                                                                              (df_read.placement == 1)].index) / 
                                                                  len(df_read[df_read.label == dic['label']].index) * 100, 2)
                df_db_labels.loc[index_label, 'defence_rate'] = round(len(df_read[(df_read.label == dic['label']) & 
                                                                                  (df_read.placement <= 4)].index) / 
                                                                      len(df_read[df_read.label == dic['label']].index) * 100, 2)

            if len(df_matchtime_gametype[(df_matchtime_gametype.label == dic_label)&
                                        (df_matchtime_gametype.gametype_id == 1)].index) == 0:
                df_db_labels.loc[index_label, 'turbo_win_rate'] = 0.00
                df_db_labels.loc[index_label, 'turbo_defence_rate'] = 0.00
            else:
                df_db_labels.loc[index_label, 'turbo_win_rate'] = round(len(df_matchtime_gametype[(df_matchtime_gametype.label == dic_label) &
                                                                                                (df_matchtime_gametype.placement == 1) &
                                                                                                (df_matchtime_gametype.gametype_id == 1)].index) /
                                                                        len(df_matchtime_gametype[(df_matchtime_gametype.label == dic_label) &
                                                                                                (df_matchtime_gametype.gametype_id == 1)].index) * 100, 2)
                df_db_labels.loc[index_label, 'turbo_defence_rate'] = round(len(df_matchtime_gametype[(df_matchtime_gametype.label == dic['label']) & 
                                                                                                    (df_matchtime_gametype.placement <= 4) &
                                                                                                    (df_matchtime_gametype.gametype_id == 1)].index) / 
                                                                            len(df_matchtime_gametype[(df_matchtime_gametype.label == dic_label) &
                                                                                                    (df_matchtime_gametype.gametype_id == 1)].index) * 100, 2)

            if len(df_matchtime_gametype[(df_matchtime_gametype.label == dic_label)&
                                        (df_matchtime_gametype.gametype_id == 2)].index) == 0:
                df_db_labels.loc[index_label, 'standard_win_rate'] = 0.00
                df_db_labels.loc[index_label, 'standard_defence_rate'] = 0.00
            else:
                df_db_labels.loc[index_label, 'standard_win_rate'] = round(len(df_matchtime_gametype[(df_matchtime_gametype.label == dic_label) &
                                                                                                (df_matchtime_gametype.placement == 1) &
                                                                                                (df_matchtime_gametype.gametype_id == 2)].index) /
                                                                        len(df_matchtime_gametype[(df_matchtime_gametype.label == dic_label) &
                                                                                                (df_matchtime_gametype.gametype_id == 2)].index) * 100, 2)
                df_db_labels.loc[index_label, 'standard_defence_rate'] = round(len(df_matchtime_gametype[(df_matchtime_gametype.label == dic['label']) & 
                                                                                                    (df_matchtime_gametype.placement <= 4) &
                                                                                                    (df_matchtime_gametype.gametype_id == 2)].index) / 
                                                                            len(df_matchtime_gametype[(df_matchtime_gametype.label == dic_label) &
                                                                                                    (df_matchtime_gametype.gametype_id == 2)].index) * 100, 2)

            period_win_rate = []
            period_defence_rate = []
            turbo_period_win_rate = []
            turbo_period_defence_rate = []
            standard_period_win_rate = []
            standard_period_defence_rate = []
            daily_win_rate = []
            daily_defence_rate = []
            turbo_daily_win_rate = []
            turbo_daily_defence_rate = []
            standard_daily_win_rate = []
            standard_daily_defence_rate = []
            for s_time, e_time in self.duration_datetime(start_time, end_time, period_timedelta):
                df_matches = df_matchtime_gametype[(df_matchtime_gametype.label == dic['label']) & 
                                            (df_matchtime_gametype.matched_at >= s_time) & 
                                            (df_matchtime_gametype.matched_at < e_time)]
                df_turbo_matches = df_matches[df_matches.gametype_id == 1]
                df_standard_matches = df_matches[df_matches.gametype_id == 2]

                if len(df_matches.index) == 0:
                    period_win_rate.append(0.00)
                    period_defence_rate.append(0.00)
                else:
                    period_win_rate.append(round(len(df_matches[(df_matches.placement == 1)].index) / len(df_matches.index) * 100, 2))
                    period_defence_rate.append(round(len(df_matches[(df_matches.placement <= 4)].index) / len(df_matches.index) * 100, 2))
                if len(df_turbo_matches.index) == 0:
                    turbo_period_win_rate.append(0.00)
                    turbo_period_defence_rate.append(0.00)
                else:
                    turbo_period_win_rate.append(round(len(df_turbo_matches[(df_turbo_matches.placement == 1)].index) / len(df_turbo_matches.index) * 100, 2))
                    turbo_period_defence_rate.append(round(len(df_turbo_matches[(df_turbo_matches.placement <= 4)].index) / len(df_turbo_matches.index) * 100, 2))
                if len(df_standard_matches.index) == 0:
                    standard_period_win_rate.append(0.00)
                    standard_period_defence_rate.append(0.00)
                else:
                    standard_period_win_rate.append(round(len(df_standard_matches[(df_standard_matches.placement == 1)].index) / len(df_standard_matches.index) * 100, 2))
                    standard_period_defence_rate.append(round(len(df_standard_matches[(df_standard_matches.placement <= 4)].index) / len(df_standard_matches.index) * 100, 2))

            for s_time, e_time in self.duration_datetime(start_time, end_time, daily_timedelta):
                df_matches = df_matchtime_gametype[(df_matchtime_gametype.label == dic['label']) & 
                                            (df_matchtime_gametype.matched_at >= s_time) & 
                                            (df_matchtime_gametype.matched_at < e_time)]
                df_turbo_matches = df_matches[df_matches.gametype_id == 1]
                df_standard_matches = df_matches[df_matches.gametype_id == 2]

                if len(df_matches.index) == 0:
                    daily_win_rate.append(0.00)
                    daily_defence_rate.append(0.00)
                else:
                    daily_win_rate.append(round(len(df_matches[(df_matches.placement == 1)].index) /len(df_matches.index) * 100, 2))
                    daily_defence_rate.append(round(len(df_matches[(df_matches.placement <= 4)].index) /len(df_matches.index) * 100, 2))
                if len(df_turbo_matches.index) == 0:
                    turbo_daily_win_rate.append(0.00)
                    turbo_daily_defence_rate.append(0.00)
                else:
                    turbo_daily_win_rate.append(round(len(df_turbo_matches[(df_turbo_matches.placement == 1)].index) / len(df_turbo_matches.index) * 100, 2))
                    turbo_daily_defence_rate.append(round(len(df_turbo_matches[(df_turbo_matches.placement <= 4)].index) / len(df_turbo_matches.index) * 100, 2))
                if len(df_standard_matches.index) == 0:
                    standard_daily_win_rate.append(0.00)
                    standard_daily_defence_rate.append(0.00)
                else:
                    standard_daily_win_rate.append(round(len(df_standard_matches[(df_standard_matches.placement == 1)].index) / len(df_standard_matches.index) * 100, 2))
                    standard_daily_defence_rate.append(round(len(df_standard_matches[(df_standard_matches.placement <= 4)].index) / len(df_standard_matches.index) * 100, 2))

            df_db_labels.loc[index_label, 'period_win_rate'] = str(period_win_rate)
            df_db_labels.loc[index_label, 'period_defence_rate'] = str(period_defence_rate)
            df_db_labels.loc[index_label, 'turbo_period_win_rate'] = str(turbo_period_win_rate)
            df_db_labels.loc[index_label, 'turbo_period_defence_rate'] = str(turbo_period_defence_rate)
            df_db_labels.loc[index_label, 'standard_period_win_rate'] = str(standard_period_win_rate)
            df_db_labels.loc[index_label, 'standard_period_defence_rate'] = str(standard_period_defence_rate)
            df_db_labels.loc[index_label, 'daily_win_rate'] = str(daily_win_rate)
            df_db_labels.loc[index_label, 'daily_defence_rate'] = str(daily_defence_rate)
            df_db_labels.loc[index_label, 'turbo_daily_win_rate'] = str(turbo_daily_win_rate)
            df_db_labels.loc[index_label, 'turbo_daily_defence_rate'] = str(turbo_daily_defence_rate)
            df_db_labels.loc[index_label, 'standard_daily_win_rate'] = str(standard_daily_win_rate)
            df_db_labels.loc[index_label, 'standard_daily_defence_rate'] = str(standard_daily_defence_rate)

        result = [{
            'info' : {
                'version': self.tft_clustering_version,
                'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
                'period': period_win_rate
            },
            'data' : df_db_labels.to_dict()
        }]
        
        return result
        
        # TODO: result를 데이터베이스 JSON 형태로 저장
        
def week_analyze_time_duration(start_date: datetime, end_date: datetime):
    analyze_date = start_date + timedelta(days=1)
    while not analyze_date > end_date:
        yield analyze_date - timedelta(days=7), analyze_date
        analyze_date = analyze_date + timedelta(days=1)

if __name__ == '__main__':
    analyzer = Analyzer()

    analyze_start_date = datetime(2021, 5, 27, 0, 0, 0)
    analyze_end_date = datetime(2021, 5, 29, 0, 0, 0)

    for s_date, e_date in week_analyze_time_duration(analyze_start_date, analyze_end_date):
        version = 1
        analyze_period = 6
        target_start_date = s_date
        target_end_date = e_date
        target_date = e_date - timedelta(days=1)

        print('Analyzing: ' + target_date.strftime('%Y-%m-%d'))

        json_result = analyzer.cluster_tft_matches(s_date, e_date, 6)
        
        ana = Analyzed(version = version, 
                        analyze_period = analyze_period, 
                        target_start_date=target_start_date, 
                        target_end_date=target_end_date,
                        target_date=target_date,
                        json_result=json_result)
        analyzer.postgres_db_manager.session.add(ana)
        analyzer.postgres_db_manager.session.commit()