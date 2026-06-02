"""
tarfile模块中文封装（tar归档）
"""

import tarfile
from .base_wrapper import ChineseModuleWrapper


class TarfileWrapper(ChineseModuleWrapper):
    """tarfile模块中文封装"""
    
    NAME_MAP = {
        '打开': 'open',
        '是TAR文件': 'is_tarfile',
        'TAR文件': 'TarFile',
        '信息': 'TarInfo',
    }
    
    def __init__(self):
        super().__init__(module=tarfile, name_map=self.NAME_MAP)
