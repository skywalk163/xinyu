"""
zlib模块中文封装（zlib压缩）
"""

import zlib

from .base_wrapper import ChineseModuleWrapper


class ZlibWrapper(ChineseModuleWrapper):
    """zlib模块中文封装"""

    NAME_MAP = {
        "压缩": "compress",
        "解压": "decompress",
        "压缩对象": "compressobj",
        "解压对象": "decompressobj",
        "计算校验和": "crc32",
        "计算哈希": "adler32",
    }

    def __init__(self):
        super().__init__(module=zlib, name_map=self.NAME_MAP)
