# src/lexer/tokens.py
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class TokenType(Enum):
    # 字面量
    NUMBER = auto()  # 数字
    STRING = auto()  # 字符串
    IDENTIFIER = auto()  # 标识符

    # 核心关键字（双字）
    VAR = auto()  # 定义
    FUNCTION = auto()  # 函数
    IF = auto()  # 如果
    TRUE = auto()  # 真值
    FALSE = auto()  # 假值

    # 语法标记（双字）
    THEN = auto()  # 那么
    ELSE = auto()  # 否则
    ELIF = auto()  # 可选
    FOR = auto()  # 循环
    WHILE = auto()  # 当满足
    REPEAT = auto()  # 重复
    CONTINUE = auto()  # 继续
    BREAK = auto()  # 跳出
    END = auto()  # 结束
    RETURN = auto()  # 返回
    PARAM = auto()  # 参数
    IN = auto()  # 遍历
    TIMES = auto()  # 次数

    # 高阶函数
    MAP = auto()  # 皆（映射）
    FILTER = auto()  # 只（筛选）
    REDUCE = auto()  # 归（归约）

    # 异常处理
    TRY = auto()  # 尝试
    CATCH = auto()  # 捕获
    FINALLY = auto()  # 最终
    RAISE = auto()  # 抛出
    AS = auto()  # 为 (用于异常变量绑定)

    # 模块导入
    IMPORT = auto()  # 导入
    FROM = auto()  # 从

    # 操作符（双字）
    PLUS = auto()  # 相加
    MINUS = auto()  # 相减
    MULTIPLY = auto()  # 相乘
    DIVIDE = auto()  # 相除
    MODULO = auto()  # 取余
    ASSIGN = auto()  # =
    EQUALS = auto()  # 等于
    NOT_EQUALS = auto()  # 不等
    LESS = auto()  # 小于
    GREATER = auto()  # 大于
    LESS_EQ = auto()  # 小等
    GREATER_EQ = auto()  # 大等
    AND = auto()  # 并且
    OR = auto()  # 或者
    NOT = auto()  # 非也

    # 分隔符
    COMMA = auto()  # ，
    PIPE = auto()  # ，（管道操作符）
    PERIOD = auto()  # 。
    COLON = auto()  # ：
    SEMICOLON = auto()  # ；
    PAUSE_MARK = auto()  # 、（顿号）
    DOT = auto()  # . （成员访问）
    LPAREN = auto()  # （
    RPAREN = auto()  # ）
    LBRACKET = auto()  # 【
    RBRACKET = auto()  # 】
    LBRACE = auto()  # {
    RBRACE = auto()  # }

    # 特殊符号
    DOLLAR = auto()  # $
    MATH_EXPR = auto()  # 数学表达式
    PYTHON_BLOCK = auto()  # Python代码块

    # 其他
    NEWLINE = auto()  # 换行
    INDENT = auto()  # 缩进
    DEDENT = auto()  # 减少缩进
    EOF = auto()  # 文件结束


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
        return (
            self.type == other.type
            and self.value == other.value
            and self.line == other.line
            and self.column == other.column
        )
