#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试带优化的代码生成器"""

import os
import sys
import time

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.codegen.python_codegen_with_optimizations import OptimizedPythonCodegenWithFolding
from src.parser.ast_nodes import (
    AssignNode,
    BinaryOpNode,
    ClassNode,
    FunctionCallNode,
    IdentifierNode,
    IfNode,
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


def create_test_ast():
    """创建测试AST"""
    # 创建包含常量表达式的复杂AST
    return ProgramNode(
        line=1,
        column=1,
        statements=[
            # 常量计算
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
            # 条件语句（条件为常量真）
            IfNode(
                line=3,
                column=1,
                condition=BinaryOpNode(
                    line=3,
                    column=1,
                    left=NumberNode(line=3, column=1, value=1),
                    operator="==",
                    right=NumberNode(line=3, column=1, value=1),
                ),
                then_branch=[
                    AssignNode(
                        line=4,
                        column=5,
                        target=IdentifierNode(line=4, column=5, name="y"),
                        value=BinaryOpNode(
                            line=4,
                            column=5,
                            left=NumberNode(line=4, column=1, value=100),
                            operator="*",
                            right=NumberNode(line=4, column=1, value=2),
                        ),
                    )
                ],
                else_branch=[
                    AssignNode(
                        line=5,
                        column=5,
                        target=IdentifierNode(line=5, column=5, name="y"),
                        value=NumberNode(line=5, column=5, value=0),
                    )
                ],
            ),
            # 死循环（条件为常量假）
            WhileNode(
                line=6,
                column=1,
                condition=NumberNode(line=6, column=1, value=0),
                body=[
                    AssignNode(
                        line=7,
                        column=5,
                        target=IdentifierNode(line=7, column=5, name="z"),
                        value=NumberNode(line=7, column=5, value=999),
                    )
                ],
            ),
            # 复杂表达式
            VarDefNode(
                line=8,
                column=1,
                name="result",
                value=BinaryOpNode(
                    line=8,
                    column=1,
                    left=UnaryOpNode(
                        line=8,
                        column=1,
                        operator="-",
                        operand=NumberNode(line=8, column=1, value=5),
                    ),
                    operator="*",
                    right=BinaryOpNode(
                        line=8,
                        column=1,
                        left=NumberNode(line=8, column=1, value=10),
                        operator="/",
                        right=NumberNode(line=8, column=1, value=2),
                    ),
                ),
            ),
            # 函数调用
            FunctionCallNode(
                line=9,
                column=1,
                name=IdentifierNode(line=9, column=1, name="打印"),
                args=[
                    BinaryOpNode(
                        line=9,
                        column=1,
                        left=StringNode(line=9, column=1, value="结果: "),
                        operator="+",
                        right=IdentifierNode(line=9, column=1, name="result"),
                    )
                ],
            ),
        ],
    )


def create_oop_test_ast():
    """创建OOP测试AST"""
    return ProgramNode(
        line=1,
        column=1,
        statements=[
            # 类定义
            ClassNode(
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
                                                line=8,
                                                column=9,
                                                obj=ThisNode(line=8, column=9),
                                                member="x",
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
                                                line=8,
                                                column=9,
                                                obj=ThisNode(line=8, column=9),
                                                member="x",
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
                                                line=8,
                                                column=9,
                                                obj=ThisNode(line=8, column=9),
                                                member="y",
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
                                                line=8,
                                                column=9,
                                                obj=ThisNode(line=8, column=9),
                                                member="y",
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
            ),
            # 创建对象并使用
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
            ),
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
            ),
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
            ),
        ],
    )


