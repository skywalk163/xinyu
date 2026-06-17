"""
linecache模块中文封装（行缓存）
"""

import linecache

from .base_wrapper import ChineseModuleWrapper


class LinecacheWrapper(ChineseModuleWrapper):
    """linecache模块中文封装"""

    NAME_MAP = {
        "获取行": "getline",
        "获取行们": "getlines",
        "清空缓存": "clearcache",
        "检查缓存": "checkcache",
        "更新缓存": "updatecache",
    }

    def __init__(self):
        super().__init__(module=linecache, name_map=self.NAME_MAP)
