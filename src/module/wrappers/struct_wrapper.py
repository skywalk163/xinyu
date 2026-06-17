"""
struct模块中文封装（二进制数据结构）
"""

import struct

from .base_wrapper import ChineseModuleWrapper


class StructWrapper(ChineseModuleWrapper):
    """struct模块中文封装"""

    NAME_MAP = {
        "打包": "pack",
        "解包": "unpack",
        "打包到": "pack_into",
        "从解包": "unpack_from",
        "计算大小": "calcsize",
        "结构": "Struct",
    }

    def __init__(self):
        super().__init__(module=struct, name_map=self.NAME_MAP)
