#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试字节码编译器"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.codegen.bytecode_compiler_fixed import BytecodeCompiler
from src.parser.ast_nodes import (
    BinaryOpNode,
    BlockNode,
    ClassNode,
    ForNode,
    FunctionCallNode,
    FunctionDefNode,
    IdentifierNode,
    IfNode,
    MemberAccessNode,
    MethodNode,
    NumberNode,
    ProgramNode,
    ReturnNode,
    StringNode,
    ThisNode,
    WhileNode,
)


def test_simple_expression():
    """测试简单表达式"""
    print("测试简单表达式...")
    compiler = BytecodeCompiler()

    # 创建一个简单的表达式：x = 10 + 20
    assign_node = AssignNode(
        line=1,
        column=1,
        target=IdentifierNode(line=1, column=1, value="x"),
        value=BinaryOpNode(
            line=1,
            column=5,
            left=NumberNode(line=1, column=5, value=10),
            op="相加",
            right=NumberNode(line=1, column=10, value=20),
        ),
    )

    block_node = BlockNode(line=1, column=1, statements=[assign_node])
    program_node = ProgramNode(line=1, column=1, statements=[block_node])

    try:
        code_obj = compiler.compile(program_node)
        print(f"✓ 成功编译简单表达式")
        print(f"  字节码对象: {code_obj}")
        print(f"  字节码长度: {len(code_obj.co_code)} 字节")

        # 执行字节码
        globals_dict = {}
        exec(code_obj, globals_dict)
        print(f"  执行结果: x = {globals_dict.get('x')}")
        return True
    except Exception as e:
        print(f"✗ 编译失败: {e}")
        return False


