"""
http模块中文封装（HTTP协议）
"""

import http

from .base_wrapper import ChineseModuleWrapper


class HttpWrapper(ChineseModuleWrapper):
    """http模块中文封装"""

    NAME_MAP = {
        "客户端": "client",
        "服务器": "server",
        "饼干": "cookies",
    }

    def __init__(self):
        super().__init__(module=http, name_map=self.NAME_MAP)
