"""
doctest模块中文封装（文档测试）
"""

import doctest

from .base_wrapper import ChineseModuleWrapper


class DoctestWrapper(ChineseModuleWrapper):
    """doctest模块中文封装"""

    NAME_MAP = {
        "测试模块": "testmod",
        "测试文件": "testfile",
        "运行测试": "run_docstring_examples",
        "输出检查器": "OutputChecker",
        "文档测试器": "DocTestRunner",
    }

    def __init__(self):
        super().__init__(module=doctest, name_map=self.NAME_MAP)
