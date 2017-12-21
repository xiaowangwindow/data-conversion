import logging

import pymongo
from motor import motor_asyncio

logger = logging.getLogger(__name__)


class MotorMongoManager():
    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def __init__(self, settings):
        self._settings = settings
        self._uri = 'mongodb://{auth_info}{host}:{port}'.format(
            auth_info='{username}:{password}@'.format(
                username=self._settings.MONGODB_USERNAME,
                password=self._settings.MONGODB_PASSWORD
            ) if self._settings.MONGODB_USERNAME else '',
            host=self._settings.MONGODB_HOST,
            port=self._settings.MONGODB_PORT
        )
        self._client = motor_asyncio.AsyncIOMotorClient(self._uri)
        self._db = self._client[self._settings.MONGODB_DB]
        self._src_coll = self._db[self._settings.MONGODB_SRC_COLL]
        self._dst_coll = self._db[self._settings.MONGODB_DST_COLL]
        self._error_coll = self._db[self._settings.MONGODB_ERROR_COLL]
        logger.info('Connect to: {}'.format(self._uri))

    async def setup_dst_coll_index(self):
        for index_item, kwargs in self._settings.MONGODB_DST_COLL_INDEX:
            await self._dst_coll.create_index(index_item, **kwargs)

    async def setup_error_coll_index(self):
        for index_item, kwargs in self._settings.MONGODB_ERROR_COLL_INDEX:
            await self._error_coll.create_index(index_item, **kwargs)

    @property
    def db_uri(self):
        return self._uri

    @property
    def dst_coll(self):
        return self._dst_coll

    @property
    def src_coll(self):
        return self._src_coll

    @property
    def error_coll(self):
        return self._error_coll


class PyMongoManager():
    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def __init__(self, settings):
        self._settings = settings
        self._uri = 'mongodb://{auth_info}{host}:{port}'.format(
            auth_info='{username}:{password}@'.format(
                username=self._settings.MONGODB_USERNAME,
                password=self._settings.MONGODB_PASSWORD
            ) if self._settings.MONGODB_USERNAME else '',
            host=self._settings.MONGODB_HOST,
            port=self._settings.MONGODB_PORT
        )
        self._client = pymongo.MongoClient(self._uri)
        self._db = self._client[self._settings.MONGODB_DB]
        self._src_coll = self._db[self._settings.MONGODB_SRC_COLL]
        self._dst_coll = self._db[self._settings.MONGODB_DST_COLL]
        self._error_coll = self._db[self._settings.MONGODB_ERROR_COLL]

    def setup_dst_coll_index(self):
        for index_item, kwargs in self._settings.MONGODB_DST_COLL_INDEX:
            self._dst_coll.create_index(index_item, **kwargs)

    def setup_error_coll_index(self):
        for index_item, kwargs in self._settings.MONGODB_ERROR_COLL_INDEX:
            self._error_coll.create_index(index_item, **kwargs)

    @property
    def db_uri(self):
        return self._uri

    @property
    def dst_coll(self):
        return self._dst_coll

    @property
    def src_coll(self):
        return self._src_coll

    @property
    def error_coll(self):
        return self._error_coll
