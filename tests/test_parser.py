# -*- coding: utf-8 -*-
"""AST节点测试"""
import pytest
from src.parser.ast_nodes import (
    # 基础节点
    NumberNode, StringNode, IdentifierNode,
    # 表达式节点
    BinaryOpNode, UnaryOpNode, ListNode, DictNode,
    MemberAccessNode, IndexNode,
    # 语句节点
    AssignNode, VarDefNode, IfNode, ForNode, WhileNode,
    RepeatNode, FunctionDefNode, FunctionCallNode, ReturnNode,
    # 特殊节点
    ProgramNode, BlockNode
)


# ============ 基础节点测试 ============

def test_number_node():
    """测试数字节点"""
    node = NumberNode(line=1, column=0, value=123)
    assert node.value == 123
    assert node.line == 1
    assert node.column == 0
    assert str(node) == "NumberNode(123)"


def test_number_node_float():
    """测试浮点数节点"""
    node = NumberNode(line=1, column=0, value=3.14)
    assert node.value == 3.14
    assert str(node) == "NumberNode(3.14)"


def test_string_node():
    """测试字符串节点"""
    node = StringNode(line=1, column=0, value="你好")
    assert node.value == "你好"
    assert str(node) == "StringNode('你好')"


def test_identifier_node():
    """测试标识符节点"""
    node = IdentifierNode(line=1, column=0, name="变量名")
    assert node.name == "变量名"
    assert str(node) == "IdentifierNode(变量名)"


# ============ 表达式节点测试 ============

def test_binary_op_node():
    """测试二元操作节点"""
    left = NumberNode(line=1, column=0, value=1)
    right = NumberNode(line=1, column=2, value=2)
    node = BinaryOpNode(line=1, column=1, left=left, operator="+", right=right)
    assert node.operator == "+"
    assert node.left == left
    assert node.right == right
    assert str(node) == "BinaryOpNode(NumberNode(1) + NumberNode(2))"


def test_unary_op_node():
    """测试一元操作节点"""
    operand = NumberNode(line=1, column=1, value=5)
    node = UnaryOpNode(line=1, column=0, operator="-", operand=operand)
    assert node.operator == "-"
    assert node.operand == operand
    assert str(node) == "UnaryOpNode(-NumberNode(5))"


def test_list_node():
    """测试列表节点"""
    elem1 = NumberNode(line=1, column=0, value=1)
    elem2 = NumberNode(line=1, column=2, value=2)
    node = ListNode(line=1, column=0, elements=[elem1, elem2])
    assert len(node.elements) == 2
    assert str(node) == "ListNode([NumberNode(1), NumberNode(2)])"


def test_list_node_empty():
    """测试空列表节点"""
    node = ListNode(line=1, column=0, elements=[])
    assert len(node.elements) == 0
    assert str(node) == "ListNode([])"


def test_dict_node():
    """测试字典节点"""
    key = StringNode(line=1, column=0, value="键")
    value = NumberNode(line=1, column=2, value=1)
    node = DictNode(line=1, column=0, pairs=[(key, value)])
    assert len(node.pairs) == 1
    assert str(node) == "DictNode({StringNode('键'): NumberNode(1)})"


def test_dict_node_empty():
    """测试空字典节点"""
    node = DictNode(line=1, column=0, pairs=[])
    assert len(node.pairs) == 0
    assert str(node) == "DictNode({})"


def test_member_access_node():
    """测试成员访问节点"""
    obj = IdentifierNode(line=1, column=0, name="对象")
    node = MemberAccessNode(line=1, column=2, obj=obj, member="属性")
    assert node.obj == obj
    assert node.member == "属性"
    assert str(node) == "MemberAccessNode(IdentifierNode(对象).属性)"


def test_index_node():
    """测试索引节点"""
    obj = IdentifierNode(line=1, column=0, name="列表")
    index = NumberNode(line=1, column=3, value=0)
    node = IndexNode(line=1, column=2, obj=obj, index=index)
    assert node.obj == obj
    assert node.index == index
    assert str(node) == "IndexNode(IdentifierNode(列表)[NumberNode(0)])"


# ============ 语句节点测试 ============

def test_assign_node():
    """测试赋值节点"""
    target = IdentifierNode(line=1, column=0, name="x")
    value = NumberNode(line=1, column=4, value=10)
    node = AssignNode(line=1, column=2, target=target, value=value)
    assert node.target == target
    assert node.value == value
    assert str(node) == "AssignNode(IdentifierNode(x) = NumberNode(10))"


