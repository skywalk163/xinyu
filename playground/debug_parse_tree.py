#!/usr/bin/env python3
"""
调试解析树
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.parser.parser import Parser
from src.lexer.lexer import Lexer
from src.parser.ast_nodes import *

def print_ast(node, indent=0):
    """打印AST树"""
    prefix = "  " * indent
    if isinstance(node, ProgramNode):
        print(f"{prefix}ProgramNode({len(node.statements)} statements)")
        for stmt in node.statements:
            print_ast(stmt, indent + 1)
    elif isinstance(node, VarDefNode):
        print(f"{prefix}VarDefNode(name={node.name})")
        print_ast(node.value, indent + 1)
    elif isinstance(node, FunctionDefNode):
        print(f"{prefix}FunctionDefNode(name={node.name}, params={node.params})")
        print_ast(node.body, indent + 1)
    elif isinstance(node, FunctionCallNode):
        print(f"{prefix}FunctionCallNode(name={node.name}, args={len(node.args)})")
        for i, arg in enumerate(node.args):
            print(f"{prefix}  arg[{i}]:")
            print_ast(arg, indent + 2)
    elif isinstance(node, BinaryOpNode):
        print(f"{prefix}BinaryOpNode(operator={node.operator})")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)
    elif isinstance(node, NumberNode):
        print(f"{prefix}NumberNode(value={node.value})")
    elif isinstance(node, IdentifierNode):
        print(f"{prefix}IdentifierNode(name={node.name})")
    elif isinstance(node, BlockNode):
        print(f"{prefix}BlockNode({len(node.statements)} statements)")
        for stmt in node.statements:
            print_ast(stmt, indent + 1)
    elif isinstance(node, ReturnNode):
        print(f"{prefix}ReturnNode")
        print_ast(node.value, indent + 1)
    else:
        print(f"{prefix}{type(node).__name__}")

# 测试代码
test_code = """定义 加法 = 函 x, y：
  返回 x 相加 y。
。

定义 结果 = 加法 (2) 3。
打印 结果。"""

print("测试代码:")
print(test_code)
print("\n" + "="*50 + "\n")

# 词法分析
lexer = Lexer(test_code)
tokens = lexer.tokenize()

print("词法分析结果:")
for i, token in enumerate(tokens):
    print(f"{i:3d}: {token.type.name:15} '{token.value}' (行{token.line}, 列{token.column})")

print("\n" + "="*50 + "\n")

# 语法分析
parser = Parser(tokens)
ast = parser.parse()

print("AST树:")
print_ast(ast)