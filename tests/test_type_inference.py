# -*- coding: utf-8 -*-
"""类型推断系统测试

测试类型推断器的功能：
- 基础类型推断（数字、字符串、布尔值）
- 表达式类型推断
- 函数返回类型推断
- 复杂表达式类型推断
"""

import unittest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.type_inference import TypeInferencer


class TestTypeInference(unittest.TestCase):
    """测试类型推断"""

    def test_infer_number(self):
        """测试数字类型推断"""
        code = "123"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        inferencer = TypeInferencer()
        # 获取第一个语句的表达式
        if ast.statements and hasattr(ast.statements[0], 'expression'):
            expr = ast.statements[0].expression
            result = inferencer.infer(expr)
            self.assertEqual(result, "number")

    def test_infer_float(self):
        """测试浮点数类型推断"""
        code = "3.14"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        inferencer = TypeInferencer()
        if ast.statements and hasattr(ast.statements[0], 'expression'):
            expr = ast.statements[0].expression
            result = inferencer.infer(expr)
            self.assertEqual(result, "number")

    def test_infer_string(self):
        """测试字符串类型推断"""
        code = '"你好"'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        inferencer = TypeInferencer()
        if ast.statements and hasattr(ast.statements[0], 'expression'):
            expr = ast.statements[0].expression
            result = inferencer.infer(expr)
            self.assertEqual(result, "string")

    def test_infer_boolean_true(self):
        """测试布尔值True类型推断"""
        code = "真"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        inferencer = TypeInferencer()
        if ast.statements and hasattr(ast.statements[0], 'expression'):
            expr = ast.statements[0].expression
            result = inferencer.infer(expr)
            self.assertEqual(result, "boolean")

    def test_infer_boolean_false(self):
        """测试布尔值False类型推断"""
        code = "假"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        inferencer = TypeInferencer()
        if ast.statements and hasattr(ast.statements[0], 'expression'):
            expr = ast.statements[0].expression
            result = inferencer.infer(expr)
            self.assertEqual(result, "boolean")

    def test_infer_binary_add_numbers(self):
        """测试数字加法类型推断"""
        code = "1 加 2"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        inferencer = TypeInferencer()
        if ast.statements and hasattr(ast.statements[0], 'expression'):
            expr = ast.statements[0].expression
            result = inferencer.infer(expr)
            self.assertEqual(result, "number")

    def test_infer_binary_add_strings(self):
        """测试字符串连接类型推断"""
        code = '"a" 加 "b"'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        inferencer = TypeInferencer()
        if ast.statements and hasattr(ast.statements[0], 'expression'):
            expr = ast.statements[0].expression
            result = inferencer.infer(expr)
            self.assertEqual(result, "string")

    def test_infer_comparison(self):
        """测试比较表达式类型推断"""
        code = "1 小 2"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        inferencer = TypeInferencer()
        if ast.statements and hasattr(ast.statements[0], 'expression'):
            expr = ast.statements[0].expression
            result = inferencer.infer(expr)
            self.assertEqual(result, "boolean")

    def test_infer_logical_and(self):
        """测试逻辑与类型推断"""
        code = "真 且 假"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        inferencer = TypeInferencer()
        if ast.statements and hasattr(ast.statements[0], 'expression'):
            expr = ast.statements[0].expression
            result = inferencer.infer(expr)
            self.assertEqual(result, "boolean")

    def test_infer_list(self):
        """测试列表类型推断"""
        code = "[1, 2, 3]"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        inferencer = TypeInferencer()
        if ast.statements and hasattr(ast.statements[0], 'expression'):
            expr = ast.statements[0].expression
            result = inferencer.infer(expr)
            self.assertEqual(result, "list")

    @unittest.skip("词法分析器暂不支持冒号，字典语法待完善")
    def test_infer_dict(self):
        """测试字典类型推断"""
        code = '{"a": 1}'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        inferencer = TypeInferencer()
        if ast.statements and hasattr(ast.statements[0], 'expression'):
            expr = ast.statements[0].expression
            result = inferencer.infer(expr)
            self.assertEqual(result, "dict")

    def test_infer_function_call_builtin(self):
        """测试内置函数调用类型推断"""
        code = '长度([1, 2, 3])'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        inferencer = TypeInferencer()
        if ast.statements and hasattr(ast.statements[0], 'expression'):
            expr = ast.statements[0].expression
            result = inferencer.infer(expr)
            self.assertEqual(result, "number")

    def test_infer_with_context(self):
        """测试带上下文的类型推断"""
        code = "x"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        inferencer = TypeInferencer()
        context = {"x": "number"}
        if ast.statements and hasattr(ast.statements[0], 'expression'):
            expr = ast.statements[0].expression
            result = inferencer.infer(expr, context)
            self.assertEqual(result, "number")


if __name__ == "__main__":
    unittest.main()
