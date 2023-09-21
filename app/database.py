import abc
from typing import Iterable

import pydantic
import pymongo

from app import config, scrapingbee

mongo_client = pymongo.MongoClient(config.MONGO_URL)


class InvalidTypeError(Exception):
    ...


def _check_item(item: pydantic.BaseModel) -> pydantic.BaseModel:
    stmnt = not issubclass(type(item), pydantic.BaseModel)
    if stmnt:
        raise InvalidTypeError(f'{type(item)!r} type is not accepted!')
    return item


def _check_items(items: Iterable[pydantic.BaseModel]) -> Iterable[pydantic.BaseModel]:
    stmnt = not isinstance(items, Iterable)
    if stmnt:
        raise InvalidTypeError(f'{type(items)!r} type is not accepted!')
    [_check_item(item) for item in items]
    return items


class AbstractRepo(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def save_one(cls, item: pydantic.BaseModel):
        ...

    @classmethod
    @abc.abstractmethod
    def save_many(cls, items: Iterable[pydantic.BaseModel]):
        ...

    @classmethod
    @abc.abstractmethod
    def find(cls, *args, **kwargs) -> pydantic.BaseModel:
        ...


class OrganicResultsRepo(AbstractRepo):
    collection: pymongo.collection.Collection = mongo_client.scrapingbee.organic_results_collection
    collection.create_index('domain', unique=True)

    @classmethod
    def __save_item(cls, item: pydantic.BaseModel):
        try:
            cls.collection.insert_one(item.model_dump())
        except Exception as error:
            config.logger.error(f'{error!r}')

    @classmethod
    def save_one(cls, item: scrapingbee.OrganicResult) -> bool:
        item = _check_item(item)
        cls.__save_item(item)
        return True

    @classmethod
    def save_many(cls, items: Iterable[scrapingbee.OrganicResult]):
        items: Iterable[pydantic.BaseModel] = _check_items(items)
        for item in items:
            cls.__save_item(item)

    @classmethod
    def find(cls, *args, **kwargs) -> list[dict]:
        results: pymongo.collection.Cursor = cls.collection.find(*args, **kwargs).limit(50)
        return [res for res in results]
