#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""增强的错误消息系统

提供更详细的中文错误提示和修复建议。
"""

import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple


class ErrorCategory(Enum):
    """错误分类"""

    SYNTAX = auto()  # 语法错误
    SEMANTIC = auto()  # 语义错误
    TYPE = auto()  # 类型错误
    NAME = auto()  # 名称错误
    IMPORT = auto()  # 导入错误
    RUNTIME = auto()  # 运行时错误
    SECURITY = auto()  # 安全错误
    VALIDATION = auto()  # 验证错误
    CONFIG = auto()  # 配置错误


@dataclass
class ErrorPattern:
    """错误模式匹配"""

    pattern: str
    category: ErrorCategory
    message_template: str
    suggestion_template: str
    severity: str  # "error", "warning", "info"


class EnhancedErrorMessages:
    """增强的错误消息系统"""

    # 常见错误模式
    ERROR_PATTERNS = [
        # 语法错误
        ErrorPattern(
            pattern=r"非法字符.*",
            category=ErrorCategory.SYNTAX,
            message_template="发现非法字符：{detail}",
            suggestion_template="请检查是否使用了不支持的字符，或检查字符编码是否正确",
            severity="error",
        ),
        ErrorPattern(
            pattern=r"语法错误.*",
            category=ErrorCategory.SYNTAX,
            message_template="语法错误：{detail}",
            suggestion_template="请检查代码语法，确保符合心语语言的语法规则",
            severity="error",
        ),
        ErrorPattern(
            pattern=r"缺少.*",
            category=ErrorCategory.SYNTAX,
            message_template="缺少必要的语法元素：{detail}",
            suggestion_template="请检查是否缺少括号、引号、冒号等语法元素",
            severity="error",
        ),
        ErrorPattern(
            pattern=r"未预期的.*",
            category=ErrorCategory.SYNTAX,
            message_template="遇到未预期的语法元素：{detail}",
            suggestion_template="请检查代码结构，确保语法正确",
            severity="error",
        ),
        # 语义错误
        ErrorPattern(
            pattern=r"未定义的.*",
            category=ErrorCategory.NAME,
            message_template="未定义的名称：{detail}",
            suggestion_template="请检查变量名、函数名是否正确拼写，或是否已定义",
            severity="error",
        ),
        ErrorPattern(
            pattern=r"重复定义.*",
            category=ErrorCategory.SEMANTIC,
            message_template="重复定义：{detail}",
            suggestion_template="请使用不同的名称，或删除重复的定义",
            severity="error",
        ),
        ErrorPattern(
            pattern=r"类型不匹配.*",
            category=ErrorCategory.TYPE,
            message_template="类型不匹配：{detail}",
            suggestion_template="请检查变量类型，确保操作符两边的类型兼容",
            severity="error",
        ),
        # 运行时错误
        ErrorPattern(
            pattern=r"除以零.*",
            category=ErrorCategory.RUNTIME,
            message_template="运行时错误：除以零",
            suggestion_template="请检查除数是否为零，或添加条件判断避免除以零",
            severity="error",
        ),
        ErrorPattern(
            pattern=r"索引超出范围.*",
            category=ErrorCategory.RUNTIME,
            message_template="运行时错误：索引超出范围",
            suggestion_template="请检查索引值是否在有效范围内",
            severity="error",
        ),
        ErrorPattern(
            pattern=r"递归深度.*",
            category=ErrorCategory.RUNTIME,
            message_template="运行时错误：递归深度超过限制",
            suggestion_template="请检查递归终止条件，或考虑使用迭代替代递归",
            severity="error",
        ),
        # 安全错误
        ErrorPattern(
            pattern=r"不安全.*",
            category=ErrorCategory.SECURITY,
            message_template="安全警告：{detail}",
            suggestion_template="请避免使用不安全的功能，或使用安全沙箱环境",
            severity="warning",
        ),
        ErrorPattern(
            pattern=r"禁止.*",
            category=ErrorCategory.SECURITY,
            message_template="安全限制：{detail}",
            suggestion_template="此操作在安全模式下被禁止，请修改代码或调整安全设置",
            severity="error",
        ),
        # 验证错误
        ErrorPattern(
            pattern=r"参数数量.*",
            category=ErrorCategory.VALIDATION,
            message_template="参数数量错误：{detail}",
            suggestion_template="请检查函数调用时提供的参数数量是否正确",
            severity="error",
        ),
        ErrorPattern(
            pattern=r"参数类型.*",
            category=ErrorCategory.VALIDATION,
            message_template="参数类型错误：{detail}",
            suggestion_template="请检查函数参数的类型是否符合要求",
            severity="error",
        ),
    ]

    @classmethod
    def enhance_error_message(
        cls, original_message: str, context: Optional[Dict] = None
    ) -> Tuple[str, str]:
        """增强错误消息

        Args:
            original_message: 原始错误消息
            context: 错误上下文信息（可选）

        Returns:
            Tuple[增强的错误消息, 修复建议]
        """
        if context is None:
            context = {}

        # 尝试匹配错误模式
        for pattern in cls.ERROR_PATTERNS:
            if re.search(pattern.pattern, original_message, re.IGNORECASE):
                # 提取错误详情
                detail = original_message

                # 如果有上下文信息，可以进一步处理
                if "detail" in context:
                    detail = context["detail"]

                # 生成增强消息
                enhanced_message = pattern.message_template.format(detail=detail)
                suggestion = pattern.suggestion_template

                # 添加严重性标签
                severity_label = {"error": "[错误]", "warning": "[警告]", "info": "[信息]"}.get(
                    pattern.severity, "[未知]"
                )

                enhanced_message = f"{severity_label} {enhanced_message}"

                return enhanced_message, suggestion

        # 如果没有匹配的模式，返回原始消息和通用建议
        return original_message, "请检查代码逻辑，或查阅文档获取更多帮助"

    @classmethod
    def get_category_suggestions(cls, category: ErrorCategory) -> List[str]:
        """获取特定错误类别的通用建议"""
        suggestions = {
            ErrorCategory.SYNTAX: [
                "检查代码语法，确保符合心语语言的语法规则",
                "检查括号、引号、冒号等是否匹配",
                "检查缩进是否正确（心语使用4个空格缩进）",
                "检查关键字拼写是否正确",
            ],
            ErrorCategory.SEMANTIC: ["检查变量是否在使用前已定义", "检查函数调用参数是否正确", "检查循环和条件语句的逻辑", "检查作用域是否正确"],
            ErrorCategory.TYPE: [
                "检查变量类型是否匹配操作符要求",
                "检查函数参数类型是否正确",
                "检查赋值语句两边的类型是否兼容",
                "考虑使用类型转换函数",
            ],
            ErrorCategory.NAME: ["检查变量名、函数名是否正确拼写", "检查名称是否在作用域内可见", "检查是否导入了必要的模块", "检查是否有拼写错误"],
            ErrorCategory.IMPORT: ["检查模块路径是否正确", "检查模块是否已安装", "检查导入语句的语法", "检查循环导入问题"],
            ErrorCategory.RUNTIME: [
                "检查边界条件（如数组索引、循环条件）",
                "检查资源使用（如内存、递归深度）",
                "检查输入数据的有效性",
                "添加异常处理代码",
            ],
            ErrorCategory.SECURITY: ["避免使用不安全的内置函数", "使用安全沙箱执行环境", "验证用户输入", "限制资源使用"],
            ErrorCategory.VALIDATION: ["检查函数调用参数的数量和类型", "验证输入数据的格式和范围", "检查前置条件和后置条件", "添加输入验证代码"],
            ErrorCategory.CONFIG: ["检查配置文件格式", "检查配置项的值是否有效", "检查环境变量设置", "检查权限设置"],
        }

        return suggestions.get(category, ["请检查代码逻辑"])

    @classmethod
    def format_error_with_context(
        cls,
        error_type: str,
        message: str,
        line: int,
        column: int,
        source_code: Optional[str] = None,
        context: Optional[Dict] = None,
    ) -> str:
        """格式化错误信息，包含上下文

        Args:
            error_type: 错误类型
            message: 错误消息
            line: 行号
            column: 列号
            source_code: 源代码（可选）
            context: 额外上下文信息（可选）

        Returns:
            格式化的错误信息
        """
        # 增强错误消息
        enhanced_message, suggestion = cls.enhance_error_message(message, context)

        # 构建错误信息
        lines = []
        lines.append(f"[位置] 第 {line} 行，第 {column} 列")
        lines.append(f"[类型] {error_type}")
        lines.append(f"[描述] {enhanced_message}")
        lines.append(f"[建议] {suggestion}")

        # 添加上下文代码
        if source_code:
            source_lines = source_code.split("\n")
            if 0 < line <= len(source_lines):
                # 显示错误行及其上下文
                start_line = max(1, line - 2)
                end_line = min(len(source_lines), line + 2)

                lines.append("\n[代码] 相关代码：")
                for i in range(start_line, end_line + 1):
                    prefix = ">>> " if i == line else "    "
                    lines.append(f"{prefix}{i:4d}: {source_lines[i - 1]}")

                # 添加指针
                if column > 0:
                    pointer_line = " " * (len(prefix) + 6 + column - 1) + "^"
                    lines.append(pointer_line)

        # 添加通用建议
        lines.append("\n[调试] 调试建议：")
        lines.append("  1. 仔细检查错误位置附近的代码")
        lines.append("  2. 确认变量名、函数名拼写正确")
        lines.append("  3. 检查语法结构（括号、引号、缩进）")
        lines.append("  4. 使用 print() 调试输出中间值")
        lines.append("  5. 查阅心语语言文档获取语法帮助")

        return "\n".join(lines)

    @classmethod
    def create_error_context(
        cls,
        error_type: str,
        line: int,
        column: int,
        source_snippet: str,
        expected: Optional[str] = None,
        actual: Optional[str] = None,
        hint: Optional[str] = None,
    ) -> Dict:
        """创建错误上下文信息

        Args:
            error_type: 错误类型
            line: 行号
            column: 列号
            source_snippet: 源代码片段
            expected: 期望的内容（可选）
            actual: 实际的内容（可选）
            hint: 额外提示（可选）

        Returns:
            错误上下文字典
        """
        context = {
            "type": error_type,
            "line": line,
            "column": column,
            "source": source_snippet,
            "expected": expected,
            "actual": actual,
            "hint": hint,
        }

        # 根据错误类型生成详细描述
        if expected and actual:
            context["detail"] = f"期望：{expected}，实际：{actual}"
        elif expected:
            context["detail"] = f"期望：{expected}"
        elif actual:
            context["detail"] = f"实际：{actual}"
        else:
            context["detail"] = source_snippet.strip()

        return context


# 错误消息模板
ERROR_TEMPLATES = {
    # 语法错误
    "syntax_error": {"message": "语法错误：{detail}", "suggestion": "请检查代码语法，确保符合心语语言的语法规则"},
    # 词法错误
    "lexical_error": {"message": "词法错误：{detail}", "suggestion": "请检查字符是否合法，或是否有拼写错误"},
    # 语义错误
    "semantic_error": {"message": "语义错误：{detail}", "suggestion": "请检查代码逻辑，确保变量使用和函数调用正确"},
    # 类型错误
    "type_error": {"message": "类型错误：{detail}", "suggestion": "请检查变量类型，确保操作符两边的类型兼容"},
    # 名称错误
    "name_error": {"message": "名称错误：{detail}", "suggestion": "请检查变量名、函数名是否正确拼写，或是否已定义"},
    # 导入错误
    "import_error": {"message": "导入错误：{detail}", "suggestion": "请检查模块路径是否正确，或模块是否已安装"},
    # 运行时错误
    "runtime_error": {"message": "运行时错误：{detail}", "suggestion": "请检查边界条件、资源使用和输入数据"},
    # 安全错误
    "security_error": {"message": "安全错误：{detail}", "suggestion": "请避免使用不安全的功能，或使用安全沙箱环境"},
    # 验证错误
    "validation_error": {"message": "验证错误：{detail}", "suggestion": "请检查参数数量、类型和取值范围"},
    # 配置错误
    "config_error": {"message": "配置错误：{detail}", "suggestion": "请检查配置文件格式和配置项的值"},
}


def get_error_template(error_type: str) -> Dict:
    """获取错误模板

    Args:
        error_type: 错误类型

    Returns:
        错误模板字典
    """
    return ERROR_TEMPLATES.get(error_type, {"message": "错误：{detail}", "suggestion": "请检查代码逻辑"})


def format_error(
    error_type: str,
    detail: str,
    line: int = 0,
    column: int = 0,
    source: Optional[str] = None,
    expected: Optional[str] = None,
    actual: Optional[str] = None,
) -> str:
    """格式化错误信息

    Args:
        error_type: 错误类型
        detail: 错误详情
        line: 行号
        column: 列号
        source: 源代码（可选）
        expected: 期望的内容（可选）
        actual: 实际的内容（可选）

    Returns:
        格式化的错误信息
    """
    template = get_error_template(error_type)

    # 构建详细描述
    if expected and actual:
        detail_with_context = f"{detail}（期望：{expected}，实际：{actual}）"
    elif expected:
        detail_with_context = f"{detail}（期望：{expected}）"
    elif actual:
        detail_with_context = f"{detail}（实际：{actual}）"
    else:
        detail_with_context = detail

    # 生成消息
    message = template["message"].format(detail=detail_with_context)
    suggestion = template["suggestion"]

    # 构建完整错误信息
    lines = []

    if line > 0 and column > 0:
        lines.append(f"位置：第 {line} 行，第 {column} 列")

    lines.append(f"错误：{message}")
    lines.append(f"建议：{suggestion}")

    # 添加上下文代码
    if source and line > 0:
        source_lines = source.split("\n")
        if line <= len(source_lines):
            lines.append("")
            lines.append("相关代码：")
            lines.append(f"  {line}: {source_lines[line - 1]}")
            if column > 0:
                lines.append(f"  {' ' * (len(str(line)) + 2 + column - 1)}^")

    return "\n".join(lines)


# 常用错误消息生成函数
def syntax_error(detail: str, line: int = 0, column: int = 0, source: Optional[str] = None) -> str:
    """生成语法错误消息"""
    return format_error("syntax_error", detail, line, column, source)


def lexical_error(detail: str, line: int = 0, column: int = 0, source: Optional[str] = None) -> str:
    """生成词法错误消息"""
    return format_error("lexical_error", detail, line, column, source)


def semantic_error(
    detail: str, line: int = 0, column: int = 0, source: Optional[str] = None
) -> str:
    """生成语义错误消息"""
    return format_error("semantic_error", detail, line, column, source)


def type_error(detail: str, line: int = 0, column: int = 0, source: Optional[str] = None) -> str:
    """生成类型错误消息"""
    return format_error("type_error", detail, line, column, source)


def name_error(detail: str, line: int = 0, column: int = 0, source: Optional[str] = None) -> str:
    """生成名称错误消息"""
    return format_error("name_error", detail, line, column, source)


def runtime_error(detail: str, line: int = 0, column: int = 0, source: Optional[str] = None) -> str:
    """生成运行时错误消息"""
    return format_error("runtime_error", detail, line, column, source)


def security_error(
    detail: str, line: int = 0, column: int = 0, source: Optional[str] = None
) -> str:
    """生成安全错误消息"""
    return format_error("security_error", detail, line, column, source)


def validation_error(
    detail: str, line: int = 0, column: int = 0, source: Optional[str] = None
) -> str:
    """生成验证错误消息"""
    return format_error("validation_error", detail, line, column, source)
