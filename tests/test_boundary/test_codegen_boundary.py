"""代码生成器边界测试

测试代码生成器的边界情况处理能力。
"""
import pytest

from src.codegen.python_codegen import PythonCodegen
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer


class TestCodegenBoundary:
    """代码生成器边界测试"""

    def test_empty_program(self):
        """测试空程序代码生成"""
        lexer = Lexer("")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        codegen = PythonCodegen()
        code = codegen.generate(ast)
        # 空程序应该生成空代码或最小代码
        assert code is not None

    def test_simple_print(self):
        """测试简单打印语句"""
        source = '打印"你好"。'
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        codegen = PythonCodegen()
        code = codegen.generate(ast)
        assert "print" in code
        assert "你好" in code

    def test_variable_definition(self):
        """测试变量定义"""
        source = "定义 变量 = 42。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        codegen = PythonCodegen()
        code = codegen.generate(ast)
        assert "变量" in code
        assert "42" in code

    def test_function_definition(self):
        """测试函数定义"""
        source = "定义 函数名 = 函数 x：返回 x 相乘 2。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        codegen = PythonCodegen()
        code = codegen.generate(ast)
        assert "def" in code
        assert "函数名" in code
        assert "return" in code

    def test_function_call(self):
        """测试函数调用"""
        source = """
定义 函数名 = 函数 x：返回 x 相加 1。
定义 结果 = 函数名 5。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        codegen = PythonCodegen()
        code = codegen.generate(ast)
        assert "函数名" in code
        assert "5" in code

    def test_if_statement(self):
        """测试if语句"""
        source = """
如果 真 那么：
    打印"真"。
否则：
    打印"假"。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        codegen = PythonCodegen()
        code = codegen.generate(ast)
        assert "if" in code
        assert "else" in code

    def test_while_loop(self):
        """测试while循环"""
        source = """
定义 计数 = 0。
当 计数 小于 5 时：
    定义 计数 = 计数 相加 1。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        codegen = PythonCodegen()
        code = codegen.generate(ast)
        assert "while" in code

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
        codegen = PythonCodegen()
        code = codegen.generate(ast)
        assert "for" in code

    def test_arithmetic_operations(self):
        """测试算术运算"""
        source = """
定义 a = 1 相加 2。
定义 b = 3 相减 1。
定义 c = 2 相乘 3。
定义 d = 6 相除 2。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        codegen = PythonCodegen()
        code = codegen.generate(ast)
        assert "+" in code or "相加" in code
        assert "-" in code or "相减" in code
        assert "*" in code or "相乘" in code
        assert "/" in code or "相除" in code

    def test_comparison_operations(self):
        """测试比较运算"""
        source = """
定义 结果1 = 1 小于 2。
定义 结果2 = 2 大于 1。
定义 结果3 = 1 等于 1。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        codegen = PythonCodegen()
        code = codegen.generate(ast)
        assert "<" in code or "小于" in code
        assert ">" in code or "大于" in code
        assert "==" in code or "等于" in code

    def test_list_literal(self):
        """测试列表字面量"""
        source = "定义 列表 = [1, 2, 3]。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        codegen = PythonCodegen()
        code = codegen.generate(ast)
        assert "[" in code
        assert "]" in code

    def test_dict_literal(self):
        """测试字典字面量"""
        source = '定义 字典 = {"键": 1}。'
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        codegen = PythonCodegen()
        code = codegen.generate(ast)
        assert "{" in code
        assert "}" in code

    def test_nested_functions(self):
        """测试嵌套函数"""
        source = """
定义 外层函数 = 函数 x：
    定义 内层函数 = 函数 y：
        返回 y 相乘 2。
    返回 内层函数 x。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        codegen = PythonCodegen()
        code = codegen.generate(ast)
        assert "def" in code
        assert "外层函数" in code
        assert "内层函数" in code

    def test_multiple_statements(self):
        """测试多语句程序"""
        source = """
定义 变量1 = 1。
定义 变量2 = 2。
定义 变量3 = 变量1 相加 变量2。
打印 变量3。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        codegen = PythonCodegen()
        code = codegen.generate(ast)
        assert "变量1" in code
        assert "变量2" in code
        assert "变量3" in code
        assert "print" in code
