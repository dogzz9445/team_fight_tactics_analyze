import pandas as pd
import numpy as np
import json

from Configuration import *

from .Util.DateUtil import duration_datetime

class Analyzer:
    def __init__(self):
        pass

    def estimate_deck_champion_and_traits(self,
                                          df_labeled,
                                          count_cluster_labels):
        # ----------------------------------------------------
        #
        # Estimate results
        #
        # ----------------------------------------------------
        df_decks = pd.DataFrame(count_cluster_labels)

        for deck in count_cluster_labels:
            deck_label = deck['label']
            index_label = deck['label'] + 1

            # ----------------------------------------------------
            #
            # Caculate centroid and distance from centroid
            #
            # ----------------------------------------------------
            mean_result = df_labeled[df_labeled.label == deck_label].mean()
            df_decks.loc[index_label, 'centroid_x'] = mean_result[0]
            df_decks.loc[index_label, 'centroid_y'] = mean_result[1]
            df_decks.loc[index_label, 'centroid_z'] = mean_result[2]

            min_distance_id = -1
            min_distance_value = 1000
            
            for idx, row in df_labeled[df_labeled.label == deck_label].iterrows():
                if np.sum((np.array(df_decks.loc[df_decks.label == deck_label, ['centroid_x', 'centroid_y', 'centroid_z']]) - np.array(row[[0,1,2]])), axis=1) ** 2 < min_distance_value:
                    min_distance_value = np.sum((np.array(df_decks[df_decks.label == deck_label, ['centroid_x', 'centroid_y', 'centroid_z']]) - np.array(row[[0,1,2]])), axis=1) ** 2
                    min_distance_id = idx
            if min_distance_id > -1:
                json_champions = json.loads(df_labeled.loc[min_distance_id, "champions"].replace("'", '"'))
                json_traits = json.loads(df_labeled.loc[min_distance_id, "traits"].replace("'", '"'))
                names = [self.staticdata_manager.GetChampionKoreanName(champion['character_id']) for champion in json_champions]
                df_decks.loc[index_label, 'champions'] = str(names)
                names.clear()
                for trait in json_traits:
                    if trait['tier_current'] > 0:
                        names.append(self.staticdata_manager.GetTraitKoreanName(trait['name']))
                df_decks.loc[index_label, 'traits'] = str(names)

        df_decks = df_decks
        return df_decks

    def estimate_win_rate(self, df_labeled, df_match_info, df_decks, start_time, end_time):
        '''
        '''
        df_gametype = pd.merge(df_labeled[['placement','match_id', 'label']], df_match_info[['id','matched_at', 'gametype_id']], how='left', left_on='match_id', right_on='id')
        
        for idx, deck in df_decks.iterrows():
            deck_label = deck['label']
            index_label = deck['label'] + 1

            # ----------------------------------------------------
            #
            # Caculate centroid and distance from centroid
            #
            # ----------------------------------------------------
            if len(df_decks[df_decks.label == deck_label].index) == 0:
                df_decks.loc[index_label, 'win_rate'] = 0.00
                df_decks.loc[index_label, 'defence_rate'] = 0.00
            else:
                df_decks.loc[index_label, 'win_rate'] = round(len(df_gametype[(df_gametype.label == deck_label) & 
                                                                              (df_gametype.placement == 1)].index) / 
                                                                  len(df_gametype[df_gametype.label == deck_label].index) * 100, 2)
                df_decks.loc[index_label, 'defence_rate'] = round(len(df_gametype[(df_gametype.label == deck_label) & 
                                                                                  (df_gametype.placement <= 4)].index) / 
                                                                      len(df_gametype[df_gametype.label == deck_label].index) * 100, 2)

            if len(df_gametype[(df_gametype.label == deck_label)&(df_gametype.gametype_id == 1)].index) == 0:
                df_decks.loc[index_label, 'turbo_win_rate'] = 0.00
                df_decks.loc[index_label, 'turbo_defence_rate'] = 0.00
            else:
                df_decks.loc[index_label, 'turbo_win_rate'] = round(len(df_gametype[(df_gametype.label == deck_label) &
                                                                                                (df_gametype.placement == 1) &
                                                                                                (df_gametype.gametype_id == 1)].index) /
                                                                        len(df_gametype[(df_gametype.label == deck_label) &
                                                                                                (df_gametype.gametype_id == 1)].index) * 100, 2)
                df_decks.loc[index_label, 'turbo_defence_rate'] = round(len(df_gametype[(df_gametype.label == deck_label) & 
                                                                                                    (df_gametype.placement <= 4) &
                                                                                                    (df_gametype.gametype_id == 1)].index) / 
                                                                            len(df_gametype[(df_gametype.label == deck_label) &
                                                                                                    (df_gametype.gametype_id == 1)].index) * 100, 2)

            if len(df_gametype[(df_gametype.label == deck_label)&
                                        (df_gametype.gametype_id == 2)].index) == 0:
                df_decks.loc[index_label, 'standard_win_rate'] = 0.00
                df_decks.loc[index_label, 'standard_defence_rate'] = 0.00
            else:
                df_decks.loc[index_label, 'standard_win_rate'] = round(len(df_gametype[(df_gametype.label == deck_label) &
                                                                                                (df_gametype.placement == 1) &
                                                                                                (df_gametype.gametype_id == 2)].index) /
                                                                        len(df_gametype[(df_gametype.label == deck_label) &
                                                                                                (df_gametype.gametype_id == 2)].index) * 100, 2)
                df_decks.loc[index_label, 'standard_defence_rate'] = round(len(df_gametype[(df_gametype.label == deck_label) & 
                                                                                                    (df_gametype.placement <= 4) &
                                                                                                    (df_gametype.gametype_id == 2)].index) / 
                                                                            len(df_gametype[(df_gametype.label == deck_label) &
                                                                                                    (df_gametype.gametype_id == 2)].index) * 100, 2)

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
            for s_time, e_time in duration_datetime(start_time, end_time, self.period_timedelta):
                df_matches = df_gametype[(df_gametype.label == deck_label) & 
                                            (df_gametype.matched_at >= s_time) & 
                                            (df_gametype.matched_at < e_time)]
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

            for s_time, e_time in duration_datetime(start_time, end_time, self.daily_timedelta):
                df_matches = df_gametype[(df_gametype.label == deck_label) & 
                                            (df_gametype.matched_at >= s_time) & 
                                            (df_gametype.matched_at < e_time)]
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

            df_decks.loc[index_label, 'period_win_rate'] = str(period_win_rate)
            df_decks.loc[index_label, 'period_defence_rate'] = str(period_defence_rate)
            df_decks.loc[index_label, 'turbo_period_win_rate'] = str(turbo_period_win_rate)
            df_decks.loc[index_label, 'turbo_period_defence_rate'] = str(turbo_period_defence_rate)
            df_decks.loc[index_label, 'standard_period_win_rate'] = str(standard_period_win_rate)
            df_decks.loc[index_label, 'standard_period_defence_rate'] = str(standard_period_defence_rate)
            df_decks.loc[index_label, 'daily_win_rate'] = str(daily_win_rate)
            df_decks.loc[index_label, 'daily_defence_rate'] = str(daily_defence_rate)
            df_decks.loc[index_label, 'turbo_daily_win_rate'] = str(turbo_daily_win_rate)
            df_decks.loc[index_label, 'turbo_daily_defence_rate'] = str(turbo_daily_defence_rate)
            df_decks.loc[index_label, 'standard_daily_win_rate'] = str(standard_daily_win_rate)
            df_decks.loc[index_label, 'standard_daily_defence_rate'] = str(standard_daily_defence_rate)

        result = [{
            'info' : {
                'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
                'num_labels': len(df_decks)
            },
            'data' : {
                'label': df_decks['label'].to_list(),
                'counts': df_decks['counts'].to_list(),
                'traits': df_decks['traits'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'champions': df_decks['champions'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'centroid_x': df_decks['centroid_x'].to_list(),
                'centroid_y': df_decks['centroid_y'].to_list(),
                'centroid_z': df_decks['centroid_z'].to_list(),
                'win_rate': df_decks['win_rate'].to_list(),
                'defence_rate': df_decks['defence_rate'].to_list(),
                'period_win_rate': df_decks['period_win_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'period_defence_rate': df_decks['period_defence_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'turbo_period_win_rate': df_decks['turbo_period_win_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'turbo_period_defence_rate': df_decks['turbo_period_defence_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'standard_period_win_rate': df_decks['standard_period_win_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'standard_period_defence_rate': df_decks['standard_period_defence_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'daily_win_rate': df_decks['daily_win_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'daily_defence_rate': df_decks['daily_defence_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'turbo_daily_win_rate': df_decks['turbo_daily_win_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'turbo_daily_defence_rate': df_decks['turbo_daily_defence_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'standard_daily_win_rate': df_decks['standard_daily_win_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
                'standard_daily_defence_rate': df_decks['standard_daily_defence_rate'].apply(lambda x: json.loads(x.replace("'", '"'))).to_list(),
            }
        }]
        
        return result
