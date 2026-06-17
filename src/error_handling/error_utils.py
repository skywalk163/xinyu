#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""错误处理工具函数

提供错误消息生成、格式化、建议等实用功能。
"""

import re
from enum import Enum
from typing import Dict, List, Optional, Tuple


class ErrorSeverity(Enum):
    """错误严重程度"""

    INFO = "info"  # 信息
    WARNING = "warning"  # 警告
    ERROR = "error"  # 错误
    FATAL = "fatal"  # 致命错误


class ErrorCode(Enum):
    """错误代码枚举"""

    # 语法错误 (1000-1999)
    SYNTAX_UNEXPECTED_TOKEN = 1001
    SYNTAX_MISSING_TOKEN = 1002
    SYNTAX_INVALID_TOKEN = 1003
    SYNTAX_INDENT_ERROR = 1004
    SYNTAX_DEDENT_ERROR = 1005

    # 词法错误 (2000-2999)
    LEXER_INVALID_CHAR = 2001
    LEXER_UNTERMINATED_STRING = 2002
    LEXER_INVALID_NUMBER = 2003
    LEXER_UNKNOWN_SYMBOL = 2004

    # 语义错误 (3000-3999)
    SEMANTIC_UNDEFINED_VARIABLE = 3001
    SEMANTIC_DUPLICATE_DEFINITION = 3002
    SEMANTIC_TYPE_MISMATCH = 3003
    SEMANTIC_INVALID_OPERATION = 3004
    SEMANTIC_INVALID_RETURN = 3005

    # 类型错误 (4000-4999)
    TYPE_INCOMPATIBLE = 4001
    TYPE_NOT_SUPPORTED = 4002
    TYPE_CONVERSION_ERROR = 4003
    TYPE_INFERENCE_FAILED = 4004

    # 名称错误 (5000-5999)
    NAME_NOT_FOUND = 5001
    NAME_AMBIGUOUS = 5002
    NAME_RESERVED = 5003
    NAME_INVALID = 5004

    # 运行时错误 (6000-6999)
    RUNTIME_DIVISION_BY_ZERO = 6001
    RUNTIME_INDEX_OUT_OF_RANGE = 6002
    RUNTIME_RECURSION_DEPTH = 6003
    RUNTIME_MEMORY_ERROR = 6004
    RUNTIME_TIMEOUT = 6005

    # 安全错误 (7000-7999)
    SECURITY_UNSAFE_OPERATION = 7001
    SECURITY_ACCESS_DENIED = 7002
    SECURITY_RESOURCE_LIMIT = 7003
    SECURITY_VALIDATION_FAILED = 7004

    # 验证错误 (8000-8999)
    VALIDATION_INVALID_ARGUMENT = 8001
    VALIDATION_MISSING_ARGUMENT = 8002
    VALIDATION_OUT_OF_RANGE = 8003
    VALIDATION_INVALID_FORMAT = 8004

    # 配置错误 (9000-9999)
    CONFIG_INVALID_VALUE = 9001
    CONFIG_MISSING_KEY = 9002
    CONFIG_FILE_NOT_FOUND = 9003
    CONFIG_PARSE_ERROR = 9004


# 错误代码到消息的映射
ERROR_MESSAGES = {
    # 语法错误
    ErrorCode.SYNTAX_UNEXPECTED_TOKEN: {
        "message": "遇到未预期的标记：{token}",
        "suggestion": "请检查语法，确保标记使用正确",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.SYNTAX_MISSING_TOKEN: {
        "message": "缺少必要的标记：{token}",
        "suggestion": "请添加缺失的标记，如括号、引号、冒号等",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.SYNTAX_INVALID_TOKEN: {
        "message": "无效的标记：{token}",
        "suggestion": "请使用合法的标记",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.SYNTAX_INDENT_ERROR: {
        "message": "缩进错误",
        "suggestion": "请使用4个空格进行缩进，确保缩进一致",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.SYNTAX_DEDENT_ERROR: {
        "message": "反缩进错误",
        "suggestion": "请检查缩进层次，确保反缩进与之前的缩进匹配",
        "severity": ErrorSeverity.ERROR,
    },
    # 词法错误
    ErrorCode.LEXER_INVALID_CHAR: {
        "message": "非法字符：{char}",
        "suggestion": "请检查是否使用了不支持的字符，或检查字符编码",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.LEXER_UNTERMINATED_STRING: {
        "message": "未终止的字符串",
        "suggestion": "请检查字符串是否以引号正确结束",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.LEXER_INVALID_NUMBER: {
        "message": "无效的数字格式：{number}",
        "suggestion": "请使用合法的数字格式，如 123、3.14、0xFF 等",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.LEXER_UNKNOWN_SYMBOL: {
        "message": "未知的符号：{symbol}",
        "suggestion": "请检查符号拼写，或确认是否已定义",
        "severity": ErrorSeverity.ERROR,
    },
    # 语义错误
    ErrorCode.SEMANTIC_UNDEFINED_VARIABLE: {
        "message": "未定义的变量：{name}",
        "suggestion": "请在使用前定义变量，或检查变量名拼写",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.SEMANTIC_DUPLICATE_DEFINITION: {
        "message": "重复的定义：{name}",
        "suggestion": "请使用不同的名称，或删除重复的定义",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.SEMANTIC_TYPE_MISMATCH: {
        "message": "类型不匹配：{detail}",
        "suggestion": "请检查变量类型，确保操作符两边的类型兼容",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.SEMANTIC_INVALID_OPERATION: {
        "message": "无效的操作：{operation}",
        "suggestion": "请检查操作是否支持当前类型",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.SEMANTIC_INVALID_RETURN: {
        "message": "无效的返回语句",
        "suggestion": "请检查返回语句是否在函数内部，或返回值的类型",
        "severity": ErrorSeverity.ERROR,
    },
    # 类型错误
    ErrorCode.TYPE_INCOMPATIBLE: {
        "message": "类型不兼容：{type1} 和 {type2}",
        "suggestion": "请使用类型转换，或确保类型兼容",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.TYPE_NOT_SUPPORTED: {
        "message": "不支持的类型：{type}",
        "suggestion": "请使用支持的类型，或检查类型定义",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.TYPE_CONVERSION_ERROR: {
        "message": "类型转换错误：从 {from_type} 到 {to_type}",
        "suggestion": "请检查类型转换是否合法，或使用显式转换",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.TYPE_INFERENCE_FAILED: {
        "message": "类型推断失败：{detail}",
        "suggestion": "请提供显式类型注解，或检查类型约束",
        "severity": ErrorSeverity.ERROR,
    },
    # 名称错误
    ErrorCode.NAME_NOT_FOUND: {
        "message": "未找到名称：{name}",
        "suggestion": "请检查名称拼写，或确认是否已导入/定义",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.NAME_AMBIGUOUS: {
        "message": "名称歧义：{name}",
        "suggestion": "请使用完全限定名，或重命名冲突的名称",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.NAME_RESERVED: {
        "message": "保留名称：{name}",
        "suggestion": "请使用其他名称，避免使用语言关键字或内置名称",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.NAME_INVALID: {
        "message": "无效的名称：{name}",
        "suggestion": "请使用合法的标识符（字母、数字、下划线，不以数字开头）",
        "severity": ErrorSeverity.ERROR,
    },
    # 运行时错误
    ErrorCode.RUNTIME_DIVISION_BY_ZERO: {
        "message": "除以零错误",
        "suggestion": "请检查除数是否为零，或添加条件判断",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.RUNTIME_INDEX_OUT_OF_RANGE: {
        "message": "索引超出范围：索引 {index}，长度 {length}",
        "suggestion": "请检查索引值是否在有效范围内（0 到 length-1）",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.RUNTIME_RECURSION_DEPTH: {
        "message": "递归深度超过限制：{depth}",
        "suggestion": "请检查递归终止条件，或考虑使用迭代替代递归",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.RUNTIME_MEMORY_ERROR: {
        "message": "内存错误",
        "suggestion": "请检查是否有内存泄漏，或减少内存使用",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.RUNTIME_TIMEOUT: {
        "message": "执行超时",
        "suggestion": "请优化算法复杂度，或增加超时限制",
        "severity": ErrorSeverity.ERROR,
    },
    # 安全错误
    ErrorCode.SECURITY_UNSAFE_OPERATION: {
        "message": "不安全操作：{operation}",
        "suggestion": "请避免使用不安全的功能，或使用安全沙箱环境",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.SECURITY_ACCESS_DENIED: {
        "message": "访问被拒绝：{resource}",
        "suggestion": "请检查权限设置，或使用授权访问",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.SECURITY_RESOURCE_LIMIT: {
        "message": "资源限制：{resource} 超过限制",
        "suggestion": "请减少资源使用，或调整限制设置",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.SECURITY_VALIDATION_FAILED: {
        "message": "安全验证失败：{detail}",
        "suggestion": "请检查输入数据，或调整安全策略",
        "severity": ErrorSeverity.ERROR,
    },
    # 验证错误
    ErrorCode.VALIDATION_INVALID_ARGUMENT: {
        "message": "无效参数：{argument}",
        "suggestion": "请检查参数值是否符合要求",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.VALIDATION_MISSING_ARGUMENT: {
        "message": "缺少必要参数：{argument}",
        "suggestion": "请提供所有必要参数",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.VALIDATION_OUT_OF_RANGE: {
        "message": "参数超出范围：{argument} = {value}，范围：{range}",
        "suggestion": "请确保参数值在有效范围内",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.VALIDATION_INVALID_FORMAT: {
        "message": "无效格式：{detail}",
        "suggestion": "请检查数据格式是否符合要求",
        "severity": ErrorSeverity.ERROR,
    },
    # 配置错误
    ErrorCode.CONFIG_INVALID_VALUE: {
        "message": "配置值无效：{key} = {value}",
        "suggestion": "请检查配置值是否符合要求",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.CONFIG_MISSING_KEY: {
        "message": "缺少配置项：{key}",
        "suggestion": "请添加必要的配置项",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.CONFIG_FILE_NOT_FOUND: {
        "message": "配置文件未找到：{path}",
        "suggestion": "请检查文件路径，或创建配置文件",
        "severity": ErrorSeverity.ERROR,
    },
    ErrorCode.CONFIG_PARSE_ERROR: {
        "message": "配置文件解析错误：{detail}",
        "suggestion": "请检查配置文件格式，确保语法正确",
        "severity": ErrorSeverity.ERROR,
    },
}


def get_error_info(error_code: ErrorCode, **kwargs) -> Dict:
    """获取错误信息

    Args:
        error_code: 错误代码
        **kwargs: 格式化参数

    Returns:
        错误信息字典
    """
    info = ERROR_MESSAGES.get(
        error_code, {"message": "未知错误", "suggestion": "请检查代码逻辑", "severity": ErrorSeverity.ERROR}
    ).copy()

    # 格式化消息
    if "message" in info:
        try:
            info["message"] = info["message"].format(**kwargs)
        except KeyError:
            pass

    return info


def create_error_message(
    error_code: ErrorCode, line: int = 0, column: int = 0, source: Optional[str] = None, **kwargs
) -> str:
    """创建错误消息

    Args:
        error_code: 错误代码
        line: 行号
        column: 列号
        source: 源代码（可选）
        **kwargs: 格式化参数

    Returns:
        格式化的错误消息
    """
    # 获取错误信息
    error_info = get_error_info(error_code, **kwargs)

    # 构建错误消息
    lines = []

    # 添加位置信息
    if line > 0 and column > 0:
        lines.append(f"[位置] 第 {line} 行，第 {column} 列")

    # 添加错误代码
    lines.append(f"[代码] {error_code.name} ({error_code.value})")

    # 添加严重程度
    severity_text = {
        ErrorSeverity.INFO: "[信息]",
        ErrorSeverity.WARNING: "[警告]",
        ErrorSeverity.ERROR: "[错误]",
        ErrorSeverity.FATAL: "[致命]",
    }.get(error_info["severity"], "[未知]")

    lines.append(f"{severity_text} 严重程度：{error_info['severity'].value}")

    # 添加错误消息
    lines.append(f"[描述] {error_info['message']}")

    # 添加修复建议
    lines.append(f"[建议] {error_info['suggestion']}")

    # 添加上下文代码
    if source and line > 0:
        source_lines = source.split("\n")
        if line <= len(source_lines):
            # 显示错误行及其上下文
            start_line = max(1, line - 2)
            end_line = min(len(source_lines), line + 2)

            lines.append("\n[代码] 相关代码：")
            for i in range(start_line, end_line + 1):
                prefix = ">>> " if i == line else "    "
                line_content = source_lines[i - 1].rstrip()
                lines.append(f"{prefix}{i:4d}: {line_content}")

            # 添加指针
            if column > 0:
                pointer_line = " " * (len(prefix) + 6 + column - 1) + "^"
                lines.append(pointer_line)

    # 添加调试建议
    lines.append("\n[调试] 调试建议：")
    lines.append("  1. 仔细检查错误位置附近的代码")
    lines.append("  2. 确认变量名、函数名拼写正确")
    lines.append("  3. 检查语法结构（括号、引号、缩进）")
    lines.append("  4. 使用 打印() 调试输出中间值")
    lines.append("  5. 查阅心语语言文档获取语法帮助")

    return "\n".join(lines)


def extract_error_context(source: str, line: int, column: int, context_lines: int = 3) -> Dict:
    """提取错误上下文

    Args:
        source: 源代码
        line: 错误行号
        column: 错误列号
        context_lines: 上下文行数

    Returns:
        错误上下文字典
    """
    source_lines = source.split("\n")

    # 计算上下文范围
    start_line = max(1, line - context_lines)
    end_line = min(len(source_lines), line + context_lines)

    # 提取上下文
    context = []
    for i in range(start_line, end_line + 1):
        context.append({"line": i, "content": source_lines[i - 1], "is_error_line": i == line})

    # 提取错误行
    error_line = source_lines[line - 1] if 0 < line <= len(source_lines) else ""

    return {
        "context": context,
        "error_line": error_line,
        "error_column": column,
        "start_line": start_line,
        "end_line": end_line,
    }


def suggest_fix(error_code: ErrorCode, context: Dict) -> List[str]:
    """根据错误代码和上下文提供修复建议

    Args:
        error_code: 错误代码
        context: 错误上下文

    Returns:
        修复建议列表
    """
    suggestions = []

    # 根据错误代码提供特定建议
    if error_code == ErrorCode.SYNTAX_INDENT_ERROR:
        suggestions.append("请使用4个空格进行缩进，不要使用制表符")
        suggestions.append("确保同一代码块的缩进一致")
        suggestions.append("检查是否有混合使用空格和制表符")

    elif error_code == ErrorCode.SYNTAX_MISSING_TOKEN:
        token = context.get("token", "")
        if token in ["(", ")", "[", "]", "{", "}"]:
            suggestions.append(f"请添加缺失的 {token}")
            suggestions.append("检查括号是否匹配")
        elif token in ['"', "'"]:
            suggestions.append("请确保字符串以引号正确结束")
        elif token == ":":
            suggestions.append("请在语句末尾添加冒号")

    elif error_code == ErrorCode.SEMANTIC_UNDEFINED_VARIABLE:
        name = context.get("name", "")
        suggestions.append(f"变量 '{name}' 在使用前需要先定义")
        suggestions.append(f"检查 '{name}' 的拼写是否正确")
        suggestions.append("确认变量是否在正确的作用域内")

    elif error_code == ErrorCode.SEMANTIC_TYPE_MISMATCH:
        suggestions.append("检查变量类型是否匹配操作符要求")
        suggestions.append("考虑使用类型转换函数")
        suggestions.append("检查函数参数类型是否正确")

    elif error_code == ErrorCode.RUNTIME_DIVISION_BY_ZERO:
        suggestions.append("在除法操作前检查除数是否为零")
        suggestions.append("使用条件判断避免除以零")
        suggestions.append("考虑使用 try-except 处理异常")

    elif error_code == ErrorCode.RUNTIME_INDEX_OUT_OF_RANGE:
        suggestions.append("检查索引值是否在有效范围内")
        suggestions.append("使用 len() 函数获取容器长度")
        suggestions.append("考虑使用循环遍历而不是直接索引")

    # 通用建议
    suggestions.append("使用 print() 调试输出变量值")
    suggestions.append("检查代码逻辑，确保没有逻辑错误")
    suggestions.append("查阅相关文档或示例代码")

    return suggestions


def format_error_summary(errors: List[Dict]) -> str:
    """格式化错误摘要

    Args:
        errors: 错误列表

    Returns:
        错误摘要字符串
    """
    if not errors:
        return "✅ 没有发现错误"

    # 按严重程度统计
    severity_counts = {}
    for error in errors:
        severity = error.get("severity", "unknown")
        severity_counts[severity] = severity_counts.get(severity, 0) + 1

    # 构建摘要
    lines = []
    lines.append("📊 错误摘要：")
    lines.append(f"  总计：{len(errors)} 个错误")

    for severity, count in severity_counts.items():
        emoji = {"info": "ℹ️", "warning": "⚠️", "error": "❌", "fatal": "💀", "unknown": "❓"}.get(
            severity, "❓"
        )
        lines.append(f"  {emoji} {severity}: {count} 个")

    # 按行号排序
    errors_by_line = sorted(errors, key=lambda e: e.get("line", 0))

    lines.append("\n📋 错误列表：")
    for i, error in enumerate(errors_by_line, 1):
        line = error.get("line", 0)
        column = error.get("column", 0)
        message = error.get("message", "未知错误")
        lines.append(f"  {i}. 第 {line} 行，第 {column} 列：{message}")

    return "\n".join(lines)


# 常用错误创建函数
def create_syntax_error(token: str, line: int, column: int, source: str) -> str:
    """创建语法错误消息"""
    return create_error_message(
        ErrorCode.SYNTAX_UNEXPECTED_TOKEN, line=line, column=column, source=source, token=token
    )


def create_lexical_error(char: str, line: int, column: int, source: str) -> str:
    """创建词法错误消息"""
    return create_error_message(
        ErrorCode.LEXER_INVALID_CHAR, line=line, column=column, source=source, char=repr(char)
    )


def create_semantic_error(name: str, line: int, column: int, source: str) -> str:
    """创建语义错误消息"""
    return create_error_message(
        ErrorCode.SEMANTIC_UNDEFINED_VARIABLE, line=line, column=column, source=source, name=name
    )


def create_type_error(type1: str, type2: str, line: int, column: int, source: str) -> str:
    """创建类型错误消息"""
    return create_error_message(
        ErrorCode.TYPE_INCOMPATIBLE,
        line=line,
        column=column,
        source=source,
        type1=type1,
        type2=type2,
    )


def create_runtime_error(operation: str, line: int, column: int, source: str) -> str:
    """创建运行时错误消息"""
    return create_error_message(
        ErrorCode.RUNTIME_DIVISION_BY_ZERO
        if "除以零" in operation
        else ErrorCode.RUNTIME_INDEX_OUT_OF_RANGE,
        line=line,
        column=column,
        source=source,
        operation=operation,
    )
