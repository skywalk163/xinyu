#!/usr/bin/env python3
"""
调试代码生成
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.codegen.python_codegen import PythonCodegen
from src.lexer.lexer import Lexer
from src.parser.parser import Parser

# 测试代码
test_code = """定义 相加函数 = 函 x, y：
  返回 x 相加 y。
。

定义 结果 = 相加函数 2 3。
打印 结果。"""

print("测试代码:")
print(test_code)
print("\n" + "=" * 50 + "\n")

# 词法分析
lexer = Lexer(test_code)
tokens = lexer.tokenize()

print("词法分析结果:")
for i, token in enumerate(tokens):
    print(f"{i:3d}: {token.type.name:15} '{token.value}' (行{token.line}, 列{token.column})")

print("\n" + "=" * 50 + "\n")

# 语法分析
parser = Parser(tokens)
ast = parser.parse()

print("语法分析结果:")
print(ast)

print("\n" + "=" * 50 + "\n")

# 代码生成
codegen = PythonCodegen()
generated_code = codegen.generate(ast)

print("生成的Python代码:")
print(generated_code)
