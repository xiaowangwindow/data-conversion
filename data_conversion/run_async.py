import asyncio
import datetime
import logging
import math
from concurrent.futures import ProcessPoolExecutor

from data_conversion.db import mongo
from data_conversion.run_sync import io_convert, settings

logging.getLogger('').setLevel(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


def run_process(arguments_list):
    start, end, batch_size = arguments_list
    async_mongo_manager = mongo.MotorMongoManager.from_settings(settings)
    asyncio.get_event_loop().run_until_complete(
        asyncio.gather(*[
            io_convert(async_mongo_manager, {
                'filter': settings.SRC_COLL_QUERY.get('filter', {}),
                'projection': settings.SRC_COLL_QUERY.get('projection', None),
                'start': index,
                'limit': min(batch_size, end - index)
            }) for index in range(start, end, batch_size)
        ])
    )


def run_by_multiprocess():
    sync_mongo_manager = mongo.PyMongoManager.from_settings(settings)
    sync_mongo_manager.setup_dst_coll_index()
    sync_mongo_manager.setup_error_coll_index()

    start = settings.SRC_COLL_QUERY.get('start', 0)
    total_count = settings.SRC_COLL_QUERY.get('limit', None)
    if total_count is None:
        total_count = sync_mongo_manager.src_coll.count(
            settings.SRC_COLL_QUERY.get('filter', {})
        ) - start
    batch_size = (
        math.ceil(total_count /
                  (settings.CONCURRENT_PER_PROCESS * settings.PROCESS_NUM))
    )
    process_batch_size = batch_size * settings.CONCURRENT_PER_PROCESS
    end = start + total_count
    logger.info('start: {}, end: {}, process_batch_size: {}'.format(
        start, end, process_batch_size))

    with ProcessPoolExecutor(settings.PROCESS_NUM) as executor:
        executor.map(run_process,
                     [(index, min(index + process_batch_size, end), batch_size)
                      for index in range(start, end, process_batch_size)])


def async_entrypoint():
    start_time = datetime.datetime.now()
    logger.info('Start At: {}'.format(start_time))

    run_by_multiprocess()

    end_time = datetime.datetime.now()
    logger.info('End At: {}'.format(end_time))
    logger.info('Cost Time: {}'.format(end_time - start_time))


if __name__ == '__main__':
    async_entrypoint()
