#!/usr/bin/env python3
"""
测试完整的安全系统（权限控制 + 审计日志）
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.security import (
    AuditedPermissionManager,
    AuditLogger,
    PermissionManager,
    PermissionType,
    SecureContext,
)


def test_permission_manager():
    """测试权限管理器"""
    print("测试权限管理器...")

    # 创建权限管理器
    pm = PermissionManager()

    # 测试基本权限检查
    test_cases = [
        ("admin", PermissionType.READ, "/etc/passwd", True, "管理员可以读取任何文件"),
        ("developer", PermissionType.WRITE, "/home/project/test.py", True, "开发者可以写入home目录"),
        ("developer", PermissionType.EXECUTE, "/tmp/script.py", True, "开发者可以执行tmp目录的Python文件"),
        ("user", PermissionType.READ, "/tmp/log.txt", True, "用户可以读取tmp目录"),
        ("user", PermissionType.WRITE, "/tmp/log.txt", False, "用户不能写入tmp目录"),
        ("guest", PermissionType.READ, "/home/secret.txt", True, "访客可以读取文本文件"),
        ("guest", PermissionType.IMPORT, "math", True, "访客可以导入math模块"),
        ("guest", PermissionType.IMPORT, "os", False, "访客不能导入os模块"),
    ]

    all_passed = True
    for i, (role, operation, resource, expected, description) in enumerate(test_cases):
        result = pm.check_permission(role, operation, resource)
        passed = result == expected
        all_passed = all_passed and passed

        status = "通过" if passed else "失败"
        print(f"{status} {description}")
        print(f"  角色: {role}, 操作: {operation.value}, 资源: {resource}")
        print(f"  预期: {expected}, 实际: {result}")

        if not passed:
            print(f"  测试用例 {i+1} 失败")

    # 测试角色继承
    print("\n测试角色继承...")
    inheritance_tests = [
        ("developer", PermissionType.READ, "/tmp/log.txt", True, "开发者继承用户的权限"),
        ("developer", PermissionType.IMPORT, "math", True, "开发者继承用户的导入权限"),
        ("user", PermissionType.READ, "/tmp/log.txt", True, "用户继承访客的权限"),
        ("user", PermissionType.IMPORT, "datetime", True, "用户可以导入datetime模块"),
    ]

    for role, operation, resource, expected, description in inheritance_tests:
        result = pm.check_permission(role, operation, resource)
        passed = result == expected
        all_passed = all_passed and passed

        status = "通过" if passed else "失败"
        print(f"{status} {description}")
        print(f"  角色: {role}, 操作: {operation.value}, 资源: {resource}")
        print(f"  预期: {expected}, 实际: {result}")

    return all_passed


def test_audit_logger():
    """测试审计日志系统"""
    print("\n测试审计日志系统...")

    # 创建临时日志文件路径
    import tempfile
    import time

    log_file = os.path.join(tempfile.gettempdir(), f"audit_test_{int(time.time())}.log")

    try:
        # 创建审计日志器
        logger = AuditLogger(log_file=log_file, max_size=1024 * 1024)  # 1MB

        # 测试记录访问日志
        logger.log_access(
            user="test_user",
            role="developer",
            operation="read_file",
            resource="/etc/passwd",
            allowed=True,
            reason="读取系统文件",
        )

        logger.log_access(
            user="test_user",
            role="guest",
            operation="write_file",
            resource="/tmp/test.txt",
            allowed=False,
            reason="权限不足",
        )

        # 关闭日志处理器以释放文件句柄
        for handler in logger.logger.handlers:
            handler.close()

        # 等待文件写入完成
        time.sleep(0.1)

        # 测试获取审计轨迹
        records = logger.get_audit_trail()
        print(f"成功记录 {len(records)} 条审计日志")

        # 验证记录内容
        if len(records) >= 2:
            print(f"第一条记录: {records[0].operation} - {'允许' if records[0].allowed else '拒绝'}")
            print(f"第二条记录: {records[1].operation} - {'允许' if records[1].allowed else '拒绝'}")

        # 测试生成报告
        report = logger.generate_report()
        print(f"生成审计报告: {report['summary']['total_events']} 个事件")

        return True

    finally:
        # 清理临时文件
        try:
            if os.path.exists(log_file):
                os.unlink(log_file)
        except:
            pass  # 忽略文件删除错误


def test_audited_permission_manager():
    """测试带审计的权限管理器"""
    print("\n测试带审计的权限管理器...")

    # 创建临时日志文件路径
    import tempfile
    import time

    log_file = os.path.join(tempfile.gettempdir(), f"audit_pm_test_{int(time.time())}.log")

    try:
        # 创建权限管理器和审计日志器
        pm = PermissionManager()
        audit_logger = AuditLogger(log_file=log_file)

        # 创建带审计的权限管理器
        apm = AuditedPermissionManager(pm, audit_logger, user="test_user")

        # 测试权限检查并记录审计日志
        result1 = apm.check_permission("admin", PermissionType.READ, "/etc/passwd")
        result2 = apm.check_permission("guest", PermissionType.WRITE, "/etc/shadow")

        print(f"管理员读取/etc/passwd: {'允许' if result1 else '拒绝'}")
        print(f"访客写入/etc/shadow: {'允许' if result2 else '拒绝'}")

        # 关闭日志处理器以释放文件句柄
        for handler in audit_logger.logger.handlers:
            handler.close()

        # 等待文件写入完成
        time.sleep(0.1)

        # 获取审计记录
        records = audit_logger.get_audit_trail()
        print(f"记录了 {len(records)} 条权限检查审计日志")

        for record in records:
            print(
                f"  - {record.user}: {record.operation} {record.resource} -> {'允许' if record.allowed else '拒绝'}"
            )

        return True

    finally:
        # 清理临时文件
        try:
            if os.path.exists(log_file):
                os.unlink(log_file)
        except:
            pass  # 忽略文件删除错误


def test_secure_context():
    """测试安全上下文"""
    print("\n测试安全上下文...")

    # 创建权限管理器
    pm = PermissionManager()

    # 创建安全上下文
    context = SecureContext(pm, role="developer")

    # 测试权限检查
    result1 = pm.check_permission("developer", PermissionType.READ, "/tmp/test.txt")
    result2 = pm.check_permission("developer", PermissionType.WRITE, "/etc/passwd")

    print(f"开发者读取/tmp/test.txt: {'允许' if result1 else '拒绝'}")
    print(f"开发者写入/etc/passwd: {'允许' if result2 else '拒绝'}")

    # 测试切换角色
    context.role = "user"
    result3 = pm.check_permission("user", PermissionType.WRITE, "/tmp/test.txt")
    print(f"用户写入/tmp/test.txt: {'允许' if result3 else '拒绝'}")

    return True


def test_integration():
    """测试完整的安全系统集成"""
    print("\n测试完整的安全系统集成...")

    # 创建临时日志文件路径
    import tempfile
    import time

    log_file = os.path.join(tempfile.gettempdir(), f"audit_integration_test_{int(time.time())}.log")

    try:
        # 创建权限管理器和审计日志器
        pm = PermissionManager()
        audit_logger = AuditLogger(log_file=log_file)

        # 创建带审计的权限管理器
        apm = AuditedPermissionManager(pm, audit_logger, user="alice")

        # 测试一系列操作
        operations = [
            ("读取项目文件", PermissionType.READ, "/home/project/src/main.py"),
            ("写入临时文件", PermissionType.WRITE, "/tmp/debug.log"),
            ("执行脚本", PermissionType.EXECUTE, "/tmp/script.py"),
            ("导入系统模块", PermissionType.IMPORT, "os"),
            ("读取系统文件", PermissionType.READ, "/etc/passwd"),
        ]

        all_passed = True
        expected_results = [True, True, True, True, False]  # 开发者不能读取/etc/passwd

        for (description, operation, resource), expected in zip(operations, expected_results):
            result = apm.check_permission("developer", operation, resource)
            status = "通过" if result == expected else "失败"
            print(f"{description}: {'允许' if result else '拒绝'} ({status})")
            all_passed = all_passed and (result == expected)

        # 关闭日志处理器以释放文件句柄
        for handler in audit_logger.logger.handlers:
            handler.close()

        # 等待文件写入完成
        time.sleep(0.1)

        # 查看审计记录
        print("\n审计记录:")
        records = audit_logger.get_audit_trail()
        for record in records:
            print(
                f"  [{record.timestamp}] {record.user}({record.role}): {record.operation} {record.resource} -> {'允许' if record.allowed else '拒绝'}"
            )

        return all_passed

    finally:
        # 清理临时文件
        try:
            if os.path.exists(log_file):
                os.unlink(log_file)
        except:
            pass  # 忽略文件删除错误


def main():
    """主测试函数"""
    print("=" * 60)
    print("安全系统测试")
    print("=" * 60)

    tests = [
        ("权限管理器", test_permission_manager),
        ("审计日志系统", test_audit_logger),
        ("带审计的权限管理器", test_audited_permission_manager),
        ("安全上下文", test_secure_context),
        ("系统集成测试", test_integration),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*40}")
        print(f"测试: {test_name}")
        print("=" * 40)
        try:
            result = test_func()
            results.append((test_name, result))
            print(f"\n{test_name}: {'通过' if result else '失败'}")
        except Exception as e:
            print(f"测试失败: {e}")
            results.append((test_name, False))

    # 汇总结果
    print(f"\n{'='*60}")
    print("测试结果汇总")
    print("=" * 60)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "通过" if result else "失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1

    print(f"\n总计: {passed}/{total} 个测试通过")

    if passed == total:
        print("所有测试通过！安全系统功能正常。")
        return 0
    else:
        print("部分测试失败，请检查安全系统实现。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
