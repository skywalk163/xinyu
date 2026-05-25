"""
意合式调用测试

测试意合式函数调用语法：参数1、参数2，函数名。
"""

import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.parser.ast_nodes import FunctionCallNode, IdentifierNode, NumberNode, StringNode
from src.codegen.python_codegen import PythonCodegen


class TestIntentionalCall:
    """测试意合式调用"""

    def test_simple_intentional_call(self):
        """测试简单的意合式调用"""
        source = "北京、上海，计算距离。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # 应该解析为函数调用
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], FunctionCallNode)
        assert ast.statements[0].name == "计算距离"
        assert len(ast.statements[0].args) == 2

    def test_intentional_call_with_numbers(self):
        """测试数字参数的意合式调用"""
        source = "10、20，求和。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], FunctionCallNode)
        assert ast.statements[0].name == "求和"
        assert len(ast.statements[0].args) == 2
        assert isinstance(ast.statements[0].args[0], NumberNode)
        assert isinstance(ast.statements[0].args[1], NumberNode)

    def test_intentional_call_with_strings(self):
        """测试字符串参数的意合式调用"""
        source = "\"张三\"、\"李四\"，发送消息。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], FunctionCallNode)
        assert ast.statements[0].name == "发送消息"
        assert len(ast.statements[0].args) == 2
        assert isinstance(ast.statements[0].args[0], StringNode)
        assert isinstance(ast.statements[0].args[1], StringNode)

    def test_intentional_call_with_three_args(self):
        """测试三个参数的意合式调用"""
        source = "1、2、3，计算平均值。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], FunctionCallNode)
        assert ast.statements[0].name == "计算平均值"
        assert len(ast.statements[0].args) == 3

    def test_multiple_intentional_calls(self):
        """测试多个意合式调用"""
        source = """
北京、上海，计算距离。
广州、深圳，计算距离。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert len(ast.statements) == 2
        assert all(isinstance(stmt, FunctionCallNode) for stmt in ast.statements)
        assert all(stmt.name == "计算距离" for stmt in ast.statements)

    def test_intentional_call_mixed_with_normal_call(self):
        """测试意合式调用与普通调用混合"""
        source = """
北京、上海，计算距离。
计算距离(北京, 上海)。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert len(ast.statements) == 2
        assert all(isinstance(stmt, FunctionCallNode) for stmt in ast.statements)
        assert all(stmt.name == "计算距离" for stmt in ast.statements)
