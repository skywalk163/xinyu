"""
gzip模块中文封装（gzip压缩）
"""

import gzip

from .base_wrapper import ChineseModuleWrapper


class GzipWrapper(ChineseModuleWrapper):
    """gzip模块中文封装"""

    NAME_MAP = {
        "打开": "open",
        "压缩": "compress",
        "解压": "decompress",
        "读取器": "GzipFile",
    }

    def __init__(self):
        super().__init__(module=gzip, name_map=self.NAME_MAP)
