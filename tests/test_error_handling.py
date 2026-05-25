# -*- coding: utf-8 -*-
"""错误处理测试

测试错误处理器的功能：
- 错误报告
- 错误格式化
- 错误统计
"""

import unittest
from src.error_handling import ErrorHandler, ErrorType


class TestErrorHandler(unittest.TestCase):
    """测试错误处理器"""

    def test_error_handler_creation(self):
        """测试错误处理器创建"""
        handler = ErrorHandler()
        self.assertEqual(len(handler.get_errors()), 0)

    def test_report_lexer_error(self):
        """测试报告词法错误"""
        handler = ErrorHandler()
        handler.report(ErrorType.LEXER_ERROR, "Unexpected character", line=1, column=5)

        errors = handler.get_errors()
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].error_type, ErrorType.LEXER_ERROR)
        self.assertEqual(errors[0].message, "Unexpected character")
        self.assertEqual(errors[0].line, 1)
        self.assertEqual(errors[0].column, 5)

    def test_report_parser_error(self):
        """测试报告语法错误"""
        handler = ErrorHandler()
        handler.report(ErrorType.PARSER_ERROR, "Expected ')'", line=3, column=10)

        errors = handler.get_errors()
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].error_type, ErrorType.PARSER_ERROR)

    def test_report_semantic_error(self):
        """测试报告语义错误"""
        handler = ErrorHandler()
        handler.report(ErrorType.SEMANTIC_ERROR, "Undefined variable", line=5, column=2)

        errors = handler.get_errors()
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].error_type, ErrorType.SEMANTIC_ERROR)

    def test_multiple_errors(self):
        """测试多个错误"""
        handler = ErrorHandler()
        handler.report(ErrorType.LEXER_ERROR, "Error 1", line=1, column=1)
        handler.report(ErrorType.PARSER_ERROR, "Error 2", line=2, column=2)
        handler.report(ErrorType.SEMANTIC_ERROR, "Error 3", line=3, column=3)

        errors = handler.get_errors()
        self.assertEqual(len(errors), 3)

    def test_error_formatting(self):
        """测试错误格式化"""
        handler = ErrorHandler()
        handler.report(
            ErrorType.PARSER_ERROR,
            "Expected ')'",
            line=3,
            column=10,
            source="印(1加2。"
        )

        formatted = handler.format_error(0)
        self.assertIn("第 3 行", formatted)
        self.assertIn("第 10 列", formatted)
        self.assertIn("Expected ')'", formatted)

    def test_error_formatting_with_context(self):
        """测试带上下文的错误格式化"""
        handler = ErrorHandler()
        source = "定 x = 。"
        handler.report(
            ErrorType.PARSER_ERROR,
            "Expected expression",
            line=1,
            column=6,
            source=source
        )

        formatted = handler.format_error(0)
        self.assertIn("第 1 行", formatted)
        self.assertIn("第 6 列", formatted)

    def test_error_statistics(self):
        """测试错误统计"""
        handler = ErrorHandler()
        handler.report(ErrorType.LEXER_ERROR, "Error 1", line=1, column=1)
        handler.report(ErrorType.LEXER_ERROR, "Error 2", line=2, column=2)
        handler.report(ErrorType.PARSER_ERROR, "Error 3", line=3, column=3)

        stats = handler.get_statistics()
        self.assertEqual(stats[ErrorType.LEXER_ERROR], 2)
        self.assertEqual(stats[ErrorType.PARSER_ERROR], 1)

    def test_has_errors(self):
        """测试是否有错误"""
        handler = ErrorHandler()
        self.assertFalse(handler.has_errors())

        handler.report(ErrorType.LEXER_ERROR, "Error", line=1, column=1)
        self.assertTrue(handler.has_errors())

    def test_clear_errors(self):
        """测试清除错误"""
        handler = ErrorHandler()
        handler.report(ErrorType.LEXER_ERROR, "Error", line=1, column=1)
        self.assertEqual(len(handler.get_errors()), 1)

        handler.clear()
        self.assertEqual(len(handler.get_errors()), 0)


if __name__ == "__main__":
    unittest.main()
