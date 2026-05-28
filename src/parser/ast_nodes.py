# -*- coding: utf-8 -*-
"""AST节点定义

定义所有抽象语法树节点类型，用于语法分析器构建AST。
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict


@dataclass
class ASTNode(ABC):
    """AST节点抽象基类

    所有AST节点都继承此类，提供位置信息和调试输出。
    """
    line: int
    column: int

    @abstractmethod
    def __str__(self) -> str:
        """返回节点的字符串表示，用于调试"""
        pass


# ============ 基础节点 ============

@dataclass
class NumberNode(ASTNode):
    """数字节点

    表示整数或浮点数字面量。
    """
    value: Any  # int 或 float

    def __str__(self) -> str:
        return f"NumberNode({self.value})"


@dataclass
class StringNode(ASTNode):
    """字符串节点

    表示字符串字面量。
    """
    value: str

    def __str__(self) -> str:
        return f"StringNode({self.value!r})"


@dataclass
class IdentifierNode(ASTNode):
    """标识符节点

    表示变量名、函数名等标识符。
    """
    name: str

    def __str__(self) -> str:
        return f"IdentifierNode({self.name})"


# ============ 表达式节点 ============

@dataclass
class BinaryOpNode(ASTNode):
    """二元操作节点

    表示二元运算，如加减乘除、比较等。
    """
    left: ASTNode
    operator: str
    right: ASTNode

    def __str__(self) -> str:
        return f"BinaryOpNode({self.left} {self.operator} {self.right})"


@dataclass
class UnaryOpNode(ASTNode):
    """一元操作节点

    表示一元运算，如负号、逻辑非等。
    """
    operator: str
    operand: ASTNode

    def __str__(self) -> str:
        return f"UnaryOpNode({self.operator}{self.operand})"


@dataclass
class ListNode(ASTNode):
    """列表节点

    表示列表字面量。
    """
    elements: List[ASTNode] = field(default_factory=list)

    def __str__(self) -> str:
        elements_str = ", ".join(str(e) for e in self.elements)
        return f"ListNode([{elements_str}])"


@dataclass
class DictNode(ASTNode):
    """字典节点

    表示字典字面量。
    """
    pairs: List[tuple] = field(default_factory=list)  # List[(ASTNode, ASTNode)]

    def __str__(self) -> str:
        pairs_str = ", ".join(f"{k}: {v}" for k, v in self.pairs)
        return f"DictNode({{{pairs_str}}})"


@dataclass
class MemberAccessNode(ASTNode):
    """成员访问节点

    表示对象成员访问，如 obj.member。
    """
    obj: ASTNode
    member: str

    def __str__(self) -> str:
        return f"MemberAccessNode({self.obj}.{self.member})"


@dataclass
class IndexNode(ASTNode):
    """索引节点

    表示索引访问，如 list[index]。
    """
    obj: ASTNode
    index: ASTNode

    def __str__(self) -> str:
        return f"IndexNode({self.obj}[{self.index}])"


# ============ 语句节点 ============

@dataclass
class AssignNode(ASTNode):
    """赋值节点

    表示变量赋值语句。
    """
    target: ASTNode  # 通常是 IdentifierNode
    value: ASTNode

    def __str__(self) -> str:
        return f"AssignNode({self.target} = {self.value})"


@dataclass
class VarDefNode(ASTNode):
    """变量定义节点

    表示变量定义语句，如 '定 x = 1'。
    """
    name: str
    value: Optional[ASTNode] = None

    def __str__(self) -> str:
        if self.value:
            return f"VarDefNode({self.name} = {self.value})"
        return f"VarDefNode({self.name})"


@dataclass
class IfNode(ASTNode):
    """条件节点

    表示条件语句，如 '若 x 则 ... 否则 ...'。
    """
    condition: ASTNode
    then_branch: List[ASTNode]
    else_branch: Optional[List[ASTNode]] = None

    def __str__(self) -> str:
        return f"IfNode(condition={self.condition}, then={len(self.then_branch)} stmts)"


@dataclass
class ForNode(ASTNode):
    """遍历循环节点

    表示遍历循环，如 '遍历 x 于 列表：...'。
    """
    var: str
    iterable: ASTNode
    body: List[ASTNode]

    def __str__(self) -> str:
        return f"ForNode({self.var} in {self.iterable}, {len(self.body)} stmts)"


@dataclass
class WhileNode(ASTNode):
    """当循环节点

    表示当循环，如 '当 条件：...'。
    """
    condition: ASTNode
    body: List[ASTNode]

    def __str__(self) -> str:
        return f"WhileNode(condition={self.condition}, {len(self.body)} stmts)"


@dataclass
class RepeatNode(ASTNode):
    """重复节点

    表示重复执行，如 '重复 10 次：...'。
    """
    count: ASTNode
    body: List[ASTNode]

    def __str__(self) -> str:
        return f"RepeatNode({self.count} times, {len(self.body)} stmts)"


@dataclass
class FunctionDefNode(ASTNode):
    """函数定义节点

    表示函数定义，如 '定 函数名 = 函 参数：...'。
    """
    name: str
    params: List[str]
    body: List[ASTNode]

    def __str__(self) -> str:
        params_str = ", ".join(self.params)
        return f"FunctionDefNode({self.name}({params_str}), {len(self.body)} stmts)"


@dataclass
class FunctionCallNode(ASTNode):
    """函数调用节点

    表示函数调用，如 '函数名 参数1 参数2'。
    """
    name: str
    args: List[ASTNode] = field(default_factory=list)
    arity: Optional['Arity'] = None  # 元数定义（可选）

    def __str__(self) -> str:
        args_str = ", ".join(str(a) for a in self.args)
        return f"FunctionCallNode({self.name}({args_str}))"


@dataclass
class ReturnNode(ASTNode):
    """返回节点

    表示返回语句。
    """
    value: Optional[ASTNode] = None

    def __str__(self) -> str:
        if self.value:
            return f"ReturnNode({self.value})"
        return "ReturnNode()"


# ============ 特殊节点 ============

@dataclass
class ProgramNode(ASTNode):
    """程序根节点

    表示整个程序的根节点。
    """
    statements: List[ASTNode] = field(default_factory=list)

    def __str__(self) -> str:
        return f"ProgramNode({len(self.statements)} statements)"


@dataclass
class BlockNode(ASTNode):
    """代码块节点

    表示一个代码块，通常用于缩进块。
    """
    statements: List[ASTNode] = field(default_factory=list)

    def __str__(self) -> str:
        return f"BlockNode({len(self.statements)} statements)"
