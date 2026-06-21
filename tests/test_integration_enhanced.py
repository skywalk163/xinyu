#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""错误处理和类型推断集成测试

测试新的集成版本是否正常工作。
"""


from src.error_handling import ErrorHandler, ErrorType
from src.lexer.lexer import Lexer
from src.lexer.lexer_with_error_handler import LexerWithErrorHandler
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.semantic.analyzer_with_inference import SemanticAnalyzerWithInference


class TestLexerWithErrorHandler:
    """测试集成了错误处理的词法分析器"""

    def test_basic_tokenization(self):
        """测试基本的词法分析功能"""
        source = "定义 x = 42"
        error_handler = ErrorHandler()
        lexer = LexerWithErrorHandler(source, error_handler)
        tokens = lexer.tokenize()

        assert not error_handler.has_errors()
        assert len(tokens) > 0
        assert tokens[-1].type.name == "EOF"

    def test_error_collection(self):
        """测试错误收集功能"""
        source = "定义 x = @#$"  # 非法字符
        error_handler = ErrorHandler()
        lexer = LexerWithErrorHandler(source, error_handler)
        lexer.tokenize()

        # 应该收集到错误
        assert error_handler.has_errors()
        errors = error_handler.get_errors()
        assert len(errors) > 0
        assert errors[0].error_type == ErrorType.LEXER_ERROR

    def test_multiple_errors(self):
        """测试多个错误的收集"""
        source = "定义 x = @ 定义 y = #"
        error_handler = ErrorHandler()
        lexer = LexerWithErrorHandler(source, error_handler)
        lexer.tokenize()

        assert error_handler.has_errors()
        errors = error_handler.get_errors()
        # 应该收集到至少一个错误
        assert len(errors) >= 1

    def test_unterminated_string(self):
        """测试未终止字符串的错误报告"""
        source = '定义 x = "未终止的字符串'
        error_handler = ErrorHandler()
        lexer = LexerWithErrorHandler(source, error_handler)
        lexer.tokenize()

        assert error_handler.has_errors()
        errors = error_handler.get_errors()
        assert any("字符串未终止" in err.message for err in errors)

    def test_chinese_operators(self):
        """测试中文操作符的正确识别"""
        source = "相加 相减 相乘 除"
        error_handler = ErrorHandler()
        lexer = LexerWithErrorHandler(source, error_handler)
        tokens = lexer.tokenize()

        assert not error_handler.has_errors()
        # 检查操作符被正确识别
        operator_tokens = [
            t for t in tokens if t.type.name in ["PLUS", "MINUS", "MULTIPLY", "DIVIDE"]
        ]
        assert len(operator_tokens) == 4


class TestSemanticAnalyzerWithInference:
    """测试集成了类型推断的语义分析器"""

    def test_basic_analysis(self):
        """测试基本的语义分析功能"""
        source = "定义 x = 42"
        error_handler = ErrorHandler()
        lexer = LexerWithErrorHandler(source, error_handler)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        analyzer = SemanticAnalyzerWithInference(error_handler)
        success = analyzer.analyze(ast)

        assert success
        assert not error_handler.has_errors()

    def test_type_inference_number(self):
        """测试数字类型推断"""
        source = "定义 x = 42"
        error_handler = ErrorHandler()
        lexer = LexerWithErrorHandler(source, error_handler)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        analyzer = SemanticAnalyzerWithInference(error_handler)
        analyzer.analyze(ast)

        # 检查变量类型
        symbol = analyzer.current_scope.lookup("x")
        assert symbol is not None
        assert symbol.get("value_type") == "number"

    def test_type_inference_string(self):
        """测试字符串类型推断"""
        source = '定义 x = "你好"'
        error_handler = ErrorHandler()
        lexer = LexerWithErrorHandler(source, error_handler)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        analyzer = SemanticAnalyzerWithInference(error_handler)
        analyzer.analyze(ast)

        # 检查变量类型
        symbol = analyzer.current_scope.lookup("x")
        assert symbol is not None
        assert symbol.get("value_type") == "string"

    def test_undefined_variable_error(self):
        """测试未定义变量的错误报告"""
        source = "打印 未定义变量"
        error_handler = ErrorHandler()
        lexer = LexerWithErrorHandler(source, error_handler)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        analyzer = SemanticAnalyzerWithInference(error_handler)
        analyzer.analyze(ast)

        # 应该报告错误
        assert error_handler.has_errors()
        errors = error_handler.get_errors()
        assert any("未定义" in err.message for err in errors)

    def test_redefinition_error(self):
        """测试重复定义的错误报告"""
        source = "定义 x = 1。定义 x = 2。"
        error_handler = ErrorHandler()
        lexer = LexerWithErrorHandler(source, error_handler)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        analyzer = SemanticAnalyzerWithInference(error_handler)
        analyzer.analyze(ast)

        # 应该报告错误
        assert error_handler.has_errors()
        errors = error_handler.get_errors()
        assert any("已定义" in err.message for err in errors)

    def test_builtin_function(self):
        """测试内置函数"""
        source = '打印 "你好"。'
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        analyzer = SemanticAnalyzer()
        success = analyzer.analyze(ast)

        assert success


class TestIntegration:
    """集成测试"""

    def test_full_pipeline(self):
        """测试完整的编译流程"""
        source = """
定义 x = 42。
定义 y = "你好"。
打印 x。
打印 y。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        analyzer = SemanticAnalyzer()
        success = analyzer.analyze(ast)

        assert success

        # 检查类型推断结果
        x_symbol = analyzer.current_scope.lookup("x")
        y_symbol = analyzer.current_scope.lookup("y")

        assert x_symbol is not None
        assert y_symbol is not None

    def test_error_recovery(self):
        """测试错误恢复能力"""
        source = "定义 y = 42。打印 y。"
        error_handler = ErrorHandler()
        lexer = LexerWithErrorHandler(source, error_handler)
        tokens = lexer.tokenize()

        # 不应该有词法错误
        assert not error_handler.has_errors()

        # 可以正常分析
        parser = Parser(tokens)
        ast = parser.parse()

        analyzer = SemanticAnalyzerWithInference(error_handler)
        analyzer.analyze(ast)

        # y 应该被正确分析
        y_symbol = analyzer.current_scope.lookup("y")
        assert y_symbol is not None
        assert y_symbol.get("value_type") == "number"
