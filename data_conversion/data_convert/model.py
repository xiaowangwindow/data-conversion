from collections import namedtuple

Mapper = namedtuple('Mapper',
                    ['src_key', 'dst_key', 'value_type', 'convert_func'])
