#!/usr/bin/env python3
"""
调试权限管理器
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.security import PermissionManager, PermissionType

def test_permission_debug():
    """调试权限管理器"""
    print("调试权限管理器...")
    
    # 创建权限管理器
    pm = PermissionManager()
    
    # 测试访客权限
    print("\n测试访客权限:")
    
    # 访客应该不能导入math模块
    result = pm.check_permission("guest", PermissionType.IMPORT, "math")
    print(f"访客导入math模块: {'允许' if result else '拒绝'} (预期: 拒绝)")
    
    # 检查访客的权限配置
    print("\n访客角色权限:")
    if "guest" in pm.roles:
        guest_role = pm.roles["guest"]
        for perm in guest_role.permissions:
            print(f"  资源: {perm.resource}, 操作: {[op.value for op in perm.operations]}")
    
    # 检查角色层次结构
    print("\n角色层次结构:")
    print(f"  {pm.role_hierarchy}")
    
    # 测试直接权限检查
    print("\n测试直接权限检查:")
    result = pm._has_direct_permission("guest", PermissionType.IMPORT, "math")
    print(f"访客直接导入math权限: {'有' if result else '无'}")
    
    # 测试通配符匹配
    print("\n测试通配符匹配:")
    import fnmatch
    test_cases = [
        ("math", "*.txt", "math匹配*.txt"),
        ("math.py", "*.py", "math.py匹配*.py"),
        ("math", "math", "math匹配math"),
        ("math", "*", "math匹配*"),
    ]
    
    for resource, pattern, description in test_cases:
        matches = fnmatch.fnmatch(resource, pattern)
        print(f"  {description}: {matches}")

if __name__ == "__main__":
    test_permission_debug()