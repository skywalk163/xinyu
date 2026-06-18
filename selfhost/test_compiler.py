# -*- coding: utf-8 -*-
"""中文编译器测试脚本

测试中文词法分析器、语法分析器和代码生成器。
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


def test_chinese_compiler():
    """测试中文编译器"""

    print("=" * 60)
    print("中文编译器测试")
    print("=" * 60)

    # 测试用例
    test_cases = [
        # 测试1：变量定义
        {
            "name": "变量定义",
            "code": "定义 x = 5。",
            "expected": "x = 5",
        },
        # 测试2：函数定义
        {
            "name": "函数定义",
            "code": """函数 平方：
  参数 n。
  返回 n 相乘 n。
""",
            "expected": "def 平方(n):",
        },
        # 测试3：条件语句
        {
            "name": "条件语句",
            "code": """如果 x 大于 5 那么
  打印 "大"。
否则
  打印 "小"。
""",
            "expected": "if x > 5:",
        },
        # 测试4：循环语句
        {
            "name": "循环语句",
            "code": """循环 i 遍历 [1, 2, 3]：
  打印 i。
""",
            "expected": "for i in [1, 2, 3]:",
        },
        # 测试5：当语句
        {
            "name": "当语句",
            "code": """当满足 x 大于 0：
  打印 x。
  x = x 相减 1。
""",
            "expected": "while x > 0:",
        },
        # 测试6：函数调用
        {
            "name": "函数调用",
            "code": "打印 平方 5。",
            "expected": "print(平方(5))",
        },
        # 测试7：二元操作
        {
            "name": "二元操作",
            "code": "定义 结果 = x 相加 y。",
            "expected": "结果 = x + y",
        },
        # 测试8：完整程序
        {
            "name": "完整程序",
            "code": """定义 x = 5。
函数 平方：
  参数 n。
  返回 n 相乘 n。
打印 平方 x。
""",
            "expected": "x = 5",
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


def test_bootstrap():
    """测试自举"""

    print("\n" + "=" * 60)
    print("自举测试")
    print("=" * 60)

    # 读取中文词法分析器
    lexer_file = project_root / "selfhost" / "lexer.yan"

    if not lexer_file.exists():
        print("[FAIL] 中文词法分析器文件不存在")
        return False

    print(f"\n读取中文词法分析器: {lexer_file}")

    with open(lexer_file, "r", encoding="utf-8") as f:
        lexer_code = f.read()

    print(f"代码行数: {len(lexer_code.split(chr(10)))}")

    try:
        # 用Python编译器编译
        print("\n1. 用Python编译器编译...")
        lexer_obj = Lexer(lexer_code)
        tokens = lexer_obj.tokenize()
        print(f"   Token数量: {len(tokens)}")

        parser_obj = Parser(tokens)
        ast = parser_obj.parse()
        print(f"   AST节点数: {len(ast.statements)}")

        codegen_obj = PythonCodegen()
        python_code = codegen_obj.generate(ast)
        print(f"   生成Python代码行数: {len(python_code.split(chr(10)))}")

        print("\n[PASS] 自举测试通过")
        return True

    except Exception as e:
        print(f"\n[FAIL] 自举测试失败: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_error_handling():
    """测试错误处理"""

    print("\n" + "=" * 60)
    print("错误处理测试")
    print("=" * 60)

    # 错误测试用例
    error_cases = [
        {
            "name": "缺少句号",
            "code": "定义 x = 5",
            "expected_error": "期望'。'",
        },
        {
            "name": "缺少等号",
            "code": "定义 x 5。",
            "expected_error": "期望'='",
        },
        {
            "name": "缺少冒号",
            "code": """函数 平方
  参数 n。
  返回 n 相乘 n。
""",
            "expected_error": "期望'：'",
        },
    ]

    # 运行测试
    passed = 0
    failed = 0

    for i, error_case in enumerate(error_cases, 1):
        print(f"\n测试 {i}: {error_case['name']}")
        print("-" * 60)

        try:
            # 尝试编译
            lexer = Lexer(error_case["code"])
            tokens = lexer.tokenize()

            parser = Parser(tokens)
            ast = parser.parse()

            codegen = PythonCodegen()
            python_code = codegen.generate(ast)

            print(f"[FAIL] 测试失败: 应该抛出错误 '{error_case['expected_error']}'")
            failed += 1

        except Exception as e:
            error_msg = str(e)
            if error_case["expected_error"] in error_msg:
                print(f"[PASS] 测试通过: 正确捕获错误 '{error_case['expected_error']}'")
                passed += 1
            else:
                print(f"[FAIL] 测试失败: 错误消息不匹配")
                print(f"   期望: {error_case['expected_error']}")
                print(f"   实际: {error_msg}")
                failed += 1

    # 输出统计
    print("\n" + "=" * 60)
    print(f"错误处理测试统计: 通过 {passed}/{len(error_cases)}, 失败 {failed}/{len(error_cases)}")
    print("=" * 60)

    return passed, failed


if __name__ == "__main__":
    # 运行所有测试
    print("\n" + "=" * 60)
    print("开始测试中文编译器")
    print("=" * 60)

    # 测试1：基本功能
    passed1, failed1 = test_chinese_compiler()

    # 测试2：错误处理
    passed2, failed2 = test_error_handling()

    # 测试3：自举
    bootstrap_success = test_bootstrap()

    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"基本功能测试: 通过 {passed1}, 失败 {failed1}")
    print(f"错误处理测试: 通过 {passed2}, 失败 {failed2}")
    print(f"自举测试: {'通过' if bootstrap_success else '失败'}")
    print("=" * 60)
