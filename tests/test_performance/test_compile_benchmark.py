"""编译性能基准测试

测试编译各阶段的性能。
"""
import pytest

from src.codegen.python_codegen import PythonCodegen
from src.lexer.lexer import Lexer
from src.main import ChineseProgram
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer

from .benchmark_utils import benchmark, format_result


class TestCompileBenchmark:
    """编译性能基准测试"""

    @benchmark(iterations=5, warmup=1)
    def test_lexer_performance_small(self):
        """测试词法分析性能（小规模：100行）"""
        source = "\n".join([f"定义 变量{i} = {i}。" for i in range(100)])
        lexer = Lexer(source)
        lexer.tokenize()

    @benchmark(iterations=5, warmup=1)
    def test_lexer_performance_medium(self):
        """测试词法分析性能（中规模：1000行）"""
        source = "\n".join([f"定义 变量{i} = {i}。" for i in range(1000)])
        lexer = Lexer(source)
        lexer.tokenize()

    @benchmark(iterations=3, warmup=1)
    def test_parser_performance_small(self):
        """测试语法分析性能（小规模：100行）"""
        source = "\n".join([f"定义 变量{i} = {i}。" for i in range(100)])
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parser.parse()

    @benchmark(iterations=3, warmup=1)
    def test_parser_performance_medium(self):
        """测试语法分析性能（中规模：1000行）"""
        source = "\n".join([f"定义 变量{i} = {i}。" for i in range(1000)])
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parser.parse()

    @benchmark(iterations=5, warmup=1)
    def test_semantic_performance_small(self):
        """测试语义分析性能（小规模：100行）"""
        source = "\n".join([f"定义 变量{i} = {i}。" for i in range(100)])
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)

    @benchmark(iterations=3, warmup=1)
    def test_semantic_performance_medium(self):
        """测试语义分析性能（中规模：1000行）"""
        source = "\n".join([f"定义 变量{i} = {i}。" for i in range(1000)])
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)

    @benchmark(iterations=5, warmup=1)
    def test_codegen_performance_small(self):
        """测试代码生成性能（小规模：100行）"""
        source = "\n".join([f"定义 变量{i} = {i}。" for i in range(100)])
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        codegen = PythonCodegen()
        codegen.generate(ast)

    @benchmark(iterations=3, warmup=1)
    def test_codegen_performance_medium(self):
        """测试代码生成性能（中规模：1000行）"""
        source = "\n".join([f"定义 变量{i} = {i}。" for i in range(1000)])
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        codegen = PythonCodegen()
        codegen.generate(ast)

    @benchmark(iterations=3, warmup=1)
    def test_full_compile_performance_small(self):
        """测试完整编译性能（小规模：100行）"""
        source = "\n".join([f"定义 变量{i} = {i}。" for i in range(100)])
        program = ChineseProgram()
        program.compile(source)

    @benchmark(iterations=2, warmup=1)
    def test_full_compile_performance_medium(self):
        """测试完整编译性能（中规模：1000行）"""
        source = "\n".join([f"定义 变量{i} = {i}。" for i in range(1000)])
        program = ChineseProgram()
        program.compile(source)

    def test_compile_performance_summary(self):
        """测试编译性能总结"""
        # 运行所有基准测试并输出结果
        small_source = "\n".join([f"定义 变量{i} = {i}。" for i in range(100)])
        medium_source = "\n".join([f"定义 变量{i} = {i}。" for i in range(1000)])

        # 小规模测试
        lexer_result = self.test_lexer_performance_small()
        parser_result = self.test_parser_performance_small()
        semantic_result = self.test_semantic_performance_small()
        codegen_result = self.test_codegen_performance_small()

        # 输出结果（用于调试）
        print(f"\n小规模（100行）性能:")
        print(format_result(lexer_result, "词法分析"))
        print(format_result(parser_result, "语法分析"))
        print(format_result(semantic_result, "语义分析"))
        print(format_result(codegen_result, "代码生成"))
