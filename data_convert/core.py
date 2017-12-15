import inspect
from typing import AnyStr, Dict, List
from collections import namedtuple
from data_convert.util import pp

from data_convert import data_mock
from data_convert.model import Mapper


async def convert(mapping: List[Mapper], src_doc: Dict) -> Dict:
    '''
    convert Data
    :param src_doc:
    :param dst_doc:
    :param mapping: [(src_key, dst_key, type, convert_func=None)]
    :return:
    '''
    res = {}
    for mapper in mapping:
        res.update(await convert_by_mapper(mapper, src_doc))
    return res


async def convert_by_mapper(mapper: Mapper, src_doc: Dict) -> Dict:
    '''
    convert src_doc to dst_doc by Mapper
    :param src_doc:
    :param mapper:
    :return:
    '''
    if mapper.src_key is None or mapper.dst_key is None:
        return {}
    mid_doc = src_doc
    for field in mapper.src_key.split('.'):
        if not field:
            break
        mid_doc = mid_doc.get(field, {})

    if mapper.convert_func:
        if inspect.iscoroutinefunction(mapper.convert_func):
            mid_doc = await mapper.convert_func(mid_doc)
        else:
            mid_doc = mapper.convert_func(mid_doc)

    if not mid_doc:
        return {}

    if not mapper.value_type or isinstance(mid_doc, mapper.value_type):
        return {mapper.dst_key: mid_doc}
    else:
        return {mapper.dst_key: mapper.value_type(mid_doc)}


if __name__ == '__main__':
    def convert_value(doc):
        return doc + 'abc'

    mapping = [
        Mapper('http.url', 'url', str, None),
    ]

    res = convert(mapping, data_mock.src_doc)
    pp.pprint(res)
