# -*- coding: utf-8 -*-
"""语法统一批量替换脚本

将旧语法批量替换为新语法。
"""

import os
import re
from pathlib import Path

# 定义替换规则
REPLACEMENTS = {
    # 核心关键字
    "定": "定义",
    "函": "函数",
    "若": "如果",
    "真": "真值",
    "假": "假值",
    # 内置函数
    "印": "打印",
    "读": "输入",
    # 操作符（注意顺序，先替换长的）
    "相加": "相加",  # 已经是新语法
    "相减": "相减",
    "相乘": "相乘",
    "相除": "相除",
    "加": "相加",
    "减": "相减",
    "乘": "相乘",
    "除": "相除",
    # 比较操作符
    "等于": "等于",
    "不等": "不等",
    "大于": "大于",
    "小于": "小于",
    "大等": "大等",
    "小等": "小等",
    "大": "大于",
    "小": "小于",
    "等": "等于",
    # 逻辑操作符
    "并且": "并且",
    "或者": "或者",
    "非也": "非也",
    "且": "并且",
    "或": "或者",
    "非": "非也",
    # 循环关键字
    "当": "当满足",
}


def replace_in_file(file_path: Path, replacements: dict) -> tuple:
    """在文件中进行批量替换

    Args:
        file_path: 文件路径
        replacements: 替换规则字典

    Returns:
        (是否修改, 修改次数)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content
        count = 0

        # 按照从长到短的顺序替换，避免部分匹配
        sorted_replacements = sorted(replacements.items(), key=lambda x: len(x[0]), reverse=True)

        for old, new in sorted_replacements:
            if old in content:
                # 统计替换次数
                occurrences = content.count(old)
                count += occurrences
                content = content.replace(old, new)

        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True, count

        return False, 0

    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return False, 0


def update_test_files():
    """更新所有测试文件"""
    tests_dir = Path("g:/dumategithub/chineseprogram/tests")

    # 要处理的测试文件
    test_files = [
        "test_integration.py",
        "test_parser.py",
        "test_semantic.py",
        "test_main.py",
        "test_codegen.py",
        "test_lexer.py",
        "test_edge_cases.py",
    ]

    total_files = 0
    total_replacements = 0

    print("=== 开始批量替换测试文件 ===\n")

    for test_file in test_files:
        file_path = tests_dir / test_file

        if not file_path.exists():
            print(f"[WARN] 文件不存在: {test_file}")
            continue

        modified, count = replace_in_file(file_path, REPLACEMENTS)

        if modified:
            total_files += 1
            total_replacements += count
            print(f"[OK] {test_file}: {count} 处替换")
        else:
            print(f"[SKIP] {test_file}: 无需修改")

    print(f"\n=== 替换完成 ===")
    print(f"修改文件数: {total_files}")
    print(f"总替换次数: {total_replacements}")


def update_example_files():
    """更新所有示例文件"""
    examples_dir = Path("g:/dumategithub/chineseprogram/examples")

    # 查找所有 .yan 文件
    yan_files = list(examples_dir.rglob("*.yan"))

    total_files = 0
    total_replacements = 0

    print("\n=== 开始批量替换示例文件 ===\n")

    for yan_file in yan_files:
        modified, count = replace_in_file(yan_file, REPLACEMENTS)

        if modified:
            total_files += 1
            total_replacements += count
            print(f"[OK] {yan_file.name}: {count} 处替换")
        else:
            print(f"[SKIP] {yan_file.name}: 无需修改")

    print(f"\n=== 替换完成 ===")
    print(f"修改文件数: {total_files}")
    print(f"总替换次数: {total_replacements}")


if __name__ == "__main__":
    # 更新测试文件
    update_test_files()

    # 更新示例文件
    update_example_files()

    print("\n[OK] 所有文件更新完成！")
