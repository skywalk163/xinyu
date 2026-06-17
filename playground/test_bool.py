#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试布尔值语法"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.codegen.python_codegen import PythonCodegen

test_cases = [
    ('真值', '定义 x = 真值。'),
    ('假值', '定义 x = 假值。'),
    ('True', '定义 x = True。'),
    ('False', '定义 x = False。'),
]

for name, code in test_cases:
    print(f"\n测试: {name}")
    print(f"代码: {code}")
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        codegen = PythonCodegen()
        python_code = codegen.generate(ast)
        print(f"Python: {python_code}")
        exec(python_code)
        print("结果: 成功")
    except Exception as e:
        print(f"错误: {e}")
