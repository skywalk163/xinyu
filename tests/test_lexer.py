# tests/test_lexer.py
import pytest
from src.lexer.tokens import Token, TokenType

def test_token_creation():
    token = Token(TokenType.NUMBER, "123", 1, 0)
    assert token.type == TokenType.NUMBER
    assert token.value == "123"
    assert token.line == 1
    assert token.column == 0

def test_token_string_representation():
    token = Token(TokenType.STRING, "你好", 1, 0)
    assert str(token) == "Token(STRING, '你好', line=1, col=0)"

def test_token_equality():
    token1 = Token(TokenType.NUMBER, "123", 1, 0)
    token2 = Token(TokenType.NUMBER, "123", 1, 0)
    assert token1 == token2


# ===== 任务3：中文关键字定义测试 =====
from src.lexer.keywords import CORE_KEYWORDS, SYNTAX_MARKERS, OPERATORS

def test_core_keywords():
    """核心关键字只有5个"""
    assert CORE_KEYWORDS["定"] == TokenType.VAR
    assert CORE_KEYWORDS["函"] == TokenType.FUNCTION
    assert CORE_KEYWORDS["若"] == TokenType.IF
    assert CORE_KEYWORDS["真"] == TokenType.TRUE
    assert CORE_KEYWORDS["假"] == TokenType.FALSE

def test_syntax_markers():
    """语法标记（非关键字）"""
    assert SYNTAX_MARKERS["则"] == TokenType.THEN
    assert SYNTAX_MARKERS["否则"] == TokenType.ELSE
    assert SYNTAX_MARKERS["遍历"] == TokenType.FOR
    assert SYNTAX_MARKERS["当"] == TokenType.WHILE

def test_operators():
    """操作符（函数，非关键字）"""
    assert OPERATORS["加"] == TokenType.PLUS
    assert OPERATORS["减"] == TokenType.MINUS
    assert OPERATORS["乘"] == TokenType.MULTIPLY
    assert OPERATORS["除"] == TokenType.DIVIDE
