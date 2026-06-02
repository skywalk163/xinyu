"""
fnmatch模块中文封装（文件名匹配）
"""

import fnmatch
from .base_wrapper import ChineseModuleWrapper


class FnmatchWrapper(ChineseModuleWrapper):
    """fnmatch模块中文封装"""
    
    NAME_MAP = {
        '匹配': 'fnmatch',
        '匹配大小写': 'fnmatchcase',
        '过滤': 'filter',
        '转义': 'translate',
    }
    
    def __init__(self):
        super().__init__(module=fnmatch, name_map=self.NAME_MAP)
