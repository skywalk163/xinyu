"""
zipfile模块中文封装（ZIP压缩）
"""

import zipfile
from .base_wrapper import ChineseModuleWrapper


class ZipfileWrapper(ChineseModuleWrapper):
    """zipfile模块中文封装"""
    
    NAME_MAP = {
        'ZIP文件': 'ZipFile',
        '是ZIP文件': 'is_zipfile',
        '压缩目录': 'ZipFile',
        '信息': 'ZipInfo',
    }
    
    def __init__(self):
        super().__init__(module=zipfile, name_map=self.NAME_MAP)
