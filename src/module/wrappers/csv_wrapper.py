"""
csv模块中文封装（CSV文件处理）
"""

import csv
from .base_wrapper import ChineseModuleWrapper


class CsvWrapper(ChineseModuleWrapper):
    """csv模块中文封装"""
    
    NAME_MAP = {
        '读取器': 'reader',
        '写入器': 'writer',
        '字典读取器': 'DictReader',
        '字典写入器': 'DictWriter',
        '注册方言': 'register_dialect',
        '获取方言': 'get_dialect',
        '列出方言': 'list_dialects',
        '字段大小限制': 'field_size_limit',
    }
    
    def __init__(self):
        super().__init__(module=csv, name_map=self.NAME_MAP)
