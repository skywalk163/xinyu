"""
审计日志系统
记录所有权限检查操作
"""

import json
import logging
import logging.handlers
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

# 使用统一的日志工具
from src.utils.logging_utils import get_logger


class AuditLevel(Enum):
    """审计日志级别"""

    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class AuditEvent:
    """审计事件"""

    timestamp: str
    level: AuditLevel
    user: str
    role: str
    operation: str
    resource: str
    allowed: bool
    reason: Optional[str] = None
    source_ip: Optional[str] = None
    user_agent: Optional[str] = None
    session_id: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        data["level"] = self.level.value
        return data

    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False)


class AuditLogger:
    """审计日志器"""

    def __init__(self, log_file: str = "audit.log", max_size: int = 10 * 1024 * 1024):
        self.log_file = Path(log_file)
        self.max_size = max_size
        self.logger = None
        self._setup_logging()

        # 使用统一的日志工具
        self.unified_logger = get_logger("security.audit")

    def _setup_logging(self) -> None:
        """设置日志记录"""
        # 创建日志目录
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # 创建logger
        self.logger = logging.getLogger("audit")
        self.logger.setLevel(logging.INFO)

        # 清除现有处理器
        self.logger.handlers.clear()

        # 文件处理器，支持轮转
        file_handler = logging.handlers.RotatingFileHandler(
            self.log_file, maxBytes=self.max_size, backupCount=5, encoding="utf-8"
        )

        # 控制台处理器
        console_handler = logging.StreamHandler()

        # 设置格式
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 添加处理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log_event(self, event: AuditEvent) -> None:
        """记录审计事件"""
        log_message = event.to_json()

        if event.level == AuditLevel.INFO:
            self.logger.info(log_message)
        elif event.level == AuditLevel.WARNING:
            self.logger.warning(log_message)
        elif event.level == AuditLevel.ERROR:
            self.logger.error(log_message)
        elif event.level == AuditLevel.CRITICAL:
            self.logger.critical(log_message)

    def log_access(
        self,
        user: str,
        role: str,
        operation: str,
        resource: str,
        allowed: bool,
        reason: Optional[str] = None,
        level: AuditLevel = AuditLevel.INFO,
        source_ip: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None,
        additional_info: Optional[Dict[str, Any]] = None,
    ) -> None:
        """记录访问日志"""
        event = AuditEvent(
            timestamp=datetime.now().isoformat(),
            level=level,
            user=user,
            role=role,
            operation=operation,
            resource=resource,
            allowed=allowed,
            reason=reason,
            source_ip=source_ip,
            user_agent=user_agent,
            session_id=session_id,
            additional_info=additional_info,
        )

        self.log_event(event)

    def log_permission_check(
        self,
        user: str,
        role: str,
        operation: str,
        resource: str,
        allowed: bool,
        reason: Optional[str] = None,
    ) -> None:
        """记录权限检查日志"""
        level = AuditLevel.INFO if allowed else AuditLevel.WARNING
        self.log_access(
            user=user,
            role=role,
            operation=operation,
            resource=resource,
            allowed=allowed,
            reason=reason,
            level=level,
        )

    def log_security_event(
        self,
        user: str,
        event_type: str,
        description: str,
        severity: AuditLevel = AuditLevel.WARNING,
        source_ip: Optional[str] = None,
        additional_info: Optional[Dict[str, Any]] = None,
    ) -> None:
        """记录安全事件"""
        event = AuditEvent(
            timestamp=datetime.now().isoformat(),
            level=severity,
            user=user,
            role="system",
            operation=event_type,
            resource="security",
            allowed=False,
            reason=description,
            source_ip=source_ip,
            user_agent=None,
            session_id=None,
            additional_info=additional_info,
        )

        self.log_event(event)

    def get_audit_trail(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        user: Optional[str] = None,
        role: Optional[str] = None,
        operation: Optional[str] = None,
        allowed: Optional[bool] = None,
        level: Optional[AuditLevel] = None,
    ) -> List[AuditEvent]:
        """获取审计轨迹"""
        events = []

        try:
            if not self.log_file.exists():
                return events

            with open(self.log_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        # 解析日志行
                        # 格式: 时间戳 - 级别 - JSON消息
                        parts = line.split(" - ", 2)
                        if len(parts) != 3:
                            continue

                        timestamp_str, level_str, json_str = parts

                        # 解析JSON
                        data = json.loads(json_str)

                        # 创建事件对象
                        event = AuditEvent(
                            timestamp=data.get("timestamp", ""),
                            level=AuditLevel(data.get("level", "INFO")),
                            user=data.get("user", ""),
                            role=data.get("role", ""),
                            operation=data.get("operation", ""),
                            resource=data.get("resource", ""),
                            allowed=data.get("allowed", False),
                            reason=data.get("reason"),
                            source_ip=data.get("source_ip"),
                            user_agent=data.get("user_agent"),
                            session_id=data.get("session_id"),
                            additional_info=data.get("additional_info"),
                        )

                        # 应用过滤器
                        if start_time and datetime.fromisoformat(event.timestamp) < start_time:
                            continue
                        if end_time and datetime.fromisoformat(event.timestamp) > end_time:
                            continue
                        if user and event.user != user:
                            continue
                        if role and event.role != role:
                            continue
                        if operation and event.operation != operation:
                            continue
                        if allowed is not None and event.allowed != allowed:
                            continue
                        if level and event.level != level:
                            continue

                        events.append(event)

                    except (json.JSONDecodeError, ValueError):
                        # 跳过无法解析的行
                        continue

        except Exception as e:
            self.unified_logger.error(f"读取审计日志失败: {e}")

        return events

    def generate_report(
        self, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """生成审计报告"""
        events = self.get_audit_trail(start_time, end_time)

        if not events:
            return {"message": "没有审计事件"}

        # 统计信息
        total_events = len(events)
        allowed_events = sum(1 for e in events if e.allowed)
        denied_events = total_events - allowed_events

        # 按级别统计
        level_stats = {}
        for event in events:
            level = event.level.value
            level_stats[level] = level_stats.get(level, 0) + 1

        # 按操作统计
        operation_stats = {}
        for event in events:
            operation = event.operation
            operation_stats[operation] = operation_stats.get(operation, 0) + 1

        # 按用户统计
        user_stats = {}
        for event in events:
            user = event.user
            user_stats[user] = user_stats.get(user, 0) + 1

        # 按资源统计
        resource_stats = {}
        for event in events:
            resource = event.resource
            resource_stats[resource] = resource_stats.get(resource, 0) + 1

        # 最近事件
        recent_events = events[-10:] if len(events) > 10 else events

        return {
            "period": {
                "start": start_time.isoformat() if start_time else "开始",
                "end": end_time.isoformat() if end_time else "现在",
            },
            "summary": {
                "total_events": total_events,
                "allowed_events": allowed_events,
                "denied_events": denied_events,
                "allow_rate": allowed_events / total_events if total_events > 0 else 0,
            },
            "statistics": {
                "by_level": level_stats,
                "by_operation": operation_stats,
                "by_user": user_stats,
                "by_resource": resource_stats,
            },
            "recent_events": [e.to_dict() for e in recent_events],
        }

    def clear_logs(self) -> None:
        """清空审计日志"""
        try:
            if self.log_file.exists():
                self.log_file.unlink()
            self._setup_logging()
            self.unified_logger.info("审计日志已清空")
        except Exception as e:
            self.unified_logger.error(f"清空审计日志失败: {e}")

    def close(self) -> None:
        """关闭审计日志器"""
        if self.logger:
            for handler in self.logger.handlers[:]:
                handler.close()
                self.logger.removeHandler(handler)


class AuditedPermissionManager:
    """带审计的权限管理器"""

    def __init__(self, permission_manager, audit_logger: AuditLogger, user: str = "system"):
        self.permission_manager = permission_manager
        self.audit_logger = audit_logger
        self.user = user

    def check_permission(self, role: str, operation: str, resource: str) -> bool:
        """检查权限并记录审计日志"""
        # 检查权限
        from .permission_manager import PermissionType

        perm_type = PermissionType(operation) if isinstance(operation, str) else operation

        allowed = self.permission_manager.check_permission(role, perm_type, resource)

        # 记录审计日志
        reason = "权限检查通过" if allowed else "权限检查失败"
        self.audit_logger.log_permission_check(
            user=self.user,
            role=role,
            operation=operation.value if hasattr(operation, "value") else operation,
            resource=resource,
            allowed=allowed,
            reason=reason,
        )

        return allowed

    def set_user(self, user: str) -> None:
        """设置当前用户"""
        self.user = user

    def get_audit_report(self, **kwargs) -> Dict[str, Any]:
        """获取审计报告"""
        return self.audit_logger.generate_report(**kwargs)


def test_audit_logger():
    """测试审计日志器"""
    logger = get_logger("security.audit_test")
    logger.info("测试审计日志器...")

    # 创建审计日志器
    import os
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
        log_file = f.name

    try:
        audit_logger = AuditLogger(log_file=log_file)

        # 测试记录访问日志
        logger.info("1. 测试记录访问日志...")
        audit_logger.log_access(
            user="test_user",
            role="developer",
            operation="read",
            resource="/home/test.txt",
            allowed=True,
            reason="正常访问",
        )

        audit_logger.log_access(
            user="test_user",
            role="guest",
            operation="write",
            resource="/etc/passwd",
            allowed=False,
            reason="权限不足",
            level=AuditLevel.WARNING,
        )

        # 测试记录安全事件
        logger.info("2. 测试记录安全事件...")
        audit_logger.log_security_event(
            user="attacker",
            event_type="brute_force",
            description="检测到暴力破解尝试",
            severity=AuditLevel.ERROR,
            source_ip="192.168.1.100",
        )

        # 测试获取审计轨迹
        logger.info("3. 测试获取审计轨迹...")
        events = audit_logger.get_audit_trail()
        logger.info(f"  记录的事件数量: {len(events)}")
        for event in events:
            logger.debug(
                f"  - {event.timestamp} {event.user} {event.operation} {event.resource} {'允许' if event.allowed else '拒绝'}"
            )

        # 测试生成报告
        logger.info("4. 测试生成审计报告...")
        report = audit_logger.generate_report()
        logger.info(f"  总事件数: {report['summary']['total_events']}")
        logger.info(f"  允许事件: {report['summary']['allowed_events']}")
        logger.info(f"  拒绝事件: {report['summary']['denied_events']}")

        return True

    finally:
        # 清理临时文件
        if os.path.exists(log_file):
            os.unlink(log_file)


if __name__ == "__main__":
    # 运行测试
    logger = get_logger("security.audit_main")
    if test_audit_logger():
        logger.info("审计日志器测试通过!")
    else:
        logger.error("审计日志器测试失败!")
