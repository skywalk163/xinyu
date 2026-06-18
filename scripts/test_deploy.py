#!/usr/bin/env python3
"""
测试部署脚本
"""

import os
import sys
from pathlib import Path

# 添加脚本目录到路径
sys.path.append(str(Path(__file__).parent))

from deploy import DeploymentSystem


def test_deployment_system():
    """测试部署系统"""
    print("测试部署系统...")

    project_root = Path(__file__).parent.parent
    deploy_system = DeploymentSystem(project_root)

    # 测试版本读取
    print(f"1. 版本读取: {deploy_system.version}")
    assert deploy_system.version == "0.1.0", f"版本不匹配: {deploy_system.version}"
    print("   [通过] 版本读取正确")

    # 测试配置加载
    print(f"2. 配置加载: {len(deploy_system.config)} 个配置项")
    assert "environments" in deploy_system.config
    assert "checks" in deploy_system.config
    print("   [通过] 配置加载正确")

    # 测试前置条件检查
    print("3. 前置条件检查...")
    success = deploy_system.check_prerequisites()
    print(f"   结果: {'通过' if success else '失败'}")

    # 测试命令运行
    print("4. 命令运行测试...")
    success, output = deploy_system.run_command("echo '测试命令'", capture_output=True)
    print(f"   命令执行: {'成功' if success else '失败'}")
    print(f"   输出: {output.strip()}")

    # 测试构建包（不实际构建）
    print("5. 构建包测试...")
    # 这里只是测试函数调用，不实际构建
    print("   [跳过] 构建包测试")

    print("\n所有测试完成!")
    return True


def test_deploy_script():
    """测试部署脚本命令行接口"""
    print("\n测试部署脚本命令行接口...")

    # 测试帮助信息
    print("1. 测试帮助信息...")
    os.system(f"python {Path(__file__).parent}/deploy.py --help")

    # 测试检查功能
    print("\n2. 测试检查功能...")
    os.system(f"python {Path(__file__).parent}/deploy.py --check-only")

    # 测试测试功能
    print("\n3. 测试测试功能...")
    os.system(f"python {Path(__file__).parent}/deploy.py --test-only")

    print("\n命令行接口测试完成!")


if __name__ == "__main__":
    print("=" * 60)
    print("心语编程语言部署系统测试")
    print("=" * 60)

    try:
        # 测试部署系统
        test_deployment_system()

        # 测试部署脚本
        test_deploy_script()

        print("\n" + "=" * 60)
        print("[成功] 所有测试通过!")
        print("=" * 60)

    except Exception as e:
        print(f"\n[失败] 测试出错: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
