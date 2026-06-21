#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""优化使用示例 - 展示如何在心语编程语言中使用性能优化"""

import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入不同的代码生成器
from src.codegen.python_codegen import PythonCodegen as OriginalCodegen
from src.codegen.python_codegen_optimized import OptimizedPythonCodegen as OptimizedCodegen
from src.codegen.python_codegen_with_optimized_folding import (
    OptimizedPythonCodegenWithOptimizedFolding as OptimizedWithFoldingCodegen,
)
from src.parser.ast_nodes import (
    AssignNode,
    BinaryOpNode,
    FunctionCallNode,
    IdentifierNode,
    IfNode,
    NumberNode,
    ProgramNode,
    ReturnNode,
    StringNode,
    UnaryOpNode,
    VarDefNode,
    WhileNode,
)


def create_example_ast():
    """创建示例AST"""
    return ProgramNode(
        line=1,
        column=1,
        statements=[
            # 常量表达式
            VarDefNode(
                line=1,
                column=1,
                name="x",
                value=BinaryOpNode(
                    line=1,
                    column=1,
                    left=NumberNode(line=1, column=1, value=10),
                    operator="+",
                    right=BinaryOpNode(
                        line=1,
                        column=1,
                        left=NumberNode(line=1, column=1, value=5),
                        operator="*",
                        right=NumberNode(line=1, column=1, value=2),
                    ),
                ),
            ),
            # 字符串连接
            VarDefNode(
                line=2,
                column=1,
                name="greeting",
                value=BinaryOpNode(
                    line=2,
                    column=1,
                    left=StringNode(line=2, column=1, value="Hello, "),
                    operator="+",
                    right=StringNode(line=2, column=1, value="World!"),
                ),
            ),
            # 条件语句
            IfNode(
                line=3,
                column=1,
                condition=BinaryOpNode(
                    line=3,
                    column=1,
                    left=IdentifierNode(line=3, column=1, name="x"),
                    operator=">",
                    right=NumberNode(line=3, column=1, value=0),
                ),
                then_branch=[
                    FunctionCallNode(
                        line=4,
                        column=5,
                        name=IdentifierNode(line=4, column=5, name="print"),
                        args=[
                            BinaryOpNode(
                                line=4,
                                column=5,
                                left=StringNode(line=4, column=5, value="x is positive: "),
                                operator="+",
                                right=IdentifierNode(line=4, column=5, name="x"),
                            )
                        ],
                    )
                ],
                else_branch=[
                    FunctionCallNode(
                        line=5,
                        column=5,
                        name=IdentifierNode(line=5, column=5, name="print"),
                        args=[StringNode(line=5, column=5, value="x is not positive")],
                    )
                ],
            ),
            # 循环
            VarDefNode(line=6, column=1, name="sum", value=NumberNode(line=6, column=1, value=0)),
            VarDefNode(line=7, column=1, name="i", value=NumberNode(line=7, column=1, value=0)),
            WhileNode(
                line=8,
                column=1,
                condition=BinaryOpNode(
                    line=8,
                    column=1,
                    left=IdentifierNode(line=8, column=1, name="i"),
                    operator="<",
                    right=NumberNode(line=8, column=1, value=10),
                ),
                body=[
                    AssignNode(
                        line=9,
                        column=5,
                        target=IdentifierNode(line=9, column=5, name="sum"),
                        value=BinaryOpNode(
                            line=9,
                            column=5,
                            left=IdentifierNode(line=9, column=5, name="sum"),
                            operator="+",
                            right=IdentifierNode(line=9, column=5, name="i"),
                        ),
                    ),
                    AssignNode(
                        line=10,
                        column=5,
                        target=IdentifierNode(line=10, column=5, name="i"),
                        value=BinaryOpNode(
                            line=10,
                            column=5,
                            left=IdentifierNode(line=10, column=5, name="i"),
                            operator="+",
                            right=NumberNode(line=10, column=5, value=1),
                        ),
                    ),
                ],
            ),
            # 函数调用
            FunctionCallNode(
                line=11,
                column=1,
                name=IdentifierNode(line=11, column=1, name="print"),
                args=[
                    BinaryOpNode(
                        line=11,
                        column=1,
                        left=StringNode(line=11, column=1, value="Sum: "),
                        operator="+",
                        right=IdentifierNode(line=11, column=1, name="sum"),
                    )
                ],
            ),
            # 复杂表达式
            VarDefNode(
                line=12,
                column=1,
                name="result",
                value=BinaryOpNode(
                    line=12,
                    column=1,
                    left=UnaryOpNode(
                        line=12,
                        column=1,
                        operator="-",
                        operand=NumberNode(line=12, column=1, value=5),
                    ),
                    operator="*",
                    right=BinaryOpNode(
                        line=12,
                        column=1,
                        left=NumberNode(line=12, column=1, value=10),
                        operator="/",
                        right=NumberNode(line=12, column=1, value=2),
                    ),
                ),
            ),
            # 返回语句
            ReturnNode(
                line=13,
                column=1,
                value=BinaryOpNode(
                    line=13,
                    column=1,
                    left=IdentifierNode(line=13, column=1, name="result"),
                    operator="+",
                    right=NumberNode(line=13, column=1, value=100),
                ),
            ),
        ],
    )


