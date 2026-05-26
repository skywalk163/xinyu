



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细的宏展开器测试
"""

import pytest
from src.macro.macro_system import Macro, MacroSystem, MacroType
from src.macro.macro_expander import MacroExpander
from src.parser.ast_nodes import (
    ProgramNode, FunctionCallNode, IfNode, ForNode, WhileNode, RepeatNode,
    IdentifierNode, NumberNode, StringNode, VarDefNode, ReturnNode, BinaryOpNode
)


class TestMacroExpanderDetailed:
    """详细的宏展开器测试"""

    def test_expand_ast_program_node(self):
        """测试展开ProgramNode"""
        system = MacroSystem()
        expander = MacroExpander(system)
        
        # 创建简单的程序节点
        program_node = ProgramNode(
            statements=[
                VarDefNode(name="x", value=NumberNode(value=5, line=1, column=5), line=1, column=1)
            ],
            line=1,
            column=1
        )
        
        # 展开AST
        expanded = expander.expand_ast(program_node)
        
        # 验证结果
        assert isinstance(expanded, ProgramNode)
        assert len(expanded.statements) == 1
        assert isinstance(expanded.statements[0], VarDefNode)
        assert expanded.statements[0].name == "x"

    def test_expand_ast_function_call_with_macro(self):
        """测试展开宏函数调用"""
        system = MacroSystem()
        
        # 注册一个简单的宏
        macro = Macro(
            name="测试宏",
            type=MacroType.SYNTAX,
            params=["参数"],
            body="印 参数。",
            description="测试宏展开"
        )
        system.register("测试宏", macro)
        
        expander = MacroExpander(system)
        
        # 创建宏调用节点
        macro_call = FunctionCallNode(
            name="测试宏",
            args=[StringNode(value="你好", line=1, column=10)],
            line=1,
            column=1
        )
        
        # 展开宏调用
        expanded = expander.expand_ast(macro_call)
        
        # 验证展开结果
        assert isinstance(expanded, FunctionCallNode)
        assert expanded.name == "印"
        assert len(expanded.args) == 1
        assert isinstance(expanded.args[0], StringNode)
        assert expanded.args[0].value == "你好"

    def test_expand_ast_function_call_without_macro(self):
        """测试展开非宏函数调用"""
        system = MacroSystem()
        expander = MacroExpander(system)
        
        # 创建普通函数调用节点
        func_call = FunctionCallNode(
            name="打印",
            args=[StringNode(value="测试", line=1, column=8)],
            line=1,
            column=1
        )
        
        # 展开（应该保持不变）
        expanded = expander.expand_ast(func_call)
        
        # 验证结果 - 非宏函数调用应该保持不变
        assert isinstance(expanded, FunctionCallNode)
        assert expanded.name == "打印"
        assert len(expanded.args) == 1
        assert expanded.args[0].value == "测试"

    def test_expand_ast_if_node(self):
        """测试展开IfNode"""
        system = MacroSystem()
        expander = MacroExpander(system)
        
        # 创建If节点
        if_node = IfNode(
            condition=IdentifierNode(name="条件", line=1, column=3),
            then_branch=[
                FunctionCallNode(name="印", args=[StringNode(value="真", line=2, column=7)], line=2, column=1)
            ],
            else_branch=[
                FunctionCallNode(name="印", args=[StringNode(value="假", line=4, column=7)], line=4, column=1)
            ],
            line=1,
            column=1
        )
        
        # 展开AST
        expanded = expander.expand_ast(if_node)
        
        # 验证结果
        assert isinstance(expanded, IfNode)
        assert isinstance(expanded.condition, IdentifierNode)
        assert expanded.condition.name == "条件"
        assert len(expanded.then_branch) == 1
        assert len(expanded.else_branch) == 1

    def test_expand_ast_for_node_with_macro(self):
        """测试展开ForNode（有遍历宏）"""
        system = MacroSystem()
        
        # 注册遍历宏 - 使用简单的宏体
        macro = Macro(
            name="遍历",
            type=MacroType.SYNTAX,
            params=["变量", "列表", "循环体"],
            body="印 变量。印 列表。",
            description="遍历列表"
        )
        system.register("遍历", macro)
        
        expander = MacroExpander(system)
        
        # 创建For节点
        for_node = ForNode(
            var="元素",
            iterable=IdentifierNode(name="列表", line=1, column=8),
            body=[
                FunctionCallNode(name="处理", args=[IdentifierNode(name="元素", line=2, column=8)], line=2, column=1)
            ],
            line=1,
            column=1
        )
        
        # 展开AST
        expanded = expander.expand_ast(for_node)
        
        # 验证结果 - 应该被展开为列表（多个语句）
        assert isinstance(expanded, list)
        assert len(expanded) == 2  # 两个印语句

    def test_expand_ast_for_node_without_macro(self):
        """测试展开ForNode（没有遍历宏）"""
        system = MacroSystem()
        expander = MacroExpander(system)
        
        # 创建For节点
        for_node = ForNode(
            var="元素",
            iterable=IdentifierNode(name="列表", line=1, column=8),
            body=[
                FunctionCallNode(name="处理", args=[IdentifierNode(name="元素", line=2, column=8)], line=2, column=1)
            ],
            line=1,
            column=1
        )
        
        # 展开AST（没有宏，应该保持不变）
        expanded = expander.expand_ast(for_node)
        
        # 验证结果
        assert isinstance(expanded, ForNode)
        assert expanded.var == "元素"

    def test_expand_ast_while_node(self):
        """测试展开WhileNode"""
        system = MacroSystem()
        expander = MacroExpander(system)
        
        # 创建While节点
        while_node = WhileNode(
            condition=IdentifierNode(name="条件", line=1, column=5),
            body=[
                FunctionCallNode(name="执行", args=[], line=2, column=1)
            ],
            line=1,
            column=1
        )
        
        # 展开AST
        expanded = expander.expand_ast(while_node)
        
        # 验证结果
        assert isinstance(expanded, WhileNode)
        assert isinstance(expanded.condition, IdentifierNode)
        assert expanded.condition.name == "条件"
        assert len(expanded.body) == 1

    def test_expand_ast_repeat_node_with_macro(self):
        """测试展开RepeatNode（有重复宏）"""
        system = MacroSystem()
        
        # 注册重复宏 - 使用简单的宏体
        macro = Macro(
            name="重复",
            type=MacroType.SYNTAX,
            params=["次数", "循环体"],
            body="印 次数。",
            description="重复执行"
        )
        system.register("重复", macro)
        
        expander = MacroExpander(system)
        
        # 创建Repeat节点
        repeat_node = RepeatNode(
            count=NumberNode(value=5, line=1, column=6),
            body=[
                FunctionCallNode(name="执行", args=[], line=2, column=1)
            ],
            line=1,
            column=1
        )
        
        # 展开AST
        expanded = expander.expand_ast(repeat_node)
        
        # 验证结果 - 应该被展开为FunctionCallNode（单个语句）
        assert isinstance(expanded, FunctionCallNode)
        assert expanded.name == "印"

    def test_expand_ast_repeat_node_without_macro(self):
        """测试展开RepeatNode（没有重复宏）"""
        system = MacroSystem()
        expander = MacroExpander(system)
        
        # 创建Repeat节点
        repeat_node = RepeatNode(
            count=NumberNode(value=5, line=1, column=6),
            body=[
                FunctionCallNode(name="执行", args=[], line=2, column=1)
            ],
            line=1,
            column=1
        )
        
        # 展开AST（没有宏，应该保持不变）
        expanded = expander.expand_ast(repeat_node)
        
        # 验证结果
        assert isinstance(expanded, RepeatNode)
        assert isinstance(expanded.count, NumberNode)
        assert expanded.count.value == 5

    def test_expand_ast_other_nodes(self):
        """测试展开其他类型节点（直接返回）"""
        system = MacroSystem()
        expander = MacroExpander(system)
        
        # 测试NumberNode
        number_node = NumberNode(value=42, line=1, column=1)
        expanded = expander.expand_ast(number_node)
        assert expanded is number_node
        
        # 测试StringNode
        string_node = StringNode(value="测试", line=1, column=1)
        expanded = expander.expand_ast(string_node)
        assert expanded is string_node
        
        # 测试IdentifierNode
        ident_node = IdentifierNode(name="变量", line=1, column=1)
        expanded = expander.expand_ast(ident_node)
        assert expanded is ident_node

    def test_expand_macro_call_recursion_limit(self):
        """测试宏展开的递归深度限制"""
        system = MacroSystem()
        
        # 注册一个递归宏（调用自身）
        macro = Macro(
            name="递归宏",
            type=MacroType.SYNTAX,
            params=["深度"],
            body="印 深度。递归宏 深度减1。",
            description="递归宏测试"
        )
        system.register("递归宏", macro)
        
        expander = MacroExpander(system)
        expander.max_depth = 5  # 设置很小的深度限制以便测试
        
        # 创建递归宏调用
        macro_call = FunctionCallNode(
            name="递归宏",
            args=[NumberNode(value=100, line=1, column=10)],
            line=1,
            column=1
        )
        
        # 应该触发递归深度限制
        with pytest.raises(RecursionError, match="宏展开深度超过限制"):
            expander.expand_ast(macro_call)

    def test_expand_macro_call_with_args_mapping(self):
        """测试宏展开时的参数映射"""
        system = MacroSystem()
        
        # 注册带参数的宏 - 使用简单的宏体
        macro = Macro(
            name="问候",
            type=MacroType.SYNTAX,
            params=["名字", "时间"],
            body="印 名字。印 时间。",
            description="问候宏"
        )
        system.register("问候", macro)
        
        expander = MacroExpander(system)
        
        # 创建带参数的宏调用
        macro_call = FunctionCallNode(
            name="问候",
            args=[
                StringNode(value="小明", line=1, column=8),
                StringNode(value="早上", line=1, column=15)
            ],
            line=1,
            column=1
        )
        
        # 展开宏调用
        expanded = expander.expand_ast(macro_call)
        
        # 验证结果 - 宏展开后应该是一个列表（两个语句）
        assert isinstance(expanded, list)
        assert len(expanded) == 2  # 两个印语句

    def test_expand_for_loop_method(self):
        """测试_expand_for_loop方法"""
        system = MacroSystem()
        
        # 注册遍历宏 - 使用简单的宏体
        macro = Macro(
            name="遍历",
            type=MacroType.SYNTAX,
            params=["变量", "列表", "循环体"],
            body="印 变量。印 列表。",
            description="遍历列表"
        )
        system.register("遍历", macro)
        
        expander = MacroExpander(system)
        
        # 创建For节点
        for_node = ForNode(
            var="元素",
            iterable=IdentifierNode(name="列表", line=1, column=8),
            body=[
                FunctionCallNode(name="处理", args=[IdentifierNode(name="元素", line=2, column=8)], line=2, column=1)
            ],
            line=1,
            column=1
        )
        
        # 直接调用_expand_for_loop方法
        expanded = expander._expand_for_loop(for_node)
        
        # 验证结果 - 应该被展开为列表（多个语句）
        assert isinstance(expanded, list)
        assert len(expanded) == 2  # 两个印语句

    def test_expand_repeat_loop_method(self):
        """测试_expand_repeat_loop方法"""
        system = MacroSystem()
        
        # 注册重复宏 - 使用简单的宏体
        macro = Macro(
            name="重复",
            type=MacroType.SYNTAX,
            params=["次数", "循环体"],
            body="印 次数。",
            description="重复执行"
        )
        system.register("重复", macro)
        
        expander = MacroExpander(system)
        
        # 创建Repeat节点
        repeat_node = RepeatNode(
            count=NumberNode(value=3, line=1, column=6),
            body=[
                FunctionCallNode(name="执行", args=[], line=2, column=1)
            ],
            line=1,
            column=1
        )
        
        # 直接调用_expand_repeat_loop方法
        expanded = expander._expand_repeat_loop(repeat_node)
        
        # 验证结果 - 应该被展开为FunctionCallNode（单个语句）
        assert isinstance(expanded, FunctionCallNode)
        assert expanded.name == "印"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

