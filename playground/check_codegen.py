#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查生成的Python代码"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.codegen.python_codegen import PythonCodegen
from src.lexer.lexer import Lexer
from src.parser.parser import Parser

# 冒泡排序
bubble = """打印 "冒泡排序算法"。
定义 数据 = [64, 34, 25, 12, 22, 11, 90]。
打印 "原始数组："。
打印 数据。
定义 轮次 = 0。
遍历 i 于 范围 0 6：
  定义 轮次 = 轮次 相加 1。
  打印 "第" 轮次 "轮"。
。
打印 "排序完成"。"""

print("冒泡排序生成的Python代码：")
print("=" * 60)
lexer = Lexer(bubble)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
codegen = PythonCodegen()
python_code = codegen.generate(ast)
print(python_code)
