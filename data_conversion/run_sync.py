import asyncio
import datetime
import importlib
import importlib.util
import logging
import sys
from functools import partial
from pathlib import PurePosixPath

from data_conversion.data_convert import core
from data_conversion.data_convert import mongo_io
from data_conversion.db import mongo

try:
    if len(sys.argv) == 2:
        settings_path = sys.argv[1]
        settings_name = PurePosixPath(settings_path).stem
        module_name = 'settings'
        spec = importlib.util.spec_from_file_location(module_name, settings_path)
        settings = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(settings)
        logging.warning('Import {} as Settings'.format(settings_name))
    else:
        from data_conversion import settings
except Exception as exc:
    logging.error('Import Settings Error: {}'.format(exc))
    from data_conversion import settings

logging.getLogger('').setLevel(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


async def io_convert(mongo_manager, query):
    io = mongo_io.MongoIO(
        mongo_manager,
        write_condition_dict=settings.WRITE_CONDITION_DICT,
        **query
    )
    await io.run(partial(core.convert_by_operate_dict, settings.OPERATE_MAPPING_DICT))


async def run():
    async_mongo_manager = mongo.MotorMongoManager.from_settings(settings)
    await async_mongo_manager.setup_dst_coll_index()
    await async_mongo_manager.setup_error_coll_index()
    await io_convert(async_mongo_manager, settings.SRC_COLL_QUERY)


def sync_entrypoint():
    start_time = datetime.datetime.now()
    logger.info('Start At: {}'.format(start_time))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

    end_time = datetime.datetime.now()
    logger.info('End At: {}'.format(end_time))
    logger.info('Cost Time: {}'.format(end_time - start_time))


if __name__ == '__main__':
    sync_entrypoint()
