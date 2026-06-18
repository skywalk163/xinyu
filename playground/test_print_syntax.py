#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试不同的打印语法"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.codegen.python_codegen import PythonCodegen
from src.lexer.lexer import Lexer
from src.parser.parser import Parser

# 测试不同的语法
test_cases = [
    ("语法1：单个参数", '打印 "你好"。'),
    ("语法2：变量", '定义 名字 = "世界"。\n打印 名字。'),
    ("语法3：两个参数", '打印 "你好" "世界"。'),
    ("语法4：字符串连接", '定义 名字 = "世界"。\n打印 "你好，" 名字。'),
]

for title, code in test_cases:
    print("=" * 60)
    print(title)
    print("=" * 60)
    print("心语代码:")
    print(code)
    print()

    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        codegen = PythonCodegen()
        python_code = codegen.generate(ast)

        print("Python代码:")
        print(python_code)
        print()

        print("执行结果:")
        exec(python_code)
        print()

    except Exception as e:
        print(f"错误: {e}")
        print()

    print()
