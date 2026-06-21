# -*- coding: utf-8 -*-
"""常量折叠优化器

在编译阶段计算常量表达式，减少运行时计算。
"""

from typing import Union

from src.parser.ast_nodes import (
    AssignNode,
    ASTNode,
    BinaryOpNode,
    BlockNode,
    ClassNode,
    ForNode,
    FunctionCallNode,
    IfNode,
    MethodNode,
    NumberNode,
    ProgramNode,
    ReturnNode,
    StringNode,
    TryNode,
    UnaryOpNode,
    VarDefNode,
    WhileNode,
)


class ConstantFoldingOptimizer:
    """常量折叠优化器

    在编译阶段计算常量表达式，减少运行时计算。
    支持以下优化：
    1. 数字常量运算：1 + 2 -> 3
    2. 字符串连接："a" + "b" -> "ab"
    3. 布尔运算：True and False -> False
    4. 逻辑运算：not True -> False
    5. 列表/字典常量操作
    """

    def __init__(self):
        """初始化常量折叠优化器"""
        self.optimized_count = 0

    def optimize(self, node: ASTNode) -> ASTNode:
        """优化AST节点

        Args:
            node: 要优化的AST节点

        Returns:
            优化后的AST节点
        """
        return self._optimize_node(node)

    def _optimize_node(self, node: ASTNode) -> ASTNode:
        """优化单个AST节点

        Args:
            node: 要优化的AST节点

        Returns:
            优化后的AST节点
        """
        if isinstance(node, BinaryOpNode):
            return self._optimize_binaryop(node)
        elif isinstance(node, UnaryOpNode):
            return self._optimize_unaryop(node)
        elif isinstance(node, IfNode):
            return self._optimize_if(node)
        elif isinstance(node, WhileNode):
            return self._optimize_while(node)
        elif isinstance(node, ForNode):
            return self._optimize_for(node)
        elif isinstance(node, BlockNode):
            return self._optimize_block(node)
        elif isinstance(node, ProgramNode):
            return self._optimize_program(node)
        elif isinstance(node, FunctionCallNode):
            return self._optimize_functioncall(node)
        elif isinstance(node, AssignNode):
            return self._optimize_assign(node)
        elif isinstance(node, VarDefNode):
            return self._optimize_vardef(node)
        elif isinstance(node, ReturnNode):
            return self._optimize_return(node)
        elif isinstance(node, ClassNode):
            return self._optimize_class(node)
        elif isinstance(node, MethodNode):
            return self._optimize_method(node)
        elif isinstance(node, TryNode):
            return self._optimize_try(node)
        else:
            # 其他节点类型不需要优化
            return node

    def _optimize_binaryop(self, node: BinaryOpNode) -> ASTNode:
        """优化二元操作节点

        Args:
            node: 二元操作节点

        Returns:
            优化后的节点
        """
        # 递归优化左右操作数
        left = self._optimize_node(node.left)
        right = self._optimize_node(node.right)

        # 如果左右都是常量，尝试折叠
        if isinstance(left, (NumberNode, StringNode)) and isinstance(
            right, (NumberNode, StringNode)
        ):
            result = self._fold_binary_constant(left, right, node.operator)
            if result is not None:
                self.optimized_count += 1
                return result

        # 如果操作数被优化了，返回新的节点
        if left is not node.left or right is not node.right:
            return BinaryOpNode(
                line=node.line, column=node.column, left=left, operator=node.operator, right=right
            )

        return node

    def _fold_binary_constant(
        self,
        left: Union[NumberNode, StringNode],
        right: Union[NumberNode, StringNode],
        operator: str,
    ) -> Union[NumberNode, StringNode, None]:
        """折叠二元常量表达式

        Args:
            left: 左操作数
            right: 右操作数
            operator: 操作符

        Returns:
            折叠后的常量节点，如果无法折叠则返回None
        """
        try:
            if isinstance(left, NumberNode) and isinstance(right, NumberNode):
                # 数字常量运算
                left_val = left.value
                right_val = right.value

                if operator in ["+", "相加", "加"]:
                    return NumberNode(
                        line=left.line, column=left.column, value=left_val + right_val
                    )
                elif operator in ["-", "相减", "减"]:
                    return NumberNode(
                        line=left.line, column=left.column, value=left_val - right_val
                    )
                elif operator in ["*", "相乘", "乘"]:
                    return NumberNode(
                        line=left.line, column=left.column, value=left_val * right_val
                    )
                elif operator in ["/", "相除", "除", "相除以"]:
                    if right_val == 0:
                        return None  # 除零错误，不折叠
                    return NumberNode(
                        line=left.line, column=left.column, value=left_val / right_val
                    )
                elif operator in ["%", "取余"]:
                    if right_val == 0:
                        return None  # 模零错误，不折叠
                    return NumberNode(
                        line=left.line, column=left.column, value=left_val % right_val
                    )
                elif operator in ["//"]:
                    if right_val == 0:
                        return None  # 除零错误，不折叠
                    return NumberNode(
                        line=left.line, column=left.column, value=left_val // right_val
                    )
                elif operator in ["==", "等于", "等"]:
                    return NumberNode(
                        line=left.line, column=left.column, value=1 if left_val == right_val else 0
                    )
                elif operator in ["!=", "不等"]:
                    return NumberNode(
                        line=left.line, column=left.column, value=1 if left_val != right_val else 0
                    )
                elif operator in ["<", "小于", "小"]:
                    return NumberNode(
                        line=left.line, column=left.column, value=1 if left_val < right_val else 0
                    )
                elif operator in [">", "大于", "大"]:
                    return NumberNode(
                        line=left.line, column=left.column, value=1 if left_val > right_val else 0
                    )
                elif operator in ["<=", "小等", "小于等于"]:
                    return NumberNode(
                        line=left.line, column=left.column, value=1 if left_val <= right_val else 0
                    )
                elif operator in [">=", "大等", "大于等于"]:
                    return NumberNode(
                        line=left.line, column=left.column, value=1 if left_val >= right_val else 0
                    )
                elif operator in ["and", "并且", "且"]:
                    # Python中非零为真
                    left_bool = bool(left_val)
                    right_bool = bool(right_val)
                    return NumberNode(
                        line=left.line,
                        column=left.column,
                        value=1 if left_bool and right_bool else 0,
                    )
                elif operator in ["or", "或者", "或"]:
                    left_bool = bool(left_val)
                    right_bool = bool(right_val)
                    return NumberNode(
                        line=left.line,
                        column=left.column,
                        value=1 if left_bool or right_bool else 0,
                    )

            elif isinstance(left, StringNode) and isinstance(right, StringNode):
                # 字符串连接
                if operator in ["+", "相加", "加"]:
                    return StringNode(
                        line=left.line, column=left.column, value=left.value + right.value
                    )

            # 其他类型组合不支持折叠
            return None

        except (ZeroDivisionError, ValueError, TypeError):
            # 运算错误，不折叠
            return None

    def _optimize_unaryop(self, node: UnaryOpNode) -> ASTNode:
        """优化一元操作节点

        Args:
            node: 一元操作节点

        Returns:
            优化后的节点
        """
        # 递归优化操作数
        operand = self._optimize_node(node.operand)

        # 如果操作数是常量，尝试折叠
        if isinstance(operand, NumberNode):
            result = self._fold_unary_constant(operand, node.operator)
            if result is not None:
                self.optimized_count += 1
                return result

        # 如果操作数被优化了，返回新的节点
        if operand is not node.operand:
            return UnaryOpNode(
                line=node.line, column=node.column, operator=node.operator, operand=operand
            )

        return node

    def _fold_unary_constant(self, operand: NumberNode, operator: str) -> Union[NumberNode, None]:
        """折叠一元常量表达式

        Args:
            operand: 操作数
            operator: 操作符

        Returns:
            折叠后的常量节点，如果无法折叠则返回None
        """
        try:
            val = operand.value

            if operator in ["-", "负"]:
                return NumberNode(line=operand.line, column=operand.column, value=-val)
            elif operator in ["not", "非也", "非也也", "非"]:
                # Python中非零为真
                return NumberNode(line=operand.line, column=operand.column, value=0 if val else 1)

            return None

        except (ValueError, TypeError):
            # 运算错误，不折叠
            return None

    def _optimize_if(self, node: IfNode) -> ASTNode:
        """优化条件语句节点

        Args:
            node: 条件语句节点

        Returns:
            优化后的节点
        """
        # 递归优化条件
        condition = self._optimize_node(node.condition)

        # 如果条件是常量，可以优化整个if语句
        if isinstance(condition, NumberNode):
            # 条件为真（非零）
            if condition.value:
                # 只保留then分支
                then_branch = self._optimize_block_or_list(node.then_branch)
                return BlockNode(line=node.line, column=node.column, statements=then_branch)
            else:
                # 条件为假（零）
                if node.else_branch:
                    # 只保留else分支
                    else_branch = self._optimize_block_or_list(node.else_branch)
                    return BlockNode(line=node.line, column=node.column, statements=else_branch)
                else:
                    # 没有else分支，整个if语句可以删除
                    return BlockNode(line=node.line, column=node.column, statements=[])

        # 优化then和else分支
        then_branch = self._optimize_block_or_list(node.then_branch) if node.then_branch else []
        else_branch = self._optimize_block_or_list(node.else_branch) if node.else_branch else []

        # 如果分支被优化了，返回新的节点
        if (
            condition is not node.condition
            or then_branch is not node.then_branch
            or else_branch is not node.else_branch
        ):
            return IfNode(
                line=node.line,
                column=node.column,
                condition=condition,
                then_branch=then_branch,
                else_branch=else_branch,
            )

        return node

    def _optimize_while(self, node: WhileNode) -> ASTNode:
        """优化while循环节点

        Args:
            node: while循环节点

        Returns:
            优化后的节点
        """
        # 递归优化条件
        condition = self._optimize_node(node.condition)

        # 如果条件是常量假，整个循环可以删除
        if isinstance(condition, NumberNode) and not condition.value:
            return BlockNode(line=node.line, column=node.column, statements=[])

        # 优化循环体
        body = self._optimize_block_or_list(node.body) if node.body else []

        # 如果条件或循环体被优化了，返回新的节点
        if condition is not node.condition or body is not node.body:
            return WhileNode(line=node.line, column=node.column, condition=condition, body=body)

        return node

    def _optimize_for(self, node: ForNode) -> ASTNode:
        """优化for循环节点

        Args:
            node: for循环节点

        Returns:
            优化后的节点
        """
        # 递归优化目标变量和可迭代对象
        target = self._optimize_node(node.target)
        iterable = self._optimize_node(node.iterable)

        # 优化循环体
        body = self._optimize_block_or_list(node.body) if node.body else []

        # 如果任何部分被优化了，返回新的节点
        if target is not node.target or iterable is not node.iterable or body is not node.body:
            return ForNode(
                line=node.line, column=node.column, target=target, iterable=iterable, body=body
            )

        return node

    def _optimize_block(self, node: BlockNode) -> BlockNode:
        """优化代码块节点

        Args:
            node: 代码块节点

        Returns:
            优化后的代码块节点
        """
        if not node.statements:
            return node

        # 优化每个语句
        optimized_statements = []
        for stmt in node.statements:
            optimized_stmt = self._optimize_node(stmt)
            if optimized_stmt:
                # 如果优化后是BlockNode，展开它
                if isinstance(optimized_stmt, BlockNode):
                    optimized_statements.extend(optimized_stmt.statements)
                else:
                    optimized_statements.append(optimized_stmt)

        # 移除空语句
        optimized_statements = [stmt for stmt in optimized_statements if stmt]

        # 如果语句列表被优化了，返回新的节点
        if optimized_statements != node.statements:
            return BlockNode(line=node.line, column=node.column, statements=optimized_statements)

        return node

    def _optimize_block_or_list(self, statements: list) -> list:
        """优化语句列表

        Args:
            statements: 语句列表

        Returns:
            优化后的语句列表
        """
        if not statements:
            return []

        optimized_statements = []
        for stmt in statements:
            optimized_stmt = self._optimize_node(stmt)
            if optimized_stmt:
                # 如果优化后是BlockNode，展开它
                if isinstance(optimized_stmt, BlockNode):
                    optimized_statements.extend(optimized_stmt.statements)
                else:
                    optimized_statements.append(optimized_stmt)

        # 移除空语句
        return [stmt for stmt in optimized_statements if stmt]

    def _optimize_program(self, node: ProgramNode) -> ProgramNode:
        """优化程序节点

        Args:
            node: 程序节点

        Returns:
            优化后的程序节点
        """
        if not node.statements:
            return node

        # 优化每个语句
        optimized_statements = self._optimize_block_or_list(node.statements)

        # 如果语句列表被优化了，返回新的节点
        if optimized_statements != node.statements:
            return ProgramNode(line=node.line, column=node.column, statements=optimized_statements)

        return node

    def _optimize_functioncall(self, node: FunctionCallNode) -> ASTNode:
        """优化函数调用节点

        Args:
            node: 函数调用节点

        Returns:
            优化后的节点
        """
        # 递归优化函数名和参数
        name = self._optimize_node(node.name) if not isinstance(node.name, str) else node.name
        args = [self._optimize_node(arg) for arg in node.args] if node.args else []

        # 如果任何部分被优化了，返回新的节点
        if name is not node.name or args != node.args:
            return FunctionCallNode(line=node.line, column=node.column, name=name, args=args)

        return node

    def _optimize_assign(self, node: AssignNode) -> ASTNode:
        """优化赋值节点

        Args:
            node: 赋值节点

        Returns:
            优化后的节点
        """
        # 递归优化目标和值
        target = self._optimize_node(node.target)
        value = self._optimize_node(node.value)

        # 如果任何部分被优化了，返回新的节点
        if target is not node.target or value is not node.value:
            return AssignNode(line=node.line, column=node.column, target=target, value=value)

        return node

    def _optimize_vardef(self, node: VarDefNode) -> ASTNode:
        """优化变量定义节点

        Args:
            node: 变量定义节点

        Returns:
            优化后的节点
        """
        # 递归优化值
        value = self._optimize_node(node.value) if node.value is not None else None

        # 如果值被优化了，返回新的节点
        if value is not node.value:
            return VarDefNode(line=node.line, column=node.column, name=node.name, value=value)

        return node

    def _optimize_return(self, node: ReturnNode) -> ASTNode:
        """优化return节点

        Args:
            node: return节点

        Returns:
            优化后的节点
        """
        # 递归优化返回值
        value = self._optimize_node(node.value) if node.value is not None else None

        # 如果值被优化了，返回新的节点
        if value is not node.value:
            return ReturnNode(line=node.line, column=node.column, value=value)

        return node

    def _optimize_class(self, node: ClassNode) -> ASTNode:
        """优化类定义节点

        Args:
            node: 类定义节点

        Returns:
            优化后的节点
        """
        # 优化类成员
        optimized_members = []
        for member in node.members:
            optimized_member = self._optimize_node(member)
            if optimized_member:
                optimized_members.append(optimized_member)

        # 如果成员被优化了，返回新的节点
        if optimized_members != node.members:
            return ClassNode(
                line=node.line,
                column=node.column,
                name=node.name,
                extends=node.extends,
                implements=node.implements,
                members=optimized_members,
            )

        return node

    def _optimize_method(self, node: MethodNode) -> ASTNode:
        """优化方法定义节点

        Args:
            node: 方法定义节点

        Returns:
            优化后的节点
        """
        # 优化方法体
        body = self._optimize_block_or_list(node.body) if node.body else []

        # 如果方法体被优化了，返回新的节点
        if body != node.body:
            return MethodNode(
                line=node.line,
                column=node.column,
                name=node.name,
                params=node.params,
                body=body,
                is_static=node.is_static,
                is_constructor=node.is_constructor,
            )

        return node

    def _optimize_try(self, node: TryNode) -> ASTNode:
        """优化try节点

        Args:
            node: try节点

        Returns:
            优化后的节点
        """
        # 优化try块
        try_body = self._optimize_block_or_list(node.try_body) if node.try_body else []

        # 优化except子句
        optimized_except_clauses = []
        for except_clause in node.except_clauses:
            optimized_except = self._optimize_node(except_clause)
            if optimized_except:
                optimized_except_clauses.append(optimized_except)

        # 优化finally块
        finally_body = self._optimize_block_or_list(node.finally_body) if node.finally_body else []

        # 如果任何部分被优化了，返回新的节点
        if (
            try_body != node.try_body
            or optimized_except_clauses != node.except_clauses
            or finally_body != node.finally_body
        ):
            return TryNode(
                line=node.line,
                column=node.column,
                try_body=try_body,
                except_clauses=optimized_except_clauses,
                finally_body=finally_body,
            )

        return node

    def get_optimization_stats(self) -> dict:
        """获取优化统计信息

        Returns:
            包含优化统计信息的字典
        """
        return {"optimized_count": self.optimized_count, "description": "常量折叠优化"}

    def reset_stats(self):
        """重置优化统计信息"""
        self.optimized_count = 0


