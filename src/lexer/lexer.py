# src/lexer/lexer.py
"""词法分析器

负责将源代码字符串转换为Token序列。
支持：
- 中文标识符、关键字、操作符
- 数字（整数和浮点数）
- 字符串（双引号）
- 缩进（Python风格）
- 注释（-- 开头）
"""

import re
from typing import List
from src.lexer.tokens import Token, TokenType
from src.lexer.keywords import ALL_KEYWORDS, OPERATORS, SYMBOLS


class LexerError(Exception):
    """词法分析错误"""
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Lexer Error at line {line}, column {column}: {message}")


class Lexer:
    """词法分析器"""
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 0
        self.indent_stack = [0]
        self.tokens: List[Token] = []
    
    def tokenize(self) -> List[Token]:
        """将源代码转换为Token序列"""
        while self.pos < len(self.source):
            self._skip_whitespace()
            
            if self.pos >= len(self.source):
                break
            
            char = self.source[self.pos]
            
            # 处理换行和缩进
            if char == '\n':
                self._handle_newline()
            # 处理注释
            elif char == '-' and self.pos + 1 < len(self.source) and self.source[self.pos + 1] == '-':
                self._skip_comment()
            # 处理字符串
            elif char == '"':
                self._read_string()
            # 处理数字
            elif char.isdigit():
                self._read_number()
            # 处理符号
            elif char in SYMBOLS:
                self._read_symbol()
            # 处理中文关键字、操作符、标识符
            elif self._is_chinese(char):
                self._read_chinese()
            # 处理英文标识符
            elif char.isalpha() or char == '_':
                self._read_identifier()
            else:
                raise LexerError(f"Unexpected character: {char}", self.line, self.column)
        
        # 处理剩余的DEDENT
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token(TokenType.DEDENT, None, self.line, self.column))
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
    
    def _skip_whitespace(self):
        """跳过空白字符（不包括换行）"""
        while self.pos < len(self.source) and self.source[self.pos] in ' \t':
            self.pos += 1
            self.column += 1
    
    def _skip_comment(self):
        """跳过注释（-- 开头到行尾）"""
        while self.pos < len(self.source) and self.source[self.pos] != '\n':
            self.pos += 1
    
    def _handle_newline(self):
        """处理换行和缩进"""
        self.tokens.append(Token(TokenType.NEWLINE, '\n', self.line, self.column))
        self.line += 1
        self.column = 0
        self.pos += 1
        
        # 计算缩进
        indent = 0
        while self.pos < len(self.source) and self.source[self.pos] == ' ':
            indent += 1
            self.pos += 1
        
        # 跳过空行
        if self.pos < len(self.source) and self.source[self.pos] == '\n':
            return
        
        # 生成INDENT/DEDENT
        if indent > self.indent_stack[-1]:
            self.indent_stack.append(indent)
            self.tokens.append(Token(TokenType.INDENT, indent, self.line, 0))
        elif indent < self.indent_stack[-1]:
            while indent < self.indent_stack[-1]:
                self.indent_stack.pop()
                self.tokens.append(Token(TokenType.DEDENT, indent, self.line, 0))
    
    def _read_string(self):
        """读取字符串"""
        start_col = self.column
        self.pos += 1  # 跳过开头的 "
        start = self.pos
        
        while self.pos < len(self.source) and self.source[self.pos] != '"':
            if self.source[self.pos] == '\\':
                self.pos += 1  # 跳过转义字符
            self.pos += 1
        
        if self.pos >= len(self.source):
            raise LexerError("Unterminated string", self.line, start_col)
        
        value = self.source[start:self.pos]
        self.pos += 1  # 跳过结尾的 "
        self.column += self.pos - start + 1
        
        # 处理转义字符
        value = value.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"')
        
        self.tokens.append(Token(TokenType.STRING, value, self.line, start_col))
    
    def _read_number(self):
        """读取数字（整数或浮点数）"""
        start_col = self.column
        start = self.pos
        
        while self.pos < len(self.source) and (self.source[self.pos].isdigit() or self.source[self.pos] == '.'):
            self.pos += 1
        
        value = self.source[start:self.pos]
        self.column += len(value)
        
        if '.' in value:
            self.tokens.append(Token(TokenType.NUMBER, float(value), self.line, start_col))
        else:
            self.tokens.append(Token(TokenType.NUMBER, int(value), self.line, start_col))
    
    def _read_symbol(self):
        """读取符号"""
        char = self.source[self.pos]
        token_type = SYMBOLS.get(char)
        
        if token_type:
            self.tokens.append(Token(token_type, char, self.line, self.column))
            self.pos += 1
            self.column += 1
    
    def _is_chinese(self, char: str) -> bool:
        """判断字符是否为中文"""
        return '\u4e00' <= char <= '\u9fff'
    
    def _read_chinese(self):
        """读取中文（关键字、操作符或标识符）"""
        start_col = self.column
        start = self.pos
        
        while self.pos < len(self.source) and self._is_chinese(self.source[self.pos]):
            self.pos += 1
        
        value = self.source[start:self.pos]
        self.column += len(value)
        
        # 检查是否为关键字
        if value in ALL_KEYWORDS:
            self.tokens.append(Token(ALL_KEYWORDS[value], value, self.line, start_col))
        # 检查是否为操作符
        elif value in OPERATORS:
            self.tokens.append(Token(OPERATORS[value], value, self.line, start_col))
        # 否则为标识符
        else:
            self.tokens.append(Token(TokenType.IDENTIFIER, value, self.line, start_col))
    
    def _read_identifier(self):
        """读取英文标识符"""
        start_col = self.column
        start = self.pos
        
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            self.pos += 1
        
        value = self.source[start:self.pos]
        self.column += len(value)
        
        self.tokens.append(Token(TokenType.IDENTIFIER, value, self.line, start_col))
