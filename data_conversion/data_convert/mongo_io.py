import logging
import sys
from typing import List

from pymongo.cursor import Cursor
from pymongo.errors import BulkWriteError

logger = logging.getLogger(__name__)


class MongoIO():
    def __init__(self,
                 mongo_manager,
                 write_condition_dict={},
                 **kwargs
                 ):
        self._mongo_manager = mongo_manager
        self._write_condition_dict = write_condition_dict
        self._filter = kwargs.get('filter', {})
        self._projection = kwargs.get('projection', None)
        self._start = kwargs.get('start', 0)
        self._limit = kwargs.get('limit', sys.maxsize)
        if not self._write_condition_dict:
            logger.warning(
                'no write_condition, dst_doc can\'t be inserted correctly!')

    async def run(self, operate_func):
        async for doc in self.read():
            try:
                dst_operate_doc = await operate_func(doc)
            except Exception as exc:
                logger.error(exc)
                doc.update({'error_reason': str(exc)})
                if isinstance(exc, ValueError) and len(exc.args) == 1:
                    doc.update({'error_key': exc.args[0]})
                await self.save_error(doc)
            else:
                await self.write(dst_operate_doc)

    def read(self) -> Cursor:
        cursor = self._mongo_manager.src_coll.find(self._filter,
                                                   self._projection,
                                                   no_cursor_timeout=True).skip(
            self._start).limit(self._limit)
        return cursor

    async def write(self, operate_doc):
        try:
            condition_params = {}
            for operate_method, condition_key_list in self._write_condition_dict.items():
                for condition_key in condition_key_list:
                    condition_params[condition_key] = operate_doc[operate_method][condition_key]
            await self._mongo_manager.dst_coll.update_one(
                condition_params,
                operate_doc,
                upsert=True
            )
        except Exception as exc:
            logger.error(exc)

    async def save_error(self, doc):
        try:
            if '_id' in doc:
                await self._mongo_manager.error_coll.update_one(
                    {'_id': doc['_id']},
                    {'$set': doc},
                    upsert=True
                )
            else:
                await self._mongo_manager.error_coll.insert_one(doc)
        except Exception as exc:
            logger.error(exc)

    async def write_bulk(self, doc_list: List):
        try:
            await self._mongo_manager.dst_coll.insert_many(doc_list,
                                                           ordered=False)
        except BulkWriteError:
            pass