def test_optimized_codegen():
    """测试带优化的代码生成器"""

    print("带优化的代码生成器测试")
    print("=" * 70)

    # 创建测试AST
    test_ast = create_test_ast()
    oop_ast = create_oop_test_ast()

    # 测试不带优化的代码生成
    print("\n1. 测试不带优化的代码生成:")
    print("-" * 50)
    codegen_without_opt = OptimizedPythonCodegenWithFolding(enable_optimizations=False)
    code_without_opt = codegen_without_opt.generate(test_ast)
    print("生成的代码:")
    print(code_without_opt)

    # 测试带优化的代码生成
    print("\n2. 测试带优化的代码生成:")
    print("-" * 50)
    codegen_with_opt = OptimizedPythonCodegenWithFolding(enable_optimizations=True)
    code_with_opt = codegen_with_opt.generate(test_ast)
    print("生成的代码:")
    print(code_with_opt)

    # 显示优化统计
    stats = codegen_with_opt.get_optimization_stats()
    print(f"\n优化统计:")
    print(f"  常量折叠优化次数: {stats['constant_folding']}")
    print(f"  死代码消除次数: {stats['dead_code_elimination']}")
    print(f"  总优化次数: {stats['total_optimizations']}")
    print(f"  方法缓存命中数: {stats['method_cache_hits']}")

    # 比较代码
    print(f"\n代码比较:")
    print(f"  不带优化代码长度: {len(code_without_opt)} 字符")
    print(f"  带优化代码长度: {len(code_with_opt)} 字符")
    print(f"  代码减少: {len(code_without_opt) - len(code_with_opt)} 字符")

    # 测试OOP代码生成
    print("\n" + "=" * 70)
    print("3. 测试OOP代码生成:")
    print("-" * 50)

    # 重置统计
    codegen_with_opt.reset_stats()

    # 生成OOP代码
    oop_code_without_opt = codegen_without_opt.generate(oop_ast)
    oop_code_with_opt = codegen_with_opt.generate(oop_ast)

    print("不带优化的OOP代码:")
    print(
        oop_code_without_opt[:200] + "..."
        if len(oop_code_without_opt) > 200
        else oop_code_without_opt
    )

    print("\n带优化的OOP代码:")
    print(oop_code_with_opt[:200] + "..." if len(oop_code_with_opt) > 200 else oop_code_with_opt)

    # 显示优化统计
    stats = codegen_with_opt.get_optimization_stats()
    print(f"\nOOP优化统计:")
    print(f"  常量折叠优化次数: {stats['constant_folding']}")
    print(f"  死代码消除次数: {stats['dead_code_elimination']}")
    print(f"  总优化次数: {stats['total_optimizations']}")

    # 性能测试
    print("\n" + "=" * 70)
    print("4. 性能测试:")
    print("-" * 50)

    # 创建大量常量表达式的AST
    large_ast = ProgramNode(
        line=1,
        column=1,
        statements=[
            VarDefNode(
                line=i,
                column=1,
                name=f"var{i}",
                value=BinaryOpNode(
                    line=i,
                    column=1,
                    left=NumberNode(line=i, column=1, value=i),
                    operator="+",
                    right=BinaryOpNode(
                        line=i,
                        column=1,
                        left=NumberNode(line=i, column=1, value=i * 2),
                        operator="*",
                        right=NumberNode(line=i, column=1, value=i * 3),
                    ),
                ),
            )
            for i in range(100)
        ],
    )

    # 测试不带优化的性能
    print("测试不带优化的性能...")
    start_time = time.perf_counter()
    for _ in range(100):
        codegen_without_opt.generate(large_ast)
    time_without_opt = time.perf_counter() - start_time

    # 测试带优化的性能
    print("测试带优化的性能...")
    codegen_with_opt.reset_stats()
    start_time = time.perf_counter()
    for _ in range(100):
        codegen_with_opt.generate(large_ast)
    time_with_opt = time.perf_counter() - start_time

    print(f"\n性能结果:")
    print(f"  不带优化: {time_without_opt:.4f} 秒")
    print(f"  带优化: {time_with_opt:.4f} 秒")
    print(f"  性能提升: {time_without_opt/time_with_opt:.2f}x")

    stats = codegen_with_opt.get_optimization_stats()
    print(f"\n优化统计:")
    print(f"  常量折叠优化次数: {stats['constant_folding']}")
    print(f"  总优化次数: {stats['total_optimizations']}")
    print(f"  方法缓存命中数: {stats['method_cache_hits']}")

    # 验证优化效果
    print("\n" + "=" * 70)
    print("5. 优化效果验证:")
    print("-" * 50)

    # 检查常量折叠
    print("常量折叠验证:")
    code_without_opt_lines = code_without_opt.split("\n")
    code_with_opt_lines = code_with_opt.split("\n")

    # 查找常量表达式
    const_exprs = []
    for line in code_without_opt_lines:
        if "10 + (5 * 2)" in line:
            const_exprs.append(("10 + (5 * 2)", line))
        elif "100 * 2" in line:
            const_exprs.append(("100 * 2", line))
        elif "-5 * (10 / 2)" in line:
            const_exprs.append(("-5 * (10 / 2)", line))

    print(f"  找到 {len(const_exprs)} 个常量表达式")
    for expr, line in const_exprs:
        print(f"    表达式: {expr}")
        print(f"    原始行: {line.strip()}")

    # 检查优化后的代码
    print("\n优化后代码分析:")
    optimized_consts = []
    for line in code_with_opt_lines:
        if "30" in line and "x = 30" in line:
            optimized_consts.append(("x = 30", line))
        elif "200" in line and "y = 200" in line:
            optimized_consts.append(("y = 200", line))
        elif "-25.0" in line and "result = -25.0" in line:
            optimized_consts.append(("result = -25.0", line))

    print(f"  找到 {len(optimized_consts)} 个优化后的常量")
    for const, line in optimized_consts:
        print(f"    常量: {const}")
        print(f"    优化行: {line.strip()}")

    # 检查死代码消除
    print("\n死代码消除验证:")
    if "while 0:" in code_without_opt and "while 0:" not in code_with_opt:
        print("  [OK] while循环（条件为假）已被消除")
    else:
        print("  [FAIL] while循环（条件为假）未被消除")

    # 检查条件语句优化
    if "if (1 == 1):" in code_without_opt and "if (1 == 1):" not in code_with_opt:
        print("  [OK] 条件语句（条件为常量真）已被优化")
    else:
        print("  [FAIL] 条件语句（条件为常量真）未被优化")

    print("\n" + "=" * 70)
    print("测试完成!")
    print("=" * 70)

    return codegen_with_opt


if __name__ == "__main__":
    test_optimized_codegen()
