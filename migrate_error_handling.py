#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
错误处理系统迁移脚本

将现有的错误处理系统迁移到新的统一错误处理系统
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 定义错误代码枚举
from enum import Enum, auto

from src.utils.error_utils import (
    BaseError,
    ErrorContext,
    ErrorInfo,
    ErrorRegistry,
    ErrorSeverity,
    create_error,
    error_handler,
    format_exception,
    get_error_info,
    register_error,
    retry_on_error,
    safe_execute,
)


class ErrorCode(Enum):
    """错误代码枚举"""

    # 词法错误
    LEXER_INVALID_CHAR = auto()
    LEXER_UNTERMINATED_STRING = auto()
    LEXER_INVALID_NUMBER = auto()
    LEXER_UNKNOWN_SYMBOL = auto()

    # 语法错误
    SYNTAX_UNEXPECTED_TOKEN = auto()
    SYNTAX_MISSING_TOKEN = auto()
    SYNTAX_INVALID_TOKEN = auto()
    SYNTAX_INDENT_ERROR = auto()
    SYNTAX_DEDENT_ERROR = auto()

    # 语义错误
    SEMANTIC_UNDEFINED_VARIABLE = auto()
    SEMANTIC_DUPLICATE_DEFINITION = auto()
    SEMANTIC_TYPE_MISMATCH = auto()
    SEMANTIC_INVALID_OPERATION = auto()
    SEMANTIC_INVALID_RETURN = auto()

    # 类型错误
    TYPE_INCOMPATIBLE = auto()
    TYPE_NOT_SUPPORTED = auto()
    TYPE_CONVERSION_ERROR = auto()
    TYPE_INFERENCE_FAILED = auto()

    # 名称错误
    NAME_NOT_FOUND = auto()
    NAME_AMBIGUOUS = auto()
    NAME_RESERVED = auto()
    NAME_INVALID = auto()

    # 运行时错误
    RUNTIME_DIVISION_BY_ZERO = auto()
    RUNTIME_INDEX_OUT_OF_RANGE = auto()
    RUNTIME_RECURSION_DEPTH = auto()
    RUNTIME_MEMORY_ERROR = auto()
    RUNTIME_TIMEOUT = auto()
    RUNTIME_ERROR = auto()  # 通用运行时错误


