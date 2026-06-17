# -*- coding: utf-8 -*-
"""错误处理系统

提供统一的错误处理机制：
- 错误报告
- 错误格式化
- 错误统计
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional

# 使用统一的日志工具
from src.utils.logging_utils import get_logger


class ErrorType(Enum):
    """错误类型枚举"""

    LEXER_ERROR = auto()  # 词法错误
    PARSER_ERROR = auto()  # 语法错误
    SEMANTIC_ERROR = auto()  # 语义错误
    RUNTIME_ERROR = auto()  # 运行时错误


@dataclass
class Error:
    """错误信息"""

    error_type: ErrorType
    message: str
    line: int
    column: int
    source: Optional[str] = None
    suggestion: Optional[str] = None  # 添加建议字段

    def __str__(self) -> str:
        """格式化错误信息"""
        type_names = {
            ErrorType.LEXER_ERROR: "词法错误",
            ErrorType.PARSER_ERROR: "语法错误",
            ErrorType.SEMANTIC_ERROR: "语义错误",
            ErrorType.RUNTIME_ERROR: "运行时错误",
        }
        type_name = type_names.get(self.error_type, "错误")

        # 基本错误信息
        result = f"{type_name}：第 {self.line} 行，第 {self.column} 列：{self.message}"

        # 添加建议
        if self.suggestion:
            result += f"\n  💡 建议：{self.suggestion}"

        return result


class ErrorHandler:
    """错误处理器"""

    def __init__(self) -> None:
        """初始化错误处理器"""
        self.errors: List[Error] = []
        self.logger = get_logger("error_handling")

    def report(
        self,
        error_type: ErrorType,
        message: str,
        line: int,
        column: int,
        source: Optional[str] = None,
        suggestion: Optional[str] = None,
    ) -> None:
        """报告错误

        Args:
            error_type: 错误类型
            message: 错误消息
            line: 行号
            column: 列号
            source: 源代码（可选）
            suggestion: 修复建议（可选）
        """
        error = Error(
            error_type=error_type,
            message=message,
            line=line,
            column=column,
            source=source,
            suggestion=suggestion,
        )
        self.errors.append(error)

    def get_errors(self) -> List[Error]:
        """获取所有错误

        Returns:
            错误列表
        """
        return self.errors

    def format_error(self, index: int) -> str:
        """格式化指定索引的错误

        Args:
            index: 错误索引

        Returns:
            格式化的错误信息
        """
        if index < 0 or index >= len(self.errors):
            return ""

        error = self.errors[index]
        result = str(error)

        # 如果有源代码，添加上下文
        if error.source:
            lines = error.source.split("\n")
            if error.line <= len(lines):
                source_line = lines[error.line - 1]
                result += f"\n  {source_line}"
                result += f"\n  {' ' * (error.column - 1)}^"

        return result

    def get_statistics(self) -> Dict[ErrorType, int]:
        """获取错误统计

        Returns:
            错误类型到数量的映射
        """
        stats: Dict[ErrorType, int] = {}
        for error in self.errors:
            if error.error_type not in stats:
                stats[error.error_type] = 0
            stats[error.error_type] += 1
        return stats

    def has_errors(self) -> bool:
        """检查是否有错误

        Returns:
            是否有错误
        """
        return len(self.errors) > 0

    def clear(self) -> None:
        """清除所有错误"""
        self.errors.clear()

    def print_errors(self) -> None:
        """打印所有错误"""
        for i in range(len(self.errors)):
            error_str = self.format_error(i)
            self.logger.error(error_str)
