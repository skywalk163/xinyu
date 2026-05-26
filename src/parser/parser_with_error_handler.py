# -*- coding: utf-8 -*-
"""语法分析器（集成错误处理）

这是语法分析器的增强版本，集成了统一的错误处理机制。
保持与原 Parser 类的向后兼容性。
"""

from typing import List, Optional
from src.lexer.tokens import Token, TokenType
from src.parser.ast_nodes import (
    ProgramNode, NumberNode, StringNode, IdentifierNode,
    BinaryOpNode, UnaryOpNode, ListNode, DictNode,
    MemberAccessNode, IndexNode, AssignNode, VarDefNode,
    IfNode, ForNode, WhileNode, RepeatNode,
    FunctionDefNode, FunctionCallNode, ReturnNode,
    BlockNode, ASTNode
)
from src.error_handling import ErrorHandler, ErrorType


class ParserWithErrorHandler:
    """语法分析器（集成错误处理）
    
    这是 Parser 的增强版本，使用 ErrorHandler 统一处理错误，
    而不是抛出异常。这样可以收集多个错误，提供更好的错误报告。
    
    Attributes:
        tokens: Token序列
        pos: 当前解析位置
        error_handler: 错误处理器
    
    Example:
        >>> from src.lexer.lexer import Lexer
        >>> from src.error_handling import ErrorHandler
        >>> error_handler = ErrorHandler()
        >>> lexer = Lexer("定 x = 42")
        >>> tokens = lexer.tokenize()
        >>> parser = ParserWithErrorHandler(tokens, error_handler)
        >>> ast = parser.parse()
        >>> not error_handler.has_errors()
        True
    """

    def __init__(self, tokens: List[Token], error_handler: Optional[ErrorHandler] = None):
        """初始化语法分析器
        
        Args:
            tokens: Token序列（由词法分析器生成）
            error_handler: 错误处理器（可选，默认创建新实例）
        """
        self.tokens = tokens
        self.pos = 0
        self.error_handler = error_handler or ErrorHandler()

    def _report_error(
        self,
        message: str,
        token: Token,
        suggestion: Optional[str] = None
    ) -> None:
        """报告错误
        
        使用 error_handler 统一报告错误，而不是抛出异常。
        
        Args:
            message: 错误消息
            token: 发生错误的Token
            suggestion: 修复建议（可选）
        """
        self.error_handler.report(
            ErrorType.PARSER_ERROR,
            message,
            token.line,
            token.column,
            suggestion=suggestion
        )

    def parse(self) -> ProgramNode:
        """解析Token序列生成抽象语法树
        
        主解析方法，遍历Token序列，解析所有语句，
        构建完整的抽象语法树。遇到错误时不抛出异常，
        而是通过 error_handler 报告错误。
        
        Returns:
            ProgramNode: 程序根节点，包含所有语句
        """
        statements = []

        while not self._check(TokenType.EOF):
            # 跳过换行
            while self._check(TokenType.NEWLINE):
                self._advance()

            if self._check(TokenType.EOF):
                break

            try:
                stmt = self._parse_statement()
                if stmt:
                    statements.append(stmt)
            except Exception as e:
                # 报告错误并尝试恢复
                self._report_error(
                    f"解析语句时发生错误: {str(e)}",
                    self._current_token(),
                    suggestion="请检查语法是否正确"
                )
                # 跳过当前token，尝试继续解析
                self._advance()

        return ProgramNode(line=1, column=0, statements=statements)

    def _current_token(self) -> Token:
        """获取当前token"""
        if self.pos >= len(self.tokens):
            return self.tokens[-1]  # EOF
        return self.tokens[self.pos]

    def _check(self, *types: TokenType) -> bool:
        """检查当前token类型"""
        return self._current_token().type in types

    def _advance(self) -> Token:
        """前进到下一个token"""
        token = self._current_token()
        if not self._check(TokenType.EOF):
            self.pos += 1
        return token

    def _expect(self, token_type: TokenType, message: str) -> Optional[Token]:
        """期望特定token类型
        
        检查当前Token是否为期望的类型，如果是则前进，否则报告错误。
        
        Args:
            token_type: 期望的Token类型
            message: 错误消息
        
        Returns:
            Token: 匹配的Token，如果类型不匹配则返回None
        """
        if self._check(token_type):
            return self._advance()
        
        # 报告错误而不是抛出异常
        self._report_error(
            message,
            self._current_token(),
            suggestion=f"期望 {token_type.name}"
        )
        return None

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
                while self._check(TokenType.PERIOD):
                    self._advance()

                return AssignNode(
                    line=name_token.line,
                    column=name_token.column,
                    target=IdentifierNode(
                        line=name_token.line,
                        column=name_token.column,
                        name=name_token.value
                    ),
                    value=value
                )
            else:
                # 不是赋值，回退并解析表达式
                self.pos = start_pos

        # 解析表达式
        expr = self._parse_expression()

        # 消耗所有连续的句号（如果有）
        while self._check(TokenType.PERIOD):
            self._advance()

        return expr

    def _parse_expression(self) -> ASTNode:
        """解析表达式"""
        return self._parse_or()

    def _parse_or(self) -> ASTNode:
        """解析逻辑或操作"""
        left = self._parse_and()

        while self._check(TokenType.OR):
            op_token = self._advance()
            right = self._parse_and()

            left = BinaryOpNode(
                line=left.line,
                column=left.column,
                left=left,
                operator="or",
                right=right
            )

        return left

    def _parse_and(self) -> ASTNode:
        """解析逻辑与操作"""
        left = self._parse_comparison()

        while self._check(TokenType.AND):
            op_token = self._advance()
            right = self._parse_comparison()

            left = BinaryOpNode(
                line=left.line,
                column=left.column,
                left=left,
                operator="and",
                right=right
            )

        return left

    def _parse_comparison(self) -> ASTNode:
        """解析比较操作"""
        left = self._parse_addition()

        while self._check(TokenType.EQUALS, TokenType.NOT_EQUALS,
                         TokenType.LESS, TokenType.GREATER,
                         TokenType.LESS_EQ, TokenType.GREATER_EQ):
            op_token = self._advance()
            right = self._parse_addition()

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
                right=right
            )

        return left

    def _parse_addition(self) -> ASTNode:
        """解析加减操作"""
        left = self._parse_multiplication()

        while self._check(TokenType.PLUS, TokenType.MINUS):
            op_token = self._advance()
            right = self._parse_multiplication()

            op = "+" if op_token.type == TokenType.PLUS else "-"
            left = BinaryOpNode(
                line=left.line,
                column=left.column,
                left=left,
                operator=op,
                right=right
            )

        return left

    def _parse_multiplication(self) -> ASTNode:
        """解析乘除操作"""
        left = self._parse_unary()

        while self._check(TokenType.MULTIPLY, TokenType.DIVIDE):
            op_token = self._advance()
            right = self._parse_unary()

            op = "*" if op_token.type == TokenType.MULTIPLY else "/"
            left = BinaryOpNode(
                line=left.line,
                column=left.column,
                left=left,
                operator=op,
                right=right
            )

        return left

    def _parse_unary(self) -> ASTNode:
        """解析一元操作（not, -）"""
        if self._check(TokenType.NOT):
            op_token = self._advance()
            operand = self._parse_unary()
            return UnaryOpNode(
                line=op_token.line,
                column=op_token.column,
                operator="not",
                operand=operand
            )

        if self._check(TokenType.MINUS):
            op_token = self._advance()
            operand = self._parse_unary()
            return UnaryOpNode(
                line=op_token.line,
                column=op_token.column,
                operator="-",
                operand=operand
            )

        return self._parse_primary()

    def _parse_primary(self) -> ASTNode:
        """解析基础表达式（数字、字符串、标识符、括号、列表）"""
        token = self._current_token()

        # 数字
        if self._check(TokenType.NUMBER):
            self._advance()
            return NumberNode(
                line=token.line,
                column=token.column,
                value=token.value
            )

        # 字符串
        if self._check(TokenType.STRING):
            self._advance()
            return StringNode(
                line=token.line,
                column=token.column,
                value=token.value
            )

        # 布尔值
        if self._check(TokenType.TRUE):
            self._advance()
            return IdentifierNode(
                line=token.line,
                column=token.column,
                name="真"
            )

        if self._check(TokenType.FALSE):
            self._advance()
            return IdentifierNode(
                line=token.line,
                column=token.column,
                name="假"
            )

        # 列表字面量
        if self._check(TokenType.LBRACKET):
            return self._parse_list()

        # 括号表达式
        if self._check(TokenType.LPAREN):
            self._advance()  # 消费 (
            expr = self._parse_expression()
            self._expect(TokenType.RPAREN, "Expected ')' after expression")
            return expr

        # 标识符或函数调用
        if self._check(TokenType.IDENTIFIER):
            return self._parse_identifier_or_call()

        # 报告错误
        self._report_error(
            f"意外的token: {token.type.name}",
            token,
            suggestion="请检查语法是否正确"
        )
        # 返回一个空的标识符节点以继续解析
        return IdentifierNode(line=token.line, column=token.column, name="")

    def _parse_identifier_or_call(self) -> ASTNode:
        """解析标识符或函数调用"""
        token = self._advance()
        name = token.value

        # 检查是否是函数调用
        if self._check(TokenType.LPAREN, TokenType.PAUSE_MARK):
            args = self._parse_arguments()
            return FunctionCallNode(
                line=token.line,
                column=token.column,
                name=name,
                args=args
            )

        # 否则返回标识符
        return IdentifierNode(
            line=token.line,
            column=token.column,
            name=name
        )

    def _parse_arguments(self) -> List[ASTNode]:
        """解析函数参数"""
        args = []

        # 消费左括号或顿号
        if self._check(TokenType.LPAREN, TokenType.PAUSE_MARK):
            self._advance()

        # 解析参数
        if not self._check(TokenType.RPAREN, TokenType.PERIOD, TokenType.EOF):
            args.append(self._parse_expression())

            while self._check(TokenType.COMMA, TokenType.PAUSE_MARK):
                self._advance()
                args.append(self._parse_expression())

        # 消费右括号
        if self._check(TokenType.RPAREN):
            self._advance()

        return args

    def _parse_list(self) -> ListNode:
        """解析列表字面量"""
        token = self._advance()  # 消费 [
        elements = []

        while not self._check(TokenType.RBRACKET, TokenType.EOF):
            elements.append(self._parse_expression())

            if self._check(TokenType.COMMA, TokenType.PAUSE_MARK):
                self._advance()
            elif not self._check(TokenType.RBRACKET):
                break

        self._expect(TokenType.RBRACKET, "Expected ']' after list elements")

        return ListNode(
            line=token.line,
            column=token.column,
            elements=elements
        )

    def _parse_var_def(self) -> VarDefNode:
        """解析变量定义"""
        var_token = self._advance()  # 消费 '定'

        # 获取变量名
        if not self._check(TokenType.IDENTIFIER):
            self._report_error(
                "期望变量名",
                self._current_token(),
                suggestion="变量定义格式：定 变量名 = 值"
            )
            return VarDefNode(
                line=var_token.line,
                column=var_token.column,
                name="",
                value=None
            )

        name_token = self._advance()
        name = name_token.value

        # 期望 '='
        self._expect(TokenType.ASSIGN, "Expected '=' after variable name")

        # 解析初始值
        value = self._parse_expression()

        # 消耗句号
        while self._check(TokenType.PERIOD):
            self._advance()

        return VarDefNode(
            line=var_token.line,
            column=var_token.column,
            name=name,
            value=value
        )

    def _parse_if(self) -> IfNode:
        """解析条件语句"""
        if_token = self._advance()  # 消费 '若'

        # 解析条件
        condition = self._parse_expression()

        # 期望 '则'
        self._expect(TokenType.THEN, "Expected '则' after condition")

        # 解析then分支
        then_branch = []
        while not self._check(TokenType.ELSE, TokenType.END, TokenType.EOF):
            stmt = self._parse_statement()
            if stmt:
                then_branch.append(stmt)

        # 解析else分支
        else_branch = None
        if self._check(TokenType.ELSE):
            self._advance()
            else_branch = []
            while not self._check(TokenType.END, TokenType.EOF):
                stmt = self._parse_statement()
                if stmt:
                    else_branch.append(stmt)

        return IfNode(
            line=if_token.line,
            column=if_token.column,
            condition=condition,
            then_branch=then_branch,
            else_branch=else_branch
        )

    def _parse_for(self) -> ForNode:
        """解析遍历循环"""
        for_token = self._advance()  # 消费 '遍历'

        # 获取循环变量
        if not self._check(TokenType.IDENTIFIER):
            self._report_error(
                "期望循环变量名",
                self._current_token(),
                suggestion="遍历循环格式：遍历 变量 于 列表：循环体"
            )
            return ForNode(
                line=for_token.line,
                column=for_token.column,
                var="",
                iterable=None,
                body=[]
            )

        var_token = self._advance()
        var = var_token.value

        # 期望 '于'
        self._expect(TokenType.IN, "Expected '于' after loop variable")

        # 解析可迭代对象
        iterable = self._parse_expression()

        # 期望 ':'
        self._expect(TokenType.COLON, "Expected ':' after iterable")

        # 解析循环体
        body = []
        while not self._check(TokenType.END, TokenType.EOF):
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)

        return ForNode(
            line=for_token.line,
            column=for_token.column,
            var=var,
            iterable=iterable,
            body=body
        )

    def _parse_while(self) -> WhileNode:
        """解析当循环"""
        while_token = self._advance()  # 消费 '当'

        # 解析条件
        condition = self._parse_expression()

        # 期望 ':'
        self._expect(TokenType.COLON, "Expected ':' after condition")

        # 解析循环体
        body = []
        while not self._check(TokenType.END, TokenType.EOF):
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)

        return WhileNode(
            line=while_token.line,
            column=while_token.column,
            condition=condition,
            body=body
        )

    def _parse_repeat(self) -> RepeatNode:
        """解析重复循环"""
        repeat_token = self._advance()  # 消费 '重复'

        # 解析次数
        count = self._parse_expression()

        # 期望 '次'
        self._expect(TokenType.TIMES, "Expected '次' after count")

        # 期望 ':'
        self._expect(TokenType.COLON, "Expected ':' after '次'")

        # 解析循环体
        body = []
        while not self._check(TokenType.END, TokenType.EOF):
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)

        return RepeatNode(
            line=repeat_token.line,
            column=repeat_token.column,
            count=count,
            body=body
        )

    def _parse_return(self) -> ReturnNode:
        """解析返回语句"""
        return_token = self._advance()  # 消费 '返回'

        # 解析返回值（可选）
        value = None
        if not self._check(TokenType.PERIOD, TokenType.NEWLINE, TokenType.EOF):
            value = self._parse_expression()

        # 消耗句号
        while self._check(TokenType.PERIOD):
            self._advance()

        return ReturnNode(
            line=return_token.line,
            column=return_token.column,
            value=value
        )
