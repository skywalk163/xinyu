"""
json模块中文封装
"""

import json

from .base_wrapper import ChineseModuleWrapper


class JsonWrapper(ChineseModuleWrapper):
    """json模块中文封装"""

    NAME_MAP = {
        "加载": "load",
        "保存": "dump",
        "加载字符串": "loads",
        "转字符串": "dumps",
    }

    def __init__(self):
        super().__init__(module=json, name_map=self.NAME_MAP)
