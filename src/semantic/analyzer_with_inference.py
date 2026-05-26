# -*- coding: utf-8 -*-
"""语义分析器（集成类型推断）

这是语义分析器的增强版本，集成了类型推断功能。
保持与原 SemanticAnalyzer 类的向后兼容性。
"""

from typing import List, Optional, Dict
from src.parser.ast_nodes import (
    ProgramNode, NumberNode, StringNode, IdentifierNode,
    BinaryOpNode, UnaryOpNode, ListNode, DictNode,
    MemberAccessNode, IndexNode, AssignNode, VarDefNode,
    IfNode, ForNode, WhileNode, RepeatNode,
    FunctionDefNode, FunctionCallNode, ReturnNode,
    BlockNode, ASTNode
)
from src.semantic.scope import Scope
from src.semantic.type_inference import TypeInferencer
from src.error_handling import ErrorHandler, ErrorType


class SemanticError(Exception):
    """语义错误异常类"""

    def __init__(self, message: str, line: int, column: int, suggestion: str = None):
        self.message = message
        self.line = line
        self.column = column
        self.suggestion = suggestion
        
        # 构建详细的错误信息
        error_msg = f"语义错误: {message} (行 {line}, 列 {column})"
        if suggestion:
            error_msg += f"\n  💡 建议: {suggestion}"
        
        super().__init__(error_msg)


