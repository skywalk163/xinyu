# -*- coding: utf-8 -*-
"""优化版词法分析器

性能优化策略：
1. 使用字符串查找代替正则表达式
2. 批量创建Token对象
3. 预计算关键字和操作符长度
4. 使用字典快速查找
5. 减少字符串切片操作
"""

from typing import List

from src.lexer.keywords import ALL_KEYWORDS, BUILTIN_FUNCTIONS, OPERATORS, SYMBOLS
from src.lexer.tokens import Token, TokenType


class OptimizedLexerError(Exception):
    """词法分析错误"""

    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"词法错误: {message} (行 {line}, 列 {column})")


class OptimizedLexer:
    """优化版词法分析器

    性能优化：
    - 使用字符串查找代替正则表达式
    - 批量Token创建
    - 预计算和缓存
    - 减少内存分配
    """

    def __init__(self, source: str):
        """初始化优化版词法分析器

        Args:
            source: 源代码字符串
        """
        self.source = source
        self.source_len = len(source)
        self.pos = 0
        self.line = 1
        self.column = 0
        self.tokens: List[Token] = []

        # 预计算关键字和操作符的最大长度
        self.max_keyword_len = max(len(k) for k in ALL_KEYWORDS.keys()) if ALL_KEYWORDS else 0
        self.max_operator_len = max(len(k) for k in OPERATORS.keys()) if OPERATORS else 0
        self.max_symbol_len = max(len(k) for k in SYMBOLS.keys()) if SYMBOLS else 0

        # 构建快速查找字典
        self._build_lookup_tables()

    def _build_lookup_tables(self):
        """构建快速查找表"""
        # 按长度分组的关键字查找表
        self.keywords_by_len = {}
        for keyword, token_type in ALL_KEYWORDS.items():
            length = len(keyword)
            if length not in self.keywords_by_len:
                self.keywords_by_len[length] = {}
            self.keywords_by_len[length][keyword] = token_type

        # 按长度分组的操作符查找表
        self.operators_by_len = {}
        for operator, token_type in OPERATORS.items():
            length = len(operator)
            if length not in self.operators_by_len:
                self.operators_by_len[length] = {}
            self.operators_by_len[length][operator] = token_type

        # 按长度分组的符号查找表
        self.symbols_by_len = {}
        for symbol, token_type in SYMBOLS.items():
            length = len(symbol)
            if length not in self.symbols_by_len:
                self.symbols_by_len[length] = {}
            self.symbols_by_len[length][symbol] = token_type

    def tokenize(self) -> List[Token]:
        """执行词法分析（优化版）

        Returns:
            Token序列
        """
        # 预分配Token列表（估算大小）
        _ = self.source_len // 3  # estimated_tokens - 未使用变量，平均每3个字符一个Token
        self.tokens = []

        while self.pos < self.source_len:
            self._skip_whitespace_fast()

            if self.pos >= self.source_len:
                break

            char = self.source[self.pos]

            # 快速处理换行
            if char == "\n":
                self._handle_newline_fast()
            # 快速处理数字
            elif char.isdigit():
                self._scan_number_fast()
            # 快速处理字符串
            elif char == '"':
                self._scan_string_fast()
            # 快速处理标识符和关键字
            elif self._is_identifier_start(char):
                self._scan_identifier_fast()
            # 快速处理符号和操作符
            else:
                self._scan_symbol_fast()

        # 添加EOF
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens

    def _skip_whitespace_fast(self):
        """快速跳过空白字符"""
        while self.pos < self.source_len:
            char = self.source[self.pos]
            if char in " \t\r":
                self.pos += 1
                self.column += 1
            else:
                break

    def _handle_newline_fast(self):
        """快速处理换行"""
        self.pos += 1
        self.line += 1
        self.column = 0

    def _scan_number_fast(self):
        """快速扫描数字"""
        start_pos = self.pos
        start_line = self.line
        start_column = self.column

        # 扫描整数部分
        while self.pos < self.source_len and self.source[self.pos].isdigit():
            self.pos += 1
            self.column += 1

        # 检查小数点
        if self.pos < self.source_len and self.source[self.pos] == ".":
            self.pos += 1
            self.column += 1

            # 扫描小数部分
            while self.pos < self.source_len and self.source[self.pos].isdigit():
                self.pos += 1
                self.column += 1

        # 提取数字字符串
        num_str = self.source[start_pos : self.pos]

        # 转换为数值
        if "." in num_str:
            value = float(num_str)
        else:
            value = int(num_str)

        self.tokens.append(Token(TokenType.NUMBER, value, start_line, start_column))

    def _scan_string_fast(self):
        """快速扫描字符串"""
        start_line = self.line
        start_column = self.column

        self.pos += 1  # 跳过开始引号
        self.column += 1

        start_pos = self.pos

        # 扫描字符串内容
        while self.pos < self.source_len and self.source[self.pos] != '"':
            if self.source[self.pos] == "\n":
                self.line += 1
                self.column = 0
            else:
                self.column += 1
            self.pos += 1

        if self.pos >= self.source_len:
            raise OptimizedLexerError("未终止的字符串", start_line, start_column)

        # 提取字符串内容
        value = self.source[start_pos : self.pos]

        self.pos += 1  # 跳过结束引号
        self.column += 1

        self.tokens.append(Token(TokenType.STRING, value, start_line, start_column))

    def _scan_identifier_fast(self):
        """快速扫描标识符和关键字"""
        start_pos = self.pos
        start_line = self.line
        start_column = self.column

        # 扫描标识符
        while self.pos < self.source_len and self._is_identifier_char(self.source[self.pos]):
            self.pos += 1
            self.column += 1

        identifier = self.source[start_pos : self.pos]
        identifier_len = len(identifier)

        # 快速查找关键字
        if identifier_len in self.keywords_by_len:
            if identifier in self.keywords_by_len[identifier_len]:
                token_type = self.keywords_by_len[identifier_len][identifier]
                self.tokens.append(Token(token_type, identifier, start_line, start_column))
                return

        # 快速查找内置函数
        if identifier in BUILTIN_FUNCTIONS:
            self.tokens.append(Token(TokenType.BUILTIN, identifier, start_line, start_column))
            return

        # 普通标识符
        self.tokens.append(Token(TokenType.IDENTIFIER, identifier, start_line, start_column))

    def _scan_symbol_fast(self):
        """快速扫描符号和操作符"""
        start_line = self.line
        start_column = self.column

        # 尝试匹配最长的操作符或符号
        max_len = max(self.max_operator_len, self.max_symbol_len)

        for length in range(max_len, 0, -1):
            if self.pos + length > self.source_len:
                continue

            substring = self.source[self.pos : self.pos + length]

            # 检查操作符
            if length in self.operators_by_len and substring in self.operators_by_len[length]:
                token_type = self.operators_by_len[length][substring]
                self.tokens.append(Token(token_type, substring, start_line, start_column))
                self.pos += length
                self.column += length
                return

            # 检查符号
            if length in self.symbols_by_len and substring in self.symbols_by_len[length]:
                token_type = self.symbols_by_len[length][substring]
                self.tokens.append(Token(token_type, substring, start_line, start_column))
                self.pos += length
                self.column += length
                return

        # 未识别的字符
        char = self.source[self.pos]
        raise OptimizedLexerError(f"未识别的字符: {char}", start_line, start_column)

    @staticmethod
    def _is_identifier_start(char: str) -> bool:
        """检查是否为标识符起始字符"""
        return char.isalpha() or char == "_" or "\u4e00" <= char <= "\u9fff"

    @staticmethod
    def _is_identifier_char(char: str) -> bool:
        """检查是否为标识符字符"""
        return char.isalnum() or char == "_" or "\u4e00" <= char <= "\u9fff"


# 性能对比测试
def benchmark_lexer():
    """词法分析器性能基准测试"""
    import time

    from src.lexer.lexer import Lexer

    # 测试代码
    test_code = (
        """
定 x = 5。
定 y = 10。
定 z = x 加 y。

若 z 大于 10 则：
    印"大于10"。
否则：
    印"小于等于10"。
"""
        * 100
    )  # 重复100次

    # 测试原始词法分析器
    start = time.time()
    lexer1 = Lexer(test_code)
    tokens1 = lexer1.tokenize()
    _ = .time() - start  # 未使用变量

    # 测试优化版词法分析器
    start = time.time()
    lexer2 = OptimizedLexer(test_code)
    tokens2 = lexer2.tokenize()
    _ = .time() - start  # 未使用变量

    print(f"原始词法分析器: {time1:.4f}秒, {len(tokens1)}个Token")
    print(f"优化词法分析器: {time2:.4f}秒, {len(tokens2)}个Token")
    print(f"性能提升: {(time1/time2):.2f}倍")


if __name__ == "__main__":
    benchmark_lexer()
