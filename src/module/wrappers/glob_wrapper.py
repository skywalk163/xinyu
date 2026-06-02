"""
glob模块中文封装（文件路径匹配）
"""

import glob
from .base_wrapper import ChineseModuleWrapper


class GlobWrapper(ChineseModuleWrapper):
    """glob模块中文封装"""
    
    NAME_MAP = {
        '匹配': 'glob',
        '递归匹配': 'iglob',
        '转义': 'escape',
    }
    
    def __init__(self):
        super().__init__(module=glob, name_map=self.NAME_MAP)
