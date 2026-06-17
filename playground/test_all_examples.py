#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试所有Playground示例"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.codegen.python_codegen import PythonCodegen

# 所有示例代码
examples = {
    'hello': '''# 你好，世界
定义 问候 = "你好，心语！"。
打印 问候。

定义 名字 = "世界"。
打印 "你好，" 名字。''',

    'variables': '''# 变量定义示例
定义 整数 = 42。
定义 浮点数 = 3.14。
定义 字符串 = "心语"。
定义 布尔值 = 真值。

打印 "整数：" 整数。
打印 "浮点数：" 浮点数。
打印 "字符串：" 字符串。
打印 "布尔值：" 布尔值。''',

    'function': '''# 函数定义示例
定义 平方 = 函 x：
  返回 x 相乘 x。
。

定义 立方 = 函 x：
  返回 x 相乘 x 相乘 x。
。

定义 两数之和 = 函 a b：
  返回 a 相加 b。
。

打印 "平方(5) = " 平方 5。
打印 "立方(3) = " 立方 3。
打印 "两数之和(10, 20) = " 两数之和 10 20。''',

    'condition': '''# 条件判断示例
定义 成绩 = 85。

如果 成绩 大于等于 90 那么：
  打印 "优秀"。
可选 成绩 大于等于 80 那么：
  打印 "良好"。
可选 成绩 大于等于 70 那么：
  打印 "中等"。
可选 成绩 大于等于 60 那么：
  打印 "及格"。
否则：
  打印 "不及格"。
。''',

    'loop': '''# 循环遍历示例
定义 水果 = 列表 "苹果" "香蕉" "橘子"。

打印 "遍历水果列表："。
遍历 水果 于 水果：
  打印 水果。
。

打印 "遍历数字范围："。
遍历 数字 于 范围 1 6：
  打印 数字。
。''',

    'fibonacci': '''# 斐波那契数列
定义 斐波那契 = 函 n：
  如果 n 小于 2 那么：
    返回 n。
  。
  返回 斐波那契 n 相减 1 相加 斐波那契 n 相减 2。
。

打印 "斐波那契数列前10项："。
遍历 i 于 范围 1 11：
  打印 "斐波那契(" i ") = " 斐波那契 i。
。''',

    'list': '''# 列表操作示例
定义 数字 = 列表 1 2 3 4 5。

打印 "原始列表：" 数字。
打印 "列表长度：" 长度 数字。

定义 求和 = 函 列表：
  定义 总和 = 0。
  遍历 元素 于 列表：
    定义 总和 = 总和 相加 元素。
  。
  返回 总和。
。

打印 "列表求和：" 求和 数字。''',

    'dict': '''# 字典操作示例
定义 学生 = {"姓名": "张三", "年龄": 20, "成绩": 85}。

打印 "学生信息：" 学生。
打印 "姓名：" 学生["姓名"]。
打印 "年龄：" 学生["年龄"]。''',

    'math': '''# 数学运算示例
定义 a = 10。
定义 b = 3。

打印 "a = " a ", b = " b。
打印 "a 相加 b = " a 相加 b。
打印 "a 相减 b = " a 相减 b。
打印 "a 相乘 b = " a 相乘 b。
打印 "a 相除 b = " a 相除 b。
打印 "a 取余 b = " a 取余 b。

打印 "平方根(16) = " 平方根 16。
打印 "绝对值(-5) = " 绝对值 -5。
打印 "最大值(1, 5, 3, 2) = " 最大值 1 5 3 2。'''
}

print("=" * 80)
print("测试所有Playground示例")
print("=" * 80)
print()

results = []

for name, code in examples.items():
    print(f"\n{'='*80}")
    print(f"测试示例: {name}")
    print(f"{'='*80}")
    print("\n心语代码:")
    print(code)
    print()

    try:
        # 编译
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        codegen = PythonCodegen()
        python_code = codegen.generate(ast)

        print("生成的Python代码:")
        print(python_code)
        print()

        # 执行
        print("执行结果:")
        exec(python_code)
        print()

        results.append((name, True, None))
        print("[PASS] 测试通过")

    except Exception as e:
        results.append((name, False, str(e)))
        print(f"[FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()

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
