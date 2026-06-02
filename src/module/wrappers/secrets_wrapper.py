"""
secrets模块中文封装（安全随机数）
"""

import secrets
from .base_wrapper import ChineseModuleWrapper


class SecretsWrapper(ChineseModuleWrapper):
    """secrets模块中文封装"""
    
    NAME_MAP = {
        '随机字节': 'token_bytes',
        '随机十六进制': 'token_hex',
        '随机URL安全字符串': 'token_urlsafe',
        '随机选择': 'choice',
        '随机整数': 'randbelow',
        '随机位数': 'randbits',
        '比较摘要': 'compare_digest',
    }
    
    def __init__(self):
        super().__init__(module=secrets, name_map=self.NAME_MAP)
