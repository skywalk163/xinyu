#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试修改后的hello示例"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.codegen.python_codegen import PythonCodegen
from src.lexer.lexer import Lexer
from src.parser.parser import Parser

# 修改后的hello示例
test_code = """# 你好，世界
定义 问候 = "你好，心语！"。
打印 问候。

定义 名字 = "世界"。
打印 "你好，" 名字。"""

print("=" * 60)
print("测试修改后的hello示例")
print("=" * 60)
print()
print("心语代码:")
print(test_code)
print()

try:
    lexer = Lexer(test_code)
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
    print()
    print("✅ 测试通过！")

except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback

    traceback.print_exc()
