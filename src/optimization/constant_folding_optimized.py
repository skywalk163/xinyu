# -*- coding: utf-8 -*-
"""优化版常量折叠优化器

在编译阶段计算常量表达式，减少运行时计算。
使用原地修改减少对象创建开销。
"""

from typing import Any, Optional

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


class OptimizedConstantFoldingOptimizer:
    """优化版常量折叠优化器

    在编译阶段计算常量表达式，减少运行时计算。
    使用原地修改减少对象创建开销。

    优化特性：
    1. 原地修改AST节点，减少对象创建
    2. 使用类型检查代替isinstance()调用
    3. 提前返回避免不必要的递归
    4. 缓存操作符映射
    """

    # 操作符映射缓存
    _BINARY_OPERATORS = {
        # 算术操作符
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,
        "%": lambda a, b: a % b,
        "//": lambda a, b: a // b,
        # 比较操作符
        "==": lambda a, b: 1 if a == b else 0,
        "!=": lambda a, b: 1 if a != b else 0,
        "<": lambda a, b: 1 if a < b else 0,
        ">": lambda a, b: 1 if a > b else 0,
        "<=": lambda a, b: 1 if a <= b else 0,
        ">=": lambda a, b: 1 if a >= b else 0,
        # 逻辑操作符
        "and": lambda a, b: 1 if a and b else 0,
        "or": lambda a, b: 1 if a or b else 0,
        # 中文操作符
        "相加": lambda a, b: a + b,
        "相减": lambda a, b: a - b,
        "相乘": lambda a, b: a * b,
        "相除": lambda a, b: a / b,
        "相除以": lambda a, b: a / b,
        "取余": lambda a, b: a % b,
        "等于": lambda a, b: 1 if a == b else 0,
        "不等": lambda a, b: 1 if a != b else 0,
        "大于": lambda a, b: 1 if a > b else 0,
        "大于于": lambda a, b: 1 if a > b else 0,
        "小于": lambda a, b: 1 if a < b else 0,
        "小于于": lambda a, b: 1 if a < b else 0,
        "大等": lambda a, b: 1 if a >= b else 0,
        "大于等于": lambda a, b: 1 if a >= b else 0,
        "小等": lambda a, b: 1 if a <= b else 0,
        "小于等于": lambda a, b: 1 if a <= b else 0,
        "并且": lambda a, b: 1 if a and b else 0,
        "或者": lambda a, b: 1 if a or b else 0,
        "加": lambda a, b: a + b,
        "减": lambda a, b: a - b,
        "乘": lambda a, b: a * b,
        "除": lambda a, b: a / b,
        "等": lambda a, b: 1 if a == b else 0,
        "大": lambda a, b: 1 if a > b else 0,
        "小": lambda a, b: 1 if a < b else 0,
        "且": lambda a, b: 1 if a and b else 0,
        "或": lambda a, b: 1 if a or b else 0,
    }

    _UNARY_OPERATORS = {
        "-": lambda a: -a,
        "not": lambda a: 0 if a else 1,
        "负": lambda a: -a,
        "非也": lambda a: 0 if a else 1,
        "非也也": lambda a: 0 if a else 1,
        "非": lambda a: 0 if a else 1,
    }

    def __init__(self):
        """初始化优化版常量折叠优化器"""
        self.optimized_count = 0
        self._changed = False

    def optimize(self, node: ASTNode) -> ASTNode:
        """优化AST节点（原地修改）

        Args:
            node: 要优化的AST节点

        Returns:
            优化后的AST节点（可能是原节点或新节点）
        """
        self._changed = False
        result = self._optimize_node(node)
        return result

    def _optimize_node(self, node: ASTNode) -> ASTNode:
        """优化单个AST节点（原地修改）

        Args:
            node: 要优化的AST节点

        Returns:
            优化后的AST节点
        """
        # 根据节点类型分派
        node_type = type(node)

        if node_type is BinaryOpNode:
            return self._optimize_binaryop(node)
        elif node_type is UnaryOpNode:
            return self._optimize_unaryop(node)
        elif node_type is IfNode:
            return self._optimize_if(node)
        elif node_type is WhileNode:
            return self._optimize_while(node)
        elif node_type is ForNode:
            return self._optimize_for(node)
        elif node_type is BlockNode:
            return self._optimize_block(node)
        elif node_type is ProgramNode:
            return self._optimize_program(node)
        elif node_type is FunctionCallNode:
            return self._optimize_functioncall(node)
        elif node_type is AssignNode:
            return self._optimize_assign(node)
        elif node_type is VarDefNode:
            return self._optimize_vardef(node)
        elif node_type is ReturnNode:
            return self._optimize_return(node)
        elif node_type is ClassNode:
            return self._optimize_class(node)
        elif node_type is MethodNode:
            return self._optimize_method(node)
        elif node_type is TryNode:
            return self._optimize_try(node)
        else:
            # 其他节点类型不需要优化
            return node

    def _optimize_binaryop(self, node: BinaryOpNode) -> ASTNode:
        """优化二元操作节点（原地修改）

        Args:
            node: 二元操作节点

        Returns:
            优化后的节点
        """
        # 递归优化左右操作数
        left = self._optimize_node(node.left)
        right = self._optimize_node(node.right)

        # 更新节点（原地修改）
        if left is not node.left:
            node.left = left
            self._changed = True

        if right is not node.right:
            node.right = right
            self._changed = True

        # 如果左右都是常量，尝试折叠
        if type(left) is NumberNode and type(right) is NumberNode:
            result = self._fold_binary_number(left.value, right.value, node.operator)
            if result is not None:
                self.optimized_count += 1
                return NumberNode(line=node.line, column=node.column, value=result)

        elif type(left) is StringNode and type(right) is StringNode:
            if node.operator in ["+", "相加", "加"]:
                self.optimized_count += 1
                return StringNode(
                    line=node.line, column=node.column, value=left.value + right.value
                )

        return node

    def _fold_binary_number(self, left_val: Any, right_val: Any, operator: str) -> Optional[Any]:
        """折叠二元数字常量表达式

        Args:
            left_val: 左操作数值
            right_val: 右操作数值
            operator: 操作符

        Returns:
            折叠后的值，如果无法折叠则返回None
        """
        try:
            op_func = self._BINARY_OPERATORS.get(operator)
            if op_func is None:
                return None

            # 特殊处理除零
            if operator in ["/", "相除", "相除以", "除", "%", "取余", "//"] and right_val == 0:
                return None

            return op_func(left_val, right_val)

        except (ZeroDivisionError, ValueError, TypeError):
            # 运算错误，不折叠
            return None

    def _optimize_unaryop(self, node: UnaryOpNode) -> ASTNode:
        """优化一元操作节点（原地修改）

        Args:
            node: 一元操作节点

        Returns:
            优化后的节点
        """
        # 递归优化操作数
        operand = self._optimize_node(node.operand)

        # 更新节点（原地修改）
        if operand is not node.operand:
            node.operand = operand
            self._changed = True

        # 如果操作数是常量，尝试折叠
        if type(operand) is NumberNode:
            result = self._fold_unary_number(operand.value, node.operator)
            if result is not None:
                self.optimized_count += 1
                return NumberNode(line=node.line, column=node.column, value=result)

        return node

    def _fold_unary_number(self, operand_val: Any, operator: str) -> Optional[Any]:
        """折叠一元数字常量表达式

        Args:
            operand_val: 操作数值
            operator: 操作符

        Returns:
            折叠后的值，如果无法折叠则返回None
        """
        try:
            op_func = self._UNARY_OPERATORS.get(operator)
            if op_func is None:
                return None

            return op_func(operand_val)

        except (ValueError, TypeError):
            # 运算错误，不折叠
            return None

    def _optimize_if(self, node: IfNode) -> ASTNode:
        """优化条件语句节点（原地修改）

        Args:
            node: 条件语句节点

        Returns:
            优化后的节点
        """
        # 递归优化条件
        condition = self._optimize_node(node.condition)

        # 更新节点（原地修改）
        if condition is not node.condition:
            node.condition = condition
            self._changed = True

        # 如果条件是常量，可以优化整个if语句
        if type(condition) is NumberNode:
            # 条件为真（非零）
            if condition.value:
                # 只保留then分支
                then_branch = (
                    self._optimize_statements(node.then_branch) if node.then_branch else []
                )
                self.optimized_count += 1
                return BlockNode(line=node.line, column=node.column, statements=then_branch)
            else:
                # 条件为假（零）
                if node.else_branch:
                    # 只保留else分支
                    else_branch = self._optimize_statements(node.else_branch)
                    self.optimized_count += 1
                    return BlockNode(line=node.line, column=node.column, statements=else_branch)
                else:
                    # 没有else分支，整个if语句可以删除
                    self.optimized_count += 1
                    return BlockNode(line=node.line, column=node.column, statements=[])

        # 优化then和else分支
        then_branch = self._optimize_statements(node.then_branch) if node.then_branch else []
        else_branch = self._optimize_statements(node.else_branch) if node.else_branch else []

        # 更新节点（原地修改）
        if then_branch is not node.then_branch:
            node.then_branch = then_branch
            self._changed = True

        if else_branch is not node.else_branch:
            node.else_branch = else_branch
            self._changed = True

        return node

    def _optimize_while(self, node: WhileNode) -> ASTNode:
        """优化while循环节点（原地修改）

        Args:
            node: while循环节点

        Returns:
            优化后的节点
        """
        # 递归优化条件
        condition = self._optimize_node(node.condition)

        # 更新节点（原地修改）
        if condition is not node.condition:
            node.condition = condition
            self._changed = True

        # 如果条件是常量假，整个循环可以删除
        if type(condition) is NumberNode and not condition.value:
            self.optimized_count += 1
            return BlockNode(line=node.line, column=node.column, statements=[])

        # 优化循环体
        body = self._optimize_statements(node.body) if node.body else []

        # 更新节点（原地修改）
        if body is not node.body:
            node.body = body
            self._changed = True

        return node

    def _optimize_for(self, node: ForNode) -> ASTNode:
        """优化for循环节点（原地修改）

        Args:
            node: for循环节点

        Returns:
            优化后的节点
        """
        # 递归优化目标变量和可迭代对象
        target = self._optimize_node(node.target)
        iterable = self._optimize_node(node.iterable)

        # 更新节点（原地修改）
        if target is not node.target:
            node.target = target
            self._changed = True

        if iterable is not node.iterable:
            node.iterable = iterable
            self._changed = True

        # 优化循环体
        body = self._optimize_statements(node.body) if node.body else []

        # 更新节点（原地修改）
        if body is not node.body:
            node.body = body
            self._changed = True

        return node

    def _optimize_block(self, node: BlockNode) -> BlockNode:
        """优化代码块节点（原地修改）

        Args:
            node: 代码块节点

        Returns:
            优化后的代码块节点
        """
        if not node.statements:
            return node

        # 优化每个语句
        optimized_statements = self._optimize_statements(node.statements)

        # 更新节点（原地修改）
        if optimized_statements is not node.statements:
            node.statements = optimized_statements
            self._changed = True

        return node

    def _optimize_statements(self, statements: list) -> list:
        """优化语句列表（原地修改）

        Args:
            statements: 语句列表

        Returns:
            优化后的语句列表
        """
        if not statements:
            return []

        optimized_statements = []
        changed = False

        for stmt in statements:
            optimized_stmt = self._optimize_node(stmt)
            if optimized_stmt:
                # 如果优化后是BlockNode，展开它
                if type(optimized_stmt) is BlockNode:
                    optimized_statements.extend(optimized_stmt.statements)
                    changed = True
                else:
                    optimized_statements.append(optimized_stmt)
                    if optimized_stmt is not stmt:
                        changed = True
            else:
                # 语句被优化掉了
                changed = True

        # 移除空语句
        if len(optimized_statements) != len(statements):
            changed = True

        return optimized_statements if changed else statements

    def _optimize_program(self, node: ProgramNode) -> ProgramNode:
        """优化程序节点（原地修改）

        Args:
            node: 程序节点

        Returns:
            优化后的程序节点
        """
        if not node.statements:
            return node

        # 优化每个语句
        optimized_statements = self._optimize_statements(node.statements)

        # 更新节点（原地修改）
        if optimized_statements is not node.statements:
            node.statements = optimized_statements
            self._changed = True

        return node

    def _optimize_functioncall(self, node: FunctionCallNode) -> ASTNode:
        """优化函数调用节点（原地修改）

        Args:
            node: 函数调用节点

        Returns:
            优化后的节点
        """
        # 递归优化函数名和参数
        if not isinstance(node.name, str):
            name = self._optimize_node(node.name)
            if name is not node.name:
                node.name = name

        args_changed = False
        if node.args:
            optimized_args = []
            for arg in node.args:
                optimized_arg = self._optimize_node(arg)
                optimized_args.append(optimized_arg)
                if optimized_arg is not arg:
                    args_changed = True

            if args_changed:
                node.args = optimized_args

        return node

    def _optimize_assign(self, node: AssignNode) -> ASTNode:
        """优化赋值节点（原地修改）

        Args:
            node: 赋值节点

        Returns:
            优化后的节点
        """
        # 递归优化目标和值
        target = self._optimize_node(node.target)
        value = self._optimize_node(node.value)

        # 更新节点（原地修改）
        if target is not node.target:
            node.target = target
            self._changed = True

        if value is not node.value:
            node.value = value
            self._changed = True

        return node

    def _optimize_vardef(self, node: VarDefNode) -> ASTNode:
        """优化变量定义节点（原地修改）

        Args:
            node: 变量定义节点

        Returns:
            优化后的节点
        """
        # 递归优化值
        if node.value is not None:
            value = self._optimize_node(node.value)
            if value is not node.value:
                node.value = value
                self._changed = True

        return node

    def _optimize_return(self, node: ReturnNode) -> ASTNode:
        """优化return节点（原地修改）

        Args:
            node: return节点

        Returns:
            优化后的节点
        """
        # 递归优化返回值
        if node.value is not None:
            value = self._optimize_node(node.value)
            if value is not node.value:
                node.value = value
                self._changed = True

        return node

    def _optimize_class(self, node: ClassNode) -> ASTNode:
        """优化类定义节点（原地修改）

        Args:
            node: 类定义节点

        Returns:
            优化后的节点
        """
        # 优化类成员
        if node.members:
            optimized_members = []
            changed = False

            for member in node.members:
                optimized_member = self._optimize_node(member)
                if optimized_member:
                    optimized_members.append(optimized_member)
                    if optimized_member is not member:
                        changed = True
                else:
                    changed = True

            if changed:
                node.members = optimized_members
                self._changed = True

        return node

    def _optimize_method(self, node: MethodNode) -> ASTNode:
        """优化方法定义节点（原地修改）

        Args:
            node: 方法定义节点

        Returns:
            优化后的节点
        """
        # 优化方法体
        if node.body:
            body = self._optimize_statements(node.body)
            if body is not node.body:
                node.body = body
                self._changed = True

        return node

    def _optimize_try(self, node: TryNode) -> ASTNode:
        """优化try节点（原地修改）

        Args:
            node: try节点

        Returns:
            优化后的节点
        """
        # 优化try块
        if node.try_body:
            try_body = self._optimize_statements(node.try_body)
            if try_body is not node.try_body:
                node.try_body = try_body
                self._changed = True

        # 优化except子句
        if node.except_clauses:
            optimized_except_clauses = []
            changed = False

            for except_clause in node.except_clauses:
                optimized_except = self._optimize_node(except_clause)
                if optimized_except:
                    optimized_except_clauses.append(optimized_except)
                    if optimized_except is not except_clause:
                        changed = True
                else:
                    changed = True

            if changed:
                node.except_clauses = optimized_except_clauses
                self._changed = True

        # 优化finally块
        if node.finally_body:
            finally_body = self._optimize_statements(node.finally_body)
            if finally_body is not node.finally_body:
                node.finally_body = finally_body
                self._changed = True

        return node

    def get_optimization_stats(self) -> dict:
        """获取优化统计信息

        Returns:
            包含优化统计信息的字典
        """
        return {
            "optimized_count": self.optimized_count,
            "changed_nodes": self._changed,
            "description": "优化版常量折叠优化",
        }

    def reset_stats(self):
        """重置优化统计信息"""
        self.optimized_count = 0
        self._changed = False


