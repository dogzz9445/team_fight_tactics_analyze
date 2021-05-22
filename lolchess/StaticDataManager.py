import os
import requests
import json
from IPython.display import Image

class StaticDataManager:
    
    def __init__(self):
        self.set_number = '5'
        self.static_data_path = 'data/set5/latest/'
        self.static_character_icon_path = self.static_data_path + 'assets/characters/'
        self.latest_url = 'http://raw.communitydragon.org/latest/'
        self.latest_game_url = self.latest_url + 'game/'
        self.latest_character_url = self.latest_game_url + 'assets/characters/'
        if os.path.exists('../data/set5/ko_kr.json') == True:
            self.json_ko_kr = json.load('../data/set5/ko_kr.json')
        else:
            self.json_ko_kr = requests.get(self.latest_url + 'cdragon/tft/ko_kr.json').json()
        if os.path.exists('../data/set5/en_us.json') == True:
            self.json_en_us = json.load('../data/set5/en_us.json')
        else:
            self.json_en_us = requests.get(self.latest_url + 'cdragon/tft/en_us.json').json()
        
    #
    # 아이템
    #
    
    """
    base
    """
    def GetItemById(self, value_json, item_id: int):
        return list(filter(lambda x: x['id'] == item_id, value_json['items']))

    def GetKoreanItemNameById(self, item_id: int):
        list_items = self.GetItemById(self.json_ko_kr, item_id)
        if list_items:
            return list_items[0]['name']
        return 'error: %d' % item_id

    def GetEnglishItemNameById(self, item_id: int):
        list_items = self.GetItemById(self.json_en_us, item_id)
        if list_items:
            return list_items[0]['name']
        return 'error: %d' % item_id

    def GetItemIconByItemId(self, id: int):
        list_items = self.GetItemById(self.json_en_us, id)
        if list_items:
            icon_url = (os.path.splitext(list_items[0]['icon'])[0] + '.png').lower()
            icon_path, icon_filename = os.path.split(icon_url)
            if os.path.exists(self.static_data_path + icon_url):
                return Image(filename=self.static_data_path + icon_url)
            else:
                try:
                    response = requests.get(self.latest_game_url + icon_url)
                except requests.HTTPError as err:
                    print(err)
                    return None
                if not os.path.exists(self.static_data_path + icon_path):
                    os.makedirs(self.static_data_path + icon_path)
                with open(self.static_data_path + icon_url, 'wb') as out_file:
                    out_file.write(response.content)                
                return Image(response.content)
    
    #
    # 챔피온
    #
        
    """
    base
    """
    def GetChampion(self, value_json, api_name: str):
        for champions in value_json['setData']:
            for champion in champions['champions']:
                if champion['apiName'] == api_name:
                    return champion
        return 'error: %d' % id
    
    def GetChampionEnglish(self, api_name: str):
        return self.GetChampion(self.json_en_us, api_name)

    def GetChampionKorean(self, api_name: str):
        return self.GetChampion(self.json_ko_kr, api_name)
    
    def GetChampionEnglishName(self, api_name: str):
        return self.GetChampion(self.json_en_us, api_name)['name']

    def GetChampionKoreanName(self, api_name: str):
        return self.GetChampion(self.json_ko_kr, api_name)['name']

    def GetChampionIcon(self, api_name: str):
        icon_file_name = (api_name + '_square.tft_set5.png').lower()
        local_file_path = (self.static_character_icon_path + api_name + '/hud/').lower()
        cdragon_url = (self.latest_character_url + api_name + '/hud/' + icon_file_name).lower()
        if os.path.exists(local_file_path + icon_file_name):
            return Image(filename=local_file_path + icon_file_name)
        else:
            try:
                response = requests.get(cdragon_url)
            except requests.HTTPError as err:
                print(err)
                return None
            if not os.path.exists(local_file_path):
                os.makedirs(local_file_path)
            with open(local_file_path + icon_file_name, 'wb') as out_file:
                out_file.write(response.content)                
            return Image(response.content)

    #
    # 시너지
    #

    """
    base
    """
    def GetTrait(self, ref_json, api_name: str):
        for trait in ref_json['sets'][self.set_number]['traits']:
            if trait['apiName'] == api_name:
                return trait
        return None
    
    def GetTraitKorean(self, api_name: str):
        return self.GetTrait(self.json_ko_kr, api_name)

    def GetTraitEnglish(self, api_name: str):
        return self.GetTrait(self.json_ko_kr, api_name)

    def GetTraitKoreanName(self, api_name: str):
        return self.GetTrait(self.json_ko_kr, api_name)['name']

    def GetTraitEnglishName(self, api_name: str):
        return self.GetTrait(self.json_ko_kr, api_name)['name']
