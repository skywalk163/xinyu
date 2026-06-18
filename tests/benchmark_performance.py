# -*- coding: utf-8 -*-
"""性能基准测试

测试编译器各阶段的性能。
"""

import time

import pytest

from src.codegen.python_codegen import PythonCodegen
from src.lexer.lexer import Lexer
from src.main import ChineseProgram
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer


class TestLexerPerformance:
    """词法分析器性能测试"""

    def test_lexer_small_program(self, benchmark):
        """测试小程序词法分析性能"""
        source = "定 x = 5。"
        benchmark(Lexer(source).tokenize)

    def test_lexer_medium_program(self, benchmark):
        """测试中等程序词法分析性能"""
        source = """
定 x = 1。
定 y = 2。
定 z = x 加 y。
印z。

定 加法 = 函 a b：
    返回 a 加 b。

定 结果 = 加法(3, 4)。
印结果。
"""
        benchmark(Lexer(source).tokenize)

    def test_lexer_large_program(self, benchmark):
        """测试大程序词法分析性能"""
        # 生成100行代码
        lines = []
        for i in range(100):
            lines.append(f"定 x{i} = {i}。")
        source = "\n".join(lines)
        benchmark(Lexer(source).tokenize)

    def test_lexer_complex_expressions(self, benchmark):
        """测试复杂表达式词法分析性能"""
        source = """
定 a = 1 加 2 乘 3 减 4 除以 5。
定 b = (1 加 2) 乘 (3 减 4)。
定 c = a 加 b 乘 2。
"""
        benchmark(Lexer(source).tokenize)


class TestParserPerformance:
    """语法分析器性能测试"""

    def test_parser_small_program(self, benchmark):
        """测试小程序语法分析性能"""
        source = "定 x = 5。"
        lexer = Lexer(source)
    _ = kenize()  # 未使用变量
        benchmark(Parser(tokens).parse)

    def test_parser_medium_program(self, benchmark):
        """测试中等程序语法分析性能"""
        source = """
定 x = 1。
定 y = 2。
定 z = x 加 y。

定 加法 = 函 a b：
    返回 a 加 b。

定 结果 = 加法(3, 4)。
"""
        lexer = Lexer(source)
    _ = kenize()  # 未使用变量
        benchmark(Parser(tokens).parse)

    def test_parser_nested_functions(self, benchmark):
        """测试嵌套函数语法分析性能"""
        source = """
定 外层 = 函 x：
    定 内层 = 函 y：
        返回 x 加 y。
    返回 内层。

定 结果 = 外层(5)(3)。
"""
        lexer = Lexer(source)
    _ = kenize()  # 未使用变量
        benchmark(Parser(tokens).parse)

    def test_parser_complex_control_flow(self, benchmark):
        """测试复杂控制流语法分析性能"""
        source = """
定 x = 10。

若 x 大于 0 则：
    若 x 大于 5 则：
        印"大于5"。
    否则：
        印"小于等于5"。
否则：
    印"非正数"。

遍历 i 于 [1, 2, 3, 4, 5]：
    若 i 大于 2 则：
        印i。
"""
        lexer = Lexer(source)
    _ = kenize()  # 未使用变量
        benchmark(Parser(tokens).parse)


class TestSemanticPerformance:
    """语义分析器性能测试"""

    def test_semantic_small_program(self, benchmark):
        """测试小程序语义分析性能"""
        source = "定 x = 5。"
        lexer = Lexer(source)
    _ = kenize()  # 未使用变量
        parser = Parser(tokens)
    _ = arse()  # 未使用变量

        analyzer = SemanticAnalyzer()
        benchmark(analyzer.analyze, ast)

    def test_semantic_medium_program(self, benchmark):
        """测试中等程序语义分析性能"""
        source = """
定 x = 1。
定 y = 2。
定 z = x 加 y。

定 加法 = 函 a b：
    返回 a 加 b。

定 结果 = 加法(3, 4)。
"""
        lexer = Lexer(source)
    _ = kenize()  # 未使用变量
        parser = Parser(tokens)
    _ = arse()  # 未使用变量

        analyzer = SemanticAnalyzer()
        benchmark(analyzer.analyze, ast)

    def test_semantic_complex_scopes(self, benchmark):
        """测试复杂作用域语义分析性能"""
        source = """
定 全局 = 10。

定 函数1 = 函 x：
    定 局部1 = x 加 全局。

    定 函数2 = 函 y：
        定 局部2 = y 加 局部1。
        返回 局部2。

    返回 函数2。

定 结果 = 函数1(5)(3)。
"""
        lexer = Lexer(source)
    _ = kenize()  # 未使用变量
        parser = Parser(tokens)
    _ = arse()  # 未使用变量

        analyzer = SemanticAnalyzer()
        benchmark(analyzer.analyze, ast)


