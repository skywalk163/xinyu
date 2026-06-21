#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试OOP解析器"""

import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.error_handling import ErrorHandler
from src.lexer.lexer_with_error_handler import LexerWithErrorHandler
from src.parser.parser_with_error_handler import ParserWithErrorHandler


def test_oop_parser():
    """测试OOP解析器"""
    print("=== 测试OOP解析器 ===")

    # 测试代码
    test_code = """
定义 类 动物：
    定义 名字 = ""。
    定义 年龄 = 0。

    函数 初始化(参数 名字, 参数 年龄)：
        自身.名字 = 名字。
        自身.年龄 = 年龄。
    。

    函数 叫()：
        返回 "动物叫声"。
    。
。

定义 我的宠物 = 新建 动物("小白", 3)。
打印 我的宠物.名字。
打印 我的宠物.叫()。
"""

    print("测试代码：")
    print(test_code)
    print("\n" + "=" * 50 + "\n")

    # 创建错误处理器
    error_handler = ErrorHandler()

    # 词法分析
    print("1. 词法分析...")
    lexer = LexerWithErrorHandler(test_code, error_handler)
    tokens = list(lexer.tokenize())

    print(f"生成 {len(tokens)} 个token")
    for i, token in enumerate(tokens[:10]):  # 只显示前10个token
        print(f"  {i}: {token.type.name} = {repr(token.value)}")
    if len(tokens) > 10:
        print(f"  ... 还有 {len(tokens)-10} 个token")

    # 语法分析
    print("\n2. 语法分析...")
    parser = ParserWithErrorHandler(tokens, error_handler)
    ast = parser.parse()

    if error_handler.has_errors():
        print("解析错误：")
        for error in error_handler.get_errors():
            print(f"  {error}")
    else:
        print("解析成功！")
        print(f"AST根节点：{ast}")

        # 显示AST结构
        print("\n3. AST结构：")
        _print_ast(ast, 0)

    print("\n" + "=" * 50)


def _print_ast(node, indent=0):
    """递归打印AST结构"""
    indent_str = "  " * indent
    print(f"{indent_str}{node}")

    # 递归打印子节点
    if hasattr(node, "statements"):
        for stmt in node.statements:
            _print_ast(stmt, indent + 1)
    elif hasattr(node, "body"):
        for stmt in node.body:
            _print_ast(stmt, indent + 1)
    elif hasattr(node, "members"):
        for member in node.members:
            _print_ast(member, indent + 1)
    elif hasattr(node, "methods"):
        for method in node.methods:
            _print_ast(method, indent + 1)
    elif hasattr(node, "left") and hasattr(node, "right"):
        print(f"{indent_str}  left: {node.left}")
        print(f"{indent_str}  right: {node.right}")
    elif hasattr(node, "operand"):
        print(f"{indent_str}  operand: {node.operand}")
    elif hasattr(node, "value"):
        print(f"{indent_str}  value: {node.value}")


def test_export_parser():
    """测试导出语句解析"""
    print("\n=== 测试导出语句解析 ===")

    test_code = """
导出 动物, 狗, 猫。
导出 我的宠物 为 宠物。
"""

    print("测试代码：")
    print(test_code)

    error_handler = ErrorHandler()
    lexer = LexerWithErrorHandler(test_code, error_handler)
    tokens = list(lexer.tokenize())

    parser = ParserWithErrorHandler(tokens, error_handler)
    ast = parser.parse()

    if error_handler.has_errors():
        print("解析错误：")
        for error in error_handler.get_errors():
            print(f"  {error}")
    else:
        print("解析成功！")
        _print_ast(ast, 0)


def test_interface_parser():
    """测试接口解析"""
    print("\n=== 测试接口解析 ===")

    test_code = """
定义 接口 可发声：
    函数 发声()。
。

定义 类 猫 实现 可发声：
    函数 发声()：
        返回 "喵喵"。
    。
。
"""

    print("测试代码：")
    print(test_code)

    error_handler = ErrorHandler()
    lexer = LexerWithErrorHandler(test_code, error_handler)
    tokens = list(lexer.tokenize())

    parser = ParserWithErrorHandler(tokens, error_handler)
    ast = parser.parse()

    if error_handler.has_errors():
        print("解析错误：")
        for error in error_handler.get_errors():
            print(f"  {error}")
    else:
        print("解析成功！")
        _print_ast(ast, 0)


if __name__ == "__main__":
    test_oop_parser()
    test_export_parser()
    test_interface_parser()
