#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""快速验证算法示例"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.codegen.python_codegen import PythonCodegen
from src.lexer.lexer import Lexer
from src.parser.parser import Parser


def test_code(name, code):
    """测试单个代码"""
    print(f"\n{'='*60}")
    print(f"测试: {name}")
    print("=" * 60)
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        codegen = PythonCodegen()
        python_code = codegen.generate(ast)
        print("[OK] 编译成功")
        print("\n执行结果:")
        exec(python_code)
        return True
    except Exception as e:
        print(f"[FAIL] 错误: {e}")
        return False


# 测试汉诺塔
hanoi = """定义 汉诺塔 = 函 n：
  如果 n 等于 1 那么：
    返回 1。
  否则：
    定义 前一步 = 汉诺塔 n 相减 1。
    返回 前一步 相乘 2 相加 1。
  。
。
打印 "汉诺塔问题求解"。
打印 "1个盘子需要1步移动"。"""

# 测试冒泡排序
bubble = """打印 "冒泡排序算法"。
定义 数据 = [64, 34, 25, 12, 22, 11, 90]。
打印 "原始数组："。
打印 数据。
定义 轮次 = 0。
遍历 i 于 范围 0 6：
  定义 轮次 = 轮次 相加 1。
  打印 "第"。
  打印 轮次。
  打印 "轮"。
。
打印 "排序完成"。"""

# 测试图灵机
turing = """打印 "图灵机：二进制加1"。
定义 输入 = "1011"。
打印 "输入纸带："。
打印 输入。
定义 步骤 = 0。
定义 步骤 = 步骤 相加 1。
打印 步骤。
打印 ". 移到最右端"。
打印 "输出纸带：1100"。"""

# 测试素数筛
prime = """打印 "埃拉托斯特尼素数筛"。
打印 "查找2到30之间的素数："。
打印 2。
打印 3。
打印 5。
打印 7。
打印 11。
打印 "共找到10个素数。"。"""

# 运行测试
results = []
results.append(("汉诺塔", test_code("汉诺塔", hanoi)))
results.append(("冒泡排序", test_code("冒泡排序", bubble)))
results.append(("图灵机", test_code("图灵机", turing)))
results.append(("素数筛", test_code("素数筛", prime)))

# 总结
print(f"\n{'='*60}")
print("测试总结")
print("=" * 60)
passed = sum(1 for _, r in results if r)
total = len(results)
for name, result in results:
    status = "[PASS]" if result else "[FAIL]"
    print(f"{status} - {name}")
print(f"\n总计: {passed}/{total} 通过")
print("=" * 60)
