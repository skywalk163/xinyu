"""
decimal模块中文封装（精确十进制运算）
"""

import decimal

from .base_wrapper import ChineseModuleWrapper


class DecimalWrapper(ChineseModuleWrapper):
    """decimal模块中文封装"""

    NAME_MAP = {
        "小数": "Decimal",
        "上下文": "Context",
        "获取上下文": "getcontext",
        "设置上下文": "setcontext",
        "本地上下文": "localcontext",
    }

    def __init__(self):
        super().__init__(module=decimal, name_map=self.NAME_MAP)
