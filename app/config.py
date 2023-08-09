import os
import pathlib

import dotenv

dotenv.load_dotenv()

ROOT_FOLDER = pathlib.Path(__file__).parent
APIKEY_PATH = pathlib.Path(ROOT_FOLDER, 'apikeys.json')

SCRAPINGBEE_APIKEY = os.environ['SCRAPINGBEE_APIKEY']
MONGO_URL = 'mongodb://root:example@10.107.8.10:27017'  # move to .env
