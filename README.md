# team_fight_tactics_analyze


# TFTStaticDataManager

champion and item icons static data for jupyter-notebook(IPython)

```python
from TFTStaticDataManager import TFTStaticDataManager

tft_static_data_manager = TFTStaticDataManager()
tft_static_data_manager.GetItemIconByItemId(1049)
```
![alt text](https://raw.communitydragon.org/latest/game/assets/maps/particles/tft/item_icons/shadow/s_hand_of_justice.png)

```python
tft_static_data_manager.GetChampionIconByApiName('TFT5_Riven')
```
![alt text](https://raw.communitydragon.org/latest/game/assets/characters/tft5_riven/hud/tft5_riven_square.tft_set5.png)