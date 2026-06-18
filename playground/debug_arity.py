#!/usr/bin/env python3
"""
调试函数元数
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.parser.verb_registry import VerbRegistry

# 测试代码
test_code = """定义 加法 = 函 x, y：
  返回 x 相加 y。
。

定义 结果 = 加法 (2 相加 3) 4。
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

# 检查动词注册表
print("动词注册表内容:")
for name, arity in parser.verb_registry._verbs.items():
    print(f"  {name}: {arity}")
