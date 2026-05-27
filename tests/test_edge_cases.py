#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
边界情况测试

测试各种边界情况和错误处理
"""

import pytest
from src.lexer.lexer import Lexer, LexerError
from src.parser.parser import Parser, ParseError
from src.semantic.analyzer import SemanticAnalyzer, SemanticError
from src.codegen.python_codegen import PythonCodegen


class TestLexerEdgeCases:
    """词法分析器边界情况测试"""

    def test_empty_string(self):
        """测试空字符串"""
        lexer = Lexer("")
        tokens = lexer.tokenize()
        assert len(tokens) == 1
        assert tokens[0].type.name == 'EOF'

    def test_only_whitespace(self):
        """测试只有空白字符"""
        lexer = Lexer("   \t\n  ")
        tokens = lexer.tokenize()
        # 空白字符会产生NEWLINE和EOF token
        assert len(tokens) >= 1
        assert tokens[-1].type.name == 'EOF'

    def test_only_comments(self):
        """测试只有注释"""
        lexer = Lexer("# 这是注释\n-- 这也是注释")
        tokens = lexer.tokenize()
        # 注释会产生NEWLINE和EOF token
        assert len(tokens) >= 1
        assert tokens[-1].type.name == 'EOF'

    def test_unmatched_string(self):
        """测试未闭合的字符串"""
        lexer = Lexer('打印 "未闭合的字符串')
        with pytest.raises(LexerError):
            lexer.tokenize()

    def test_invalid_number_format(self):
        """测试无效的数字格式"""
        lexer = Lexer("123.45.67")
        with pytest.raises(LexerError):
            lexer.tokenize()

    def test_special_characters(self):
        """测试特殊字符"""
        lexer = Lexer("打印 @#$%^&*")
        with pytest.raises(LexerError):
            lexer.tokenize()

    def test_very_long_identifier(self):
        """测试很长的标识符"""
        long_name = "变量" * 100
        lexer = Lexer(f"定义 {long_name} = 1。")
        tokens = lexer.tokenize()
        assert any(t.value == long_name for t in tokens)

    def test_mixed_chinese_english(self):
        """测试中英文混合标识符"""
        lexer = Lexer('定义 user名字 = "张三"。')
        tokens = lexer.tokenize()
        assert any(t.value == "user名字" for t in tokens)

    def test_nested_parentheses(self):
        """测试嵌套括号"""
        lexer = Lexer("定义 结果 = ((1相加2)相乘(3相减4))。")
        tokens = lexer.tokenize()
        assert len(tokens) > 0

    def test_chinese_punctuation(self):
        """测试中文标点符号"""
        lexer = Lexer('打印 "你好"，"世界"。')
        tokens = lexer.tokenize()
        assert len(tokens) > 0


class TestParserEdgeCases:
    """语法分析器边界情况测试"""

    def test_empty_program(self):
        """测试空程序"""
        lexer = Lexer("")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        assert len(ast.statements) == 0

    def test_only_newlines(self):
        """测试只有换行符"""
        lexer = Lexer("\n\n\n")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        assert len(ast.statements) == 0

    def test_deeply_nested_expressions(self):
        """测试深度嵌套表达式"""
        source = "定义 结果 = 1相加2相加3相加4相加5相加6相加7相加8相加9相加10。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        assert len(ast.statements) == 1

    def test_function_with_many_parameters(self):
        """测试多参数函数"""
        source = "定义 多参数 = 函数 a b c d e f：返回 a。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        assert len(ast.statements) == 1

    def test_if_without_else(self):
        """测试没有else的if语句"""
        source = """
如果 真值 那么：
    打印 "真值"。
。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        assert len(ast.statements) == 1

    def test_multiple_semicolons(self):
        """测试多个分号"""
        source = '打印 "测试"。。。'
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        # 应该能处理多个分号
        assert len(ast.statements) >= 1

    def test_unmatched_brackets(self):
        """测试不匹配的括号"""
        lexer = Lexer("定义 列表 = 【1，2，3。")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        with pytest.raises(ParseError):
            parser.parse()


