import abc

import pymongo

from app import config

mongo_client = pymongo.MongoClient(config.MONGO_URL)
db = mongo_client.scrapingbee


class ToDict(abc.ABC):

    @abc.abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError


class Database:

    def save(self, data: ToDict):
        '''
        save(data.to_dict())

        :param data:
        :return:
        '''
        raise NotImplementedError
