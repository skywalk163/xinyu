# -*- coding: utf-8 -*-
"""语法分析器

负责将Token序列转换为AST。
支持：
- 中文关键字和操作符
- 递归下降解析
- 缩进块（Python风格）
- 单行和多行语句
"""

from typing import List, Optional

from src.lexer.tokens import Token, TokenType
from src.parser.arity import Arity
from src.parser.ast_nodes import (
    AssignNode,
    ASTNode,
    BinaryOpNode,
    BlockNode,
    DictNode,
    ForNode,
    FunctionCallNode,
    FunctionDefNode,
    IdentifierNode,
    IfNode,
    IndexNode,
    ListNode,
    MemberAccessNode,
    NumberNode,
    ProgramNode,
    RepeatNode,
    ReturnNode,
    StringNode,
    UnaryOpNode,
    VarDefNode,
    WhileNode,
)
from src.parser.verb_registry import VerbRegistry


class ParseError(Exception):
    """解析错误异常类"""

    def __init__(self, message: str, token: Token, suggestion: str = None):
        self.message = message
        self.token = token
        self.suggestion = suggestion

        # 构建详细的错误信息
        error_msg = f"语法错误: {message} (行 {token.line}, 列 {token.column})"
        if suggestion:
            error_msg += f"\n  💡 建议: {suggestion}"

        super().__init__(error_msg)


