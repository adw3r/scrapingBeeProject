import sys
import os
import pathlib

import dotenv
import loguru

dotenv.load_dotenv()

ROOT_FOLDER = pathlib.Path(__file__).parent
APIKEY_PATH = pathlib.Path(ROOT_FOLDER, 'apikeys.json')

SCRAPINGBEE_APIKEY = os.environ['SCRAPINGBEE_APIKEY']
MONGO_URL = 'mongodb://root:example@10.107.8.10:27017'  # move to .env

config = {
    "handlers": [
        {"sink": sys.stdout, 'level': 'DEBUG'},
        # {"sink": pathlib.Path(ROOT_FOLDER, "logs.log"), 'level': 'DEBUG', 'retention': '2 days'},
    ],
}
logger = loguru.logger
logger.configure(**config)
