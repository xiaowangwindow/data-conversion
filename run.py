import sys
import asyncio
from typing import List
from functools import partial

from db import mongo
from data_convert import mongo_io
from data_convert import core
from data_convert.util import pp
try:
    import settings_release as settings
except:
    import settings

mongo_manager = mongo.MotorMongoManager.from_settings(settings)

async def main():
    await mongo_manager.setup_dst_coll_index()
    io = mongo_io.MongoIO(
        mongo_manager,
        limit=10
    )
    await io.run(partial(core.convert, settings.MAPPING))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