class SemanticAnalyzerWithInference:
    """语义分析器（集成类型推断）
    
    这是 SemanticAnalyzer 的增强版本，集成了类型推断功能，
    可以在语义分析过程中推断变量和表达式的类型。
    
    Attributes:
        global_scope: 全局作用域
        current_scope: 当前作用域
        error_handler: 错误处理器
        type_inferencer: 类型推断器
    
    Example:
        >>> from src.lexer.lexer import Lexer
        >>> from src.parser.parser import Parser
        >>> from src.error_handling import ErrorHandler
        >>> error_handler = ErrorHandler()
        >>> lexer = Lexer("定 x 为 42")
        >>> tokens = lexer.tokenize()
        >>> parser = Parser(tokens)
        >>> ast = parser.parse()
        >>> analyzer = SemanticAnalyzerWithInference(error_handler)
        >>> analyzer.analyze(ast)
        >>> not error_handler.has_errors()
        True
    """

    # 内置函数
    BUILTIN_FUNCTIONS = {
        "印": {"params": -1, "return_type": "void"},
        "读取": {"params": 0, "return_type": "string"},
        "写入": {"params": -1, "return_type": "void"},
    }

    # 内置模块
    BUILTIN_MODULES = {
        "math", "random", "json", "re", "datetime", "date", "time", "timedelta"
    }

    def __init__(self, error_handler: Optional[ErrorHandler] = None):
        """初始化语义分析器
        
        Args:
            error_handler: 错误处理器（可选，默认创建新实例）
        """
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.error_handler = error_handler or ErrorHandler()
        self.type_inferencer = TypeInferencer()

        # 注册内置函数
        for name, info in self.BUILTIN_FUNCTIONS.items():
            self.global_scope.define(
                name,
                "function",
                value_type="function",
                params=info["params"],
                return_type=info.get("return_type", "unknown"),
                is_builtin=True
            )

        # 注册内置模块
        for module_name in self.BUILTIN_MODULES:
            self.global_scope.define(
                module_name,
                "module",
                value_type="module",
                is_builtin=True
            )

    def has_errors(self) -> bool:
        """检查是否有错误
        
        Returns:
            bool: True表示存在错误，False表示无错误
        """
        return self.error_handler.has_errors()

    def error_count(self) -> int:
        """返回错误数量
        
        Returns:
            int: 错误数量
        """
        return len(self.error_handler.get_errors())

    def get_errors(self) -> List:
        """返回所有错误列表
        
        Returns:
            List: 错误列表
        """
        return self.error_handler.get_errors()

    def _report_error(
        self,
        message: str,
        line: int,
        column: int,
        suggestion: Optional[str] = None
    ) -> None:
        """报告错误
        
        Args:
            message: 错误消息
            line: 行号
            column: 列号
            suggestion: 修复建议（可选）
        """
        self.error_handler.report(
            ErrorType.SEMANTIC_ERROR,
            message,
            line,
            column,
            suggestion=suggestion
        )

    def _build_type_context(self) -> Dict[str, str]:
        """构建类型上下文
        
        收集当前作用域中所有变量的类型信息，
        用于类型推断。
        
        Returns:
            Dict[str, str]: 变量名到类型的映射
        """
        context = {}
        scope = self.current_scope
        for name, symbol in scope.symbols.items():
            if symbol.get('value_type'):
                context[name] = symbol['value_type']
        return context

    def _infer_type(self, node: ASTNode, context: Optional[Dict[str, str]] = None) -> str:
        """推断AST节点的类型
        
        使用类型推断器推断给定节点的类型。
        
        Args:
            node: AST节点
            context: 类型上下文（变量名到类型的映射）
        
        Returns:
            str: 推断的类型字符串（如 'number', 'string', 'boolean'）
        """
        return self.type_inferencer.infer(node, context)

    def analyze(self, ast: ProgramNode) -> bool:
        """分析抽象语法树
        
        对AST进行语义分析，包括符号表构建、类型检查、作用域检查等。
        
        Args:
            ast: 程序根节点
        
        Returns:
            bool: 分析是否成功（无错误）
        """
        for stmt in ast.statements:
            self._visit(stmt)
        
        return not self.has_errors()

    def _visit(self, node: ASTNode) -> Optional[str]:
        """访问AST节点
        
        根据节点类型调用相应的访问方法。
        
        Args:
            node: AST节点
        
        Returns:
            Optional[str]: 节点的类型（如果可推断）
        """
        if isinstance(node, VarDefNode):
            return self._visit_var_def(node)
        elif isinstance(node, AssignNode):
            return self._visit_assign(node)
        elif isinstance(node, IfNode):
            return self._visit_if(node)
        elif isinstance(node, ForNode):
            return self._visit_for(node)
        elif isinstance(node, WhileNode):
            return self._visit_while(node)
        elif isinstance(node, RepeatNode):
            return self._visit_repeat(node)
        elif isinstance(node, FunctionDefNode):
            return self._visit_function_def(node)
        elif isinstance(node, FunctionCallNode):
            return self._visit_function_call(node)
        elif isinstance(node, ReturnNode):
            return self._visit_return(node)
        elif isinstance(node, BinaryOpNode):
            return self._visit_binary_op(node)
        elif isinstance(node, UnaryOpNode):
            return self._visit_unary_op(node)
        elif isinstance(node, IdentifierNode):
            return self._visit_identifier(node)
        elif isinstance(node, NumberNode):
            return "number"
        elif isinstance(node, StringNode):
            return "string"
        elif isinstance(node, ListNode):
            return "list"
        elif isinstance(node, DictNode):
            return "dict"
        else:
            return None

    def _visit_var_def(self, node: VarDefNode) -> str:
        """访问变量定义节点
        
        分析变量定义，推断变量类型，并添加到符号表。
        
        Args:
            node: 变量定义节点
        
        Returns:
            str: 变量的类型
        """
        # 检查变量是否已定义
        if self.current_scope.has(node.name):
            symbol = self.current_scope.lookup(node.name)
            self._report_error(
                f"变量 '{node.name}' 已定义",
                node.line,
                node.column,
                suggestion=f"请使用不同的变量名，或删除重复的定义"
            )
            return "unknown"
        
        # 推断变量类型
        inferred_type = "unknown"
        if node.value:
            # 构建类型上下文
            context = self._build_type_context()
            # 推断初始值的类型
            inferred_type = self._infer_type(node.value, context)
            # 访问初始值表达式
            self._visit(node.value)
        
        # 添加到符号表
        self.current_scope.define(
            node.name,
            "variable",
            value_type=inferred_type,
            line=node.line,
            column=node.column
        )
        
        return inferred_type

    def _visit_assign(self, node: AssignNode) -> str:
        """访问赋值节点
        
        分析赋值语句，检查变量是否已定义，推断赋值类型。
        
        Args:
            node: 赋值节点
        
        Returns:
            str: 赋值的类型
        """
        # 检查变量是否已定义
        if not self.current_scope.has(node.target.name):
            self._report_error(
                f"变量 '{node.target.name}' 未定义",
                node.line,
                node.column,
                suggestion=f"请先定义变量 '定 {node.target.name} 为 ...'"
            )
            return "unknown"
        
        # 推断赋值类型
        context = self._build_type_context()
        inferred_type = self._infer_type(node.value, context)
        
        # 访问赋值表达式
        self._visit(node.value)
        
        # 更新符号表中的类型信息
        symbol = self.current_scope.lookup(node.target.name)
        if symbol and symbol.get('value_type') == 'unknown':
            symbol['value_type'] = inferred_type
        
        return inferred_type

    def _visit_identifier(self, node: IdentifierNode) -> str:
        """访问标识符节点
        
        检查标识符是否已定义，返回其类型。
        
        Args:
            node: 标识符节点
        
        Returns:
            str: 标识符的类型
        """
        if not self.current_scope.has(node.name):
            self._report_error(
                f"变量 '{node.name}' 未定义",
                node.line,
                node.column,
                suggestion=f"请先定义变量 '定 {node.name} 为 ...'"
            )
            return "unknown"
        
        symbol = self.current_scope.lookup(node.name)
        return symbol.get('value_type', 'unknown') if symbol else "unknown"

    def _visit_binary_op(self, node: BinaryOpNode) -> str:
        """访问二元运算节点
        
        分析二元运算，推断结果类型。
        
        Args:
            node: 二元运算节点
        
        Returns:
            str: 运算结果的类型
        """
        left_type = self._visit(node.left)
        right_type = self._visit(node.right)
        
        # 使用类型推断器推断结果类型
        context = self._build_type_context()
        result_type = self._infer_type(node, context)
        
        return result_type

    def _visit_unary_op(self, node: UnaryOpNode) -> str:
        """访问一元运算节点
        
        分析一元运算，推断结果类型。
        
        Args:
            node: 一元运算节点
        
        Returns:
            str: 运算结果的类型
        """
        operand_type = self._visit(node.operand)
        
        # 根据操作符推断结果类型
        if node.operator in ("not", "非"):
            return "boolean"
        elif node.operator in ("-", "负"):
            return "number"
        
        return operand_type

    def _visit_function_call(self, node: FunctionCallNode) -> str:
        """访问函数调用节点
        
        分析函数调用，检查参数，推断返回类型。
        
        Args:
            node: 函数调用节点
        
        Returns:
            str: 函数返回值的类型
        """
        # 检查函数是否已定义
        if not self.current_scope.has(node.name):
            # 可能是内置函数
            if node.name not in self.BUILTIN_FUNCTIONS:
                self._report_error(
                    f"函数 '{node.name}' 未定义",
                    node.line,
                    node.column,
                    suggestion=f"请先定义函数 '函 {node.name}(...) ...'"
                )
                return "unknown"
        
        # 访问参数
        arg_types = []
        for arg in node.args:
            arg_type = self._visit(arg)
            arg_types.append(arg_type)
        
        # 推断返回类型
        symbol = self.current_scope.lookup(node.name)
        if symbol and symbol.get('return_type'):
            return symbol['return_type']
        
        # 使用类型推断器推断返回类型
        return self.type_inferencer.infer_call_return(node.name, arg_types)

    def _visit_if(self, node: IfNode) -> str:
        """访问条件语句节点"""
        self._visit(node.condition)
        
        # 进入then分支
        for stmt in node.then_branch:
            self._visit(stmt)
        
        # 进入else分支
        if node.else_branch:
            for stmt in node.else_branch:
                self._visit(stmt)
        
        return "void"

    def _visit_for(self, node: ForNode) -> str:
        """访问遍历循环节点"""
        self._visit(node.iterable)
        
        # 定义循环变量
        self.current_scope.define(
            node.var,
            "variable",
            value_type="unknown",
            line=node.line,
            column=node.column
        )
        
        # 访问循环体
        for stmt in node.body:
            self._visit(stmt)
        
        return "void"

    def _visit_while(self, node: WhileNode) -> str:
        """访问当循环节点"""
        self._visit(node.condition)
        
        for stmt in node.body:
            self._visit(stmt)
        
        return "void"

    def _visit_repeat(self, node: RepeatNode) -> str:
        """访问重复循环节点"""
        self._visit(node.count)
        
        for stmt in node.body:
            self._visit(stmt)
        
        return "void"

    def _visit_function_def(self, node: FunctionDefNode) -> str:
        """访问函数定义节点"""
        # 检查函数是否已定义
        if self.current_scope.has(node.name):
            self._report_error(
                f"函数 '{node.name}' 已定义",
                node.line,
                node.column,
                suggestion="请使用不同的函数名"
            )
            return "unknown"
        
        # 添加函数到符号表
        self.current_scope.define(
            node.name,
            "function",
            value_type="function",
            params=len(node.params),
            line=node.line,
            column=node.column
        )
        
        # 创建新的作用域
        old_scope = self.current_scope
        self.current_scope = Scope(parent=self.current_scope)
        
        # 添加参数到新作用域
        for param in node.params:
            self.current_scope.define(
                param,
                "parameter",
                value_type="unknown"
            )
        
        # 访问函数体
        for stmt in node.body:
            self._visit(stmt)
        
        # 恢复作用域
        self.current_scope = old_scope
        
        return "function"

    def _visit_return(self, node: ReturnNode) -> str:
        """访问返回语句节点"""
        if node.value:
            return self._visit(node.value)
        return "void"