def test_var_def_node_with_value():
    """测试带值的变量定义节点"""
    value = NumberNode(line=1, column=4, value=5)
    node = VarDefNode(line=1, column=0, name="x", value=value)
    assert node.name == "x"
    assert node.value == value
    assert str(node) == "VarDefNode(x = NumberNode(5))"


def test_var_def_node_without_value():
    """测试不带值的变量定义节点"""
    node = VarDefNode(line=1, column=0, name="x")
    assert node.name == "x"
    assert node.value is None
    assert str(node) == "VarDefNode(x)"


def test_if_node_with_else():
    """测试带else的条件节点"""
    condition = IdentifierNode(line=1, column=0, name="x")
    then_branch = [NumberNode(line=1, column=0, value=1)]
    else_branch = [NumberNode(line=1, column=0, value=2)]
    node = IfNode(line=1, column=0, condition=condition, then_branch=then_branch, else_branch=else_branch)
    assert node.condition == condition
    assert len(node.then_branch) == 1
    assert len(node.else_branch) == 1
    assert str(node) == "IfNode(condition=IdentifierNode(x), then=1 stmts)"


def test_if_node_without_else():
    """测试不带else的条件节点"""
    condition = IdentifierNode(line=1, column=0, name="x")
    then_branch = [NumberNode(line=1, column=0, value=1)]
    node = IfNode(line=1, column=0, condition=condition, then_branch=then_branch)
    assert node.else_branch is None


def test_for_node():
    """测试遍历循环节点"""
    iterable = IdentifierNode(line=1, column=4, name="列表")
    body = [NumberNode(line=1, column=0, value=1)]
    node = ForNode(line=1, column=0, var="x", iterable=iterable, body=body)
    assert node.var == "x"
    assert node.iterable == iterable
    assert len(node.body) == 1
    assert str(node) == "ForNode(x in IdentifierNode(列表), 1 stmts)"


def test_while_node():
    """测试当循环节点"""
    condition = IdentifierNode(line=1, column=0, name="条件")
    body = [NumberNode(line=1, column=0, value=1)]
    node = WhileNode(line=1, column=0, condition=condition, body=body)
    assert node.condition == condition
    assert len(node.body) == 1
    assert str(node) == "WhileNode(condition=IdentifierNode(条件), 1 stmts)"


def test_repeat_node():
    """测试重复节点"""
    count = NumberNode(line=1, column=0, value=10)
    body = [NumberNode(line=1, column=0, value=1)]
    node = RepeatNode(line=1, column=0, count=count, body=body)
    assert node.count == count
    assert len(node.body) == 1
    assert str(node) == "RepeatNode(NumberNode(10) times, 1 stmts)"


def test_function_def_node():
    """测试函数定义节点"""
    body = [NumberNode(line=1, column=0, value=1)]
    node = FunctionDefNode(line=1, column=0, name="函数名", params=["x", "y"], body=body)
    assert node.name == "函数名"
    assert node.params == ["x", "y"]
    assert len(node.body) == 1
    assert str(node) == "FunctionDefNode(函数名(x, y), 1 stmts)"


def test_function_def_node_no_params():
    """测试无参数函数定义节点"""
    body = [NumberNode(line=1, column=0, value=1)]
    node = FunctionDefNode(line=1, column=0, name="函数名", params=[], body=body)
    assert node.params == []
    assert str(node) == "FunctionDefNode(函数名(), 1 stmts)"


def test_function_call_node():
    """测试函数调用节点"""
    arg1 = NumberNode(line=1, column=0, value=1)
    arg2 = NumberNode(line=1, column=2, value=2)
    node = FunctionCallNode(line=1, column=0, name="函数名", args=[arg1, arg2])
    assert node.name == "函数名"
    assert len(node.args) == 2
    assert str(node) == "FunctionCallNode(函数名(NumberNode(1), NumberNode(2)))"


def test_function_call_node_no_args():
    """测试无参数函数调用节点"""
    node = FunctionCallNode(line=1, column=0, name="函数名", args=[])
    assert len(node.args) == 0
    assert str(node) == "FunctionCallNode(函数名())"


def test_return_node_with_value():
    """测试带返回值的返回节点"""
    value = NumberNode(line=1, column=0, value=42)
    node = ReturnNode(line=1, column=0, value=value)
    assert node.value == value
    assert str(node) == "ReturnNode(NumberNode(42))"


