from riotwatcher import TftWatcher, ApiError
import importlib
import secret
import pickle
from datetime import datetime

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
