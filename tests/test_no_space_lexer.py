"""无空格词法分析器测试

测试完全无空格的中文编程语法。
"""

import pytest

from src.lexer.no_space_lexer import NoSpaceLexer, detect_no_space_mode
from src.lexer.tokens import TokenType


class TestNoSpaceLexer:
    """无空格词法分析器测试"""

    def test_variable_definition(self):
        """测试无空格变量定义"""
        source = "定义x=5。"
        lexer = NoSpaceLexer(source)
    _ = kenize()  # 未使用变量

        # 验证token数量（包括EOF）
        assert len(tokens) == 6

        # 验证token类型
        assert tokens[0].type == TokenType.VAR
        assert tokens[1].type == TokenType.IDENTIFIER
        assert tokens[1].value == "x"
        assert tokens[2].type == TokenType.ASSIGN
        assert tokens[3].type == TokenType.NUMBER
        assert tokens[3].value == "5"
        assert tokens[4].type == TokenType.PERIOD

    def test_variable_with_chinese_name(self):
        """测试中文变量名"""
        source = "定义价格=100。"
        lexer = NoSpaceLexer(source)
    _ = kenize()  # 未使用变量

        assert tokens[0].type == TokenType.VAR
        assert tokens[1].type == TokenType.IDENTIFIER
        assert tokens[1].value == "价格"
        assert tokens[3].value == "100"

    def test_print_statement(self):
        """测试打印语句"""
        source = "打印x。"
        lexer = NoSpaceLexer(source)
    _ = kenize()  # 未使用变量

        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "print"
        assert tokens[1].type == TokenType.IDENTIFIER
        assert tokens[1].value == "x"

    def test_print_string(self):
        """测试打印字符串"""
        source = '打印"你好"。'
        lexer = NoSpaceLexer(source)
    _ = kenize()  # 未使用变量

        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "print"
        assert tokens[1].type == TokenType.STRING
        assert tokens[1].value == "你好"

    def test_arithmetic_operators(self):
        """测试算术操作符"""
        source = "定义结果=3相加5。"
        lexer = NoSpaceLexer(source)
    _ = kenize()  # 未使用变量

        assert tokens[0].type == TokenType.VAR
        assert tokens[1].value == "结果"
        assert tokens[3].value == "3"
        assert tokens[4].type == TokenType.PLUS
        assert tokens[5].value == "5"

    def test_comparison_operators(self):
        """测试比较操作符"""
        source = '如果x大于5那么：打印"大"。'
        lexer = NoSpaceLexer(source)
    _ = kenize()  # 未使用变量

        assert tokens[0].type == TokenType.IF
        assert tokens[1].value == "x"
        assert tokens[2].type == TokenType.GREATER
        assert tokens[3].value == "5"
        assert tokens[4].type == TokenType.THEN
        assert tokens[5].type == TokenType.COLON

    def test_function_definition(self):
        """测试函数定义"""
        source = "定义平方=函x：返回x相乘x。。"
        lexer = NoSpaceLexer(source)
    _ = kenize()  # 未使用变量

        assert tokens[0].type == TokenType.VAR
        assert tokens[1].value == "平方"
        assert tokens[3].type == TokenType.FUNCTION
        assert tokens[4].value == "x"
        assert tokens[5].type == TokenType.COLON
        assert tokens[6].type == TokenType.RETURN

    def test_if_else_statement(self):
        """测试if-else语句"""
        source = '如果x大于5那么：打印"大"。否则：打印"小"。。'
        lexer = NoSpaceLexer(source)
    _ = kenize()  # 未使用变量

        assert tokens[0].type == TokenType.IF
        assert tokens[4].type == TokenType.THEN
        assert tokens[9].type == TokenType.ELSE

    def test_while_loop(self):
        """测试while循环"""
        source = "当满足x小于10：打印x。。"
        lexer = NoSpaceLexer(source)
    _ = kenize()  # 未使用变量

        assert tokens[0].type == TokenType.WHILE
        assert tokens[1].value == "x"
        assert tokens[2].type == TokenType.LESS

    def test_for_loop(self):
        """测试for循环"""
        source = "循环x遍历列表1 2 3：打印x。。"
        lexer = NoSpaceLexer(source)
    _ = kenize()  # 未使用变量

        assert tokens[0].type == TokenType.FOR
        assert tokens[1].value == "x"
        assert tokens[2].type == TokenType.IN

    def test_builtin_functions(self):
        """测试内置函数"""
        source = "定义结果=平方根16。"
        lexer = NoSpaceLexer(source)
    _ = kenize()  # 未使用变量

        assert tokens[3].type == TokenType.IDENTIFIER
        assert tokens[3].value == "sqrt"
        assert tokens[4].value == "16"

    def test_multiple_variables(self):
        """测试多个变量定义"""
        source = "定义x=5。定义y=10。定义z=x相加y。"
        lexer = NoSpaceLexer(source)
    _ = kenize()  # 未使用变量

        # 验证第一个变量
        assert tokens[0].type == TokenType.VAR
        assert tokens[1].value == "x"

        # 验证第二个变量（位置5：定义x=5。共5个token，第6个是第二个定义）
        assert tokens[5].type == TokenType.VAR
        assert tokens[6].value == "y"

        # 验证第三个变量（位置10：前两个定义各5个token）
        assert tokens[10].type == TokenType.VAR
        assert tokens[11].value == "z"

    def test_complex_expression(self):
        """测试复杂表达式"""
        source = "定义结果=(3相加5)相乘2。"
        lexer = NoSpaceLexer(source)
    _ = kenize()  # 未使用变量

        assert tokens[3].type == TokenType.LPAREN
        assert tokens[4].value == "3"
        assert tokens[5].type == TokenType.PLUS
        assert tokens[6].value == "5"
        assert tokens[7].type == TokenType.RPAREN
        assert tokens[8].type == TokenType.MULTIPLY

    def test_boolean_values(self):
        """测试布尔值"""
        source = "定义flag=真值。"
        lexer = NoSpaceLexer(source)
    _ = kenize()  # 未使用变量

        assert tokens[3].type == TokenType.TRUE

    def test_logical_operators(self):
        """测试逻辑操作符"""
        source = "定义结果=真值并且假值。"
        lexer = NoSpaceLexer(source)
    _ = kenize()  # 未使用变量

        assert tokens[3].type == TokenType.TRUE
        assert tokens[4].type == TokenType.AND
        assert tokens[5].type == TokenType.FALSE

    def test_compatibility_mode(self):
        """测试兼容模式（旧语法）"""
        source = "定x=5。"
        lexer = NoSpaceLexer(source)
    _ = kenize()  # 未使用变量

        assert tokens[0].type == TokenType.VAR
        assert tokens[1].value == "x"


