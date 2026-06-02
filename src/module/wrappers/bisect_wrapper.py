"""
bisect模块中文封装（二分查找）
"""

import bisect
from .base_wrapper import ChineseModuleWrapper


class BisectWrapper(ChineseModuleWrapper):
    """bisect模块中文封装"""
    
    NAME_MAP = {
        '查找位置': 'bisect',
        '查找左位置': 'bisect_left',
        '查找右位置': 'bisect_right',
        '插入': 'insort',
        '插入左边': 'insort_left',
        '插入右边': 'insort_right',
    }
    
    def __init__(self):
        super().__init__(module=bisect, name_map=self.NAME_MAP)
