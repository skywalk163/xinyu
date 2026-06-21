#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""性能分析工具 - 分析心语编程语言的代码生成性能"""

import cProfile
import io
import os
import pstats
import sys
import time
from typing import Any, Dict, List, Tuple

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.codegen.python_codegen import PythonCodegen
from src.parser.ast_nodes import (
    AssignNode,
    BinaryOpNode,
    BlockNode,
    ClassNode,
    FunctionCallNode,
    IdentifierNode,
    IfNode,
    MethodNode,
    NewNode,
    NumberNode,
    ProgramNode,
    PropertyNode,
    ReturnNode,
    StringNode,
    UnaryOpNode,
    VarDefNode,
    WhileNode,
)


class PerformanceAnalyzer:
    """性能分析器"""

    def __init__(self):
        self.codegen = PythonCodegen()
        self.results = {}

    def create_test_ast(self, complexity: int = 100) -> ProgramNode:
        """创建测试用的AST

        Args:
            complexity: 复杂度级别，控制AST的大小

        Returns:
            测试用的AST程序节点
        """
        statements = []

        # 添加变量定义
        for i in range(complexity // 10):
            statements.append(
                VarDefNode(
                    line=1, column=1, name=f"变量{i}", value=NumberNode(line=1, column=1, value=i)
                )
            )

        # 添加赋值语句
        for i in range(complexity // 10):
            statements.append(
                AssignNode(
                    line=2,
                    column=1,
                    target=IdentifierNode(line=2, column=1, name=f"变量{i}"),
                    value=BinaryOpNode(
                        line=2,
                        column=1,
                        left=IdentifierNode(line=2, column=1, name=f"变量{i}"),
                        operator="相加",
                        right=NumberNode(line=2, column=1, value=1),
                    ),
                )
            )

        # 添加if语句
        if complexity > 20:
            condition = BinaryOpNode(
                line=3,
                column=1,
                left=IdentifierNode(line=3, column=1, name="变量0"),
                operator="大于",
                right=NumberNode(line=3, column=1, value=5),
            )
            then_block = BlockNode(
                line=3,
                column=1,
                statements=[
                    AssignNode(
                        line=4,
                        column=1,
                        target=IdentifierNode(line=4, column=1, name="结果"),
                        value=StringNode(line=4, column=1, value="条件成立"),
                    )
                ],
            )
            else_block = BlockNode(
                line=5,
                column=1,
                statements=[
                    AssignNode(
                        line=6,
                        column=1,
                        target=IdentifierNode(line=6, column=1, name="结果"),
                        value=StringNode(line=6, column=1, value="条件不成立"),
                    )
                ],
            )
            statements.append(
                IfNode(
                    line=3,
                    column=1,
                    condition=condition,
                    then_branch=then_block.statements,
                    else_branch=else_block.statements,
                )
            )

        # 添加while循环
        if complexity > 30:
            condition = BinaryOpNode(
                line=7,
                column=1,
                left=IdentifierNode(line=7, column=1, name="计数器"),
                operator="小于",
                right=NumberNode(line=7, column=1, value=10),
            )
            loop_body = BlockNode(
                line=7,
                column=1,
                statements=[
                    AssignNode(
                        line=8,
                        column=1,
                        target=IdentifierNode(line=8, column=1, name="计数器"),
                        value=BinaryOpNode(
                            line=8,
                            column=1,
                            left=IdentifierNode(line=8, column=1, name="计数器"),
                            operator="相加",
                            right=NumberNode(line=8, column=1, value=1),
                        ),
                    )
                ],
            )
            statements.append(WhileNode(line=7, column=1, condition=condition, body=loop_body))

        # 添加函数调用
        for i in range(complexity // 20):
            statements.append(
                FunctionCallNode(
                    line=9,
                    column=1,
                    name=IdentifierNode(line=9, column=1, name="打印"),
                    args=[StringNode(line=9, column=1, value=f"迭代 {i}")],
                )
            )

        # 添加OOP相关节点（如果复杂度足够高）
        if complexity > 50:
            # 添加类定义
            class_node = ClassNode(
                line=10,
                column=1,
                name="测试类",
                extends=None,
                implements=[],
                members=[
                    PropertyNode(
                        line=11,
                        column=5,
                        name="属性1",
                        value=NumberNode(line=11, column=5, value=42),
                        is_static=False,
                    ),
                    PropertyNode(
                        line=12,
                        column=5,
                        name="属性2",
                        value=StringNode(line=12, column=5, value="测试"),
                        is_static=False,
                    ),
                    MethodNode(
                        line=13,
                        column=5,
                        name="方法1",
                        params=["参数1", "参数2"],
                        body=[
                            ReturnNode(
                                line=14,
                                column=9,
                                value=BinaryOpNode(
                                    line=14,
                                    column=9,
                                    left=IdentifierNode(line=14, column=9, name="参数1"),
                                    operator="相加",
                                    right=IdentifierNode(line=14, column=9, name="参数2"),
                                ),
                            )
                        ],
                        is_static=False,
                        is_constructor=False,
                    ),
                ],
            )
            statements.append(class_node)

            # 添加对象创建
            statements.append(
                AssignNode(
                    line=15,
                    column=1,
                    target=IdentifierNode(line=15, column=1, name="对象"),
                    value=NewNode(line=15, column=1, class_name="测试类", args=[]),
                )
            )

        return ProgramNode(line=1, column=1, statements=statements)

    def benchmark_generate(self, ast: ProgramNode, iterations: int = 1000) -> Dict[str, Any]:
        """基准测试代码生成性能

        Args:
            ast: 要测试的AST
            iterations: 迭代次数

        Returns:
            性能指标字典
        """
        print(f"开始基准测试，迭代次数: {iterations}")
        print(f"AST节点数: {len(ast.statements)}")

        # 预热
        for _ in range(10):
            self.codegen.generate(ast)

        # 性能测试
        start_time = time.perf_counter()
        for i in range(iterations):
            _ = self.codegen.generate(ast)  # 忽略结果
        end_time = time.perf_counter()

        total_time = end_time - start_time
        avg_time = total_time / iterations
        ops_per_second = iterations / total_time

        # 计算生成的代码大小
        code = self.codegen.generate(ast)
        code_size = len(code)

        return {
            "iterations": iterations,
            "total_time": total_time,
            "avg_time_per_iteration": avg_time,
            "operations_per_second": ops_per_second,
            "generated_code_size": code_size,
            "ast_node_count": len(ast.statements),
        }

    def memory_profile_generate(self, ast: ProgramNode, iterations: int = 100):
        """内存性能分析（简化版）

        Args:
            ast: 要测试的AST
            iterations: 迭代次数
        """
        print(f"内存性能分析，迭代次数: {iterations}")

        import gc
        import tracemalloc

        # 开始内存跟踪
        tracemalloc.start()

        # 记录初始内存
        snapshot1 = tracemalloc.take_snapshot()

        results = []
        for i in range(iterations):
            result = self.codegen.generate(ast)
            results.append(result)

        # 记录结束内存
        snapshot2 = tracemalloc.take_snapshot()

        # 计算内存差异
        top_stats = snapshot2.compare_to(snapshot1, "lineno")

        print("内存使用变化（前10个最大分配）:")
        for stat in top_stats[:10]:
            print(f"  {stat}")

        # 停止内存跟踪
        tracemalloc.stop()

        # 强制垃圾回收
        gc.collect()

        return results

    def profile_generate(self, ast: ProgramNode, iterations: int = 1000):
        """CPU性能分析

        Args:
            ast: 要测试的AST
            iterations: 迭代次数
        """
        print(f"CPU性能分析，迭代次数: {iterations}")

        # 设置性能分析
        pr = cProfile.Profile()
        pr.enable()

        for i in range(iterations):
            self.codegen.generate(ast)

        pr.disable()

        # 输出分析结果
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
        ps.print_stats(20)  # 显示前20个最耗时的函数

        return s.getvalue()

    def analyze_codegen_methods(self):
        """分析代码生成器方法的性能特征"""
        print("分析代码生成器方法...")

        methods = [
            ("_generate_number", NumberNode(line=1, column=1, value=42)),
            ("_generate_string", StringNode(line=1, column=1, value="测试字符串")),
            ("_generate_identifier", IdentifierNode(line=1, column=1, name="变量名")),
            (
                "_generate_binaryop",
                BinaryOpNode(
                    line=1,
                    column=1,
                    left=NumberNode(line=1, column=1, value=10),
                    operator="相加",
                    right=NumberNode(line=1, column=1, value=20),
                ),
            ),
            (
                "_generate_unaryop",
                UnaryOpNode(
                    line=1,
                    column=1,
                    operator="非也",
                    operand=IdentifierNode(line=1, column=1, name="条件"),
                ),
            ),
        ]

        results = {}
        for method_name, node in methods:
            if hasattr(self.codegen, method_name):
                method = getattr(self.codegen, method_name)

                # 预热
                for _ in range(100):
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

                results[method_name] = {
                    "avg_time_ns": avg_time * 1e9,  # 转换为纳秒
                    "ops_per_second": ops_per_second,
                    "iterations": iterations,
                }

                print(f"  {method_name}: {avg_time * 1e6:.2f} 微秒/次, {ops_per_second:,.0f} 次/秒")

        return results

    def run_comprehensive_benchmark(self):
        """运行全面的性能基准测试"""
        print("=" * 60)
        print("心语编程语言代码生成性能分析")
        print("=" * 60)

        results = {}

        # 测试不同复杂度的AST
        complexities = [10, 50, 100, 200, 500]
        for complexity in complexities:
            print(f"\n测试复杂度: {complexity}")
            print("-" * 40)

            ast = self.create_test_ast(complexity)
            benchmark_result = self.benchmark_generate(ast, iterations=100)
            results[f"complexity_{complexity}"] = benchmark_result

            print(f"  总时间: {benchmark_result['total_time']:.4f} 秒")
            print(f"  平均时间: {benchmark_result['avg_time_per_iteration'] * 1e6:.2f} 微秒/次")
            print(f"  操作数/秒: {benchmark_result['operations_per_second']:,.0f}")
            print(f"  生成代码大小: {benchmark_result['generated_code_size']} 字符")
            print(f"  AST节点数: {benchmark_result['ast_node_count']}")

        # 分析方法性能
        print("\n分析方法性能...")
        print("-" * 40)
        method_results = self.analyze_codegen_methods()
        results["method_analysis"] = method_results

        # 运行CPU性能分析
        print("\n运行CPU性能分析...")
        print("-" * 40)
        ast = self.create_test_ast(100)
        profile_output = self.profile_generate(ast, iterations=1000)

        # 保存结果
        self.save_results(results, profile_output)

        return results

    def save_results(self, results: Dict, profile_output: str):
        """保存性能分析结果"""
        output_dir = "benchmark/results"
        os.makedirs(output_dir, exist_ok=True)

        timestamp = time.strftime("%Y%m%d_%H%M%S")

        # 保存基准测试结果
        results_file = os.path.join(output_dir, f"benchmark_results_{timestamp}.txt")
        with open(results_file, "w", encoding="utf-8") as f:
            f.write("心语编程语言代码生成性能基准测试结果\n")
            f.write("=" * 60 + "\n\n")

            for key, result in results.items():
                if key.startswith("complexity_"):
                    f.write(f"复杂度: {key.split('_')[1]}\n")
                    f.write(f"  迭代次数: {result['iterations']}\n")
                    f.write(f"  总时间: {result['total_time']:.4f} 秒\n")
                    f.write(f"  平均时间: {result['avg_time_per_iteration'] * 1e6:.2f} 微秒/次\n")
                    f.write(f"  操作数/秒: {result['operations_per_second']:,.0f}\n")
                    f.write(f"  生成代码大小: {result['generated_code_size']} 字符\n")
                    f.write(f"  AST节点数: {result['ast_node_count']}\n\n")
                elif key == "method_analysis":
                    f.write("方法性能分析:\n")
                    for method_name, method_result in result.items():
                        f.write(f"  {method_name}:\n")
                        f.write(f"    平均时间: {method_result['avg_time_ns']:.2f} ns\n")
                        f.write(f"    操作数/秒: {method_result['ops_per_second']:,.0f}\n")
                        f.write(f"    迭代次数: {method_result['iterations']}\n")
                    f.write("\n")

        # 保存性能分析输出
        profile_file = os.path.join(output_dir, f"profile_output_{timestamp}.txt")
        with open(profile_file, "w", encoding="utf-8") as f:
            f.write("CPU性能分析结果\n")
            f.write("=" * 60 + "\n\n")
            f.write(profile_output)

        print("\n结果已保存到:")
        print(f"  基准测试结果: {results_file}")
        print(f"  性能分析结果: {profile_file}")

    def identify_bottlenecks(self, profile_output: str) -> List[Tuple[str, float]]:
        """识别性能瓶颈

        Args:
            profile_output: 性能分析输出

        Returns:
            瓶颈列表（函数名，耗时百分比）
        """
        bottlenecks = []
        lines = profile_output.split("\n")

        for line in lines:
            if "generate" in line.lower() or "_generate" in line:
                # 解析性能分析行
                parts = line.strip().split()
                if len(parts) >= 6:
                    try:
                        time_percent = float(parts[0].strip("%"))
                        cumulative_time = float(parts[3])
                        function_name = " ".join(parts[5:])

                        if time_percent > 1.0:  # 只关注耗时超过1%的函数
                            bottlenecks.append((function_name, time_percent, cumulative_time))
                    except (ValueError, IndexError):
                        continue

        # 按耗时百分比排序
        bottlenecks.sort(key=lambda x: x[1], reverse=True)
        return bottlenecks

    def generate_optimization_report(self, results: Dict, bottlenecks: List[Tuple[str, float]]):
        """生成优化报告

        Args:
            results: 基准测试结果
            bottlenecks: 性能瓶颈列表
        """
        print("\n" + "=" * 60)
        print("性能优化建议报告")
        print("=" * 60)

        # 分析基准测试结果
        print("\n1. 基准测试分析:")
        print("-" * 40)

        complexities = [10, 50, 100, 200, 500]
        for complexity in complexities:
            key = f"complexity_{complexity}"
            if key in results:
                result = results[key]
                print(f"  复杂度 {complexity}:")
                print(f"    AST节点数: {result['ast_node_count']}")
                print(f"    平均生成时间: {result['avg_time_per_iteration'] * 1e6:.2f} 微秒")
                print(
                    f"    每节点时间: {result['avg_time_per_iteration'] * 1e6 / result['ast_node_count']:.2f} "
                    "微秒/节点"
                )

        # 分析瓶颈
        print("\n2. 性能瓶颈分析:")
        print("-" * 40)
        if bottlenecks:
            print("  主要性能瓶颈:")
            for func_name, percent, cum_time in bottlenecks[:10]:  # 显示前10个瓶颈
                print(f"    {func_name}: {percent:.1f}% ({cum_time:.3f}秒)")
        else:
            print("  未发现明显的性能瓶颈")

        # 生成优化建议
        print("\n3. 优化建议:")
        print("-" * 40)

        optimization_suggestions = [
            ("字符串构建优化", "使用列表和join()代替字符串拼接", "高", "减少内存分配和复制"),
            ("方法查找缓存", "缓存getattr()结果，避免重复查找", "高", "减少反射调用开销"),
            ("常量折叠", "在编译时计算常量表达式", "中", "减少运行时计算"),
            ("死代码消除", "移除不会执行的代码", "中", "减少生成的代码量"),
            ("循环展开", "展开小循环", "低", "减少循环开销"),
            ("内联小函数", "内联简单的方法调用", "中", "减少函数调用开销"),
            ("使用生成器", "使用生成器表达式代替列表", "中", "减少内存使用"),
            ("预计算映射表", "预计算操作符映射表", "低", "减少字典查找"),
        ]

        for suggestion, description, priority, benefit in optimization_suggestions:
            print(f"  [{priority}] {suggestion}:")
            print(f"     描述: {description}")
            print(f"     收益: {benefit}")

        # 具体实施建议
        print("\n4. 实施计划:")
        print("-" * 40)
        print("  第一阶段（高优先级）:")
        print("    1. 实现字符串构建优化")
        print("    2. 实现方法查找缓存")
        print("    3. 添加性能监控")
        print()
        print("  第二阶段（中优先级）:")
        print("    1. 实现常量折叠")
        print("    2. 实现死代码消除")
        print("    3. 实现内联优化")
        print()
        print("  第三阶段（低优先级）:")
        print("    1. 实现循环展开")
        print("    2. 优化映射表查找")
        print("    3. 添加JIT编译支持")


def main():
    """主函数"""
    analyzer = PerformanceAnalyzer()

    print("开始性能分析...")

    # 运行全面的基准测试
    results = analyzer.run_comprehensive_benchmark()

    # 运行CPU性能分析并识别瓶颈
    ast = analyzer.create_test_ast(100)
    profile_output = analyzer.profile_generate(ast, iterations=1000)
    bottlenecks = analyzer.identify_bottlenecks(profile_output)

    # 生成优化报告
    analyzer.generate_optimization_report(results, bottlenecks)

    print("\n" + "=" * 60)
    print("性能分析完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
