#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试常量折叠优化器"""

import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.optimization.constant_folding import ConstantFoldingOptimizer
from src.parser.ast_nodes import (
    AssignNode,
    BinaryOpNode,
    BlockNode,
    IdentifierNode,
    IfNode,
    NumberNode,
    ProgramNode,
    StringNode,
    UnaryOpNode,
    VarDefNode,
    WhileNode,
)


def test_constant_folding():
    """测试常量折叠优化器"""

    optimizer = ConstantFoldingOptimizer()

    # 测试1: 数字常量运算
    print("测试1: 数字常量运算")
    node = BinaryOpNode(
        line=1,
        column=1,
        left=NumberNode(line=1, column=1, value=10),
        operator="+",
        right=NumberNode(line=1, column=1, value=20),
    )
    optimized = optimizer.optimize(node)
    print(f"  原始: {node}")
    print(f"  优化后: {optimized}")
    print(f"  类型: {type(optimized).__name__}")
    print(f"  值: {optimized.value if isinstance(optimized, NumberNode) else 'N/A'}")
    print()

    # 测试2: 字符串连接
    print("测试2: 字符串连接")
    node = BinaryOpNode(
        line=1,
        column=1,
        left=StringNode(line=1, column=1, value="Hello, "),
        operator="+",
        right=StringNode(line=1, column=1, value="World!"),
    )
    optimized = optimizer.optimize(node)
    print(f"  原始: {node}")
    print(f"  优化后: {optimized}")
    print(f"  类型: {type(optimized).__name__}")
    print(f"  值: {optimized.value if isinstance(optimized, StringNode) else 'N/A'}")
    print()

    # 测试3: 一元操作
    print("测试3: 一元操作")
    node = UnaryOpNode(
        line=1, column=1, operator="-", operand=NumberNode(line=1, column=1, value=42)
    )
    optimized = optimizer.optimize(node)
    print(f"  原始: {node}")
    print(f"  优化后: {optimized}")
    print(f"  类型: {type(optimized).__name__}")
    print(f"  值: {optimized.value if isinstance(optimized, NumberNode) else 'N/A'}")
    print()

    # 测试4: 条件语句优化（条件为真）
    print("测试4: 条件语句优化（条件为真）")
    node = IfNode(
        line=1,
        column=1,
        condition=NumberNode(line=1, column=1, value=1),  # 真
        then_branch=[
            BinaryOpNode(
                line=2,
                column=1,
                left=NumberNode(line=2, column=1, value=1),
                operator="+",
                right=NumberNode(line=2, column=1, value=2),
            )
        ],
        else_branch=[
            BinaryOpNode(
                line=3,
                column=1,
                left=NumberNode(line=3, column=1, value=3),
                operator="+",
                right=NumberNode(line=3, column=1, value=4),
            )
        ],
    )
    optimized = optimizer.optimize(node)
    print(f"  原始: IfNode with condition=True")
    print(f"  优化后类型: {type(optimized).__name__}")
    if isinstance(optimized, BlockNode):
        print(f"  优化后语句数: {len(optimized.statements)}")
        for i, stmt in enumerate(optimized.statements):
            print(f"    语句{i+1}: {stmt}")
    else:
        print(f"  优化后语句数: N/A")
    print()

    # 测试5: 条件语句优化（条件为假）
    print("测试5: 条件语句优化（条件为假）")
    node = IfNode(
        line=1,
        column=1,
        condition=NumberNode(line=1, column=1, value=0),  # 假
        then_branch=[
            BinaryOpNode(
                line=2,
                column=1,
                left=NumberNode(line=2, column=1, value=1),
                operator="+",
                right=NumberNode(line=2, column=1, value=2),
            )
        ],
        else_branch=[
            BinaryOpNode(
                line=3,
                column=1,
                left=NumberNode(line=3, column=1, value=3),
                operator="+",
                right=NumberNode(line=3, column=1, value=4),
            )
        ],
    )
    optimized = optimizer.optimize(node)
    print(f"  原始: IfNode with condition=False")
    print(f"  优化后类型: {type(optimized).__name__}")
    if isinstance(optimized, BlockNode):
        print(f"  优化后语句数: {len(optimized.statements)}")
        for i, stmt in enumerate(optimized.statements):
            print(f"    语句{i+1}: {stmt}")
    else:
        print(f"  优化后语句数: N/A")
    print()

    # 测试6: while循环优化（条件为假）
    print("测试6: while循环优化（条件为假）")
    node = WhileNode(
        line=1,
        column=1,
        condition=NumberNode(line=1, column=1, value=0),  # 假
        body=[
            BinaryOpNode(
                line=2,
                column=1,
                left=NumberNode(line=2, column=1, value=1),
                operator="+",
                right=NumberNode(line=2, column=1, value=2),
            )
        ],
    )
    optimized = optimizer.optimize(node)
    print(f"  原始: WhileNode with condition=False")
    print(f"  优化后类型: {type(optimized).__name__}")
    if isinstance(optimized, BlockNode):
        print(f"  优化后语句数: {len(optimized.statements)}")
    else:
        print(f"  优化后语句数: N/A")
    print()

    # 测试7: 复杂表达式优化
    print("测试7: 复杂表达式优化")
    node = BinaryOpNode(
        line=1,
        column=1,
        left=BinaryOpNode(
            line=1,
            column=1,
            left=NumberNode(line=1, column=1, value=10),
            operator="*",
            right=NumberNode(line=1, column=1, value=2),
        ),
        operator="+",
        right=BinaryOpNode(
            line=1,
            column=1,
            left=NumberNode(line=1, column=1, value=5),
            operator="/",
            right=NumberNode(line=1, column=1, value=2),
        ),
    )
    optimized = optimizer.optimize(node)
    print(f"  原始: (10 * 2) + (5 / 2)")
    print(f"  优化后: {optimized}")
    print(f"  类型: {type(optimized).__name__}")
    if isinstance(optimized, NumberNode):
        print(f"  值: {optimized.value}")
    else:
        print(f"  值: N/A (未完全折叠)")
    print()

    # 测试8: 中文操作符
    print("测试8: 中文操作符")
    node = BinaryOpNode(
        line=1,
        column=1,
        left=NumberNode(line=1, column=1, value=10),
        operator="相加",
        right=NumberNode(line=1, column=1, value=20),
    )
    optimized = optimizer.optimize(node)
    print(f"  原始: 10 相加 20")
    print(f"  优化后: {optimized}")
    print(f"  类型: {type(optimized).__name__}")
    print(f"  值: {optimized.value if isinstance(optimized, NumberNode) else 'N/A'}")
    print()

    # 测试9: 布尔运算
    print("测试9: 布尔运算")
    node = BinaryOpNode(
        line=1,
        column=1,
        left=NumberNode(line=1, column=1, value=1),  # True
        operator="并且",
        right=NumberNode(line=1, column=1, value=0),  # False
    )
    optimized = optimizer.optimize(node)
    print(f"  原始: 1 并且 0")
    print(f"  优化后: {optimized}")
    print(f"  类型: {type(optimized).__name__}")
    print(f"  值: {optimized.value if isinstance(optimized, NumberNode) else 'N/A'}")
    print()

    # 测试10: 除零保护
    print("测试10: 除零保护")
    node = BinaryOpNode(
        line=1,
        column=1,
        left=NumberNode(line=1, column=1, value=10),
        operator="/",
        right=NumberNode(line=1, column=1, value=0),
    )
    optimized = optimizer.optimize(node)
    print(f"  原始: 10 / 0")
    print(f"  优化后: {optimized}")
    print(f"  类型: {type(optimized).__name__}")
    print(f"  是否折叠: {isinstance(optimized, NumberNode)}")
    print()

    # 输出统计信息
    stats = optimizer.get_optimization_stats()
    print(f"优化统计:")
    print(f"  折叠的常量表达式数量: {stats['optimized_count']}")
    print(f"  优化类型: {stats['description']}")

    return optimizer


