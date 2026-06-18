# -*- coding: utf-8 -*-
"""心语语言异常处理机制

支持异常处理：
- 尝试执行代码块
- 捕获异常
- 抛出异常
- 自定义异常类型
"""

from enum import Enum
from typing import Any, Callable, Optional


class XinyuExceptionType(Enum):
    """心语异常类型"""

    语法错误 = "SyntaxError"
    运行时错误 = "RuntimeError"
    类型错误 = "TypeError"
    值错误 = "ValueError"
    索引错误 = "IndexError"
    键错误 = "KeyError"
    除零错误 = "ZeroDivisionError"
    文件错误 = "FileError"
    导入错误 = "ImportError"
    自定义错误 = "CustomError"


class XinyuException(Exception):
    """心语异常基类"""

    def __init__(
        self,
        message: str,
        exception_type: XinyuExceptionType = XinyuExceptionType.自定义错误,
        line: Optional[int] = None,
        column: Optional[int] = None,
        suggestion: Optional[str] = None,
    ):
        """初始化异常

        Args:
            message: 错误消息
            exception_type: 异常类型
            line: 行号
            column: 列号
            suggestion: 建议信息
        """
        self.message = message
        self.exception_type = exception_type
        self.line = line
        self.column = column
        self.suggestion = suggestion

        # 构建完整错误消息
        full_message = f"{exception_type.value}: {message}"
        if line is not None:
            full_message += f" (行 {line}"
            if column is not None:
                full_message += f", 列 {column}"
            full_message += ")"
        if suggestion:
            full_message += f"\n  建议: {suggestion}"

        super().__init__(full_message)


class TryBlock:
    """尝试块"""

    def __init__(self):
        """初始化尝试块"""
        self.try_code: Optional[Callable] = None
        self.except_handlers: dict = {}
        self.finally_code: Optional[Callable] = None
        self.else_code: Optional[Callable] = None

    def set_try(self, code: Callable):
        """设置尝试代码

        Args:
            code: 代码函数
        """
        self.try_code = code

    def add_except(self, exception_type: str, handler: Callable):
        """添加异常处理器

        Args:
            exception_type: 异常类型
            handler: 处理函数
        """
        self.except_handlers[exception_type] = handler

    def set_finally(self, code: Callable):
        """设置最终代码

        Args:
            code: 代码函数
        """
        self.finally_code = code

    def set_else(self, code: Callable):
        """设置否则代码（无异常时执行）

        Args:
            code: 代码函数
        """
        self.else_code = code

    def execute(self) -> Any:
        """执行尝试块

        Returns:
            执行结果
        """
    _ =   # 未使用变量
        exception_occurred = False

        try:
            # 执行尝试代码
            if self.try_code:
    _ =   # 未使用变量

        except XinyuException as e:
            exception_occurred = True
            # 查找匹配的异常处理器
            exception_type = e.exception_type.value

            if exception_type in self.except_handlers:
    _ = lers[exception_type](e)  # 未使用变量
            elif "所有" in self.except_handlers or "异常" in self.except_handlers:
                # 捕获所有异常
                handler = self.except_handlers.get("所有") or self.except_handlers.get("异常")
    _ =   # 未使用变量
            else:
                # 未捕获的异常，重新抛出
                raise

        except Exception as e:
            exception_occurred = True
            # 处理Python异常
            exception_type = type(e).__name__

            if exception_type in self.except_handlers:
    _ = lers[exception_type](e)  # 未使用变量
            elif "所有" in self.except_handlers or "异常" in self.except_handlers:
                handler = self.except_handlers.get("所有") or self.except_handlers.get("异常")
    _ =   # 未使用变量
            else:
                raise

        else:
            # 无异常，执行else代码
            if self.else_code:
    _ =   # 未使用变量

        finally:
            # 执行最终代码
            if self.finally_code:
                self.finally_code()

        return result


def xinyu_try(try_code: Callable) -> TryBlock:
    """创建尝试块

    Args:
        try_code: 尝试代码

    Returns:
        TryBlock实例
    """
    block = TryBlock()
    block.set_try(try_code)
    return block


def xinyu_except(block: TryBlock, exception_type: str) -> Callable:
    """异常处理器装饰器

    Args:
        block: TryBlock实例
        exception_type: 异常类型

    Returns:
        装饰器函数
    """

    def decorator(handler: Callable):
        block.add_except(exception_type, handler)
        return handler

    return decorator


def xinyu_throw(message: str, exception_type: XinyuExceptionType = XinyuExceptionType.自定义错误):
    """抛出异常

    Args:
        message: 错误消息
        exception_type: 异常类型
    """
    raise XinyuException(message, exception_type)


# 使用示例
if __name__ == "__main__":
    print("=== 异常处理示例 ===\n")

    # 示例1：基本异常处理
    def example1():
        block = TryBlock()

        def try_code():
            print("尝试执行代码")
            xinyu_throw("这是一个测试错误", XinyuExceptionType.值错误)

        def except_handler(e):
            print(f"捕获异常: {e}")
            return "已处理"

        block.set_try(try_code)
        block.add_except("ValueError", except_handler)

    _ = ecute()  # 未使用变量
        print(f"结果: {result}")

    example1()

    print("\n" + "=" * 50 + "\n")

    # 示例2：使用装饰器
    def example2():
        block = xinyu_try(lambda: 1 / 0)

        @xinyu_except(block, "ZeroDivisionError")
        def handle_zero_div(e):
            print(f"捕获除零错误: {e}")
            return "无穷大"

    _ = ecute()  # 未使用变量
        print(f"结果: {result}")

    example2()

    print("\n" + "=" * 50 + "\n")

    # 示例3：完整的try-except-else-finally
    def example3():
        block = TryBlock()

        def try_code():
            print("尝试代码")
            return "成功"

        def else_code():
            print("无异常，执行else")
            return "else结果"

        def finally_code():
            print("最终代码（总是执行）")

        block.set_try(try_code)
        block.set_else(else_code)
        block.set_finally(finally_code)

    _ = ecute()  # 未使用变量
        print(f"结果: {result}")

    example3()
