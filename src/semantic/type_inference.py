# -*- coding: utf-8 -*-
"""类型推断系统

实现类型推断功能：
- 基础类型推断（数字、字符串、布尔值）
- 表达式类型推断
- 函数返回类型推断
- 类型规则检查
"""

from typing import Dict, Optional
from src.parser.ast_nodes import (
    ASTNode, NumberNode, StringNode,
    IdentifierNode, BinaryOpNode, UnaryOpNode, FunctionCallNode,
    ListNode, DictNode
)


class TypeInferencer:
    """类型推断器"""

    def __init__(self):
        """初始化类型推断器"""
        # 类型规则： (左类型, 操作符, 右类型) -> 结果类型
        self.type_rules = {
            # 算术运算（双字）
            ('number', '+', 'number'): 'number',
            ('number', '-', 'number'): 'number',
            ('number', '*', 'number'): 'number',
            ('number', '/', 'number'): 'number',
            ('number', '相加', 'number'): 'number',
            ('number', '相减', 'number'): 'number',
            ('number', '相乘', 'number'): 'number',
            ('number', '相除', 'number'): 'number',
            ('number', '取余', 'number'): 'number',

            # 字符串连接（双字）
            ('string', '+', 'string'): 'string',
            ('string', '相加', 'string'): 'string',

            # 比较运算（双字）
            ('number', '==', 'number'): 'boolean',
            ('number', '!=', 'number'): 'boolean',
            ('number', '<', 'number'): 'boolean',
            ('number', '>', 'number'): 'boolean',
            ('number', '<=', 'number'): 'boolean',
            ('number', '>=', 'number'): 'boolean',
            ('number', '等于', 'number'): 'boolean',
            ('number', '不等', 'number'): 'boolean',
            ('number', '小于', 'number'): 'boolean',
            ('number', '大于', 'number'): 'boolean',
            ('number', '小等', 'number'): 'boolean',
            ('number', '大等', 'number'): 'boolean',

            # 逻辑运算（双字）
            ('boolean', 'and', 'boolean'): 'boolean',
            ('boolean', 'or', 'boolean'): 'boolean',
            ('boolean', '并且', 'boolean'): 'boolean',
            ('boolean', '或者', 'boolean'): 'boolean',
        }

        # 内置函数返回类型（双字）
        self.builtin_returns = {
            '打印': None,  # print函数无返回值
            '读取': 'string',  # input返回字符串
            '输入': 'string',  # input返回字符串
            '输出': None,  # output无返回值
            '写入': None,  # write无返回值
            '长度': 'number',  # len返回数字
            '求和': 'number',  # sum返回数字
            '最大': 'number',  # max返回数字
            '最小': 'number',  # min返回数字
            '排序': 'list',  # sorted返回列表
            '映射': 'list',  # map返回列表
            '过滤': 'list',  # filter返回列表
            '反转': 'list',  # reverse返回列表
            '范围': 'list',  # range返回列表
        }

    def infer(self, node: ASTNode, context: Optional[Dict[str, str]] = None) -> str:
        """推断AST节点的类型

        Args:
            node: AST节点
            context: 类型上下文（变量名 -> 类型）

        Returns:
            推断的类型字符串
        """
        if context is None:
            context = {}

        # 数字字面量
        if isinstance(node, NumberNode):
            return 'number'

        # 字符串字面量
        if isinstance(node, StringNode):
            return 'string'

        # 标识符
        if isinstance(node, IdentifierNode):
            # 特殊处理布尔值（双字）
            if node.name in ['真值', '假值']:
                return 'boolean'
            return context.get(node.name, 'unknown')

        # 二元运算
        if isinstance(node, BinaryOpNode):
            left_type = self.infer(node.left, context)
            right_type = self.infer(node.right, context)
            operator = node.operator

            # 查找类型规则
            result = self.type_rules.get((left_type, operator, right_type))
            if result:
                return result

            # 特殊处理：数字和字符串的加法（双字）
            if operator in ['+', '相加']:
                if left_type == 'number' and right_type == 'number':
                    return 'number'
                if left_type == 'string' or right_type == 'string':
                    return 'string'

            return 'unknown'

        # 一元运算
        if isinstance(node, UnaryOpNode):
            operand_type = self.infer(node.operand, context)
            operator = node.operator

            # 逻辑非（双字）
            if operator in ['not', '非也']:
                return 'boolean'

            # 负号
            if operator in ['-', '负']:
                if operand_type == 'number':
                    return 'number'

            return 'unknown'

        # 函数调用
        if isinstance(node, FunctionCallNode):
            return self._infer_function_return_type(node, context)

        # 列表
        if isinstance(node, ListNode):
            return 'list'

        # 字典
        if isinstance(node, DictNode):
            return 'dict'

        return 'unknown'

    def _infer_function_return_type(self, node: FunctionCallNode, context: Dict[str, str]) -> str:
        """推断函数调用的返回类型

        Args:
            node: 函数调用节点
            context: 类型上下文

        Returns:
            返回类型字符串
        """
        # 获取函数名
        if isinstance(node.name, IdentifierNode):
            func_name = node.name.name
        else:
            func_name = str(node.name)

        # 检查内置函数
        if func_name in self.builtin_returns:
            return self.builtin_returns[func_name]

        # 检查上下文中的用户定义函数
        # TODO: 从符号表中获取函数返回类型

        return 'unknown'

    def check_type_compatibility(self, expected_type: str, actual_type: str) -> bool:
        """检查类型兼容性

        Args:
            expected_type: 期望类型
            actual_type: 实际类型

        Returns:
            是否兼容
        """
        # 相同类型
        if expected_type == actual_type:
            return True

        # unknown类型可以与任何类型兼容
        if expected_type == 'unknown' or actual_type == 'unknown':
            return True

        # 其他情况不兼容
        return False
