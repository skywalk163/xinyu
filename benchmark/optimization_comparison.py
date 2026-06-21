#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""优化效果对比测试 - 比较原始和优化版代码生成器的性能"""

import os
import sys
import time

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.codegen.python_codegen import PythonCodegen as OriginalCodegen
from src.codegen.python_codegen_optimized import OptimizedPythonCodegen as OptimizedCodegen
from src.parser.ast_nodes import (
    AssignNode,
    BinaryOpNode,
    ClassNode,
    FunctionCallNode,
    IdentifierNode,
    MemberAccessNode,
    MethodNode,
    NewNode,
    NumberNode,
    ProgramNode,
    PropertyNode,
    ReturnNode,
    StringNode,
    ThisNode,
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


def create_oop_ast():
    """创建包含OOP的AST用于测试"""
    statements = []

    # 类定义
    class_node = ClassNode(
        line=1,
        column=1,
        name="点",
        extends=None,
        implements=[],
        members=[
            PropertyNode(
                line=2,
                column=5,
                name="x",
                value=NumberNode(line=2, column=5, value=0),
                is_static=False,
            ),
            PropertyNode(
                line=3,
                column=5,
                name="y",
                value=NumberNode(line=3, column=5, value=0),
                is_static=False,
            ),
            MethodNode(
                line=4,
                column=5,
                name="初始化",
                params=["x", "y"],
                body=[
                    AssignNode(
                        line=5,
                        column=9,
                        target=MemberAccessNode(
                            line=5, column=9, obj=ThisNode(line=5, column=9), member="x"
                        ),
                        value=IdentifierNode(line=5, column=9, name="x"),
                    ),
                    AssignNode(
                        line=6,
                        column=9,
                        target=MemberAccessNode(
                            line=6, column=9, obj=ThisNode(line=6, column=9), member="y"
                        ),
                        value=IdentifierNode(line=6, column=9, name="y"),
                    ),
                ],
                is_static=False,
                is_constructor=True,
            ),
            MethodNode(
                line=7,
                column=5,
                name="距离",
                params=["其他点"],
                body=[
                    ReturnNode(
                        line=8,
                        column=9,
                        value=BinaryOpNode(
                            line=8,
                            column=9,
                            left=BinaryOpNode(
                                line=8,
                                column=9,
                                left=BinaryOpNode(
                                    line=8,
                                    column=9,
                                    left=MemberAccessNode(
                                        line=8, column=9, obj=ThisNode(line=8, column=9), member="x"
                                    ),
                                    operator="相减",
                                    right=MemberAccessNode(
                                        line=8,
                                        column=9,
                                        obj=IdentifierNode(line=8, column=9, name="其他点"),
                                        member="x",
                                    ),
                                ),
                                operator="相乘",
                                right=BinaryOpNode(
                                    line=8,
                                    column=9,
                                    left=MemberAccessNode(
                                        line=8, column=9, obj=ThisNode(line=8, column=9), member="x"
                                    ),
                                    operator="相减",
                                    right=MemberAccessNode(
                                        line=8,
                                        column=9,
                                        obj=IdentifierNode(line=8, column=9, name="其他点"),
                                        member="x",
                                    ),
                                ),
                            ),
                            operator="相加",
                            right=BinaryOpNode(
                                line=8,
                                column=9,
                                left=BinaryOpNode(
                                    line=8,
                                    column=9,
                                    left=MemberAccessNode(
                                        line=8, column=9, obj=ThisNode(line=8, column=9), member="y"
                                    ),
                                    operator="相减",
                                    right=MemberAccessNode(
                                        line=8,
                                        column=9,
                                        obj=IdentifierNode(line=8, column=9, name="其他点"),
                                        member="y",
                                    ),
                                ),
                                operator="相乘",
                                right=BinaryOpNode(
                                    line=8,
                                    column=9,
                                    left=MemberAccessNode(
                                        line=8, column=9, obj=ThisNode(line=8, column=9), member="y"
                                    ),
                                    operator="相减",
                                    right=MemberAccessNode(
                                        line=8,
                                        column=9,
                                        obj=IdentifierNode(line=8, column=9, name="其他点"),
                                        member="y",
                                    ),
                                ),
                            ),
                        ),
                    )
                ],
                is_static=False,
                is_constructor=False,
            ),
        ],
    )

    statements.append(class_node)

    # 创建对象并使用
    statements.append(
        AssignNode(
            line=10,
            column=1,
            target=IdentifierNode(line=10, column=1, name="点1"),
            value=NewNode(
                line=10,
                column=1,
                class_name="点",
                args=[
                    NumberNode(line=10, column=1, value=0),
                    NumberNode(line=10, column=1, value=0),
                ],
            ),
        )
    )

    statements.append(
        AssignNode(
            line=11,
            column=1,
            target=IdentifierNode(line=11, column=1, name="点2"),
            value=NewNode(
                line=11,
                column=1,
                class_name="点",
                args=[
                    NumberNode(line=11, column=1, value=3),
                    NumberNode(line=11, column=1, value=4),
                ],
            ),
        )
    )

    statements.append(
        FunctionCallNode(
            line=12,
            column=1,
            name=IdentifierNode(line=12, column=1, name="打印"),
            args=[
                BinaryOpNode(
                    line=12,
                    column=1,
                    left=StringNode(line=12, column=1, value="两点距离："),
                    operator="相加",
                    right=FunctionCallNode(
                        line=12,
                        column=1,
                        name=MemberAccessNode(
                            line=12,
                            column=1,
                            obj=IdentifierNode(line=12, column=1, name="点1"),
                            member="距离",
                        ),
                        args=[IdentifierNode(line=12, column=1, name="点2")],
                    ),
                )
            ],
        )
    )

    return ProgramNode(line=1, column=1, statements=statements)


def benchmark_codegen(codegen, ast, iterations=1000, name="测试"):
    """基准测试代码生成性能"""

    # 预热
    for _ in range(10):
        codegen.generate(ast)

    # 测试
    start_time = time.perf_counter()
    for i in range(iterations):
        result = codegen.generate(ast)
    end_time = time.perf_counter()

    total_time = end_time - start_time
    avg_time = total_time / iterations
    ops_per_second = iterations / total_time

    return {
        "name": name,
        "total_time": total_time,
        "avg_time": avg_time,
        "ops_per_second": ops_per_second,
        "code_size": len(result),
        "node_count": len(ast.statements),
    }


def run_comparison():
    """运行性能对比测试"""
    print("=" * 70)
    print("心语编程语言代码生成器性能对比测试")
    print("=" * 70)
    print()

    # 创建测试AST
    print("创建测试AST...")
    simple_ast = create_simple_ast()
    oop_ast = create_oop_ast()

    print(f"简单AST节点数: {len(simple_ast.statements)}")
    print(f"OOP AST节点数: {len(oop_ast.statements)}")
    print()

    # 创建代码生成器实例
    original_codegen = OriginalCodegen()
    optimized_codegen = OptimizedCodegen()

    # 测试配置
    test_cases = [
        ("简单AST", simple_ast, 5000),
        ("OOP AST", oop_ast, 2000),
    ]

    results = []

    # 运行测试
    for test_name, ast, iterations in test_cases:
        print(f"测试: {test_name} (迭代次数: {iterations})")
        print("-" * 50)

        # 测试原始版本
        print("  原始版本...")
        original_result = benchmark_codegen(original_codegen, ast, iterations, "原始版本")
        results.append(original_result)

        print(f"    总时间: {original_result['total_time']:.4f} 秒")
        print(f"    平均时间: {original_result['avg_time']*1e6:.2f} 微秒/次")
        print(f"    操作数/秒: {original_result['ops_per_second']:,.0f}")

        # 测试优化版本
        print("  优化版本...")
        optimized_result = benchmark_codegen(optimized_codegen, ast, iterations, "优化版本")
        results.append(optimized_result)

        print(f"    总时间: {optimized_result['total_time']:.4f} 秒")
        print(f"    平均时间: {optimized_result['avg_time']*1e6:.2f} 微秒/次")
        print(f"    操作数/秒: {optimized_result['ops_per_second']:,.0f}")

        # 计算性能提升
        speedup = original_result["total_time"] / optimized_result["total_time"]
        improvement = (speedup - 1) * 100

        print(f"  性能提升: {speedup:.2f}x ({improvement:+.1f}%)")
        print()

    # 输出总结
    print("=" * 70)
    print("性能对比总结")
    print("=" * 70)
    print()

    print("测试结果:")
    print("-" * 70)
    print(f"{'测试用例':<15} {'版本':<10} {'总时间(秒)':<12} {'平均时间(微秒)':<15} {'操作数/秒':<15} {'性能提升':<10}")
    print("-" * 70)

    for i in range(0, len(results), 2):
        original = results[i]
        optimized = results[i + 1]

        speedup = original["total_time"] / optimized["total_time"]
        improvement = (speedup - 1) * 100

        print(
            f"{original['name']:<15} {'原始':<10} {original['total_time']:<12.4f} "
            f"{original['avg_time']*1e6:<15.2f} {original['ops_per_second']:<15,.0f} {'-':<10}"
        )
        print(
            f"{'':<15} {'优化':<10} {optimized['total_time']:<12.4f} "
            f"{optimized['avg_time']*1e6:<15.2f} {optimized['ops_per_second']:<15,.0f} "
            f"{f'{speedup:.2f}x ({improvement:+.1f}%)':<10}"
        )
        print()

    # 计算总体性能提升
    total_original_time = sum(r["total_time"] for r in results if r["name"] == "原始版本")
    total_optimized_time = sum(r["total_time"] for r in results if r["name"] == "优化版本")
    overall_speedup = total_original_time / total_optimized_time
    overall_improvement = (overall_speedup - 1) * 100

    print(f"总体性能提升: {overall_speedup:.2f}x ({overall_improvement:+.1f}%)")
    print()

    # 分析优化效果
    print("优化效果分析:")
    print("-" * 70)

    optimizations = [
        ("字符串构建优化", "使用列表+join()代替字符串拼接", "20-30%"),
        ("方法查找缓存", "缓存getattr()结果", "15-25%"),
        ("局部变量缓存", "缓存字典引用到局部变量", "5-10%"),
        ("减少临时对象", "重用字符串缓冲区", "5-10%"),
    ]

    for name, description, expected in optimizations:
        print(f"  {name}:")
        print(f"    描述: {description}")
        print(f"    预期提升: {expected}")

    print()

    # 内存使用对比（简单估算）
    print("内存使用对比（估算）:")
    print("-" * 70)

    # 生成代码并估算内存使用
    simple_code_original = original_codegen.generate(simple_ast)
    simple_code_optimized = optimized_codegen.generate(simple_ast)

    oop_code_original = original_codegen.generate(oop_ast)
    oop_code_optimized = optimized_codegen.generate(oop_ast)

    print("简单AST代码大小:")
    print(f"  原始版本: {len(simple_code_original)} 字符")
    print(f"  优化版本: {len(simple_code_optimized)} 字符")
    print(f"  差异: {len(simple_code_optimized) - len(simple_code_original):+d} 字符")
    print()

    print("OOP AST代码大小:")
    print(f"  原始版本: {len(oop_code_original)} 字符")
    print(f"  优化版本: {len(oop_code_optimized)} 字符")
    print(f"  差异: {len(oop_code_optimized) - len(oop_code_original):+d} 字符")
    print()

    # 验证代码正确性
    print("代码正确性验证:")
    print("-" * 70)

    # 检查生成的代码是否相同
    if simple_code_original == simple_code_optimized:
        print("  [OK] 简单AST: 原始版本和优化版本生成的代码相同")
    else:
        print("  [DIFF] 简单AST: 原始版本和优化版本生成的代码不同")
        print(f"    原始版本:\n{simple_code_original[:100]}...")
        print(f"    优化版本:\n{simple_code_optimized[:100]}...")

    if oop_code_original == oop_code_optimized:
        print("  [OK] OOP AST: 原始版本和优化版本生成的代码相同")
    else:
        print("  [DIFF] OOP AST: 原始版本和优化版本生成的代码不同")
        print(f"    原始版本:\n{oop_code_original[:100]}...")
        print(f"    优化版本:\n{oop_code_optimized[:100]}...")

    print()
    print("=" * 70)
    print("测试完成!")
    print("=" * 70)

    # 保存结果
    output_dir = "benchmark/results"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    results_file = os.path.join(output_dir, f"optimization_comparison_{timestamp}.txt")

    with open(results_file, "w", encoding="utf-8") as f:
        f.write("心语编程语言代码生成器性能对比测试结果\n")
        f.write("=" * 70 + "\n\n")

        f.write("测试配置:\n")
        f.write(f"  简单AST节点数: {len(simple_ast.statements)}\n")
        f.write(f"  OOP AST节点数: {len(oop_ast.statements)}\n\n")

        f.write("性能结果:\n")
        f.write("-" * 70 + "\n")
        f.write(
            f"{'测试用例':<15} {'版本':<10} {'总时间(秒)':<12} {'平均时间(微秒)':<15} {'操作数/秒':<15} {'性能提升':<10}\n"
        )
        f.write("-" * 70 + "\n")

        for i in range(0, len(results), 2):
            original = results[i]
            optimized = results[i + 1]

            speedup = original["total_time"] / optimized["total_time"]
            improvement = (speedup - 1) * 100

            f.write(
                f"{original['name']:<15} {'原始':<10} {original['total_time']:<12.4f} "
                f"{original['avg_time'] * 1e6:<15.2f} {original['ops_per_second']:<15,.0f} {'-':<10}\n"
            )
            f.write(
                f"{'':<15} {'优化':<10} {optimized['total_time']:<12.4f} "
                f"{optimized['avg_time'] * 1e6:<15.2f} {optimized['ops_per_second']:<15,.0f} "
                f"{f'{speedup:.2f}x ({improvement:+.1f}%)':<10}\n\n"
            )

        f.write(f"总体性能提升: {overall_speedup:.2f}x ({overall_improvement:+.1f}%)\n\n")

        f.write("优化效果分析:\n")
        for name, description, expected in optimizations:
            f.write(f"  {name}: {description} (预期提升: {expected})\n")

        f.write("\n代码正确性验证:\n")
        f.write(f"  简单AST代码相同: {simple_code_original == simple_code_optimized}\n")
        f.write(f"  OOP AST代码相同: {oop_code_original == oop_code_optimized}\n")

        f.write("\n生成的代码示例:\n")
        f.write("简单AST（原始版本）:\n")
        f.write(simple_code_original + "\n\n")
        f.write("简单AST（优化版本）:\n")
        f.write(simple_code_optimized + "\n\n")
        f.write("OOP AST（原始版本）:\n")
        f.write(oop_code_original[:500] + "...\n\n")
        f.write("OOP AST（优化版本）:\n")
        f.write(oop_code_optimized[:500] + "...\n")

    print(f"\n详细结果已保存到: {results_file}")

    return results


def main():
    """主函数"""
    try:
        results = run_comparison()

        # 输出建议
        print("\n优化建议:")
        print("-" * 70)

        # 分析结果并给出建议
        overall_speedup = 0
        test_count = 0

        for i in range(0, len(results), 2):
            original = results[i]
            optimized = results[i + 1]
            speedup = original["total_time"] / optimized["total_time"]
            overall_speedup += speedup
            test_count += 1

        if test_count > 0:
            avg_speedup = overall_speedup / test_count

            if avg_speedup >= 1.5:
                print("  [GOOD] 优化效果显著！性能提升超过50%")
                print("     建议：继续实施其他优化方案")
            elif avg_speedup >= 1.2:
                print("  [WARN] 优化效果一般，性能提升20-50%")
                print("     建议：进一步优化字符串构建和方法查找")
            else:
                print("  [BAD] 优化效果不明显，性能提升小于20%")
                print("     建议：重新分析性能瓶颈，调整优化策略")

            print(f"\n  平均性能提升: {avg_speedup:.2f}x")

            # 具体建议
            if avg_speedup < 1.3:
                print("\n  具体优化建议:")
                print("  1. 进一步优化字符串构建，使用更高效的数据结构")
                print("  2. 实现方法分派表，避免动态查找")
                print("  3. 添加常量折叠优化")
                print("  4. 实现死代码消除")

    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