class TestCodegenPerformance:
    """代码生成器性能测试"""

    def test_codegen_small_program(self, benchmark):
        """测试小程序代码生成性能"""
        source = "定 x = 5。"
        lexer = Lexer(source)
    _ = kenize()  # 未使用变量
        parser = Parser(tokens)
    _ = arse()  # 未使用变量

        codegen = PythonCodegen()
        benchmark(codegen.generate, ast)

    def test_codegen_medium_program(self, benchmark):
        """测试中等程序代码生成性能"""
        source = """
定 x = 1。
定 y = 2。
定 z = x 加 y。

定 加法 = 函 a b：
    返回 a 加 b。

定 结果 = 加法(3, 4)。
"""
        lexer = Lexer(source)
    _ = kenize()  # 未使用变量
        parser = Parser(tokens)
    _ = arse()  # 未使用变量

        codegen = PythonCodegen()
        benchmark(codegen.generate, ast)

    def test_codegen_complex_program(self, benchmark):
        """测试复杂程序代码生成性能"""
        source = """
定 斐波那契 = 函 n：
    若 n 小于 2 则：
        返回 n。
    否则：
        返回 斐波那契(n 减 1) 加 斐波那契(n 减 2)。

遍历 i 于 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]：
    印斐波那契(i)。
"""
        lexer = Lexer(source)
    _ = kenize()  # 未使用变量
        parser = Parser(tokens)
    _ = arse()  # 未使用变量

        codegen = PythonCodegen()
        benchmark(codegen.generate, ast)


class TestFullPipelinePerformance:
    """完整编译流程性能测试"""

    def test_full_pipeline_small(self, benchmark):
        """测试小程序完整编译流程性能"""
        source = "定 x = 5。印x。"

        def compile_and_run():
            program = ChineseProgram()
            return program.run(source)

        benchmark(compile_and_run)

    def test_full_pipeline_medium(self, benchmark):
        """测试中等程序完整编译流程性能"""
        source = """
定 x = 1。
定 y = 2。
定 z = x 加 y。

定 加法 = 函 a b：
    返回 a 加 b。

定 结果 = 加法(3, 4)。
印结果。
"""

        def compile_and_run():
            program = ChineseProgram()
            return program.run(source)

        benchmark(compile_and_run)

    def test_full_pipeline_complex(self, benchmark):
        """测试复杂程序完整编译流程性能"""
        source = """
定 阶乘 = 函 n：
    若 n 小于等于 1 则：
        返回 1。
    否则：
        返回 n 乘 阶乘(n 减 1)。

遍历 i 于 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]：
    印阶乘(i)。
"""

        def compile_and_run():
            program = ChineseProgram()
            return program.run(source)

        benchmark(compile_and_run)


class TestMemoryUsage:
    """内存使用测试"""

    def test_memory_large_source(self):
        """测试大源代码内存使用"""
        # 生成1000行代码
        lines = []
        for i in range(1000):
            lines.append(f"定 x{i} = {i}。")
        source = "\n".join(lines)

        # 编译
        lexer = Lexer(source)
    _ = kenize()  # 未使用变量

        # 检查Token数量
        assert len(tokens) > 1000

        # 检查内存使用（简单检查）
        import sys

        token_size = sys.getsizeof(tokens)
        assert token_size < 10 * 1024 * 1024  # 小于10MB


class TestScalability:
    """可扩展性测试"""

    def test_scalability_linear_growth(self):
        """测试线性增长性能"""
        times = []
        sizes = [10, 50, 100, 200]

        for size in sizes:
            # 生成指定大小的代码
            lines = []
            for i in range(size):
                lines.append(f"定 x{i} = {i}。")
            source = "\n".join(lines)

            # 测量编译时间
            start = time.time()
            lexer = Lexer(source)
    _ = ze()  # 未使用变量
            parser = Parser(tokens)
    _ = ()  # 未使用变量
            end = time.time()

            times.append(end - start)

        # 检查时间增长是否合理（不超过线性增长）
        # 最后一个时间应该不超过第一个时间的20倍（允许一定波动）
        assert times[-1] < times[0] * 20


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--benchmark-only"])
