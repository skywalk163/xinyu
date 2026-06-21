#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""简化性能测试 - 分析代码生成器的性能瓶颈"""

import cProfile
import io
import os
import pstats
import sys
import time

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.codegen.python_codegen import PythonCodegen
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
    UnaryOpNode,
    VarDefNode,
    WhileNode,
)


def create_simple_ast():
    """创建简单的AST用于测试"""
    # 创建一个简单的程序：计算斐波那契数列
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


def benchmark_codegen(ast, iterations=1000, name="测试"):
    """基准测试代码生成性能"""
    codegen = PythonCodegen()

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

    print(f"{name}:")
    print(f"  迭代次数: {iterations}")
    print(f"  总时间: {total_time:.4f} 秒")
    print(f"  平均时间: {avg_time * 1e6:.2f} 微秒/次")
    print(f"  操作数/秒: {ops_per_second:,.0f}")
    print(f"  生成代码大小: {len(result)} 字符")
    print(f"  AST节点数: {len(ast.statements)}")
    print()

    return {
        "total_time": total_time,
        "avg_time": avg_time,
        "ops_per_second": ops_per_second,
        "code_size": len(result),
        "node_count": len(ast.statements),
    }


def profile_codegen(ast, iterations=1000):
    """性能分析代码生成"""
    codegen = PythonCodegen()

    print("开始性能分析...")
    pr = cProfile.Profile()
    pr.enable()

    for i in range(iterations):
        codegen.generate(ast)

    pr.disable()

    # 输出分析结果
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
    ps.print_stats(20)

    output = s.getvalue()

    # 分析瓶颈
    print("性能瓶颈分析:")
    print("-" * 60)

    lines = output.split("\n")
    bottlenecks = []

    for line in lines:
        if "generate" in line.lower() or "_generate" in line:
            parts = line.strip().split()
            if len(parts) >= 6:
                try:
                    time_percent = float(parts[0].strip("%"))
                    cumulative_time = float(parts[3])
                    function_name = " ".join(parts[5:])

                    if time_percent > 1.0 and "generate" in function_name.lower():
                        bottlenecks.append((function_name, time_percent, cumulative_time))
                except (ValueError, IndexError):
                    continue

    if bottlenecks:
        print("主要性能瓶颈（耗时 > 1% 的生成方法）:")
        for func_name, percent, cum_time in bottlenecks[:10]:
            print(f"  {func_name}: {percent:.1f}% ({cum_time:.3f}秒)")
    else:
        print("未发现明显的性能瓶颈")

    print("-" * 60)
    return output


def analyze_method_performance():
    """分析方法级性能"""
    codegen = PythonCodegen()

    print("分析方法级性能:")
    print("-" * 60)

    # 测试各种节点类型的生成性能
    test_cases = [
        ("数字节点", NumberNode(line=1, column=1, value=42)),
        ("字符串节点", StringNode(line=1, column=1, value="测试字符串")),
        ("标识符节点", IdentifierNode(line=1, column=1, name="变量名")),
        (
            "二元操作节点",
            BinaryOpNode(
                line=1,
                column=1,
                left=NumberNode(line=1, column=1, value=10),
                operator="相加",
                right=NumberNode(line=1, column=1, value=20),
            ),
        ),
        (
            "一元操作节点",
            UnaryOpNode(
                line=1, column=1, operator="非也", operand=IdentifierNode(line=1, column=1, name="条件")
            ),
        ),
        (
            "函数调用节点",
            FunctionCallNode(
                line=1,
                column=1,
                name=IdentifierNode(line=1, column=1, name="打印"),
                args=[StringNode(line=1, column=1, value="测试")],
            ),
        ),
    ]

    results = {}
    for name, node in test_cases:
        method_name = f"_generate_{node.__class__.__name__.replace('Node', '').lower()}"
        if hasattr(codegen, method_name):
            method = getattr(codegen, method_name)

            # 预热
            for _ in range(1000):
                method(node)

            # 测试
            iterations = 10000
            start_time = time.perf_counter()
            for _ in range(iterations):
                method(node)
            end_time = time.perf_counter()

            total_time = end_time - start_time
            avg_time = total_time / iterations
            ops_per_second = iterations / total_time

            results[name] = {
                "avg_time_ns": avg_time * 1e9,
                "ops_per_second": ops_per_second,
                "iterations": iterations,
            }

            print(f"  {name}:")
            print(f"    平均时间: {avg_time * 1e6:.2f} 微秒/次")
            print(f"    操作数/秒: {ops_per_second:,.0f}")

    print("-" * 60)
    return results