def test_function_definition():
    """测试函数定义"""
    print("\n测试函数定义...")
    compiler = BytecodeCompiler()

    # 创建一个简单的函数：函数 加法(a, b) { 返回 a + b }
    function_def = FunctionDefNode(
        line=1,
        column=1,
        name="加法",
        params=[
            IdentifierNode(line=1, column=8, value="a"),
            IdentifierNode(line=1, column=11, value="b"),
        ],
        body=BlockNode(
            line=1,
            column=15,
            statements=[
                ReturnNode(
                    line=1,
                    column=17,
                    value=BinaryOpNode(
                        line=1,
                        column=24,
                        left=IdentifierNode(line=1, column=24, value="a"),
                        op="相加",
                        right=IdentifierNode(line=1, column=28, value="b"),
                    ),
                )
            ],
        ),
    )

    block_node = BlockNode(line=1, column=1, statements=[function_def])
    program_node = ProgramNode(line=1, column=1, statements=[block_node])

    try:
        code_obj = compiler.compile(program_node)
        print(f"✓ 成功编译函数定义")
        print(f"  字节码对象: {code_obj}")

        # 执行字节码
        globals_dict = {}
        exec(code_obj, globals_dict)
        print(f"  函数已定义: {'加法' in globals_dict}")

        # 测试函数调用
        if "加法" in globals_dict:
            result = globals_dict["加法"](5, 3)
            print(f"  函数调用结果: 加法(5, 3) = {result}")
        return True
    except Exception as e:
        print(f"✗ 编译失败: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_class_definition():
    """测试类定义"""
    print("\n测试类定义...")
    compiler = BytecodeCompiler()

    # 创建一个简单的类
    class_def = ClassNode(
        line=1,
        column=1,
        name="Person",
        body=BlockNode(
            line=1,
            column=10,
            statements=[
                MethodNode(
                    line=2,
                    column=5,
                    name="初始化",
                    params=[
                        IdentifierNode(line=2, column=12, value="name"),
                        IdentifierNode(line=2, column=17, value="age"),
                    ],
                    body=BlockNode(
                        line=2,
                        column=22,
                        statements=[
                            AssignNode(
                                line=3,
                                column=9,
                                target=MemberAccessNode(
                                    line=3, column=9, obj=ThisNode(line=3, column=9), member="name"
                                ),
                                value=IdentifierNode(line=3, column=16, value="name"),
                            ),
                            AssignNode(
                                line=4,
                                column=9,
                                target=MemberAccessNode(
                                    line=4, column=9, obj=ThisNode(line=4, column=9), member="age"
                                ),
                                value=IdentifierNode(line=4, column=15, value="age"),
                            ),
                        ],
                    ),
                ),
                MethodNode(
                    line=6,
                    column=5,
                    name="介绍",
                    params=[],
                    body=BlockNode(
                        line=6,
                        column=9,
                        statements=[
                            FunctionCallNode(
                                line=7,
                                column=9,
                                function=IdentifierNode(line=7, column=9, value="打印"),
                                args=[
                                    BinaryOpNode(
                                        line=7,
                                        column=15,
                                        left=StringNode(line=7, column=15, value="我是"),
                                        op="相加",
                                        right=BinaryOpNode(
                                            line=7,
                                            column=20,
                                            left=MemberAccessNode(
                                                line=7,
                                                column=20,
                                                obj=ThisNode(line=7, column=20),
                                                member="name",
                                            ),
                                            op="相加",
                                            right=StringNode(line=7, column=25, value="，今年"),
                                        ),
                                    )
                                ],
                            )
                        ],
                    ),
                ),
            ],
        ),
    )

    block_node = BlockNode(line=1, column=1, statements=[class_def])
    program_node = ProgramNode(line=1, column=1, statements=[block_node])

    try:
        code_obj = compiler.compile(program_node)
        print(f"✓ 成功编译类定义")
        print(f"  字节码对象: {code_obj}")

        # 执行字节码
        globals_dict = {}
        exec(code_obj, globals_dict)
        print(f"  类已定义: {'Person' in globals_dict}")

        # 测试类实例化
        if "Person" in globals_dict:
            person = globals_dict["Person"]("张三", 25)
            print(f"  创建Person实例: {person}")
            print(f"  实例属性: name={person.name}, age={person.age}")
            person.介绍()
        return True
    except Exception as e:
        print(f"✗ 编译失败: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_control_flow():
    """测试控制流"""
    print("\n测试控制流...")
    compiler = BytecodeCompiler()

    # 创建一个if语句
    if_node = IfNode(
        line=1,
        column=1,
        condition=BinaryOpNode(
            line=1,
            column=4,
            left=IdentifierNode(line=1, column=4, value="x"),
            op="大于",
            right=NumberNode(line=1, column=8, value=0),
        ),
        then_branch=BlockNode(
            line=1,
            column=12,
            statements=[
                FunctionCallNode(
                    line=2,
                    column=5,
                    function=IdentifierNode(line=2, column=5, value="打印"),
                    args=[StringNode(line=2, column=10, value="x是正数")],
                )
            ],
        ),
        else_branch=BlockNode(
            line=3,
            column=5,
            statements=[
                FunctionCallNode(
                    line=4,
                    column=5,
                    function=IdentifierNode(line=4, column=5, value="打印"),
                    args=[StringNode(line=4, column=10, value="x不是正数")],
                )
            ],
        ),
    )

    block_node = BlockNode(line=1, column=1, statements=[if_node])
    program_node = ProgramNode(line=1, column=1, statements=[block_node])

    try:
        code_obj = compiler.compile(program_node)
        print(f"✓ 成功编译控制流")
        print(f"  字节码对象: {code_obj}")

        # 执行字节码
        for x in [5, -3, 0]:
            print(f"  测试 x = {x}:")
            globals_dict = {"x": x}
            exec(code_obj, globals_dict)
        return True
    except Exception as e:
        print(f"✗ 编译失败: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_loop():
    """测试循环"""
    print("\n测试循环...")
    compiler = BytecodeCompiler()

    # 创建一个while循环
    while_node = WhileNode(
        line=1,
        column=1,
        condition=BinaryOpNode(
            line=1,
            column=7,
            left=IdentifierNode(line=1, column=7, value="i"),
            op="小于",
            right=NumberNode(line=1, column=11, value=5),
        ),
        body=BlockNode(
            line=1,
            column=15,
            statements=[
                FunctionCallNode(
                    line=2,
                    column=5,
                    function=IdentifierNode(line=2, column=5, value="打印"),
                    args=[
                        BinaryOpNode(
                            line=2,
                            column=11,
                            left=StringNode(line=2, column=11, value="i = "),
                            op="相加",
                            right=IdentifierNode(line=2, column=18, value="i"),
                        )
                    ],
                ),
                AssignNode(
                    line=3,
                    column=5,
                    target=IdentifierNode(line=3, column=5, value="i"),
                    value=BinaryOpNode(
                        line=3,
                        column=9,
                        left=IdentifierNode(line=3, column=9, value="i"),
                        op="相加",
                        right=NumberNode(line=3, column=13, value=1),
                    ),
                ),
            ],
        ),
    )

    # 初始化i
    init_i = AssignNode(
        line=1,
        column=1,
        target=IdentifierNode(line=1, column=1, value="i"),
        value=NumberNode(line=1, column=5, value=0),
    )

    block_node = BlockNode(line=1, column=1, statements=[init_i, while_node])
    program_node = ProgramNode(line=1, column=1, statements=[block_node])

    try:
        code_obj = compiler.compile(program_node)
        print(f"✓ 成功编译循环")
        print(f"  字节码对象: {code_obj}")

        # 执行字节码
        globals_dict = {}
        exec(code_obj, globals_dict)
        print(f"  循环执行完成")
        return True
    except Exception as e:
        print(f"✗ 编译失败: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_builtin_functions():
    """测试内置函数"""
    print("\n测试内置函数...")
    compiler = BytecodeCompiler()

    # 测试内置函数调用
    print_call = FunctionCallNode(
        line=1,
        column=1,
        function=IdentifierNode(line=1, column=1, value="打印"),
        args=[StringNode(line=1, column=7, value="Hello, World!")],
    )

    block_node = BlockNode(line=1, column=1, statements=[print_call])
    program_node = ProgramNode(line=1, column=1, statements=[block_node])

    try:
        code_obj = compiler.compile(program_node)
        print(f"✓ 成功编译内置函数调用")
        print(f"  字节码对象: {code_obj}")

        # 执行字节码
        print("  执行输出:")
        exec(code_obj)
        return True
    except Exception as e:
        print(f"✗ 编译失败: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_performance():
    """测试性能"""
    print("\n测试性能...")
    compiler = BytecodeCompiler()

    # 创建一个简单的循环来计算性能
    # sum = 0
    # for i in range(1000):
    #     sum = sum + i
    init_sum = AssignNode(
        line=1,
        column=1,
        target=IdentifierNode(line=1, column=1, value="sum"),
        value=NumberNode(line=1, column=7, value=0),
    )

    for_node = ForNode(
        line=2,
        column=1,
        var=IdentifierNode(line=2, column=5, value="i"),
        iterable=FunctionCallNode(
            line=2,
            column=9,
            function=IdentifierNode(line=2, column=9, value="范围"),
            args=[NumberNode(line=2, column=15, value=1000)],
        ),
        body=BlockNode(
            line=2,
            column=20,
            statements=[
                AssignNode(
                    line=3,
                    column=5,
                    target=IdentifierNode(line=3, column=5, value="sum"),
                    value=BinaryOpNode(
                        line=3,
                        column=11,
                        left=IdentifierNode(line=3, column=11, value="sum"),
                        op="相加",
                        right=IdentifierNode(line=3, column=17, value="i"),
                    ),
                )
            ],
        ),
    )

    block_node = BlockNode(line=1, column=1, statements=[init_sum, for_node])
    program_node = ProgramNode(line=1, column=1, statements=[block_node])

    try:
        import time

        start_time = time.time()
        code_obj = compiler.compile(program_node)
        compile_time = time.time() - start_time

        print(f"✓ 编译时间: {compile_time*1000:.2f}ms")
        print(f"  字节码大小: {len(code_obj.co_code)} 字节")

        # 执行性能测试
        start_time = time.time()
        globals_dict = {}
        exec(code_obj, globals_dict)
        exec_time = time.time() - start_time

        print(f"  执行时间: {exec_time*1000:.2f}ms")
        print(f"  计算结果: sum = {globals_dict.get('sum')}")
        return True
    except Exception as e:
        print(f"✗ 编译失败: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("=" * 60)
    print("字节码编译器测试")
    print("=" * 60)

    tests = [
        ("简单表达式", test_simple_expression),
        ("函数定义", test_function_definition),
        ("类定义", test_class_definition),
        ("控制流", test_control_flow),
        ("循环", test_loop),
        ("内置函数", test_builtin_functions),
        ("性能测试", test_performance),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"✗ 测试异常: {e}")
            import traceback

            traceback.print_exc()
            results.append((test_name, False))

    print("\n" + "=" * 60)
    print("测试结果汇总:")
    print("=" * 60)

    passed = 0
    total = len(results)

    for test_name, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"{test_name}: {status}")
        if success:
            passed += 1

    print(f"\n总计: {passed}/{total} 通过")

    if passed == total:
        print("🎉 所有测试通过！")
    else:
        print("⚠️  部分测试失败，请检查错误信息。")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
