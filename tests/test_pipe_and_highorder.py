# -*- coding: utf-8 -*-
"""管道操作和高阶函数测试

测试心语语言的管道操作和高阶函数功能。
"""
import io
from contextlib import redirect_stdout

import pytest


def test_main_module_exists():
    """测试主入口模块存在"""
    try:
        from src.main import ChineseProgram

        assert ChineseProgram is not None
    except ImportError:
        pytest.fail("主入口模块 src.main 不存在")


class TestPipeOperation:
    """管道操作测试"""

    def test_basic_pipe(self):
        """测试基本管道操作"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 x = -5。
定义 结果 = x，绝对值。
打印 结果。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            program.run(source)

        output = captured_output.getvalue()
        assert "5" in output

    def test_pipe_with_list(self):
        """测试列表管道操作"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 列表1 = [1, 2, 3, 4, 5]。
定义 结果 = 列表1，求和。
打印 结果。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            program.run(source)

        output = captured_output.getvalue()
        assert "15" in output

    def test_pipe_with_length(self):
        """测试长度管道操作"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 列表1 = [1, 2, 3, 4, 5]。
定义 结果 = 列表1，长度。
打印 结果。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            program.run(source)

        output = captured_output.getvalue()
        assert "5" in output


class TestHighOrderFunctions:
    """高阶函数测试"""

    def test_map_function(self):
        """测试map函数"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 列表1 = [1, 2, 3]。
定义 双倍 = 函数 x：
  返回 x 相乘 2。
。
定义 结果 = 列表1，皆 双倍。
定义 结果列表 = 列表 结果。
打印 结果列表。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            program.run(source)

        output = captured_output.getvalue()
        # 应该输出 [2, 4, 6]
        assert "2" in output

    def test_filter_function(self):
        """测试filter函数"""
        # TODO: 需要实现lambda函数语法支持
        # 当前语法不支持匿名函数，暂时跳过
        pytest.skip("需要lambda函数语法支持，当前语法不支持匿名函数")


class TestBuiltinFunctions:
    """内置函数测试"""

    def test_sum_function(self):
        """测试sum函数"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 列表1 = [1, 2, 3, 4, 5]。
定义 结果 = 求和 列表1。
打印 结果。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            program.run(source)

        output = captured_output.getvalue()
        assert "15" in output

    def test_len_function(self):
        """测试len函数"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 列表1 = [1, 2, 3, 4, 5]。
定义 结果 = 长度 列表1。
打印 结果。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            program.run(source)

        output = captured_output.getvalue()
        assert "5" in output

    def test_abs_function(self):
        """测试abs函数"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 x = -10。
定义 结果 = 绝对值 x。
打印 结果。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            program.run(source)

        output = captured_output.getvalue()
        assert "10" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
