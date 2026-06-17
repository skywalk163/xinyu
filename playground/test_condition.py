#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试条件语法"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.codegen.python_codegen import PythonCodegen

code = '''定义 成绩 = 85。

如果 成绩 大于等于 90 那么：
  打印 "优秀"。
可选 成绩 大于等于 80 那么：
  打印 "良好"。
否则：
  打印 "不及格"。
。'''

print("心语代码:")
print(code)
print()

try:
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    codegen = PythonCodegen()
    python_code = codegen.generate(ast)

    print("Python代码:")
    print(python_code)
    print()

    print("执行结果:")
    exec(python_code)

except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
