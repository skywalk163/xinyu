#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查词法分析器关键字"""

from src.lexer.lexer import Lexer

# 查看词法分析器的关键字
lexer = Lexer("")
print("关键字映射:")
for keyword, token_type in lexer.keywords.items():
    print(f"  {repr(keyword)}: {token_type.name}")

# 检查'则'是否在关键字中
print()
print('检查"则":', "则" in lexer.keywords)
print('检查"那么":', "那么" in lexer.keywords)

# 查看THEN对应的关键字
print()
print("THEN关键字对应的中文:")
for keyword, token_type in lexer.keywords.items():
    if token_type.name == "THEN":
        print(f"  {repr(keyword)}")
