"""
心语异常类定义

定义心语语言专用的异常类。
"""

from typing import Optional


class XinyuException(Exception):
    """心语异常基类"""

    def __init__(self, message: str, original_exception: Optional[Exception] = None):
        """
        初始化异常

        Args:
            message: 中文错误信息
            original_exception: 原始Python异常
        """
        super().__init__(message)
        self.message = message
        self.original_exception = original_exception


class XinyuTypeError(XinyuException):
    """类型错误"""


class XinyuValueError(XinyuException):
    """值错误"""


class XinyuAttributeError(XinyuException):
    """属性错误"""


class XinyuKeyError(XinyuException):
    """键错误"""


class XinyuIndexError(XinyuException):
    """索引错误"""


class XinyuImportError(XinyuException):
    """导入错误"""


class XinyuNameError(XinyuException):
    """名称错误"""


class XinyuRuntimeError(XinyuException):
    """运行时错误"""
