#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""调试if语句解析"""

from src.error_handling import ErrorHandler
from src.lexer.lexer import Lexer
from src.parser.parser_with_error_handler import ParserWithErrorHandler

# 测试if语句解析
source = '若 真 那么 打印 "hello"'
print("源代码:", repr(source))

lexer = Lexer(source)
tokens = lexer.tokenize()
print("Tokens:")
for token in tokens:
    print(f"  {token.type.name:15} {repr(token.value):10} (行 {token.line}, 列 {token.column})")

error_handler = ErrorHandler()
parser = ParserWithErrorHandler(tokens, error_handler)
ast = parser.parse()

print("\n是否有错误:", error_handler.has_errors())
if error_handler.has_errors():
    errors = error_handler.get_errors()
    for error in errors:
        print(f"错误: {error.error_type} - {error.message} (行 {error.line}, 列 {error.column})")

print("\nAST:", ast)
print("AST语句数量:", len(ast.statements) if ast.statements else 0)
if ast.statements:
    if_node = ast.statements[0]
    print("第一个语句类型:", type(if_node))
    print("第一个语句:", if_node)
    print("条件:", if_node.condition)
    print("then分支:", if_node.then_branch)
    print("then分支数量:", len(if_node.then_branch))
    for i, stmt in enumerate(if_node.then_branch):
        print(f"  语句{i}: {type(stmt)} = {stmt}")
