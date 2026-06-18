# -*- coding: utf-8 -*-
"""批量修复测试文件中的重复替换问题"""

import re
from pathlib import Path

# 修复规则
FIXES = {
    # 修复重复的打印
    "打打印": "打印",
    "打印印": "打印",
    # 修复重复的定义
    "定义义": "定义",
    "函数数": "函数",
    "真值值": "真值",
    "假值值": "假值",
    # 修复重复的操作符
    "相相加": "相加",
    "相相减": "相减",
    "相相乘": "相乘",
    "相相除": "相除",
    # 修复重复的关键字
    "当满足满足": "当满足",
    "遍历遍历": "遍历",
    # 修复错误的语法
    "次：": "次数：",
    "次。": "次数。",
}


def fix_file(file_path: Path) -> int:
    """修复文件

    Args:
        file_path: 文件路径

    Returns:
        int: 修复次数
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content
        count = 0

        for wrong, correct in FIXES.items():
            if wrong in content:
                occurrences = content.count(wrong)
                count += occurrences
                content = content.replace(wrong, correct)

        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return count

        return 0

    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return 0


def fix_all_tests():
    """修复所有测试文件"""
    tests_dir = Path("g:/dumategithub/chineseprogram/tests")
    test_files = list(tests_dir.glob("test_*.py"))

    total_fixes = 0

    print("=== 批量修复测试文件 ===\n")

    for test_file in test_files:
        count = fix_file(test_file)
        if count > 0:
            total_fixes += count
            print(f"[FIX] {test_file.name}: {count} 处修复")

    print(f"\n总修复次数: {total_fixes}")
    return total_fixes


if __name__ == "__main__":
    fixes = fix_all_tests()
    if fixes > 0:
        print(f"\n✅ 成功修复 {fixes} 处问题！")
    else:
        print("\n✅ 没有需要修复的问题！")
