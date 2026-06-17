#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试math示例"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.codegen.python_codegen import PythonCodegen

code = '''# 数学运算示例
定义 a = 10。
定义 b = 3。

打印 "a = " a ", b = " b。
打印 "a 相加 b = " a 相加 b。
打印 "a 相减 b = " a 相减 b。
打印 "a 相乘 b = " a 相乘 b。
打印 "a 相除 b = " a 相除 b。

打印 "绝对值(-5) = " 绝对值 -5。
打印 "最大值(10, 20) = " 最大值 10 20。'''

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

except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
