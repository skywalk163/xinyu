# -*- coding: utf-8 -*-
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.codegen.python_codegen import PythonCodegen

# 测试正确的函数定义语法
code = '''定 平方 = 函 x：
  返回 x 乘 x。

印 平方 5。
'''

lexer = Lexer(code)
tokens = lexer.tokenize()

print("Tokens:")
for token in tokens:
    print(f"  {token}")

print("\nParsing...")
parser = Parser(tokens)
ast = parser.parse()

print(f"\nAST: {ast}")

print("\nGenerating Python code...")
codegen = PythonCodegen()
python_code = codegen.generate(ast)

print("\nGenerated Python code:")
print(python_code)

print("\nExecuting...")
exec(python_code)
