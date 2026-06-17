"""
socket模块中文封装（网络套接字）
"""

import socket

from .base_wrapper import ChineseModuleWrapper


class SocketWrapper(ChineseModuleWrapper):
    """socket模块中文封装"""

    NAME_MAP = {
        "套接字": "socket",
        "创建套接字": "socket",
        "获取主机名": "gethostname",
        "获取主机地址": "gethostbyname",
        "获取主机信息": "gethostbyname_ex",
        "获取服务端口": "getservbyname",
        "获取端口服务": "getservbyport",
        "协议族": "AF_INET",
        "套接字类型": "SOCK_STREAM",
    }

    def __init__(self):
        super().__init__(module=socket, name_map=self.NAME_MAP)
