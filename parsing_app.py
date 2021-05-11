from riotwatcher import TftWatcher, ApiError
import secret

class TFTParsingApp:
    self.api = TftWatcher(api_key=secret.RIOT_API_KEY)

    def __init__(self):
        pass