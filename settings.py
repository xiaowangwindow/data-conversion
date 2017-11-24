import pymongo

from utils import custom_convert
from data_convert.model import Mapper

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_USERNAME = None
MONGODB_PASSWORD = None
MONGODB_AUTHDB = 'admin'
MONGODB_DB = 'db'

MONGODB_SRC_COLL = 'src_coll'
MONGODB_DST_COLL = 'dst_coll'
MONGODB_DST_COLL_INDEX = [
    ([('url', pymongo.ASCENDING)], {'unique': True}),
]

MAPPING = []
