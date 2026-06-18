# -*- coding: utf-8 -*-
"""调试模块导入"""

from src.codegen.python_codegen import PythonCodegen
from src.lexer.lexer import Lexer
from src.parser.parser import Parser

source = """
导入 math。
打印 math.sqrt(16)。
"""

print("=== 词法分析 ===")
lexer = Lexer(source)
tokens = lexer.tokenize()
print("Tokens:")
for token in tokens:
    print(f"  {token}")

print("\n=== 语法分析 ===")
parser = Parser(tokens)
ast = parser.parse()
print("AST:")
print(ast)

print("\n=== 代码生成 ===")
codegen = PythonCodegen()
python_code = codegen.generate(ast)
print("Python代码:")
print(python_code)
