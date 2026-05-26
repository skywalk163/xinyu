#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer

code = '打印 "你好"。'
print(f"测试代码: {code}")

lexer = Lexer(code)
tokens = lexer.tokenize()
print(f"Tokens: {tokens}")

parser = Parser(tokens)
ast = parser.parse()
print(f"AST: {ast}")

analyzer = SemanticAnalyzer()
success = analyzer.analyze(ast)
print(f"Success: {success}")
print(f"Errors: {analyzer.errors}")
