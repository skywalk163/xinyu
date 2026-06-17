"""
unittest模块中文封装（单元测试）
"""

import unittest

from .base_wrapper import ChineseModuleWrapper


class UnittestWrapper(ChineseModuleWrapper):
    """unittest模块中文封装"""

    NAME_MAP = {
        "测试用例": "TestCase",
        "测试套件": "TestSuite",
        "测试加载器": "TestLoader",
        "测试运行器": "TextTestRunner",
        "主函数": "main",
        "跳过": "skip",
        "跳过如果": "skipIf",
        "跳过除非": "skipUnless",
        "预期失败": "expectedFailure",
    }

    def __init__(self):
        super().__init__(module=unittest, name_map=self.NAME_MAP)
