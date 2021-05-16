from riotwatcher import TftWatcher, ApiError
import secret
from datetime import datetime
from lolchess.DatabaseManager import DatabaseManager

from lolchess.model.summoner import Summoner
from lolchess.model.match import GameType, Match
from lolchess.model.participant import Participant

from sqlalchemy import create_engine, exists
import time


class TFTParsingApp:
    """
    
    """

    def __init__(self,
        platform = 'KR',
        routing = 'ASIA'):
        self.api = TftWatcher(api_key=secret.RIOT_API_KEY)
        self.platform = platform
        self.routing = routing
        self.default_start_datetime = datetime.strptime('2018-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        self.default_start_timestamp = int(datetime.timestamp(self.default_start_datetime) * 1000)
        self.season5_start_datetime = datetime.strptime('2021-04-28 12:00:00', '%Y-%m-%d %H:%M:%S')
        self.season5_start_timestamp = int(datetime.timestamp(self.season5_start_datetime) * 1000)
        self.db = DatabaseManager()

    # -------------------------------------------------------------------------------
    #
    # Class method for asynchronized requests pool
    #
    # -------------------------------------------------------------------------------
    async def GetMatch(self, puuid: str, count: int = 20):
        """
        
        """
        response = None
        try:
            response = await self.api.match.by_puuid(self.routing, str(puuid), 100)
        except ApiError as err:
            print(err)
        return response

    # -------------------------------------------------------------------------------
    #
    # Class method for test
    #
    # -------------------------------------------------------------------------------
    def requestTopSummoners(self):
        """
        
        """
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
            standard = standard[0:300]

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
        """
        
        """
        summoners = []
        for summoner_id in summoner_Ids:
            if self.db.session.query(exists().where(Summoner.summoner_id == summoner_id)).scalar():
                summoner = self.db.session.query(Summoner).where(Summoner.summoner_id == summoner_id).first()
                summoners.append({
                    'summonerId' : summoner.summoner_id,
                    'puuid' : summoner.summoner_puuid
                })
            else:
                try:
                    response = self.api.summoner.by_id(self.platform, summoner_id)
                    summoners.append({
                        'summonerId' : summoner_id,
                        'puuid' : response['puuid']
                    })
                    summoner = Summoner(summoner_id=summoner_id, summoner_puuid=response['puuid'])
                    self.db.session.add(summoner)
                except ApiError as err:
                    print(err)
                except:
                    time.sleep(30)
        self.db.commit()
        return summoners

    def requestMatchIdsByList(self, list_puuids: list, count: int = 50):
        """
        
        """
        local_match_ids = []
        for idx, puuid in enumerate(list_puuids):
            try:
                response = self.api.match.by_puuid(self.routing, str(puuid['puuid']), count)
                for match_id in response:
                    if not self.db.session.query(exists().where(Match.match_id == match_id)).scalar():
                        local_match_ids.append(match_id)
            except ApiError as err:
                print(err)
            print('Get matches by puuids... (%5d/%5d)' % (idx, len(list_puuids)))
        return sorted(list(set(local_match_ids)), reverse=True)

    def requestMatchesByList(self, list_match_ids: list):
        """
        
        """
        for idx, match_id in enumerate(list_match_ids):
            try:
                response = self.api.match.by_id(self.routing, match_id)
                if response['info']['game_datetime'] > self.season5_start_timestamp:
                    if not self.db.session.query(exists().where(Match.match_id == response['metadata']['match_id'])).scalar():
                        # FIXME:
                        gametype_id = 0
                        if response['info']['tft_game_type'] == 'standard':
                            gametype_id = 2
                        elif response['info']['tft_game_type'] == 'turbo':
                            gametype_id = 1

                        # add match to db
                        match = Match(
                            match_id=response['metadata']['match_id'],
                            setnumber=str(response['info']['tft_set_number']),
                            matched_at=int(response['info']['game_datetime']),
                            gametype_id=gametype_id)
                        self.db.session.add(match)

                        if self.db.session.query(exists().where(Match.match_id == response['metadata']['match_id'])).scalar():
                            match_id = self.db.session.query(Match).filter_by(match_id=response['metadata']['match_id']).first()
                        
                            # add participant to db
                            for participant in response['info']['participants']:
                                model_participant = Participant(
                                    gold_left=int(participant['gold_left']), 
                                    last_round=int(participant['last_round']), 
                                    level=int(participant['level']), 
                                    placement=int(participant['placement']), 
                                    players_eliminated=int(participant['players_eliminated']), 
                                    time_eliminated=int(participant['time_eliminated']), 
                                    total_damage_to_players=int(participant['total_damage_to_players']), 
                                    champions=str(participant['units']), 
                                    traits=str(participant['traits']),
                                    match_id=int(match.id))
                                self.db.session.add(model_participant)
                            self.db.commit()

            except ApiError as err:
                print(err)
            print('Get matches by match ids... (%5d/%5d)' % (idx, len(list_match_ids)))

class test_parsing_app:

    def test_requestMatchesByList(self):
        pass


if __name__ == '__main__':
    
    RIOT_API_KEY = secret.RIOT_API_KEY
    tft_watcher = TftWatcher(api_key=RIOT_API_KEY)
    region = 'KR'
    region_match = 'ASIA'

    app = TFTParsingApp()

    result = tft_watcher.league.rated_ladders(region, 'RANKED_TFT_TURBO')
    result = [x['summonerId'] for x in result[0:2]]
    puuids = app.requestPuuids(result)
    matchids = app.requestMatchIdsByList(puuids)
    matches = app.requestMatchesByList(matchids)