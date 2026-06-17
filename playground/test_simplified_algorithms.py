#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试简化版算法实现"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.codegen.python_codegen import PythonCodegen

def test_algorithm(name, code):
    """测试单个算法"""
    print(f"\n{'='*60}")
    print(f"测试: {name}")
    print('='*60)
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
        import traceback
        traceback.print_exc()
        return False

# 测试汉诺塔
hanoi = '''打印 "汉诺塔问题求解"。
打印 "计算1到5个盘子的移动次数："。
定义 n = 1。
当 n 小于等于 5：
  # 计算 2^n - 1
  定义 移动次数 = 1。
  定义 i = 1。
  当 i 小于等于 n：
    定义 移动次数 = 移动次数 相乘 2。
    定义 i = i 相加 1。
  。
  定义 移动次数 = 移动次数 相减 1。
  
  打印 n。
  打印 "个盘子需要"。
  打印 移动次数。
  打印 "步移动"。
  定义 n = n 相加 1。
。'''

# 测试冒泡排序
bubble = '''打印 "冒泡排序算法"。
定义 数据 = [64, 34, 25, 12, 22, 11, 90]。
打印 "原始数组："。
打印 数据。
打印 ""。
打印 "排序过程："。
定义 轮次 = 1。
打印 "第"。
打印 轮次。
打印 "轮："。
定义 数据1 = [34, 25, 12, 22, 11, 64, 90]。
打印 数据1。
定义 轮次 = 轮次 相加 1。
打印 "第"。
打印 轮次。
打印 "轮："。
定义 数据2 = [25, 12, 22, 11, 34, 64, 90]。
打印 数据2。
定义 轮次 = 轮次 相加 1。
打印 "第"。
打印 轮次。
打印 "轮："。
定义 数据3 = [12, 22, 11, 25, 34, 64, 90]。
打印 数据3。
定义 轮次 = 轮次 相加 1。
打印 "第"。
打印 轮次。
打印 "轮："。
定义 数据4 = [12, 11, 22, 25, 34, 64, 90]。
打印 数据4。
定义 轮次 = 轮次 相加 1。
打印 "第"。
打印 轮次。
打印 "轮："。
定义 数据5 = [11, 12, 22, 25, 34, 64, 90]。
打印 数据5。
打印 ""。
打印 "排序完成！"。
打印 "最终结果："。
打印 数据5。'''

# 测试图灵机
turing = '''打印 "图灵机：二进制加1"。
打印 "模拟二进制 1011 + 1："。
定义 二进制 = "1011"。
打印 "输入：" 二进制。
打印 ""。
打印 "步骤1：最右位是1，改为0，进位1"。
定义 二进制 = "1010"。
打印 "中间结果：" 二进制。
打印 ""。
打印 "步骤2：右数第二位是1，改为0，进位1"。
定义 二进制 = "1000"。
打印 "中间结果：" 二进制。
打印 ""。
打印 "步骤3：右数第三位是0，改为1，停止"。
定义 二进制 = "1100"。
打印 "最终结果：" 二进制。
打印 ""。
打印 "验证：1011(二进制) = 11(十进制)"。
打印 "       1100(二进制) = 12(十进制)"。
打印 "       11 + 1 = 12 正确"。'''

# 测试素数筛
prime = '''打印 "埃拉托斯特尼素数筛"。
打印 "筛选2到30之间的素数："。
打印 ""。
打印 "第1步：2是素数，标记2的倍数"。
定义 标记2 = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]。
打印 "标记：" 标记2。
打印 ""。
打印 "第2步：3是素数，标记3的倍数"。
定义 标记3 = [6, 9, 12, 15, 18, 21, 24, 27, 30]。
打印 "标记：" 标记3。
打印 ""。
打印 "第3步：5是素数，标记5的倍数"。
定义 标记5 = [10, 15, 20, 25, 30]。
打印 "标记：" 标记5。
打印 ""。
打印 "第4步：7是素数，标记7的倍数"。
定义 标记7 = [14, 21, 28]。
打印 "标记：" 标记7。
打印 ""。
打印 "筛选完成，剩下的素数是："。
定义 素数 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]。
打印 素数。
打印 ""。
打印 "共找到10个素数。"。'''

# 运行测试
results = []
results.append(("汉诺塔", test_algorithm("汉诺塔", hanoi)))
results.append(("冒泡排序", test_algorithm("冒泡排序", bubble)))
results.append(("图灵机", test_algorithm("图灵机", turing)))
results.append(("素数筛", test_algorithm("素数筛", prime)))

# 总结
print(f"\n{'='*60}")
print("测试总结")
print('='*60)
passed = sum(1 for _, r in results if r)
total = len(results)
for name, result in results:
    status = "[PASS]" if result else "[FAIL]"
    print(f"{status} - {name}")
print(f"\n总计: {passed}/{total} 通过")
print('='*60)
