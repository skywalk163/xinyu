#!/usr/bin/env python3
"""
调试词法分析器
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer.lexer import Lexer

# 测试代码
test_code = """定义 加 = 函 x, y：
  返回 x 相加 y。
。

打印 "加(2, 3) = " 加 2 3。"""

print("测试代码:")
print(test_code)
print("\n" + "="*50 + "\n")

# 词法分析
lexer = Lexer(test_code)
tokens = lexer.tokenize()

print("词法分析结果:")
for i, token in enumerate(tokens):
    print(f"{i:3d}: {token.type.name:15} '{token.value}' (行{token.line}, 列{token.column})")