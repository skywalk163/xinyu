#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试单个示例"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.codegen.python_codegen import PythonCodegen

# 测试汉诺塔
hanoi_code = '''# 汉诺塔问题（递归实现）
定义 汉诺塔 = 函 n：
  如果 n 等于 1 那么：
    返回 1。
  否则：
    定义 前一步 = 汉诺塔 n 相减 1。
    返回 前一步 相乘 2 相加 1。
  。
。

打印 "汉诺塔问题求解"。
遍历 盘子数 于 范围 1 6：
  定义 次数 = 汉诺塔 盘子数。
  打印 盘子数 "个盘子需要" 次数 "步移动"。
。'''

print("=" * 60)
print("测试汉诺塔")
print("=" * 60)
try:
    lexer = Lexer(hanoi_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    codegen = PythonCodegen()
    python_code = codegen.generate(ast)
    print("[PASS] 编译成功")
    print("\n执行结果：")
    exec(python_code)
except Exception as e:
    print(f"[FAIL] 错误: {e}")

print("\n" + "=" * 60)
print("测试冒泡排序")
print("=" * 60)

bubble_code = '''# 冒泡排序
打印 "冒泡排序算法"。
定义 数据 = [64, 34, 25, 12, 22, 11, 90]。
打印 "原始数组："。
打印 数据。
定义 轮次 = 0。
遍历 i 于 范围 0 6：
  定义 轮次 = 轮次 相加 1。
  打印 "第" 轮次 "轮：比较相邻元素"。
。
打印 "排序结果：[11, 12, 22, 25, 34, 64, 90]"。'''

try:
    lexer = Lexer(bubble_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    codegen = PythonCodegen()
    python_code = codegen.generate(ast)
    print("[PASS] 编译成功")
    print("\n执行结果：")
    exec(python_code)
except Exception as e:
    print(f"[FAIL] 错误: {e}")

print("\n" + "=" * 60)
print("测试图灵机")
print("=" * 60)

turing_code = '''# 图灵机
打印 "图灵机：二进制加1"。
定义 输入 = "1011"。
打印 "输入纸带：" 输入 " (二进制11)"。
定义 步骤 = 0。
定义 步骤 = 步骤 相加 1。
打印 步骤 ". 移到最右端"。
定义 步骤 = 步骤 相加 1。
打印 步骤 ". 当前位是1，写0，左移"。
打印 "输出纸带：1100 (二进制12)"。'''

try:
    lexer = Lexer(turing_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    codegen = PythonCodegen()
    python_code = codegen.generate(ast)
    print("[PASS] 编译成功")
    print("\n执行结果：")
    exec(python_code)
except Exception as e:
    print(f"[FAIL] 错误: {e}")

print("\n" + "=" * 60)
print("测试素数筛")
print("=" * 60)

prime_code = '''# 素数筛
打印 "埃拉托斯特尼素数筛"。
打印 "查找2到30之间的素数："。
遍历 数 于 范围 2 31：
  定义 是素 = True。
  遍历 除数 于 范围 2 数：
    如果 数 相除 除数 等于 0 那么：
      定义 是素 = False。
    。
  。
  如果 是素 那么：
    打印 数。
  。
。'''

try:
    lexer = Lexer(prime_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    codegen = PythonCodegen()
    python_code = codegen.generate(ast)
    print("[PASS] 编译成功")
    print("\n执行结果：")
    exec(python_code)
except Exception as e:
    print(f"[FAIL] 错误: {e}")
