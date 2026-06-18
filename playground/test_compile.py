#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试心语代码编译"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.codegen.python_codegen import PythonCodegen
from src.lexer.lexer import Lexer
from src.parser.parser import Parser

# 测试代码
test_code = """定义 问候 = "你好，心语！"。
打印 问候。"""

print("=" * 60)
print("测试心语代码编译")
print("=" * 60)
print()
print("原始代码:")
print(test_code)
print()

try:
    # 词法分析
    print("1. 词法分析...")
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    print(f"   生成 {len(tokens)} 个token")

    # 语法分析
    print("2. 语法分析...")
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"   生成AST: {type(ast).__name__}")

    # 代码生成
    print("3. 代码生成...")
    codegen = PythonCodegen()
    python_code = codegen.generate(ast)

    print()
    print("=" * 60)
    print("生成的Python代码:")
    print("=" * 60)
    print(python_code)
    print()

    # 执行代码
    print("=" * 60)
    print("执行结果:")
    print("=" * 60)
    exec(python_code)

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()
