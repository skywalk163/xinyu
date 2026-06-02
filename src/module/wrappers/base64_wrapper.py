"""
base64模块中文封装（Base64编码）
"""

import base64
from .base_wrapper import ChineseModuleWrapper


class Base64Wrapper(ChineseModuleWrapper):
    """base64模块中文封装"""
    
    NAME_MAP = {
        '编码': 'b64encode',
        '解码': 'b64decode',
        '标准编码': 'standard_b64encode',
        '标准解码': 'standard_b64decode',
        'URL编码': 'urlsafe_b64encode',
        'URL解码': 'urlsafe_b64decode',
        '十六进制编码': 'b16encode',
        '十六进制解码': 'b16decode',
        '三十二进制编码': 'b32encode',
        '三十二进制解码': 'b32decode',
    }
    
    def __init__(self):
        super().__init__(module=base64, name_map=self.NAME_MAP)
