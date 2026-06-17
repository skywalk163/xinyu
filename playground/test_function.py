#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试函数调用"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.codegen.python_codegen import PythonCodegen

code = '''定义 两数之和 = 函 a b：
  返回 a 相加 b。
。

打印 两数之和 10 20。'''

print("心语代码:")
print(code)
print()

try:
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    print("Tokens:")
    for t in tokens:
        print(f"  {t.type}: {t.value}")
    print()

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
