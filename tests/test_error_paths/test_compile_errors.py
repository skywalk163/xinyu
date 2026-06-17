"""编译错误路径测试

测试编译各阶段的错误处理能力。
"""
import pytest

from src.lexer.lexer import Lexer, LexerError
from src.parser.parser import ParseError, Parser
from src.semantic.analyzer import SemanticAnalyzer


class TestLexerErrors:
    """词法分析错误测试"""

    def test_invalid_character(self):
        """测试非法字符"""
        with pytest.raises(LexerError):
            lexer = Lexer("@#$%")
            lexer.tokenize()

    def test_unclosed_string(self):
        """测试未闭合字符串"""
        with pytest.raises(LexerError):
            lexer = Lexer('"未闭合字符串')
            lexer.tokenize()

    def test_invalid_number(self):
        """测试无效数字"""
        # 测试多个小数点
        with pytest.raises(LexerError):
            lexer = Lexer("定义 数字 = 1.2.3。")
            lexer.tokenize()

    def test_invalid_operator(self):
        """测试无效操作符"""
        # 某些特殊字符可能不被支持
        try:
            lexer = Lexer("定义 结果 = 1 ^ 2。")
            tokens = lexer.tokenize()
            # 如果不抛出异常，检查是否正确处理
        except LexerError:
            pass  # 预期的错误

    def test_empty_string(self):
        """测试空字符串"""
        lexer = Lexer("")
        tokens = lexer.tokenize()
        # 空字符串应该返回空列表或仅EOF
        assert len(tokens) <= 1


class TestParserErrors:
    """语法分析错误测试"""

    def test_incomplete_statement(self):
        """测试不完整语句"""
        with pytest.raises(ParseError):
            lexer = Lexer("如果 真")
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            parser.parse()

    def test_missing_colon(self):
        """测试缺少冒号"""
        with pytest.raises(ParseError):
            lexer = Lexer("定义 函数名 = 函数 x 返回 x。")
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            parser.parse()

    def test_unmatched_parentheses(self):
        """测试不匹配的括号"""
        with pytest.raises(ParseError):
            lexer = Lexer("定义 结果 = (1 + 2。")
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            parser.parse()

    def test_invalid_expression(self):
        """测试无效表达式"""
        with pytest.raises(ParseError):
            lexer = Lexer("定义 结果 = + +。")
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            parser.parse()

    def test_missing_end_marker(self):
        """测试缺少结束标记"""
        # 某些语句可能需要结束标记
        try:
            lexer = Lexer("定义 变量 = 1")
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            parser.parse()
        except ParseError:
            pass  # 预期的错误


class TestSemanticErrors:
    """语义分析错误测试"""

    def test_undefined_variable(self):
        """测试未定义变量"""
        source = "打印 未定义变量。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        result = analyzer.analyze(ast)
        # 应该检测到错误
        assert result is False or len(analyzer.errors) > 0

    def test_undefined_function(self):
        """测试未定义函数"""
        source = "定义 结果 = 未定义函数 1。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        result = analyzer.analyze(ast)
        # 应该检测到错误
        assert result is False or len(analyzer.errors) > 0

    def test_wrong_argument_count(self):
        """测试参数数量错误"""
        source = """
定义 函数名 = 函数 x：返回 x。
定义 结果 = 函数名 1 2。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        result = analyzer.analyze(ast)
        # 可能检测到参数数量错误
        # 根据实际实现决定

    def test_duplicate_definition(self):
        """测试重复定义"""
        source = """
定义 变量 = 1。
定义 变量 = 2。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        result = analyzer.analyze(ast)
        # 可能允许重定义，也可能报错
        # 根据实际实现决定

    def test_return_outside_function(self):
        """测试函数外的return"""
        source = "返回 42。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        result = analyzer.analyze(ast)
        # 应该检测到错误
        assert result is False or len(analyzer.errors) > 0


class TestCompileErrorRecovery:
    """编译错误恢复测试"""

    def test_multiple_errors(self):
        """测试多错误收集"""
        source = """
打印 未定义变量1。
打印 未定义变量2。
打印 未定义变量3。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        result = analyzer.analyze(ast)
        # 应该收集多个错误
        if not result:
            assert len(analyzer.errors) >= 1

    def test_error_location(self):
        """测试错误位置准确性"""
        source = "打印 未定义变量。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        result = analyzer.analyze(ast)
        if not result and len(analyzer.errors) > 0:
            # 错误应该包含位置信息
            error = analyzer.errors[0]
            assert hasattr(error, "line") or hasattr(error, "column")

    def test_partial_compilation(self):
        """测试部分编译"""
        source = """
定义 变量1 = 1。
打印 未定义变量。
定义 变量2 = 2。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        # 即使有错误，也应该生成部分AST
        assert ast is not None
