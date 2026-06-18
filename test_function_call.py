#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试函数调用语法"""

from src.error_handling import ErrorHandler
from src.lexer.lexer import Lexer
from src.parser.parser_with_error_handler import ParserWithErrorHandler

# 测试1: 打印 "hello"
source1 = '打印 "hello"'
print("测试1:", repr(source1))
lexer1 = Lexer(source1)
tokens1 = lexer1.tokenize()
print("Tokens1:")
for t in tokens1:
    print(f"  {t.type.name:15} {repr(t.value):10}")

error_handler1 = ErrorHandler()
parser1 = ParserWithErrorHandler(tokens1, error_handler1)
ast1 = parser1.parse()
print("AST1:", ast1)
print("语句数量:", len(ast1.statements))
if ast1.statements:
    stmt = ast1.statements[0]
    print("语句类型:", type(stmt))
    print("语句:", stmt)

print()

# 测试2: 打印("hello")
source2 = '打印("hello")'
print("测试2:", repr(source2))
lexer2 = Lexer(source2)
tokens2 = lexer2.tokenize()
print("Tokens2:")
for t in tokens2:
    print(f"  {t.type.name:15} {repr(t.value):10}")

error_handler2 = ErrorHandler()
parser2 = ParserWithErrorHandler(tokens2, error_handler2)
ast2 = parser2.parse()
print("AST2:", ast2)
print("语句数量:", len(ast2.statements))
if ast2.statements:
    stmt = ast2.statements[0]
    print("语句类型:", type(stmt))
    print("语句:", stmt)

print()

# 测试3: 打印 "hello"。
source3 = '打印 "hello"。'
print("测试3:", repr(source3))
lexer3 = Lexer(source3)
tokens3 = lexer3.tokenize()
print("Tokens3:")
for t in tokens3:
    print(f"  {t.type.name:15} {repr(t.value):10}")

error_handler3 = ErrorHandler()
parser3 = ParserWithErrorHandler(tokens3, error_handler3)
ast3 = parser3.parse()
print("AST3:", ast3)
print("语句数量:", len(ast3.statements))
if ast3.statements:
    stmt = ast3.statements[0]
    print("语句类型:", type(stmt))
    print("语句:", stmt)
