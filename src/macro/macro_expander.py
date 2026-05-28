"""
宏展开器

负责在AST中查找宏调用并展开它们。
"""

from typing import List, Optional
from src.macro.macro_system import MacroSystem
from src.parser.ast_nodes import (
    ASTNode, ProgramNode, FunctionCallNode, IfNode, ForNode,
    WhileNode, RepeatNode, IdentifierNode
)


class MacroExpander:
    """宏展开器"""

    def __init__(self, macro_system: MacroSystem):
        self.macro_system = macro_system
        self.max_depth = 100  # 防止无限递归
        self.current_depth = 0

    def expand_ast(self, node: ASTNode) -> ASTNode:
        """
        展开AST中的宏调用

        Args:
            node: AST节点

        Returns:
            展开后的AST节点
        """
        if self.current_depth >= self.max_depth:
            raise RecursionError("宏展开深度超过限制")

        self.current_depth += 1
        try:
            # 处理列表（宏展开可能返回多个语句）
            if isinstance(node, list):
                expanded_items = []
                for item in node:
                    expanded = self.expand_ast(item)
                    if isinstance(expanded, list):
                        expanded_items.extend(expanded)
                    else:
                        expanded_items.append(expanded)
                return expanded_items

            if isinstance(node, ProgramNode):
                expanded_statements = []
                for stmt in node.statements:
                    expanded = self.expand_ast(stmt)
                    if isinstance(expanded, list):
                        expanded_statements.extend(expanded)
                    else:
                        expanded_statements.append(expanded)
                return ProgramNode(line=node.line, column=node.column, statements=expanded_statements)

            elif isinstance(node, FunctionCallNode):
                # 检查是否是宏调用
                if self.macro_system.has(node.name):
                    expanded = self._expand_macro_call(node)
                    # 如果展开结果是列表，需要继续展开列表中的每个元素
                    if isinstance(expanded, list):
                        return self.expand_ast(expanded)
                    else:
                        return expanded
                else:
                    # 递归展开参数
                    expanded_args = [self.expand_ast(arg) for arg in node.args]
                    return FunctionCallNode(name=node.name, args=expanded_args, line=node.line, column=node.column)

            elif isinstance(node, IfNode):
                expanded_condition = self.expand_ast(node.condition)
                expanded_then = [self.expand_ast(stmt) for stmt in node.then_branch]
                expanded_else = [self.expand_ast(stmt) for stmt in node.else_branch] if node.else_branch else None
                return IfNode(condition=expanded_condition, then_branch=expanded_then, else_branch=expanded_else, line=node.line, column=node.column)

            elif isinstance(node, ForNode):
                # 遍历循环可能是宏调用
                if self.macro_system.has("遍历"):
                    return self._expand_for_loop(node)
                return node

            elif isinstance(node, WhileNode):
                expanded_condition = self.expand_ast(node.condition)
                expanded_body = [self.expand_ast(stmt) for stmt in node.body]
                return WhileNode(condition=expanded_condition, body=expanded_body, line=node.line, column=node.column)

            elif isinstance(node, RepeatNode):
                # 重复循环是宏调用
                if self.macro_system.has("重复"):
                    return self._expand_repeat_loop(node)
                return node

            else:
                # 其他节点类型直接返回
                return node
        finally:
            self.current_depth -= 1

    def _expand_macro_call(self, node: FunctionCallNode) -> ASTNode:
        """
        展开宏调用

        Args:
            node: 函数调用节点

        Returns:
            展开后的AST节点
        """
        macro = self.macro_system.get(node.name)
        if not macro:
            return node

        # 构建参数映射
        args = {}
        for i, param in enumerate(macro.params):
            if i < len(node.args):
                args[param] = node.args[i]

        # 展开宏体
        expanded_code = self.macro_system.expand(node.name, args)

        # 解析展开后的代码
        from src.lexer.lexer import Lexer
        from src.parser.parser import Parser

        lexer = Lexer(expanded_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        expanded_ast = parser.parse()

        # 递归展开AST中可能存在的宏调用
        # 注意：这里不调用expand_ast，因为会在外层的expand_ast中处理
        # 只需要返回展开后的AST，让外层的expand_ast继续处理
        
        # 返回展开后的语句列表或单个语句
        if len(expanded_ast.statements) > 1:
            # 多个语句，返回列表，让外层的expand_ast处理
            return expanded_ast.statements
        elif len(expanded_ast.statements) == 1:
            # 单个语句，直接返回，让外层的expand_ast继续展开
            return expanded_ast.statements[0]
        else:
            return node

    def _expand_for_loop(self, node: ForNode) -> ASTNode:
        """
        展开遍历循环

        Args:
            node: For节点

        Returns:
            展开后的AST节点
        """
        # 将遍历循环转换为宏调用
        macro_call = FunctionCallNode(name="遍历", args=[IdentifierNode(name=node.var, line=node.line, column=node.column), node.iterable, node.body], line=node.line, column=node.column)
        expanded = self._expand_macro_call(macro_call)
        # 如果展开结果是列表，直接返回
        if isinstance(expanded, list):
            return expanded
        # 否则包装成列表（单个语句）
        return [expanded] if expanded else []

    def _expand_repeat_loop(self, node: RepeatNode) -> ASTNode:
        """
        展开重复循环

        Args:
            node: Repeat节点

        Returns:
            展开后的AST节点
        """
        # 将重复循环转换为宏调用
        macro_call = FunctionCallNode(name="重复", args=[node.count, node.body], line=node.line, column=node.column)
        expanded = self._expand_macro_call(macro_call)
        # 如果展开结果是列表，直接返回
        if isinstance(expanded, list):
            return expanded
        # 否则包装成列表（单个语句）
        return [expanded] if expanded else []
