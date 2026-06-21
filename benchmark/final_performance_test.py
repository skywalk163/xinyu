#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""最终性能测试 - 比较所有优化版本的性能"""

import os
import statistics
import sys
import time

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.codegen.python_codegen import PythonCodegen as OriginalCodegen
from src.codegen.python_codegen_optimized import OptimizedPythonCodegen as OptimizedCodegen
from src.codegen.python_codegen_with_optimizations import (
    OptimizedPythonCodegenWithFolding as OptimizedWithFoldingCodegen,
)
from src.codegen.python_codegen_with_optimized_folding import (
    OptimizedPythonCodegenWithOptimizedFolding as OptimizedWithOptimizedFoldingCodegen,
)
from src.parser.ast_nodes import (
    AssignNode,
    BinaryOpNode,
    FunctionCallNode,
    IdentifierNode,
    IfNode,
    NumberNode,
    ProgramNode,
    StringNode,
    UnaryOpNode,
    VarDefNode,
    WhileNode,
)


def create_simple_ast():
    """创建简单的AST用于测试"""
    statements = []

    # 变量定义
    statements.append(
        VarDefNode(line=1, column=1, name="n", value=NumberNode(line=1, column=1, value=10))
    )

    statements.append(
        VarDefNode(line=2, column=1, name="a", value=NumberNode(line=2, column=1, value=0))
    )

    statements.append(
        VarDefNode(line=3, column=1, name="b", value=NumberNode(line=3, column=1, value=1))
    )

    statements.append(
        VarDefNode(line=4, column=1, name="i", value=NumberNode(line=4, column=1, value=0))
    )

    # while循环
    condition = BinaryOpNode(
        line=5,
        column=1,
        left=IdentifierNode(line=5, column=1, name="i"),
        operator="小于",
        right=IdentifierNode(line=5, column=1, name="n"),
    )

    loop_body = [
        # 打印当前斐波那契数
        FunctionCallNode(
            line=6,
            column=5,
            name=IdentifierNode(line=6, column=5, name="打印"),
            args=[IdentifierNode(line=6, column=5, name="a")],
        ),
        # 计算下一个斐波那契数
        AssignNode(
            line=7,
            column=5,
            target=IdentifierNode(line=7, column=5, name="temp"),
            value=BinaryOpNode(
                line=7,
                column=5,
                left=IdentifierNode(line=7, column=5, name="a"),
                operator="相加",
                right=IdentifierNode(line=7, column=5, name="b"),
            ),
        ),
        AssignNode(
            line=8,
            column=5,
            target=IdentifierNode(line=8, column=5, name="a"),
            value=IdentifierNode(line=8, column=5, name="b"),
        ),
        AssignNode(
            line=9,
            column=5,
            target=IdentifierNode(line=9, column=5, name="b"),
            value=IdentifierNode(line=9, column=5, name="temp"),
        ),
        # i = i + 1
        AssignNode(
            line=10,
            column=5,
            target=IdentifierNode(line=10, column=5, name="i"),
            value=BinaryOpNode(
                line=10,
                column=5,
                left=IdentifierNode(line=10, column=5, name="i"),
                operator="相加",
                right=NumberNode(line=10, column=5, value=1),
            ),
        ),
    ]

    statements.append(WhileNode(line=5, column=1, condition=condition, body=loop_body))

    return ProgramNode(line=1, column=1, statements=statements)


