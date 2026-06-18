#!/usr/bin/env python3
"""
测试心语语言的语法限制
分析为什么算法示例实现起来比较费劲
"""


def analyze_syntax_limits():
    """分析心语语言的语法限制"""
    print("=== 心语语言语法限制分析 ===")
    print()

    print("1. 函数定义语法：")
    print("   定义 函数名 = 函 参数：")
    print("     函数体")
    print("   。")
    print()

    print("2. 递归调用问题：")
    print("   - 纯言语言支持：汉诺塔 (减 n 1) 源 辅助 目标")
    print("   - 心语语言可能不支持：函数名 (表达式) 参数1 参数2 参数3")
    print("   - 需要分步计算：")
    print("     定义 新n = 减 n 1。")
    print("     汉诺塔 新n 源 辅助 目标。")
    print()

    print("3. 语句块限制：")
    print("   - 每个语句必须以句号结束")
    print("   - 条件语句和循环语句的缩进必须正确")
    print("   - 函数体中的语句需要正确缩进")
    print()

    print("4. 变量作用域问题：")
    print("   - 在循环内部定义同名变量可能导致问题")
    print("   - 函数参数传递可能有限制")
    print()

    print("5. 多参数函数调用：")
    print('   - 纯言语言：汉诺塔 3 "A" "C" "B"')
    print('   - 心语语言可能需要：汉诺塔 3 "A" "C" "B"')
    print("   - 但实际可能不支持多个字符串参数")
    print()

    print("=== 具体问题分析 ===")
    print()

    print("问题1：递归函数的参数传递")
    print("   纯言语言：汉诺塔 (减 n 1) 源 辅助 目标")
    print("   心语语言可能需要：")
    print("     定义 新n = 减 n 1。")
    print("     汉诺塔 新n 源 辅助 目标。")
    print()

    print("问题2：字符串连接")
    print('   纯言语言：印 连 "移动盘子从 " 源 " 到 " 目标')
    print('   心语语言：打印 连 "移动盘子从 " 源 " 到 " 目标')
    print("   注意：心语使用'打印'而不是'印'")
    print()

    print("问题3：条件语句嵌套")
    print("   纯言语言：")
    print("     若 等 n 1：")
    print("       印 ...")
    print("     。")
    print("     若 大 n 1：")
    print("       ...")
    print("     。")
    print("   。")
    print("   心语语言：")
    print("     如果 等 n 1 那么：")
    print("       打印 ...")
    print("     。")
    print("     否则：")
    print("       ...")
    print("     。")
    print("   。")
    print()

    print("=== 解决方案 ===")
    print()

    print("1. 简化递归：使用迭代代替递归")
    print("   - 汉诺塔：使用循环计算移动次数，手动列出步骤")
    print("   - 斐波那契：使用迭代版本")
    print()

    print("2. 避免复杂参数：")
    print("   - 将多参数函数拆分为多个单参数调用")
    print("   - 使用中间变量存储计算结果")
    print()

    print("3. 简化字符串操作：")
    print("   - 使用多个打印语句代替字符串连接")
    print("   - 或者使用'连'函数但注意参数顺序")
    print()

    print("4. 使用明确的变量名：")
    print("   - 避免在循环内重复定义同名变量")
    print("   - 使用不同的变量名存储中间结果")
    print()

    print("=== 示例对比 ===")
    print()

    print("纯言语言汉诺塔：")
    print("   定 汉诺塔 = 函 n 源 目标 辅助：")
    print("     若 等 n 1：")
    print('       印 连 "移动盘子从 " 源 " 到 " 目标。')
    print("     。")
    print("     若 大 n 1：")
    print("       汉诺塔 (减 n 1) 源 辅助 目标。")
    print('       印 连 "移动盘子从 " 源 " 到 " 目标。')
    print("       汉诺塔 (减 n 1) 辅助 目标 源。")
    print("     。")
    print("   。。")
    print()

    print("心语语言汉诺塔（简化版）：")
    print("   # 使用迭代计算移动次数")
    print("   定义 n = 1。")
    print("   当 n 小于等于 5：")
    print("     # 计算 2^n - 1")
    print("     定义 移动次数 = 1。")
    print("     定义 i = 1。")
    print("     当 i 小于等于 n：")
    print("       定义 移动次数 = 移动次数 相乘 2。")
    print("       定义 i = i 相加 1。")
    print("     。")
    print("     定义 移动次数 = 移动次数 相减 1。")
    print('     打印 n "个盘子需要" 移动次数 "步移动"。')
    print("     定义 n = n 相加 1。")
    print("   。")
    print()

    print("=== 结论 ===")
    print("心语语言对复杂递归和函数调用的支持有限，需要：")
    print("1. 使用迭代代替递归")
    print("2. 简化参数传递")
    print("3. 避免复杂的字符串操作")
    print("4. 使用明确的中间变量")
    print("5. 分步执行复杂计算")


if __name__ == "__main__":
    analyze_syntax_limits()