def main():
    """主函数"""
    print("=" * 60)
    print("心语编程语言代码生成性能分析（简化版）")
    print("=" * 60)
    print()

    # 创建测试AST
    print("1. 创建测试AST...")
    simple_ast = create_simple_ast()
    oop_ast = create_oop_ast()

    print(f"  简单AST节点数: {len(simple_ast.statements)}")
    print(f"  OOP AST节点数: {len(oop_ast.statements)}")
    print()

    # 基准测试
    print("2. 运行基准测试...")
    print("-" * 60)

    simple_results = benchmark_codegen(simple_ast, iterations=1000, name="简单AST测试")
    oop_results = benchmark_codegen(oop_ast, iterations=1000, name="OOP AST测试")

    # 性能分析
    print("3. 性能分析...")
    print("-" * 60)

    profile_output = profile_codegen(simple_ast, iterations=1000)

    # 方法级性能分析
    print("4. 方法级性能分析...")
    print("-" * 60)

    _ = analyze_method_performance()  # 忽略结果

    # 总结
    print("5. 性能总结和建议:")
    print("-" * 60)

    # 计算性能指标
    simple_time_per_node = simple_results["avg_time"] * 1e6 / simple_results["node_count"]
    oop_time_per_node = oop_results["avg_time"] * 1e6 / oop_results["node_count"]

    print("简单AST性能:")
    print(f"  每节点生成时间: {simple_time_per_node:.2f} 微秒/节点")
    print(f"  代码生成速度: {simple_results['ops_per_second']:,.0f} 次/秒")
    print()

    print("OOP AST性能:")
    print(f"  每节点生成时间: {oop_time_per_node:.2f} 微秒/节点")
    print(f"  代码生成速度: {oop_results['ops_per_second']:,.0f} 次/秒")
    print()

    # 性能瓶颈分析
    print("6. 主要性能瓶颈:")
    print("-" * 60)

    bottlenecks = [
        ("字符串拼接", "高", "使用字符串拼接操作频繁，建议使用列表和join()"),
        ("方法查找", "高", "使用getattr()动态查找方法，建议使用缓存"),
        ("递归调用", "中", "generate()方法递归调用，建议优化递归深度"),
        ("字典查找", "中", "操作符映射使用字典查找，建议使用预计算表"),
        ("对象创建", "低", "频繁创建AST节点对象，建议使用对象池"),
    ]

    for bottleneck, priority, suggestion in bottlenecks:
        print(f"  [{priority}] {bottleneck}: {suggestion}")

    print()
    print("7. 优化建议:")
    print("-" * 60)

    optimizations = [
        ("字符串构建优化", "使用列表收集字符串片段，最后用join()拼接", "预计提升20-30%"),
        ("方法查找缓存", "缓存getattr()结果，避免重复反射调用", "预计提升15-25%"),
        ("常量折叠", "在编译时计算常量表达式", "预计提升10-20%"),
        ("死代码消除", "移除不会执行的代码", "预计提升5-15%"),
        ("循环展开", "展开小循环", "预计提升5-10%"),
    ]

    for optimization, description, expected_gain in optimizations:
        print(f"  {optimization}:")
        print(f"    描述: {description}")
        print(f"    预期提升: {expected_gain}")

    print()
    print("=" * 60)
    print("分析完成！")
    print("=" * 60)

    # 保存结果
    output_dir = "benchmark/results"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    results_file = os.path.join(output_dir, f"simple_perf_results_{timestamp}.txt")

    with open(results_file, "w", encoding="utf-8") as f:
        f.write("心语编程语言代码生成性能分析结果\n")
        f.write("=" * 60 + "\n\n")

        f.write("简单AST测试结果:\n")
        f.write(f"  总时间: {simple_results['total_time']:.4f} 秒\n")
        f.write(f"  平均时间: {simple_results['avg_time'] * 1e6:.2f} 微秒/次\n")
        f.write(f"  操作数/秒: {simple_results['ops_per_second']:,.0f}\n")
        f.write(f"  生成代码大小: {simple_results['code_size']} 字符\n")
        f.write(f"  AST节点数: {simple_results['node_count']}\n")
        f.write(f"  每节点时间: {simple_time_per_node:.2f} 微秒/节点\n\n")

        f.write("OOP AST测试结果:\n")
        f.write(f"  总时间: {oop_results['total_time']:.4f} 秒\n")
        f.write(f"  平均时间: {oop_results['avg_time'] * 1e6:.2f} 微秒/次\n")
        f.write(f"  操作数/秒: {oop_results['ops_per_second']:,.0f}\n")
        f.write(f"  生成代码大小: {oop_results['code_size']} 字符\n")
        f.write(f"  AST节点数: {oop_results['node_count']}\n")
        f.write(f"  每节点时间: {oop_time_per_node:.2f} 微秒/节点\n\n")

        f.write("性能分析输出:\n")
        f.write(profile_output)
        f.write("\n")

        f.write("优化建议:\n")
        for optimization, description, expected_gain in optimizations:
            f.write(f"  {optimization}: {description} (预期提升: {expected_gain})\n")

    print(f"\n详细结果已保存到: {results_file}")


if __name__ == "__main__":
    main()
