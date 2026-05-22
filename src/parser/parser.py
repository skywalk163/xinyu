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
from src.parser.ast_nodes import (
    ProgramNode, NumberNode, StringNode, IdentifierNode,
    BinaryOpNode, UnaryOpNode, ListNode, DictNode,
    MemberAccessNode, IndexNode, AssignNode, VarDefNode,
    IfNode, ForNode, WhileNode, RepeatNode,
    FunctionDefNode, FunctionCallNode, ReturnNode,
    BlockNode, ASTNode
)


class ParseError(Exception):
    """解析错误异常类"""
    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        super().__init__(f"Parse Error at line {token.line}, column {token.column}: {message}")


class Parser:
    """语法分析器类
    
    使用递归下降解析方法，支持：
    - 中文关键字和操作符
    - 缩进块（Python风格）
    - 单行和多行语句
    """
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    # ============ 核心方法 ============
    
    def parse(self) -> ProgramNode:
        """主解析方法，返回 ProgramNode"""
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
    
    def _expect(self, token_type: TokenType, message: str) -> Token:
        """期望特定token类型"""
        if self._check(token_type):
            return self._advance()
        raise ParseError(message, self._current_token())
    
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
        
        # 表达式语句（包括赋值）
        return self._parse_expression_statement()
    
    def _parse_expression_statement(self) -> ASTNode:
        """解析表达式语句（包括赋值）"""
        expr = self._parse_expression()
        
        # 检查是否为赋值
        if self._check(TokenType.ASSIGN):
            self._advance()  # 消费 =
            value = self._parse_expression()
            
            # 左侧必须是标识符
            if isinstance(expr, IdentifierNode):
                return AssignNode(
                    line=expr.line,
                    column=expr.column,
                    target=expr,
                    value=value
                )
            else:
                raise ParseError("Invalid assignment target", self._current_token())
        
        return expr
    
    # ============ 表达式解析（优先级从低到高） ============
    
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
        """解析比较操作（==, !=, <, >, <=, >=）"""
        left = self._parse_addition()
        
        while self._check(TokenType.EQUALS, TokenType.NOT_EQUALS,
                         TokenType.LESS, TokenType.GREATER,
                         TokenType.LESS_EQ, TokenType.GREATER_EQ):
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
                right=right
            )
        
        return left
    
    def _parse_addition(self) -> ASTNode:
        """解析加减操作（+, -）"""
        left = self._parse_multiplication()
        
        while self._check(TokenType.PLUS, TokenType.MINUS):
            op_token = self._advance()
            right = self._parse_multiplication()
            
            op_map = {
                TokenType.PLUS: "+",
                TokenType.MINUS: "-",
            }
            
            left = BinaryOpNode(
                line=left.line,
                column=left.column,
                left=left,
                operator=op_map[op_token.type],
                right=right
            )
        
        return left
    
    def _parse_multiplication(self) -> ASTNode:
        """解析乘除操作（*, /）"""
        left = self._parse_unary()
        
        while self._check(TokenType.MULTIPLY, TokenType.DIVIDE):
            op_token = self._advance()
            right = self._parse_unary()
            
            op_map = {
                TokenType.MULTIPLY: "*",
                TokenType.DIVIDE: "/",
            }
            
            left = BinaryOpNode(
                line=left.line,
                column=left.column,
                left=left,
                operator=op_map[op_token.type],
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
        """解析基础表达式（数字、字符串、标识符、括号）"""
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
        
        # 括号表达式
        if self._check(TokenType.LPAREN):
            self._advance()  # 消费 (
            expr = self._parse_expression()
            self._expect(TokenType.RPAREN, "Expected ')' after expression")
            return expr
        
        # 标识符或函数调用
        if self._check(TokenType.IDENTIFIER):
            return self._parse_identifier_or_call()
        
        raise ParseError(f"Unexpected token: {token.type.name}", token)
    
    def _parse_identifier_or_call(self) -> ASTNode:
        """解析标识符或函数调用"""
        token = self._advance()
        name = token.value
        
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
            
            return FunctionCallNode(
                line=token.line,
                column=token.column,
                name=name,
                args=args
            )
        
        # 检查是否为无括号函数调用（后面跟着参数）
        args = []
        while not self._check(TokenType.NEWLINE, TokenType.EOF, TokenType.PERIOD,
                             TokenType.THEN, TokenType.ELSE, TokenType.ELIF,
                             TokenType.RPAREN, TokenType.RBRACKET, TokenType.RBRACE,
                             TokenType.COMMA, TokenType.COLON):
            # 检查是否是操作符或关键字
            if self._check(TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE,
                          TokenType.EQUALS, TokenType.NOT_EQUALS, TokenType.LESS, TokenType.GREATER,
                          TokenType.LESS_EQ, TokenType.GREATER_EQ, TokenType.AND, TokenType.OR, TokenType.NOT,
                          TokenType.ASSIGN):
                break
            
            # 尝试解析参数
            try:
                arg = self._parse_primary()
                args.append(arg)
            except ParseError:
                break
        
        if args:
            return FunctionCallNode(
                line=token.line,
                column=token.column,
                name=name,
                args=args
            )
        
        return IdentifierNode(
            line=token.line,
            column=token.column,
            name=name
        )
    
    # ============ 控制流解析 ============
    
    def _parse_if(self) -> IfNode:
        """解析条件语句（若 ... 则 ... 否则 ...）"""
        token = self._advance()  # 消费 若
        
        # 解析条件
        condition = self._parse_expression()
        
        # 期望 则
        self._expect(TokenType.THEN, "Expected '则' after condition")
        
        # 解析 then 分支
        then_branch = self._parse_block()
        
        # 检查是否有 else 分支
        else_branch = None
        if self._check(TokenType.ELSE):
            self._advance()  # 消费 否则
            else_branch = self._parse_block()
        
        # 消费结尾的 。
        if self._check(TokenType.PERIOD):
            self._advance()
        
        return IfNode(
            line=token.line,
            column=token.column,
            condition=condition,
            then_branch=then_branch,
            else_branch=else_branch
        )
    
    def _parse_for(self) -> ForNode:
        """解析遍历循环（遍历 x 于 列表：...）"""
        token = self._advance()  # 消费 遍历
        
        # 解析循环变量
        var_token = self._expect(TokenType.IDENTIFIER, "Expected variable name after '遍历'")
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
        
        return ForNode(
            line=token.line,
            column=token.column,
            var=var,
            iterable=iterable,
            body=body
        )
    
    def _parse_while(self) -> WhileNode:
        """解析当循环（当 条件：...）"""
        token = self._advance()  # 消费 当
        
        # 解析条件
        condition = self._parse_expression()
        
        # 期望 ：
        self._expect(TokenType.COLON, "Expected '：' after condition")
        
        # 解析循环体
        body = self._parse_block()
        
        # 消费结尾的 。
        if self._check(TokenType.PERIOD):
            self._advance()
        
        return WhileNode(
            line=token.line,
            column=token.column,
            condition=condition,
            body=body
        )
    
    def _parse_repeat(self) -> RepeatNode:
        """解析重复语句（重复 N 次：...）"""
        token = self._advance()  # 消费 重复
        
        # 解析重复次数
        count = self._parse_expression()
        
        # 期望 次
        self._expect(TokenType.TIMES, "Expected '次' after count")
        
        # 期望 ：
        self._expect(TokenType.COLON, "Expected '：' after '次'")
        
        # 解析循环体
        body = self._parse_block()
        
        # 消费结尾的 。
        if self._check(TokenType.PERIOD):
            self._advance()
        
        return RepeatNode(
            line=token.line,
            column=token.column,
            count=count,
            body=body
        )
    
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
            return VarDefNode(
                line=token.line,
                column=token.column,
                name=name,
                value=func_def
            )
        
        # 解析值
        value = self._parse_expression()
        
        return VarDefNode(
            line=token.line,
            column=token.column,
            name=name,
            value=value
        )
    
    def _parse_function_def(self, name: str, line: int, column: int) -> FunctionDefNode:
        """解析函数定义"""
        self._advance()  # 消费 函
        
        # 解析参数列表
        params = []
        while not self._check(TokenType.COLON, TokenType.NEWLINE, TokenType.EOF):
            if self._check(TokenType.IDENTIFIER):
                param_token = self._advance()
                params.append(param_token.value)
            else:
                break
        
        # 期望 ：
        self._expect(TokenType.COLON, "Expected '：' after function parameters")
        
        # 解析函数体
        body = self._parse_block()
        
        # 消费结尾的 。
        if self._check(TokenType.PERIOD):
            self._advance()
        
        return FunctionDefNode(
            line=line,
            column=column,
            name=name,
            params=params,
            body=body
        )
    
    def _parse_return(self) -> ReturnNode:
        """解析返回语句"""
        token = self._advance()  # 消费 返回
        
        # 检查是否有返回值
        value = None
        if not self._check(TokenType.NEWLINE, TokenType.EOF, TokenType.PERIOD):
            value = self._parse_expression()
        
        return ReturnNode(
            line=token.line,
            column=token.column,
            value=value
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
