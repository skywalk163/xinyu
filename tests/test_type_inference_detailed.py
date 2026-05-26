



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细的类型推断器测试
"""

import pytest
from src.semantic.type_inference import TypeInferencer
from src.parser.ast_nodes import (
    NumberNode, StringNode, IdentifierNode, BinaryOpNode,
    UnaryOpNode, FunctionCallNode, ListNode, DictNode
)


class TestTypeInferencerDetailed:
    """详细的类型推断器测试"""

    def setup_method(self):
        """测试初始化"""
        self.inferencer = TypeInferencer()

    def test_type_rules_initialization(self):
        """测试类型规则初始化"""
        # 检查一些基本的类型规则
        assert len(self.inferencer.type_rules) > 0

        # 检查算术运算规则（双字）
        assert ('number', '+', 'number') in self.inferencer.type_rules
        assert ('number', '相加', 'number') in self.inferencer.type_rules
        assert self.inferencer.type_rules[('number', '+', 'number')] == 'number'

        # 检查比较运算规则（双字）
        assert ('number', '==', 'number') in self.inferencer.type_rules
        assert ('number', '等于', 'number') in self.inferencer.type_rules
        assert self.inferencer.type_rules[('number', '==', 'number')] == 'boolean'

        # 检查逻辑运算规则（双字）
        assert ('boolean', 'and', 'boolean') in self.inferencer.type_rules
        assert ('boolean', '并且', 'boolean') in self.inferencer.type_rules

    def test_builtin_returns_initialization(self):
        """测试内置函数返回类型初始化"""
        # 检查一些内置函数的返回类型（双字）
        assert '打印' in self.inferencer.builtin_returns
        assert self.inferencer.builtin_returns['打印'] is None

        assert '读取' in self.inferencer.builtin_returns
        assert self.inferencer.builtin_returns['读取'] == 'string'

        assert '输入' in self.inferencer.builtin_returns
        assert self.inferencer.builtin_returns['输入'] == 'string'

        assert '长度' in self.inferencer.builtin_returns
        assert self.inferencer.builtin_returns['长度'] == 'number'

    def test_infer_number_node(self):
        """测试推断NumberNode类型"""
        node = NumberNode(value=42, line=1, column=1)
        result = self.inferencer.infer(node)
        assert result == 'number'

    def test_infer_string_node(self):
        """测试推断StringNode类型"""
        node = StringNode(value="测试", line=1, column=1)
        result = self.inferencer.infer(node)
        assert result == 'string'

    def test_infer_identifier_node_with_context(self):
        """测试推断IdentifierNode类型（有上下文）"""
        node = IdentifierNode(name="x", line=1, column=1)
        
        # 没有上下文
        result = self.inferencer.infer(node)
        assert result == 'unknown'
        
        # 有上下文
        context = {"x": "number"}
        result = self.inferencer.infer(node, context)
        assert result == 'number'

    def test_infer_identifier_node_boolean_keywords(self):
        """测试推断布尔关键字IdentifierNode类型"""
        # 真
        node = IdentifierNode(name="真值", line=1, column=1)
        result = self.inferencer.infer(node)
        assert result == 'boolean'
        
        # 假
        node = IdentifierNode(name="假值", line=1, column=1)
        result = self.inferencer.infer(node)
        assert result == 'boolean'

    def test_infer_binary_op_node_arithmetic(self):
        """测试推断算术运算BinaryOpNode类型"""
        # 加法
        node = BinaryOpNode(
            left=NumberNode(value=1, line=1, column=1),
            operator="相加",
            right=NumberNode(value=2, line=1, column=4),
            line=1,
            column=1
        )
        result = self.inferencer.infer(node)
        assert result == 'number'
        
        # 减法
        node = BinaryOpNode(
            left=NumberNode(value=5, line=1, column=1),
            operator="相减",
            right=NumberNode(value=3, line=1, column=4),
            line=1,
            column=1
        )
        result = self.inferencer.infer(node)
        assert result == 'number'

    def test_infer_binary_op_node_comparison(self):
        """测试推断比较运算BinaryOpNode类型"""
        # 小于
        node = BinaryOpNode(
            left=NumberNode(value=1, line=1, column=1),
            operator="小于",
            right=NumberNode(value=2, line=1, column=4),
            line=1,
            column=1
        )
        result = self.inferencer.infer(node)
        assert result == 'boolean'
        
        # 等于
        node = BinaryOpNode(
            left=NumberNode(value=1, line=1, column=1),
            operator="等于",
            right=NumberNode(value=1, line=1, column=4),
            line=1,
            column=1
        )
        result = self.inferencer.infer(node)
        assert result == 'boolean'

    def test_infer_binary_op_node_logical(self):
        """测试推断逻辑运算BinaryOpNode类型"""
        # 逻辑与
        node = BinaryOpNode(
            left=IdentifierNode(name="真值", line=1, column=1),
            operator="并且",
            right=IdentifierNode(name="假值", line=1, column=4),
            line=1,
            column=1
        )
        result = self.inferencer.infer(node)
        assert result == 'boolean'

    def test_infer_binary_op_node_string_concat(self):
        """测试推断字符串连接BinaryOpNode类型"""
        # 字符串连接
        node = BinaryOpNode(
            left=StringNode(value="a", line=1, column=1),
            operator="相加",
            right=StringNode(value="b", line=1, column=5),
            line=1,
            column=1
        )
        result = self.inferencer.infer(node)
        assert result == 'string'

    def test_infer_binary_op_node_mixed_types(self):
        """测试推断混合类型BinaryOpNode类型"""
        # 数字加字符串（应为字符串）
        node = BinaryOpNode(
            left=NumberNode(value=1, line=1, column=1),
            operator="相加",
            right=StringNode(value="b", line=1, column=4),
            line=1,
            column=1
        )
        result = self.inferencer.infer(node)
        assert result == 'string'
        
        # 字符串加数字（应为字符串）
        node = BinaryOpNode(
            left=StringNode(value="a", line=1, column=1),
            operator="相加",
            right=NumberNode(value=2, line=1, column=5),
            line=1,
            column=1
        )
        result = self.inferencer.infer(node)
        assert result == 'string'

    def test_infer_binary_op_node_unknown_types(self):
        """测试推断未知类型BinaryOpNode类型"""
        # 未知类型的运算
        node = BinaryOpNode(
            left=IdentifierNode(name="x", line=1, column=1),
            operator="相加",
            right=IdentifierNode(name="y", line=1, column=4),
            line=1,
            column=1
        )
        result = self.inferencer.infer(node)
        assert result == 'unknown'

    def test_infer_unary_op_node(self):
        """测试推断UnaryOpNode类型"""
        # 逻辑非
        node = UnaryOpNode(
            operator="非也",
            operand=IdentifierNode(name="真值", line=1, column=2),
            line=1,
            column=1
        )
        result = self.inferencer.infer(node)
        assert result == 'boolean'
        
        # 负号
        node = UnaryOpNode(
            operator="负",
            operand=NumberNode(value=5, line=1, column=2),
            line=1,
            column=1
        )
        result = self.inferencer.infer(node)
        assert result == 'number'
        
        # 未知操作符
        node = UnaryOpNode(
            operator="未知操作符",
            operand=NumberNode(value=5, line=1, column=6),
            line=1,
            column=1
        )
        result = self.inferencer.infer(node)
        assert result == 'unknown'

    def test_infer_function_call_node_builtin(self):
        """测试推断内置函数FunctionCallNode类型"""
        # 内置函数 印
        node = FunctionCallNode(
            name="打印",
            args=[StringNode(value="测试", line=1, column=4)],
            line=1,
            column=1
        )
        result = self.inferencer.infer(node)
        assert result is None  # 印函数无返回值
        
        # 内置函数 长度
        node = FunctionCallNode(
            name="长度",
            args=[ListNode(elements=[], line=1, column=4)],
            line=1,
            column=1
        )
        result = self.inferencer.infer(node)
        assert result == 'number'
        
        # 内置函数 读取
        node = FunctionCallNode(
            name="读取",
            args=[],
            line=1,
            column=1
        )
        result = self.inferencer.infer(node)
        assert result == 'string'

    def test_infer_function_call_node_unknown(self):
        """测试推断未知函数FunctionCallNode类型"""
        # 未知函数
        node = FunctionCallNode(
            name="未知函数",
            args=[],
            line=1,
            column=1
        )
        result = self.inferencer.infer(node)
        assert result == 'unknown'

    def test_infer_list_node(self):
        """测试推断ListNode类型"""
        node = ListNode(
            elements=[
                NumberNode(value=1, line=1, column=2),
                NumberNode(value=2, line=1, column=5),
                NumberNode(value=3, line=1, column=8)
            ],
            line=1,
            column=1
        )
        result = self.inferencer.infer(node)
        assert result == 'list'

    def test_infer_dict_node(self):
        """测试推断DictNode类型"""
        node = DictNode(
            pairs=[
                (StringNode(value="a", line=1, column=2), NumberNode(value=1, line=1, column=6))
            ],
            line=1,
            column=1
        )
        result = self.inferencer.infer(node)
        assert result == 'dict'

    def test_infer_unknown_node_type(self):
        """测试推断未知节点类型"""
        # 创建一个简单对象模拟未知节点类型
        class UnknownNode:
            pass
        
        node = UnknownNode()
        result = self.inferencer.infer(node)
        assert result == 'unknown'

    def test_infer_function_return_type_builtin(self):
        """测试推断内置函数返回类型（直接调用方法）"""
        node = FunctionCallNode(
            name="长度",
            args=[],
            line=1,
            column=1
        )
        result = self.inferencer._infer_function_return_type(node, {})
        assert result == 'number'
        
        node = FunctionCallNode(
            name="求和",
            args=[],
            line=1,
            column=1
        )
        result = self.inferencer._infer_function_return_type(node, {})
        assert result == 'number'

    def test_infer_function_return_type_identifier_name(self):
        """测试推断函数返回类型（函数名为IdentifierNode）"""
        node = FunctionCallNode(
            name=IdentifierNode(name="长度", line=1, column=1),
            args=[],
            line=1,
            column=1
        )
        result = self.inferencer._infer_function_return_type(node, {})
        assert result == 'number'

    def test_check_type_compatibility(self):
        """测试类型兼容性检查"""
        # 相同类型
        assert self.inferencer.check_type_compatibility("number", "number") == True
        assert self.inferencer.check_type_compatibility("string", "string") == True
        
        # unknown类型兼容任何类型
        assert self.inferencer.check_type_compatibility("unknown", "number") == True
        assert self.inferencer.check_type_compatibility("string", "unknown") == True
        assert self.inferencer.check_type_compatibility("unknown", "unknown") == True
        
        # 不同类型不兼容
        assert self.inferencer.check_type_compatibility("number", "string") == False
        assert self.inferencer.check_type_compatibility("string", "boolean") == False
        assert self.inferencer.check_type_compatibility("boolean", "list") == False
        
        # 边缘情况
        assert self.inferencer.check_type_compatibility("", "number") == False
        assert self.inferencer.check_type_compatibility("number", "") == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


