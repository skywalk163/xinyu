"""
异常转换器

将Python异常转换为心语异常。
"""

from .xinyu_exceptions import (
    XinyuAttributeError,
    XinyuException,
    XinyuImportError,
    XinyuIndexError,
    XinyuKeyError,
    XinyuNameError,
    XinyuRuntimeError,
    XinyuTypeError,
    XinyuValueError,
)


class ExceptionTranslator:
    """异常转换器"""

    def translate(self, exception: Exception) -> XinyuException:
        """转换异常"""
        # 占位实现，将在任务4中完善
        exception_map = {
            TypeError: XinyuTypeError,
            ValueError: XinyuValueError,
            AttributeError: XinyuAttributeError,
            KeyError: XinyuKeyError,
            IndexError: XinyuIndexError,
            ImportError: XinyuImportError,
            NameError: XinyuNameError,
            RuntimeError: XinyuRuntimeError,
        }

        exception_class = exception_map.get(type(exception), XinyuException)
        chinese_message = self.get_chinese_message(exception)

        return exception_class(chinese_message, original_exception=exception)

    def get_chinese_message(self, exception: Exception) -> str:
        """获取中文错误信息"""
        # 占位实现，将在任务4中完善
        return str(exception)
