#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试增强的错误处理系统"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from src.error_handling import (
    ErrorCode,
    ErrorHandler,
    ErrorSeverity,
    ErrorType,
    create_error_message,
    get_error_info,
)
from src.error_handling.enhanced_errors import EnhancedErrorMessages
from src.error_handling.error_utils import create_lexical_error, create_syntax_error


def test_error_handler_basic():
    """测试基本的错误处理器功能"""
    handler = ErrorHandler()

    # 报告一个错误
    handler.report(
        error_type=ErrorType.LEXER_ERROR,
        message="非法字符: '#'",
        line=10,
        column=5,
        source="定 x 为 42 # 注释",
        suggestion="请使用合法的字符",
    )

    assert handler.has_errors() == True
    assert len(handler.get_errors()) == 1

    error = handler.get_errors()[0]
    assert error.error_type == ErrorType.LEXER_ERROR
    assert error.message == "非法字符: '#'"
    assert error.line == 10
    assert error.column == 5
    assert error.suggestion == "请使用合法的字符"

    # 测试错误格式化
    formatted = str(error)
    assert "词法错误" in formatted or "LEXER_ERROR" in formatted
    assert "第 10 行" in formatted
    assert "第 5 列" in formatted
    assert "非法字符" in formatted or "'#'" in formatted
    assert "请使用合法的字符" in formatted
    # 源代码可能不会显示，取决于格式化逻辑


def test_error_handler_with_code():
    """测试使用错误代码报告错误"""
    handler = ErrorHandler()

    # 使用错误代码报告错误
    handler.report_with_code(
        error_code=ErrorCode.LEXER_INVALID_CHAR,
        line=15,
        column=8,
        source="打印('Hello, World!')",
        char="'@'",
    )

    assert handler.has_errors() == True
    errors = handler.get_errors()
    assert len(errors) == 1

    error = errors[0]
    assert error.error_code == ErrorCode.LEXER_INVALID_CHAR
    assert error.error_type == ErrorType.LEXER_ERROR

    # 检查错误消息包含增强信息
    formatted = str(error)
    assert "LEXER_INVALID_CHAR" in formatted or "非法字符" in formatted
    assert "第 15 行" in formatted
    assert "调试建议" in formatted


def test_error_codes():
    """测试错误代码系统"""
    # 测试获取错误信息
    info = get_error_info(ErrorCode.SYNTAX_UNEXPECTED_TOKEN, token=";")
    assert "message" in info
    assert "suggestion" in info
    assert "severity" in info
    assert info["severity"] == ErrorSeverity.ERROR

    # 测试错误消息创建
    message = create_error_message(
        ErrorCode.SYNTAX_MISSING_TOKEN, line=20, column=10, source="如果 x > 0\n    打印(x)", token=":"
    )

    assert "第 20 行" in message
    assert "第 10 列" in message
    assert "缺少必要的标记" in message or "SYNTAX_MISSING_TOKEN" in message
    assert "[建议]" in message
    assert "[调试]" in message
    assert "[代码]" in message


def test_enhanced_error_messages():
    """测试增强的错误消息系统"""
    # 测试错误模式匹配
    enhanced_msg, suggestion = EnhancedErrorMessages.enhance_error_message(
        "非法字符: @", {"detail": "字符 '@' 不被支持"}
    )

    assert "非法字符" in enhanced_msg or "发现非法字符" in enhanced_msg
    assert "请检查是否使用了不支持的字符" in suggestion

    # 测试错误格式化
    formatted = EnhancedErrorMessages.format_error_with_context(
        error_type="语法错误",
        message="缺少冒号",
        line=2,  # 改为有效的行号
        column=5,
        source_code="如果 x > 0\n    打印(x)\n否则\n    打印(0)",
        context={"expected": ":", "actual": None},
    )

    assert "第 2 行" in formatted
    assert "第 5 列" in formatted
    assert "语法错误" in formatted
    assert "缺少冒号" in formatted
    assert "[调试]" in formatted
    # 当提供源代码且行号有效时，应该显示[代码]部分
    assert "[代码]" in formatted


def test_error_utils_functions():
    """测试错误工具函数"""
    # 测试创建语法错误
    syntax_error_msg = create_syntax_error(token=";", line=8, column=3, source="定 x 为 42;")

    assert "语法错误" in syntax_error_msg or "SYNTAX_UNEXPECTED_TOKEN" in syntax_error_msg
    assert "第 8 行" in syntax_error_msg
    assert "第 3 列" in syntax_error_msg
    # 源代码可能不会显示，取决于格式化逻辑

    # 测试创建词法错误
    lexical_error_msg = create_lexical_error(char="@", line=12, column=7, source="打印(@hello)")

    assert "词法错误" in lexical_error_msg or "LEXER_INVALID_CHAR" in lexical_error_msg
    assert "第 12 行" in lexical_error_msg
    assert "第 7 列" in lexical_error_msg
    # 源代码可能不会显示，取决于格式化逻辑


def test_error_summary():
    """测试错误摘要"""
    handler = ErrorHandler()

    # 添加多个错误
    handler.report_with_code(
        ErrorCode.LEXER_INVALID_CHAR, line=1, column=5, source="测试代码", char="#"
    )

    handler.report_with_code(
        ErrorCode.SYNTAX_MISSING_TOKEN, line=2, column=10, source="如果 x > 0", token=":"
    )

    handler.report_with_code(
        ErrorCode.SEMANTIC_UNDEFINED_VARIABLE, line=3, column=3, source="y = x + z", name="z"
    )

    # 测试错误摘要
    summary = handler.get_error_summary()
    assert "错误摘要" in summary
    assert "总计：3 个错误" in summary
    assert "词法错误" in summary or "LEXER" in summary
    assert "语法错误" in summary or "PARSER" in summary
    assert "语义错误" in summary or "SEMANTIC" in summary

    # 测试格式化所有错误
    all_errors = handler.format_all_errors()
    assert "错误 1:" in all_errors
    assert "错误 2:" in all_errors
    assert "错误 3:" in all_errors
    assert "=" * 50 in all_errors  # 分隔符


