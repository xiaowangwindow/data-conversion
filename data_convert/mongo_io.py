import sys
import logging
from typing import List

from pymongo.cursor import Cursor
from pymongo.errors import BulkWriteError

import settings
from db import mongo

logger = logging.getLogger(__name__)


class MongoIO():
    def __init__(self,
                 mongo_manager,
                 filter_={},
                 projection=None,
                 start=0,
                 limit=sys.maxsize,
                 write_condition=[]):
        self._mongo_manager = mongo_manager
        self._filter = filter_
        self._projection = projection
        self._start = start
        self._limit = limit
        self._write_condition = write_condition
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