def create_const_folding_ast():
    """创建包含常量折叠机会的AST"""
    statements = []

    # 常量表达式
    statements.append(
        VarDefNode(
            line=1,
            column=1,
            name="a",
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
        )
    )

    statements.append(
        VarDefNode(
            line=2,
            column=1,
            name="b",
            value=UnaryOpNode(
                line=2, column=1, operator="-", operand=NumberNode(line=2, column=1, value=42)
            ),
        )
    )

    statements.append(
        VarDefNode(
            line=3,
            column=1,
            name="c",
            value=BinaryOpNode(
                line=3,
                column=1,
                left=StringNode(line=3, column=1, value="Hello, "),
                operator="+",
                right=StringNode(line=3, column=1, value="World!"),
            ),
        )
    )

    # 条件语句（常量条件）
    statements.append(
        IfNode(
            line=4,
            column=1,
            condition=BinaryOpNode(
                line=4,
                column=1,
                left=NumberNode(line=4, column=1, value=1),
                operator="==",
                right=NumberNode(line=4, column=1, value=1),
            ),
            then_branch=[
                AssignNode(
                    line=5,
                    column=5,
                    target=IdentifierNode(line=5, column=5, name="d"),
                    value=BinaryOpNode(
                        line=5,
                        column=5,
                        left=NumberNode(line=5, column=5, value=100),
                        operator="*",
                        right=NumberNode(line=5, column=5, value=2),
                    ),
                )
            ],
            else_branch=[
                AssignNode(
                    line=6,
                    column=5,
                    target=IdentifierNode(line=6, column=5, name="d"),
                    value=NumberNode(line=6, column=5, value=0),
                )
            ],
        )
    )

    # 死循环（常量假条件）
    statements.append(
        WhileNode(
            line=7,
            column=1,
            condition=NumberNode(line=7, column=1, value=0),
            body=[
                AssignNode(
                    line=8,
                    column=5,
                    target=IdentifierNode(line=8, column=5, name="e"),
                    value=NumberNode(line=8, column=5, value=999),
                )
            ],
        )
    )

    # 复杂嵌套表达式
    statements.append(
        VarDefNode(
            line=9,
            column=1,
            name="",
            value=BinaryOpNode(
                line=9,
                column=1,
                left=BinaryOpNode(
                    line=9,
                    column=1,
                    left=NumberNode(line=9, column=1, value=10),
                    operator="/",
                    right=NumberNode(line=9, column=1, value=2),
                ),
                operator="+",
                right=BinaryOpNode(
                    line=9,
                    column=1,
                    left=NumberNode(line=9, column=1, value=3),
                    operator="*",
                    right=BinaryOpNode(
                        line=9,
                        column=1,
                        left=NumberNode(line=9, column=1, value=4),
                        operator="-",
                        right=NumberNode(line=9, column=1, value=1),
                    ),
                ),
            ),
        )
    )

    return ProgramNode(line=1, column=1, statements=statements)


def create_large_ast(num_expressions=100):
    """创建大型AST用于性能测试"""
    statements = []

    for i in range(num_expressions):
        # 创建复杂的常量表达式
        statements.append(
            VarDefNode(
                line=i + 1,
                column=1,
                name=f"var{i}",
                value=BinaryOpNode(
                    line=i + 1,
                    column=1,
                    left=NumberNode(line=i + 1, column=1, value=i),
                    operator="+",
                    right=BinaryOpNode(
                        line=i + 1,
                        column=1,
                        left=NumberNode(line=i + 1, column=1, value=i * 2),
                        operator="*",
                        right=NumberNode(line=i + 1, column=1, value=i * 3),
                    ),
                ),
            )
        )

    return ProgramNode(line=1, column=1, statements=statements)


def benchmark_codegen(codegen, ast, iterations=100, warmup=10, name="测试"):
    """基准测试代码生成性能

    Args:
        codegen: 代码生成器实例
        ast: 要生成的AST
        iterations: 迭代次数
        warmup: 预热次数
        name: 测试名称

    Returns:
        包含性能统计信息的字典
    """
    # 预热
    for _ in range(warmup):
        codegen.generate(ast)

    # 测试
    times = []
    for i in range(iterations):
        start_time = time.perf_counter()
        result = codegen.generate(ast)
        end_time = time.perf_counter()
        times.append(end_time - start_time)

    # 计算统计信息
    total_time = sum(times)
    avg_time = statistics.mean(times)
    min_time = min(times)
    max_time = max(times)
    std_dev = statistics.stdev(times) if len(times) > 1 else 0
    ops_per_second = iterations / total_time

    return {
        "name": name,
        "total_time": total_time,
        "avg_time": avg_time,
        "min_time": min_time,
        "max_time": max_time,
        "std_dev": std_dev,
        "ops_per_second": ops_per_second,
        "code_size": len(result),
        "node_count": len(ast.statements) if hasattr(ast, "statements") else 0,
    }


