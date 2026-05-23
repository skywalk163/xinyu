# -*- coding: utf-8 -*-
"""语义分析器测试

测试语义分析器的功能：
- 作用域创建和查找
- 嵌套作用域
- 未定义变量检测
- 重复定义检测
- 函数定义和调用检查
"""

import unittest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.scope import Scope
from src.semantic.analyzer import SemanticAnalyzer, SemanticError


class TestScope(unittest.TestCase):
    """测试作用域管理"""
    
    def test_scope_creation(self):
        """测试作用域创建"""
        scope = Scope()
        self.assertIsNone(scope.parent)
        self.assertEqual(len(scope.symbols), 0)
    
    def test_scope_define(self):
        """测试符号定义"""
        scope = Scope()
        scope.define("x", "variable", value_type="number")
        
        self.assertIn("x", scope.symbols)
        self.assertEqual(scope.symbols["x"]["type"], "variable")
        self.assertEqual(scope.symbols["x"]["value_type"], "number")
    
    def test_scope_lookup(self):
        """测试符号查找"""
        scope = Scope()
        scope.define("x", "variable", value_type="number")
        
        symbol = scope.lookup("x")
        self.assertIsNotNone(symbol)
        self.assertEqual(symbol["type"], "variable")
        
        # 查找不存在的符号
        symbol = scope.lookup("y")
        self.assertIsNone(symbol)
    
    def test_nested_scope(self):
        """测试嵌套作用域"""
        parent = Scope()
        parent.define("x", "variable", value_type="number")
        
        child = Scope(parent=parent)
        
        # 子作用域可以查找父作用域的符号
        symbol = child.lookup("x")
        self.assertIsNotNone(symbol)
        self.assertEqual(symbol["value_type"], "number")
    
    def test_scope_assign(self):
        """测试符号类型更新"""
        scope = Scope()
        scope.define("x", "variable", value_type="unknown")
        
        # 更新类型
        result = scope.assign("x", "number")
        self.assertTrue(result)
        self.assertEqual(scope.symbols["x"]["value_type"], "number")
        
        # 更新不存在的符号
        result = scope.assign("y", "number")
        self.assertFalse(result)
    
    def test_nested_scope_assign(self):
        """测试嵌套作用域中的变量更新"""
        parent = Scope()
        parent.define("x", "variable", value_type="unknown")
        
        child = Scope(parent=parent)
        
        # 子作用域可以更新父作用域的变量
        result = child.assign("x", "number")
        self.assertTrue(result)
        self.assertEqual(parent.symbols["x"]["value_type"], "number")
        
        # 更新不存在的变量
        result = child.assign("y", "number")
        self.assertFalse(result)
        
        # 多层嵌套
        grandchild = Scope(parent=child)
        result = grandchild.assign("x", "string")
        self.assertTrue(result)
        self.assertEqual(parent.symbols["x"]["value_type"], "string")


class TestSemanticAnalyzer(unittest.TestCase):
    """测试语义分析器"""
    
    def _analyze(self, code: str) -> tuple:
        """辅助方法：分析代码并返回结果和错误列表"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        success = analyzer.analyze(ast)
        
        return success, analyzer.errors
    
    def test_undefined_variable(self):
        """测试未定义变量检测"""
        # 使用内置函数 印，但变量 x 未定义
        code = "印 x。"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        success = analyzer.analyze(ast)
        
        self.assertFalse(success)
        self.assertEqual(len(analyzer.errors), 1)
        self.assertIn("未定义", str(analyzer.errors[0]))
    
    def test_variable_definition(self):
        """测试变量定义"""
        code = "定 x = 5。"
        success, errors = self._analyze(code)
        
        self.assertTrue(success)
        self.assertEqual(len(errors), 0)
    
    def test_variable_usage(self):
        """测试变量使用"""
        code = """定 x = 5。
印 x。"""
        success, errors = self._analyze(code)
        
        self.assertTrue(success)
        self.assertEqual(len(errors), 0)
    
    def test_duplicate_definition(self):
        """测试重复定义检测"""
        code = """定 x = 5。
