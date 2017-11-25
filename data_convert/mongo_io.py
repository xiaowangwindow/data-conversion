import sys
import logging
from typing import List

from pymongo.cursor import Cursor
from pymongo.errors import BulkWriteError

from db import mongo

logger = logging.getLogger(__name__)


class MongoIO():
    def __init__(self,
                 mongo_manager,
                 write_condition=[],
                 **kwargs
                 ):
        self._mongo_manager = mongo_manager
        self._write_condition = write_condition
        self._filter = kwargs.get('filter', {})
        self._projection = kwargs.get('projection', None)
        self._start = kwargs.get('start', 0)
        self._limit = kwargs.get('limit', sys.maxsize)
        if not self._write_condition:
            logger.warning('no write_condition, dst_doc can\'t be inserted correctly!')

    async def run(self, operate_func):
        async for doc in self.read():
            dst_doc = operate_func(doc)
            await self.write(dst_doc)

    def read(self) -> Cursor:
        cursor = self._mongo_manager.src_coll.find(self._filter,
                                                   self._projection).skip(
            self._start).limit(self._limit)
        return cursor

    async def write(self, doc):
        try:
            await self._mongo_manager.dst_coll.update_one(
                {condition: doc[condition] for condition in
                 self._write_condition},
                {'$set': doc},
                upsert=True
            )
        except Exception as exc:
            logger.error(exc)

    async def write_bulk(self, doc_list: List):
        try:
            await self._mongo_manager.dst_coll.insert_many(doc_list,
                                                           ordered=False)
        except BulkWriteError:
            pass
