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

from sklearn.cluster import DBSCAN, MeanShift
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA

from Configuration import *

class Analyzer:
    def __init__(self):
        self.tft_clustering_version = 1
        self.db_manager = DatabaseManager()
        self.postgres_db_manager = PostgresDatabaseManager()
        self.staticdata_manager = StaticDataManager()

    '''
    duration_datetime:
        
    params:
        
    returns:
        
    '''
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
        i_period_win_rate -> int: hour 기본
    returns:
        result -> json: 
    '''
    def cluster_tft_matches(self, start_time: datetime, end_time: datetime, i_period_win_rate: int):
        # ----------------------------------------------------
        #
        # Configuration
        #
        # ----------------------------------------------------
        period_timedelta = timedelta(hours=i_period_win_rate)
        daily_timedelta = timedelta(days=1)
        
        # ----------------------------------------------------
        #
        # Read match information by participants
        #
        # ----------------------------------------------------
        df_match_info = pd.read_sql(self.db_manager.session.query(Match) \
                .filter(Match.setnumber == 5) \
                .filter(and_(Match.matched_at <= end_time, Match.matched_at >= start_time)).limit(100).statement, \
            self.db_manager.session.bind)
        df_read = pd.read_sql(self.db_manager.session.query(AnalyzeSet5, Participant) \
                .join(Participant) \
                .join(Match) \
                .filter(Participant.is_analyzed == True) \
                .filter(Match.setnumber == 5) \
                .filter(and_(Match.matched_at <= end_time, Match.matched_at >= start_time)).limit(100).statement, \
            self.db_manager.session.bind)

        # ----------------------------------------------------
        #
        # Drop unused value for clustering
        #
        # ----------------------------------------------------
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
        df_dbscan = df_clustering

        # ----------------------------------------------------
        #
        # Cluster data
        #
        # ----------------------------------------------------
        df_dbscan = StandardScaler().fit_transform(df_dbscan)
        dbscan_model = DBSCAN(eps=7.142, min_samples=30).fit(df_dbscan)
        X_db_fit_pca = PCA(n_components=3).fit_transform(df_dbscan)

        dbscan_labels = dbscan_model.labels_
        dbscan_n_clusters_ = len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0)
        dbscan_n_noise_ = list(dbscan_labels).count(-1)

        print('Estimated number of clusters: %d' % dbscan_n_clusters_)
        print('Estimated number of noise points: %d' % dbscan_n_noise_)

        count_dbscan_labels = []
        unique, counts = np.unique(dbscan_labels, return_counts=True)
        for u, c in zip(unique, counts):
            print('label ' + str(u) + ": " + str(c))
            count_dbscan_labels.append(dict({'label': u, 'counts': c}))

        df_dbscan_result = pd.DataFrame(X_db_fit_pca)
        df_dbscan_result['label'] = pd.Series(dbscan_labels, name='label')
        df_read['label'] = pd.Series(dbscan_labels, name='label')
        df_dbscan_result['id'] = df_read['id']
        
        # ----------------------------------------------------
        #
        # Estimate results
        #
        # ----------------------------------------------------
        df_result = pd.DataFrame(count_dbscan_labels)
        df_matchtime_gametype = pd.merge(df_read[['placement','match_id', 'label']], df_match_info[['id','matched_at', 'gametype_id']], how='left', left_on='match_id', right_on='id')

        for dic in count_dbscan_labels:
            deck_label = dic['label']
            index_label = dic['label'] + 1

            # ----------------------------------------------------
            #
            # Caculate centroid and distance from centroid
            #
            # ----------------------------------------------------
            mean_result = df_dbscan_result[df_dbscan_result.label == deck_label].mean()
            df_result.loc[index_label, 'centroid_x'] = mean_result[0]
            df_result.loc[index_label, 'centroid_y'] = mean_result[1]
            df_result.loc[index_label, 'centroid_z'] = mean_result[2]

            df_cur_label = df_result[df_result.label == deck_label]
            df_cur_dbscan = df_dbscan_result[df_dbscan_result.label == deck_label]
            min_distance_id = -1
            min_distance_value = 1000
            
            df_cur_dbscan['distance'] = np.sum((np.array(df_cur_label[['centroid_x', '']])))

            for idx, row in df_dbscan_result[df_dbscan_result.label == deck_label].iterrows():
                if np.sum((np.array(df_cur_label[['centroid_x', 'centroid_y', 'centroid_z']]) - np.array(row[[0,1,2]])), axis=1) ** 2 < min_distance_value:
                    min_distance_value = np.sum((np.array(df_cur_label[['centroid_x', 'centroid_y', 'centroid_z']]) - np.array(row[[0,1,2]])), axis=1) ** 2
                    min_distance_id = idx
            if min_distance_id > -1:
                json_champions = json.loads(df_read.loc[min_distance_id, "champions"].replace("'", '"'))
                json_traits = json.loads(df_read.loc[min_distance_id, "traits"].replace("'", '"'))
                names = [self.staticdata_manager.GetChampionKoreanName(champion['character_id']) for champion in json_champions]
                df_result.loc[index_label, 'champions'] = str(names)
                names.clear()
                for trait in json_traits:
                    if trait['tier_current'] > 0:
                        names.append(self.staticdata_manager.GetTraitKoreanName(trait['name']))
                df_result.loc[index_label, 'traits'] = str(names)

            # ----------------------------------------------------
            #
            # win_reate, defense_rate
            #
            # ----------------------------------------------------
            if len(df_read[df_read.label == deck_label].index) == 0:
                df_result.loc[index_label, 'win_rate'] = 0.00
                df_result.loc[index_label, 'defence_rate'] = 0.00
            else:
                df_result.loc[index_label, 'win_rate'] = round(len(df_read[(df_read.label == deck_label) & 
                                                                              (df_read.placement == 1)].index) / 
                                                                  len(df_read[df_read.label == deck_label].index) * 100, 2)
                df_result.loc[index_label, 'defence_rate'] = round(len(df_read[(df_read.label == deck_label) & 
                                                                                  (df_read.placement <= 4)].index) / 
                                                                      len(df_read[df_read.label == deck_label].index) * 100, 2)

            if len(df_matchtime_gametype[(df_matchtime_gametype.label == deck_label)&
                                        (df_matchtime_gametype.gametype_id == 1)].index) == 0:
                df_result.loc[index_label, 'turbo_win_rate'] = 0.00
                df_result.loc[index_label, 'turbo_defence_rate'] = 0.00
            else:
                df_result.loc[index_label, 'turbo_win_rate'] = round(len(df_matchtime_gametype[(df_matchtime_gametype.label == deck_label) &
                                                                                                (df_matchtime_gametype.placement == 1) &
                                                                                                (df_matchtime_gametype.gametype_id == 1)].index) /
                                                                        len(df_matchtime_gametype[(df_matchtime_gametype.label == deck_label) &
                                                                                                (df_matchtime_gametype.gametype_id == 1)].index) * 100, 2)
                df_result.loc[index_label, 'turbo_defence_rate'] = round(len(df_matchtime_gametype[(df_matchtime_gametype.label == deck_label) & 
                                                                                                    (df_matchtime_gametype.placement <= 4) &
                                                                                                    (df_matchtime_gametype.gametype_id == 1)].index) / 
                                                                            len(df_matchtime_gametype[(df_matchtime_gametype.label == deck_label) &
                                                                                                    (df_matchtime_gametype.gametype_id == 1)].index) * 100, 2)

            if len(df_matchtime_gametype[(df_matchtime_gametype.label == deck_label)&
                                        (df_matchtime_gametype.gametype_id == 2)].index) == 0:
                df_result.loc[index_label, 'standard_win_rate'] = 0.00
                df_result.loc[index_label, 'standard_defence_rate'] = 0.00
            else:
                df_result.loc[index_label, 'standard_win_rate'] = round(len(df_matchtime_gametype[(df_matchtime_gametype.label == deck_label) &
                                                                                                (df_matchtime_gametype.placement == 1) &
                                                                                                (df_matchtime_gametype.gametype_id == 2)].index) /
                                                                        len(df_matchtime_gametype[(df_matchtime_gametype.label == deck_label) &
                                                                                                (df_matchtime_gametype.gametype_id == 2)].index) * 100, 2)
                df_result.loc[index_label, 'standard_defence_rate'] = round(len(df_matchtime_gametype[(df_matchtime_gametype.label == deck_label) & 
                                                                                                    (df_matchtime_gametype.placement <= 4) &
                                                                                                    (df_matchtime_gametype.gametype_id == 2)].index) / 
                                                                            len(df_matchtime_gametype[(df_matchtime_gametype.label == deck_label) &
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
                df_matches = df_matchtime_gametype[(df_matchtime_gametype.label == deck_label) & 
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
                df_matches = df_matchtime_gametype[(df_matchtime_gametype.label == deck_label) & 
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

            df_result.loc[index_label, 'period_win_rate'] = str(period_win_rate)
            df_result.loc[index_label, 'period_defence_rate'] = str(period_defence_rate)
            df_result.loc[index_label, 'turbo_period_win_rate'] = str(turbo_period_win_rate)
            df_result.loc[index_label, 'turbo_period_defence_rate'] = str(turbo_period_defence_rate)
            df_result.loc[index_label, 'standard_period_win_rate'] = str(standard_period_win_rate)
            df_result.loc[index_label, 'standard_period_defence_rate'] = str(standard_period_defence_rate)
            df_result.loc[index_label, 'daily_win_rate'] = str(daily_win_rate)
            df_result.loc[index_label, 'daily_defence_rate'] = str(daily_defence_rate)
            df_result.loc[index_label, 'turbo_daily_win_rate'] = str(turbo_daily_win_rate)
            df_result.loc[index_label, 'turbo_daily_defence_rate'] = str(turbo_daily_defence_rate)
            df_result.loc[index_label, 'standard_daily_win_rate'] = str(standard_daily_win_rate)
            df_result.loc[index_label, 'standard_daily_defence_rate'] = str(standard_daily_defence_rate)

        result = [{
            'info' : {
                'version': self.tft_clustering_version,
                'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
                'period': i_period_win_rate,
                'num_labels': dbscan_n_clusters_
            },
            'data' : {
                'label': df_result['label'].to_list(),
                'counts': df_result['counts'].to_list(),
                'traits': df_result['traits'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'champions': df_result['champions'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'centroid_x': df_result['centroid_x'].to_list(),
                'centroid_y': df_result['centroid_y'].to_list(),
                'centroid_z': df_result['centroid_z'].to_list(),
                'win_rate': df_result['win_rate'].to_list(),
                'defence_rate': df_result['defence_rate'].to_list(),
                'period_win_rate': df_result['period_win_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'period_defence_rate': df_result['period_defence_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'turbo_period_win_rate': df_result['turbo_period_win_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'turbo_period_defence_rate': df_result['turbo_period_defence_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'standard_period_win_rate': df_result['standard_period_win_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'standard_period_defence_rate': df_result['standard_period_defence_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'daily_win_rate': df_result['daily_win_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'daily_defence_rate': df_result['daily_defence_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'turbo_daily_win_rate': df_result['turbo_daily_win_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'turbo_daily_defence_rate': df_result['turbo_daily_defence_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'standard_daily_win_rate': df_result['standard_daily_win_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'standard_daily_defence_rate': df_result['standard_daily_defence_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
            }
        }]
        
        return result
        
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
        
        # test
        # print(json_result)
        # print(json.loads(json_result))
        # break

        # product
        ana = Analyzed(version = version, 
                        analyze_period = analyze_period, 
                        target_start_date=target_start_date, 
                        target_end_date=target_end_date,
                        target_date=target_date,
                        json_result=json_result)
        analyzer.postgres_db_manager.session.add(ana)
        analyzer.postgres_db_manager.session.commit()