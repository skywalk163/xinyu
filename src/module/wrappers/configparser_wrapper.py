"""
configparser模块中文封装（配置文件）
"""

import configparser

from .base_wrapper import ChineseModuleWrapper


class ConfigparserWrapper(ChineseModuleWrapper):
    """configparser模块中文封装"""

    NAME_MAP = {
        "配置解析器": "ConfigParser",
        "安全配置解析器": "SafeConfigParser",
        "原始配置解析器": "RawConfigParser",
        "读取": "read",
        "写入": "write",
    }

    def __init__(self):
        super().__init__(module=configparser, name_map=self.NAME_MAP)
