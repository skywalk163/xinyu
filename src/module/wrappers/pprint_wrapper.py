"""
pprint模块中文封装（格式化打印）
"""

import pprint
from .base_wrapper import ChineseModuleWrapper


class PprintWrapper(ChineseModuleWrapper):
    """pprint模块中文封装"""
    
    NAME_MAP = {
        '美化打印': 'pprint',
        '格式化': 'pformat',
        '安全美化打印': 'saferepr',
        '是否可读': 'isreadable',
        '是否递归': 'isrecursive',
        '美化打印机': 'PrettyPrinter',
    }
    
    def __init__(self):
        super().__init__(module=pprint, name_map=self.NAME_MAP)