# 测试函数
def test_optimized_constant_folding():
    """测试优化版常量折叠优化器"""
    from src.parser.ast_nodes import (
        BinaryOpNode,
        BlockNode,
        IfNode,
        NumberNode,
        StringNode,
        UnaryOpNode,
        WhileNode,
    )

    optimizer = OptimizedConstantFoldingOptimizer()

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
    print(f"  值: {optimized.value if type(optimized) is NumberNode else 'N/A'}")
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
    print(f"  值: {optimized.value if type(optimized) is StringNode else 'N/A'}")
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
    print(f"  值: {optimized.value if type(optimized) is NumberNode else 'N/A'}")
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
    if type(optimized) is BlockNode:
        print(f"  优化后语句数: {len(optimized.statements)}")
        for i, stmt in enumerate(optimized.statements):
            print(f"    语句{i+1}: {stmt}")
    else:
        print("  优化后语句数: N/A")
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
    if type(optimized) is BlockNode:
        print(f"  优化后语句数: {len(optimized.statements)}")
        for i, stmt in enumerate(optimized.statements):
            print(f"    语句{i+1}: {stmt}")
    else:
        print("  优化后语句数: N/A")
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
    if type(optimized) is BlockNode:
        print(f"  优化后语句数: {len(optimized.statements)}")
    else:
        print("  优化后语句数: N/A")
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
    if type(optimized) is NumberNode:
        print(f"  值: {optimized.value}")
    else:
        print("  值: N/A (未完全折叠)")
    print()

    # 输出统计信息
    stats = optimizer.get_optimization_stats()
    print("优化统计:")
    print(f"  折叠的常量表达式数量: {stats['optimized_count']}")
    print(f"  节点是否被修改: {stats['changed_nodes']}")
    print(f"  优化类型: {stats['description']}")

    return optimizer


if __name__ == "__main__":
    test_optimized_constant_folding()