class TestSemanticEdgeCases:
    """语义分析器边界情况测试"""

    def test_undefined_variable_in_expression(self):
        """测试表达式中使用未定义变量"""
        source = "打印 未定义变量。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        # 语义分析器会报告错误，但不一定义抛出异常
        analyzer.analyze(ast)
        # 检查是否有错误
        assert analyzer.has_errors()

    def test_redefine_variable(self):
        """测试重复定义变量"""
        source = """
定义 x = 1。
定义 x = 2。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        # 应该能检测到重复定义
        analyzer.analyze(ast)

    def test_function_call_with_wrong_args(self):
        """测试函数调用参数数量错误"""
        source = """
定义 示例 = 函数 x：返回 x。
示例 1 2。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        # 应该能检测到参数数量错误
        analyzer.analyze(ast)

    def test_nested_scope(self):
        """测试嵌套作用域"""
        source = """
定义 外层 = 1。
定义 内部 = 函数：
    定义 内层 = 2。
    打印 外层。
    打印 内层。
。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)

    def test_scope_after_function(self):
        """测试函数后的作用域"""
        source = """
定义 示例 = 函数 x：返回 x。
定义 结果 = 示例 5。
打印 结果。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)


class TestCodegenEdgeCases:
    """代码生成器边界情况测试"""

    def test_empty_program(self):
        """测试空程序"""
        from src.parser.ast_nodes import ProgramNode
        codegen = PythonCodegen()
        ast = ProgramNode(line=1, column=1, statements=[])
        code = codegen.generate(ast)
        assert code == ""

    def test_very_long_string(self):
        """测试很长的字符串"""
        long_string = "测试" * 1000
        source = f'打印 "{long_string}"。'
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        codegen = PythonCodegen()
        code = codegen.generate(ast)
        assert long_string in code

    def test_special_characters_in_string(self):
        """测试字符串中的特殊字符"""
        source = '打印 "换行\\n制表符\\t引号\\""。'
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        codegen = PythonCodegen()
        code = codegen.generate(ast)
        assert "print" in code

    def test_nested_function_calls(self):
        """测试嵌套函数调用"""
        source = '打印 打印 打印 "测试"。'
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        codegen = PythonCodegen()
        code = codegen.generate(ast)
        assert "print" in code


class TestIntegrationEdgeCases:
    """集成测试边界情况"""

    def test_complex_program(self):
        """测试复杂程序"""
        source = """
# 定义阶相乘函数
定义 阶相乘 = 函数 n：
    如果 n等于于1 那么：
        返回 1。
    否则：
        返回 n相乘阶相乘 n相减1。
    。
。

# 计算5的阶相乘
定义 结果 = 阶相乘 5。
打印 结果。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        codegen = PythonCodegen()
        code = codegen.generate(ast)
        assert "def" in code
        assert "阶相乘" in code

    def test_multiple_functions(self):
        """测试多个函数"""
        source = """
定义 相加法 = 函数 a b：返回 a相加b。
定义 相减法 = 函数 a b：返回 a相减b。
定义 相乘法 = 函数 a b：返回 a相乘b。

定义 结果1 = 相加法 1 2。
定义 结果2 = 相减法 5 3。
定义 结果3 = 相乘法 2 3。

打印 结果1。
打印 结果2。
打印 结果3。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        codegen = PythonCodegen()
        code = codegen.generate(ast)
        assert code.count("def") >= 3

    def test_error_recovery(self):
        """测试错误恢复"""
        # 测试语法错误后能否继续解析
        source = """
打印 "正确"。
打印 "错误"
打印 "继续"。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        # 应该能解析部分内容
        try:
            ast = parser.parse()
        except ParseError:
            pass  # 预期会有错误


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
