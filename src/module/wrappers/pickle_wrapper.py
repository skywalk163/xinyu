"""
pickle模块中文封装（对象序列化）
"""

import pickle

from .base_wrapper import ChineseModuleWrapper


class PickleWrapper(ChineseModuleWrapper):
    """pickle模块中文封装"""

    NAME_MAP = {
        "保存": "dump",
        "加载": "load",
        "保存字符串": "dumps",
        "加载字符串": "loads",
        "协议": "HIGHEST_PROTOCOL",
        "默认协议": "DEFAULT_PROTOCOL",
    }

    def __init__(self):
        super().__init__(module=pickle, name_map=self.NAME_MAP)
