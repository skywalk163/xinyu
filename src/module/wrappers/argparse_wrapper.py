"""
argparse模块中文封装（命令行参数解析）
"""

import argparse

from .base_wrapper import ChineseModuleWrapper


class ArgparseWrapper(ChineseModuleWrapper):
    """argparse模块中文封装"""

    NAME_MAP = {
        "参数解析器": "ArgumentParser",
        "子解析器": "ArgumentParser",
        "动作": "Action",
        "文件类型": "FileType",
        "命名空间": "Namespace",
    }

    def __init__(self):
        super().__init__(module=argparse, name_map=self.NAME_MAP)
