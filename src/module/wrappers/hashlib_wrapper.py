"""
hashlib模块中文封装（哈希算法）
"""

import hashlib

from .base_wrapper import ChineseModuleWrapper


class HashlibWrapper(ChineseModuleWrapper):
    """hashlib模块中文封装"""

    NAME_MAP = {
        "MD5": "md5",
        "SHA1": "sha1",
        "SHA224": "sha224",
        "SHA256": "sha256",
        "SHA384": "sha384",
        "SHA512": "sha512",
        "新哈希": "new",
        "算法列表": "algorithms_available",
        "保证算法": "algorithms_guaranteed",
    }

    def __init__(self):
        super().__init__(module=hashlib, name_map=self.NAME_MAP)
