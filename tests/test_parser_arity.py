"""元数驱动解析器测试

测试元数驱动参数收集功能。
"""

import pytest

from src.lexer.lexer import Lexer
from src.parser.ast_nodes import (
    BinaryOpNode,
    FunctionCallNode,
    IdentifierNode,
    NumberNode,
    StringNode,
)
from src.parser.parser import Parser


class TestArityDrivenParsing:
    """元数驱动解析测试"""

    def test_fixed_arity_function_call(self):
        """测试固定元数函数调用"""
        source = "平方根 16。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, FunctionCallNode)
        assert stmt.name == "平方根"
        assert len(stmt.args) == 1
        assert isinstance(stmt.args[0], NumberNode)
        assert stmt.args[0].value == 16

    def test_variable_arity_function_call(self):
        """测试可变元数函数调用"""
        source = '打印 "你好" "世界" "！"。'
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, FunctionCallNode)
        assert stmt.name == "打印"
        assert len(stmt.args) == 3

    def test_operator_verb_in_expression(self):
        """测试操作符动词在表达式中"""
        source = "a 相加 b。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, BinaryOpNode)
        assert stmt.operator == "+"

    def test_operator_verb_multiplication(self):
        """测试操作符动词乘法"""
        source = "a 相乘 b。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, BinaryOpNode)
        assert stmt.operator == "*"

    def test_operator_verb_division(self):
        """测试操作符动词除法"""
        source = "a 相除 b。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, BinaryOpNode)
        assert stmt.operator == "/"

    def test_operator_verb_subtraction(self):
        """测试操作符动词减法"""
        source = "a 相减 b。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, BinaryOpNode)
        assert stmt.operator == "-"

    def test_function_call_with_operator_args(self):
        """测试函数调用参数包含操作符"""
        source = "平方根 n 相减 1。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # 实际解析为：平方根(n - 1)，即函数调用，参数是二元操作
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, FunctionCallNode)
        assert stmt.name == "平方根"
        assert len(stmt.args) == 1
        # 参数是二元操作
        assert isinstance(stmt.args[0], BinaryOpNode)
        assert stmt.args[0].operator == "-"

    def test_multiple_function_calls(self):
        """测试多个函数调用"""
        source = "平方根 16。平方根 25。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert len(ast.statements) == 2
        assert isinstance(ast.statements[0], FunctionCallNode)
        assert isinstance(ast.statements[1], FunctionCallNode)

    def test_nested_function_calls(self):
        """测试嵌套函数调用"""
        source = "平方根 平方根 16。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, FunctionCallNode)
        assert stmt.name == "平方根"
        assert len(stmt.args) == 1
        # 参数应该是另一个函数调用
        assert isinstance(stmt.args[0], FunctionCallNode)

    def test_operator_verb_with_numbers(self):
        """测试操作符动词与数字"""
        source = "5 相加 3。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, BinaryOpNode)
        assert stmt.operator == "+"
        assert isinstance(stmt.left, NumberNode)
        assert stmt.left.value == 5
        assert isinstance(stmt.right, NumberNode)
        assert stmt.right.value == 3

    def test_chained_operator_verbs(self):
        """测试链式操作符动词"""
        source = "a 相加 b 相乘 c。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, BinaryOpNode)
        assert stmt.operator == "+"
        # 右侧应该是乘法
        assert isinstance(stmt.right, BinaryOpNode)
        assert stmt.right.operator == "*"

    def test_builtin_function_arity(self):
        """测试内置函数元数"""
        # 绝对值：固定1个参数（使用括号避免歧义）
        source = "绝对值（-5）。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, FunctionCallNode)
        assert stmt.name == "绝对值"
        assert len(stmt.args) == 1

    def test_variable_arity_with_multiple_args(self):
        """测试可变元数多参数"""
        source = "求和 1 2 3 4 5。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, FunctionCallNode)
        assert stmt.name == "求和"
        assert len(stmt.args) == 5

    def test_range_arity_function(self):
        """测试范围元数函数"""
        # 范围：1-3个参数
        source = "范围 10。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, FunctionCallNode)
        assert stmt.name == "范围"
        assert len(stmt.args) == 1

    def test_range_arity_with_two_args(self):
        """测试范围元数函数（2个参数）"""
        source = "范围 1 10。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, FunctionCallNode)
        assert stmt.name == "范围"
        assert len(stmt.args) == 2

    def test_unregistered_function(self):
        """测试未注册函数（默认可变元数）"""
        source = "自定义函数 1 2 3。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, FunctionCallNode)
        assert stmt.name == "自定义函数"
        assert len(stmt.args) == 3

    def test_operator_verb_stops_argument_collection(self):
        """测试操作符动词在参数中的处理"""
        source = "平方根 16 相加 平方根 25。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # 实际解析为：平方根(16 + 平方根(25))，即函数调用，参数是二元操作
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, FunctionCallNode)
        assert stmt.name == "平方根"
        assert len(stmt.args) == 1
        # 参数是二元操作
        assert isinstance(stmt.args[0], BinaryOpNode)
        assert stmt.args[0].operator == "+"
