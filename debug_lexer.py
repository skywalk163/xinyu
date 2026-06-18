#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""调试词法分析器"""

from src.lexer.lexer import Lexer

# 测试词法分析器
source = '若 真 则 打印 "hello"'
print("源代码:", repr(source))

lexer = Lexer(source)
tokens = lexer.tokenize()

print("Tokens:")
for token in tokens:
    print(f"  {token.type.name:15} {repr(token.value):10} (行 {token.line}, 列 {token.column})")