class TestDetectNoSpaceMode:
    """检测无空格模式测试"""

    def test_detect_no_space(self):
        """测试检测无空格模式"""
        source = "定义x=5。"
        assert detect_no_space_mode(source) is True

    def test_detect_standard_mode(self):
        """测试检测标准模式"""
        source = "定义 x = 5。"
        assert detect_no_space_mode(source) is False

    def test_detect_with_print(self):
        """测试检测打印语句"""
        source = "打印x。"
        assert detect_no_space_mode(source) is True

    def test_detect_with_if(self):
        """测试检测if语句"""
        source = '如果x大于5那么：打印"大"。'
        assert detect_no_space_mode(source) is True


class TestNoSpaceEdgeCases:
    """无空格边界情况测试"""

    def test_empty_source(self):
        """测试空源代码"""
        source = ""
        lexer = NoSpaceLexer(source)
    _ = kenize()  # 未使用变量

        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF

    def test_only_whitespace(self):
        """测试只有空白字符"""
        source = "   \n\t  "
        lexer = NoSpaceLexer(source)
    _ = kenize()  # 未使用变量

        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF

    def test_chinese_numbers(self):
        """测试中文数字"""
        source = "定义x=123。"
        lexer = NoSpaceLexer(source)
    _ = kenize()  # 未使用变量

        assert tokens[3].type == TokenType.NUMBER
        assert tokens[3].value == "123"

    def test_float_numbers(self):
        """测试浮点数"""
        source = "定义x=3.14。"
        lexer = NoSpaceLexer(source)
    _ = kenize()  # 未使用变量

        assert tokens[3].type == TokenType.NUMBER
        assert tokens[3].value == "3.14"

    def test_multiline_code(self):
        """测试多行代码"""
        source = """定义x=5。
定义y=10。
打印x。"""
        lexer = NoSpaceLexer(source)
    _ = kenize()  # 未使用变量

        # 验证token数量
        assert len(tokens) > 1

        # 验证行号
        assert tokens[0].line == 1
        # 找到第二个定义的token
        var_tokens = [t for t in tokens if t.type == TokenType.VAR]
        assert len(var_tokens) == 2

    def test_string_with_spaces(self):
        """测试包含空格的字符串"""
        source = '打印"你好 世界"。'
        lexer = NoSpaceLexer(source)
    _ = kenize()  # 未使用变量

        assert tokens[1].type == TokenType.STRING
        assert tokens[1].value == "你好 世界"

    def test_nested_parentheses(self):
        """测试嵌套括号"""
        source = "定义结果=((3相加5)相乘2)。"
        lexer = NoSpaceLexer(source)
    _ = kenize()  # 未使用变量

        # 验证括号匹配
        lparens = [t for t in tokens if t.type == TokenType.LPAREN]
        rparens = [t for t in tokens if t.type == TokenType.RPAREN]
        assert len(lparens) == len(rparens)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
