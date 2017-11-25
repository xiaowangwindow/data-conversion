import importlib
import sys
import asyncio
import datetime
import logging
from typing import List
from functools import partial
from copy import deepcopy
from concurrent.futures import ProcessPoolExecutor

from db import mongo
from data_convert import mongo_io
from data_convert import core
from data_convert.util import pp

try:
    import settings_release as settings
except:
    import settings

async_mongo_manager = mongo.MotorMongoManager.from_settings(settings)
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)



async def io_convert(mongo_manager, query):
    io = mongo_io.MongoIO(
        mongo_manager,
        write_condition=settings.WRITE_CONDITION,
        **query
    )
    await io.run(partial(core.convert, settings.MAPPING))


async def run():
    await async_mongo_manager.setup_dst_coll_index()
    await io_convert(async_mongo_manager, settings.SRC_COLL_QUERY)



if __name__ == '__main__':
    if len(sys.argv) == 2:
        logger.info('Import {} as Settings'.format(sys.argv[1]))
        settings = importlib.import_module(sys.argv[1])

    start_time = datetime.datetime.now()
    logger.info('Start At: {}'.format(start_time))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

    end_time = datetime.datetime.now()
    logger.info('End At: {}'.format(end_time))
    logger.info('Cost Time: {}'.format(end_time-start_time))