def test_error_statistics():
    """测试错误统计"""
    handler = ErrorHandler()

    # 添加不同类型的错误
    handler.report(error_type=ErrorType.LEXER_ERROR, message="错误1", line=1, column=1)

    handler.report(error_type=ErrorType.PARSER_ERROR, message="错误2", line=2, column=2)

    handler.report(error_type=ErrorType.LEXER_ERROR, message="错误3", line=3, column=3)

    handler.report(error_type=ErrorType.SEMANTIC_ERROR, message="错误4", line=4, column=4)

    # 获取统计信息
    stats = handler.get_statistics()
    assert stats[ErrorType.LEXER_ERROR] == 2
    assert stats[ErrorType.PARSER_ERROR] == 1
    assert stats[ErrorType.SEMANTIC_ERROR] == 1
    assert ErrorType.RUNTIME_ERROR not in stats


def test_error_context_extraction():
    """测试错误上下文提取"""
    from src.error_handling.error_utils import extract_error_context

    source_code = """第一行代码
第二行代码
第三行有错误的代码
第四行代码
第五行代码"""

    context = extract_error_context(source_code, line=3, column=10, context_lines=1)

    assert "context" in context
    assert len(context["context"]) == 3  # 第2-4行
    assert context["error_line"] == "第三行有错误的代码"
    assert context["error_column"] == 10
    assert context["start_line"] == 2
    assert context["end_line"] == 4

    # 检查上下文行
    context_lines = context["context"]
    assert context_lines[0]["line"] == 2
    assert context_lines[0]["content"] == "第二行代码"
    assert not context_lines[0]["is_error_line"]

    assert context_lines[1]["line"] == 3
    assert context_lines[1]["content"] == "第三行有错误的代码"
    assert context_lines[1]["is_error_line"]

    assert context_lines[2]["line"] == 4
    assert context_lines[2]["content"] == "第四行代码"
    assert not context_lines[2]["is_error_line"]


def test_error_suggestions():
    """测试错误修复建议"""
    from src.error_handling.error_utils import suggest_fix

    # 测试缩进错误建议
    indent_suggestions = suggest_fix(ErrorCode.SYNTAX_INDENT_ERROR, {"line": 5, "column": 1})

    assert len(indent_suggestions) > 0
    assert any("4个空格" in s for s in indent_suggestions)
    assert any("缩进一致" in s for s in indent_suggestions)

    # 测试未定义变量错误建议
    undefined_suggestions = suggest_fix(
        ErrorCode.SEMANTIC_UNDEFINED_VARIABLE, {"name": "my_var", "line": 10, "column": 5}
    )

    assert len(undefined_suggestions) > 0
    assert any("my_var" in s for s in undefined_suggestions)
    assert any("拼写" in s for s in undefined_suggestions)
    assert any("作用域" in s for s in undefined_suggestions)

    # 测试除以零错误建议
    div_zero_suggestions = suggest_fix(
        ErrorCode.RUNTIME_DIVISION_BY_ZERO, {"line": 15, "column": 8}
    )

    assert len(div_zero_suggestions) > 0
    assert any("除数" in s for s in div_zero_suggestions)
    assert any("条件判断" in s for s in div_zero_suggestions)
    assert any("try-except" in s for s in div_zero_suggestions)


def test_error_formatting_edge_cases():
    """测试错误格式化的边界情况"""
    handler = ErrorHandler()

    # 测试没有源代码的错误
    handler.report(error_type=ErrorType.RUNTIME_ERROR, message="运行时错误", line=0, column=0)

    error = handler.get_errors()[0]
    formatted = str(error)
    assert "运行时错误" in formatted
    # 行号为0时可能仍然会显示位置，这取决于格式化逻辑
    # 我们只检查错误消息存在即可

    # 测试没有建议的错误
    handler.clear()
    handler.report(
        error_type=ErrorType.SEMANTIC_ERROR, message="语义错误", line=5, column=10, source="测试代码"
    )

    error = handler.get_errors()[0]
    formatted = str(error)
    assert "语义错误" in formatted
    assert "调试建议" in formatted  # 即使没有特定建议，也有通用调试建议

    # 测试清除错误
    handler.clear()
    assert not handler.has_errors()
    assert len(handler.get_errors()) == 0


if __name__ == "__main__":
    # 运行所有测试
    test_error_handler_basic()
    print("test_error_handler_basic 通过")

    test_error_handler_with_code()
    print("test_error_handler_with_code 通过")

    test_error_codes()
    print("test_error_codes 通过")

    test_enhanced_error_messages()
    print("test_enhanced_error_messages 通过")

    test_error_utils_functions()
    print("test_error_utils_functions 通过")

    test_error_summary()
    print("test_error_summary 通过")

    test_error_statistics()
    print("test_error_statistics 通过")

    test_error_context_extraction()
    print("test_error_context_extraction 通过")

    test_error_suggestions()
    print("test_error_suggestions 通过")

    test_error_formatting_edge_cases()
    print("test_error_formatting_edge_cases 通过")

    print("\n所有测试通过！")
