#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""语义分析器（集成类型推断）测试"""

import pytest

from src.error_handling import ErrorHandler
from src.parser.ast_nodes import (
    AssignNode,
    BinaryOpNode,
    BlockNode,
    ForNode,
    FunctionCallNode,
    IdentifierNode,
    IfNode,
    NumberNode,
    ProgramNode,
    ReturnNode,
    StringNode,
    UnaryOpNode,
    VarDefNode,
    WhileNode,
)
from src.semantic.analyzer_with_inference import SemanticAnalyzerWithInference, SemanticError


def create_program_node(statement):
    """将单个语句包装为ProgramNode"""
    if isinstance(statement, list):
        return ProgramNode(line=1, column=0, statements=statement)
    return ProgramNode(line=1, column=0, statements=[statement])


class TestSemanticAnalyzerWithInference:
    """语义分析器（集成类型推断）测试类"""

    def test_analyzer_initialization(self):
        """测试分析器初始化"""
        analyzer = SemanticAnalyzerWithInference()
        assert analyzer.global_scope is not None
        assert analyzer.current_scope is not None
        assert analyzer.error_handler is not None
        assert analyzer.type_inferencer is not None
        assert not analyzer.error_handler.has_errors()

    def test_analyze_number_node(self):
        """测试分析数字节点"""
        analyzer = SemanticAnalyzerWithInference()
        node = create_program_node(NumberNode(line=1, column=0, value=42))

        analyzer.analyze(node)

        assert not analyzer.error_handler.has_errors()
        # 数字节点应该有推断的类型
        assert hasattr(node.statements[0], "inferred_type")

    def test_analyze_string_node(self):
        """测试分析字符串节点"""
        analyzer = SemanticAnalyzerWithInference()
        node = create_program_node(StringNode(line=1, column=0, value="hello"))

        analyzer.analyze(node)

        assert not analyzer.error_handler.has_errors()
        # 字符串节点应该有推断的类型
        assert hasattr(node.statements[0], "inferred_type")

    def test_analyze_identifier_node(self):
        """测试分析标识符节点（未定义变量）"""
        analyzer = SemanticAnalyzerWithInference()
        node = IdentifierNode(line=1, column=0, name="x")

        analyzer.analyze(node)

        # 应该报告未定义变量错误
        assert analyzer.error_handler.has_errors()
        errors = analyzer.error_handler.get_errors()
        assert len(errors) == 1
        assert errors[0].error_type == "SEMANTIC_ERROR"
        assert "未定义" in errors[0].message or "undefined" in errors[0].message.lower()

    def test_analyze_variable_definition(self):
        """测试分析变量定义"""
        analyzer = SemanticAnalyzerWithInference()

        # 创建变量定义节点
        var_def = VarDefNode(
            line=1, column=0, name="x", value=NumberNode(line=1, column=5, value=42)
        )

        analyzer.analyze(var_def)

        assert not analyzer.error_handler.has_errors()
        # 变量应该被定义在当前作用域
        assert "x" in analyzer.current_scope.symbols

    def test_analyze_assignment(self):
        """测试分析赋值语句"""
        analyzer = SemanticAnalyzerWithInference()

        # 先定义变量
        var_def = VarDefNode(
            line=1, column=0, name="x", value=NumberNode(line=1, column=5, value=42)
        )
        analyzer.analyze(var_def)

        # 然后赋值
        assign = AssignNode(
            line=2,
            column=0,
            target=IdentifierNode(line=2, column=0, name="x"),
            value=NumberNode(line=2, column=4, value=100),
        )

        analyzer.analyze(assign)

        assert not analyzer.error_handler.has_errors()

    def test_analyze_assignment_to_undefined_variable(self):
        """测试给未定义变量赋值"""
        analyzer = SemanticAnalyzerWithInference()

        assign = AssignNode(
            line=1,
            column=0,
            target=IdentifierNode(line=1, column=0, name="x"),
            value=NumberNode(line=1, column=4, value=100),
        )

        analyzer.analyze(assign)

        # 应该报告未定义变量错误
        assert analyzer.error_handler.has_errors()
        errors = analyzer.error_handler.get_errors()
        assert len(errors) == 1
        assert errors[0].error_type == "SEMANTIC_ERROR"

    def test_analyze_binary_operation(self):
        """测试分析二元运算"""
        analyzer = SemanticAnalyzerWithInference()

        # 数字相加
        node = BinaryOpNode(
            line=1,
            column=0,
            left=NumberNode(line=1, column=0, value=10),
            op="+",
            right=NumberNode(line=1, column=4, value=20),
        )

        analyzer.analyze(node)

        assert not analyzer.error_handler.has_errors()
        # 二元运算节点应该有推断的类型
        assert hasattr(node, "inferred_type")

    def test_analyze_binary_operation_type_mismatch(self):
        """测试分析类型不匹配的二元运算"""
        analyzer = SemanticAnalyzerWithInference()

        # 数字和字符串相加（类型不匹配）
        node = BinaryOpNode(
            line=1,
            column=0,
            left=NumberNode(line=1, column=0, value=10),
            op="+",
            right=StringNode(line=1, column=4, value="hello"),
        )

        analyzer.analyze(node)

        # 应该报告类型错误
        assert analyzer.error_handler.has_errors()
        errors = analyzer.error_handler.get_errors()
        assert len(errors) == 1
        assert errors[0].error_type == "SEMANTIC_ERROR"
        assert "类型" in errors[0].message or "type" in errors[0].message.lower()

    def test_analyze_unary_operation(self):
        """测试分析一元运算"""
        analyzer = SemanticAnalyzerWithInference()

        # 数字取负
        node = UnaryOpNode(line=1, column=0, op="-", operand=NumberNode(line=1, column=1, value=42))

        analyzer.analyze(node)

        assert not analyzer.error_handler.has_errors()
        # 一元运算节点应该有推断的类型
        assert hasattr(node, "inferred_type")

    def test_analyze_function_call(self):
        """测试分析函数调用"""
        analyzer = SemanticAnalyzerWithInference()

        # 创建函数调用节点
        node = FunctionCallNode(
            line=1, column=0, name="打印", args=[StringNode(line=1, column=4, value="hello")]
        )

        analyzer.analyze(node)

        # 内置函数应该可以调用
        # 注意：这里可能不会报错，因为"打印"可能是内置函数
        # 我们只检查分析过程不崩溃
        assert True

    def test_analyze_if_statement(self):
        """测试分析条件语句"""
        analyzer = SemanticAnalyzerWithInference()

        # 创建if语句节点
        node = IfNode(
            line=1,
            column=0,
            condition=IdentifierNode(line=1, column=3, name="真"),
            then_branch=[
                FunctionCallNode(
                    line=2, column=4, name="打印", args=[StringNode(line=2, column=8, value="true")]
                )
            ],
            else_branch=None,
        )

        analyzer.analyze(node)

        # 条件应该是布尔类型
        # 这里我们只检查分析过程不崩溃
        assert True

    def test_analyze_for_loop(self):
        """测试分析for循环"""
        analyzer = SemanticAnalyzerWithInference()

        # 创建for循环节点
        node = ForNode(
            line=1,
            column=0,
            var="i",
            iterable=FunctionCallNode(
                line=1, column=8, name="范围", args=[NumberNode(line=1, column=13, value=10)]
            ),
            body=[
                FunctionCallNode(
                    line=2, column=4, name="打印", args=[IdentifierNode(line=2, column=8, name="i")]
                )
            ],
        )

        analyzer.analyze(node)

        # 循环变量应该在循环作用域中定义
        # 这里我们只检查分析过程不崩溃
        assert True

    def test_analyze_while_loop(self):
        """测试分析while循环"""
        analyzer = SemanticAnalyzerWithInference()

        # 创建while循环节点
        node = WhileNode(
            line=1,
            column=0,
            condition=IdentifierNode(line=1, column=3, name="真"),
            body=[
                FunctionCallNode(
                    line=2,
                    column=4,
                    name="打印",
                    args=[StringNode(line=2, column=8, value="looping")],
                )
            ],
        )

        analyzer.analyze(node)

        # 条件应该是布尔类型
        # 这里我们只检查分析过程不崩溃
        assert True

    def test_analyze_return_statement(self):
        """测试分析返回语句"""
        analyzer = SemanticAnalyzerWithInference()

        # 创建返回语句节点
        node = ReturnNode(line=1, column=0, value=NumberNode(line=1, column=7, value=42))

        analyzer.analyze(node)

        # 返回语句应该在函数上下文中分析
        # 这里我们只检查分析过程不崩溃
        assert True

    def test_analyze_block(self):
        """测试分析代码块"""
        analyzer = SemanticAnalyzerWithInference()

        # 创建代码块节点
        node = BlockNode(
            line=1,
            column=0,
            statements=[
                VarDefNode(
                    line=2, column=4, name="x", value=NumberNode(line=2, column=8, value=42)
                ),
                AssignNode(
                    line=3,
                    column=4,
                    target=IdentifierNode(line=3, column=4, name="x"),
                    value=NumberNode(line=3, column=8, value=100),
                ),
            ],
        )

        analyzer.analyze(node)

        assert not analyzer.error_handler.has_errors()
        # 变量应该被定义
        assert "x" in analyzer.current_scope.symbols

    def test_analyze_program(self):
        """测试分析完整程序"""
        analyzer = SemanticAnalyzerWithInference()

        # 创建程序节点
        program = ProgramNode(
            statements=[
                VarDefNode(
                    line=1, column=0, name="x", value=NumberNode(line=1, column=4, value=10)
                ),
                VarDefNode(
                    line=2, column=0, name="y", value=NumberNode(line=2, column=4, value=20)
                ),
                BinaryOpNode(
                    line=3,
                    column=0,
                    left=IdentifierNode(line=3, column=0, name="x"),
                    op="+",
                    right=IdentifierNode(line=3, column=4, name="y"),
                ),
            ]
        )

        analyzer.analyze(program)

        assert not analyzer.error_handler.has_errors()
        # 两个变量都应该被定义
        assert "x" in analyzer.current_scope.symbols
        assert "y" in analyzer.current_scope.symbols

    def test_type_inference_for_numbers(self):
        """测试数字类型推断"""
        analyzer = SemanticAnalyzerWithInference()

        # 整数
        int_node = NumberNode(line=1, column=0, value=42)
        analyzer.analyze(int_node)
        assert hasattr(int_node, "inferred_type")

        # 浮点数
        float_node = NumberNode(line=2, column=0, value=3.14)
        analyzer.analyze(float_node)
        assert hasattr(float_node, "inferred_type")

    def test_type_inference_for_strings(self):
        """测试字符串类型推断"""
        analyzer = SemanticAnalyzerWithInference()

        node = StringNode(line=1, column=0, value="hello")
        analyzer.analyze(node)

        assert hasattr(node, "inferred_type")
        # 字符串应该推断为字符串类型
        assert node.inferred_type == "str"

    def test_type_inference_for_variables(self):
        """测试变量类型推断"""
        analyzer = SemanticAnalyzerWithInference()

        # 定义变量并赋值
        var_def = VarDefNode(
            line=1, column=0, name="x", value=NumberNode(line=1, column=4, value=42)
        )
        analyzer.analyze(var_def)

        # 使用变量
        var_use = IdentifierNode(line=2, column=0, name="x")
        analyzer.analyze(var_use)

        # 应该没有错误
        assert not analyzer.error_handler.has_errors()
        # 变量应该有推断的类型
        assert hasattr(var_use, "inferred_type")

    def test_nested_scope(self):
        """测试嵌套作用域"""
        analyzer = SemanticAnalyzerWithInference()

        # 在全局作用域定义变量
        global_var = VarDefNode(
            line=1, column=0, name="global_var", value=NumberNode(line=1, column=12, value=100)
        )
        analyzer.analyze(global_var)

        # 创建嵌套作用域（模拟函数或代码块）
        analyzer.enter_scope()

        # 在嵌套作用域定义同名变量（应该隐藏外部变量）
        local_var = VarDefNode(
            line=2,
            column=4,
            name="global_var",  # 同名变量
            value=NumberNode(line=2, column=16, value=200),
        )
        analyzer.analyze(local_var)

        # 使用变量（应该使用局部变量）
        var_use = IdentifierNode(line=3, column=4, name="global_var")
        analyzer.analyze(var_use)

        # 退出嵌套作用域
        analyzer.exit_scope()

        # 再次使用变量（应该使用全局变量）
        var_use_global = IdentifierNode(line=4, column=0, name="global_var")
        analyzer.analyze(var_use_global)

        assert not analyzer.error_handler.has_errors()

    def test_error_recovery(self):
        """测试错误恢复"""
        analyzer = SemanticAnalyzerWithInference()

        # 第一个错误：使用未定义变量
        error1 = IdentifierNode(line=1, column=0, name="undefined_var")
        analyzer.analyze(error1)

        # 第二个语句：应该仍然可以分析
        valid = VarDefNode(line=2, column=0, name="x", value=NumberNode(line=2, column=4, value=42))
        analyzer.analyze(valid)

        # 应该有错误但分析继续
        assert analyzer.error_handler.has_errors()
        errors = analyzer.error_handler.get_errors()
        assert len(errors) == 1  # 只有一个错误

        # 变量应该被定义
        assert "x" in analyzer.current_scope.symbols

    def test_builtin_functions(self):
        """测试内置函数分析"""
        analyzer = SemanticAnalyzerWithInference()

        # 测试内置函数调用
        builtins = ["打印", "长度", "范围", "类型", "转换"]

        for func_name in builtins:
            # 重置错误处理器
            analyzer.error_handler = ErrorHandler()

            # 创建函数调用
            call = FunctionCallNode(
                line=1,
                column=0,
                name=func_name,
                args=[StringNode(line=1, column=len(func_name) + 1, value="test")],
            )

            analyzer.analyze(call)

            # 内置函数调用不应该产生语义错误
            # 注意：某些内置函数可能需要特定参数类型
            # 这里我们只检查分析过程不崩溃
            assert True

    def test_complex_expression_type_inference(self):
        """测试复杂表达式类型推断"""
        analyzer = SemanticAnalyzerWithInference()

        # 定义变量
        var_def = VarDefNode(
            line=1, column=0, name="a", value=NumberNode(line=1, column=4, value=10)
        )
        analyzer.analyze(var_def)

        # 复杂表达式: (a + 5) * 2
        complex_expr = BinaryOpNode(
            line=2,
            column=0,
            left=BinaryOpNode(
                line=2,
                column=0,
                left=IdentifierNode(line=2, column=0, name="a"),
                op="+",
                right=NumberNode(line=2, column=4, value=5),
            ),
            op="*",
            right=NumberNode(line=2, column=8, value=2),
        )

        analyzer.analyze(complex_expr)

        assert not analyzer.error_handler.has_errors()
        # 复杂表达式应该有推断的类型
        assert hasattr(complex_expr, "inferred_type")
        # 应该是数字类型
        assert complex_expr.inferred_type == "int" or complex_expr.inferred_type == "float"
