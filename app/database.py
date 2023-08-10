from typing import Protocol

import pymongo

from app import config

mongo_client = pymongo.MongoClient(config.MONGO_URL)
db = mongo_client.scrapingbee


class JsonProtocol(Protocol):

    def model_dump(self, *args, **kwargs) -> dict:
        raise NotImplementedError


class Database:

    def save(self, data: JsonProtocol):
        '''
        save(data.to_dict())

        :param data:
        :return:
        '''
        raise NotImplementedError