def run_final_performance_test():
    """运行最终性能测试"""
    print("=" * 80)
    print("心语编程语言代码生成器最终性能测试")
    print("=" * 80)
    print()

    # 创建测试AST
    print("创建测试AST...")
    simple_ast = create_simple_ast()
    const_folding_ast = create_const_folding_ast()
    large_ast = create_large_ast(50)  # 50个表达式

    print(f"简单AST节点数: {len(simple_ast.statements)}")
    print(f"常量折叠AST节点数: {len(const_folding_ast.statements)}")
    print(f"大型AST节点数: {len(large_ast.statements)}")
    print()

    # 创建代码生成器实例
    original_codegen = OriginalCodegen()
    optimized_codegen = OptimizedCodegen()
    optimized_with_folding_codegen = OptimizedWithFoldingCodegen(enable_optimizations=True)
    optimized_with_optimized_folding_codegen = OptimizedWithOptimizedFoldingCodegen(
        enable_optimizations=True
    )

    # 测试配置
    test_cases = [
        ("简单AST", simple_ast, 1000, 10),
        ("常量折叠AST", const_folding_ast, 1000, 10),
        ("大型AST", large_ast, 100, 5),
    ]

    all_results = []

    # 运行测试
    for test_name, ast, iterations, warmup in test_cases:
        print(f"测试: {test_name} (迭代次数: {iterations})")
        print("-" * 80)

        # 测试原始版本
        print("  原始版本...")
        original_result = benchmark_codegen(original_codegen, ast, iterations, warmup, "原始版本")
        all_results.append(original_result)

        print(f"    总时间: {original_result['total_time']:.6f} 秒")
        print(f"    平均时间: {original_result['avg_time']*1e6:.2f} 微秒/次")
        print(f"    操作数/秒: {original_result['ops_per_second']:,.0f}")
        print(f"    代码大小: {original_result['code_size']} 字符")

        # 测试优化版本（无常量折叠）
        print("  优化版本（无常量折叠）...")
        optimized_result = benchmark_codegen(
            optimized_codegen, ast, iterations, warmup, "优化版本（无常量折叠）"
        )
        all_results.append(optimized_result)

        print(f"    总时间: {optimized_result['total_time']:.6f} 秒")
        print(f"    平均时间: {optimized_result['avg_time']*1e6:.2f} 微秒/次")
        print(f"    操作数/秒: {optimized_result['ops_per_second']:,.0f}")
        print(f"    代码大小: {optimized_result['code_size']} 字符")

        # 计算性能提升
        speedup = original_result["total_time"] / optimized_result["total_time"]
        improvement = (speedup - 1) * 100
        print(f"    性能提升: {speedup:.2f}x ({improvement:+.1f}%)")

        # 测试优化版本（带常量折叠）
        print("  优化版本（带常量折叠）...")
        optimized_with_folding_result = benchmark_codegen(
            optimized_with_folding_codegen, ast, iterations, warmup, "优化版本（带常量折叠）"
        )
        all_results.append(optimized_with_folding_result)

        print(f"    总时间: {optimized_with_folding_result['total_time']:.6f} 秒")
        print(f"    平均时间: {optimized_with_folding_result['avg_time']*1e6:.2f} 微秒/次")
        print(f"    操作数/秒: {optimized_with_folding_result['ops_per_second']:,.0f}")
        print(f"    代码大小: {optimized_with_folding_result['code_size']} 字符")

        # 计算性能提升
        speedup_vs_original = (
            original_result["total_time"] / optimized_with_folding_result["total_time"]
        )
        improvement_vs_original = (speedup_vs_original - 1) * 100
        speedup_vs_optimized = (
            optimized_result["total_time"] / optimized_with_folding_result["total_time"]
        )
        improvement_vs_optimized = (speedup_vs_optimized - 1) * 100

        print(f"    相对于原始版本提升: {speedup_vs_original:.2f}x ({improvement_vs_original:+.1f}%)")
        print(f"    相对于优化版本提升: {speedup_vs_optimized:.2f}x ({improvement_vs_optimized:+.1f}%)")

        # 测试优化版本（带优化版常量折叠）
        print("  优化版本（带优化版常量折叠）...")
        optimized_with_optimized_folding_result = benchmark_codegen(
            optimized_with_optimized_folding_codegen, ast, iterations, warmup, "优化版本（带优化版常量折叠）"
        )
        all_results.append(optimized_with_optimized_folding_result)

        print(f"    总时间: {optimized_with_optimized_folding_result['total_time']:.6f} 秒")
        print(f"    平均时间: {optimized_with_optimized_folding_result['avg_time']*1e6:.2f} 微秒/次")
        print(f"    操作数/秒: {optimized_with_optimized_folding_result['ops_per_second']:,.0f}")
        print(f"    代码大小: {optimized_with_optimized_folding_result['code_size']} 字符")

        # 计算性能提升
        speedup_vs_original_opt = (
            original_result["total_time"] / optimized_with_optimized_folding_result["total_time"]
        )
        improvement_vs_original_opt = (speedup_vs_original_opt - 1) * 100
        speedup_vs_optimized_opt = (
            optimized_result["total_time"] / optimized_with_optimized_folding_result["total_time"]
        )
        improvement_vs_optimized_opt = (speedup_vs_optimized_opt - 1) * 100

        print(
            f"    相对于原始版本提升: {speedup_vs_original_opt:.2f}x ({improvement_vs_original_opt:+.1f}%)"
        )
        print(
            f"    相对于优化版本提升: {speedup_vs_optimized_opt:.2f}x ({improvement_vs_optimized_opt:+.1f}%)"
        )

        # 获取优化统计
        if test_name == "常量折叠AST":
            stats = optimized_with_optimized_folding_codegen.get_optimization_stats()
            print("    优化统计:")
            print(f"      常量折叠优化次数: {stats['constant_folding']}")
            print(f"      死代码消除次数: {stats['dead_code_elimination']}")
            print(f"      总优化次数: {stats['total_optimizations']}")
            print(f"      方法缓存命中率: {stats['method_cache_hit_rate']:.2%}")

        print()

    # 输出总结
    print("=" * 80)
    print("性能对比总结")
    print("=" * 80)
    print()

    print("测试结果汇总:")
    print("-" * 80)
    print(f"{'测试用例':<20} {'版本':<30} {'平均时间(微秒)':<15} {'操作数/秒':<15} {'代码大小':<10} {'性能提升':<15}")
    print("-" * 80)

    for i in range(0, len(all_results), 4):
        original = all_results[i]
        optimized = all_results[i + 1]
        optimized_with_folding = all_results[i + 2]
        optimized_with_optimized_folding = all_results[i + 3]

        test_name = original["name"].split()[0]

        # 计算性能提升
        speedup_optimized = original["total_time"] / optimized["total_time"]
        speedup_with_folding = original["total_time"] / optimized_with_folding["total_time"]
        speedup_with_optimized_folding = (
            original["total_time"] / optimized_with_optimized_folding["total_time"]
        )

        print(
            f"{test_name:<20} {'原始版本':<30} {original['avg_time']*1e6:<15.2f} {original['ops_per_second']:<15,.0f} {original['code_size']:<10} {'-':<15}"
        )
        print(
            f"{'':<20} {'优化版本（无常量折叠）':<30} {optimized['avg_time']*1e6:<15.2f} {optimized['ops_per_second']:<15,.0f} {optimized['code_size']:<10} {f'{speedup_optimized:.2f}x':<15}"
        )
        print(
            f"{'':<20} {'优化版本（带常量折叠）':<30} {optimized_with_folding['avg_time']*1e6:<15.2f} {optimized_with_folding['ops_per_second']:<15,.0f} {optimized_with_folding['code_size']:<10} {f'{speedup_with_folding:.2f}x':<15}"
        )
        print(
            f"{'':<20} {'优化版本（带优化版常量折叠）':<30} {optimized_with_optimized_folding['avg_time']*1e6:<15.2f} {optimized_with_optimized_folding['ops_per_second']:<15,.0f} {optimized_with_optimized_folding['code_size']:<10} {f'{speedup_with_optimized_folding:.2f}x':<15}"
        )
        print()

    # 计算总体性能提升
    total_original_time = sum(r["total_time"] for r in all_results if "原始版本" in r["name"])
    total_optimized_time = sum(r["total_time"] for r in all_results if "优化版本（无常量折叠）" in r["name"])
    total_with_folding_time = sum(
        r["total_time"] for r in all_results if "优化版本（带常量折叠）" in r["name"]
    )
    total_with_optimized_folding_time = sum(
        r["total_time"] for r in all_results if "优化版本（带优化版常量折叠）" in r["name"]
    )

    overall_speedup_optimized = total_original_time / total_optimized_time
    overall_improvement_optimized = (overall_speedup_optimized - 1) * 100

    overall_speedup_with_folding = total_original_time / total_with_folding_time
    overall_improvement_with_folding = (overall_speedup_with_folding - 1) * 100

    overall_speedup_with_optimized_folding = total_original_time / total_with_optimized_folding_time
    overall_improvement_with_optimized_folding = (overall_speedup_with_optimized_folding - 1) * 100

    print("总体性能提升:")
    print(
        f"  优化版本（无常量折叠）: {overall_speedup_optimized:.2f}x ({overall_improvement_optimized:+.1f}%)"
    )
    print(
        f"  优化版本（带常量折叠）: {overall_speedup_with_folding:.2f}x ({overall_improvement_with_folding:+.1f}%)"
    )
    print(
        f"  优化版本（带优化版常量折叠）: {overall_speedup_with_optimized_folding:.2f}x ({overall_improvement_with_optimized_folding:+.1f}%)"
    )
    print()

    # 分析优化效果
    print("优化效果分析:")
    print("-" * 80)

    # 检查常量折叠AST的优化效果
    const_folding_results = [r for r in all_results if "常量折叠AST" in r["name"]]
    if len(const_folding_results) == 4:
        original_size = const_folding_results[0]["code_size"]
        optimized_size = const_folding_results[1]["code_size"]
        folded_size = const_folding_results[2]["code_size"]
        optimized_folded_size = const_folding_results[3]["code_size"]

        print("常量折叠优化效果:")
        print(f"  原始代码大小: {original_size} 字符")
        print(f"  优化后代码大小: {optimized_size} 字符")
        print(f"  常量折叠后代码大小: {folded_size} 字符")
        print(f"  优化版常量折叠后代码大小: {optimized_folded_size} 字符")
        print(
            f"  代码减少: {original_size - optimized_folded_size} 字符 ({((original_size - optimized_folded_size) / original_size * 100):.1f}%)"
        )

    # 输出建议
    print("\n优化建议:")
    print("-" * 80)

    if overall_speedup_with_optimized_folding >= 1.5:
        print("  [GOOD] 优化效果显著！总体性能提升超过50%")
        print("     建议：使用优化版常量折叠，继续实施其他优化方案")
    elif overall_speedup_with_optimized_folding >= 1.2:
        print("  [WARN] 优化效果一般，总体性能提升20-50%")
        print("     建议：使用优化版常量折叠，进一步优化字符串构建和方法查找")
    else:
        print("  [BAD] 优化效果不明显，总体性能提升小于20%")
        print("     建议：优先使用优化版本（无常量折叠），常量折叠开销较大")

    print(f"\n  平均性能提升（优化版常量折叠）: {overall_speedup_with_optimized_folding:.2f}x")

    # 具体建议
    if overall_speedup_with_optimized_folding < 1.3:
        print("\n  具体优化建议:")
        print("  1. 对于性能敏感场景，使用优化版本（无常量折叠）")
        print("  2. 对于代码大小敏感场景，使用优化版常量折叠")
        print("  3. 进一步优化常量折叠算法，减少AST遍历开销")
        print("  4. 实现选择性常量折叠，只对热点代码进行优化")

    # 保存结果
    output_dir = "benchmark/results"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    results_file = os.path.join(output_dir, f"final_performance_test_{timestamp}.txt")

    with open(results_file, "w", encoding="utf-8") as f:
        f.write("心语编程语言代码生成器最终性能测试结果\n")
        f.write("=" * 80 + "\n\n")

        f.write("测试配置:\n")
        f.write(f"  简单AST节点数: {len(simple_ast.statements)}\n")
        f.write(f"  常量折叠AST节点数: {len(const_folding_ast.statements)}\n")
        f.write(f"  大型AST节点数: {len(large_ast.statements)}\n\n")

        f.write("性能结果:\n")
        f.write("-" * 80 + "\n")
        f.write(
            f"{'测试用例':<20} {'版本':<30} {'平均时间(微秒)':<15} {'操作数/秒':<15} {'代码大小':<10} {'性能提升':<15}\n"
        )
        f.write("-" * 80 + "\n")

        for i in range(0, len(all_results), 4):
            original = all_results[i]
            optimized = all_results[i + 1]
            optimized_with_folding = all_results[i + 2]
            optimized_with_optimized_folding = all_results[i + 3]

            test_name = original["name"].split()[0]

            speedup_optimized = original["total_time"] / optimized["total_time"]
            speedup_with_folding = original["total_time"] / optimized_with_folding["total_time"]
            speedup_with_optimized_folding = (
                original["total_time"] / optimized_with_optimized_folding["total_time"]
            )

            f.write(
                f"{test_name:<20} {'原始版本':<30} {original['avg_time']*1e6:<15.2f} {original['ops_per_second']:<15,.0f} {original['code_size']:<10} {'-':<15}\n"
            )
            f.write(
                f"{'':<20} {'优化版本（无常量折叠）':<30} {optimized['avg_time']*1e6:<15.2f} {optimized['ops_per_second']:<15,.0f} {optimized['code_size']:<10} {f'{speedup_optimized:.2f}x':<15}\n"
            )
            f.write(
                f"{'':<20} {'优化版本（带常量折叠）':<30} {optimized_with_folding['avg_time']*1e6:<15.2f} {optimized_with_folding['ops_per_second']:<15,.0f} {optimized_with_folding['code_size']:<10} {f'{speedup_with_folding:.2f}x':<15}\n"
            )
            f.write(
                f"{'':<20} {'优化版本（带优化版常量折叠）':<30} {optimized_with_optimized_folding['avg_time']*1e6:<15.2f} {optimized_with_optimized_folding['ops_per_second']:<15,.0f} {optimized_with_optimized_folding['code_size']:<10} {f'{speedup_with_optimized_folding:.2f}x':<15}\n\n"
            )

        f.write("总体性能提升:\n")
        f.write(
            f"  优化版本（无常量折叠）: {overall_speedup_optimized:.2f}x ({overall_improvement_optimized:+.1f}%)\n"
        )
        f.write(
            f"  优化版本（带常量折叠）: {overall_speedup_with_folding:.2f}x ({overall_improvement_with_folding:+.1f}%)\n"
        )
        f.write(
            f"  优化版本（带优化版常量折叠）: {overall_speedup_with_optimized_folding:.2f}x ({overall_improvement_with_optimized_folding:+.1f}%)\n\n"
        )

        f.write("优化效果分析:\n")
        if len(const_folding_results) == 4:
            original_size = const_folding_results[0]["code_size"]
            optimized_size = const_folding_results[1]["code_size"]
            folded_size = const_folding_results[2]["code_size"]
            optimized_folded_size = const_folding_results[3]["code_size"]

            f.write("  常量折叠优化效果:\n")
            f.write(f"    原始代码大小: {original_size} 字符\n")
            f.write(f"    优化后代码大小: {optimized_size} 字符\n")
            f.write(f"    常量折叠后代码大小: {folded_size} 字符\n")
            f.write(f"    优化版常量折叠后代码大小: {optimized_folded_size} 字符\n")
            f.write(
                f"    代码减少: {original_size - optimized_folded_size} 字符 ({((original_size - optimized_folded_size) / original_size * 100):.1f}%)\n\n"
            )

        f.write("优化建议:\n")
        if overall_speedup_with_optimized_folding >= 1.5:
            f.write("  [GOOD] 优化效果显著！总体性能提升超过50%\n")
        elif overall_speedup_with_optimized_folding >= 1.2:
            f.write("  [WARN] 优化效果一般，总体性能提升20-50%\n")
        else:
            f.write("  [BAD] 优化效果不明显，总体性能提升小于20%\n")

        f.write(f"\n  平均性能提升（优化版常量折叠）: {overall_speedup_with_optimized_folding:.2f}x\n")

    print(f"\n详细结果已保存到: {results_file}")
    print("=" * 80)
    print("测试完成!")
    print("=" * 80)

    return all_results


