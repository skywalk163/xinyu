"""
sys模块中文封装
"""

import sys

from .base_wrapper import ChineseModuleWrapper


class SysWrapper(ChineseModuleWrapper):
    """sys模块中文封装"""

    NAME_MAP = {
        "版本": "version",
        "平台": "platform",
        "退出": "exit",
        "命令行参数": "argv",
        "模块搜索路径": "path",
        "标准输入": "stdin",
        "标准输出": "stdout",
        "标准错误": "stderr",
    }

    def __init__(self):
        super().__init__(module=sys, name_map=self.NAME_MAP)
