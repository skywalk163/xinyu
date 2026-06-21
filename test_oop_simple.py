#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""简单测试OOP解析器"""

import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 直接测试我们的实现
print("=== 测试OOP关键字和AST节点 ===")

# 测试TokenType
from src.lexer.tokens import TokenType

print("1. 检查TokenType:")
print(f"  CLASS: {TokenType.CLASS}")
print(f"  EXTENDS: {TokenType.EXTENDS}")
print(f"  IMPLEMENTS: {TokenType.IMPLEMENTS}")
print(f"  NEW: {TokenType.NEW}")
print(f"  THIS: {TokenType.THIS}")
print(f"  STATIC: {TokenType.STATIC}")
print(f"  INTERFACE: {TokenType.INTERFACE}")
print(f"  SUPER: {TokenType.SUPER}")
print(f"  EXPORT: {TokenType.EXPORT}")

# 测试keywords.py
from src.lexer.keywords import ALL_KEYWORDS

print("\n2. 检查关键字映射:")
print(f"  '类' -> {ALL_KEYWORDS.get('类')}")
print(f"  '继承' -> {ALL_KEYWORDS.get('继承')}")
print(f"  '实现' -> {ALL_KEYWORDS.get('实现')}")
print(f"  '新建' -> {ALL_KEYWORDS.get('新建')}")
print(f"  '自身' -> {ALL_KEYWORDS.get('自身')}")
print(f"  '静态' -> {ALL_KEYWORDS.get('静态')}")
print(f"  '接口' -> {ALL_KEYWORDS.get('接口')}")
print(f"  '父类' -> {ALL_KEYWORDS.get('父类')}")
print(f"  '导出' -> {ALL_KEYWORDS.get('导出')}")

# 测试AST节点
from src.parser.ast_nodes import (
    ClassNode,
    ExportNode,
    InterfaceNode,
    MethodNode,
    NewNode,
    PropertyNode,
    SuperNode,
    ThisNode,
)

print("\n3. 检查AST节点:")
print(f"  ClassNode: {ClassNode}")
print(f"  InterfaceNode: {InterfaceNode}")
print(f"  MethodNode: {MethodNode}")
print(f"  PropertyNode: {PropertyNode}")
print(f"  NewNode: {NewNode}")
print(f"  ThisNode: {ThisNode}")
print(f"  SuperNode: {SuperNode}")
print(f"  ExportNode: {ExportNode}")

# 测试解析器导入
print("\n4. 检查解析器导入:")
try:
    from src.parser.parser import Parser

    print("  Parser导入成功")

    # 检查Parser是否有新的解析方法
    parser_methods = [m for m in dir(Parser) if m.startswith("_parse_")]
    new_methods = [
        m
        for m in parser_methods
        if m
        in [
            "_parse_class_definition",
            "_parse_interface_definition",
            "_parse_export",
            "_parse_class_body",
            "_parse_class_member",
            "_parse_constructor",
            "_parse_method_definition",
            "_parse_property_definition",
            "_parse_interface_body",
            "_parse_interface_method",
        ]
    ]

    print(f"  找到 {len(new_methods)} 个新的解析方法:")
    for method in new_methods:
        print(f"    - {method}")

except ImportError as e:
    print(f"  Parser导入失败: {e}")

# 测试代码生成器导入
print("\n5. 检查代码生成器导入:")
try:
    from src.codegen.python_codegen import PythonCodegen

    print("  PythonCodegen导入成功")

    # 检查PythonCodegen是否有新的生成方法
    codegen_methods = [m for m in dir(PythonCodegen) if m.startswith("_generate_")]
    new_generate_methods = [
        m
        for m in codegen_methods
        if m
        in [
            "_generate_class",
            "_generate_interface",
            "_generate_interface_method",
            "_generate_method",
            "_generate_property",
            "_generate_new",
            "_generate_this",
            "_generate_super",
            "_generate_export",
        ]
    ]

    print(f"  找到 {len(new_generate_methods)} 个新的生成方法:")
    for method in new_generate_methods:
        print(f"    - {method}")

except ImportError as e:
    print(f"  PythonCodegen导入失败: {e}")

print("\n=== 测试完成 ===")
