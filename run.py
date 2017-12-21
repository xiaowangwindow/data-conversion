import asyncio
import datetime
import importlib
import logging
from functools import partial
from pathlib import PurePosixPath

import sys

from data_convert import core
from data_convert import mongo_io
from db import mongo

try:
    if len(sys.argv) == 2:
        module_name = PurePosixPath(sys.argv[1]).stem
        logging.warning('Import {} as Settings'.format(module_name))
        settings = importlib.import_module(module_name)
    else:
        import settings
except:
    if not settings:
        import settings

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
