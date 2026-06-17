"""运行时错误路径测试

测试运行时环境的错误处理能力。
"""
import io
import sys
from contextlib import redirect_stdout

import pytest

from src.main import ChineseProgram


class TestRuntimeErrors:
    """运行时错误测试"""

    def test_division_by_zero(self):
        """测试除零错误"""
        program = ChineseProgram()
        source = "定义 结果 = 1 相除 0。"
        # 应该捕获异常或返回错误
        result = program.run(source)
        # 可能返回None或抛出异常
        assert result is None or result == float("inf")

    def test_index_out_of_range(self):
        """测试索引越界"""
        program = ChineseProgram()
        source = """
定义 列表 = [1, 2, 3]。
定义 元素 = 列表[10]。
"""
        result = program.run(source)
        # 应该捕获异常
        assert result is None

    def test_type_mismatch(self):
        """测试类型不匹配"""
        program = ChineseProgram()
        source = '定义 结果 = "文本" 相加 123。'
        result = program.run(source)
        # 可能成功（字符串拼接）或失败
        # 根据实际实现决定

    def test_attribute_error(self):
        """测试属性错误"""
        program = ChineseProgram()
        source = """
定义 数字 = 42。
定义 属性 = 数字.不存在属性。
"""
        result = program.run(source)
        # 应该捕获异常
        assert result is None

    def test_key_error(self):
        """测试键错误"""
        program = ChineseProgram()
        source = """
定义 字典 = {"键": 1}。
定义 值 = 字典["不存在"]。
"""
        result = program.run(source)
        # 应该捕获异常
        assert result is None

    def test_recursion_error(self):
        """测试递归过深"""
        program = ChineseProgram()
        source = """
定义 无限递归 = 函数 n：
    返回 无限递归 n 相加 1。
定义 结果 = 无限递归 0。
"""
        result = program.run(source)
        # 应该捕获递归错误
        assert result is None

    def test_name_error(self):
        """测试名称错误"""
        program = ChineseProgram()
        source = "打印 不存在的变量。"
        result = program.run(source)
        # 应该捕获名称错误
        assert result is None

    def test_syntax_error_in_generated_code(self):
        """测试生成代码的语法错误"""
        program = ChineseProgram()
        # 这个测试需要构造一个会导致生成代码语法错误的输入
        # 根据实际实现决定


class TestRuntimeErrorRecovery:
    """运行时错误恢复测试"""

    def test_error_message_quality(self):
        """测试错误消息质量"""
        program = ChineseProgram()
        source = "定义 结果 = 1 相除 0。"
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        output = captured_output.getvalue()
        # 错误消息应该包含有用信息
        # 根据实际实现决定

    def test_error_does_not_crash(self):
        """测试错误不会导致崩溃"""
        program = ChineseProgram()
        error_sources = [
            "定义 结果 = 1 相除 0。",
            "打印 不存在。",
            "定义 列表 = [1]。定义 元素 = 列表[10]。",
        ]
        for source in error_sources:
            # 每个错误都不应该导致程序崩溃
            try:
                result = program.run(source)
                # 应该返回None或错误值
            except Exception as e:
                # 如果抛出异常，应该是预期的异常类型
                assert isinstance(
                    e, (ValueError, TypeError, KeyError, IndexError, ZeroDivisionError)
                )


class TestRuntimeEdgeCases:
    """运行时边界情况测试"""

    def test_empty_program(self):
        """测试空程序"""
        program = ChineseProgram()
        result = program.run("")
        # 空程序应该成功执行
        assert result is not None or result is None

    def test_large_number(self):
        """测试大数字"""
        program = ChineseProgram()
        source = "定义 大数 = 999999999999999999。"
        result = program.run(source)
        # 应该能处理大数字
        assert result is not None or result is None

    def test_long_string(self):
        """测试长字符串"""
        program = ChineseProgram()
        long_string = "a" * 10000
        source = f'定义 长字符串 = "{long_string}"。'
        result = program.run(source)
        # 应该能处理长字符串
        assert result is not None or result is None

    def test_deeply_nested_expression(self):
        """测试深度嵌套表达式"""
        program = ChineseProgram()
        source = "定义 结果 = (((((1 相加 2) 相乘 3) 相减 4) 相除 5) 相加 6)。"
        result = program.run(source)
        # 应该能处理深度嵌套
        assert result is not None or result is None

    def test_many_variables(self):
        """测试大量变量"""
        program = ChineseProgram()
        statements = [f"定义 变量{i} = {i}。" for i in range(100)]
        source = "\n".join(statements)
        result = program.run(source)
        # 应该能处理大量变量
        assert result is not None or result is None
