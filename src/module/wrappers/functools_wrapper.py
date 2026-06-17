"""
functools模块中文封装（高阶函数工具）
"""

import functools

from .base_wrapper import ChineseModuleWrapper


class FunctoolsWrapper(ChineseModuleWrapper):
    """functools模块中文封装"""

    NAME_MAP = {
        "缓存": "cache",
        "记忆化": "lru_cache",
        "偏函数": "partial",
        "归约": "reduce",
        "包装器": "wraps",
        "总排序": "total_ordering",
    }

    def __init__(self):
        super().__init__(module=functools, name_map=self.NAME_MAP)
