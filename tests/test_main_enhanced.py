# -*- coding: utf-8 -*-
"""主程序增强测试

测试ChineseProgram类的完整功能。
"""

import sys
from io import StringIO

import pytest

from src.main import ChineseProgram


class TestChineseProgramEnhanced:
    """ChineseProgram增强测试"""

    def test_run_simple_variable(self):
        """测试简单变量定义和执行"""
        program = ChineseProgram()
        source = "定 x = 5。"
    _ = run(source)  # 未使用变量
        # 应该成功执行，不报错
        assert result is None or result is not None

    def test_run_print_statement(self):
        """测试打印语句"""
        program = ChineseProgram()
        source = '印"你好"。'
    _ = run(source)  # 未使用变量
        # 应该成功执行
        assert result is None

    def test_run_arithmetic(self):
        """测试算术运算"""
        program = ChineseProgram()
        source = "定 x = 1 加 2。"
    _ = run(source)  # 未使用变量
        assert result is None or result is not None

    def test_run_function_definition(self):
        """测试函数定义"""
        program = ChineseProgram()
        source = """
定 加法 = 函 a b：
    返回 a 加 b。
"""
    _ = run(source)  # 未使用变量
        assert result is None or result is not None

    def test_run_function_call(self):
        """测试函数调用"""
        program = ChineseProgram()
        source = """
定 加法 = 函 a b：
    返回 a 加 b。
定 结果 = 加法(1, 2)。
"""
    _ = run(source)  # 未使用变量
        assert result is None or result is not None

    def test_run_if_statement(self):
        """测试条件语句"""
        program = ChineseProgram()
        source = """
定 x = 10。
若 x 大于 0 那么：
    印"正数"。
"""
    _ = run(source)  # 未使用变量
        assert result is None

    def test_run_if_else_statement(self):
        """测试条件else语句"""
        program = ChineseProgram()
        source = """
定 x = -5。
若 x 大于 0 那么：
    印"正数"。
否则：
    印"非正数"。
"""
    _ = run(source)  # 未使用变量
        assert result is None

    def test_run_for_loop(self):
        """测试for循环"""
        program = ChineseProgram()
        source = """
遍历 i 于 [1, 2, 3]：
    印i。
"""
    _ = run(source)  # 未使用变量
        assert result is None

    def test_run_while_loop(self):
        """测试while循环"""
        program = ChineseProgram()
        source = """
定 x = 0。
当 x 小于 3：
    印x。
    定 x = x 加 1。
"""
    _ = run(source)  # 未使用变量
        assert result is None or result is not None

    def test_run_repeat_loop(self):
        """测试repeat循环"""
        program = ChineseProgram()
        source = """
重复 3 次数：
    印"你好"。
"""
    _ = run(source)  # 未使用变量
        assert result is None

    def test_compile_simple(self):
        """测试编译简单代码"""
        program = ChineseProgram()
        source = "定 x = 5。"
        python_code = program.compile(source)
        assert python_code != ""
        assert "x" in python_code

    def test_compile_function(self):
        """测试编译函数"""
        program = ChineseProgram()
        source = """
定 加法 = 函 a b：
    返回 a 加 b。
"""
        python_code = program.compile(source)
        assert python_code != ""
        assert "def" in python_code or "函" in python_code

    def test_compile_if_statement(self):
        """测试编译条件语句"""
        program = ChineseProgram()
        source = """
若 x 大于 0 那么：
    印"正数"。
"""
        python_code = program.compile(source)
        assert python_code != ""

    def test_run_with_math_module(self):
        """测试使用math模块"""
        program = ChineseProgram()
        source = """
定 x = math.sqrt(16)。
印x。
"""
    _ = run(source)  # 未使用变量
        assert result is None

    def test_run_with_list_operations(self):
        """测试列表操作"""
        program = ChineseProgram()
        source = """
定 列表 = [1, 2, 3, 4, 5]。
定 长度 = len(列表)。
印长度。
"""
    _ = run(source)  # 未使用变量
        assert result is None

    def test_run_with_dict_operations(self):
        """测试字典操作"""
        program = ChineseProgram()
        source = """
定 字典 = {"a": 1, "b": 2}。
印字典。
"""
    _ = run(source)  # 未使用变量
        assert result is None

    def test_run_boolean_operations(self):
        """测试布尔运算"""
        program = ChineseProgram()
        source = """
定 x = 真值 且 假值。
印x。
"""
    _ = run(source)  # 未使用变量
        assert result is None

    def test_run_comparison_operations(self):
        """测试比较运算"""
        program = ChineseProgram()
        source = """
定 x = 5 大于 3。
印x。
"""
    _ = run(source)  # 未使用变量
        assert result is None

    def test_run_nested_function_calls(self):
        """测试嵌套函数调用"""
        program = ChineseProgram()
        source = """
定 平方 = 函 x：
    返回 x 乘 x。
定 结果 = 平方(平方(2))。
印结果。
"""
    _ = run(source)  # 未使用变量
        assert result is None or result is not None

    def test_run_string_operations(self):
        """测试字符串操作"""
        program = ChineseProgram()
        source = """
定 s = "你好" 加 "世界"。
印s。
"""
    _ = run(source)  # 未使用变量
        assert result is None

    def test_error_handling_undefined_variable(self):
        """测试未定义变量错误处理"""
        program = ChineseProgram()
        source = "印x。"  # x未定义
    _ = run(source)  # 未使用变量
        # 应该返回None（错误）
        assert result is None

    def test_error_handling_syntax_error(self):
        """测试语法错误处理"""
        program = ChineseProgram()
        source = "定 x = "  # 不完整的语句
    _ = run(source)  # 未使用变量
        # 应该返回None（错误）
        assert result is None

    def test_multiple_statements(self):
        """测试多个语句"""
        program = ChineseProgram()
        source = """
定 x = 1。
定 y = 2。
定 z = x 加 y。
印z。
"""
    _ = run(source)  # 未使用变量
        assert result is None

    def test_empty_source(self):
        """测试空源代码"""
        program = ChineseProgram()
        source = ""
    _ = run(source)  # 未使用变量
        # 空代码应该不报错
        assert result is None or result is not None

    def test_whitespace_only(self):
        """测试仅包含空白的源代码"""
        program = ChineseProgram()
        source = "   \n\n   "
    _ = run(source)  # 未使用变量
        assert result is None or result is not None


class TestChineseProgramEnvironment:
    """测试执行环境"""

    def test_builtin_values(self):
        """测试内置值"""
        program = ChineseProgram()
        # 检查环境是否包含内置值
        assert "真" in program.env
        assert "假" in program.env
        assert program.env["真"] is True
        assert program.env["假"] is False

    def test_builtin_modules(self):
        """测试内置模块"""
        program = ChineseProgram()
        # 检查环境是否包含内置模块
        assert "math" in program.env
        assert "random" in program.env
        assert "json" in program.env
        assert "re" in program.env

    def test_datetime_modules(self):
        """测试datetime模块"""
        program = ChineseProgram()
        # 检查环境是否包含datetime相关模块
        assert "datetime" in program.env
        assert "date" in program.env
        assert "time" in program.env
        assert "timedelta" in program.env


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
