"""
urllib模块中文封装（URL处理）
"""

import urllib

from .base_wrapper import ChineseModuleWrapper


class UrllibWrapper(ChineseModuleWrapper):
    """urllib模块中文封装"""

    NAME_MAP = {
        "请求": "request",
        "解析": "parse",
        "错误": "error",
        "机器人": "robotparser",
    }

    def __init__(self):
        super().__init__(module=urllib, name_map=self.NAME_MAP)
