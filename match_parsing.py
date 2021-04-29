from riotwatcher import TftWatcher, ApiError
import importlib
import secret
import pickle
from datetime import datetime

default_date_string = '2018-01-01 00:00:00'
default_start_date = datetime.strptime(default_date_string, '%Y-%m-%d %H:%M:%S')
default_start_timestamp = int(datetime.timestamp(default_start_date) * 1000)

def GetMatchIdsByList(list_puuids: list, count: int = 20):
    local_match_ids = []
    for idx, puuid in enumerate(list_puuids):
        try:
            response = tft_watcher.match.by_puuid(region_match, str(puuid), 20)
            local_match_ids.extend(response)
        except ApiError as err:
            print(err)
        print('Get matches by puuids... (%5d/%5d)' % (idx, len(list_puuids)))
    return local_match_ids

def GetMatchesByList(list_match_ids: list, limit_start_timestamp: int = default_start_timestamp):
    local_matches = []
    for idx, match_id in enumerate(list_match_ids):
        try:
            response = tft_watcher.match.by_id(region_match, match_id)
            if (response['info']['game_datetime'] < limit_start_timestamp):
                break
            local_matches.append(response)
        except ApiError as err:
            print(err)
        print('Get matches by match ids... (%5d/%5d)' % (idx, len(list_match_ids)))
    return local_matches


if __name__ == '__main__':
    RIOT_API_KEY = secret.RIOT_API_KEY
    tft_watcher = TftWatcher(api_key=RIOT_API_KEY)
    region = 'KR'
    region_match = 'ASIA'

    summoner_names_file = 'data/summoner_names.txt'
    summoner_puuid_file = 'data/summoner_puuid.txt'
    
    matches_file = 'data/set5/matches_' + datetime.now().strftime("%m%d_%H%M") +'.txt'

    season5_date_string = '2021-04-28 20:00:00'
    season5_start_date = datetime.strptime(season5_date_string, '%Y-%m-%d %H:%M:%S')
    season5_start_timestamp = int(datetime.timestamp(season5_start_date) * 1000)

    puuids = None

    with open(summoner_puuid_file, 'rb') as in_file:
        puuids = pickle.load(in_file)

    match_ids = GetMatchIdsByList(puuids[:10000], 13)
    match_ids = sorted(list(set(match_ids)), reverse=True)

    with open('data/match_ids.txt', 'wb') as out_file:
        pickle.dump(match_ids, out_file)

    with open('data/match_ids.txt', 'rb') as in_file:
        match_ids = pickle.load(in_file)

    matches = GetMatchesByList(match_ids, season5_start_timestamp)

    with open(matches_file, 'wb') as out_file:
     pickle.dump(matches, out_file)