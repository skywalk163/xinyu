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


# ===== 任务4：词法分析器基础测试 =====
from src.lexer.lexer import Lexer

def test_lexer_number():
    """词法分析器：数字"""
    lexer = Lexer("123")
    tokens = lexer.tokenize()
    assert len(tokens) == 2  # NUMBER + EOF
    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].value == 123

def test_lexer_string():
    """词法分析器：字符串"""
    lexer = Lexer('"你好世界"')
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "你好世界"

def test_lexer_identifier():
    """词法分析器：标识符"""
    lexer = Lexer("用户数据")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == "用户数据"

def test_lexer_keyword():
    """词法分析器：关键字"""
    lexer = Lexer("若")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.IF
