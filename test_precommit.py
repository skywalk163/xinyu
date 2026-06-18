#!/usr/bin/env python3
"""
测试预提交钩子管理器
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.precommit_hook import PreCommitHook


def test_precommit_hook():
    """测试预提交钩子管理器"""
    print("测试预提交钩子管理器...")

    # 创建钩子管理器
    hook_manager = PreCommitHook()

    # 测试格式化检查
    print("\n1. 测试代码格式化检查...")
    test_files = ["src/precommit_hook.py", "test_precommit.py"]
    result = hook_manager.format_code(test_files)
    print(f"格式化检查结果: {'通过' if result else '失败'}")

    # 测试类型检查
    print("\n2. 测试类型检查...")
    result = hook_manager.type_check(["src/precommit_hook.py"])
    print(f"类型检查结果: {'通过' if result else '失败'}")

    # 测试代码质量检查
    print("\n3. 测试代码质量检查...")
    result = hook_manager.check_code_quality(test_files)
    print(f"代码质量检查结果: {'通过' if result else '失败'}")

    # 测试安全扫描
    print("\n4. 测试安全扫描...")
    result = hook_manager.security_scan(["src/"])
    print(f"安全扫描结果: {'通过' if result else '失败'}")

    # 测试单元测试
    print("\n5. 测试单元测试...")
    result = hook_manager.run_tests()
    print(f"单元测试结果: {'通过' if result else '失败'}")

    print("\n所有测试完成!")


if __name__ == "__main__":
    test_precommit_hook()
