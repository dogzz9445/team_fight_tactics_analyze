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
    # Configuration 
    #
    # -------------------------------------------------------------------------------
    app = TFTParsingApp()

    # -------------------------------------------------------------------------------
    # Main Loop
    # -------------------------------------------------------------------------------
    while True:
        summoners = app.requestTopSummoners()
        time.sleep(0.01)