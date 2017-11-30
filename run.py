import importlib
import logging
import sys

try:
    if len(sys.argv) == 2:
        logging.warning('Import {} as Settings'.format(sys.argv[1]))
        settings = importlib.import_module(sys.argv[1])
    else:
        import settings
except:
    if not settings:
        import settings

import asyncio
import datetime
from typing import List
from functools import partial
from copy import deepcopy
from concurrent.futures import ProcessPoolExecutor

from db import mongo
from data_convert import mongo_io
from data_convert import core
from data_convert.util import pp

logging.getLogger('').setLevel(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


async def io_convert(mongo_manager, query):
    io = mongo_io.MongoIO(
        mongo_manager,
        write_condition=settings.WRITE_CONDITION,
        **query
    )
    for MAPPING in settings.MAPPING_LIST:
        await io.run(partial(core.convert, MAPPING))


async def run():
    async_mongo_manager = mongo.MotorMongoManager.from_settings(settings)
    await async_mongo_manager.setup_dst_coll_index()
    await async_mongo_manager.setup_error_coll_index()
    await io_convert(async_mongo_manager, settings.SRC_COLL_QUERY)


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    logger.info('Start At: {}'.format(start_time))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

    end_time = datetime.datetime.now()
    logger.info('End At: {}'.format(end_time))
    logger.info('Cost Time: {}'.format(end_time - start_time))
