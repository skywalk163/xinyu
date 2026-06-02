"""
dbm模块中文封装（DBM数据库）
"""

import dbm
from .base_wrapper import ChineseModuleWrapper


class DbmWrapper(ChineseModuleWrapper):
    """dbm模块中文封装"""
    
    NAME_MAP = {
        '打开': 'open',
        '哪个数据库': 'whichdb',
    }
    
    def __init__(self):
        super().__init__(module=dbm, name_map=self.NAME_MAP)
