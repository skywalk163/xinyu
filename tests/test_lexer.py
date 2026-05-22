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
