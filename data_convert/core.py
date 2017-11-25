from typing import AnyStr, Dict, List
from collections import namedtuple
from data_convert.util import pp

from data_convert import data_mock
from data_convert.model import Mapper


def convert(mapping: List[Mapper], src_doc: Dict) -> Dict:
    '''
    convert Data
    :param src_doc:
    :param dst_doc:
    :param mapping: [(src_key, dst_key, type, convert_func=None)]
    :return:
    '''
    res = {}
    for mapper in mapping:
        res.update(convert_by_mapper(mapper, src_doc))
    return res


def convert_by_mapper(mapper: Mapper, src_doc: Dict) -> Dict:
    '''
    convert src_doc to dst_doc by Mapper
    :param src_doc:
    :param mapper:
    :return:
    '''
    if not mapper.src_key or not mapper.dst_key:
        return {}
    mid_doc = src_doc
    for field in mapper.src_key.split('.'):
        mid_doc = mid_doc.get(field, {})

    if mapper.convert_func:
        mid_doc = mapper.convert_func(mid_doc)

    if isinstance(mid_doc, mapper.value_type):
        return {mapper.dst_key: mid_doc}
    else:
        try:
            return {mapper.dst_key: mapper.value_type(mid_doc)}
        except:
            return {}


if __name__ == '__main__':
    def convert_value(doc):
        return doc + 'abc'

    mapping = [
        Mapper('http.url', 'url', str, None),
    ]

    res = convert(mapping, data_mock.src_doc)
    pp.pprint(res)
