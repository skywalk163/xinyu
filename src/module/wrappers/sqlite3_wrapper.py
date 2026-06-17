"""
sqlite3模块中文封装（SQLite数据库）
"""

import sqlite3

from .base_wrapper import ChineseModuleWrapper


class Sqlite3Wrapper(ChineseModuleWrapper):
    """sqlite3模块中文封装"""

    NAME_MAP = {
        "连接": "connect",
        "数据库": "Connection",
        "游标": "Cursor",
        "行": "Row",
        "注册适配器": "register_adapter",
        "注册转换器": "register_converter",
    }

    def __init__(self):
        super().__init__(module=sqlite3, name_map=self.NAME_MAP)
