# -*- coding: utf-8 -*-
"""简化测试脚本

测试中文编译器的基本功能。
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


def test_simple():
    """简单测试"""

    print("=" * 60)
    print("简单测试")
    print("=" * 60)

    # 测试用例
    test_cases = [
        # 测试1：变量定义
        {
            "name": "变量定义",
            "code": "定义 x = 5。",
            "expected": "x = 5",
        },
        # 测试2：函数调用
        {
            "name": "函数调用",
            "code": "打印 平方 5。",
            "expected": "print(平方(5))",
        },
        # 测试3：二元操作
        {
            "name": "二元操作",
            "code": "定义 结果 = x 相加 y。",
            "expected": "结果 = (x + y)",
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


def test_lexer_yan():
    """测试中文词法分析器文件"""

    print("\n" + "=" * 60)
    print("测试中文词法分析器文件")
    print("=" * 60)

    # 读取中文词法分析器
    lexer_file = project_root / "selfhost" / "lexer.yan"

    if not lexer_file.exists():
        print("[FAIL] 中文词法分析器文件不存在")
        return False

    print(f"\n读取文件: {lexer_file}")

    with open(lexer_file, "r", encoding="utf-8") as f:
        code = f.read()

    print(f"代码行数: {len(code.split(chr(10)))}")
    print(f"代码长度: {len(code)} 字符")

    # 显示前几行
    lines = code.split("\n")
    print(f"\n前10行:")
    for i, line in enumerate(lines[:10], 1):
        print(f"  {i}: {line}")

    return True


if __name__ == "__main__":
    # 运行测试
    print("\n" + "=" * 60)
    print("开始测试")
    print("=" * 60)

    # 测试1：基本功能
    passed, failed = test_simple()

    # 测试2：中文词法分析器文件
    lexer_success = test_lexer_yan()

    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"基本功能测试: 通过 {passed}, 失败 {failed}")
    print(f"中文词法分析器文件: {'存在' if lexer_success else '不存在'}")
    print("=" * 60)
