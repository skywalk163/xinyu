"""
collections模块中文封装（高级数据结构）
"""

import collections
from .base_wrapper import ChineseModuleWrapper


class CollectionsWrapper(ChineseModuleWrapper):
    """collections模块中文封装"""
    
    NAME_MAP = {
        '计数器': 'Counter',
        '默认字典': 'defaultdict',
        '有序字典': 'OrderedDict',
        '命名元组': 'namedtuple',
        '双端队列': 'deque',
        '链式映射': 'ChainMap',
    }
    
    def __init__(self):
        super().__init__(module=collections, name_map=self.NAME_MAP)
