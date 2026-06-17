#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""增强的REPL历史记录管理器

支持历史记录的搜索、编辑、持久化存储和导入导出功能。
"""

import gzip
import json
import pickle
import sqlite3
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class CommandType(str, Enum):
    """命令类型枚举"""

    EXPRESSION = "expression"  # 表达式求值
    STATEMENT = "statement"  # 语句执行
    DEFINITION = "definition"  # 定义（函数、变量等）
    IMPORT = "import"  # 导入语句
    CONTROL = "control"  # 控制语句（if、for等）
    DEBUG = "debug"  # 调试命令
    HELP = "help"  # 帮助命令
    OTHER = "other"  # 其他命令


@dataclass
class HistoryEntry:
    """历史记录条目"""

    timestamp: datetime
    command: str
    result: Optional[str] = None
    command_type: CommandType = CommandType.OTHER
    execution_time: Optional[float] = None  # 执行时间（秒）
    success: bool = True
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        data["command_type"] = self.command_type.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HistoryEntry":
        """从字典创建"""
        data = data.copy()
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        data["command_type"] = CommandType(data["command_type"])
        return cls(**data)


class HistoryManager:
    """增强的历史记录管理器"""

    def __init__(
        self, max_size: int = 1000, history_file: Optional[Path] = None, use_database: bool = False
    ):
        """初始化历史记录管理器

        Args:
            max_size: 最大历史记录数量
            history_file: 历史记录文件路径
            use_database: 是否使用SQLite数据库存储
        """
        self.max_size = max_size
        self.history_file = history_file or Path.home() / ".xinyu_history"
        self.use_database = use_database
        self.history: List[HistoryEntry] = []

        # 初始化存储
        if use_database:
            self._init_database()
        else:
            self._load_history()

    def _init_database(self) -> None:
        """初始化数据库"""
        db_path = self.history_file.with_suffix(".db")
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        # 创建历史记录表
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                command TEXT NOT NULL,
                result TEXT,
                command_type TEXT NOT NULL,
                execution_time REAL,
                success INTEGER NOT NULL,
                tags TEXT,
                metadata TEXT
            )
        """
        )

        # 创建索引
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON history(timestamp)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_command_type ON history(command_type)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_tags ON history(tags)")

        self.conn.commit()

    def _detect_command_type(self, command: str) -> CommandType:
        """检测命令类型"""
        command = command.strip()

        if not command:
            return CommandType.OTHER

        # 检查是否为表达式（以值结尾）
        if (
            command.startswith("计算")
            or command.startswith("求值")
            or command.replace(" ", "").replace("\t", "").replace("\n", "").isdigit()
            or command.startswith('"')
            or command.startswith("'")
        ):
            return CommandType.EXPRESSION

        # 检查是否为定义
        if command.startswith("定义") or command.startswith("变量") or command.startswith("函数"):
            return CommandType.DEFINITION

        # 检查是否为导入
        if command.startswith("导入") or command.startswith("从"):
            return CommandType.IMPORT

        # 检查是否为控制语句
        if (
            command.startswith("如果")
            or command.startswith("否则")
            or command.startswith("循环")
            or command.startswith("当")
            or command.startswith("对于")
            or command.startswith("重复")
        ):
            return CommandType.CONTROL

        # 检查是否为调试命令
        if (
            command.startswith("调试")
            or command.startswith("断点")
            or command.startswith("查看")
            or command.startswith("跟踪")
        ):
            return CommandType.DEBUG

        # 检查是否为帮助命令
        if command.startswith("帮助") or command.startswith("?") or command == "help":
            return CommandType.HELP

        # 默认为语句
        return CommandType.STATEMENT

    def add_entry(
        self,
        command: str,
        result: Optional[str] = None,
        execution_time: Optional[float] = None,
        success: bool = True,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> HistoryEntry:
        """添加历史记录条目

        Args:
            command: 执行的命令
            result: 命令结果
            execution_time: 执行时间（秒）
            success: 是否执行成功
            tags: 标签列表
            metadata: 元数据

        Returns:
            创建的历史记录条目
        """
        entry = HistoryEntry(
            timestamp=datetime.now(),
            command=command,
            result=result,
            command_type=self._detect_command_type(command),
            execution_time=execution_time,
            success=success,
            tags=tags or [],
            metadata=metadata or {},
        )

        if self.use_database:
            self._save_to_database(entry)
        else:
            self.history.append(entry)

            # 保持历史记录大小限制
            if len(self.history) > self.max_size:
                self.history = self.history[-self.max_size :]

            self._save_history()

        return entry

    def _save_to_database(self, entry: HistoryEntry) -> None:
        """保存到数据库"""
        self.cursor.execute(
            """
            INSERT INTO history
            (timestamp, command, result, command_type, execution_time, success, tags, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                entry.timestamp.isoformat(),
                entry.command,
                entry.result,
                entry.command_type.value,
                entry.execution_time,
                1 if entry.success else 0,
                json.dumps(entry.tags),
                json.dumps(entry.metadata),
            ),
        )
        self.conn.commit()

    def search(
        self,
        keyword: Optional[str] = None,
        command_type: Optional[CommandType] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
        success_only: bool = False,
        limit: int = 100,
    ) -> List[HistoryEntry]:
        """搜索历史记录

        Args:
            keyword: 搜索关键词
            command_type: 命令类型过滤
            start_time: 开始时间
            end_time: 结束时间
            tags: 标签过滤
            success_only: 是否只显示成功的命令
            limit: 返回结果数量限制

        Returns:
            匹配的历史记录条目列表
        """
        if self.use_database:
            return self._search_in_database(
                keyword, command_type, start_time, end_time, tags, success_only, limit
            )
        else:
            return self._search_in_memory(
                keyword, command_type, start_time, end_time, tags, success_only, limit
            )

    def _search_in_memory(
        self,
        keyword: Optional[str],
        command_type: Optional[CommandType],
        start_time: Optional[datetime],
        end_time: Optional[datetime],
        tags: Optional[List[str]],
        success_only: bool,
        limit: int,
    ) -> List[HistoryEntry]:
        """在内存中搜索历史记录"""
        results = []

        for entry in reversed(self.history):  # 从最新开始搜索
            # 应用过滤器
            if success_only and not entry.success:
                continue

            if command_type and entry.command_type != command_type:
                continue

            if start_time and entry.timestamp < start_time:
                continue

            if end_time and entry.timestamp > end_time:
                continue

            if tags and not any(tag in entry.tags for tag in tags):
                continue

            if keyword and keyword.lower() not in entry.command.lower():
                continue

            results.append(entry)

            if len(results) >= limit:
                break

        return results

    def _search_in_database(
        self,
        keyword: Optional[str],
        command_type: Optional[CommandType],
        start_time: Optional[datetime],
        end_time: Optional[datetime],
        tags: Optional[List[str]],
        success_only: bool,
        limit: int,
    ) -> List[HistoryEntry]:
        """在数据库中搜索历史记录"""
        query = "SELECT * FROM history WHERE 1=1"
        params = []

        if keyword:
            query += " AND command LIKE ?"
            params.append(f"%{keyword}%")

        if command_type:
            query += " AND command_type = ?"
            params.append(command_type.value)

        if start_time:
            query += " AND timestamp >= ?"
            params.append(start_time.isoformat())

        if end_time:
            query += " AND timestamp <= ?"
            params.append(end_time.isoformat())

        if tags:
            tag_conditions = []
            for tag in tags:
                tag_conditions.append("tags LIKE ?")
                params.append(f'%"{tag}"%')
            query += " AND (" + " OR ".join(tag_conditions) + ")"

        if success_only:
            query += " AND success = 1"

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()

        # 转换结果
        entries = []
        for row in rows:
            entry = HistoryEntry(
                timestamp=datetime.fromisoformat(row[1]),
                command=row[2],
                result=row[3],
                command_type=CommandType(row[4]),
                execution_time=row[5],
                success=bool(row[6]),
                tags=json.loads(row[7]) if row[7] else [],
                metadata=json.loads(row[8]) if row[8] else {},
            )
            entries.append(entry)

        return entries

    def edit_and_reexecute(self, index: int, new_command: str) -> Optional[HistoryEntry]:
        """编辑历史命令并创建新条目

        Args:
            index: 历史记录索引（0-based，从最新开始）
            new_command: 新的命令

        Returns:
            新的历史记录条目，如果索引无效则返回None
        """
        if self.use_database:
            return self._edit_in_database(index, new_command)
        else:
            return self._edit_in_memory(index, new_command)

    def _edit_in_memory(self, index: int, new_command: str) -> Optional[HistoryEntry]:
        """在内存中编辑历史命令"""
        if 0 <= index < len(self.history):
            # 获取原始条目（从最新开始）
            original_index = len(self.history) - 1 - index
            old_entry = self.history[original_index]

            # 创建新条目
            new_entry = HistoryEntry(
                timestamp=datetime.now(),
                command=new_command,
                result=None,  # 结果将在执行后设置
                command_type=self._detect_command_type(new_command),
                execution_time=None,
                success=True,
                tags=old_entry.tags.copy(),
                metadata={
                    "edited_from": old_entry.command,
                    "original_timestamp": old_entry.timestamp.isoformat(),
                    **old_entry.metadata,
                },
            )

            self.history.append(new_entry)

            # 保持历史记录大小限制
            if len(self.history) > self.max_size:
                self.history = self.history[-self.max_size :]

            self._save_history()
            return new_entry

        return None

    def _edit_in_database(self, index: int, new_command: str) -> Optional[HistoryEntry]:
        """在数据库中编辑历史命令"""
        # 获取原始条目
        self.cursor.execute(
            "SELECT * FROM history ORDER BY timestamp DESC LIMIT 1 OFFSET ?", (index,)
        )
        row = self.cursor.fetchone()

        if row:
            # 创建新条目
            new_entry = HistoryEntry(
                timestamp=datetime.now(),
                command=new_command,
                result=None,
                command_type=self._detect_command_type(new_command),
                execution_time=None,
                success=True,
                tags=json.loads(row[7]) if row[7] else [],
                metadata={
                    "edited_from": row[2],
                    "original_timestamp": row[1],
                    **(json.loads(row[8]) if row[8] else {}),
                },
            )

            # 保存到数据库
            self._save_to_database(new_entry)
            return new_entry

        return None

    def clear(self) -> None:
        """清空历史记录"""
        if self.use_database:
            self.cursor.execute("DELETE FROM history")
            self.conn.commit()
        else:
            self.history.clear()
            self._save_history()

    def export_json(self, filepath: Path) -> None:
        """导出历史记录为JSON格式

        Args:
            filepath: 导出文件路径
        """
        if self.use_database:
            entries = self._get_all_from_database()
        else:
            entries = self.history

        data = {
            "version": "1.0",
            "export_time": datetime.now().isoformat(),
            "count": len(entries),
            "entries": [entry.to_dict() for entry in entries],
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def export_csv(self, filepath: Path) -> None:
        """导出历史记录为CSV格式

        Args:
            filepath: 导出文件路径
        """
        if self.use_database:
            entries = self._get_all_from_database()
        else:
            entries = self.history

        import csv

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # 写入表头
            writer.writerow(
                [
                    "timestamp",
                    "command",
                    "result",
                    "command_type",
                    "execution_time",
                    "success",
                    "tags",
                    "metadata",
                ]
            )

            # 写入数据
            for entry in entries:
                writer.writerow(
                    [
                        entry.timestamp.isoformat(),
                        entry.command,
                        entry.result or "",
                        entry.command_type.value,
                        entry.execution_time or "",
                        "是" if entry.success else "否",
                        ";".join(entry.tags),
                        json.dumps(entry.metadata, ensure_ascii=False),
                    ]
                )

    def import_json(self, filepath: Path) -> int:
        """从JSON文件导入历史记录

        Args:
            filepath: 导入文件路径

        Returns:
            导入的记录数量
        """
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        count = 0
        for entry_data in data.get("entries", []):
            try:
                entry = HistoryEntry.from_dict(entry_data)

                if self.use_database:
                    self._save_to_database(entry)
                else:
                    self.history.append(entry)
                    count += 1
            except Exception as e:
                print(f"导入历史记录失败: {e}")
                continue

        if not self.use_database:
            # 保持历史记录大小限制
            if len(self.history) > self.max_size:
                self.history = self.history[-self.max_size :]

            self._save_history()

        return count

    def _get_all_from_database(self) -> List[HistoryEntry]:
        """从数据库获取所有历史记录"""
        self.cursor.execute("SELECT * FROM history ORDER BY timestamp")
        rows = self.cursor.fetchall()

        entries = []
        for row in rows:
            entry = HistoryEntry(
                timestamp=datetime.fromisoformat(row[1]),
                command=row[2],
                result=row[3],
                command_type=CommandType(row[4]),
                execution_time=row[5],
                success=bool(row[6]),
                tags=json.loads(row[7]) if row[7] else [],
                metadata=json.loads(row[8]) if row[8] else {},
            )
            entries.append(entry)

        return entries

    def _load_history(self) -> None:
        """从文件加载历史记录"""
        try:
            if self.history_file.exists():
                with open(self.history_file, "rb") as f:
                    self.history = pickle.load(f)
        except Exception as e:
            print(f"加载历史记录失败: {e}")
            self.history = []

    def _save_history(self) -> None:
        """保存历史记录到文件"""
        try:
            # 确保目录存在
            self.history_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.history_file, "wb") as f:
                pickle.dump(self.history, f)
        except Exception as e:
            print(f"保存历史记录失败: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """获取历史记录统计信息

        Returns:
            统计信息字典
        """
        if self.use_database:
            return self._get_stats_from_database()
        else:
            return self._get_stats_from_memory()

    def _get_stats_from_memory(self) -> Dict[str, Any]:
        """从内存获取统计信息"""
        total = len(self.history)
        successful = sum(1 for entry in self.history if entry.success)
        failed = total - successful

        # 按类型统计
        type_stats = {}
        for entry in self.history:
            type_name = entry.command_type.value
            type_stats[type_name] = type_stats.get(type_name, 0) + 1

        # 计算平均执行时间
        exec_times = [e.execution_time for e in self.history if e.execution_time]
        avg_exec_time = sum(exec_times) / len(exec_times) if exec_times else 0

        return {
            "total_entries": total,
            "successful_entries": successful,
            "failed_entries": failed,
            "success_rate": successful / total if total > 0 else 0,
            "type_distribution": type_stats,
            "average_execution_time": avg_exec_time,
            "oldest_entry": min((e.timestamp for e in self.history), default=None),
            "newest_entry": max((e.timestamp for e in self.history), default=None),
        }

    def _get_stats_from_database(self) -> Dict[str, Any]:
        """从数据库获取统计信息"""
        # 总数量
        self.cursor.execute("SELECT COUNT(*) FROM history")
        total = self.cursor.fetchone()[0]

        # 成功数量
        self.cursor.execute("SELECT COUNT(*) FROM history WHERE success = 1")
        successful = self.cursor.fetchone()[0]

        # 失败数量
        failed = total - successful

        # 按类型统计
        self.cursor.execute("SELECT command_type, COUNT(*) FROM history GROUP BY command_type")
        type_stats = dict(self.cursor.fetchall())

        # 平均执行时间
        self.cursor.execute(
            "SELECT AVG(execution_time) FROM history WHERE execution_time IS NOT NULL"
        )
        avg_exec_time = self.cursor.fetchone()[0] or 0

        # 最旧和最新时间戳
        self.cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM history")
        min_time, max_time = self.cursor.fetchone()

        return {
            "total_entries": total,
            "successful_entries": successful,
            "failed_entries": failed,
            "success_rate": successful / total if total > 0 else 0,
            "type_distribution": type_stats,
            "average_execution_time": avg_exec_time,
            "oldest_entry": datetime.fromisoformat(min_time) if min_time else None,
            "newest_entry": datetime.fromisoformat(max_time) if max_time else None,
        }

    def __len__(self) -> int:
        """获取历史记录数量"""
        if self.use_database:
            self.cursor.execute("SELECT COUNT(*) FROM history")
            return self.cursor.fetchone()[0]
        else:
            return len(self.history)

    def __getitem__(self, index: int) -> HistoryEntry:
        """通过索引获取历史记录（0为最新）"""
        if self.use_database:
            return self._get_from_database(index)
        else:
            # 索引0表示最新的记录
            if 0 <= index < len(self.history):
                return self.history[-(index + 1)]
            raise IndexError("历史记录索引超出范围")

    def _get_from_database(self, index: int) -> HistoryEntry:
        """从数据库通过索引获取历史记录"""
        self.cursor.execute(
            "SELECT * FROM history ORDER BY timestamp DESC LIMIT 1 OFFSET ?", (index,)
        )
        row = self.cursor.fetchone()

        if row:
            return HistoryEntry(
                timestamp=datetime.fromisoformat(row[1]),
                command=row[2],
                result=row[3],
                command_type=CommandType(row[4]),
                execution_time=row[5],
                success=bool(row[6]),
                tags=json.loads(row[7]) if row[7] else [],
                metadata=json.loads(row[8]) if row[8] else {},
            )

        raise IndexError("历史记录索引超出范围")

    def __iter__(self):
        """迭代历史记录（从最新到最旧）"""
        if self.use_database:
            return self._iterate_database()
        else:
            return iter(reversed(self.history))

    def _iterate_database(self):
        """迭代数据库中的历史记录"""
        self.cursor.execute("SELECT * FROM history ORDER BY timestamp DESC")
        for row in self.cursor.fetchall():
            yield HistoryEntry(
                timestamp=datetime.fromisoformat(row[1]),
                command=row[2],
                result=row[3],
                command_type=CommandType(row[4]),
                execution_time=row[5],
                success=bool(row[6]),
                tags=json.loads(row[7]) if row[7] else [],
                metadata=json.loads(row[8]) if row[8] else {},
            )

    def close(self) -> None:
        """关闭历史记录管理器"""
        if self.use_database:
            self.conn.close()


# 便捷函数
def create_history_manager(max_size: int = 1000, use_database: bool = False) -> HistoryManager:
    """创建历史记录管理器

    Args:
        max_size: 最大历史记录数量
        use_database: 是否使用数据库存储

    Returns:
        历史记录管理器实例
    """
    return HistoryManager(max_size=max_size, use_database=use_database)


def print_history_stats(manager: HistoryManager) -> None:
    """打印历史记录统计信息

    Args:
        manager: 历史记录管理器
    """
    stats = manager.get_stats()

    print("历史记录统计:")
    print(f"  总记录数: {stats['total_entries']}")
    print(f"  成功记录: {stats['successful_entries']}")
    print(f"  失败记录: {stats['failed_entries']}")
    print(f"  成功率: {stats['success_rate']:.1%}")
    print(f"  平均执行时间: {stats['average_execution_time']:.3f}秒")

    if stats["type_distribution"]:
        print("  命令类型分布:")
        for type_name, count in stats["type_distribution"].items():
            percentage = count / stats["total_entries"] * 100
            print(f"    {type_name}: {count} ({percentage:.1f}%)")

    if stats["oldest_entry"]:
        print(f"  最早记录: {stats['oldest_entry'].strftime('%Y-%m-%d %H:%M:%S')}")

    if stats["newest_entry"]:
        print(f"  最新记录: {stats['newest_entry'].strftime('%Y-%m-%d %H:%M:%S')}")
