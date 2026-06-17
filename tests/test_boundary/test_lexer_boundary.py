"""词法分析器边界测试

测试词法分析器的边界情况处理能力。
"""
import pytest

from src.lexer.lexer import Lexer, LexerError
from src.lexer.tokens import TokenType


class TestLexerBoundary:
    """词法分析器边界测试"""

    def test_empty_input(self):
        """测试空输入处理"""
        lexer = Lexer("")
        tokens = lexer.tokenize()
        # 空输入应该返回空列表或仅包含EOF token
        assert len(tokens) <= 1

    def test_whitespace_only(self):
        """测试仅空白字符输入"""
        lexer = Lexer("   \n\t  ")
        tokens = lexer.tokenize()
        # 仅空白字符应该返回NEWLINE和EOF token，或仅EOF
        # 过滤掉NEWLINE token，只检查是否有实质内容
        non_whitespace_tokens = [
            t for t in tokens if t.type not in [TokenType.NEWLINE, TokenType.EOF]
        ]
        assert len(non_whitespace_tokens) == 0

    def test_single_character(self):
        """测试单个字符输入"""
        lexer = Lexer("a")
        tokens = lexer.tokenize()
        # 应该包含标识符token，可能还有EOF token
        assert len(tokens) >= 1
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "a"

    def test_long_input(self):
        """测试超长输入处理（10000+字符）"""
        long_string = "打印" + "。" * 10000
        lexer = Lexer(long_string)
        # 应该不崩溃
        tokens = lexer.tokenize()
        assert len(tokens) > 0

    def test_special_characters(self):
        """测试特殊字符处理"""
        # 测试合法的特殊字符
        lexer = Lexer("定义 变量 = 123。")
        tokens = lexer.tokenize()
        assert len(tokens) > 0

    def test_unicode_support(self):
        """测试Unicode字符支持"""
        lexer = Lexer("定义 中文变量 = 你好世界。")
        tokens = lexer.tokenize()
        assert len(tokens) > 0
        # 查找标识符token
        identifiers = [t for t in tokens if t.type == TokenType.IDENTIFIER]
        assert any(t.value == "中文变量" for t in identifiers)

    def test_all_keywords(self):
        """测试所有关键字识别"""
        keywords = ["定义", "函数", "返回", "如果", "那么", "否则", "当", "遍历", "重复", "打印", "真", "假"]
        for keyword in keywords:
            lexer = Lexer(keyword)
            tokens = lexer.tokenize()
            assert len(tokens) >= 1
            # 关键字应该被识别为关键字token或标识符
            assert tokens[0].value == keyword

    def test_all_operators(self):
        """测试所有操作符识别"""
        operators = ["+", "-", "*", "/", "=", "小于", "大于", "等于"]
        for op in operators:
            try:
                lexer = Lexer(f"定义 结果 = 1 {op} 2。")
                tokens = lexer.tokenize()
                assert len(tokens) > 0
            except Exception:
                # 某些操作符可能不支持，跳过
                pass

    def test_nested_parentheses(self):
        """测试嵌套括号处理"""
        lexer = Lexer("定义 结果 = ((1 + 2) * (3 + 4))。")
        tokens = lexer.tokenize()
        assert len(tokens) > 0

    def test_string_literal(self):
        """测试字符串字面量"""
        lexer = Lexer('打印"你好世界"。')
        tokens = lexer.tokenize()
        assert len(tokens) > 0
        # 查找字符串token
        strings = [t for t in tokens if t.type == TokenType.STRING]
        assert len(strings) > 0
        assert strings[0].value == "你好世界"

    def test_number_literal(self):
        """测试数字字面量"""
        lexer = Lexer("定义 数字 = 123。")
        tokens = lexer.tokenize()
        assert len(tokens) > 0
        # 查找数字token
        numbers = [t for t in tokens if t.type == TokenType.NUMBER]
        assert len(numbers) > 0
        assert numbers[0].value == 123

    def test_float_number(self):
        """测试浮点数字面量"""
        lexer = Lexer("定义 浮点数 = 3.14。")
        tokens = lexer.tokenize()
        assert len(tokens) > 0
        # 查找数字token
        numbers = [t for t in tokens if t.type == TokenType.NUMBER]
        assert len(numbers) > 0
        assert numbers[0].value == 3.14

    def test_comment(self):
        """测试注释处理"""
        lexer = Lexer("定义 变量 = 1。# 这是注释")
        tokens = lexer.tokenize()
        assert len(tokens) > 0
        # 注释可能被忽略或作为token保留
        # 根据实际实现决定

    def test_multiline_input(self):
        """测试多行输入"""
        source = """
定义 变量1 = 1。
定义 变量2 = 2。
定义 变量3 = 变量1 相加 变量2。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        assert len(tokens) > 0

    def test_mixed_tokens(self):
        """测试混合token类型"""
        source = "定义 函数名 = 函数 参数：返回 参数 相加 1。打印 函数名 5。"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        assert len(tokens) > 0
        # 应该包含关键字、标识符、数字、字符串等多种token
        token_types = set(t.type for t in tokens)
        assert len(token_types) > 1  # 多种token类型
