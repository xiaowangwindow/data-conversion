import logging
import os
import sys

import pymongo

from data_conversion.data_convert.model import Mapper

sys.path.append(os.path.abspath('.'))
# import your module here

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_USERNAME = None
MONGODB_PASSWORD = None
MONGODB_AUTHDB = 'admin'
MONGODB_DB = 'data'

MONGODB_SRC_COLL = 'src_coll'
MONGODB_DST_COLL = 'dst_coll'
MONGODB_DST_COLL_INDEX = [
    ([('url', pymongo.ASCENDING)], {'unique': True}),
]
MONGODB_ERROR_COLL = 'error_coll'
MONGODB_ERROR_COLL_INDEX = [
    ([('url', pymongo.ASCENDING)], {'unique': True}),
]

SRC_COLL_QUERY = {
    # 'filter': {},
    # 'projection': None,
    # 'start': 0,
    # 'limit': 1000
}
WRITE_CONDITION_DICT = {
    '$set': ['url']
}

MAPPING = [
    Mapper('url', 'url', str, None),
]

PUSH_MAPPING = []

ADD2SET_MAPPING = []

OPERATE_MAPPING_DICT = {
    '$set': MAPPING,
    '$push': PUSH_MAPPING,
    'addToSet': ADD2SET_MAPPING,
}

PROCESS_NUM = 4
CONCURRENT_PER_PROCESS = 1000

LOG_LEVEL = logging.INFO