def test_return_node_without_value():
    """测试不带返回值的返回节点"""
    node = ReturnNode(line=1, column=0)
    assert node.value is None
    assert str(node) == "ReturnNode()"


# ============ 特殊节点测试 ============

def test_program_node():
    """测试程序根节点"""
    stmt1 = NumberNode(line=1, column=0, value=1)
    stmt2 = NumberNode(line=1, column=0, value=2)
    node = ProgramNode(line=1, column=0, statements=[stmt1, stmt2])
    assert len(node.statements) == 2
    assert str(node) == "ProgramNode(2 statements)"


def test_program_node_empty():
    """测试空程序根节点"""
    node = ProgramNode(line=1, column=0, statements=[])
    assert len(node.statements) == 0
    assert str(node) == "ProgramNode(0 statements)"


def test_block_node():
    """测试代码块节点"""
    stmt1 = NumberNode(line=1, column=0, value=1)
    stmt2 = NumberNode(line=1, column=0, value=2)
    node = BlockNode(line=1, column=0, statements=[stmt1, stmt2])
    assert len(node.statements) == 2
    assert str(node) == "BlockNode(2 statements)"


def test_block_node_empty():
    """测试空代码块节点"""
    node = BlockNode(line=1, column=0, statements=[])
    assert len(node.statements) == 0
    assert str(node) == "BlockNode(0 statements)"


# ============ 复杂场景测试 ============

def test_nested_binary_op():
    """测试嵌套二元操作"""
    # 1 + 2 * 3
    one = NumberNode(line=1, column=0, value=1)
    two = NumberNode(line=1, column=4, value=2)
    three = NumberNode(line=1, column=8, value=3)
    multiply = BinaryOpNode(line=1, column=6, left=two, operator="*", right=three)
    add = BinaryOpNode(line=1, column=2, left=one, operator="+", right=multiply)
    assert add.left == one
    assert add.right == multiply


def test_nested_if():
    """测试嵌套条件"""
    # 若 x 则 若 y 则 1 否则 2 否则 3
    x = IdentifierNode(line=1, column=0, name="x")
    y = IdentifierNode(line=1, column=0, name="y")
    inner_if = IfNode(
        line=2, column=0,
        condition=y,
        then_branch=[NumberNode(line=2, column=0, value=1)],
        else_branch=[NumberNode(line=2, column=0, value=2)]
    )
    outer_if = IfNode(
        line=1, column=0,
        condition=x,
        then_branch=[inner_if],
        else_branch=[NumberNode(line=1, column=0, value=3)]
    )
    assert len(outer_if.then_branch) == 1
    assert isinstance(outer_if.then_branch[0], IfNode)


def test_function_with_nested_body():
    """测试带嵌套语句的函数"""
    # 函 阶乘 n：
    #   若 n 小等 1 则 返回 1
    #   否则 返回 n 乘 阶乘 n 减 1
    n = IdentifierNode(line=1, column=0, name="n")
    one = NumberNode(line=1, column=0, value=1)
    
    condition = BinaryOpNode(line=2, column=0, left=n, operator="<=", right=one)
    return1 = ReturnNode(line=2, column=0, value=one)
    if_stmt = IfNode(line=2, column=0, condition=condition, then_branch=[return1])
    
    func = FunctionDefNode(line=1, column=0, name="阶乘", params=["n"], body=[if_stmt])
    assert func.name == "阶乘"
    assert len(func.body) == 1


# ============ 语法分析器测试 ============

import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser, ParseError


class TestParserBasic:
    """基础解析测试"""
    
    def test_parse_empty_program(self):
        """测试空程序"""
        lexer = Lexer("")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 0
    
    def test_parse_number(self):
        """测试数字解析"""
        lexer = Lexer("42")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], NumberNode)
        assert ast.statements[0].value == 42
    
    def test_parse_string(self):
        """测试字符串解析"""
        lexer = Lexer('"你好世界"')
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], StringNode)
        assert ast.statements[0].value == "你好世界"
    
    def test_parse_identifier(self):
        """测试标识符解析"""
        lexer = Lexer("变量名")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], IdentifierNode)
        assert ast.statements[0].name == "变量名"