# 测试函数
def test_constant_folding():
    """测试常量折叠优化器"""
    from src.parser.ast_nodes import (
        BinaryOpNode,
        BlockNode,
        IfNode,
        NumberNode,
        StringNode,
        UnaryOpNode,
        WhileNode,
    )

    optimizer = ConstantFoldingOptimizer()

    # 测试1: 数字常量运算
    print("测试1: 数字常量运算")
    node = BinaryOpNode(
        line=1,
        column=1,
        left=NumberNode(line=1, column=1, value=10),
        operator="+",
        right=NumberNode(line=1, column=1, value=20),
    )
    optimized = optimizer.optimize(node)
    print(f"  原始: {node}")
    print(f"  优化后: {optimized}")
    print(f"  类型: {type(optimized).__name__}")
    print(f"  值: {optimized.value if isinstance(optimized, NumberNode) else 'N/A'}")
    print()

    # 测试2: 字符串连接
    print("测试2: 字符串连接")
    node = BinaryOpNode(
        line=1,
        column=1,
        left=StringNode(line=1, column=1, value="Hello, "),
        operator="+",
        right=StringNode(line=1, column=1, value="World!"),
    )
    optimized = optimizer.optimize(node)
    print(f"  原始: {node}")
    print(f"  优化后: {optimized}")
    print(f"  类型: {type(optimized).__name__}")
    print(f"  值: {optimized.value if isinstance(optimized, StringNode) else 'N/A'}")
    print()

    # 测试3: 一元操作
    print("测试3: 一元操作")
    node = UnaryOpNode(
        line=1, column=1, operator="-", operand=NumberNode(line=1, column=1, value=42)
    )
    optimized = optimizer.optimize(node)
    print(f"  原始: {node}")
    print(f"  优化后: {optimized}")
    print(f"  类型: {type(optimized).__name__}")
    print(f"  值: {optimized.value if isinstance(optimized, NumberNode) else 'N/A'}")
    print()

    # 测试4: 条件语句优化（条件为真）
    print("测试4: 条件语句优化（条件为真）")
    node = IfNode(
        line=1,
        column=1,
        condition=NumberNode(line=1, column=1, value=1),  # 真
        then_branch=[
            BinaryOpNode(
                line=2,
                column=1,
                left=NumberNode(line=2, column=1, value=1),
                operator="+",
                right=NumberNode(line=2, column=1, value=2),
            )
        ],
        else_branch=[
            BinaryOpNode(
                line=3,
                column=1,
                left=NumberNode(line=3, column=1, value=3),
                operator="+",
                right=NumberNode(line=3, column=1, value=4),
            )
        ],
    )
    optimized = optimizer.optimize(node)
    print("  原始: IfNode with condition=True")
    print(f"  优化后类型: {type(optimized).__name__}")
    print(f"  优化后语句数: {len(optimized.statements) if isinstance(optimized, BlockNode) else 'N/A'}")
    print()

    # 测试5: 条件语句优化（条件为假）
    print("测试5: 条件语句优化（条件为假）")
    node = IfNode(
        line=1,
        column=1,
        condition=NumberNode(line=1, column=1, value=0),  # 假
        then_branch=[
            BinaryOpNode(
                line=2,
                column=1,
                left=NumberNode(line=2, column=1, value=1),
                operator="+",
                right=NumberNode(line=2, column=1, value=2),
            )
        ],
        else_branch=[
            BinaryOpNode(
                line=3,
                column=1,
                left=NumberNode(line=3, column=1, value=3),
                operator="+",
                right=NumberNode(line=3, column=1, value=4),
            )
        ],
    )
    optimized = optimizer.optimize(node)
    print("  原始: IfNode with condition=False")
    print(f"  优化后类型: {type(optimized).__name__}")
    print(f"  优化后语句数: {len(optimized.statements) if isinstance(optimized, BlockNode) else 'N/A'}")
    print()

    # 测试6: while循环优化（条件为假）
    print("测试6: while循环优化（条件为假）")
    node = WhileNode(
        line=1,
        column=1,
        condition=NumberNode(line=1, column=1, value=0),  # 假
        body=[
            BinaryOpNode(
                line=2,
                column=1,
                left=NumberNode(line=2, column=1, value=1),
                operator="+",
                right=NumberNode(line=2, column=1, value=2),
            )
        ],
    )
    optimized = optimizer.optimize(node)
    print("  原始: WhileNode with condition=False")
    print(f"  优化后类型: {type(optimized).__name__}")
    print(f"  优化后语句数: {len(optimized.statements) if isinstance(optimized, BlockNode) else 'N/A'}")
    print()

    # 测试7: 复杂表达式优化
    print("测试7: 复杂表达式优化")
    node = BinaryOpNode(
        line=1,
        column=1,
        left=BinaryOpNode(
            line=1,
            column=1,
            left=NumberNode(line=1, column=1, value=10),
            operator="*",
            right=NumberNode(line=1, column=1, value=2),
        ),
        operator="+",
        right=BinaryOpNode(
            line=1,
            column=1,
            left=NumberNode(line=1, column=1, value=5),
            operator="/",
            right=NumberNode(line=1, column=1, value=2),
        ),
    )
    optimized = optimizer.optimize(node)
    print("  原始: (10 * 2) + (5 / 2)")
    print(f"  优化后: {optimized}")
    print(f"  类型: {type(optimized).__name__}")
    print(f"  值: {optimized.value if isinstance(optimized, NumberNode) else 'N/A'}")
    print()

    # 输出统计信息
    stats = optimizer.get_optimization_stats()
    print("优化统计:")
    print(f"  折叠的常量表达式数量: {stats['optimized_count']}")
    print(f"  优化类型: {stats['description']}")

    return optimizer


if __name__ == "__main__":
    test_constant_folding()