class Parser:
    """语法分析器类

    使用递归下降解析方法，将Token序列转换为抽象语法树（AST）。

    支持特性：
    - 中文关键字和操作符
    - 缩进块（Python风格）
    - 单行和多行语句
    - 变量定义、函数定义、控制流语句

    Attributes:
        tokens: Token序列
        pos: 当前解析位置

    Example:
        >>> from src.lexer.lexer import Lexer
        >>> lexer = Lexer("定 x 为 42")
        >>> tokens = lexer.tokenize()
        >>> parser = Parser(tokens)
        >>> ast = parser.parse()
        >>> isinstance(ast, ProgramNode)
        True
    """

    def __init__(self, tokens: List[Token]):
        """初始化语法分析器

        Args:
            tokens: Token序列（由词法分析器生成）
        """
        self.tokens = tokens
        self.pos = 0

        # 初始化动词注册表
        self.verb_registry = VerbRegistry()
        self.verb_registry.register_builtin_verbs()

    # ============ 核心方法 ============

    def parse(self) -> ProgramNode:
        """解析Token序列生成抽象语法树

        主解析方法，遍历Token序列，解析所有语句，
        构建完整的抽象语法树。

        Returns:
            ProgramNode: 程序根节点，包含所有语句

        Raises:
            ParseError: 当遇到语法错误时
        """
        statements = []

        while not self._check(TokenType.EOF):
            # 跳过换行
            while self._check(TokenType.NEWLINE):
                self._advance()

            if self._check(TokenType.EOF):
                break

            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)

        return ProgramNode(line=1, column=0, statements=statements)

    def _current_token(self) -> Token:
        """获取当前token

        Returns:
            Token: 当前位置的Token，如果超出范围则返回EOF
        """
        if self.pos >= len(self.tokens):
            return self.tokens[-1]  # EOF
        return self.tokens[self.pos]

    def _check(self, *types: TokenType) -> bool:
        """检查当前token类型

        Args:
            *types: 要检查的TokenType列表

        Returns:
            bool: 如果当前token类型在给定类型列表中返回True
        """
        return self._current_token().type in types

    def _advance(self) -> Token:
        """前进到下一个token

        移动解析位置到下一个Token，并返回当前Token。

        Returns:
            Token: 当前Token
        """
        token = self._current_token()
        if not self._check(TokenType.EOF):
            self.pos += 1
        return token

    def _expect(self, token_type: TokenType, message: str) -> Token:
        """期望特定token类型

        检查当前Token是否为期望的类型，如果是则前进，否则抛出错误。

        Args:
            token_type: 期望的Token类型
            message: 错误消息

        Returns:
            Token: 匹配的Token

        Raises:
            ParseError: 当当前Token不是期望类型时
        """
        if self._check(token_type):
            return self._advance()
        raise ParseError(message, self._current_token())

    # ============ 元数系统辅助方法 ============

    def _is_at_end(self) -> bool:
        """检查是否到达Token序列末尾

        Returns:
            是否到达末尾
        """
        return self._check(TokenType.EOF)

    def _is_operator_verb(self, name: str) -> bool:
        """判断是否是操作符动词

        Args:
            name: 动词名称

        Returns:
            是否是操作符动词
        """
        return self.verb_registry.is_operator(name)

    def _get_verb_arity(self, name: str) -> Optional[Arity]:
        """获取动词元数

        Args:
            name: 动词名称

        Returns:
            元数定义，如果未注册则返回None
        """
        return self.verb_registry.get(name)

    def _should_stop_collecting_args(self) -> bool:
        """判断是否应该停止收集参数

        Returns:
            是否应该停止收集
        """
        current = self._current_token()

        # 遇到操作符动词（标识符形式），停止收集
        if current.type == TokenType.IDENTIFIER:
            if self._is_operator_verb(current.value):
                return True
            # 遇到另一个函数调用，停止收集
            # 如果下一个标识符是已注册动词（非操作符），停止
            if self.verb_registry.get(current.value) and not self.verb_registry.is_operator(
                current.value
            ):
                # 但如果是用户定义的函数，继续收集参数
                # 只有内置动词才停止
                pass

        # 遇到终止符，停止收集
        if self._check(
            TokenType.NEWLINE,
            TokenType.EOF,
            TokenType.PERIOD,
            TokenType.THEN,
            TokenType.ELSE,
            TokenType.ELIF,
            TokenType.RPAREN,
            TokenType.RBRACKET,
            TokenType.RBRACE,
            TokenType.COMMA,
            TokenType.COLON,
        ):
            return True

        return False

    def _collect_args_by_arity(self, arity: Arity) -> List[ASTNode]:
        """根据元数收集参数

        Args:
            arity: 元数定义

        Returns:
            参数列表
        """
        args = []

        while not self._is_at_end():
            # 检查是否应该停止收集
            if self._should_stop_collecting_args():
                break

            # 检查元数是否已满足
            if arity.should_stop_collecting(len(args)):
                break

            # 解析参数（解析包含操作符的子表达式）
            try:
                # 支持括号表达式作为参数
                if self._check(TokenType.LPAREN):
                    self._advance()  # 消费 (
                    arg = self._parse_term()  # 使用 _parse_term 而不是 _parse_expression
                    self._expect(TokenType.RPAREN, "Expected ')' after expression")
                    args.append(arg)
                    # 解析括号表达式后，继续收集下一个参数
                    continue
                else:
                    arg = self._parse_term()
                args.append(arg)
            except ParseError:
                break

        # 验证参数数量（对于固定元数和范围元数）
        if not arity.is_satisfied(len(args)):
            # 对于可变元数和最小元数，如果参数不足，给出警告但不报错
            from src.parser.arity import ArityType

            if arity.type in (ArityType.FIXED, ArityType.RANGE):
                # 如果完全没有参数，可能是标识符而非函数调用
                if len(args) == 0:
                    return []
                # 否则报错
                raise ParseError(f"参数数量错误：期望{arity}，实际{len(args)}", self._current_token())

        return args

    # ============ 语句解析 ============

    def _parse_statement(self) -> Optional[ASTNode]:
        """解析语句"""
        # 跳过换行
        while self._check(TokenType.NEWLINE):
            self._advance()

        # 跳过缩进/减进
        while self._check(TokenType.INDENT, TokenType.DEDENT):
            self._advance()

        if self._check(TokenType.EOF):
            return None

        # 变量定义：定 x = ...
        if self._check(TokenType.VAR):
            return self._parse_var_def()

        # 条件语句：若 ... 则 ...
        if self._check(TokenType.IF):
            return self._parse_if()

        # 遍历循环：遍历 x 于 列表：
        if self._check(TokenType.FOR):
            return self._parse_for()

        # 当循环：当 条件：
        if self._check(TokenType.WHILE):
            return self._parse_while()

        # 重复语句：重复 N 次：
        if self._check(TokenType.REPEAT):
            return self._parse_repeat()

        # 返回语句：返回 ...
        if self._check(TokenType.RETURN):
            return self._parse_return()

        # 异常处理语句：尝试 ... 捕获 ... 最终 ...
        if self._check(TokenType.TRY):
            return self._parse_try()

        # 抛出语句：抛出 ...
        if self._check(TokenType.RAISE):
            return self._parse_raise()

        # 导入语句：导入 ...
        if self._check(TokenType.IMPORT):
            return self._parse_import()

        # 从...导入语句：从 ... 导入 ...
        if self._check(TokenType.FROM):
            return self._parse_from_import()

        # 表达式语句（包括赋值）
        return self._parse_expression_statement()

    def _parse_expression_statement(self) -> ASTNode:
        """解析表达式语句"""
        # 检查是否是赋值语句：标识符 = 表达式
        if self._check(TokenType.IDENTIFIER):
            # 保存当前位置
            start_pos = self.pos
            name_token = self._advance()

            # 检查是否是赋值
            if self._check(TokenType.ASSIGN):
                self._advance()  # 消费 =
                value = self._parse_expression()

                # 消耗所有连续的句号（如果有）
                # 修改：使用while循环处理多个句号的情况
                while self._check(TokenType.PERIOD):
                    self._advance()

                return AssignNode(
                    line=name_token.line,
                    column=name_token.column,
                    target=IdentifierNode(
                        line=name_token.line, column=name_token.column, name=name_token.value
                    ),
                    value=value,
                )
            else:
                # 不是赋值，回退并解析表达式
                self.pos = start_pos

        # 解析表达式
        expr = self._parse_expression()

        # 消耗所有连续的句号（如果有）
        # 修改：使用while循环处理多个句号的情况
        while self._check(TokenType.PERIOD):
            self._advance()

        return expr

    # ============ 表达式解析（优先级从低到高） ============

    def _parse_term(self) -> ASTNode:
        """解析项（用于参数收集）

        解析包含操作符的子表达式，但只解析一层加减操作符。
        这允许参数如 "n 相减 1" 被解析为完整表达式，
        但不会继续解析 "n 相减 1 相加 ..." 中的 "相加"。

        注意：这是一个关键的修改，用于正确处理递归函数调用。
        """
        left = self._parse_multiplication_for_term()

        # 只解析一层加减操作符
        if self._check(TokenType.PLUS, TokenType.MINUS) or (
            self._check(TokenType.IDENTIFIER) and self._current_token().value in ("相加", "相减")
        ):
            op_token = self._advance()
            right = self._parse_multiplication_for_term()

            # 映射操作符
            if op_token.type == TokenType.IDENTIFIER:
                verb_map = {
                    "相加": "+",
                    "相减": "-",
                }
                op = verb_map.get(op_token.value, op_token.value)
            else:
                op_map = {
                    TokenType.PLUS: "+",
                    TokenType.MINUS: "-",
                }
                op = op_map[op_token.type]

            left = BinaryOpNode(
                line=left.line, column=left.column, left=left, operator=op, right=right
            )

        return left

    def _parse_atom_for_term(self) -> ASTNode:
        """解析原子表达式（用于项解析，支持函数调用）"""
        token = self._current_token()

        # 数字
        if self._check(TokenType.NUMBER):
            self._advance()
            return NumberNode(line=token.line, column=token.column, value=token.value)

        # 字符串
        if self._check(TokenType.STRING):
            self._advance()
            return StringNode(line=token.line, column=token.column, value=token.value)

        # 布尔值
        if self._check(TokenType.TRUE):
            self._advance()
            return IdentifierNode(line=token.line, column=token.column, name="真")

        if self._check(TokenType.FALSE):
            self._advance()
            return IdentifierNode(line=token.line, column=token.column, name="假")

        # 括号表达式
        if self._check(TokenType.LPAREN):
            self._advance()  # 消费 (
            expr = self._parse_term()  # 使用 _parse_term 而不是 _parse_expression
            self._expect(TokenType.RPAREN, "Expected ')' after expression")
            return expr

        # 列表字面量
        if self._check(TokenType.LBRACKET):
            return self._parse_list()

        # 字典字面量
        if self._check(TokenType.LBRACE):
            return self._parse_dict()

        # 标识符或函数调用
        if self._check(TokenType.IDENTIFIER):
            # 检查是否是操作符动词
            if self._is_operator_verb(token.value):
                # 操作符动词，返回标识符
                self._advance()
                return IdentifierNode(line=token.line, column=token.column, name=token.value)

            # 检查下一个token，判断是否是函数调用
            saved_pos = self.pos
            self._advance()  # 消费当前标识符

            # 检查是否是括号函数调用
            if self._check(TokenType.LPAREN):
                # 回退，使用正常的函数调用解析
                self.pos = saved_pos
                return self._parse_identifier_or_call_in_term()

            # 检查是否是无括号函数调用
            # 如果下一个token不是操作符、终止符，则可能是函数调用
            next_token = self._current_token()
            if next_token.type in (
                TokenType.NUMBER,
                TokenType.STRING,
                TokenType.IDENTIFIER,
            ) and not self._is_operator_verb(
                next_token.value if next_token.type == TokenType.IDENTIFIER else ""
            ):
                # 回退，使用正常的函数调用解析
                self.pos = saved_pos
                return self._parse_identifier_or_call_in_term()

            # 否则，返回普通标识符
            return IdentifierNode(line=token.line, column=token.column, name=token.value)

        raise ParseError(f"Unexpected token: {token.type.name}", token)

    def _parse_addition_for_term(self) -> ASTNode:
        """解析加减操作（用于项解析）"""
        left = self._parse_multiplication_for_term()

        while self._check(TokenType.PLUS, TokenType.MINUS) or (
            self._check(TokenType.IDENTIFIER) and self._current_token().value in ("相加", "相减")
        ):
            op_token = self._advance()
            right = self._parse_multiplication_for_term()

            # 映射操作符
            if op_token.type == TokenType.IDENTIFIER:
                verb_map = {
                    "相加": "+",
                    "相减": "-",
                }
                op = verb_map.get(op_token.value, op_token.value)
            else:
                op_map = {
                    TokenType.PLUS: "+",
                    TokenType.MINUS: "-",
                }
                op = op_map[op_token.type]

            left = BinaryOpNode(
                line=left.line, column=left.column, left=left, operator=op, right=right
            )

        return left

    def _parse_multiplication_for_term(self) -> ASTNode:
        """解析乘除操作（用于项解析）"""
        left = self._parse_comparison_for_term()

        while self._check(TokenType.MULTIPLY, TokenType.DIVIDE) or (
            self._check(TokenType.IDENTIFIER) and self._current_token().value in ("相乘", "相除", "取余")
        ):
            op_token = self._advance()
            right = self._parse_comparison_for_term()

            # 映射操作符
            if op_token.type == TokenType.IDENTIFIER:
                verb_map = {
                    "相乘": "*",
                    "相除": "/",
                    "取余": "%",
                }
                op = verb_map.get(op_token.value, op_token.value)
            else:
                op_map = {
                    TokenType.MULTIPLY: "*",
                    TokenType.DIVIDE: "/",
                }
                op = op_map[op_token.type]

            left = BinaryOpNode(
                line=left.line, column=left.column, left=left, operator=op, right=right
            )

        return left

    def _parse_comparison_for_term(self) -> ASTNode:
        """解析比较操作（用于项解析）"""
        left = self._parse_atom_for_term()

        while self._check(
            TokenType.EQUALS,
            TokenType.NOT_EQUALS,
            TokenType.LESS,
            TokenType.GREATER,
            TokenType.LESS_EQ,
            TokenType.GREATER_EQ,
        ) or (
            self._check(TokenType.IDENTIFIER)
            and self._current_token().value in ("等于", "不等于", "大于", "小于", "大于等于", "小于等于")
        ):
            op_token = self._advance()
            right = self._parse_primary()

            # 转换操作符
            if op_token.type == TokenType.IDENTIFIER:
                verb_map = {
                    "等于": "==",
                    "不等于": "!=",
                    "大于": ">",
                    "小于": "<",
                    "大于等于": ">=",
                    "小于等于": "<=",
                }
                op = verb_map.get(op_token.value, op_token.value)
            else:
                op_map = {
                    TokenType.EQUALS: "==",
                    TokenType.NOT_EQUALS: "!=",
                    TokenType.LESS: "<",
                    TokenType.GREATER: ">",
                    TokenType.LESS_EQ: "<=",
                    TokenType.GREATER_EQ: ">=",
                }
                op = op_map[op_token.type]

            left = BinaryOpNode(
                line=left.line, column=left.column, left=left, operator=op, right=right
            )

        return left

    def _parse_expression(self) -> ASTNode:
        """解析表达式"""
        return self._parse_pipe()

    def _parse_pipe(self) -> ASTNode:
        """解析管道操作"""
        expr = self._parse_or()

        # 检查是否有管道操作（逗号）
        while self._check(TokenType.COMMA):
            # 保存位置，以便回退
            pos = self.pos
            self._advance()  # 消费逗号

            # 检查下一个token，如果是数字、字符串、左括号等，可能是列表元素
            # 只有当下一个token是标识符或关键字（函数名）时，才处理管道操作
            if not self._check(
                TokenType.IDENTIFIER, TokenType.MAP, TokenType.FILTER, TokenType.REDUCE
            ):
                # 回退并退出
                self.pos = pos
                break

            # 解析管道右侧的函数
            func = self._parse_or()

            # 创建函数调用，将左侧表达式作为参数
            if isinstance(func, IdentifierNode):
                # 简单函数名：f -> f(expr)
                expr = FunctionCallNode(
                    line=func.line, column=func.column, name=func.name, args=[expr]
                )
            elif isinstance(func, FunctionCallNode):
                # 函数调用：f x -> f(expr, x) 或 f(x) -> f(expr)
                # 将expr插入到参数列表的最前面
                func.args.insert(0, expr)
                expr = func
            else:
                # 其他情况，创建函数调用
                expr = FunctionCallNode(line=func.line, column=func.column, name=func, args=[expr])

        return expr

    def _parse_or(self) -> ASTNode:
        """解析逻辑或操作"""
        left = self._parse_and()

        while self._check(TokenType.OR):
            op_token = self._advance()
            right = self._parse_and()

            left = BinaryOpNode(
                line=left.line, column=left.column, left=left, operator="or", right=right
            )

        return left

    def _parse_and(self) -> ASTNode:
        """解析逻辑与操作"""
        left = self._parse_comparison()

        while self._check(TokenType.AND):
            op_token = self._advance()
            right = self._parse_comparison()

            left = BinaryOpNode(
                line=left.line, column=left.column, left=left, operator="and", right=right
            )

        return left

    def _parse_comparison(self) -> ASTNode:
        """解析比较操作（==, !=, <, >, <=, >=）"""
        left = self._parse_addition()

        while self._check(
            TokenType.EQUALS,
            TokenType.NOT_EQUALS,
            TokenType.LESS,
            TokenType.GREATER,
            TokenType.LESS_EQ,
            TokenType.GREATER_EQ,
        ):
            op_token = self._advance()
            right = self._parse_addition()

            # 转换操作符
            op_map = {
                TokenType.EQUALS: "==",
                TokenType.NOT_EQUALS: "!=",
                TokenType.LESS: "<",
                TokenType.GREATER: ">",
                TokenType.LESS_EQ: "<=",
                TokenType.GREATER_EQ: ">=",
            }

            left = BinaryOpNode(
                line=left.line,
                column=left.column,
                left=left,
                operator=op_map[op_token.type],
                right=right,
            )

        return left

    def _parse_addition(self) -> ASTNode:
        """解析加减操作（+, -, 相加, 相减）"""
        left = self._parse_multiplication()

        while self._check(TokenType.PLUS, TokenType.MINUS) or (
            self._check(TokenType.IDENTIFIER) and self._current_token().value in ("相加", "相减")
        ):
            op_token = self._advance()
            right = self._parse_multiplication()

            # 映射操作符
            if op_token.type == TokenType.IDENTIFIER:
                # 操作符动词映射
                verb_map = {
                    "相加": "+",
                    "相减": "-",
                }
                op = verb_map.get(op_token.value, op_token.value)
            else:
                # Token类型映射
                op_map = {
                    TokenType.PLUS: "+",
                    TokenType.MINUS: "-",
                }
                op = op_map[op_token.type]

            left = BinaryOpNode(
                line=left.line, column=left.column, left=left, operator=op, right=right
            )

        return left

    def _parse_multiplication(self) -> ASTNode:
        """解析乘除操作（*, /, 相乘, 相除）"""
        left = self._parse_unary()

        while self._check(TokenType.MULTIPLY, TokenType.DIVIDE) or (
            self._check(TokenType.IDENTIFIER) and self._current_token().value in ("相乘", "相除", "取余")
        ):
            op_token = self._advance()
            right = self._parse_unary()

            # 映射操作符
            if op_token.type == TokenType.IDENTIFIER:
                # 操作符动词映射
                verb_map = {
                    "相乘": "*",
                    "相除": "/",
                    "取余": "%",
                }
                op = verb_map.get(op_token.value, op_token.value)
            else:
                # Token类型映射
                op_map = {
                    TokenType.MULTIPLY: "*",
                    TokenType.DIVIDE: "/",
                }
                op = op_map[op_token.type]

            left = BinaryOpNode(
                line=left.line, column=left.column, left=left, operator=op, right=right
            )

        return left

    def _parse_unary(self) -> ASTNode:
        """解析一元操作（not, -）"""
        if self._check(TokenType.NOT):
            op_token = self._advance()
            operand = self._parse_unary()
            return UnaryOpNode(
                line=op_token.line, column=op_token.column, operator="not", operand=operand
            )

        if self._check(TokenType.MINUS):
            op_token = self._advance()
            operand = self._parse_unary()
            return UnaryOpNode(
                line=op_token.line, column=op_token.column, operator="-", operand=operand
            )

        return self._parse_primary()

    def _parse_primary(self) -> ASTNode:
        """解析基础表达式（数字、字符串、标识符、括号、列表）"""
        token = self._current_token()

        # 数字
        if self._check(TokenType.NUMBER):
            self._advance()
            node = NumberNode(line=token.line, column=token.column, value=token.value)
            # 检查是否是意合式调用
            if self._check(TokenType.PAUSE_MARK):
                return self._parse_intentional_call_from_literal(node)
            return node

        # 字符串
        if self._check(TokenType.STRING):
            self._advance()
            node = StringNode(line=token.line, column=token.column, value=token.value)
            # 检查是否是意合式调用
            if self._check(TokenType.PAUSE_MARK):
                return self._parse_intentional_call_from_literal(node)
            return node

        # 布尔值
        if self._check(TokenType.TRUE):
            self._advance()
            return IdentifierNode(line=token.line, column=token.column, name="真")

        if self._check(TokenType.FALSE):
            self._advance()
            return IdentifierNode(line=token.line, column=token.column, name="假")

        # 列表字面量 [1, 2, 3] 或 【1，2，3】
        if self._check(TokenType.LBRACKET):
            return self._parse_list()

        # 字典字面量
        if self._check(TokenType.LBRACE):
            return self._parse_dict()

        # 括号表达式
        if self._check(TokenType.LPAREN):
            self._advance()  # 消费 (
            expr = self._parse_expression()
            self._expect(TokenType.RPAREN, "Expected ')' after expression")
            return expr

        # 标识符或函数调用
        if self._check(TokenType.IDENTIFIER):
            return self._parse_identifier_or_call()

        # 高阶函数关键字（皆、只、归）
        if self._check(TokenType.MAP, TokenType.FILTER, TokenType.REDUCE):
            token = self._advance()
            # 将关键字转换为标识符节点
            return IdentifierNode(line=token.line, column=token.column, name=token.value)

        raise ParseError(f"Unexpected token: {token.type.name}", token)

    def _parse_intentional_call_from_literal(self, first_arg: ASTNode) -> ASTNode:
        """
        从数字或字符串字面量开始解析意合式调用

        语法：参数1、参数2，函数名。
        示例：10、20，求和。
        """
        args = [first_arg]

        # 收集顿号分隔的参数
        while self._check(TokenType.PAUSE_MARK):
            self._advance()  # 消费顿号

            # 解析下一个参数（只支持基本类型：数字、字符串、标识符）
            # 直接解析，不检查意合式调用
            token = self._current_token()

            if self._check(TokenType.NUMBER):
                self._advance()
                args.append(NumberNode(line=token.line, column=token.column, value=token.value))
            elif self._check(TokenType.STRING):
                self._advance()
                args.append(StringNode(line=token.line, column=token.column, value=token.value))
            elif self._check(TokenType.IDENTIFIER):
                self._advance()
                args.append(IdentifierNode(line=token.line, column=token.column, name=token.value))
            else:
                raise ParseError(f"Expected argument after '、', got {token.type.name}", token)

        # 检查是否有逗号和函数名
        if self._check(TokenType.COMMA):
            self._advance()  # 消费逗号

            # 解析函数名
            if self._check(TokenType.IDENTIFIER):
                func_token = self._advance()
                func_name = func_token.value

                # 消耗句号（如果有）
                if self._check(TokenType.PERIOD):
                    self._advance()

                return FunctionCallNode(
                    line=first_arg.line, column=first_arg.column, name=func_name, args=args
                )

        # 如果没有逗号和函数名，说明不是意合式调用
        # 这种情况不应该发生，因为我们是在看到顿号后才调用这个方法的
        raise ParseError(
            "Expected function name after intentional call arguments", self._current_token()
        )

    def _parse_list(self) -> ListNode:
        """解析列表字面量"""
        token = self._advance()  # 消费 [ 或 【
        elements = []

        # 解析元素列表
        while not self._check(TokenType.RBRACKET):
            elem = self._parse_expression()
            elements.append(elem)

            # 跳过逗号（中文或英文）
            if self._check(TokenType.COMMA):
                self._advance()

        self._expect(TokenType.RBRACKET, "Expected ']' or '】' after list elements")

        return ListNode(line=token.line, column=token.column, elements=elements)

    def _parse_dict(self) -> DictNode:
        """解析字典字面量"""
        token = self._advance()  # 消费 {
        pairs = []

        # 解析键值对列表
        while not self._check(TokenType.RBRACE):
            # 解析键
            key = self._parse_expression()

            # 期望冒号（中文或英文）
            self._expect(TokenType.COLON, "Expected '：' or ':' after dictionary key")

            # 解析值
            value = self._parse_expression()

            pairs.append((key, value))

            # 跳过逗号（中文或英文）
            if self._check(TokenType.COMMA):
                self._advance()

        self._expect(TokenType.RBRACE, "Expected '}' after dictionary pairs")

        return DictNode(line=token.line, column=token.column, pairs=pairs)

    def _parse_identifier_or_call(self) -> ASTNode:
        """解析标识符或函数调用（元数驱动）"""
        token = self._advance()
        name = token.value

        # 检查是否为意合式调用：参数1、参数2，函数名。
        if self._check(TokenType.PAUSE_MARK):
            return self._parse_intentional_call(token)

        # 检查是否为括号函数调用：（参数）
        if self._check(TokenType.LPAREN):
            self._advance()  # 消费 （
            args = []

            # 解析参数列表
            while not self._check(TokenType.RPAREN):
                arg = self._parse_expression()
                args.append(arg)

                # 跳过逗号
                if self._check(TokenType.COMMA):
                    self._advance()

            self._expect(TokenType.RPAREN, "Expected '）' after arguments")

            node = FunctionCallNode(line=token.line, column=token.column, name=name, args=args)
            return self._parse_postfix(node)

        # 检查是否是操作符动词（在中缀位置）
        if self._is_operator_verb(name):
            # 操作符动词在中缀位置，不应该作为函数调用
            # 回退，让表达式解析器处理
            self.pos -= 1
            return IdentifierNode(line=token.line, column=token.column, name=name)

        # 获取动词元数
        arity = self._get_verb_arity(name)

        if arity is None:
            # 未注册的动词，可能是用户定义的函数
            # 使用可变元数，允许收集多个参数
            # 这样可以正确处理 "自定义函数 1 2 3" 的情况
            arity = Arity.variable(0)  # 可变元数，最少0个参数

        # 根据元数收集参数
        args = self._collect_args_by_arity(arity)

        if args:
            node = FunctionCallNode(line=token.line, column=token.column, name=name, args=args)
            return self._parse_postfix(node)

        node = IdentifierNode(line=token.line, column=token.column, name=name)
        return self._parse_postfix(node)

    def _parse_identifier_or_call_in_term(self) -> ASTNode:
        """解析标识符或函数调用（在项解析中，限制参数收集）

        与 _parse_identifier_or_call() 类似，但使用固定元数（1个参数），
        避免收集过多参数。
        """
        token = self._advance()
        name = token.value

        # 检查是否为意合式调用：参数1、参数2，函数名。
        if self._check(TokenType.PAUSE_MARK):
            return self._parse_intentional_call(token)

        # 检查是否为括号函数调用：（参数）
        # 在项解析中，我们不处理括号函数调用，让 _collect_args_by_arity 处理
        # 因为 函数名 (表达式) 参数 应该被解析为函数调用，参数为 (表达式) 和 参数
        # 而不是 函数名(表达式, 参数)
        # 所以这里直接跳过，让后面的逻辑处理
        if self._check(TokenType.LPAREN):
            # 如果是左括号，不处理括号函数调用，让 _collect_args_by_arity 处理
            pass

        # 检查是否是操作符动词（在中缀位置）
        if self._is_operator_verb(name):
            # 操作符动词在中缀位置，不应该作为函数调用
            # 回退，让表达式解析器处理
            self.pos -= 1
            return IdentifierNode(line=token.line, column=token.column, name=name)

        # 获取动词元数
        arity = self._get_verb_arity(name)

        if arity is None:
            # 未注册的动词，可能是用户定义的函数
            # 使用可变元数，允许收集多个参数
            # 这样可以正确处理 "自定义函数 1 2 3" 的情况
            arity = Arity.variable()

        # 根据元数收集参数
        args = self._collect_args_by_arity(arity)

        if args:
            node = FunctionCallNode(line=token.line, column=token.column, name=name, args=args)
            return self._parse_postfix(node)

        node = IdentifierNode(line=token.line, column=token.column, name=name)
        return self._parse_postfix(node)

        # 检查是否是操作符动词（在中缀位置）
        if self._is_operator_verb(name):
            # 操作符动词在中缀位置，不应该作为函数调用
            # 回退，让表达式解析器处理
            self.pos -= 1
            return IdentifierNode(line=token.line, column=token.column, name=name)

        # 获取动词元数
        arity = self._get_verb_arity(name)

        if arity is None:
            # 未注册的动词，可能是用户定义的函数
            # 使用可变元数，允许收集多个参数
            # 这样可以正确处理 "自定义函数 1 2 3" 的情况
            arity = Arity.variable()

        # 根据元数收集参数
        args = self._collect_args_by_arity(arity)

        if args:
            node = FunctionCallNode(line=token.line, column=token.column, name=name, args=args)
            return self._parse_postfix(node)

        node = IdentifierNode(line=token.line, column=token.column, name=name)
        return self._parse_postfix(node)

    def _parse_intentional_call(self, first_token: Token) -> ASTNode:
        """
        解析意合式调用

        语法：参数1、参数2，函数名。
        示例：北京、上海，计算距离。
        """
        args = []

        # 第一个参数已经解析过了（first_token对应的标识符）
        args.append(
            IdentifierNode(line=first_token.line, column=first_token.column, name=first_token.value)
        )

        # 收集顿号分隔的参数
        while self._check(TokenType.PAUSE_MARK):
            self._advance()  # 消费顿号

            # 解析下一个参数
            arg = self._parse_primary()
            args.append(arg)

        # 检查是否有逗号和函数名
        if self._check(TokenType.COMMA):
            self._advance()  # 消费逗号

            # 解析函数名
            if self._check(TokenType.IDENTIFIER):
                func_token = self._advance()
                func_name = func_token.value

                # 消耗句号（如果有）
                if self._check(TokenType.PERIOD):
                    self._advance()

                return FunctionCallNode(
                    line=first_token.line, column=first_token.column, name=func_name, args=args
                )

        # 如果没有逗号和函数名，说明不是意合式调用
        # 返回第一个参数（这种情况下应该报错，但为了简单起见，返回第一个标识符）
        return args[0]

    def _parse_postfix(self, node: ASTNode) -> ASTNode:
        """解析后缀表达式（成员访问、索引、函数调用）"""
        while True:
            # 成员访问：obj.member
            if self._check(TokenType.DOT):
                self._advance()  # 消费 .
                if self._check(TokenType.IDENTIFIER):
                    member_token = self._advance()
                    node = MemberAccessNode(
                        line=node.line, column=node.column, obj=node, member=member_token.value
                    )
                else:
                    raise ParseError("Expected identifier after '.'", self._current_token())
            # 索引访问：obj[index]
            elif self._check(TokenType.LBRACKET):
                self._advance()  # 消费 [
                index = self._parse_expression()
                self._expect(TokenType.RBRACKET, "Expected ']' after index")
                node = IndexNode(line=node.line, column=node.column, obj=node, index=index)
            # 函数调用：func(args)
            elif self._check(TokenType.LPAREN):
                self._advance()  # 消费 (
                args = []
                if not self._check(TokenType.RPAREN):
                    args.append(self._parse_expression())
                    while self._check(TokenType.COMMA):
                        self._advance()
                        args.append(self._parse_expression())
                self._expect(TokenType.RPAREN, "Expected ')' after arguments")
                # 对于成员访问，我们需要生成正确的函数调用
                # 例如：math.sqrt(16) 应该生成 math.sqrt(16)
                node = FunctionCallNode(
                    line=node.line,
                    column=node.column,
                    name=node,  # 将整个node作为name（可以是IdentifierNode或MemberAccessNode）
                    args=args,
                )
            else:
                break

        return node

    # ============ 控制流解析 ============

    def _parse_if(self) -> IfNode:
        """解析条件语句（若 ... 则 ... 否则 ...）"""
        token = self._advance()  # 消费 若

        # 解析条件
        condition = self._parse_expression()

        # 期望 那么
        self._expect(TokenType.THEN, "Expected '那么' after condition")

        # 消费冒号（可选）
        if self._check(TokenType.COLON):
            self._advance()

        # 解析 then 分支
        then_branch = self._parse_block()

        # 检查是否有 else 分支
        else_branch = None
        if self._check(TokenType.ELSE):
            self._advance()  # 消费 否则
            # 消费冒号（可选）
            if self._check(TokenType.COLON):
                self._advance()
            else_branch = self._parse_block()

        # 消费结尾的 。
        if self._check(TokenType.PERIOD):
            self._advance()

        return IfNode(
            line=token.line,
            column=token.column,
            condition=condition,
            then_branch=then_branch,
            else_branch=else_branch,
        )

    def _parse_for(self) -> ForNode:
        """解析遍历循环（循环 x 于 列表：...）"""
        token = self._advance()  # 消费 循环

        # 解析循环变量
        var_token = self._expect(TokenType.IDENTIFIER, "Expected variable name after '循环'")
        var = var_token.value

        # 期望 于
        self._expect(TokenType.IN, "Expected '于' after variable name")

        # 解析可迭代对象
        iterable = self._parse_expression()

        # 期望 ：
        self._expect(TokenType.COLON, "Expected '：' after iterable")

        # 解析循环体
        body = self._parse_block()

        # 消费结尾的 。
        if self._check(TokenType.PERIOD):
            self._advance()

        return ForNode(line=token.line, column=token.column, var=var, iterable=iterable, body=body)

    def _parse_while(self) -> WhileNode:
        """解析当循环（当 条件 时：... 或 当满足 条件：...）"""
        token = self._advance()  # 消费 当 或 当满足

        # 解析条件
        condition = self._parse_expression()

        # 可选的"时"关键字
        if self._check(TokenType.THEN):
            self._advance()  # 消费 时

        # 期望 ：
        self._expect(TokenType.COLON, "Expected '：' after condition")

        # 解析循环体
        body = self._parse_block()

        # 消费结尾的 。
        if self._check(TokenType.PERIOD):
            self._advance()

        return WhileNode(line=token.line, column=token.column, condition=condition, body=body)

    def _parse_repeat(self) -> RepeatNode:
        """解析重复语句（重复 N 次：...）"""
        token = self._advance()  # 消费 重复

        # 解析重复次数
        count = self._parse_expression()

        # 期望 次数
        self._expect(TokenType.TIMES, "Expected '次数' after count")

        # 期望 ：
        self._expect(TokenType.COLON, "Expected '：' after '次数'")

        # 解析循环体
        body = self._parse_block()

        # 消费结尾的 。
        if self._check(TokenType.PERIOD):
            self._advance()

        return RepeatNode(line=token.line, column=token.column, count=count, body=body)

    # ============ 函数解析 ============

    def _parse_var_def(self) -> ASTNode:
        """解析变量定义（定 x = 5）"""
        token = self._advance()  # 消费 定

        # 解析变量名
        name_token = self._expect(TokenType.IDENTIFIER, "Expected variable name after '定'")
        name = name_token.value

        # 期望 =
        self._expect(TokenType.ASSIGN, "Expected '=' after variable name")

        # 检查是否为函数定义
        if self._check(TokenType.FUNCTION):
            func_def = self._parse_function_def(name, token.line, token.column)
            # 函数定义应该包装在 VarDefNode 中
            return VarDefNode(line=token.line, column=token.column, name=name, value=func_def)

        # 解析值
        value = self._parse_expression()

        # 消费语句结束符 。
        if self._check(TokenType.PERIOD):
            self._advance()

        return VarDefNode(line=token.line, column=token.column, name=name, value=value)

    def _parse_function_def(self, name: str, line: int, column: int) -> FunctionDefNode:
        """解析函数定义"""
        self._advance()  # 消费 函 或 函数

        # 解析参数列表
        params = []
        while not self._check(TokenType.COLON, TokenType.NEWLINE, TokenType.EOF):
            if self._check(TokenType.IDENTIFIER):
                param_token = self._advance()
                params.append(param_token.value)
                # 跳过逗号（中文或英文）
                if self._check(TokenType.COMMA):
                    self._advance()
            else:
                break

        # 期望 ：
        self._expect(TokenType.COLON, "Expected '：' after function parameters")

        # 解析函数体
        body = self._parse_block()

        # 消费结尾的 。
        if self._check(TokenType.PERIOD):
            self._advance()

        # 推断元数：根据参数数量
        arity = Arity.fixed(len(params))

        # 注册到动词注册表
        self.verb_registry.register(name, arity, is_function=True)

        return FunctionDefNode(line=line, column=column, name=name, params=params, body=body)

    def _parse_return(self) -> ReturnNode:
        """解析返回语句"""
        token = self._advance()  # 消费 返回

        # 检查是否有返回值
        value = None
        if not self._check(TokenType.NEWLINE, TokenType.EOF, TokenType.PERIOD):
            value = self._parse_expression()

        # 消费语句结束符 。
        if self._check(TokenType.PERIOD):
            self._advance()

        return ReturnNode(line=token.line, column=token.column, value=value)

    def _parse_try(self) -> "TryNode":
        """解析try-except-finally语句

        语法：
        尝试：
            try块。
        捕获 异常类型 那么：
            except块。
        最终：
            finally块。
        。
        """
        from src.parser.ast_nodes import ExceptNode, TryNode

        token = self._advance()  # 消费 尝试

        # 消费冒号
        if self._check(TokenType.COLON):
            self._advance()

        # 解析try块
        try_body = self._parse_block()

        # 解析except子句（可能有多个）
        except_clauses = []
        while self._check(TokenType.CATCH):
            except_node = self._parse_except()
            except_clauses.append(except_node)

        # 解析finally块（可选）
        finally_body = None
        if self._check(TokenType.FINALLY):
            self._advance()  # 消费 最终
            if self._check(TokenType.COLON):
                self._advance()
            finally_body = self._parse_block()

        # 消费语句结束符 。
        if self._check(TokenType.PERIOD):
            self._advance()

        return TryNode(
            line=token.line,
            column=token.column,
            try_body=try_body,
            except_clauses=except_clauses,
            finally_body=finally_body,
        )

    def _parse_except(self) -> "ExceptNode":
        """解析except子句

        语法：
        捕获 异常类型 那么：
            except块。
        或
        捕获 异常类型 为 变量名 那么：
            except块。
        """
        from src.parser.ast_nodes import ExceptNode

        token = self._advance()  # 消费 捕获

        # 解析异常类型（可选）
        exception_type = None
        exception_var = None

        if not self._check(TokenType.THEN, TokenType.COLON):
            # 解析异常类型
            exception_type = self._parse_expression()

            # 检查是否有异常变量（为 变量名）
            if self._check(TokenType.AS):
                self._advance()  # 消费 为
                if self._check(TokenType.IDENTIFIER):
                    var_token = self._advance()
                    exception_var = var_token.value

        # 消费 那么
        if self._check(TokenType.THEN):
            self._advance()

        # 消费冒号
        if self._check(TokenType.COLON):
            self._advance()

        # 解析except块
        body = self._parse_block()

        return ExceptNode(
            line=token.line,
            column=token.column,
            exception_type=exception_type,
            exception_var=exception_var,
            body=body,
        )

    def _parse_raise(self) -> "RaiseNode":
        """解析raise语句

        语法：
        抛出 异常对象。
        或
        抛出。
        """
        from src.parser.ast_nodes import RaiseNode

        token = self._advance()  # 消费 抛出

        # 检查是否有异常对象
        exception = None
        if not self._check(TokenType.NEWLINE, TokenType.EOF, TokenType.PERIOD):
            exception = self._parse_expression()

        # 消费语句结束符 。
        if self._check(TokenType.PERIOD):
            self._advance()

        return RaiseNode(line=token.line, column=token.column, exception=exception)

    def _parse_import(self) -> "ImportNode":
        """解析import语句

        语法：
        导入 模块名。
        导入 模块名 为 别名。
        """
        from src.parser.ast_nodes import ImportNode

        token = self._advance()  # 消费 导入

        # 解析模块名
        if not self._check(TokenType.IDENTIFIER):
            raise ParseError("期望模块名", self._current_token())

        module_token = self._advance()
        module_name = module_token.value

        # 解析别名（可选）
        alias = None
        if self._check(TokenType.AS):
            self._advance()  # 消费 为
            if not self._check(TokenType.IDENTIFIER):
                raise ParseError("期望别名", self._current_token())
            alias_token = self._advance()
            alias = alias_token.value

        # 消费语句结束符 。
        if self._check(TokenType.PERIOD):
            self._advance()

        return ImportNode(line=token.line, column=token.column, module=module_name, alias=alias)

    def _parse_from_import(self) -> "FromImportNode":
        """解析from...import语句

        语法：
        从 模块名 导入 名称。
        从 模块名 导入 名称1, 名称2。
        从 模块名 导入 名称 为 别名。
        """
        from src.parser.ast_nodes import FromImportNode

        token = self._advance()  # 消费 从

        # 解析模块名
        if not self._check(TokenType.IDENTIFIER):
            raise ParseError("期望模块名", self._current_token())

        module_token = self._advance()
        module_name = module_token.value

        # 消费 导入
        if not self._check(TokenType.IMPORT):
            raise ParseError("期望 '导入'", self._current_token())
        self._advance()

        # 解析导入的名称列表
        names = []
        aliases = {}

        while True:
            # 解析名称
            if not self._check(TokenType.IDENTIFIER):
                raise ParseError("期望导入的名称", self._current_token())

            name_token = self._advance()
            name = name_token.value
            names.append(name)

            # 检查是否有别名
            if self._check(TokenType.AS):
                self._advance()  # 消费 为
                if not self._check(TokenType.IDENTIFIER):
                    raise ParseError("期望别名", self._current_token())
                alias_token = self._advance()
                aliases[name] = alias_token.value

            # 检查是否有逗号（继续导入更多名称）
            if self._check(TokenType.COMMA):
                self._advance()
                continue
            else:
                break

        # 消费语句结束符 。
        if self._check(TokenType.PERIOD):
            self._advance()

        return FromImportNode(
            line=token.line, column=token.column, module=module_name, names=names, aliases=aliases
        )

    # ============ 块解析 ============

    def _parse_block(self) -> List[ASTNode]:
        """解析代码块（支持单行和多行）"""
        statements = []

        # 跳过换行
        while self._check(TokenType.NEWLINE):
            self._advance()

        # 检查是否有缩进（多行块）
        if self._check(TokenType.INDENT):
            self._advance()  # 消费 INDENT

            # 解析块内语句
            while not self._check(TokenType.DEDENT, TokenType.EOF):
                # 跳过换行
                while self._check(TokenType.NEWLINE):
                    self._advance()

                if self._check(TokenType.DEDENT, TokenType.EOF):
                    break

                stmt = self._parse_statement()
                if stmt:
                    statements.append(stmt)

            # 消费 DEDENT
            if self._check(TokenType.DEDENT):
                self._advance()
        else:
            # 单行块
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)

        return statements