class TestParserExpression:
    """表达式解析测试"""
    
    def test_parse_binary_add(self):
        """测试加法表达式"""
        lexer = Lexer("1 加 2")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        expr = ast.statements[0]
        assert isinstance(expr, BinaryOpNode)
        assert expr.operator == "+"
        assert expr.left.value == 1
        assert expr.right.value == 2
    
    def test_parse_binary_subtract(self):
        """测试减法表达式"""
        lexer = Lexer("5 减 3")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        expr = ast.statements[0]
        assert isinstance(expr, BinaryOpNode)
        assert expr.operator == "-"
    
    def test_parse_binary_multiply(self):
        """测试乘法表达式"""
        lexer = Lexer("3 乘 4")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        expr = ast.statements[0]
        assert isinstance(expr, BinaryOpNode)
        assert expr.operator == "*"
    
    def test_parse_binary_divide(self):
        """测试除法表达式"""
        lexer = Lexer("10 除 2")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        expr = ast.statements[0]
        assert isinstance(expr, BinaryOpNode)
        assert expr.operator == "/"
    
    def test_parse_comparison_equals(self):
        """测试相等比较"""
        lexer = Lexer("x 等 5")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        expr = ast.statements[0]
        assert isinstance(expr, BinaryOpNode)
        assert expr.operator == "=="
    
    def test_parse_comparison_less(self):
        """测试小于比较"""
        lexer = Lexer("a 小 b")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        expr = ast.statements[0]
        assert isinstance(expr, BinaryOpNode)
        assert expr.operator == "<"
    
    def test_parse_unary_not(self):
        """测试逻辑非"""
        lexer = Lexer("非 真")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        expr = ast.statements[0]
        assert isinstance(expr, UnaryOpNode)
        assert expr.operator == "not"
    
    def test_parse_unary_negative(self):
        """测试负号"""
        lexer = Lexer("-5")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        expr = ast.statements[0]
        assert isinstance(expr, UnaryOpNode)
        assert expr.operator == "-"
    
    def test_parse_parentheses(self):
        """测试括号表达式"""
        lexer = Lexer("（1 加 2）")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        expr = ast.statements[0]
        assert isinstance(expr, BinaryOpNode)
        assert expr.operator == "+"
    
    def test_parse_operator_precedence(self):
        """测试运算符优先级：1 加 2 乘 3 应该解析为 1 + (2 * 3)"""
        lexer = Lexer("1 加 2 乘 3")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        expr = ast.statements[0]
        assert isinstance(expr, BinaryOpNode)
        assert expr.operator == "+"
        assert isinstance(expr.right, BinaryOpNode)
        assert expr.right.operator == "*"
    
    def test_parse_logical_and(self):
        """测试逻辑与操作"""
        lexer = Lexer("x 且 y")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        expr = ast.statements[0]
        assert isinstance(expr, BinaryOpNode)
        assert expr.operator == "and"
    
    def test_parse_logical_or(self):
        """测试逻辑或操作"""
        lexer = Lexer("x 或 y")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        expr = ast.statements[0]
        assert isinstance(expr, BinaryOpNode)
        assert expr.operator == "or"
    
    def test_parse_logical_precedence(self):
        """测试逻辑操作符优先级：x 或 y 且 z 应该解析为 x 或 (y 且 z)"""
        lexer = Lexer("x 或 y 且 z")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        expr = ast.statements[0]
        assert isinstance(expr, BinaryOpNode)
        assert expr.operator == "or"
        assert isinstance(expr.right, BinaryOpNode)
        assert expr.right.operator == "and"


class TestParserStatement:
    """语句解析测试"""
    
    def test_parse_var_def(self):
        """测试变量定义"""
        lexer = Lexer("定 x = 5")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, VarDefNode)
        assert stmt.name == "x"
        assert stmt.value.value == 5
    
    def test_parse_assignment(self):
        """测试赋值语句"""
        lexer = Lexer("x = 10")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, AssignNode)
        assert stmt.target.name == "x"
        assert stmt.value.value == 10
    
    def test_parse_function_call_no_args(self):
        """测试无参数函数调用（使用括号）"""
        lexer = Lexer("函数名（）")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, FunctionCallNode)
        assert stmt.name == "函数名"
        assert len(stmt.args) == 0
    
    def test_parse_identifier_not_call(self):
        """测试单独的标识符不是函数调用"""
        lexer = Lexer("变量名")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        # 单独的标识符应该是标识符引用，不是函数调用
        assert isinstance(stmt, IdentifierNode)
        assert stmt.name == "变量名"
    
    def test_parse_function_call_with_args(self):
        """测试带参数函数调用"""
        lexer = Lexer("函数名 1 2 3")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        stmt = ast.statements[0]
        assert isinstance(stmt, FunctionCallNode)
        assert stmt.name == "函数名"
        assert len(stmt.args) == 3


