#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试汉诺塔示例"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.codegen.python_codegen import PythonCodegen

code = '''# 汉诺塔问题（递归实现）
# 汉诺塔递归函数
定义 汉诺塔 = 函 n：
  如果 n 等于 1 那么：
    返回 1。
  否则：
    定义 前一步 = 汉诺塔 n 相减 1。
    返回 前一步 相乘 2 相加 1。
  。
。

打印 "汉诺塔问题求解"。
打印 "=================="。
打印 ""。
打印 "汉诺塔递归公式：移动次数 = 2^n - 1"。
打印 ""。

# 计算1到5个盘子的移动次数
定义 盘子数 = 1。
遍历 i 于 范围 1 6：
  定义 次数 = 汉诺塔 盘子数。
  打印 盘子数 "个盘子需要" 次数 "步移动"。
  定义 盘子数 = 盘子数 相加 1。
。'''

print("测试汉诺塔代码...")
try:
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    codegen = PythonCodegen()
    python_code = codegen.generate(ast)
    print("编译成功！")
    print("\nPython代码：")
    print(python_code)
    print("\n执行结果：")
    exec(python_code)
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
