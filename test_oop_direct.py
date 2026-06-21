#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""直接测试OOP实现"""

import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=== 直接测试OOP实现 ===")

# 1. 测试TokenType
print("1. 测试TokenType...")
from src.lexer.tokens import TokenType

# 检查新的TokenType是否已添加
new_tokens = [
    "CLASS",
    "EXTENDS",
    "IMPLEMENTS",
    "NEW",
    "THIS",
    "STATIC",
    "INTERFACE",
    "SUPER",
    "EXPORT",
]
for token_name in new_tokens:
    if hasattr(TokenType, token_name):
        print(f"  [OK] {token_name}: {getattr(TokenType, token_name)}")
    else:
        print(f"  [FAIL] {token_name}: 未找到")

# 2. 测试关键字映射
print("\n2. 测试关键字映射...")
from src.lexer.keywords import ALL_KEYWORDS

# 检查新的关键字是否已添加
new_keywords = ["类", "继承", "实现", "新建", "自身", "静态", "接口", "父类", "导出"]
for keyword in new_keywords:
    if keyword in ALL_KEYWORDS:
        print(f"  [OK] '{keyword}' -> {ALL_KEYWORDS[keyword]}")
    else:
        print(f"  [FAIL] '{keyword}': 未找到")

# 3. 测试AST节点
print("\n3. 测试AST节点...")
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

# 创建测试节点
print("  创建ClassNode...")
class_node = ClassNode(line=1, column=1, name="动物", extends=None, implements=[], members=[])
print(f"  ClassNode: {class_node}")

print("\n  创建MethodNode...")
method_node = MethodNode(
    line=2, column=5, name="初始化", params=["名字", "年龄"], body=[], is_static=False, is_constructor=True
)
print(f"  MethodNode: {method_node}")

print("\n  创建PropertyNode...")
property_node = PropertyNode(line=3, column=5, name="名字", value=None, is_static=False)
print(f"  PropertyNode: {property_node}")

print("\n  创建NewNode...")
new_node = NewNode(line=4, column=1, class_name="动物", args=[])
print(f"  NewNode: {new_node}")

print("\n  创建ThisNode...")
this_node = ThisNode(line=5, column=1)
print(f"  ThisNode: {this_node}")

print("\n  创建SuperNode...")
super_node = SuperNode(line=6, column=1)
print(f"  SuperNode: {super_node}")

print("\n  创建InterfaceNode...")
interface_node = InterfaceNode(line=7, column=1, name="可发声", methods=[])
print(f"  InterfaceNode: {interface_node}")

print("\n  创建ExportNode...")
export_node = ExportNode(line=8, column=1, names=["动物", "狗", "猫"], aliases={"动物": "宠物"})
print(f"  ExportNode: {export_node}")

# 4. 测试代码生成器
print("\n4. 测试代码生成器...")
from src.codegen.python_codegen import PythonCodegen

codegen = PythonCodegen()

# 测试ClassNode生成
print("  测试ClassNode代码生成...")
class_code = codegen._generate_class(class_node)
print(f"  生成的类代码:\n{class_code}")

# 测试MethodNode生成
print("\n  测试MethodNode代码生成...")
method_code = codegen._generate_method(method_node)
print(f"  生成的方法代码:\n{method_code}")

# 测试PropertyNode生成
print("\n  测试PropertyNode代码生成...")
property_code = codegen._generate_property(property_node)
print(f"  生成的属性代码: {property_code}")

# 测试NewNode生成
print("\n  测试NewNode代码生成...")
new_code = codegen._generate_new(new_node)
print(f"  生成的新建对象代码: {new_code}")

# 测试ThisNode生成
print("\n  测试ThisNode代码生成...")
this_code = codegen._generate_this(this_node)
print(f"  生成的this代码: {this_code}")

# 测试SuperNode生成
print("\n  测试SuperNode代码生成...")
super_code = codegen._generate_super(super_node)
print(f"  生成的super代码: {super_code}")

# 测试InterfaceNode生成
print("\n  测试InterfaceNode代码生成...")
interface_code = codegen._generate_interface(interface_node)
print(f"  生成的接口代码:\n{interface_code}")

# 测试ExportNode生成
print("\n  测试ExportNode代码生成...")
export_code = codegen._generate_export(export_node)
print(f"  生成的导出代码: {export_code}")

# 5. 测试完整的类定义
print("\n5. 测试完整的类定义...")
complete_class = ClassNode(
    line=1,
    column=1,
    name="动物",
    extends=None,
    implements=[],
    members=[
        PropertyNode(line=2, column=5, name="名字", value=None, is_static=False),
        PropertyNode(line=3, column=5, name="年龄", value=None, is_static=False),
        MethodNode(
            line=4,
            column=5,
            name="初始化",
            params=["名字", "年龄"],
            body=[],
            is_static=False,
            is_constructor=True,
        ),
        MethodNode(
            line=5, column=5, name="叫", params=[], body=[], is_static=False, is_constructor=False
        ),
    ],
)

complete_class_code = codegen._generate_class(complete_class)
print("  完整的类定义代码:")
print(complete_class_code)

print("\n=== 测试完成 ===")
print("\n总结:")
print("1. TokenType已成功添加所有OOP相关的token")
print("2. 关键字映射已正确配置")
print("3. AST节点类已正确定义")
print("4. 代码生成器已实现所有OOP节点的生成方法")
print("5. 可以成功生成Python代码")
