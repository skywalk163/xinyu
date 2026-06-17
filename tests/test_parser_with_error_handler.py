"""解析器错误处理测试

测试src/parser/parser_with_error_handler.py模块的功能。
"""

import pytest

from src.error_handling import ErrorHandler, ErrorType
from src.lexer.lexer import Lexer
from src.lexer.tokens import TokenType
from src.parser.ast_nodes import (
    AssignNode,
    BinaryOpNode,
    ForNode,
    FunctionCallNode,
    IdentifierNode,
    IfNode,
    ListNode,
    NumberNode,
    ProgramNode,
    RepeatNode,
    ReturnNode,
    StringNode,
    UnaryOpNode,
    VarDefNode,
    WhileNode,
)
from src.parser.parser_with_error_handler import ParserWithErrorHandler


class TestParserWithErrorHandler:
    """测试ParserWithErrorHandler类"""

    def test_parser_initialization(self):
        """测试解析器初始化"""
        # 创建词法分析器和错误处理器
        lexer = Lexer("定 x = 42")
        tokens = lexer.tokenize()
        error_handler = ErrorHandler()

        # 创建解析器
        parser = ParserWithErrorHandler(tokens, error_handler)

        assert parser.tokens == tokens
        assert parser.pos == 0
        assert parser.error_handler == error_handler
        assert not error_handler.has_errors()

    def test_parse_simple_expression(self):
        """测试解析简单表达式"""
        lexer = Lexer("1 相加 2")
        tokens = lexer.tokenize()
        error_handler = ErrorHandler()
        parser = ParserWithErrorHandler(tokens, error_handler)

        ast = parser.parse()

        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        assert not error_handler.has_errors()

        # 检查表达式结构
        expr = ast.statements[0]
        assert isinstance(expr, BinaryOpNode)
        assert expr.operator == "+"

        left = expr.left
        right = expr.right
        assert isinstance(left, NumberNode)
        assert left.value == 1
        assert isinstance(right, NumberNode)
        assert right.value == 2

    def test_parse_variable_definition(self):
        """测试解析变量定义"""
        lexer = Lexer("定 x = 42")
        tokens = lexer.tokenize()
        error_handler = ErrorHandler()
        parser = ParserWithErrorHandler(tokens, error_handler)

        ast = parser.parse()

        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        assert not error_handler.has_errors()

        # 检查变量定义
        var_def = ast.statements[0]
        assert isinstance(var_def, VarDefNode)
        assert var_def.name == "x"
        assert isinstance(var_def.value, NumberNode)
        assert var_def.value.value == 42

    def test_parse_assignment(self):
        """测试解析赋值语句"""
        lexer = Lexer("x = 42")
        tokens = lexer.tokenize()
        error_handler = ErrorHandler()
        parser = ParserWithErrorHandler(tokens, error_handler)

        ast = parser.parse()

        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        assert not error_handler.has_errors()

        # 检查赋值
        assign = ast.statements[0]
        assert isinstance(assign, AssignNode)
        assert isinstance(assign.target, IdentifierNode)
        assert assign.target.name == "x"
        assert isinstance(assign.value, NumberNode)
        assert assign.value.value == 42

    def test_parse_if_statement(self):
        """测试解析条件语句"""
        lexer = Lexer('若 真 那么 打印("hello")')
        tokens = lexer.tokenize()
        error_handler = ErrorHandler()
        parser = ParserWithErrorHandler(tokens, error_handler)

        ast = parser.parse()

        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        assert not error_handler.has_errors()

        # 检查if语句
        if_node = ast.statements[0]
        assert isinstance(if_node, IfNode)
        assert isinstance(if_node.condition, IdentifierNode)
        assert if_node.condition.name == "真"
        assert len(if_node.then_branch) == 1
        assert isinstance(if_node.then_branch[0], FunctionCallNode)
        assert if_node.then_branch[0].name == "打印"
        assert if_node.else_branch is None

    def test_parse_for_loop(self):
        """测试解析for循环"""
        lexer = Lexer("遍历 i 于 范围(10)：打印(i)")
        tokens = lexer.tokenize()
        error_handler = ErrorHandler()
        parser = ParserWithErrorHandler(tokens, error_handler)

        ast = parser.parse()

        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        assert not error_handler.has_errors()

        # 检查for循环
        for_node = ast.statements[0]
        assert isinstance(for_node, ForNode)
        assert for_node.var == "i"
        assert isinstance(for_node.iterable, FunctionCallNode)
        assert for_node.iterable.name == "范围"
        assert len(for_node.body) == 1
        assert isinstance(for_node.body[0], FunctionCallNode)
        assert for_node.body[0].name == "打印"

    def test_parse_while_loop(self):
        """测试解析while循环"""
        lexer = Lexer('当 真：打印("hello")')
        tokens = lexer.tokenize()
        error_handler = ErrorHandler()
        parser = ParserWithErrorHandler(tokens, error_handler)

        ast = parser.parse()

        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        assert not error_handler.has_errors()

        # 检查while循环
        while_node = ast.statements[0]
        assert isinstance(while_node, WhileNode)
        assert isinstance(while_node.condition, IdentifierNode)
        assert while_node.condition.name == "真"
        assert len(while_node.body) == 1
        assert isinstance(while_node.body[0], FunctionCallNode)
        assert while_node.body[0].name == "打印"

    def test_parse_return_statement(self):
        """测试解析返回语句"""
        lexer = Lexer("返回 42")
        tokens = lexer.tokenize()
        error_handler = ErrorHandler()
        parser = ParserWithErrorHandler(tokens, error_handler)

        ast = parser.parse()

        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        assert not error_handler.has_errors()

        # 检查返回语句
        return_node = ast.statements[0]
        assert isinstance(return_node, ReturnNode)
        assert isinstance(return_node.value, NumberNode)
        assert return_node.value.value == 42

    def test_error_handling_missing_equals(self):
        """测试错误处理：变量定义缺少等号"""
        lexer = Lexer("定 x 42")
        tokens = lexer.tokenize()
        error_handler = ErrorHandler()
        parser = ParserWithErrorHandler(tokens, error_handler)

        ast = parser.parse()

        # 应该报告错误
        assert error_handler.has_errors()
        errors = error_handler.get_errors()
        assert len(errors) > 0

        # 检查错误类型
        error = errors[0]
        assert error.error_type == ErrorType.PARSER_ERROR
        assert "Expected '=' after variable name" in error.message or "期望" in error.message

    def test_error_handling_missing_identifier(self):
        """测试错误处理：变量定义缺少标识符"""
        lexer = Lexer("定 = 42")
        tokens = lexer.tokenize()
        error_handler = ErrorHandler()
        parser = ParserWithErrorHandler(tokens, error_handler)

        ast = parser.parse()

        # 应该报告错误
        assert error_handler.has_errors()
        errors = error_handler.get_errors()
        assert len(errors) > 0

        # 检查错误类型
        error = errors[0]
        assert error.error_type == ErrorType.PARSER_ERROR
        assert "期望变量名" in error.message or "Expected variable name" in error.message

    def test_error_handling_unexpected_token(self):
        """测试错误处理：意外的token"""
        lexer = Lexer("+ 42")
        tokens = lexer.tokenize()
        error_handler = ErrorHandler()
        parser = ParserWithErrorHandler(tokens, error_handler)

        ast = parser.parse()

        # 应该报告错误
        assert error_handler.has_errors()
        errors = error_handler.get_errors()
        assert len(errors) > 0

        # 检查错误类型
        error = errors[0]
        assert error.error_type == ErrorType.PARSER_ERROR
        assert "意外的token" in error.message or "Unexpected token" in error.message

    def test_error_recovery(self):
        """测试错误恢复：多个语句中的错误"""
        lexer = Lexer("定 x = 42\n定 y 100\n定 z = 200")
        tokens = lexer.tokenize()
        error_handler = ErrorHandler()
        parser = ParserWithErrorHandler(tokens, error_handler)

        ast = parser.parse()

        # 应该报告错误
        assert error_handler.has_errors()

        # 应该成功解析第一个和第三个语句
        assert len(ast.statements) >= 2

        # 检查第一个语句
        var_def1 = ast.statements[0]
        assert isinstance(var_def1, VarDefNode)
        assert var_def1.name == "x"

        # 检查第三个语句
        var_def2 = ast.statements[1]
        assert isinstance(var_def2, VarDefNode)
        assert var_def2.name == "z"

    def test_parse_multiple_statements(self):
        """测试解析多个语句"""
        source = """
定 x = 10
定 y = 20
打印 x 相加 y
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        error_handler = ErrorHandler()
        parser = ParserWithErrorHandler(tokens, error_handler)

        ast = parser.parse()

        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 3
        assert not error_handler.has_errors()

        # 检查语句
        assert isinstance(ast.statements[0], VarDefNode)
        assert ast.statements[0].name == "x"

        assert isinstance(ast.statements[1], VarDefNode)
        assert ast.statements[1].name == "y"

        assert isinstance(ast.statements[2], FunctionCallNode)
        assert ast.statements[2].name == "打印"

    def test_parse_complex_expression(self):
        """测试解析复杂表达式"""
        lexer = Lexer("(1 相加 2) 相乘 3")
        tokens = lexer.tokenize()
        error_handler = ErrorHandler()
        parser = ParserWithErrorHandler(tokens, error_handler)

        ast = parser.parse()

        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        assert not error_handler.has_errors()

        # 检查表达式结构
        expr = ast.statements[0]
        assert isinstance(expr, BinaryOpNode)
        assert expr.operator == "*"

        left = expr.left
        right = expr.right
        assert isinstance(left, BinaryOpNode)
        assert left.operator == "+"
        assert isinstance(right, NumberNode)
        assert right.value == 3

    def test_parse_list_literal(self):
        """测试解析列表字面量"""
        lexer = Lexer("[1, 2, 3]")
        tokens = lexer.tokenize()
        error_handler = ErrorHandler()
        parser = ParserWithErrorHandler(tokens, error_handler)

        ast = parser.parse()

        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        assert not error_handler.has_errors()

        # 检查列表
        list_node = ast.statements[0]
        assert isinstance(list_node, ListNode)
        assert len(list_node.elements) == 3

        for i, elem in enumerate(list_node.elements, 1):
            assert isinstance(elem, NumberNode)
            assert elem.value == i


if __name__ == "__main__":
    # 运行测试
    import sys

    sys.exit(pytest.main([__file__, "-v"]))
