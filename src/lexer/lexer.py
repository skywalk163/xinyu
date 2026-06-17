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

from typing import List

from src.lexer.keywords import ALL_KEYWORDS, BUILTIN_FUNCTIONS, OPERATORS, SYMBOLS
from src.lexer.tokens import Token, TokenType


class LexerError(Exception):
    """词法分析错误"""

    def __init__(self, message: str, line: int, column: int, suggestion: str = None):
        self.message = message
        self.line = line
        self.column = column
        self.suggestion = suggestion

        # 构建详细的错误信息
        error_msg = f"词法错误: {message} (行 {line}, 列 {column})"
        if suggestion:
            error_msg += f"\n  💡 建议: {suggestion}"

        super().__init__(error_msg)


class Lexer:
    """词法分析器

    负责将源代码字符串转换为Token序列。支持中文编程语言的各种语法元素。

    Attributes:
        source: 源代码字符串
        pos: 当前位置索引
        line: 当前行号
        column: 当前列号
        indent_stack: 缩进栈（用于Python风格的缩进处理）
        tokens: 已识别的Token列表

    Example:
        >>> lexer = Lexer("定 x 为 42")
        >>> tokens = lexer.tokenize()
        >>> tokens[0].type
        <TokenType.VAR: ...>
    """

    def __init__(self, source: str):
        """初始化词法分析器

        Args:
            source: 要分析的源代码字符串
        """
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 0
        self.indent_stack = [0]
        self.tokens: List[Token] = []

    def tokenize(self) -> List[Token]:
        """将源代码转换为Token序列

        对源代码进行词法分析，识别并提取所有的词法单元（Token）。
        支持中文关键字、操作符、标识符，以及数字、字符串、注释等。

        Returns:
            List[Token]: Token序列列表，以EOF标记结束

        Raises:
            LexerError: 当遇到非法字符或未终止的字符串时

        Example:
            >>> lexer = Lexer("变量 x 为 42")
            >>> tokens = lexer.tokenize()
            >>> len(tokens) > 0
            True
        """
        while self.pos < len(self.source):
            self._skip_whitespace()

            if self.pos >= len(self.source):
                break

            char = self.source[self.pos]

            # 处理换行和缩进
            if char == "\n":
                self._handle_newline()
            # 处理注释（支持 -- 和 # 两种格式）
            elif (
                char == "-" and self.pos + 1 < len(self.source) and self.source[self.pos + 1] == "-"
            ):
                self._skip_comment()
            elif char == "#":
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
            elif char.isalpha() or char == "_":
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
        """跳过空白字符（不包括换行）

        跳过空格和制表符，更新列号。
        """
        while self.pos < len(self.source) and self.source[self.pos] in " \t":
            self.pos += 1
            self.column += 1

    def _skip_comment(self):
        """跳过注释

        跳过从当前位置到行尾的所有字符（注释内容）。
        支持 -- 和 # 两种注释格式。
        """
        while self.pos < len(self.source) and self.source[self.pos] != "\n":
            self.pos += 1

    def _handle_newline(self):
        """处理换行和缩进

        处理换行符，计算新行的缩进级别，生成相应的INDENT/DEDENT Token。
        采用Python风格的缩进处理机制。
        """
        self.tokens.append(Token(TokenType.NEWLINE, "\n", self.line, self.column))
        self.line += 1
        self.column = 0
        self.pos += 1

        # 计算缩进
        indent = 0
        while self.pos < len(self.source) and self.source[self.pos] == " ":
            indent += 1
            self.pos += 1

        # 跳过空行
        if self.pos < len(self.source) and self.source[self.pos] == "\n":
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
        """读取字符串

        读取双引号包围的字符串字面量，支持转义字符。

        Raises:
            LexerError: 当字符串未正确终止时
        """
        start_col = self.column
        self.pos += 1  # 跳过开头的 "
        start = self.pos

        while self.pos < len(self.source) and self.source[self.pos] != '"':
            if self.source[self.pos] == "\\":
                self.pos += 1  # 跳过转义字符
            self.pos += 1

        if self.pos >= len(self.source):
            raise LexerError("Unterminated string", self.line, start_col)

        value = self.source[start : self.pos]
        self.pos += 1  # 跳过结尾的 "
        self.column += self.pos - start + 1

        # 处理转义字符（注意顺序：先处理 \\，再处理其他）
        value = value.replace("\\\\", "\x00")  # 临时占位符
        value = value.replace("\\n", "\n")
        value = value.replace("\\t", "\t")
        value = value.replace('\\"', '"')
        value = value.replace("\x00", "\\")  # 恢复反斜杠

        self.tokens.append(Token(TokenType.STRING, value, self.line, start_col))

    def _read_number(self):
        """读取数字（整数或浮点数）

        读取连续的数字字符，支持一个小数点（浮点数）。

        Raises:
            LexerError: 当数字格式错误（如多个小数点）时
        """
        start_col = self.column
        start = self.pos
        dot_count = 0

        while self.pos < len(self.source):
            char = self.source[self.pos]
            if char.isdigit():
                self.pos += 1
            elif char == ".":
                dot_count += 1
                if dot_count > 1:
                    # 遇到第二个小数点，停止解析并报错
                    error_msg = (
                        f"Invalid number format: multiple decimal points "
                        f"in '{self.source[start:self.pos + 1]}'"
                    )
                    raise LexerError(error_msg, self.line, start_col)
                self.pos += 1
            else:
                break

        value = self.source[start : self.pos]
        self.column += len(value)

        if "." in value:
            self.tokens.append(Token(TokenType.NUMBER, float(value), self.line, start_col))
        else:
            self.tokens.append(Token(TokenType.NUMBER, int(value), self.line, start_col))

    def _read_symbol(self):
        """读取符号"""
        char = self.source[self.pos]
        token_type = SYMBOLS.get(char)

        if token_type is None:
            raise LexerError(f"Unknown symbol: {char}", self.line, self.column)

        self.tokens.append(Token(token_type, char, self.line, self.column))
        self.pos += 1
        self.column += 1

    def _is_chinese(self, char: str) -> bool:
        """判断字符是否为中文

        Args:
            char: 要判断的字符

        Returns:
            bool: 如果是中文字符返回True，否则返回False
        """
        return "\u4e00" <= char <= "\u9fff"

    def _read_chinese(self):
        """读取中文（关键字、操作符或标识符）

        使用最长匹配原则：
        1. 先读取完整的标识符（包括中文字符、英文、数字、下划线）
        2. 检查这个完整的标识符是否是关键字或操作符
        3. 如果是，则识别为关键字/操作符；否则识别为普通标识符

        支持的中文元素：
        - 关键字：定、函、若、则、否则、真、假等
        - 操作符：加、减、乘、除、等、且、或、非等
        - 标识符：用户定义的变量名、函数名等
        """
        start_col = self.column
        start = self.pos

        # 先尝试匹配内置函数（优先级最高，内置函数总是独立token）
        for func_name in BUILTIN_FUNCTIONS:
            if self.source[start : start + len(func_name)] == func_name:
                # 内置函数应该总是被识别为独立token，即使后面跟着其他字符
                # 因为内置函数后面可以跟参数（如"印结果"中的"结果"是参数，不是函数名的一部分）
                self.pos = start + len(func_name)
                self.column = start_col + len(func_name)
                self.tokens.append(Token(TokenType.IDENTIFIER, func_name, self.line, start_col))
                return

        # 使用最长匹配原则读取中文操作符或标识符
        # 需要考虑上下文来区分操作符和标识符

        # 先尝试匹配操作符（最长匹配）
        best_op_match = None
        best_op_len = 0
        for op in OPERATORS.keys():
            if self.source[start : start + len(op)] == op:
                if len(op) > best_op_len:
                    best_op_match = op
                    best_op_len = len(op)

        # 如果找到操作符匹配，检查上下文
        if best_op_match:
            # 检查前一个token是否是操作数（数字、标识符、字符串、右括号等）
            prev_is_operand = False
            # 检查前一个token是否是声明关键字（定、函等）
            prev_is_declaration = False

            if self.tokens:
                last_token = self.tokens[-1]
                if last_token.type in (
                    TokenType.NUMBER,
                    TokenType.IDENTIFIER,
                    TokenType.STRING,
                    TokenType.RPAREN,
                    TokenType.RBRACKET,
                    TokenType.RBRACE,
                ):
                    prev_is_operand = True
                elif last_token.type in (TokenType.VAR, TokenType.FUNCTION, TokenType.ASSIGN):
                    prev_is_declaration = True

            # 检查后面是否是操作数
            next_is_operand = False
            next_pos = start + best_op_len
            if next_pos < len(self.source):
                next_char = self.source[next_pos]
                if (
                    next_char.isdigit()
                    or next_char.isalpha()
                    or next_char == "_"
                    or self._is_chinese(next_char)
                ):
                    next_is_operand = True

            # 如果前面是声明关键字，则不识别为操作符（如"定 加 为 5"中的"加"是变量名）
            if prev_is_declaration:
                pass  # 继续作为标识符处理
            # 否则，识别为操作符
            # 修改：只要不是声明上下文，就识别为操作符
            # 这样可以正确处理单独出现的操作符（如"加 减 乘 除"）
            else:
                self.pos = start + best_op_len
                self.column = start_col + best_op_len
                self.tokens.append(
                    Token(OPERATORS[best_op_match], best_op_match, self.line, start_col)
                )
                return

        # 如果不是操作符，读取所有连续的中文字符作为标识符
        while self.pos < len(self.source) and self._is_chinese(self.source[self.pos]):
            self.pos += 1

        # 继续读取后面的英文/数字/下划线（支持混合标识符如"用户name"）
        while self.pos < len(self.source) and (
            self.source[self.pos].isalnum() or self.source[self.pos] == "_"
        ):
            self.pos += 1

        # 获取完整的标识符
        value = self.source[start : self.pos]

        # 检查是否为关键字
        if value in ALL_KEYWORDS:
            self.column = start_col + len(value)
            token_type = ALL_KEYWORDS[value]
            self.tokens.append(Token(token_type, value, self.line, start_col))
            return

        # 否则为普通标识符
        self.column = start_col + len(value)
        self.tokens.append(Token(TokenType.IDENTIFIER, value, self.line, start_col))

    def _read_identifier(self):
        """读取英文标识符"""
        start_col = self.column
        start = self.pos

        while self.pos < len(self.source) and (
            self.source[self.pos].isalnum() or self.source[self.pos] == "_"
        ):
            self.pos += 1

        value = self.source[start : self.pos]
        self.column += len(value)

        self.tokens.append(Token(TokenType.IDENTIFIER, value, self.line, start_col))
