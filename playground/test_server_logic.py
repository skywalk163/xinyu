#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试server.py的执行功能"""

import io
import os
import sys
from contextlib import redirect_stderr, redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.codegen.python_codegen import PythonCodegen
from src.lexer.lexer import Lexer
from src.parser.parser import Parser

# 测试代码
test_code = """定义 问候 = "你好，心语！"。
打印 问候。"""

print("=" * 60)
print("测试server.py执行逻辑")
print("=" * 60)
print()
print("原始代码:")
print(test_code)
print()

try:
    # 词法分析
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()

    # 语法分析
    parser = Parser(tokens)
    ast = parser.parse()

    # 代码生成
    codegen = PythonCodegen()
    python_code = codegen.generate(ast)

    print("生成的Python代码:")
    print(python_code)
    print()

    # 执行代码（模拟server.py的逻辑）
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()

    try:
        # 创建执行环境，包含所有内置函数
        import builtins

        exec_globals = {
            "__name__": "__main__",
            "__builtins__": builtins,
            # 添加常用的内置函数
            "print": print,
            "len": len,
            "range": range,
            "list": list,
            "dict": dict,
            "str": str,
            "int": int,
            "float": float,
            "abs": abs,
            "max": max,
            "min": min,
            "sum": sum,
            "sorted": sorted,
            "type": type,
        }

        # 执行代码
        exec(python_code, exec_globals)

        # 获取输出
        stdout_value = sys.stdout.getvalue()
        stderr_value = sys.stderr.getvalue()

        print()
        print("=" * 60)
        print("执行结果:")
        print("=" * 60)
        if stdout_value:
            print(stdout_value.strip())
        if stderr_value:
            print(f"错误: {stderr_value.strip()}")

    except Exception as e:
        print(f"执行错误: {str(e)}")
        import traceback

        traceback.print_exc()
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

except Exception as e:
    print(f"编译错误: {e}")
    import traceback

    traceback.print_exc()
