#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量更新测试文件中的关键字

将单字关键字替换为双字关键字。
"""

import os
import re
from pathlib import Path

# 关键字映射（旧 -> 新）
KEYWORD_MAPPINGS = {
    # 核心关键字
    '"定"': '"定义"',
    '"函"': '"函数"',
    '"若"': '"如果"',
    '"真"': '"真值"',
    '"假"': '"假值"',

    # 语法标记
    '"则"': '"那么"',
    '"否则若"': '"可选"',
    '"遍历"': '"循环"',
    '"当"': '"当满足"',
    '"持续"': '"继续"',
    '"于"': '"遍历"',
    '"次"': '"次数"',
    '"接收"': '"参数"',

    # 操作符
    '"加"': '"相加"',
    '"减"': '"相减"',
    '"乘"': '"相乘"',
    '"除"': '"相除"',
    '"等"': '"等于"',
    '"小"': '"小于"',
    '"大"': '"大于"',
    '"且"': '"并且"',
    '"或"': '"或者"',
    '"非"': '"非也"',

    # 内置函数
    '"印"': '"打印"',

    # 字符串中的关键字（需要更谨慎）
    '定 ': '定义 ',
    '函 ': '函数 ',
    '若 ': '如果 ',
    '真 ': '真值 ',
    '假 ': '假值 ',
    '则 ': '那么 ',
    '当 ': '当满足 ',
    '于 ': '遍历 ',
    '次 ': '次数 ',
    '加 ': '相加 ',
    '减 ': '相减 ',
    '乘 ': '相乘 ',
    '除 ': '相除 ',
    '等 ': '等于 ',
    '小 ': '小于 ',
    '大 ': '大于 ',
    '且 ': '并且 ',
    '或 ': '或者 ',
    '非 ': '非也 ',
    '印 ': '打印 ',
}

# 代码示例中的关键字（在字符串中）
CODE_MAPPINGS = {
    '定 ': '定义 ',
    '函 ': '函数 ',
    '若 ': '如果 ',
    '真': '真值',
    '假': '假值',
    '则': '那么',
    '当': '当满足',
    '于': '遍历',
    '次': '次数',
    '加': '相加',
    '减': '相减',
    '乘': '相乘',
    '除': '相除',
    '等': '等于',
    '小': '小于',
    '大': '大于',
    '且': '并且',
    '或': '或者',
    '非': '非也',
    '印': '打印',
}


def update_file(file_path: Path) -> bool:
    """更新单个文件

    Args:
        file_path: 文件路径

    Returns:
        是否进行了更改
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 应用关键字映射
        for old, new in KEYWORD_MAPPINGS.items():
            content = content.replace(old, new)

        # 如果内容有变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True

        return False

    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return False


def main():
    """主函数"""
    # 测试文件目录
    tests_dir = Path('g:/dumategithub/chineseprogram/tests')

    # 查找所有测试文件
    test_files = list(tests_dir.glob('test_*.py'))

    print(f"找到 {len(test_files)} 个测试文件")

    updated_count = 0
    for test_file in test_files:
        if update_file(test_file):
            print(f"[OK] 已更新: {test_file.name}")
            updated_count += 1
        else:
            print(f"[--] 无需更新: {test_file.name}")

    print(f"\n总计更新了 {updated_count} 个文件")


if __name__ == '__main__':
    main()
