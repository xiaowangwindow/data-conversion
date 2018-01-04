================
Data-Conversion
================

Data-Conversion is a framework to convert data from origin style to target style easily.
With custom settings, data-conversion can read data from MongoDB, convert
data by MAPPING Rules in settings, and save to destination collection in MongoDB.

How to Use
===========

First, you should create a new settings file, for example, `settings_release.py`.
Then, define custom settings like Setting Template File `settings.py`, whose arguments also describe below.
Finally, run asynchronously:

```
python run_async.py settings_release
```
or run synchronously:

```
python run.py settings_release
```


Settings
==========

| Argument                 | Description                                                                                | Value Example                                                                            |
|--------------------------|--------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| MONGODB_HOST             | Host of MongoDB which store origin data                                                    | '127.0.0.1'                                                                              |
| MONGODB_PORT             | Port of MongoDB which store origin data                                                    | 27017                                                                                    |
| MONGODB_USERNAME         | Username of MongoDB which store origin data                                                | None / 'admin'                                                                           |
| MONGODB_PASSWORD         | Password of MongoDB which store origin data                                                | None / '123456'                                                                          |
| MONGODB_AUTHDB           | DB of authorization which store username and password                                      | 'admin'                                                                                  |
| MONGODB_DB               | DB of MongoDB which store origin data and will store result data                           | 'data'                                                                                   |
| MONGODB_SRC_COLL         | Source Collection of MongoDB which store origin data                                       | 'src_coll'                                                                               |
| MONGODB_DST_COLL         | Destination Collection of MongoDB which will store result data                             | 'dst_coll'                                                                               |
| MONGODB_DST_COLL_INDEX   | Destination Collection Index of MongoDB which store result data                            | [([('url', pymongo.ASCENDING)], {'unique':True}), ([('domain', pymongo.ASCENDING)], {})] |
| MONGODB_ERROR_COLL       | Error Collection of MongoDB which will store error data when convert raise exception       | 'error_coll'                                                                             |
| MONGODB_ERROR_COLL_INDEX | Collection Index of Error Collection of MongoDB                                            | [([('url', pymongo.ASCENDING)], {'unique': True})]                                       |
| SRC_COLL_QUERY           | Query condition to select documents to be converted                                        | { 'filter': {}, 'projection': None, 'start': 0, 'limit': 1000 }                          |
| WRITE_CONDITION          | write to dst_coll which collection.update({CONDITION}, {$set:{dst_document}}, upsert=True) | ['url']                                                                                  |
| MAPPING                  | list to mapper, rules of conversion                                                        | [Mapper('url', 'url', str, None)] // src_key, dst_key, dst_type, custom_convert_function |
| MAPPING_LIST             | list of mapping, convert by MAPPING in order                                               | [MAPPING1, MAPPING2]                                                                     |
| PROCESS_NUM              | Number of process to run conversion                                                        | 1                                                                                        |
| CONCURRENT_PER_PROCESS   | number of concurrent group to run in one process                                           | 100                                                                                      |
| LOG_LEVEL                | Level of logging                                                                           | logging.INFO                                                                             |

Settings explain
==================
The most important part in settings is MAPPING. MAPPING contains a list of Mapper,
which is a namedtuple (src_key, dst_key, dst_type, custom_convert).
dst_type and custom_convert can be `None` if you want to preserve origin type and value.


Exception Handling
===================
Exception occured in convert function will be save into error collection which
defined in settings.

If you want to record the key of document which excpetion raise, you can
raise ValueError('key') contains `key` as an argument. 
