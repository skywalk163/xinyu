# -*- coding: utf-8 -*-
"""扩展测试脚本

测试更多语法结构和功能。
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.codegen.python_codegen import PythonCodegen
from src.lexer.lexer import Lexer
from src.parser.parser import Parser


def test_extended():
    """扩展测试"""

    print("=" * 60)
    print("扩展测试")
    print("=" * 60)

    # 测试用例
    test_cases = [
        # 测试1：字符串
        {
            "name": "字符串",
            "code": '定义 消息 = "你好世界"。',
            "expected": '消息 = "你好世界"',
        },
        # 测试2：布尔值
        {
            "name": "布尔值",
            "code": "定义 标志 = 真值。",
            "expected": "标志 = True",
        },
        # 测试3：列表
        {
            "name": "列表",
            "code": "定义 列表 = [1, 2, 3]。",
            "expected": "列表 = [1, 2, 3]",
        },
        # 测试4：比较操作
        {
            "name": "比较操作",
            "code": "定义 结果 = x 等于 y。",
            "expected": "结果 = (x == y)",
        },
        # 测试5：逻辑操作
        {
            "name": "逻辑操作",
            "code": "定义 结果 = a 并且 b。",
            "expected": "结果 = (a and b)",
        },
        # 测试6：嵌套函数调用
        {
            "name": "嵌套函数调用",
            "code": "打印 相加 相乘 2 3 4。",
            "expected": "print(相加(相乘(2, 3), 4))",
        },
        # 测试7：多参数函数
        {
            "name": "多参数函数",
            "code": "定义 结果 = 相加 1 2 3。",
            "expected": "结果 = 相加(1, 2, 3)",
        },
        # 测试8：数学表达式
        {
            "name": "数学表达式",
            "code": "定义 结果 = x 相加 y 相乘 z。",
            "expected": "结果 = (x + (y * z))",
        },
    ]

    # 运行测试
    passed = 0
    failed = 0

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {test_case['name']}")
        print("-" * 60)

        try:
            # 词法分析
            print("1. 词法分析...")
            lexer = Lexer(test_case["code"])
            tokens = lexer.tokenize()
            print(f"   Token数量: {len(tokens)}")

            # 语法分析
            print("2. 语法分析...")
            parser = Parser(tokens)
            ast = parser.parse()
            print(f"   AST节点数: {len(ast.statements)}")

            # 代码生成
            print("3. 代码生成...")
            codegen = PythonCodegen()
            python_code = codegen.generate(ast)
            print(f"   生成代码:\n{python_code}")

            # 验证结果
            if test_case["expected"] in python_code:
                print("[PASS] 测试通过")
                passed += 1
            else:
                print(f"[FAIL] 测试失败: 期望包含 '{test_case['expected']}'")
                failed += 1

        except Exception as e:
            print(f"[FAIL] 测试失败: {e}")
            failed += 1

    # 输出统计
    print("\n" + "=" * 60)
    print(f"测试统计: 通过 {passed}/{len(test_cases)}, 失败 {failed}/{len(test_cases)}")
    print("=" * 60)

    return passed, failed


def test_complex():
    """复杂测试"""

    print("\n" + "=" * 60)
    print("复杂测试")
    print("=" * 60)

    # 测试用例
    test_cases = [
        # 测试1：完整函数定义
        {
            "name": "完整函数定义",
            "code": """函数 平方：
  参数 n。
  返回 n 相乘 n。
""",
            "expected": "def 平方(n):",
        },
        # 测试2：条件语句
        {
            "name": "条件语句",
            "code": """如果 x 大于 5 那么
  打印 "大"。
否则
  打印 "小"。
""",
            "expected": "if (x > 5):",
        },
        # 测试3：循环语句
        {
            "name": "循环语句",
            "code": """循环 i 遍历 [1, 2, 3]：
  打印 i。
""",
            "expected": "for i in [1, 2, 3]:",
        },
    ]

    # 运行测试
    passed = 0
    failed = 0

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {test_case['name']}")
        print("-" * 60)

        try:
            # 词法分析
            print("1. 词法分析...")
            lexer = Lexer(test_case["code"])
            tokens = lexer.tokenize()
            print(f"   Token数量: {len(tokens)}")

            # 语法分析
            print("2. 语法分析...")
            parser = Parser(tokens)
            ast = parser.parse()
            print(f"   AST节点数: {len(ast.statements)}")

            # 代码生成
            print("3. 代码生成...")
            codegen = PythonCodegen()
            python_code = codegen.generate(ast)
            print(f"   生成代码:\n{python_code}")

            # 验证结果
            if test_case["expected"] in python_code:
                print("[PASS] 测试通过")
                passed += 1
            else:
                print(f"[FAIL] 测试失败: 期望包含 '{test_case['expected']}'")
                failed += 1

        except Exception as e:
            print(f"[FAIL] 测试失败: {e}")
            failed += 1

    # 输出统计
    print("\n" + "=" * 60)
    print(f"测试统计: 通过 {passed}/{len(test_cases)}, 失败 {failed}/{len(test_cases)}")
    print("=" * 60)

    return passed, failed


def test_complete_program():
    """完整程序测试"""

    print("\n" + "=" * 60)
    print("完整程序测试")
    print("=" * 60)

    # 完整程序
    program = """定义 x = 5。
定义 y = 10。

函数 相加：
  参数 a。
  参数 b。
  返回 a 相加 b。

定义 结果 = 相加 x y。
打印 结果。
"""

    print("\n心语代码:")
    print(program)

    try:
        # 词法分析
        print("\n1. 词法分析...")
        lexer = Lexer(program)
        tokens = lexer.tokenize()
        print(f"   Token数量: {len(tokens)}")

        # 语法分析
        print("\n2. 语法分析...")
        parser = Parser(tokens)
        ast = parser.parse()
        print(f"   AST节点数: {len(ast.statements)}")

        # 代码生成
        print("\n3. 代码生成...")
        codegen = PythonCodegen()
        python_code = codegen.generate(ast)
        print(f"   生成Python代码:")
        print(python_code)

        # 执行生成的代码
        print("\n4. 执行生成的代码...")
        exec_globals = {}
        exec(python_code, exec_globals)

        print("\n[PASS] 完整程序测试通过")
        return True

    except Exception as e:
        print(f"\n[FAIL] 完整程序测试失败: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    # 运行所有测试
    print("\n" + "=" * 60)
    print("开始扩展测试")
    print("=" * 60)

    # 测试1：扩展测试
    passed1, failed1 = test_extended()

    # 测试2：复杂测试
    passed2, failed2 = test_complex()

    # 测试3：完整程序测试
    complete_success = test_complete_program()

    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"扩展测试: 通过 {passed1}, 失败 {failed1}")
    print(f"复杂测试: 通过 {passed2}, 失败 {failed2}")
    print(f"完整程序测试: {'通过' if complete_success else '失败'}")
    print("=" * 60)
