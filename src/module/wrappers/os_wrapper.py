"""
os模块中文封装
"""

import os

from .base_wrapper import ChineseModuleWrapper


class OsWrapper(ChineseModuleWrapper):
    """os模块中文封装"""

    NAME_MAP = {
        "获取当前目录": "getcwd",
        "列出目录": "listdir",
        "创建目录": "mkdir",
        "删除目录": "rmdir",
        "删除文件": "remove",
        "重命名": "rename",
        "路径存在": "path.exists",
        "是否文件": "path.isfile",
        "是否目录": "path.isdir",
        "获取环境变量": "getenv",
        "设置环境变量": "putenv",
    }

    def __init__(self):
        super().__init__(module=os, name_map=self.NAME_MAP)
