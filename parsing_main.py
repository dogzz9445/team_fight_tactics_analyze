from datetime import datetime
import importlib
from parsing_app import TFTParsingApp
import pickle
import time
import asyncio

from riotwatcher import TftWatcher, ApiError
import secret

if __name__ == '__main__':
    # -------------------------------------------------------------------------------
    #
    # Configuration 
    #
    # -------------------------------------------------------------------------------
    

    # -------------------------------------------------------------------------------
    #
    # Initializing
    #
    # -------------------------------------------------------------------------------
    app = TFTParsingApp()

    # -------------------------------------------------------------------------------
    # Main Loop
    # -------------------------------------------------------------------------------
    while True:
        summoners = app.requestTopSummoners()
        puuids = app.requestPuuids(summoners['standard'] + summoners['turbo'])
        matchids = app.requestMatchIdsByList(puuids)
        matches = app.requestMatchesByList(matchids)

        time.sleep(0.01)
        
        if datetime.now() > datetime(2021, 5, 16, 15, 0, 0):
            break