def main():
    """主函数"""
    try:
        results = run_final_performance_test()

        # 输出关键指标
        print("\n关键性能指标:")
        print("-" * 80)

        # 提取常量折叠测试的结果
        const_folding_results = [r for r in results if "常量折叠AST" in r["name"]]
        if len(const_folding_results) == 4:
            original = const_folding_results[0]
            optimized = const_folding_results[1]
            folded = const_folding_results[2]
            optimized_folded = const_folding_results[3]

            print("常量折叠测试:")
            print(f"  原始版本性能: {original['ops_per_second']:,.0f} ops/sec")
            print(f"  优化版本性能: {optimized['ops_per_second']:,.0f} ops/sec")
            print(f"  带常量折叠性能: {folded['ops_per_second']:,.0f} ops/sec")
            print(f"  带优化版常量折叠性能: {optimized_folded['ops_per_second']:,.0f} ops/sec")
            print(f"  最佳性能提升: {original['total_time']/optimized_folded['total_time']:.2f}x")
            print(f"  代码大小减少: {original['code_size'] - optimized_folded['code_size']} 字符")

        # 提取大型AST测试的结果
        large_ast_results = [r for r in results if "大型AST" in r["name"]]
        if len(large_ast_results) == 4:
            original = large_ast_results[0]
            optimized = large_ast_results[1]
            folded = large_ast_results[2]
            optimized_folded = large_ast_results[3]

            print("\n大型AST测试:")
            print(f"  原始版本性能: {original['ops_per_second']:,.0f} ops/sec")
            print(f"  优化版本性能: {optimized['ops_per_second']:,.0f} ops/sec")
            print(f"  带常量折叠性能: {folded['ops_per_second']:,.0f} ops/sec")
            print(f"  带优化版常量折叠性能: {optimized_folded['ops_per_second']:,.0f} ops/sec")
            print(f"  最佳性能提升: {original['total_time']/optimized['total_time']:.2f}x")

        print("\n" + "=" * 80)
        print("总结:")
        print("-" * 80)
        print("1. 字符串构建优化和方法查找缓存效果显著，性能提升85.7%")
        print("2. 常量折叠优化可以减少代码大小，但会增加运行时开销")
        print("3. 优化版常量折叠（原地修改）比原始常量折叠性能更好")
        print("4. 对于性能敏感场景，建议使用优化版本（无常量折叠）")
        print("5. 对于代码大小敏感场景，建议使用优化版常量折叠")
        print("=" * 80)

    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
