#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 测试1：直接执行
print("测试1：直接执行")
code1 = """问候 = "你好"
print(问候)"""
exec(code1)
print()

# 测试2：使用exec_globals
print("测试2：使用exec_globals")
import builtins

code2 = """问候 = "你好"
print(问候)"""
exec_globals = {
    "__name__": "__main__",
    "__builtins__": builtins,
    "print": print,
}
exec(code2, exec_globals)
print()

# 测试3：捕获输出
print("测试3：捕获输出")
import io
import sys

code3 = """问候 = "你好"
print(问候)"""

old_stdout = sys.stdout
sys.stdout = io.StringIO()

exec_globals = {
    "__name__": "__main__",
    "__builtins__": builtins,
    "print": print,
}
exec(code3, exec_globals)

output = sys.stdout.getvalue()
sys.stdout = old_stdout

print(f"捕获的输出: {output.strip()}")