def compare_code_generation():
    """比较不同代码生成器的输出"""
    ast = create_example_ast()

    print("=" * 80)
    print("心语编程语言代码生成器优化示例")
    print("=" * 80)
    print()

    # 1. 原始代码生成器
    print("1. 原始代码生成器 (PythonCodegen):")
    print("-" * 40)
    original_codegen = OriginalCodegen()
    original_code = original_codegen.generate(ast)
    print(original_code)
    print(f"代码长度: {len(original_code)} 字符")
    print()

    # 2. 优化代码生成器（无常量折叠）
    print("2. 优化代码生成器 (OptimizedPythonCodegen):")
    print("-" * 40)
    optimized_codegen = OptimizedCodegen()
    optimized_code = optimized_codegen.generate(ast)
    print(optimized_code)
    print(f"代码长度: {len(optimized_code)} 字符")
    print()

    # 3. 优化代码生成器（带优化版常量折叠）
    print("3. 优化代码生成器 (OptimizedPythonCodegenWithOptimizedFolding):")
    print("-" * 40)
    optimized_with_folding_codegen = OptimizedWithFoldingCodegen(enable_optimizations=True)
    optimized_with_folding_code = optimized_with_folding_codegen.generate(ast)
    print(optimized_with_folding_code)
    print(f"代码长度: {len(optimized_with_folding_code)} 字符")

    # 获取优化统计
    stats = optimized_with_folding_codegen.get_optimization_stats()
    print("优化统计:")
    print(f"  常量折叠优化次数: {stats['constant_folding']}")
    print(f"  死代码消除次数: {stats['dead_code_elimination']}")
    print(f"  总优化次数: {stats['total_optimizations']}")
    print(f"  方法缓存命中率: {stats['method_cache_hit_rate']:.2%}")
    print()

    # 比较结果
    print("4. 比较结果:")
    print("-" * 40)
    print(f"原始代码长度: {len(original_code)} 字符")
    print(f"优化代码长度: {len(optimized_code)} 字符")
    print(f"优化+折叠代码长度: {len(optimized_with_folding_code)} 字符")
    print()

    print(f"代码减少 (优化 vs 原始): {len(original_code) - len(optimized_code)} 字符")
    print(f"代码减少 (优化+折叠 vs 原始): {len(original_code) - len(optimized_with_folding_code)} 字符")
    reduction_ratio = (
        (len(original_code) - len(optimized_with_folding_code)) / len(original_code) * 100
    )
    print(f"代码减少比例 (优化+折叠 vs 原始): {reduction_ratio:.1f}%")
    print()

    # 检查常量折叠效果
    print("5. 常量折叠效果检查:")
    print("-" * 40)

    # 查找原始代码中的常量表达式
    original_lines = original_code.split("\n")
    optimized_lines = optimized_with_folding_code.split("\n")

    print("原始代码中的常量表达式:")
    for i, line in enumerate(original_lines, 1):
        if "10 + (5 * 2)" in line:
            print(f"  行 {i}: {line.strip()}")
        elif "Hello, " in line and "World!" in line and "+" in line:
            print(f"  行 {i}: {line.strip()}")
        elif "-5 * (10 / 2)" in line:
            print(f"  行 {i}: {line.strip()}")

    print("\n优化后代码中的常量表达式:")
    for i, line in enumerate(optimized_lines, 1):
        if "x = 30" in line:
            print(f"  行 {i}: {line.strip()} (已折叠: 10 + (5 * 2) = 30)")
        elif "greeting = 'Hello, World!'" in line:
            print(f"  行 {i}: {line.strip()} (已折叠: 'Hello, ' + 'World!' = 'Hello, World!')")
        elif "result = -25.0" in line:
            print(f"  行 {i}: {line.strip()} (已折叠: -5 * (10 / 2) = -25.0)")

    print()
    print("=" * 80)
    print("使用建议:")
    print("-" * 80)
    print("1. 性能优先场景:")
    print("   from src.codegen.python_codegen_optimized import OptimizedPythonCodegen")
    print("   codegen = OptimizedPythonCodegen()")
    print("   # 性能提升: ~42.6%，代码大小不变")
    print()
    print("2. 代码大小优先场景:")
    print(
        "   from src.codegen.python_codegen_with_optimized_folding import "
        "OptimizedPythonCodegenWithOptimizedFolding"
    )
    print("   codegen = OptimizedPythonCodegenWithOptimizedFolding(enable_optimizations=True)")
    print("   # 性能: 基本持平，代码大小减少: ~66.4% (对于常量表达式)")
    print()
    print("3. 调试模式:")
    print("   codegen = OptimizedPythonCodegenWithOptimizedFolding(enable_optimizations=True)")
    print("   stats = codegen.get_optimization_stats()")
    print("   print(f'优化统计: {stats}')")
    print()
    print("4. 禁用优化:")
    print("   codegen = OptimizedPythonCodegenWithOptimizedFolding(enable_optimizations=False)")
    print("   # 或使用原始代码生成器")
    print("   from src.codegen.python_codegen import PythonCodegen")
    print("   codegen = PythonCodegen()")
    print("=" * 80)


