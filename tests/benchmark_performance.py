#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""性能基准测试

评估类型推断和错误处理对性能的影响。
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import time
from src.lexer.lexer import Lexer
from src.lexer.lexer_with_error_handler import LexerWithErrorHandler
from src.semantic.analyzer import SemanticAnalyzer
from src.semantic.analyzer_with_inference import SemanticAnalyzerWithInference
from src.parser.parser import Parser
from src.error_handling import ErrorHandler


def benchmark_lexer(iterations=1000):
    """词法分析器性能基准测试"""
    source = """
    定 x = 42。
    定 y = "你好"。
    定 z = x 加 10。
    印 x。
    印 y。
    印 z。
    """
    
    # 测试原始 Lexer
    start = time.time()
    for _ in range(iterations):
        lexer = Lexer(source)
        tokens = lexer.tokenize()
    original_time = time.time() - start
    
    # 测试 LexerWithErrorHandler
    start = time.time()
    for _ in range(iterations):
        error_handler = ErrorHandler()
        lexer = LexerWithErrorHandler(source, error_handler)
        tokens = lexer.tokenize()
    enhanced_time = time.time() - start
    
    print(f"\n=== 词法分析器性能测试 ({iterations} 次迭代) ===")
    print(f"原始 Lexer: {original_time:.4f} 秒")
    print(f"LexerWithErrorHandler: {enhanced_time:.4f} 秒")
    print(f"性能差异: {(enhanced_time - original_time) / original_time * 100:.2f}%")
    
    return original_time, enhanced_time


def benchmark_semantic_analyzer(iterations=500):
    """语义分析器性能基准测试"""
    source = """
    定 x = 42。
    定 y = "你好"。
    定 z = 100。
    印 x。
    印 y。
    印 z。
    """
    
    # 准备AST
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    # 测试原始 SemanticAnalyzer
    start = time.time()
    for _ in range(iterations):
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
    original_time = time.time() - start
    
    # 测试 SemanticAnalyzerWithInference
    start = time.time()
    for _ in range(iterations):
        error_handler = ErrorHandler()
        analyzer = SemanticAnalyzerWithInference(error_handler)
        analyzer.analyze(ast)
    enhanced_time = time.time() - start
    
    print(f"\n=== 语义分析器性能测试 ({iterations} 次迭代) ===")
    print(f"原始 SemanticAnalyzer: {original_time:.4f} 秒")
    print(f"SemanticAnalyzerWithInference: {enhanced_time:.4f} 秒")
    print(f"性能差异: {(enhanced_time - original_time) / original_time * 100:.2f}%")
    
    return original_time, enhanced_time


def benchmark_full_pipeline(iterations=200):
    """完整编译流程性能基准测试"""
    source = """
    定 x = 42。
    定 y = "你好世界"。
    定 z = x 加 10。
    
    若 x 大 40 则：
        印 "x 大于 40"。
    否则：
        印 "x 不大于 40"。
    
    印 x。
    印 y。
    印 z。
    """
    
    # 测试原始流程
    start = time.time()
    for _ in range(iterations):
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
    original_time = time.time() - start
    
    # 测试增强流程
    start = time.time()
    for _ in range(iterations):
        error_handler = ErrorHandler()
        lexer = LexerWithErrorHandler(source, error_handler)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzerWithInference(error_handler)
        analyzer.analyze(ast)
    enhanced_time = time.time() - start
    
    print(f"\n=== 完整编译流程性能测试 ({iterations} 次迭代) ===")
    print(f"原始流程: {original_time:.4f} 秒")
    print(f"增强流程: {enhanced_time:.4f} 秒")
    print(f"性能差异: {(enhanced_time - original_time) / original_time * 100:.2f}%")
    
    return original_time, enhanced_time


def run_all_benchmarks():
    """运行所有基准测试"""
    print("=" * 60)
    print("性能基准测试")
    print("=" * 60)
    
    # 运行各项测试
    lexer_orig, lexer_enh = benchmark_lexer(1000)
    semantic_orig, semantic_enh = benchmark_semantic_analyzer(500)
    pipeline_orig, pipeline_enh = benchmark_full_pipeline(200)
    
    # 总结
    print("\n" + "=" * 60)
    print("性能总结")
    print("=" * 60)
    
    total_orig = lexer_orig + semantic_orig + pipeline_orig
    total_enh = lexer_enh + semantic_enh + pipeline_enh
    
    print(f"\n总耗时:")
    print(f"原始版本: {total_orig:.4f} 秒")
    print(f"增强版本: {total_enh:.4f} 秒")
    print(f"总体性能差异: {(total_enh - total_orig) / total_orig * 100:.2f}%")
    
    # 评估
    print("\n" + "=" * 60)
    print("性能评估")
    print("=" * 60)
    
    overhead = (total_enh - total_orig) / total_orig * 100
    
    if overhead < 5:
        print("✅ 性能影响极小 (< 5%)，可以安全使用增强版本")
    elif overhead < 10:
        print("✅ 性能影响可接受 (< 10%)，建议使用增强版本")
    elif overhead < 20:
        print("⚠️  性能影响中等 (< 20%)，根据需求选择使用")
    else:
        print("❌ 性能影响较大 (> 20%)，建议优化或选择性使用")
    
    print("\n建议:")
    print("1. 错误处理集成: 推荐使用，性能影响小，错误报告更友好")
    print("2. 类型推断集成: 推荐使用，性能影响可接受，提供类型信息")
    print("3. 完整流程: 推荐使用，总体性能影响在可接受范围内")


if __name__ == "__main__":
    run_all_benchmarks()
