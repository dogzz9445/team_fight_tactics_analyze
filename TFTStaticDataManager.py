import os
from os import path
import json
import requests
from IPython.display import Image, display

class TFTStaticDataManager:
    
    def __init__(self):
        self.static_data_path = 'data/set5/latest/'
        self.static_character_icon_path = self.static_data_path + 'assets/characters/'
        self.latest_url = 'http://raw.communitydragon.org/latest/'
        self.latest_game_url = self.latest_url + 'game/'
        self.latest_character_url = self.latest_game_url + 'assets/characters/'
        self.json_ko_kr = requests.get(self.latest_url + 'cdragon/tft/ko_kr.json').json()
        self.json_en_us = requests.get(self.latest_url + 'cdragon/tft/en_us.json').json()
        
    #
    # 아이템
    #
    
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
            if path.exists(self.static_data_path + icon_url):
                return Image(filename=self.static_data_path + icon_url)
            else:
                response = requests.get(self.latest_game_url + icon_url)
                if not os.path.exists(self.static_data_path + icon_path):
                    os.makedirs(self.static_data_path + icon_path)
                with open(self.static_data_path + icon_url, 'wb') as out_file:
                    out_file.write(response.content)                
                return Image(response.content)
        return None
    
    #
    # 챔피온
    #
        
    def GetChampionByApiName(self, value_json, api_name: str):
        for champions in value_json['setData']:
            for champion in champions['champions']:
                if champion['apiName'] == api_name:
                    return champion
        return 'error: %d' % id
    
    def GetEnglishChampionNameByApiName(self, api_name: str):
        return self.GetChampionByApiName(self.json_ko_kr, api_name)

    def GetKoreanChampionNameByApiName(self, api_name: str):
        return self.GetChampionByApiName(self.json_en_us, api_name)
    
    def GetChampionIconByApiName(self, api_name: str):
        icon_file_name = (api_name + '_square.tft_set5.png').lower()
        local_file_path = (self.static_character_icon_path + api_name + '/hud/').lower()
        cdragon_url = (self.latest_character_url + api_name + '/hud/' + icon_file_name).lower()
        if path.exists(local_file_path + icon_file_name):
            return Image(filename=local_file_path + icon_file_name)
        else:
            response = requests.get(cdragon_url)
            if not os.path.exists(local_file_path):
                os.makedirs(local_file_path)
            with open(local_file_path + icon_file_name, 'wb') as out_file:
                out_file.write(response.content)                
            return Image(response.content)
        return None
            