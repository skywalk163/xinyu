#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从index.html提取并测试所有示例"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.codegen.python_codegen import PythonCodegen
from src.lexer.lexer import Lexer
from src.parser.parser import Parser

# 从index.html读取示例
with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 提取示例代码
examples = {}
pattern = r"(\w+):\s*`([^`]+)`"
for match in re.finditer(pattern, content, re.DOTALL):
    name = match.group(1)
    code = match.group(2).strip()
    if name in [
        "hello",
        "variables",
        "function",
        "condition",
        "loop",
        "fibonacci",
        "list",
        "dict",
        "math",
        "hanoi",
        "bubble",
        "turing",
        "prime",
    ]:
        examples[name] = code

print("=" * 80)
print("测试所有Playground示例（从index.html提取）")
print("=" * 80)
print()

results = []

for name, code in examples.items():
    print(f"\n{'='*80}")
    print(f"测试示例: {name}")
    print(f"{'='*80}")

    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        codegen = PythonCodegen()
        python_code = codegen.generate(ast)

        exec(python_code)
        results.append((name, True, None))
        print("[PASS] 测试通过")

    except Exception as e:
        results.append((name, False, str(e)))
        print(f"[FAIL] 测试失败: {e}")

# 总结
print("\n" + "=" * 80)
print("测试总结")
print("=" * 80)
for name, success, error in results:
    if success:
        print(f"[PASS] {name}: 通过")
    else:
        print(f"[FAIL] {name}: 失败 - {error}")

passed = sum(1 for _, success, _ in results if success)
total = len(results)
print(f"\n总计: {passed}/{total} 通过")
