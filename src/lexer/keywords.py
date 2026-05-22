# src/lexer/keywords.py
"""中文关键字、语法标记和操作符定义

核心设计原则：
- 只有5个核心关键字（定、函、若、真、假）
- 其他功能通过函数和宏实现
- 操作符（加、减、乘、除等）是函数，不是关键字
- 语法标记（则、否则、遍历等）不是关键字，用于构建语法结构
"""

from src.lexer.tokens import TokenType

# 核心关键字（仅5个，不可扩展）
CORE_KEYWORDS = {
    "定": TokenType.VAR,
    "函": TokenType.FUNCTION,
    "若": TokenType.IF,
    "真": TokenType.TRUE,
    "假": TokenType.FALSE,
}

# 语法标记（非关键字，用于构建语法结构）
SYNTAX_MARKERS = {
    # 条件语法标记
    "则": TokenType.THEN,
    "否则": TokenType.ELSE,
    "否则若": TokenType.ELIF,
    
    # 循环语法标记（通过宏实现）
    "遍历": TokenType.FOR,
    "当": TokenType.WHILE,
    "重复": TokenType.REPEAT,
    "持续": TokenType.CONTINUE,
    "于": TokenType.IN,
    "次": TokenType.TIMES,
    
    # 函数语法标记
    "返回": TokenType.RETURN,
    "接收": TokenType.RECEIVE,
}

# 操作符（函数，非关键字）
OPERATORS = {
    "加": TokenType.PLUS,
    "减": TokenType.MINUS,
    "乘": TokenType.MULTIPLY,
    "除": TokenType.DIVIDE,
    "等": TokenType.EQUALS,
    "不等": TokenType.NOT_EQUALS,
    "小": TokenType.LESS,
    "大": TokenType.GREATER,
    "小等": TokenType.LESS_EQ,
    "大等": TokenType.GREATER_EQ,
    "且": TokenType.AND,
    "或": TokenType.OR,
    "非": TokenType.NOT,
}

# 符号映射
SYMBOLS = {
    "，": TokenType.COMMA,
    "。": TokenType.PERIOD,
    "：": TokenType.COLON,
    "；": TokenType.SEMICOLON,
    "、": TokenType.PAUSE_MARK,  # 顿号
    "（": TokenType.LPAREN,
    "）": TokenType.RPAREN,
    "(": TokenType.LPAREN,      # 英文括号（用于数学表达式）
    ")": TokenType.RPAREN,
    "【": TokenType.LBRACKET,
    "】": TokenType.RBRACKET,
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
    "=": TokenType.ASSIGN,
    "$": TokenType.DOLLAR,
    # 数学表达式符号
    "*": TokenType.MULTIPLY,
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "/": TokenType.DIVIDE,
}

# 合并所有关键字和标记（用于词法分析）
ALL_KEYWORDS = {**CORE_KEYWORDS, **SYNTAX_MARKERS}