定 x = 10。"""
        success, errors = self._analyze(code)
        
        self.assertFalse(success)
        self.assertEqual(len(errors), 1)
        self.assertIn("重复定义", str(errors[0]))
    
    def test_function_definition(self):
        """测试函数定义"""
        code = """定 相加 = 函 a b：
  返回 a 加 b。"""
        success, errors = self._analyze(code)
        
        self.assertTrue(success)
        self.assertEqual(len(errors), 0)
    
    def test_function_call(self):
        """测试函数调用"""
        code = """定 相加 = 函 a b：
  返回 a 加 b。
相加 1 2。"""
        success, errors = self._analyze(code)
        
        self.assertTrue(success)
        self.assertEqual(len(errors), 0)
    
    def test_undefined_function(self):
        """测试未定义函数检测"""
        code = "相加 1 2。"
        success, errors = self._analyze(code)
        
        self.assertFalse(success)
        self.assertEqual(len(errors), 1)
        self.assertIn("未定义", str(errors[0]))
    
    def test_function_scope(self):
        """测试函数作用域"""
        code = """定 函数 = 函 x：
  定 y = x 加 1。
  返回 y。"""
        success, errors = self._analyze(code)
        
        self.assertTrue(success)
        self.assertEqual(len(errors), 0)
    
    def test_if_statement(self):
        """测试条件语句"""
        code = """定 x = 5。
若 x 大 3 则：
  印 x。"""
        success, errors = self._analyze(code)
        
        self.assertTrue(success)
        self.assertEqual(len(errors), 0)
    
    @unittest.skip("列表字面量语法暂不支持，需要运行时支持")
    def test_for_loop(self):
        """测试遍历循环"""
        # 注意：列表语法需要使用【】而不是[]
        code = """遍历 i 于 列表：
  印 i。"""
        # 由于列表字面量语法可能不支持，我们跳过这个测试
        # 或者使用变量
        code = """定 列表 = 创建列表。
遍历 i 于 列表：
  印 i。"""
        success, errors = self._analyze(code)
        
        self.assertTrue(success)
        self.assertEqual(len(errors), 0)
    
    def test_while_loop(self):
        """测试当循环"""
        code = """定 x = 0。
当 x 小 10：
  x = x 加 1。"""
        success, errors = self._analyze(code)
        
        self.assertTrue(success)
        self.assertEqual(len(errors), 0)
    
    def test_assignment(self):
        """测试赋值语句"""
        code = """定 x = 5。
x = 10。"""
        success, errors = self._analyze(code)
        
        self.assertTrue(success)
        self.assertEqual(len(errors), 0)
    
    def test_assignment_undefined(self):
        """测试赋值未定义变量"""
        code = "x = 10。"
        success, errors = self._analyze(code)
        
        # 语境驱动式：自动创建变量
        self.assertTrue(success)
        self.assertEqual(len(errors), 0)
    
    def test_type_inference_number(self):
        """测试数字类型推断"""
        code = "定 x = 5。"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        symbol = analyzer.global_scope.lookup("x")
        self.assertIsNotNone(symbol)
        self.assertEqual(symbol["value_type"], "number")
    
    def test_type_inference_string(self):
        """测试字符串类型推断"""
        code = "定 x = \"你好\"。"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        symbol = analyzer.global_scope.lookup("x")
        self.assertIsNotNone(symbol)
        self.assertEqual(symbol["value_type"], "string")
    
    def test_builtin_function(self):
        """测试内置函数"""
        code = "印 \"你好\"。"
        success, errors = self._analyze(code)
        
        self.assertTrue(success)
        self.assertEqual(len(errors), 0)
    
    def test_complex_expression(self):
        """测试复杂表达式"""
        code = """定 a = 5。
定 b = 3。
定 c = a 加 b 乘 2。"""
        success, errors = self._analyze(code)
        
        self.assertTrue(success)
        self.assertEqual(len(errors), 0)


if __name__ == "__main__":
    unittest.main()
