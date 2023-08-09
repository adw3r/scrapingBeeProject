import pathlib

ROOT_FOLDER = pathlib.Path(__file__).parent
APIKEY_PATH = pathlib.Path(ROOT_FOLDER, 'apikeys.json')

SCRAPINGBEE_APIKEY = "M977YHXCMPJJ569DSB0B8KSKL9NRU2O2327MIDT55785T8LS9TJGDW4GFMCMOZNRVN3GPSXF0Y6DGC32"  # move to .env
MONGO_URL = 'mongodb://root:example@10.107.8.10:27017'  # move to .env
