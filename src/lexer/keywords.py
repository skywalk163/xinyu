# src/lexer/keywords.py
"""中文关键字、语法标记和操作符定义

核心设计原则：
- 双字关键字，单义无歧义
- 贴合中文严谨句式
- 语义明确，易于理解
"""

from src.lexer.tokens import TokenType

# 核心关键字（双字，单义）
CORE_KEYWORDS = {
    "定义": TokenType.VAR,        # 变量定义
    "函数": TokenType.FUNCTION,   # 函数定义
    "如果": TokenType.IF,         # 条件判断
    "真值": TokenType.TRUE,       # 布尔真值
    "假值": TokenType.FALSE,      # 布尔假值
}

# 语法标记（双字，用于构建语法结构）
SYNTAX_MARKERS = {
    # 条件语法标记
    "那么": TokenType.THEN,       # then
    "否则": TokenType.ELSE,       # else
    "可选": TokenType.ELIF,       # elif

    # 循环语法标记
    "循环": TokenType.FOR,        # for
    "当满足": TokenType.WHILE,    # while
    "重复": TokenType.REPEAT,     # repeat
    "继续": TokenType.CONTINUE,   # continue
    "跳出": TokenType.BREAK,      # break
    "结束": TokenType.END,        # end
    "遍历": TokenType.IN,         # in (用于遍历)
    "次数": TokenType.TIMES,      # times

    # 函数语法标记
    "返回": TokenType.RETURN,     # return
    "参数": TokenType.PARAM,      # parameter
}

# 操作符（双字，单义，明确指向运算）
OPERATORS = {
    # 算术运算
    "相加": TokenType.PLUS,       # 加法
    "相减": TokenType.MINUS,      # 减法
    "相乘": TokenType.MULTIPLY,   # 乘法
    "相除": TokenType.DIVIDE,     # 除法
    "取余": TokenType.MODULO,     # 取余

    # 关系运算
    "等于": TokenType.EQUALS,     # 等于
    "不等": TokenType.NOT_EQUALS, # 不等于
    "大于": TokenType.GREATER,    # 大于
    "小于": TokenType.LESS,       # 小于
    "大等": TokenType.GREATER_EQ, # 大于等于
    "小等": TokenType.LESS_EQ,    # 小于等于

    # 逻辑运算
    "并且": TokenType.AND,        # 逻辑与
    "或者": TokenType.OR,         # 逻辑或
    "非也": TokenType.NOT,        # 逻辑非
}

# 符号映射
SYMBOLS = {
    "，": TokenType.COMMA,
    ",": TokenType.COMMA,      # 英文逗号
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
    "[": TokenType.LBRACKET,    # 英文方括号（用于列表）
    "]": TokenType.RBRACKET,
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
    "=": TokenType.ASSIGN,
    "$": TokenType.DOLLAR,
    ".": TokenType.DOT,         # 成员访问符
    # 数学表达式符号
    "*": TokenType.MULTIPLY,
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "/": TokenType.DIVIDE,
    "%": TokenType.MODULO,
}

# 内置函数（双字，单义）
BUILTIN_FUNCTIONS = {
    "打印": TokenType.IDENTIFIER,  # print
    "输入": TokenType.IDENTIFIER,  # input
    "输出": TokenType.IDENTIFIER,  # output
    "写入": TokenType.IDENTIFIER,  # write
    "读取": TokenType.IDENTIFIER,  # read
}

# 合并所有关键字和标记（用于词法分析）
ALL_KEYWORDS = {**CORE_KEYWORDS, **SYNTAX_MARKERS}
