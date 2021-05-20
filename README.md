# Team Fight Tactics using clustering

1.
2.
3.

# Features

# Analyze Overview
## Analyze target
- TFT standard: top 300
- TFT turbo: top 100

## Analyze method
1. 일봉, 주봉 승률
2. 챔피언별 아이템 선택률
3. 덱별 아이템 선택률 -> 핵심 아이템 없을시 평균등수
4. 개인별 유형분석
5. 군집화시 각덱 중심거리 대비 덱완성도 
6. 덱을 얼마나 종류별로 쓰는가
7. 핵심아이템은 얼마나 잘모았나
8. 순위나 점수 급등 인물 분석

# Team Fight Tactics API Parsing

# Preprocessing
1. 6레벨 이하
2. 넣은 데미지 6이하
3. 50골드 이상 7등 이하

# Optimize Clustering

# System Overview

# 

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