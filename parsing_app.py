from riotwatcher import TftWatcher, ApiError
import secret
import datetime

class TFTParsingApp:

    def __init__(self,
        RIOT_API_KEY,
        platform = 'KR',
        routing = 'ASIA'):
        self.api = TftWatcher(api_key=secret.RIOT_API_KEY)
        self.platform = platform
        self.routing = routing
        self.default_start_datetime = datetime.strptime('2018-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        self.default_start_timestamp = int(datetime.timestamp(self.default_start_datetime) * 1000)
        self.season5_start_datetime = datetime.strptime('2021-04-28 12:00:00', '%Y-%m-%d %H:%M:%S')
        self.season5_start_timestamp = int(datetime.timestamp(self.season5_start_datetime) * 1000)

    # -------------------------------------------------------------------------------
    #
    # Class method for asynchronized requests pool
    #
    # -------------------------------------------------------------------------------
    async def GetMatch(self, puuid: str, count: int = 20):
        response = None
        try:
            response = await self.api.match.by_puuid(self.routing, str(puuid), 20)
        except ApiError as err:
            print(err)
        return response

    # -------------------------------------------------------------------------------
    #
    # Class method for test
    #
    # -------------------------------------------------------------------------------
    def requestTopSummoners(self):
        limit_top_summoners = 200
        try:
            challengers = self.api.league.challenger(self.platform)
            grandmasters = self.api.league.grandmaster(self.platform)
            masters = self.api.league.master(self.platform)
        except ApiError as err:
            print(err)
        challengers = [summoner['summonerId'] for summoner in challengers['entries']]
        grandmasters = [summoner['summonerId'] for summoner in grandmasters['entries']]
        masters = [summoner['summonerId'] for summoner in masters['entries']]
        standard = challengers + grandmasters + masters
        if len(standard) > limit_top_summoners:
            standard = standard[0:200]

        hot_turbo = []
        try:
            turbo = self.api.league.rated_ladders(self.platform, 'RANKED_TFT_TURBO')
        except ApiError as err:
            print(err)
        for idx, summoner in enumerate(turbo):
            if idx < summoner['previousUpdateLadderPosition'] - 10:
                hot_turbo.append(summoner['summonerId'])
        turbo = [summoner['summonerId'] for summoner in turbo]
        
        return {
            'standard' : standard,
            'turbo' : turbo,
            'hot_turbo' : hot_turbo
        }

    def requestPuuids(self, summoner_Ids):
        summoners = []
        for summoner_id in summoner_Ids:
            try:
                response = self.api.summoner.by_id(self.paltform, summoner_id)
                summoners.append({
                    'summonerId' : summoner_id,
                    'puuid' : response['puuid']
                })
            except ApiError as err:
                print(err)
        return summoners

    def requestMatchIdsByList(self, list_puuids: list, count: int = 20):
        local_match_ids = []
        for idx, puuid in enumerate(list_puuids):
            try:
                response = self.api.match.by_puuid(self.routing, str(puuid), 20)
                local_match_ids.append(response)
            except ApiError as err:
                print(err)
            print('Get matches by puuids... (%5d/%5d)' % (idx, len(list_puuids)))
        return local_match_ids

    def GetMatchesByList(self, list_match_ids: list):
        local_matches = []
        for idx, match_id in enumerate(list_match_ids):
            try:
                response = self.api.match.by_id(self.routing, match_id)
                if (response['info']['game_datetime'] < self.season5_start_timestamp):
                    break
                local_matches.append(response)
            except ApiError as err:
                print(err)
            print('Get matches by match ids... (%5d/%5d)' % (idx, len(list_match_ids)))
        return local_matches