# 注册错误信息
def register_all_errors():
    """注册所有错误信息"""

    # 词法错误
    register_error(
        ErrorInfo(
            code=ErrorCode.LEXER_INVALID_CHAR.name,
            message="无效字符: {char}",
            severity=ErrorSeverity.ERROR,
            suggestion="请检查字符编码或使用有效字符",
            category="lexer",
        )
    )

    register_error(
        ErrorInfo(
            code=ErrorCode.LEXER_UNTERMINATED_STRING,
            message="未终止的字符串字面量",
            severity=ErrorSeverity.ERROR,
            suggestion="请添加匹配的引号",
            category="lexer",
        )
    )

    register_error(
        ErrorInfo(
            code=ErrorCode.LEXER_INVALID_NUMBER,
            message="无效的数字字面量: {value}",
            severity=ErrorSeverity.ERROR,
            suggestion="请使用有效的数字格式",
            category="lexer",
        )
    )

    register_error(
        ErrorInfo(
            code=ErrorCode.LEXER_UNKNOWN_SYMBOL,
            message="未知符号: {symbol}",
            severity=ErrorSeverity.ERROR,
            suggestion="请检查拼写或导入相应的模块",
            category="lexer",
        )
    )

    # 语法错误
    register_error(
        ErrorInfo(
            code=ErrorCode.SYNTAX_UNEXPECTED_TOKEN,
            message="意外的标记: {token}，期望: {expected}",
            severity=ErrorSeverity.ERROR,
            suggestion="请检查语法结构",
            category="parser",
        )
    )

    register_error(
        ErrorInfo(
            code=ErrorCode.SYNTAX_MISSING_TOKEN,
            message="缺少标记: {token}",
            severity=ErrorSeverity.ERROR,
            suggestion="请添加缺失的标记",
            category="parser",
        )
    )

    register_error(
        ErrorInfo(
            code=ErrorCode.SYNTAX_INVALID_TOKEN,
            message="无效的标记: {token}",
            severity=ErrorSeverity.ERROR,
            suggestion="请使用有效的标记",
            category="parser",
        )
    )

    register_error(
        ErrorInfo(
            code=ErrorCode.SYNTAX_INDENT_ERROR,
            message="缩进错误",
            severity=ErrorSeverity.ERROR,
            suggestion="请检查缩进级别",
            category="parser",
        )
    )

    register_error(
        ErrorInfo(
            code=ErrorCode.SYNTAX_DEDENT_ERROR,
            message="反缩进错误",
            severity=ErrorSeverity.ERROR,
            suggestion="请检查缩进级别",
            category="parser",
        )
    )

    # 语义错误
    register_error(
        ErrorInfo(
            code=ErrorCode.SEMANTIC_UNDEFINED_VARIABLE,
            message="未定义的变量: {name}",
            severity=ErrorSeverity.ERROR,
            suggestion="请先定义变量或检查变量名拼写",
            category="semantic",
        )
    )

    register_error(
        ErrorInfo(
            code=ErrorCode.SEMANTIC_DUPLICATE_DEFINITION,
            message="重复定义: {name}",
            severity=ErrorSeverity.ERROR,
            suggestion="请使用不同的名称或删除重复定义",
            category="semantic",
        )
    )

    register_error(
        ErrorInfo(
            code=ErrorCode.SEMANTIC_TYPE_MISMATCH,
            message="类型不匹配: {actual} 不能转换为 {expected}",
            severity=ErrorSeverity.ERROR,
            suggestion="请检查类型或进行类型转换",
            category="semantic",
        )
    )

    register_error(
        ErrorInfo(
            code=ErrorCode.SEMANTIC_INVALID_OPERATION,
            message="无效操作: {operation}",
            severity=ErrorSeverity.ERROR,
            suggestion="请使用有效的操作",
            category="semantic",
        )
    )

    register_error(
        ErrorInfo(
            code=ErrorCode.SEMANTIC_INVALID_RETURN,
            message="无效的返回语句",
            severity=ErrorSeverity.ERROR,
            suggestion="请检查返回类型和位置",
            category="semantic",
        )
    )

    # 类型错误
    register_error(
        ErrorInfo(
            code=ErrorCode.TYPE_INCOMPATIBLE,
            message="类型不兼容: {type1} 和 {type2}",
            severity=ErrorSeverity.ERROR,
            suggestion="请使用兼容的类型",
            category="type",
        )
    )

    register_error(
        ErrorInfo(
            code=ErrorCode.TYPE_NOT_SUPPORTED,
            message="不支持的类型: {type}",
            severity=ErrorSeverity.ERROR,
            suggestion="请使用支持的类型",
            category="type",
        )
    )

    register_error(
        ErrorInfo(
            code=ErrorCode.TYPE_CONVERSION_ERROR,
            message="类型转换错误: 无法将 {from_type} 转换为 {to_type}",
            severity=ErrorSeverity.ERROR,
            suggestion="请检查类型转换逻辑",
            category="type",
        )
    )

    register_error(
        ErrorInfo(
            code=ErrorCode.TYPE_INFERENCE_FAILED,
            message="类型推断失败",
            severity=ErrorSeverity.ERROR,
            suggestion="请显式指定类型",
            category="type",
        )
    )

    # 名称错误
    register_error(
        ErrorInfo(
            code=ErrorCode.NAME_NOT_FOUND,
            message="名称未找到: {name}",
            severity=ErrorSeverity.ERROR,
            suggestion="请检查名称拼写或导入相应的模块",
            category="name",
        )
    )

    register_error(
        ErrorInfo(
            code=ErrorCode.NAME_AMBIGUOUS,
            message="名称歧义: {name}",
            severity=ErrorSeverity.ERROR,
            suggestion="请使用完全限定名",
            category="name",
        )
    )

    register_error(
        ErrorInfo(
            code=ErrorCode.NAME_RESERVED,
            message="保留名称: {name}",
            severity=ErrorSeverity.ERROR,
            suggestion="请使用其他名称",
            category="name",
        )
    )

    register_error(
        ErrorInfo(
            code=ErrorCode.NAME_INVALID,
            message="无效名称: {name}",
            severity=ErrorSeverity.ERROR,
            suggestion="请使用有效的标识符",
            category="name",
        )
    )

    # 运行时错误
    register_error(
        ErrorInfo(
            code=ErrorCode.RUNTIME_DIVISION_BY_ZERO,
            message="除以零错误",
            severity=ErrorSeverity.ERROR,
            suggestion="请检查除数是否为零",
            category="runtime",
        )
    )

    register_error(
        ErrorInfo(
            code=ErrorCode.RUNTIME_INDEX_OUT_OF_RANGE,
            message="索引超出范围: 索引 {index}，长度 {length}",
            severity=ErrorSeverity.ERROR,
            suggestion="请检查索引值",
            category="runtime",
        )
    )

    register_error(
        ErrorInfo(
            code=ErrorCode.RUNTIME_RECURSION_DEPTH,
            message="递归深度超出限制: {depth}",
            severity=ErrorSeverity.ERROR,
            suggestion="请优化递归逻辑或增加递归深度限制",
            category="runtime",
        )
    )

    register_error(
        ErrorInfo(
            code=ErrorCode.RUNTIME_MEMORY_ERROR,
            message="内存错误",
            severity=ErrorSeverity.ERROR,
            suggestion="请检查内存使用或优化算法",
            category="runtime",
        )
    )

    register_error(
        ErrorInfo(
            code=ErrorCode.RUNTIME_TIMEOUT,
            message="操作超时",
            severity=ErrorSeverity.ERROR,
            suggestion="请优化算法或增加超时时间",
            category="runtime",
        )
    )


