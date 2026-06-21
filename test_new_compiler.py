#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试新的编译器接口"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.compiler import XinyuCompiler


def test_compiler_basic():
    """测试基本编译功能"""
    print("测试基本编译功能...")

    compiler = XinyuCompiler(enable_safety=True)

    # 测试1: 简单打印语句
    source = '印"你好，世界！"。'
    print(f"源代码: {source}")

    try:
        result = compiler.compile(source)
        print(f"生成的Python代码:\n{result}")
        print("✓ 编译成功")
    except Exception as e:
        print(f"✗ 编译失败: {e}")
        return False

    # 测试2: 变量定义
    source2 = "定 x 为 42。印x。"
    print(f"\n源代码: {source2}")

    try:
        result2 = compiler.compile(source2)
        print(f"生成的Python代码:\n{result2}")
        print("✓ 编译成功")
    except Exception as e:
        print(f"✗ 编译失败: {e}")
        return False

    # 测试3: 错误处理
    source3 = "定 x 为 。"  # 语法错误
    print(f"\n源代码（有错误）: {source3}")

    try:
        compiler.compile(source3)
        if compiler.has_errors():
            print("检测到错误:")
            for diagnostic in compiler.get_diagnostics():
                print(f"  - {diagnostic}")
            print("✓ 错误检测成功")
        else:
            print("✗ 应该检测到错误但没有")
            return False
    except Exception as e:
        print(f"✗ 编译失败: {e}")
        return False

    return True


def test_compiler_execution():
    """测试编译和执行"""
    print("\n测试编译和执行...")

    compiler = XinyuCompiler(enable_safety=True)

    # 测试安全执行
    source = "定 x 为 10 加 20。印x。"
    print(f"源代码: {source}")

    try:
        result = compiler.execute(source)
        print(f"执行结果: {result}")
        print("✓ 执行成功")
    except Exception as e:
        print(f"✗ 执行失败: {e}")
        return False

    # 测试不安全代码（应该被阻止）
    unsafe_source = '__import__("os").system("echo dangerous")'
    print(f"\n不安全源代码: {unsafe_source}")

    try:
        result = compiler.execute(unsafe_source)
        print(f"执行结果: {result}")
        print("✗ 应该阻止不安全代码但没有")
        return False
    except Exception as e:
        print(f"✓ 安全阻止: {e}")

    return True


def test_compiler_validation():
    """测试代码验证"""
    print("\n测试代码验证...")

    compiler = XinyuCompiler(enable_safety=True)

    # 测试有效代码
    valid_source = "定 x 为 5。"
    print(f"有效源代码: {valid_source}")

    is_valid = compiler.validate(valid_source)
    print(f"验证结果: {'有效' if is_valid else '无效'}")

    if not is_valid:
        print("✗ 应该验证为有效但没有")
        return False

    # 测试无效代码
    invalid_source = "定 x 为 。"  # 语法错误
    print(f"\n无效源代码: {invalid_source}")

    is_valid = compiler.validate(invalid_source)
    print(f"验证结果: {'有效' if is_valid else '无效'}")

    if is_valid:
        print("✗ 应该验证为无效但没有")
        return False

    print("✓ 验证功能正常")
    return True


def main():
    """主测试函数"""
    print("=" * 60)
    print("测试新的编译器接口")
    print("=" * 60)

    tests = [
        ("基本编译功能", test_compiler_basic),
        ("编译和执行", test_compiler_execution),
        ("代码验证", test_compiler_validation),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            if test_func():
                print(f"✓ {test_name} 通过")
                passed += 1
            else:
                print(f"✗ {test_name} 失败")
        except Exception as e:
            print(f"✗ {test_name} 异常: {e}")

    print(f"\n{'='*60}")
    print(f"测试结果: {passed}/{total} 通过")

    if passed == total:
        print("✅ 所有测试通过！")
        return 0
    else:
        print("❌ 部分测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
