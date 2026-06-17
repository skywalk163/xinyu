"""
traceback模块中文封装（堆栈跟踪）
"""

import traceback

from .base_wrapper import ChineseModuleWrapper


class TracebackWrapper(ChineseModuleWrapper):
    """traceback模块中文封装"""

    NAME_MAP = {
        "打印异常": "print_exc",
        "打印最后异常": "print_last",
        "打印堆栈": "print_stack",
        "格式异常": "format_exc",
        "格式堆栈": "format_stack",
        "提取堆栈": "extract_stack",
        "提取异常": "extract_tb",
    }

    def __init__(self):
        super().__init__(module=traceback, name_map=self.NAME_MAP)