# 错误类型映射
def map_error_type_to_severity(error_type):
    """将错误类型映射到严重程度"""
    error_type_to_severity = {
        "lexer": ErrorSeverity.ERROR,
        "parser": ErrorSeverity.ERROR,
        "semantic": ErrorSeverity.ERROR,
        "type": ErrorSeverity.ERROR,
        "name": ErrorSeverity.ERROR,
        "runtime": ErrorSeverity.ERROR,
    }
    return error_type_to_severity.get(error_type, ErrorSeverity.ERROR)


# 创建兼容的ErrorHandler类
class EnhancedErrorHandler:
    """增强的错误处理器，兼容新旧系统"""

    def __init__(self):
        self.errors = []
        self.registry = ErrorRegistry()
        register_all_errors()

    def report_with_code(self, error_code, line, column, source=None, **kwargs):
        """使用错误代码报告错误"""
        # 创建错误上下文
        context = ErrorContext(
            line=line, column=column, file_path=source, function_name=None, variables=kwargs
        )

        # 创建错误
        error = create_error(
            code=error_code.name if hasattr(error_code, "name") else error_code,
            context=context,
            **kwargs,
        )

        self.errors.append(error)
        return error

    def report(self, error_type, message, line, column, source=None, suggestion=None):
        """报告错误（兼容旧接口）"""
        # 将错误类型映射到错误代码
        error_code_map = {
            "LEXER_ERROR": ErrorCode.LEXER_INVALID_CHAR,
            "PARSER_ERROR": ErrorCode.SYNTAX_UNEXPECTED_TOKEN,
            "SEMANTIC_ERROR": ErrorCode.SEMANTIC_UNDEFINED_VARIABLE,
            "RUNTIME_ERROR": ErrorCode.RUNTIME_DIVISION_BY_ZERO,
        }

        error_code = error_code_map.get(error_type.name, ErrorCode.RUNTIME_ERROR)

        # 创建错误上下文
        context = ErrorContext(
            line=line,
            column=column,
            file_path=source,
            function_name=None,
            variables={"message": message},
        )

        # 创建错误
        error = BaseError(
            message=message,
            code=error_code.name,
            severity=ErrorSeverity.ERROR,
            context=context,
            suggestion=suggestion,
            stack_trace=None,
        )

        self.errors.append(error)
        return error

    def get_errors(self):
        """获取所有错误"""
        return self.errors

    def format_error(self, index):
        """格式化错误"""
        if index < 0 or index >= len(self.errors):
            return ""
        return str(self.errors[index])

    def format_all_errors(self):
        """格式化所有错误"""
        if not self.errors:
            return "✅ 编译成功，没有发现错误"

        result = []
        for i, error in enumerate(self.errors, 1):
            result.append(f"错误 {i}:")
            result.append(str(error))
            if i < len(self.errors):
                result.append("\n" + "=" * 50 + "\n")

        return "\n".join(result)

    def get_statistics(self):
        """获取错误统计"""
        stats = {}
        for error in self.errors:
            category = error.code.split("_")[0].lower() if "_" in error.code else "unknown"
            if category not in stats:
                stats[category] = 0
            stats[category] += 1
        return stats

    def has_errors(self):
        """检查是否有错误"""
        return len(self.errors) > 0

    def clear(self):
        """清除所有错误"""
        self.errors.clear()

    def print_errors(self):
        """打印所有错误"""
        print(self.format_all_errors())

    def print_summary(self):
        """打印错误摘要"""
        if not self.errors:
            print("[OK] 编译成功，没有发现错误")
            return

        stats = self.get_statistics()
        print("[统计] 错误摘要：")
        print(f"  总计：{len(self.errors)} 个错误")

        for category, count in stats.items():
            category_name = {
                "lexer": "词法错误",
                "parser": "语法错误",
                "semantic": "语义错误",
                "type": "类型错误",
                "name": "名称错误",
                "runtime": "运行时错误",
            }.get(category, category)
            print(f"  [X] {category_name}: {count} 个")


def main():
    """主函数"""
    print("=" * 60)
    print("错误处理系统迁移工具")
    print("=" * 60)

    # 注册所有错误
    register_all_errors()
    print("[OK] 已注册所有错误代码")

    # 测试错误处理器
    handler = EnhancedErrorHandler()

    # 测试使用错误代码报告错误
    print("\n测试使用错误代码报告错误：")
    error1 = handler.report_with_code(
        ErrorCode.LEXER_INVALID_CHAR, line=10, column=5, source="test.cp", char="@"
    )
    print(f"  错误1: {error1}")

    # 测试使用旧接口报告错误
    print("\n测试使用旧接口报告错误：")
    from src.error_handling import ErrorType

    error2 = handler.report(
        ErrorType.PARSER_ERROR,
        message="意外的标记: ';'，期望: ')'",
        line=20,
        column=15,
        source="test.cp",
        suggestion="请检查语法结构",
    )
    print(f"  错误2: {error2}")

    # 测试错误统计
    print("\n测试错误统计：")
    stats = handler.get_statistics()
    print(f"  错误统计: {stats}")

    # 测试错误格式化
    print("\n测试错误格式化：")
    print(handler.format_all_errors())

    # 测试错误摘要
    print("\n测试错误摘要：")
    handler.print_summary()

    print("\n" + "=" * 60)
    print("迁移测试完成！")
    print("=" * 60)

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
