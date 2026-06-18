#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""心语代码格式化工具演示"""

import os
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools"))

from simple_formatter import SimpleXinyuFormatter


def demo_basic_formatting():
    """演示基本格式化功能"""
    print("=" * 60)
    print("心语代码格式化工具演示")
    print("=" * 60)

    # 创建格式化器
    formatter = SimpleXinyuFormatter()

    # 示例1：基本格式化
    print("\n1. 基本格式化示例:")
    print("-" * 40)

    unformatted_code = """# 未格式化的代码
定义 计算和(数字列表):
结果=0
对于 数字 在 数字列表:
结果=结果+数字
返回 结果

主函数():
数字=[1,2,3,4,5]
和=计算和(数字)
印"和是:"+字符串(和)
"""

    print("格式化前:")
    print(unformatted_code)

    formatted_code = formatter.format_code(unformatted_code)
    print("格式化后:")
    print(formatted_code)

    # 示例2：检查格式问题
    print("\n2. 格式检查示例:")
    print("-" * 40)

    issues = formatter.check_format(unformatted_code)
    print(f"发现 {len(issues)} 个格式问题:")
    for issue in issues:
        print(f"  第{issue['line']}行第{issue['column']}列: {issue['message']} ({issue['severity']})")

    # 示例3：使用不同配置
    print("\n3. 不同配置示例:")
    print("-" * 40)

    configs = [
        {"indent_size": 2, "name": "2空格缩进"},
        {"indent_size": 4, "name": "4空格缩进（默认）"},
        {"indent_size": 8, "name": "8空格缩进"},
    ]

    test_code = "定义 测试():如果 真:返回 1否则:返回 2"

    for config in configs:
        custom_formatter = SimpleXinyuFormatter(config)
        result = custom_formatter.format_code(test_code)
        print(f"{config['name']}:")
        print(result)

    # 示例4：文件操作
    print("\n4. 文件操作示例:")
    print("-" * 40)

    # 创建临时文件
    import tempfile

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".xinyu", delete=False, encoding="utf-8"
    ) as f:
        f.write(unformatted_code)
        temp_file = Path(f.name)

    try:
        # 格式化文件
        changed = formatter.apply_format(temp_file)
        if changed:
            print(f"文件已格式化: {temp_file}")

            # 读取格式化后的内容
            with open(temp_file, "r", encoding="utf-8") as f:
                formatted = f.read()

            print("格式化后的内容:")
            print(formatted)
        else:
            print("文件无需格式化")

    finally:
        # 清理临时文件
        if temp_file.exists():
            temp_file.unlink()

    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


def show_usage():
    """显示使用说明"""
    print("\n使用说明:")
    print("-" * 40)
    print("1. 格式化单个文件:")
    print("   python tools/xinyu_format.py --in-place 文件.xinyu")
    print("")
    print("2. 检查格式问题:")
    print("   python tools/xinyu_format.py --check 文件.xinyu")
    print("")
    print("3. 使用自定义配置:")
    print("   python tools/xinyu_format.py --config .xinyu-formatter.yaml 文件.xinyu")
    print("")
    print("4. 安装预提交钩子:")
    print("   pip install pre-commit")
    print("   pre-commit install")
    print("")
    print("5. 运行设置脚本:")
    print("   python tools/setup_formatter.py")


if __name__ == "__main__":
    demo_basic_formatting()
    show_usage()
