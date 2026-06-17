"""
locale模块中文封装（本地化）
"""

import locale

from .base_wrapper import ChineseModuleWrapper


class LocaleWrapper(ChineseModuleWrapper):
    """locale模块中文封装"""

    NAME_MAP = {
        "设置": "setlocale",
        "获取": "getlocale",
        "获取默认": "getdefaultlocale",
        "格式化字符串": "format_string",
        "格式化": "format",
        "货币符号": "currency",
        "比较字符串": "strcoll",
    }

    def __init__(self):
        super().__init__(module=locale, name_map=self.NAME_MAP)
