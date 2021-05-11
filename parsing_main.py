from datetime import datetime
import importlib
import pickle
import time
import asyncio

from riotwatcher import TftWatcher, ApiError
import secret

RIOT_API_KEY = secret.RIOT_API_KEY
platform_regions = {
    '한국' : 'KR',
    '미국' : 'NA1'
}
routing_regions = {
    '한국' : 'ASIA',
    '미국' : 'AMERICAS'
}

default_start_datetime = datetime.strptime('2018-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
default_start_timestamp = int(datetime.timestamp(default_start_datetime) * 1000)
season5_start_datetime = datetime.strptime('2021-04-28 12:00:00', '%Y-%m-%d %H:%M:%S')
season5_start_timestamp = int(datetime.timestamp(season5_start_datetime) * 1000)

async def GetMatchesByList(list_match_ids: list, limit_start_timestamp: int = default_start_timestamp):
    local_matches = []
    for idx, match_id in enumerate(list_match_ids):
        try:
            response = tft_watcher.match.by_id(routing_regions['한국'], match_id)
            if (response['info']['game_datetime'] < limit_start_timestamp):
                break
            local_matches.append(response)
        except ApiError as err:
            print(err)
        print('Get matches by match ids... (%5d/%5d)' % (idx, len(list_match_ids)))
    return local_matches

async def GetMatch(idx: int, puuid: str, count: int = 20):
    response = None
    try:
        response = await tft_watcher.match.by_puuid(routing_regions['한국'], str(puuid), 20)
    except ApiError as err:
        print(err)
    print('Get matches by puuids... (%5d/%5d)' % (idx, len(list_puuids)))
    return response

async def GetMatchIdsByList(list_puuids: list, count: int = 20):
    local_match_ids = []
    for idx, puuid in enumerate(list_puuids):
        try:
            response = tft_watcher.match.by_puuid(routing_regions['한국'], str(puuid), 20)
            local_match_ids.append(response)
        except ApiError as err:
            print(err)
        print('Get matches by puuids... (%5d/%5d)' % (idx, len(list_puuids)))
    return local_match_ids

if __name__ == '__main__':
    # -------------------------------------------------------------------------------
    #
    # Configuration 
    #
    # -------------------------------------------------------------------------------
    

    # -------------------------------------------------------------------------------
    #
    # Configuration 
    #
    # -------------------------------------------------------------------------------
    RIOT_API_KEY = secret.RIOT_API_KEY
    tft_watcher = TftWatcher(api_key=RIOT_API_KEY)


    # -------------------------------------------------------------------------------
    # Main Loop
    # -------------------------------------------------------------------------------
    while True:
        
        time.sleep(0.01)