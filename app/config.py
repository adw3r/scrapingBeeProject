import sys
import os
import pathlib

import dotenv
import loguru

ROOT_FOLDER = pathlib.Path(__file__).parent.parent
__ENV_CONFIG = dotenv.dotenv_values(ROOT_FOLDER / '.env')

APIKEY_PATH = pathlib.Path(ROOT_FOLDER, 'apikeys.jsonc')

SCRAPINGBEE_APIKEY = __ENV_CONFIG['SCRAPINGBEE_APIKEY']
MONGO_URL = __ENV_CONFIG['MONGO_DB_URL']  # move to .env

logging_config = {
    "handlers": [
        {"sink": sys.stdout, 'level': 'DEBUG'},
        # {"sink": pathlib.Path(ROOT_FOLDER, "logs.log"), 'level': 'DEBUG', 'retention': '2 days'},
    ],
}
logger = loguru.logger
logger.configure(**logging_config)