class TestParserControlFlow:
    """控制流解析测试"""
    
    def test_parse_if_then(self):
        """测试条件语句（只有then分支）"""
        source = """若 x 则
    印 1
。"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, IfNode)
        assert isinstance(stmt.condition, IdentifierNode)
        assert stmt.condition.name == "x"
        assert len(stmt.then_branch) == 1
        assert stmt.else_branch is None
    
    def test_parse_if_then_else(self):
        """测试条件语句（带else分支）"""
        source = """若 x 则
    印 1
否则
    印 2
。"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        stmt = ast.statements[0]
        assert isinstance(stmt, IfNode)
        assert len(stmt.then_branch) == 1
        assert len(stmt.else_branch) == 1
    
    def test_parse_for_loop(self):
        """测试遍历循环"""
        source = """遍历 x 于 列表：
    印 x
。"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, ForNode)
        assert stmt.var == "x"
        assert isinstance(stmt.iterable, IdentifierNode)
        assert len(stmt.body) == 1
    
    def test_parse_while_loop(self):
        """测试当循环"""
        source = """当 条件：
    印 1
。"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, WhileNode)
        assert isinstance(stmt.condition, IdentifierNode)
        assert len(stmt.body) == 1
    
    def test_parse_repeat(self):
        """测试重复语句"""
        source = """重复 5 次：
    印 1
。"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, RepeatNode)
        assert stmt.count.value == 5
        assert len(stmt.body) == 1


class TestParserFunction:
    """函数解析测试"""
    
    def test_parse_function_def_no_params(self):
        """测试无参数函数定义"""
        source = """定 函数名 = 函：
    返回 1
。"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        # 函数定义是通过变量定义实现的
        stmt = ast.statements[0]
        assert isinstance(stmt, VarDefNode)
        assert stmt.name == "函数名"
        assert isinstance(stmt.value, FunctionDefNode)
        assert len(stmt.value.params) == 0
        assert len(stmt.value.body) == 1
    
    def test_parse_function_def_with_params(self):
        """测试带参数函数定义"""
        source = """定 加法 = 函 x y：
    返回 x 加 y
。"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        stmt = ast.statements[0]
        assert isinstance(stmt, VarDefNode)
        assert stmt.name == "加法"
        assert isinstance(stmt.value, FunctionDefNode)
        assert stmt.value.params == ["x", "y"]
        assert len(stmt.value.body) == 1
    
    def test_parse_return_with_value(self):
        """测试带返回值的返回语句"""
        source = "返回 42"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, ReturnNode)
        assert stmt.value.value == 42
    
    def test_parse_return_without_value(self):
        """测试不带返回值的返回语句"""
        source = "返回"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, ReturnNode)
        assert stmt.value is None


class TestParserError:
    """错误处理测试"""
    
    def test_parse_error_unexpected_token(self):
        """测试意外的token错误"""
        lexer = Lexer("定 = 5")  # 缺少变量名
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        with pytest.raises(ParseError):
            parser.parse()
    
    def test_parse_error_missing_colon(self):
        """测试缺少冒号错误"""
        source = """遍历 x 于 列表
    印 x
。"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        
        with pytest.raises(ParseError):
            parser.parse()


class TestParserComplex:
    """复杂场景测试"""
    
    def test_parse_multiple_statements(self):
        """测试多个语句"""
        source = """定 x = 1
定 y = 2
印 x 加 y"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 3
    
    def test_parse_nested_if(self):
        """测试嵌套条件"""
        source = """若 x 则
    若 y 则
        印 1
    。
。"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        stmt = ast.statements[0]
        assert isinstance(stmt, IfNode)
        assert isinstance(stmt.then_branch[0], IfNode)
    
    def test_parse_function_in_function(self):
        """测试函数内定义函数"""
        source = """定 外层 = 函：
    定 内层 = 函：
        返回 1
    。
    返回 内层
。"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        assert isinstance(ast, ProgramNode)
        stmt = ast.statements[0]
        # 外层是 VarDefNode，值是 FunctionDefNode
        assert isinstance(stmt, VarDefNode)
        assert isinstance(stmt.value, FunctionDefNode)
        # 函数体内第一个语句是 VarDefNode
        assert isinstance(stmt.value.body[0], VarDefNode)
        # 内层函数定义
        assert isinstance(stmt.value.body[0].value, FunctionDefNode)
