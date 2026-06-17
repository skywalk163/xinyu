"""
权限管理器
基于角色的权限控制系统
"""

import fnmatch
from typing import Dict, List, Set, Any, Optional
from enum import Enum
from dataclasses import dataclass
from pathlib import Path

# 使用统一的导入工具
from src.utils.imports import import_optional
from src.utils.config_utils import ConfigManager

# 导入可选模块
yaml = import_optional('yaml')


class PermissionType(Enum):
    """权限类型枚举"""
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    IMPORT = "import"
    NETWORK = "network"
    SYSTEM = "system"
    ALL = "all"


@dataclass
class Permission:
    """权限定义"""
    resource: str  # 资源路径，支持通配符
    operations: List[PermissionType]  # 允许的操作
    description: str = ""  # 权限描述


@dataclass
class Role:
    """角色定义"""
    name: str  # 角色名称
    permissions: List[Permission]  # 角色权限
    parent_roles: List[str] = None  # 父角色列表
    
    def __post_init__(self):
        if self.parent_roles is None:
            self.parent_roles = []


class PermissionManager:
    """权限管理器"""
    
    def __init__(self, policy_file: str = "security_policy.yaml"):
        self.policy_file = policy_file
        self.roles: Dict[str, Role] = {}
        self.role_hierarchy: Dict[str, List[str]] = {}
        self.permission_cache: Dict[str, Set[str]] = {}
        
        # 使用统一的日志工具
        from src.utils.logging_utils import get_logger
        self.logger = get_logger("security.permission_manager")
        
        self._load_policy()
        
    def _load_policy(self) -> None:
        """加载安全策略"""
        try:
            # 使用统一的配置工具
            config_manager = ConfigManager(self.policy_file)
            
            if config_manager.file_exists():
                # 加载配置
                if config_manager.load():
                    # 获取配置数据
                    policy_data = config_manager.get_config()
                    self._parse_policy(policy_data)
                else:
                    self.logger.warning(f"配置文件加载失败: {self.policy_file}")
                    self._create_default_policy()
            else:
                # 使用默认策略
                self.logger.info(f"配置文件不存在，创建默认策略: {self.policy_file}")
                self._create_default_policy()
                self._save_policy()
                
        except Exception as e:
            self.logger.error(f"加载安全策略失败: {e}")
            self._create_default_policy()
            
    def _parse_policy(self, policy_data: Dict[str, Any]) -> None:
        """解析策略数据"""
        # 解析角色
        self.roles.clear()
        for role_name, role_data in policy_data.get("roles", {}).items():
            permissions = []
            for perm_data in role_data.get("permissions", []):
                perm = Permission(
                    resource=perm_data.get("resource", ""),
                    operations=[PermissionType(op) for op in perm_data.get("operations", [])],
                    description=perm_data.get("description", "")
                )
                permissions.append(perm)
                
            role = Role(
                name=role_name,
                permissions=permissions,
                parent_roles=role_data.get("parent_roles", [])
            )
            self.roles[role_name] = role
            
        # 解析角色层次结构
        self.role_hierarchy = policy_data.get("role_hierarchy", {})
        
    def _create_default_policy(self) -> None:
        """创建默认安全策略"""
        # 定义默认角色
        admin_role = Role(
            name="admin",
            permissions=[
                Permission("*", [PermissionType.ALL], "管理员拥有所有权限"),
            ],
            parent_roles=[]
        )
        
        developer_role = Role(
            name="developer",
            permissions=[
                Permission("/home/*", [PermissionType.READ, PermissionType.WRITE], "开发者可以读写home目录"),
                Permission("/tmp/*", [PermissionType.READ, PermissionType.WRITE, PermissionType.EXECUTE], "开发者可以读写执行tmp目录"),
                Permission("*.py", [PermissionType.READ, PermissionType.EXECUTE], "开发者可以执行Python文件"),
                Permission("http://api.example.com/*", [PermissionType.NETWORK], "开发者可以访问示例API"),
            ],
            parent_roles=[]
        )
        
        user_role = Role(
            name="user",
            permissions=[
                Permission("/home/user/*", [PermissionType.READ, PermissionType.WRITE], "用户可以读写自己的home目录"),
                Permission("*.txt", [PermissionType.READ], "用户可以读取文本文件"),
                Permission("math", [PermissionType.IMPORT], "用户可以导入math模块"),
                Permission("datetime", [PermissionType.IMPORT], "用户可以导入datetime模块"),
            ],
            parent_roles=[]
        )
        
        guest_role = Role(
            name="guest",
            permissions=[
                Permission("/tmp/*", [PermissionType.READ], "访客可以读取tmp目录"),
                Permission("*.txt", [PermissionType.READ], "访客可以读取文本文件"),
            ],
            parent_roles=[]
        )
        
        self.roles = {
            "admin": admin_role,
            "developer": developer_role,
            "user": user_role,
            "guest": guest_role,
        }
        
        # 定义角色层次结构
        self.role_hierarchy = {
            "developer": ["user"],
            "user": ["guest"],
        }
        
    def _save_policy(self) -> None:
        """保存安全策略"""
        try:
            policy_data = {
                "roles": {},
                "role_hierarchy": self.role_hierarchy
            }
            
            for role_name, role in self.roles.items():
                role_data = {
                    "permissions": [],
                    "parent_roles": role.parent_roles
                }
                
                for perm in role.permissions:
                    perm_data = {
                        "resource": perm.resource,
                        "operations": [op.value for op in perm.operations],
                        "description": perm.description
                    }
                    role_data["permissions"].append(perm_data)
                    
                policy_data["roles"][role_name] = role_data
                
            # 使用统一的配置工具
            config_manager = ConfigManager(self.policy_file)
            config_manager.save(policy_data)
                
        except Exception as e:
            self.logger.error(f"保存安全策略失败: {e}")
            
    def check_permission(self, role: str, operation: PermissionType, resource: str) -> bool:
        """检查角色是否有权限执行操作
        
        Args:
            role: 角色名称
            operation: 操作类型
            resource: 资源路径
            
        Returns:
            是否有权限
        """
        # 检查直接权限
        if self._has_direct_permission(role, operation, resource):
            return True
            
        # 检查继承权限
        if role in self.role_hierarchy:
            for parent_role in self.role_hierarchy[role]:
                if self.check_permission(parent_role, operation, resource):
                    return True
                    
        return False
        
    def _has_direct_permission(self, role: str, operation: PermissionType, resource: str) -> bool:
        """检查直接权限"""
        if role not in self.roles:
            return False
            
        role_obj = self.roles[role]
        
        for perm in role_obj.permissions:
            if self._match_permission(perm, operation, resource):
                return True
                
        return False
        
    def _match_permission(self, permission: Permission, operation: PermissionType, resource: str) -> bool:
        """检查权限是否匹配"""
        # 检查操作匹配
        if PermissionType.ALL not in permission.operations and operation not in permission.operations:
            return False
            
        # 检查资源匹配（支持通配符）
        return fnmatch.fnmatch(resource, permission.resource)
        
    def add_role(self, role: Role) -> bool:
        """添加角色"""
        if role.name in self.roles:
            self.logger.warning(f"角色 {role.name} 已存在")
            return False
            
        self.roles[role.name] = role
        self._save_policy()
        return True
        
    def remove_role(self, role_name: str) -> bool:
        """移除角色"""
        if role_name not in self.roles:
            self.logger.warning(f"角色 {role_name} 不存在")
            return False
            
        # 检查是否有其他角色继承此角色
        for child_role, parents in self.role_hierarchy.items():
            if role_name in parents:
                self.logger.warning(f"角色 {role_name} 被 {child_role} 继承，无法删除")
                return False
                
        del self.roles[role_name]
        
        # 从层次结构中移除
        if role_name in self.role_hierarchy:
            del self.role_hierarchy[role_name]
            
        # 从其他角色的父角色中移除
        for child_role in self.role_hierarchy:
            if role_name in self.role_hierarchy[child_role]:
                self.role_hierarchy[child_role].remove(role_name)
                
        self._save_policy()
        return True
        
    def add_permission(self, role_name: str, permission: Permission) -> bool:
        """为角色添加权限"""
        if role_name not in self.roles:
            self.logger.warning(f"角色 {role_name} 不存在")
            return False
            
        self.roles[role_name].permissions.append(permission)
        self._save_policy()
        return True
        
    def remove_permission(self, role_name: str, resource: str, operation: PermissionType) -> bool:
        """从角色移除权限"""
        if role_name not in self.roles:
            self.logger.warning(f"角色 {role_name} 不存在")
            return False
            
        role = self.roles[role_name]
        
        # 查找并移除权限
        for i, perm in enumerate(role.permissions):
            if perm.resource == resource and operation in perm.operations:
                # 移除操作
                perm.operations.remove(operation)
                
                # 如果权限没有操作了，移除整个权限
                if not perm.operations:
                    del role.permissions[i]
                    
                self._save_policy()
                return True
                
        self.logger.warning(f"角色 {role_name} 没有对资源 {resource} 的 {operation.value} 权限")
        return False
        
    def add_role_inheritance(self, child_role: str, parent_role: str) -> bool:
        """添加角色继承关系"""
        if child_role not in self.roles:
            self.logger.warning(f"子角色 {child_role} 不存在")
            return False
            
        if parent_role not in self.roles:
            self.logger.warning(f"父角色 {parent_role} 不存在")
            return False
            
        # 检查循环继承
        if self._has_inheritance_cycle(child_role, parent_role):
            self.logger.warning(f"添加继承关系会导致循环继承")
            return False
            
        if child_role not in self.role_hierarchy:
            self.role_hierarchy[child_role] = []
            
        if parent_role not in self.role_hierarchy[child_role]:
            self.role_hierarchy[child_role].append(parent_role)
            
        self._save_policy()
        return True
        
    def _has_inheritance_cycle(self, start_role: str, target_role: str) -> bool:
        """检查是否有循环继承"""
        visited = set()
        
        def dfs(role: str) -> bool:
            if role == start_role:
                return True
                
            if role in visited:
                return False
                
            visited.add(role)
            
            if role in self.role_hierarchy:
                for parent in self.role_hierarchy[role]:
                    if dfs(parent):
                        return True
                        
            return False
            
        return dfs(target_role)
        
    def get_role_permissions(self, role_name: str) -> List[Dict[str, Any]]:
        """获取角色的所有权限（包括继承的）"""
        if role_name not in self.roles:
            return []
            
        permissions = []
        visited_roles = set()
        
        def collect_permissions(role: str):
            if role in visited_roles:
                return
                
            visited_roles.add(role)
            
            # 添加当前角色的权限
            if role in self.roles:
                for perm in self.roles[role].permissions:
                    permissions.append({
                        "role": role,
                        "resource": perm.resource,
                        "operations": [op.value for op in perm.operations],
                        "description": perm.description,
                        "inherited": role != role_name
                    })
                    
            # 递归收集父角色的权限
            if role in self.role_hierarchy:
                for parent in self.role_hierarchy[role]:
                    collect_permissions(parent)
                    
        collect_permissions(role_name)
        return permissions
        
    def list_roles(self) -> List[str]:
        """列出所有角色"""
        return list(self.roles.keys())
        
    def get_role_hierarchy(self) -> Dict[str, List[str]]:
        """获取角色层次结构"""
        return self.role_hierarchy.copy()
        
    def validate_resource_access(self, role: str, operation: PermissionType, resource: str) -> Dict[str, Any]:
        """验证资源访问权限，返回详细结果"""
        has_permission = self.check_permission(role, operation, resource)
        
        result = {
            "allowed": has_permission,
            "role": role,
            "operation": operation.value,
            "resource": resource,
            "matching_permissions": []
        }
        
        if has_permission:
            # 查找匹配的权限
            all_permissions = self.get_role_permissions(role)
            for perm in all_permissions:
                if fnmatch.fnmatch(resource, perm["resource"]):
                    if operation.value in perm["operations"] or "all" in perm["operations"]:
                        result["matching_permissions"].append(perm)
                        
        return result