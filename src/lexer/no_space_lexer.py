"""无空格词法分析器

实现完全无空格的中文编程语法。
使用字典驱动的最长匹配算法。
"""

from typing import List, Optional
from src.lexer.tokens import Token, TokenType


class NoSpaceLexer:
    """无空格词法分析器
    
    使用字典驱动的最长匹配算法，实现完全无空格的中文编程语法。
    """
    
    # 关键字字典（按长度降序排列）
    KEYWORDS = {
        # 4字关键字
        "大于等于": (TokenType.GREATER_EQ, ">="),
        "小于等于": (TokenType.LESS_EQ, "<="),
        
        # 3字关键字
        "定义": (TokenType.VAR, "var"),
        "函数": (TokenType.FUNCTION, "function"),
        "如果": (TokenType.IF, "if"),
        "那么": (TokenType.THEN, "then"),
        "否则": (TokenType.ELSE, "else"),
        "当满足": (TokenType.WHILE, "while"),
        "重复": (TokenType.REPEAT, "repeat"),
        "次数": (TokenType.TIMES, "times"),
        "遍历": (TokenType.IN, "in"),
        "返回": (TokenType.RETURN, "return"),
        "循环": (TokenType.FOR, "for"),
        "可选": (TokenType.ELIF, "elif"),
        "继续": (TokenType.CONTINUE, "continue"),
        "跳出": (TokenType.BREAK, "break"),
        "结束": (TokenType.END, "end"),
        "平方根": (TokenType.IDENTIFIER, "sqrt"),
        "绝对值": (TokenType.IDENTIFIER, "abs"),
        "最大值": (TokenType.IDENTIFIER, "max"),
        "最小值": (TokenType.IDENTIFIER, "min"),
        "求和": (TokenType.IDENTIFIER, "sum"),
        "转整数": (TokenType.IDENTIFIER, "int"),
        "转浮点": (TokenType.IDENTIFIER, "float"),
        "转字符串": (TokenType.IDENTIFIER, "str"),
        
        # 2字关键字
        "相加": (TokenType.PLUS, "+"),
        "相减": (TokenType.MINUS, "-"),
        "相乘": (TokenType.MULTIPLY, "*"),
        "相除": (TokenType.DIVIDE, "/"),
        "取余": (TokenType.MODULO, "%"),
        "等于": (TokenType.EQUALS, "=="),
        "不等": (TokenType.NOT_EQUALS, "!="),
        "大于": (TokenType.GREATER, ">"),
        "小于": (TokenType.LESS, "<"),
        "并且": (TokenType.AND, "and"),
        "或者": (TokenType.OR, "or"),
        "打印": (TokenType.IDENTIFIER, "print"),
        "输入": (TokenType.IDENTIFIER, "input"),
        "长度": (TokenType.IDENTIFIER, "len"),
        "列表": (TokenType.IDENTIFIER, "list"),
        "范围": (TokenType.IDENTIFIER, "range"),
        "追加": (TokenType.IDENTIFIER, "append"),
        "弹出": (TokenType.IDENTIFIER, "pop"),
        "真值": (TokenType.TRUE, "true"),
        "假值": (TokenType.FALSE, "false"),
        "非也": (TokenType.NOT, "not"),
    }
    
    # 兼容旧语法
    COMPAT_KEYWORDS = {
        # 单字关键字（兼容旧语法）
        "定": (TokenType.VAR, "var"),
        "函": (TokenType.FUNCTION, "function"),
        "若": (TokenType.IF, "if"),
        "则": (TokenType.THEN, "then"),
        "否": (TokenType.ELSE, "else"),
        "真": (TokenType.TRUE, "true"),
        "假": (TokenType.FALSE, "false"),
    }
    
    def __init__(self, source: str):
        """初始化词法分析器
        
        Args:
            source: 源代码字符串
        """
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def tokenize(self) -> List[Token]:
        """词法分析
        
        Returns:
            Token列表
        """
        self.tokens = []
        
        while self.pos < len(self.source):
            token = self._next_token()
            if token:
                self.tokens.append(token)
        
        # 添加EOF token
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens
    
    def _next_token(self) -> Optional[Token]:
        """获取下一个token
        
        Returns:
            Token或None
        """
        self._skip_whitespace()
        
        if self.pos >= len(self.source):
            return None
        
        # 尝试匹配最长关键字（从4到1）
        for length in range(4, 0, -1):
            if self.pos + length <= len(self.source):
                substring = self.source[self.pos:self.pos + length]
                
                # 先检查主关键字字典
                if substring in self.KEYWORDS:
                    token_type, value = self.KEYWORDS[substring]
                    token = Token(token_type, value, self.line, self.column)
                    self._advance(length)
                    return token
                
                # 再检查兼容关键字字典
                if substring in self.COMPAT_KEYWORDS:
                    token_type, value = self.COMPAT_KEYWORDS[substring]
                    token = Token(token_type, value, self.line, self.column)
                    self._advance(length)
                    return token
        
        # 匹配数字
        if self.source[self.pos].isdigit():
            return self._read_number()
        
        # 匹配字符串
        if self.source[self.pos] == '"':
            return self._read_string()
        
        # 匹配标识符
        if self._is_identifier_start():
            return self._read_identifier()
        
        # 匹配符号
        return self._read_symbol()
    
    def _skip_whitespace(self):
        """跳过空白字符"""
        while self.pos < len(self.source) and self.source[self.pos].isspace():
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def _advance(self, count: int = 1):
        """前进count个字符
        
        Args:
            count: 前进的字符数
        """
        for _ in range(count):
            if self.pos < len(self.source):
                if self.source[self.pos] == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.pos += 1
    
    def _is_identifier_start(self) -> bool:
        """判断是否是标识符开始
        
        Returns:
            是否是标识符开始字符
        """
        char = self.source[self.pos]
        return (char.isalpha() or 
                '\u4e00' <= char <= '\u9fff' or 
                char == '_')
    
    def _is_identifier_char(self) -> bool:
        """判断是否是标识符字符
        
        Returns:
            是否是标识符字符
        """
        if self.pos >= len(self.source):
            return False
        
        char = self.source[self.pos]
        
        # 如果是数字、字母、中文或下划线，可能是标识符
        if char.isalnum() or '\u4e00' <= char <= '\u9fff' or char == '_':
            # 但需要检查是否是关键字的一部分
            # 检查从当前位置开始是否能匹配关键字
            for length in range(4, 0, -1):
                if self.pos + length <= len(self.source):
                    substring = self.source[self.pos:self.pos + length]
                    if substring in self.KEYWORDS or substring in self.COMPAT_KEYWORDS:
                        return False
            return True
        
        return False
    
    def _read_number(self) -> Token:
        """读取数字
        
        Returns:
            数字Token
        """
        start = self.pos
        start_col = self.column
        
        # 读取整数部分
        while self.pos < len(self.source) and self.source[self.pos].isdigit():
            self._advance()
        
        # 读取小数部分
        if self.pos < len(self.source) and self.source[self.pos] == '.':
            self._advance()
            while self.pos < len(self.source) and self.source[self.pos].isdigit():
                self._advance()
        
        value = self.source[start:self.pos]
        return Token(TokenType.NUMBER, value, self.line, start_col)
    
    def _read_string(self) -> Token:
        """读取字符串
        
        Returns:
            字符串Token
        """
        start_col = self.column
        self._advance()  # 跳过开始引号
        
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos] != '"':
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
        
        value = self.source[start:self.pos]
        self._advance()  # 跳过结束引号
        
        return Token(TokenType.STRING, value, self.line, start_col)
    
    def _read_identifier(self) -> Token:
        """读取标识符
        
        Returns:
            标识符Token
        """
        start = self.pos
        start_col = self.column
        
        while self.pos < len(self.source) and self._is_identifier_char():
            self._advance()
        
        value = self.source[start:self.pos]
        return Token(TokenType.IDENTIFIER, value, self.line, start_col)
    
    def _read_symbol(self) -> Token:
        """读取符号
        
        Returns:
            符号Token
        """
        char = self.source[self.pos]
        start_col = self.column
        
        symbol_map = {
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            '。': TokenType.PERIOD,
            '，': TokenType.COMMA,
            '：': TokenType.COLON,
            '=': TokenType.ASSIGN,
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '%': TokenType.MODULO,
            '<': TokenType.LESS,
            '>': TokenType.GREATER,
            '!': TokenType.NOT,
            ':': TokenType.COLON,
            ',': TokenType.COMMA,
            '.': TokenType.PERIOD,
        }
        
        token_type = symbol_map.get(char)
        if token_type is None:
            # 未知符号，跳过
            self._advance()
            return None
        
        token = Token(token_type, char, self.line, start_col)
        self._advance()
        
        return token


def detect_no_space_mode(source: str) -> bool:
    """检测是否应该使用无空格模式
    
    Args:
        source: 源代码字符串
        
    Returns:
        是否使用无空格模式
    """
    # 检测无空格模式特征
    no_space_patterns = [
        "定义x", "定义y", "定义z", "定义a", "定义b", "定义c",
        "如果x", "如果y", "如果z",
        "打印x", "打印y", "打印z",
        "返回x", "返回y", "返回z",
    ]
    
    for pattern in no_space_patterns:
        if pattern in source:
            return True
    
    return False
