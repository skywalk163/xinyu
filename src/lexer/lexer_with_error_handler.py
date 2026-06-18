# -*- coding: utf-8 -*-
"""词法分析器（集成错误处理）

这是词法分析器的增强版本，集成了统一的错误处理机制。
保持与原 Lexer 类的向后兼容性。
"""

from typing import List, Optional

from src.error_handling import ErrorCode, ErrorHandler, ErrorType
from src.lexer.keywords import ALL_KEYWORDS, BUILTIN_FUNCTIONS, OPERATORS, SYMBOLS
from src.lexer.tokens import Token, TokenType


class LexerWithErrorHandler:
    """词法分析器（集成错误处理）

    这是 Lexer 的增强版本，使用 ErrorHandler 统一处理错误，
    而不是抛出异常。这样可以收集多个错误，提供更好的错误报告。

    Attributes:
        source: 源代码字符串
        pos: 当前位置索引
        line: 当前行号
        column: 当前列号
        indent_stack: 缩进栈
        tokens: 已识别的Token列表
        error_handler: 错误处理器

    Example:
        >>> from src.error_handling import ErrorHandler
        >>> error_handler = ErrorHandler()
        >>> lexer = LexerWithErrorHandler("定 x 为 42", error_handler)
        >>> tokens = lexer.tokenize()
        >>> not error_handler.has_errors()
        True
    """

    def __init__(self, source: str, error_handler: Optional[ErrorHandler] = None):
        """初始化词法分析器

        Args:
            source: 要分析的源代码字符串
            error_handler: 错误处理器（可选，默认创建新实例）
        """
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 0
        self.indent_stack = [0]
        self.tokens: List[Token] = []
        self.error_handler = error_handler or ErrorHandler()

    def tokenize(self) -> List[Token]:
        """将源代码转换为Token序列

        对源代码进行词法分析，识别并提取所有的词法单元（Token）。
        遇到错误时不抛出异常，而是通过 error_handler 报告错误。

        Returns:
            List[Token]: Token序列列表，以EOF标记结束

        Example:
            >>> lexer = LexerWithErrorHandler("变量 x 为 42")
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
            # 处理注释
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
                # 报告错误而不是抛出异常
                self.error_handler.report_with_code(
                    ErrorCode.LEXER_INVALID_CHAR,
                    line=self.line,
                    column=self.column,
                    source=self.source,
                    char=repr(char),
                )
                self.pos += 1
                self.column += 1

        # 处理剩余的DEDENT
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token(TokenType.DEDENT, None, self.line, self.column))

        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens

    def _report_error(
        self, message: str, line: int, column: int, suggestion: Optional[str] = None
    ) -> None:
        """报告错误

        使用 error_handler 统一报告错误，而不是抛出异常。

        Args:
            message: 错误消息
            line: 行号
            column: 列号
            suggestion: 修复建议（可选）
        """
        self.error_handler.report(
            ErrorType.LEXER_ERROR, message, line, column, source=self.source, suggestion=suggestion
        )

    def _skip_whitespace(self):
        """跳过空白字符（不包括换行）"""
        while self.pos < len(self.source) and self.source[self.pos] in " \t":
            self.pos += 1
            self.column += 1

    def _skip_comment(self):
        """跳过注释"""
        while self.pos < len(self.source) and self.source[self.pos] != "\n":
            self.pos += 1

    def _handle_newline(self):
        """处理换行和缩进"""
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
        """读取字符串"""
        start_col = self.column
        self.pos += 1  # 跳过开头的 "
        start = self.pos

        while self.pos < len(self.source) and self.source[self.pos] != '"':
            if self.source[self.pos] == "\\":
                self.pos += 1  # 跳过转义字符
            self.pos += 1

        if self.pos >= len(self.source):
            # 报告错误而不是抛出异常
            self.error_handler.report_with_code(
                ErrorCode.LEXER_UNTERMINATED_STRING,
                line=self.line,
                column=start_col,
                source=self.source,
            )
            return

        value = self.source[start : self.pos]
        self.pos += 1  # 跳过结尾的 "
        self.column += self.pos - start + 1

        # 处理转义字符
        value = value.replace("\\\\", "\x00")
        value = value.replace("\\n", "\n")
        value = value.replace("\\t", "\t")
        value = value.replace('\\"', '"')
        value = value.replace("\x00", "\\")

        self.tokens.append(Token(TokenType.STRING, value, self.line, start_col))

    def _read_number(self):
        """读取数字（整数或浮点数）"""
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
                    # 报告错误
                    self._report_error(
                        "数字格式错误：多个小数点", self.line, start_col, suggestion="请检查数字格式，确保最多只有一个小数点"
                    )
                    return
                self.pos += 1
            else:
                break

        value_str = self.source[start : self.pos]
        self.column += self.pos - start

        if dot_count == 0:
            value = int(value_str)
        else:
            value = float(value_str)

        self.tokens.append(Token(TokenType.NUMBER, value, self.line, start_col))

    def _read_symbol(self):
        """读取符号"""
        char = self.source[self.pos]
        token_type = SYMBOLS[char]
        self.tokens.append(Token(token_type, char, self.line, self.column))
        self.pos += 1
        self.column += 1

    def _is_chinese(self, char: str) -> bool:
        """判断字符是否为中文"""
        return "\u4e00" <= char <= "\u9fff"

    def _read_chinese(self):
        """读取中文（关键字、操作符或标识符）"""
        start_col = self.column
        start = self.pos

        # 先尝试匹配内置函数
        for func_name in BUILTIN_FUNCTIONS:
            if self.source[start : start + len(func_name)] == func_name:
                self.pos = start + len(func_name)
                self.column = start_col + len(func_name)
                self.tokens.append(Token(TokenType.IDENTIFIER, func_name, self.line, start_col))
                return

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
            prev_is_operand = False
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
                    _ = True  # prev_is_operand - 未使用变量
                elif last_token.type in (TokenType.VAR, TokenType.FUNCTION, TokenType.ASSIGN):
                    prev_is_declaration = True

            # 如果前面是声明关键字，则不识别为操作符
            if prev_is_declaration:
                pass  # 继续作为标识符处理
            # 否则，识别为操作符
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

        # 继续读取后面的英文/数字/下划线
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
        self.column += self.pos - start

        # 检查是否为关键字
        if value in ALL_KEYWORDS:
            token_type = ALL_KEYWORDS[value]
            self.tokens.append(Token(token_type, value, self.line, start_col))
        else:
            self.tokens.append(Token(TokenType.IDENTIFIER, value, self.line, start_col))
