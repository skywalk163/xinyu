#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""调试parser_with_error_handler测试"""

from src.lexer.lexer import Lexer
from src.error_handling import ErrorHandler
from src.parser.parser_with_error_handler import ParserWithErrorHandler

# 测试if语句解析
source = '若 真 则 打印 "hello"'
print('源代码:', repr(source))

lexer = Lexer(source)
tokens = lexer.tokenize()
print('Tokens数量:', len(tokens))
for i, token in enumerate(tokens):
    print(f'  {i}: {token}')

error_handler = ErrorHandler()
parser = ParserWithErrorHandler(tokens, error_handler)
ast = parser.parse()

print('是否有错误:', error_handler.has_errors())
if error_handler.has_errors():
    errors = error_handler.get_errors()
    for error in errors:
        print(f'错误: {error.error_type} - {error.message} (行 {error.line}, 列 {error.column})')

print('AST:', ast)
print('AST语句数量:', len(ast.statements) if ast.statements else 0)
if ast.statements:
    print('第一个语句类型:', type(ast.statements[0]))
    print('第一个语句:', ast.statements[0])