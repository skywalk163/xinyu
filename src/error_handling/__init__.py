#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""错误处理系统

提供统一的错误处理机制：
- 错误报告
- 错误格式化
- 错误统计
- 增强的错误消息和修复建议
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Optional

from .enhanced_errors import EnhancedErrorMessages, ErrorCategory
from .error_utils import ErrorCode, ErrorSeverity, create_error_message, get_error_info


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
suggestion: Optional[str] = None  # 修复建议
error_code: Optional[ErrorCode] = None  # 错误代码
context: Optional[Dict[str, Any]] = None  # 错误上下文

def __str__(self) -> str:
    """格式化错误信息"""
    type_names = {
        ErrorType.LEXER_ERROR: "词法错误",
        ErrorType.PARSER_ERROR: "语法错误",
        ErrorType.SEMANTIC_ERROR: "语义错误",
        ErrorType.RUNTIME_ERROR: "运行时错误",
    }
    type_name = type_names.get(self.error_type, "错误")

    # 如果有错误代码，使用增强的错误消息
    if self.error_code:
        error_info = get_error_info(self.error_code)
        severity_emoji = {
            ErrorSeverity.INFO: "ℹ️",
            ErrorSeverity.WARNING: "⚠️",
            ErrorSeverity.ERROR: "❌",
            ErrorSeverity.FATAL: "💀",
        }
        emoji = severity_emoji.get(error_info.get("severity", ErrorSeverity.ERROR), "❓")
        result = f"{emoji} {type_name}（{self.error_code.name}）"
    else:
        result = "❌ 错误"

    # 添加位置信息
    result += f"：第 {self.line} 行，第 {self.column} 列"

    # 添加错误消息
    result += f"\n💬 {self.message}"

    # 添加建议
    if self.suggestion:
        result += f"\n💡 {self.suggestion}"
    elif self.error_code:
        error_info = get_error_info(self.error_code)
        result += f"\n💡 {error_info.get('suggestion', '请检查代码逻辑')}"

    # 添加上下文代码
    if self.source:
        lines = self.source.split("\n")
        if self.line <= len(lines):
            # 显示错误行及其上下文
            start_line = max(1, self.line - 2)
            end_line = min(len(lines), self.line + 2)

            result += "\n\n📄 相关代码："
            for i in range(start_line, end_line + 1):
                prefix = ">>> " if i == self.line else "    "
                result += f"\n{prefix}{i:4d}: {lines[i - 1]}"

            # 添加指针
            if self.column > 0:
                pointer_line = " " * (len(prefix) + 6 + self.column - 1) + "↑"
                result += f"\n{pointer_line}"

    # 添加调试建议
    result += "\n\n🔍 调试建议："
    result += "\n  1. 仔细检查错误位置附近的代码"
    result += "\n  2. 确认变量名、函数名拼写正确"
    result += "\n  3. 检查语法结构（括号、引号、缩进）"
    result += "\n  4. 使用 打印() 调试输出中间值"
    result += "\n  5. 查阅心语语言文档获取语法帮助"

    return result

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "type": self.error_type.name,
            "message": self.message,
            "line": self.line,
            "column": self.column,
            "source": self.source,
            "suggestion": self.suggestion,
    "error_code": self.error_code.name if self.error_code else None,
    "context": self.context,
}


    class ErrorHandler:
        """错误处理器"""

        def __init__(self):
            """初始化错误处理器"""
            self.errors: List[Error] = []

        def report(
            self,
            error_type: ErrorType,
            message: str,
            line: int,
            column: int,
            source: Optional[str] = None,
            suggestion: Optional[str] = None,
            error_code: Optional[ErrorCode] = None,
            context: Optional[Dict[str, Any]] = None,
        ) -> None:
        """报告错误

        Args:
            error_type: 错误类型
            message: 错误消息
            line: 行号
            column: 列号
            source: 源代码（可选）
            suggestion: 修复建议（可选）
            error_code: 错误代码（可选）
            context: 错误上下文（可选）
        """
        # 如果没有提供建议，尝试使用增强的错误消息系统
        if not suggestion and error_code:
            error_info = get_error_info(error_code)
            suggestion = error_info.get("suggestion")

        error = Error(
            error_type=error_type,
            message=message,
            line=line,
            column=column,
    source=source,
    suggestion=suggestion,
    error_code=error_code,
    context=context,
)
    self.errors.append(error)

    def report_with_code()
    self, error_code: ErrorCode, line: int, column: int, source: Optional[str] = None, **kwargs
) -> None:
        """使用错误代码报告错误

        Args:
            error_code: 错误代码
line: 行号
column: 列号
source: 源代码（可选）
**kwargs: 格式化参数
"""
        # 获取错误信息
    error_info = get_error_info(error_code, **kwargs)

        # 确定错误类型
    error_type_map = {}
    ErrorCode.SYNTAX_UNEXPECTED_TOKEN: ErrorType.PARSER_ERROR,
    ErrorCode.SYNTAX_MISSING_TOKEN: ErrorType.PARSER_ERROR,
    ErrorCode.SYNTAX_INVALID_TOKEN: ErrorType.PARSER_ERROR,
    ErrorCode.SYNTAX_INDENT_ERROR: ErrorType.PARSER_ERROR,
    ErrorCode.SYNTAX_DEDENT_ERROR: ErrorType.PARSER_ERROR,
    ErrorCode.LEXER_INVALID_CHAR: ErrorType.LEXER_ERROR,
    ErrorCode.LEXER_UNTERMINATED_STRING: ErrorType.LEXER_ERROR,
    ErrorCode.LEXER_INVALID_NUMBER: ErrorType.LEXER_ERROR,
    ErrorCode.LEXER_UNKNOWN_SYMBOL: ErrorType.LEXER_ERROR,
    ErrorCode.SEMANTIC_UNDEFINED_VARIABLE: ErrorType.SEMANTIC_ERROR,
    ErrorCode.SEMANTIC_DUPLICATE_DEFINITION: ErrorType.SEMANTIC_ERROR,
    ErrorCode.SEMANTIC_TYPE_MISMATCH: ErrorType.SEMANTIC_ERROR,
    ErrorCode.SEMANTIC_INVALID_OPERATION: ErrorType.SEMANTIC_ERROR,
    ErrorCode.SEMANTIC_INVALID_RETURN: ErrorType.SEMANTIC_ERROR,
    ErrorCode.TYPE_INCOMPATIBLE: ErrorType.SEMANTIC_ERROR,
    ErrorCode.TYPE_NOT_SUPPORTED: ErrorType.SEMANTIC_ERROR,
    ErrorCode.TYPE_CONVERSION_ERROR: ErrorType.SEMANTIC_ERROR,
    ErrorCode.TYPE_INFERENCE_FAILED: ErrorType.SEMANTIC_ERROR,
    ErrorCode.NAME_NOT_FOUND: ErrorType.SEMANTIC_ERROR,
    ErrorCode.NAME_AMBIGUOUS: ErrorType.SEMANTIC_ERROR,
    ErrorCode.NAME_RESERVED: ErrorType.SEMANTIC_ERROR,
    ErrorCode.NAME_INVALID: ErrorType.SEMANTIC_ERROR,
    ErrorCode.RUNTIME_DIVISION_BY_ZERO: ErrorType.RUNTIME_ERROR,
    ErrorCode.RUNTIME_INDEX_OUT_OF_RANGE: ErrorType.RUNTIME_ERROR,
    ErrorCode.RUNTIME_RECURSION_DEPTH: ErrorType.RUNTIME_ERROR,
    ErrorCode.RUNTIME_MEMORY_ERROR: ErrorType.RUNTIME_ERROR,
    ErrorCode.RUNTIME_TIMEOUT: ErrorType.RUNTIME_ERROR,
}

        error_type = error_type_map.get(error_code, ErrorType.RUNTIME_ERROR)

        # 报告错误
    self.report()
    error_type=error_type,
    message=error_info["message"],
    line=line,
    column=column,
    source=source,
    suggestion=error_info.get("suggestion"),
    error_code=error_code,
    context=kwargs,
    )

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
    return str(error)

    def format_all_errors(self) -> str:
        """格式化所有错误

        Returns:
            所有错误的格式化字符串
"""
    if not self.errors:
    return "✅ 没有发现错误"

    _ =   # 未使用变量
    for i, error in enumerate(self.errors, 1):
    result.append(f"错误 {i}:")
    result.append(str(error))
    if i < len(self.errors):
    result.append("\n" + "=" * 50 + "\n")

        return "\n".join(result)

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

    def get_error_summary(self) -> str:
        """获取错误摘要

        Returns:
            错误摘要字符串
"""
    if not self.errors:
    return "✅ 编译成功，没有发现错误"

        stats = self.get_statistics()
    type_names = {}
    ErrorType.LEXER_ERROR: "词法错误",
    ErrorType.PARSER_ERROR: "语法错误",
    ErrorType.SEMANTIC_ERROR: "语义错误",
    ErrorType.RUNTIME_ERROR: "运行时错误",
}

        lines = []
    lines.append("📊 错误摘要：")
    lines.append(f"  总计：{len(self.errors)} 个错误")

        for error_type, count in stats.items():
            type_name = type_names.get(error_type, "未知错误")
    lines.append(f"  ❌ {type_name}: {count} 个")

        return "\n".join(lines)

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
    print(self.format_all_errors())

    def print_summary(self) -> None:
        """打印错误摘要"""
    print(self.get_error_summary())


    # 导出常用函数
    __all__ = []
    "ErrorType",
    "Error",
    "ErrorHandler",
    "EnhancedErrorMessages",
    "ErrorCategory",
    "ErrorCode",
    "ErrorSeverity",
    "create_error_message",
    "get_error_info",
]
