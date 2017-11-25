import importlib
import sys
import asyncio
import datetime
import pymongo
import logging
import math
from typing import List
from functools import partial
from copy import deepcopy
from concurrent.futures import ProcessPoolExecutor

from db import mongo
from data_convert import mongo_io
from data_convert import core
from data_convert.util import pp
from run import io_convert, settings

async_mongo_manager = mongo.MotorMongoManager.from_settings(settings)
logging.getLogger('').setLevel(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


def run_process(query_condition):
    start, end, batch_size = query_condition
    asyncio.get_event_loop().run_until_complete(
        asyncio.gather(*[
            io_convert(async_mongo_manager, {
                'filter': settings.SRC_COLL_QUERY.get('filter', {}),
                'projection': settings.SRC_COLL_QUERY.get('projection', None),
                'start': index,
                'limit': batch_size
            }) for index in range(start, end, batch_size)
        ])
    )


def run_by_multiprocess():
    sync_mongo_manager = mongo.PyMongoManager.from_settings(settings)
    sync_mongo_manager.setup_dst_coll_index()

    total_count = settings.SRC_COLL_QUERY.get('limit', None)
    if total_count is None:
        total_count = sync_mongo_manager.src_coll.count(
            settings.SRC_COLL_QUERY.get('filter', {})
        )
    batch_size = (
        math.ceil(total_count /
            (settings.CONCURRENT_PER_PROCESS * settings.PROCESS_NUM))
    )
    process_batch_size = batch_size * settings.CONCURRENT_PER_PROCESS
    start = settings.SRC_COLL_QUERY.get('start', 0)
    end = start + total_count + 1
    with ProcessPoolExecutor(settings.PROCESS_NUM) as executor:
        executor.map(run_process,
                     [(index, index + process_batch_size, batch_size)
                       for index in range(start, end, process_batch_size)])


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    logger.info('Start At: {}'.format(start_time))

    run_by_multiprocess()

    end_time = datetime.datetime.now()
    logger.info('End At: {}'.format(end_time))
    logger.info('Cost Time: {}'.format(end_time-start_time))
