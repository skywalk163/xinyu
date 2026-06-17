"""
权限检查拦截器
拦截系统调用并检查权限
"""

import builtins
import os
import sys
from typing import Any, Callable, Dict, List, Optional

# 使用统一的日志工具
from src.utils.logging_utils import get_logger

from .permission_manager import PermissionManager, PermissionType


class PermissionInterceptor:
    """权限检查拦截器"""

    def __init__(self, permission_manager: PermissionManager, role: str = "user"):
        self.permission_manager = permission_manager
        self.role = role
        self.original_open = None
        self.original_import = None
        self.original_socket = None

        # 使用统一的日志工具
        self.logger = get_logger("security.permission_interceptor")
        self.original_subprocess = None
        self.intercepted = False

    def intercept(self) -> None:
        """开始拦截系统调用"""
        if self.intercepted:
            return

        # 保存原始函数
        self.original_open = builtins.open
        self.original_import = builtins.__import__

        # 拦截文件操作
        builtins.open = self._intercept_open

        # 拦截导入操作
        builtins.__import__ = self._intercept_import

        # 拦截网络操作（需要时再实现）
        # 拦截系统调用（需要时再实现）

        self.intercepted = True
        self.logger.info(f"权限拦截已启用，角色: {self.role}")

    def restore(self) -> None:
        """恢复原始系统调用"""
        if not self.intercepted:
            return

        # 恢复原始函数
        if self.original_open:
            builtins.open = self.original_open

        if self.original_import:
            builtins.__import__ = self.original_import

        self.intercepted = False
        self.logger.info("权限拦截已禁用")

    def _intercept_open(self, file, mode="r", *args, **kwargs):
        """拦截文件打开操作"""
        # 解析操作类型
        operation = self._get_file_operation(mode)

        # 检查权限
        if not self.permission_manager.check_permission(self.role, operation, str(file)):
            raise PermissionError(f"角色 '{self.role}' 没有权限以 '{mode}' 模式访问文件 '{file}'")

        # 调用原始函数
        return self.original_open(file, mode, *args, **kwargs)

    def _intercept_import(self, name, *args, **kwargs):
        """拦截模块导入操作"""
        # 检查权限
        if not self.permission_manager.check_permission(self.role, PermissionType.IMPORT, name):
            raise ImportError(f"角色 '{self.role}' 没有权限导入模块 '{name}'")

        # 调用原始函数
        return self.original_import(name, *args, **kwargs)

    def _get_file_operation(self, mode: str) -> PermissionType:
        """根据文件模式获取操作类型"""
        if "r" in mode:
            return PermissionType.READ
        elif "w" in mode or "a" in mode or "x" in mode:
            return PermissionType.WRITE
        elif "+" in mode:
            return PermissionType.READ | PermissionType.WRITE
        else:
            return PermissionType.READ

    def check_file_access(self, path: str, operation: PermissionType) -> bool:
        """检查文件访问权限"""
        return self.permission_manager.check_permission(self.role, operation, path)

    def check_module_import(self, module_name: str) -> bool:
        """检查模块导入权限"""
        return self.permission_manager.check_permission(
            self.role, PermissionType.IMPORT, module_name
        )

    def check_network_access(self, url: str) -> bool:
        """检查网络访问权限"""
        return self.permission_manager.check_permission(self.role, PermissionType.NETWORK, url)

    def check_system_call(self, command: str) -> bool:
        """检查系统调用权限"""
        return self.permission_manager.check_permission(self.role, PermissionType.SYSTEM, command)

    def set_role(self, role: str) -> None:
        """设置当前角色"""
        if role not in self.permission_manager.list_roles():
            raise ValueError(f"角色 '{role}' 不存在")

        self.role = role
        self.logger.info(f"角色已切换为: {role}")

    def get_current_role(self) -> str:
        """获取当前角色"""
        return self.role

    def get_role_permissions(self) -> List[Dict[str, Any]]:
        """获取当前角色的所有权限"""
        return self.permission_manager.get_role_permissions(self.role)

    def validate_access(self, operation: PermissionType, resource: str) -> Dict[str, Any]:
        """验证访问权限，返回详细结果"""
        return self.permission_manager.validate_resource_access(self.role, operation, resource)


class SecureContext:
    """安全上下文管理器"""

    def __init__(self, permission_manager: PermissionManager, role: str = "user"):
        self.permission_manager = permission_manager
        self.role = role
        self.interceptor = None

    def __enter__(self):
        """进入安全上下文"""
        self.interceptor = PermissionInterceptor(self.permission_manager, self.role)
        self.interceptor.intercept()
        return self.interceptor

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出安全上下文"""
        if self.interceptor:
            self.interceptor.restore()

    @classmethod
    def create(cls, role: str = "user", policy_file: str = "security_policy.yaml"):
        """创建安全上下文"""
        permission_manager = PermissionManager(policy_file)
        return cls(permission_manager, role)


def test_permission_system():
    """测试权限系统"""
    logger = get_logger("security.test")
    logger.info("测试权限系统...")

    # 创建权限管理器
    pm = PermissionManager()

    # 测试权限检查
    test_cases = [
        ("admin", PermissionType.READ, "/etc/passwd", True, "管理员可以读取任何文件"),
        ("developer", PermissionType.WRITE, "/home/test.txt", True, "开发者可以写入home目录"),
        ("developer", PermissionType.EXECUTE, "/tmp/script.py", True, "开发者可以执行tmp目录的Python文件"),
        ("user", PermissionType.READ, "/tmp/test.txt", True, "用户可以读取tmp目录"),
        ("user", PermissionType.WRITE, "/tmp/test.txt", False, "用户不能写入tmp目录"),
        ("guest", PermissionType.READ, "/home/secret.txt", False, "访客不能读取home目录"),
        ("guest", PermissionType.IMPORT, "math", True, "访客可以导入math模块"),
        ("guest", PermissionType.IMPORT, "os", False, "访客不能导入os模块"),
    ]

    all_passed = True
    for role, operation, resource, expected, description in test_cases:
        result = pm.check_permission(role, operation, resource)
        passed = result == expected
        all_passed = all_passed and passed

        status = "✓" if passed else "✗"
        if passed:
            logger.info(f"{status} {description}")
        else:
            logger.error(f"{status} {description}")
        logger.debug(f"  角色: {role}, 操作: {operation.value}, 资源: {resource}")
        logger.debug(f"  预期: {expected}, 实际: {result}")

    return all_passed


if __name__ == "__main__":
    # 运行测试
    logger = get_logger("security.permission_test")
    if test_permission_system():
        logger.info("所有权限测试通过!")
    else:
        logger.error("部分权限测试失败!")
