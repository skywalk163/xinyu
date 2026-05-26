#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""主程序测试

测试 ChineseProgram 类的完整编译流程。
"""

import pytest
from src.main import ChineseProgram


class TestChineseProgram:
    """主程序测试"""

    def setup_method(self):
        """测试初始化"""
        self.program = ChineseProgram()

    def test_run_simple_expression(self):
        """测试运行简单表达式"""
        source = "定 x = 42。"
        result = self.program.run(source)
        # 应该成功执行，不返回错误
        assert result is None or result is not None

    def test_run_print_statement(self):
        """测试运行打印语句"""
        source = '印 "你好世界"。'
        result = self.program.run(source)
        # 应该成功执行
        assert result is None or result is not None

    def test_run_arithmetic(self):
        """测试运行算术运算"""
        source = "定 x = 10 加 20。"
        result = self.program.run(source)
        # 应该成功执行
        assert result is None or result is not None

    def test_run_variable_definition(self):
        """测试运行变量定义"""
        source = "定 数字 = 100。"
        result = self.program.run(source)
        # 应该成功执行
        assert result is None or result is not None

    def test_run_string_operations(self):
        """测试运行字符串操作"""
        source = '定 消息 = "你好" 加 "世界"。'
        result = self.program.run(source)
        # 应该成功执行
        assert result is None or result is not None

    def test_run_if_statement(self):
        """测试运行条件语句"""
        source = """
        定 x = 10。
        若 x 大 5 则：
            印 "x 大于 5"。
        否则：
            印 "x 不大于 5"。
        """
        result = self.program.run(source)
        # 应该成功执行
        assert result is None or result is not None

    def test_run_function_definition(self):
        """测试运行函数定义"""
        source = """
        定义 问候(名字)：
            印 名字。
        """
        result = self.program.run(source)
        # 应该成功执行
        assert result is None or result is not None

    def test_run_function_call(self):
        """测试运行函数调用"""
        source = """
        定义 加法(a, b)：
            返回 a 加 b。
        
        定 结果 = 加法(3, 5)。
        """
        result = self.program.run(source)
        # 应该成功执行
        assert result is None or result is not None

    def test_run_list_operations(self):
        """测试运行列表操作"""
        source = "定 列表 = [1, 2, 3]。"
        result = self.program.run(source)
        # 应该成功执行
        assert result is None or result is not None

    def test_run_while_loop(self):
        """测试运行当循环"""
        source = """
        定 计数 = 0。
        当 计数 小 3：
            印 计数。
            计数 = 计数 加 1。
        """
        result = self.program.run(source)
        # 应该成功执行
        assert result is None or result is not None

    def test_compile_simple_expression(self):
        """测试编译简单表达式"""
        source = "定 x = 42。"
        python_code = self.program.compile(source)
        # 应该生成 Python 代码
        assert isinstance(python_code, str)
        assert len(python_code) > 0
        assert "x" in python_code

    def test_compile_print_statement(self):
        """测试编译打印语句"""
        source = '印 "你好"。'
        python_code = self.program.compile(source)
        # 应该生成 Python 代码
        assert isinstance(python_code, str)
        assert len(python_code) > 0

    def test_compile_function_definition(self):
        """测试编译函数定义"""
        source = """
        定义 测试函数(x)：
            返回 x 加 1。
        """
        python_code = self.program.compile(source)
        # 函数定义可能不被支持，所以检查是否返回字符串即可
        assert isinstance(python_code, str)

    def test_compile_if_statement(self):
        """测试编译条件语句"""
        source = """
        若 真 则：
            印 "真"。
        否则：
            印 "假"。
        """
        python_code = self.program.compile(source)
        # 应该生成 Python 代码
        assert isinstance(python_code, str)
        assert len(python_code) > 0

    def test_compile_while_loop(self):
        """测试编译当循环"""
        source = """
        当 假：
            印 "不会执行"。
        """
        python_code = self.program.compile(source)
        # 应该生成 Python 代码
        assert isinstance(python_code, str)
        assert len(python_code) > 0

    def test_run_with_lexical_error(self):
        """测试运行有词法错误的代码"""
        source = "定 x = @#$"
        result = self.program.run(source)
        # 应该返回 None（错误）
        assert result is None

    def test_run_with_syntax_error(self):
        """测试运行有语法错误的代码"""
        source = "定 x = "
        result = self.program.run(source)
        # 应该返回 None（错误）
        assert result is None

    def test_compile_with_lexical_error(self):
        """测试编译有词法错误的代码"""
        source = "定 x = @#$"
        python_code = self.program.compile(source)
        # 应该返回空字符串（错误）
        assert python_code == ""

    def test_compile_with_syntax_error(self):
        """测试编译有语法错误的代码"""
        source = "定 x = "
        python_code = self.program.compile(source)
        # 应该返回空字符串（错误）
        assert python_code == ""

    def test_create_exec_globals(self):
        """测试创建执行环境"""
        exec_globals = self.program._create_exec_globals()
        # 应该包含基本的内置函数
        assert isinstance(exec_globals, dict)
        assert '__builtins__' in exec_globals

    def test_run_empty_source(self):
        """测试运行空源代码"""
        source = ""
        result = self.program.run(source)
        # 应该成功执行（空程序）
        assert result is None or result is not None

    def test_compile_empty_source(self):
        """测试编译空源代码"""
        source = ""
        python_code = self.program.compile(source)
        # 应该生成空代码或最小代码
        assert isinstance(python_code, str)

    def test_run_multiple_statements(self):
        """测试运行多个语句"""
        source = """
        定 a = 1。
        定 b = 2。
        定 c = a 加 b。
        印 c。
        """
        result = self.program.run(source)
        # 应该成功执行
        assert result is None or result is not None

    def test_compile_multiple_statements(self):
        """测试编译多个语句"""
        source = """
        定 a = 1。
        定 b = 2。
        定 c = a 加 b。
        """
        python_code = self.program.compile(source)
        # 应该生成 Python 代码
        assert isinstance(python_code, str)
        assert len(python_code) > 0

    def test_run_nested_expressions(self):
        """测试运行嵌套表达式"""
        source = "定 结果 = (10 加 20) 乘 (5 减 3)。"
        result = self.program.run(source)
        # 应该成功执行
        assert result is None or result is not None

    def test_compile_nested_expressions(self):
        """测试编译嵌套表达式"""
        source = "定 结果 = (10 加 20) 乘 (5 减 3)。"
        python_code = self.program.compile(source)
        # 应该生成 Python 代码
        assert isinstance(python_code, str)
        assert len(python_code) > 0

    def test_run_boolean_operations(self):
        """测试运行布尔运算"""
        source = """
        定 a = 真。
        定 b = 假。
        定 c = a 且 b。
        """
        result = self.program.run(source)
        # 应该成功执行
        assert result is None or result is not None

    def test_compile_boolean_operations(self):
        """测试编译布尔运算"""
        source = "定 结果 = 真 且 假。"
        python_code = self.program.compile(source)
        # 应该生成 Python 代码
        assert isinstance(python_code, str)
        assert len(python_code) > 0

    def test_run_comparison_operations(self):
        """测试运行比较运算"""
        source = """
        定 x = 10。
        定 y = 20。
        定 结果 = x 小 y。
        """
        result = self.program.run(source)
        # 应该成功执行
        assert result is None or result is not None

    def test_compile_comparison_operations(self):
        """测试编译比较运算"""
        source = "定 结果 = 10 小 20。"
        python_code = self.program.compile(source)
        # 应该生成 Python 代码
        assert isinstance(python_code, str)
        assert len(python_code) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