def test_complex_program():
    """测试复杂程序优化"""
    print("\n" + "=" * 70)
    print("测试复杂程序优化")
    print("=" * 70)

    # 创建一个复杂的程序
    program = ProgramNode(
        line=1,
        column=1,
        statements=[
            # 常量计算
            VarDefNode(
                line=1,
                column=1,
                name="a",
                value=BinaryOpNode(
                    line=1,
                    column=1,
                    left=NumberNode(line=1, column=1, value=10),
                    operator="+",
                    right=NumberNode(line=1, column=1, value=20),
                ),
            ),
            # 字符串连接
            VarDefNode(
                line=2,
                column=1,
                name="b",
                value=BinaryOpNode(
                    line=2,
                    column=1,
                    left=StringNode(line=2, column=1, value="Hello, "),
                    operator="+",
                    right=StringNode(line=2, column=1, value="World!"),
                ),
            ),
            # 条件语句（条件为常量）
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
                        target=IdentifierNode(line=4, column=5, name="c"),
                        value=BinaryOpNode(
                            line=4,
                            column=5,
                            left=NumberNode(line=4, column=5, value=100),
                            operator="*",
                            right=NumberNode(line=4, column=5, value=2),
                        ),
                    )
                ],
                else_branch=[
                    AssignNode(
                        line=5,
                        column=5,
                        target=IdentifierNode(line=5, column=5, name="c"),
                        value=NumberNode(line=5, column=5, value=0),
                    )
                ],
            ),
            # 死循环（条件为假）
            WhileNode(
                line=6,
                column=1,
                condition=NumberNode(line=6, column=1, value=0),
                body=[
                    AssignNode(
                        line=7,
                        column=5,
                        target=IdentifierNode(line=7, column=5, name="d"),
                        value=NumberNode(line=7, column=5, value=999),
                    )
                ],
            ),
            # 复杂表达式
            VarDefNode(
                line=8,
                column=1,
                name="e",
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
        ],
    )

    optimizer = ConstantFoldingOptimizer()
    optimized_program = optimizer.optimize(program)

    print("\n原始程序:")
    print(program)

    print("\n优化后程序:")
    print(optimized_program)

    stats = optimizer.get_optimization_stats()
    print(f"\n优化统计:")
    print(f"  折叠的常量表达式数量: {stats['optimized_count']}")

    # 显示优化后的语句
    print(f"\n优化后语句数: {len(optimized_program.statements)}")
    for i, stmt in enumerate(optimized_program.statements):
        print(f"  语句{i+1}: {stmt}")

    return optimized_program


if __name__ == "__main__":
    print("常量折叠优化器测试")
    print("=" * 70)

    # 运行基本测试
    optimizer = test_constant_folding()

    # 运行复杂程序测试
    optimized_program = test_complex_program()

    print("\n" + "=" * 70)
    print("测试完成!")
    print("=" * 70)
