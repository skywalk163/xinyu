"""语法分析器边界测试

测试语法分析器的边界情况处理能力。
"""
import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser, ParseError
from src.parser.ast_nodes import ProgramNode, FunctionDefNode, IfNode, VarDefNode


class TestParserBoundary:
    """语法分析器边界测试"""

    def test_empty_program(self):
        """测试空程序解析"""
        lexer = Lexer("")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        assert isinstance(ast, ProgramNode)
        assert ast.statements == []

    def test_whitespace_only_program(self):
        """测试仅空白字符的程序"""
        lexer = Lexer("   \n\t  ")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        assert isinstance(ast, ProgramNode)
        assert ast.statements == []

    def test_single_statement(self):
        """测试单语句程序"""
        lexer = Lexer('打印"你好"。')
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1

    def test_multiple_statements(self):
        """测试多语句程序"""
        source = """
定义 变量1 = 1。
定义 变量2 = 2。
打印 变量1。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 3

    def test_empty_function_body(self):
        """测试空函数体"""
        source = "定义 空函数 = 函数：返回 空。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1

    def test_nested_if_statements(self):
        """测试嵌套if语句"""
        source = """
如果 真 那么：
    如果 假 那么：
        打印"内层"。
    否则：
        打印"外层"。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], IfNode)

    def test_function_with_parameters(self):
        """测试带参数的函数"""
        source = "定义 加法 = 函数 a, b：返回 a 相加 b。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        # 函数定义被包装在VarDefNode中
        assert isinstance(ast.statements[0], VarDefNode)
        assert isinstance(ast.statements[0].value, FunctionDefNode)

    def test_function_call(self):
        """测试函数调用"""
        source = """
定义 函数名 = 函数 x：返回 x 相乘 2。
定义 结果 = 函数名 5。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 2

    def test_complex_expression(self):
        """测试复杂表达式"""
        source = "定义 结果 = (1 相加 2) 相乘 (3 相减 4)。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1

    def test_list_literal(self):
        """测试列表字面量"""
        source = "定义 列表 = [1, 2, 3, 4, 5]。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1

    def test_dict_literal(self):
        """测试字典字面量"""
        source = '定义 字典 = {"键1": 1, "键2": 2}。'
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1

    def test_while_loop(self):
        """测试while循环"""
        source = """
定义 计数 = 0。
当 计数 小于 10 时：
    定义 计数 = 计数 相加 1。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        assert isinstance(ast, ProgramNode)

    def test_for_loop(self):
        """测试for循环"""
        source = """
定义 列表 = [1, 2, 3]。
遍历 元素 于 列表：
    打印 元素。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        assert isinstance(ast, ProgramNode)

    def test_return_statement(self):
        """测试return语句"""
        source = "定义 函数名 = 函数：返回 42。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1

    def test_assignment(self):
        """测试赋值语句"""
        source = """
定义 变量 = 1。
定义 变量 = 变量 相加 1。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 2
