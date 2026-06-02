"""
typing模块中文封装（类型提示）
"""

import typing
from .base_wrapper import ChineseModuleWrapper


class TypingWrapper(ChineseModuleWrapper):
    """typing模块中文封装"""
    
    NAME_MAP = {
        '列表': 'List',
        '字典': 'Dict',
        '集合': 'Set',
        '元组': 'Tuple',
        '可选': 'Optional',
        '联合': 'Union',
        '任意': 'Any',
        '类型变量': 'TypeVar',
        '泛型': 'Generic',
        '可调用': 'Callable',
        '序列': 'Sequence',
        '映射': 'Mapping',
        '可迭代': 'Iterable',
        '迭代器': 'Iterator',
    }
    
    def __init__(self):
        super().__init__(module=typing, name_map=self.NAME_MAP)
