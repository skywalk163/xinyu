"""
pathlib模块中文封装（路径操作）
"""

import pathlib

from .base_wrapper import ChineseModuleWrapper


class PathlibWrapper(ChineseModuleWrapper):
    """pathlib模块中文封装"""

    NAME_MAP = {
        "路径": "Path",
        "纯路径": "PurePath",
        "当前目录": "Path.cwd",
        "主目录": "Path.home",
    }

    def __init__(self):
        super().__init__(module=pathlib, name_map=self.NAME_MAP)
