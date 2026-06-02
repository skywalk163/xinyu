"""
re模块中文封装（正则表达式）
"""

import re
from .base_wrapper import ChineseModuleWrapper


class ReWrapper(ChineseModuleWrapper):
    """re模块中文封装"""
    
    NAME_MAP = {
        '匹配': 'match',
        '搜索': 'search',
        '查找所有': 'findall',
        '查找迭代': 'finditer',
        '替换': 'sub',
        '替换计数': 'subn',
        '分割': 'split',
        '转义': 'escape',
        '编译': 'compile',
    }
    
    def __init__(self):
        super().__init__(module=re, name_map=self.NAME_MAP)
