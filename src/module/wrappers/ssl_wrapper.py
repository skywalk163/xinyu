"""
ssl模块中文封装（SSL/TLS加密）
"""

import ssl
from .base_wrapper import ChineseModuleWrapper


class SslWrapper(ChineseModuleWrapper):
    """ssl模块中文封装"""
    
    NAME_MAP = {
        '创建上下文': 'create_default_context',
        '包装套接字': 'wrap_socket',
        '获取服务器证书': 'get_server_certificate',
        '证书要求': 'CERT_REQUIRED',
        '证书可选': 'CERT_OPTIONAL',
        '无证书': 'CERT_NONE',
    }
    
    def __init__(self):
        super().__init__(module=ssl, name_map=self.NAME_MAP)
