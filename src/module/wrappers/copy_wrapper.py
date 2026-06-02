"""
copy模块中文封装（对象复制）
"""

import copy
from .base_wrapper import ChineseModuleWrapper


class CopyWrapper(ChineseModuleWrapper):
    """copy模块中文封装"""
    
    NAME_MAP = {
        '浅复制': 'copy',
        '深复制': 'deepcopy',
    }
    
    def __init__(self):
        super().__init__(module=copy, name_map=self.NAME_MAP)
