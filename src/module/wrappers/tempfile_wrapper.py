"""
tempfile模块中文封装（临时文件）
"""

import tempfile

from .base_wrapper import ChineseModuleWrapper


class TempfileWrapper(ChineseModuleWrapper):
    """tempfile模块中文封装"""

    NAME_MAP = {
        "临时文件": "TemporaryFile",
        "命名临时文件": "NamedTemporaryFile",
        "临时目录": "TemporaryDirectory",
        "获取临时目录": "gettempdir",
        "获取临时目录名": "gettempdirb",
        "模板": "template",
    }

    def __init__(self):
        super().__init__(module=tempfile, name_map=self.NAME_MAP)