def performance_comparison():
    """性能比较示例"""
    import time

    ast = create_example_ast()

    print("性能比较示例:")
    print("-" * 40)

    # 创建代码生成器实例
    original_codegen = OriginalCodegen()
    optimized_codegen = OptimizedCodegen()
    optimized_with_folding_codegen = OptimizedWithFoldingCodegen(enable_optimizations=True)

    # 测试配置
    iterations = 1000
    warmup = 100

    print(f"测试配置: {iterations} 次迭代，{warmup} 次预热")
    print()

    # 预热
    for _ in range(warmup):
        original_codegen.generate(ast)
        optimized_codegen.generate(ast)
        optimized_with_folding_codegen.generate(ast)

    # 测试原始版本
    print("测试原始版本...")
    start_time = time.perf_counter()
    for _ in range(iterations):
        original_codegen.generate(ast)
    original_time = time.perf_counter() - start_time

    # 测试优化版本
    print("测试优化版本（无常量折叠）...")
    start_time = time.perf_counter()
    for _ in range(iterations):
        optimized_codegen.generate(ast)
    optimized_time = time.perf_counter() - start_time

    # 测试优化版本（带常量折叠）
    print("测试优化版本（带优化版常量折叠）...")
    start_time = time.perf_counter()
    for _ in range(iterations):
        optimized_with_folding_codegen.generate(ast)
    optimized_with_folding_time = time.perf_counter() - start_time

    # 计算性能提升
    speedup_optimized = original_time / optimized_time
    speedup_with_folding = original_time / optimized_with_folding_time

    print()
    print("性能结果:")
    print("-" * 40)
    print(f"原始版本: {original_time:.6f} 秒")
    print(f"优化版本（无常量折叠）: {optimized_time:.6f} 秒")
    print(f"优化版本（带优化版常量折叠）: {optimized_with_folding_time:.6f} 秒")
    print()
    print(f"性能提升（优化 vs 原始）: {speedup_optimized:.2f}x")
    print(f"性能提升（优化+折叠 vs 原始）: {speedup_with_folding:.2f}x")
    print()

    # 获取优化统计
    stats = optimized_with_folding_codegen.get_optimization_stats()
    print("优化统计:")
    print(f"  常量折叠优化次数: {stats['constant_folding']}")
    print(f"  死代码消除次数: {stats['dead_code_elimination']}")
    print(f"  总优化次数: {stats['total_optimizations']}")
    print(f"  方法缓存命中率: {stats['method_cache_hit_rate']:.2%}")


def main():
    """主函数"""
    print("心语编程语言代码生成器优化使用示例")
    print("=" * 80)
    print()

    # 比较代码生成
    compare_code_generation()

    print()
    print("=" * 80)
    print()

    # 性能比较
    performance_comparison()

    print()
    print("=" * 80)
    print("示例完成!")
    print("=" * 80)


if __name__ == "__main__":
    main()
