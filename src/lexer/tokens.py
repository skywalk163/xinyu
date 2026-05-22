# src/lexer/tokens.py
from enum import Enum, auto
from dataclasses import dataclass
from typing import Any

class TokenType(Enum):
    # 字面量
    NUMBER = auto()      # 数字
    STRING = auto()      # 字符串
    IDENTIFIER = auto()  # 标识符
    
    # 核心关键字（仅5个）
    VAR = auto()         # 定
    FUNCTION = auto()    # 函
    IF = auto()          # 若
    TRUE = auto()        # 真
    FALSE = auto()       # 假
    
    # 语法标记（非关键字）
    THEN = auto()        # 则
    ELSE = auto()        # 否则
    ELIF = auto()        # 否则若
    FOR = auto()         # 遍历
    WHILE = auto()       # 当
    REPEAT = auto()      # 重复
    CONTINUE = auto()    # 持续
    RETURN = auto()      # 返回
    RECEIVE = auto()     # 接收
    IN = auto()          # 于
    TIMES = auto()       # 次
    
    # 操作符（函数，非关键字）
    PLUS = auto()        # 加
    MINUS = auto()       # 减
    MULTIPLY = auto()    # 乘
    DIVIDE = auto()      # 除
    ASSIGN = auto()      # =
    EQUALS = auto()      # 等
    NOT_EQUALS = auto()  # 不等
    LESS = auto()        # 小
    GREATER = auto()     # 大
    LESS_EQ = auto()     # 小等
    GREATER_EQ = auto()  # 大等
    AND = auto()         # 且
    OR = auto()          # 或
    NOT = auto()         # 非
    
    # 分隔符
    COMMA = auto()       # ，
    PERIOD = auto()      # 。
    COLON = auto()       # ：
    SEMICOLON = auto()   # ；
    PAUSE_MARK = auto()  # 、（顿号）
    LPAREN = auto()      # （
    RPAREN = auto()      # ）
    LBRACKET = auto()    # 【
    RBRACKET = auto()    # 】
    LBRACE = auto()      # {
    RBRACE = auto()      # }
    
    # 特殊符号
    DOLLAR = auto()      # $
    MATH_EXPR = auto()   # 数学表达式
    PYTHON_BLOCK = auto() # Python代码块
    
    # 其他
    NEWLINE = auto()     # 换行
    INDENT = auto()      # 缩进
    DEDENT = auto()      # 减少缩进
    EOF = auto()         # 文件结束

@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int
    
    def __str__(self):
        return f"Token({self.type.name}, {repr(self.value)}, line={self.line}, col={self.column})"
    
    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return (self.type == other.type and 
                self.value == other.value and 
                self.line == other.line and 
                self.column == other.column)
