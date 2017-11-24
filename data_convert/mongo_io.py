import sys
from typing import List

from pymongo.cursor import Cursor
from pymongo.errors import BulkWriteError

import settings
from db import mongo


class MongoIO():
    def __init__(self,
                 mongo_manager,
                 filter_={},
                 projection=None,
                 start=0,
                 limit=sys.maxsize):
        self._mongo_manager = mongo_manager
        self._filter = filter_
        self._projection = projection
        self._start = start
        self._limit = limit

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
            await self._mongo_manager.dst_coll.insert(doc)
        except:
            pass

    async def write_bulk(self, doc_list: List):
        try:
            await self._mongo_manager.dst_coll.insert_many(doc_list,
                                                           ordered=False)
        except BulkWriteError:
            pass
