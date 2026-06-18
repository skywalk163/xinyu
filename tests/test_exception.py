# -*- coding: utf-8 -*-
"""异常处理测试

测试心语语言的异常处理功能。
"""
import io
import sys
from contextlib import redirect_stdout

import pytest


def test_main_module_exists():
    """测试主入口模块存在"""
    try:
        from src.main import ChineseProgram

        assert ChineseProgram is not None
    except ImportError:
        pytest.fail("主入口模块 src.main 不存在")


class TestTryExcept:
    """try-except语句测试"""

    def test_basic_try_except(self):
        """测试基本的try-except语句"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
尝试：
    定义 x = 1 相除 0。
捕获 那么：
    打印 "捕获到异常"。
。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "捕获到异常" in output

    def test_try_except_with_exception_type(self):
        """测试带异常类型的try-except语句"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
尝试：
    定义 x = 1 相除 0。
捕获 ZeroDivisionError 那么：
    打印 "除零错误"。
。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "除零错误" in output

    def test_try_except_finally(self):
        """测试try-except-finally语句"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 结果 = "未执行"。
尝试：
    定义 x = 1 相除 0。
捕获 那么：
    定义 结果 = "异常捕获"。
最终：
    打印 "最终执行"。
。
打印 结果。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "最终执行" in output
        assert "异常捕获" in output

    def test_multiple_except_clauses(self):
        """测试多个except子句"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
尝试：
    定义 x = 1 相除 0。
捕获 ValueError 那么：
    打印 "值错误"。
捕获 ZeroDivisionError 那么：
    打印 "除零错误"。
捕获 那么：
    打印 "其他错误"。
。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "除零错误" in output


class TestRaise:
    """raise语句测试"""

    def test_raise_exception(self):
        """测试抛出异常"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
尝试：
    抛出 ValueError "测试异常"。
捕获 ValueError 那么：
    打印 "捕获到ValueError"。
。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "捕获到ValueError" in output

    def test_raise_without_arguments(self):
        """测试无参数的raise语句"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
尝试：
    尝试：
        定义 x = 1 相除 0。
    捕获 那么：
        抛出。
    。
捕获 那么：
    打印 "重新抛出成功"。
。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "重新抛出成功" in output


class TestExceptionWithVariable:
    """带异常变量的测试"""

    def test_except_with_variable(self):
        """测试带异常变量的except子句"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
尝试：
    定义 x = 1 相除 0。
捕获 ZeroDivisionError 为 e 那么：
    打印 "捕获到异常"。
。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "捕获到异常" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
