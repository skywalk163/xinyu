# -*- coding: utf-8 -*-
"""语义分析器

分析AST，进行语义检查：
- 变量定义和使用检查
- 函数定义和调用检查
- 作用域管理
- 类型推断
"""

from typing import List, Optional
from src.parser.ast_nodes import (
    ProgramNode, NumberNode, StringNode, IdentifierNode,
    BinaryOpNode, UnaryOpNode, ListNode, DictNode,
    MemberAccessNode, IndexNode, AssignNode, VarDefNode,
    IfNode, ForNode, WhileNode, RepeatNode,
    FunctionDefNode, FunctionCallNode, ReturnNode,
    BlockNode, ASTNode
)
from src.semantic.scope import Scope


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


class SemanticAnalyzer:
    """语义分析器类

    使用访问者模式遍历AST，进行语义分析。

    属性：
        global_scope: 全局作用域
        current_scope: 当前作用域
        errors: 错误列表
    """

    # 内置函数
    BUILTIN_FUNCTIONS = {
        "打印": {"params": -1},  # 可变参数
        "输入": {"params": 0},
        "输出": {"params": -1},  # 可变参数
        "读取": {"params": 0},
        "写入": {"params": -1},  # 可变参数
    }

    # 内置模块
    BUILTIN_MODULES = {
        "math", "random", "json", "re", "datetime", "date", "time", "timedelta"
    }

    def __init__(self):
        """初始化语义分析器"""
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.errors: List[SemanticError] = []

        # 注册内置函数
        for name, info in self.BUILTIN_FUNCTIONS.items():
            self.global_scope.define(
                name,
                "function",
                value_type="function",
                params=info["params"],
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
        """
        检查语义分析过程中是否检测到错误

        Returns:
            bool: True表示存在错误，False表示无错误
        """
        return len(self.errors) > 0

    def error_count(self) -> int:
        """
        返回错误数量

        Returns:
            int: 错误数量
        """
        return len(self.errors)

    def get_errors(self) -> List[SemanticError]:
        """
        返回所有错误列表

        Returns:
            List[SemanticError]: 错误列表
        """
        return self.errors

    def analyze(self, ast: ProgramNode) -> bool:
        """分析AST

        Args:
            ast: 程序AST

        Returns:
            是否分析成功（无错误）
        """
        self._visit_program(ast)
        return len(self.errors) == 0

    # ============ 访问方法 ============

    def _visit_program(self, node: ProgramNode) -> None:
        """访问程序节点"""
        for stmt in node.statements:
            self._visit_statement(stmt)

    def _visit_statement(self, node: ASTNode) -> None:
        """访问语句节点"""
        if isinstance(node, VarDefNode):
            self._visit_var_def(node)
        elif isinstance(node, AssignNode):
            self._visit_assign(node)
        elif isinstance(node, IfNode):
            self._visit_if(node)
        elif isinstance(node, ForNode):
            self._visit_for(node)
        elif isinstance(node, WhileNode):
            self._visit_while(node)
        elif isinstance(node, RepeatNode):
            self._visit_repeat(node)
        elif isinstance(node, ReturnNode):
            self._visit_return(node)
        elif isinstance(node, FunctionCallNode):
            self._visit_function_call(node)
        elif isinstance(node, IdentifierNode):
            # 单独的标识符（可能是未使用的变量）
            self._visit_identifier(node)
        elif isinstance(node, BinaryOpNode):
            # 表达式语句
            self._visit_expression(node)
        else:
            # 其他表达式
            self._visit_expression(node)

    def _visit_var_def(self, node: VarDefNode) -> None:
        """访问变量定义节点"""
        # 检查重复定义
        if self.current_scope.lookup_local(node.name):
            self.errors.append(SemanticError(
                f"重复定义：'{node.name}' 已在此作用域中定义",
                node.line,
                node.column
            ))
            return

        # 推断类型
        value_type = "unknown"
        if node.value:
            if isinstance(node.value, FunctionDefNode):
                # 函数定义
                value_type = "function"
                self.current_scope.define(
                    node.name,
                    "function",
                    value_type="function",
                    params=node.value.params,
                    is_builtin=False
                )
                # 分析函数体
                self._visit_function_def(node.value)
                return
            else:
                value_type = self._visit_expression(node.value)

        # 定义变量
        self.current_scope.define(
            node.name,
            "variable",
            value_type=value_type
        )

    def _visit_function_def(self, node: FunctionDefNode) -> None:
        """访问函数定义节点"""
        # 创建函数作用域
        function_scope = Scope(parent=self.current_scope)
        self.current_scope = function_scope

        # 定义参数
        for param in node.params:
            self.current_scope.define(
                param,
                "parameter",
                value_type="unknown"
            )

        # 分析函数体
        for stmt in node.body:
            self._visit_statement(stmt)

        # 恢复作用域
        self.current_scope = self.current_scope.parent

    def _visit_assign(self, node: AssignNode) -> None:
        """访问赋值节点"""
        # 推断右侧类型
        value_type = self._visit_expression(node.value)

        # 检查左侧
        if isinstance(node.target, IdentifierNode):
            name = node.target.name

            # 查找变量
            symbol = self.current_scope.lookup(name)

            if symbol:
                # 更新类型
                self.current_scope.assign(name, value_type)
            else:
                # 语境驱动式：自动创建变量
                self.current_scope.define(
                    name,
                    "variable",
                    value_type=value_type
                )
        else:
            # 成员访问或索引赋值
            self._visit_expression(node.target)

    def _visit_if(self, node: IfNode) -> None:
        """访问条件节点"""
        # 分析条件
        self._visit_expression(node.condition)

        # 分析 then 分支
        for stmt in node.then_branch:
            self._visit_statement(stmt)

        # 分析 else 分支
        if node.else_branch:
            for stmt in node.else_branch:
                self._visit_statement(stmt)

    def _visit_for(self, node: ForNode) -> None:
        """访问遍历循环节点"""
        # 分析可迭代对象
        self._visit_expression(node.iterable)

        # 创建循环作用域
        loop_scope = Scope(parent=self.current_scope)
        self.current_scope = loop_scope

        # 定义循环变量
        self.current_scope.define(
            node.var,
            "variable",
            value_type="unknown"
        )

        # 分析循环体
        for stmt in node.body:
            self._visit_statement(stmt)

        # 恢复作用域
        self.current_scope = self.current_scope.parent

    def _visit_while(self, node: WhileNode) -> None:
        """访问当循环节点"""
        # 分析条件
        self._visit_expression(node.condition)

        # 创建循环作用域
        loop_scope = Scope(parent=self.current_scope)
        self.current_scope = loop_scope

        # 分析循环体
        for stmt in node.body:
            self._visit_statement(stmt)

        # 恢复作用域
        self.current_scope = self.current_scope.parent

    def _visit_repeat(self, node: RepeatNode) -> None:
        """访问重复节点"""
        # 分析重复次数
        self._visit_expression(node.count)

        # 创建循环作用域
        loop_scope = Scope(parent=self.current_scope)
        self.current_scope = loop_scope

        # 分析循环体
        for stmt in node.body:
            self._visit_statement(stmt)

        # 恢复作用域
        self.current_scope = self.current_scope.parent

    def _visit_return(self, node: ReturnNode) -> None:
        """访问返回节点"""
        if node.value:
            self._visit_expression(node.value)

    def _visit_expression(self, node: ASTNode) -> str:
        """访问表达式节点，返回类型"""
        if isinstance(node, NumberNode):
            return "number"

        if isinstance(node, StringNode):
            return "string"

        if isinstance(node, IdentifierNode):
            return self._visit_identifier(node)

        if isinstance(node, BinaryOpNode):
            return self._visit_binary_op(node)

        if isinstance(node, UnaryOpNode):
            return self._visit_unary_op(node)

        if isinstance(node, ListNode):
            return self._visit_list(node)

        if isinstance(node, DictNode):
            return self._visit_dict(node)

        if isinstance(node, MemberAccessNode):
            return self._visit_member_access(node)

        if isinstance(node, IndexNode):
            return self._visit_index(node)

        if isinstance(node, FunctionCallNode):
            return self._visit_function_call(node)

        return "unknown"

    def _visit_identifier(self, node: IdentifierNode) -> str:
        """访问标识符节点"""
        # 特殊标识符：真、假
        if node.name in ("真", "假"):
            return "boolean"

        # 查找符号
        symbol = self.current_scope.lookup(node.name)

        if not symbol:
            self.errors.append(SemanticError(
                f"未定义的变量：'{node.name}'",
                node.line,
                node.column
            ))
            return "unknown"

        return symbol.get("value_type", "unknown")

    def _visit_binary_op(self, node: BinaryOpNode) -> str:
        """访问二元操作节点"""
        left_type = self._visit_expression(node.left)
        right_type = self._visit_expression(node.right)

        return self._infer_binary_op_type(left_type, right_type, node.operator)

    def _visit_unary_op(self, node: UnaryOpNode) -> str:
        """访问一元操作节点"""
        operand_type = self._visit_expression(node.operand)

        if node.operator == "not":
            return "boolean"

        if node.operator == "-":
            if operand_type == "number":
                return "number"
            return "unknown"

        return "unknown"

    def _visit_list(self, node: ListNode) -> str:
        """访问列表节点"""
        # 分析元素类型
        for elem in node.elements:
            self._visit_expression(elem)

        return "list"

    def _visit_dict(self, node: DictNode) -> str:
        """访问字典节点"""
        # 分析键值对
        for key, value in node.pairs:
            self._visit_expression(key)
            self._visit_expression(value)

        return "dict"

    def _visit_member_access(self, node: MemberAccessNode) -> str:
        """访问成员访问节点"""
        obj_type = self._visit_expression(node.obj)

        # 如果是内置模块的成员访问，不报错
        if isinstance(node.obj, IdentifierNode):
            if node.obj.name in self.BUILTIN_MODULES:
                return "unknown"

        # TODO: 根据对象类型推断成员类型
        return "unknown"

    def _visit_index(self, node: IndexNode) -> str:
        """访问索引节点"""
        obj_type = self._visit_expression(node.obj)
        index_type = self._visit_expression(node.index)

        if obj_type == "list":
            return "unknown"  # 列表元素类型未知
        elif obj_type == "dict":
            return "unknown"  # 字典值类型未知

        return "unknown"

    def _visit_function_call(self, node: FunctionCallNode) -> str:
        """访问函数调用节点"""
        # 查找函数
        symbol = self.current_scope.lookup(node.name)

        if not symbol:
            self.errors.append(SemanticError(
                f"未定义的函数：'{node.name}'",
                node.line,
                node.column
            ))
            return "unknown"

        if symbol["type"] != "function":
            self.errors.append(SemanticError(
                f"'{node.name}' 不是函数",
                node.line,
                node.column
            ))
            return "unknown"

        # 检查参数数量
        # params 可能是列表（用户定义函数）或整数（内置函数，-1 表示可变参数）
        params_info = symbol.get("params", [])
        if isinstance(params_info, list):
            # 用户定义函数
            expected_params = len(params_info)
            actual_params = len(node.args)
            if actual_params != expected_params:
                self.errors.append(SemanticError(
                    f"函数 '{node.name}' 期望 {expected_params} 个参数，但提供了 {actual_params} 个",
                    node.line,
                    node.column
                ))
        elif isinstance(params_info, int):
            # 内置函数
            expected_params = params_info
            if expected_params >= 0:
                actual_params = len(node.args)
                if actual_params != expected_params:
                    self.errors.append(SemanticError(
                        f"函数 '{node.name}' 期望 {expected_params} 个参数，但提供了 {actual_params} 个",
                        node.line,
                        node.column
                    ))

        # 分析参数
        for arg in node.args:
            self._visit_expression(arg)

        return "unknown"  # 函数返回类型未知

    def _infer_binary_op_type(self, left_type: str, right_type: str, operator: str) -> str:
        """推断二元操作类型

        Args:
            left_type: 左操作数类型
            right_type: 右操作数类型
            operator: 操作符

        Returns:
            结果类型
        """
        # 比较操作符
        if operator in ("==", "!=", "<", ">", "<=", ">="):
            return "boolean"

        # 逻辑操作符
        if operator in ("and", "or"):
            return "boolean"

        # 算术操作符
        if operator in ("+", "-", "*", "/"):
            if left_type == "number" and right_type == "number":
                return "number"
            if left_type == "string" and right_type == "string" and operator == "+":
                return "string"
            return "unknown"

        return "unknown"
