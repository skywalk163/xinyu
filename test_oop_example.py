#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试OOP示例文件"""

import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=== 测试OOP示例文件 ===")

# 检查示例文件是否存在
example_file = "examples/16_oop_example.心语"
if not os.path.exists(example_file):
    print(f"[ERROR] 示例文件不存在: {example_file}")
    sys.exit(1)

print(f"找到示例文件: {example_file}")

# 读取示例文件内容
with open(example_file, "r", encoding="utf-8") as f:
    content = f.read()
    print(f"文件大小: {len(content)} 字符")
    print(f"文件行数: {len(content.splitlines())}")

# 检查关键语法元素
print("\n检查关键语法元素:")

# 检查类定义
keywords_to_check = [
    ("类", "类定义"),
    ("继承", "继承关键字"),
    ("实现", "接口实现关键字"),
    ("新建", "对象创建关键字"),
    ("自身", "this关键字"),
    ("父类", "super关键字"),
    ("静态", "静态成员关键字"),
    ("接口", "接口定义关键字"),
    ("导出", "模块导出关键字"),
    ("导入", "模块导入关键字"),
]

for keyword, description in keywords_to_check:
    count = content.count(keyword)
    if count > 0:
        print(f"  [OK] {description} ('{keyword}'): {count} 次")
    else:
        print(f"  [WARN] {description} ('{keyword}'): 未找到")

# 检查具体的类定义
classes_to_check = ["动物", "狗", "猫", "数学工具", "工厂", "银行账户", "储蓄账户", "鸟", "鱼"]
for class_name in classes_to_check:
    if f"定义 类 {class_name}" in content:
        print(f"  [OK] 类定义: {class_name}")
    else:
        print(f"  [WARN] 类定义: {class_name} 未找到")

# 检查接口定义
interfaces_to_check = ["可发声", "可移动"]
for interface_name in interfaces_to_check:
    if f"定义 接口 {interface_name}" in content:
        print(f"  [OK] 接口定义: {interface_name}")
    else:
        print(f"  [WARN] 接口定义: {interface_name} 未找到")

# 检查方法定义
methods_to_check = [
    ("初始化", "构造函数"),
    ("叫", "方法"),
    ("介绍", "方法"),
    ("摇尾巴", "方法"),
    ("抓老鼠", "方法"),
    ("存款", "方法"),
    ("取款", "方法"),
    ("查询余额", "方法"),
    ("计算利息", "方法"),
    ("发声", "接口方法"),
    ("移动", "接口方法"),
]

for method_name, description in methods_to_check:
    if f"函数 {method_name}" in content:
        print(f"  [OK] 方法定义: {method_name} ({description})")
    else:
        print(f"  [WARN] 方法定义: {method_name} ({description}) 未找到")

# 检查对象创建
object_creations = [
    ("新建 动物", "动物对象创建"),
    ("新建 狗", "狗对象创建"),
    ("新建 猫", "猫对象创建"),
    ("新建 银行账户", "银行账户对象创建"),
    ("新建 储蓄账户", "储蓄账户对象创建"),
    ("新建 鸟", "鸟对象创建"),
    ("新建 鱼", "鱼对象创建"),
]

for creation, description in object_creations:
    if creation in content:
        print(f"  [OK] 对象创建: {description}")
    else:
        print(f"  [WARN] 对象创建: {description} 未找到")

# 检查继承关系
inheritance_checks = [
    ("狗 继承 动物", "狗继承动物"),
    ("猫 继承 动物", "猫继承动物"),
    ("储蓄账户 继承 银行账户", "储蓄账户继承银行账户"),
]

for inheritance, description in inheritance_checks:
    if inheritance in content:
        print(f"  [OK] 继承关系: {description}")
    else:
        print(f"  [WARN] 继承关系: {description} 未找到")

# 检查接口实现
implementation_checks = [
    ("鸟 实现 可发声, 可移动", "鸟实现接口"),
    ("鱼 实现 可发声, 可移动", "鱼实现接口"),
]

for implementation, description in implementation_checks:
    if implementation in content:
        print(f"  [OK] 接口实现: {description}")
    else:
        print(f"  [WARN] 接口实现: {description} 未找到")

# 检查静态成员
static_checks = [
    ("静态 定义", "静态属性"),
    ("静态 函数", "静态方法"),
    ("类函数", "类方法"),
]

for static_item, description in static_checks:
    if static_item in content:
        print(f"  [OK] 静态成员: {description}")
    else:
        print(f"  [WARN] 静态成员: {description} 未找到")

# 检查模块导出
export_checks = [
    ("导出 动物", "导出动物类"),
    ("导出 狗, 猫", "导出狗和猫类"),
    ("导出 创建动物", "导出函数"),
    ("导出 动物 为 基础动物", "导出别名"),
]

for export, description in export_checks:
    if export in content:
        print(f"  [OK] 模块导出: {description}")
    else:
        print(f"  [WARN] 模块导出: {description} 未找到")

# 检查多态使用
polymorphism_checks = [
    ("循环 动物 遍历 动物列表", "多态循环"),
    ("动物.叫()", "多态方法调用"),
]

for poly_check, description in polymorphism_checks:
    if poly_check in content:
        print(f"  [OK] 多态使用: {description}")
    else:
        print(f"  [WARN] 多态使用: {description} 未找到")

# 检查父类调用
super_checks = [
    ("父类.初始化", "调用父类构造函数"),
    ("父类.显示信息", "调用父类方法"),
]

for super_check, description in super_checks:
    if super_check in content:
        print(f"  [OK] 父类调用: {description}")
    else:
        print(f"  [WARN] 父类调用: {description} 未找到")

# 检查访问控制
access_checks = [
    ("自身.名字", "访问自身属性"),
    ("自身._余额", "访问私有属性（约定）"),
]

for access_check, description in access_checks:
    if access_check in content:
        print(f"  [OK] 访问控制: {description}")
    else:
        print(f"  [WARN] 访问控制: {description} 未找到")

# 总结统计
print("\n=== 统计总结 ===")
total_checks = (
    len(keywords_to_check)
    + len(classes_to_check)
    + len(interfaces_to_check)
    + len(methods_to_check)
    + len(object_creations)
    + len(inheritance_checks)
    + len(implementation_checks)
    + len(static_checks)
    + len(export_checks)
    + len(polymorphism_checks)
    + len(super_checks)
    + len(access_checks)
)
print(f"总检查项: {total_checks}")

# 计算通过率
passed = 0
for check_list in [
    keywords_to_check,
    classes_to_check,
    interfaces_to_check,
    methods_to_check,
    object_creations,
    inheritance_checks,
    implementation_checks,
    static_checks,
    export_checks,
    polymorphism_checks,
    super_checks,
    access_checks,
]:
    for item in check_list:
        if isinstance(item, tuple):
            keyword = item[0]
        else:
            keyword = item

        if keyword in content:
            passed += 1

pass_rate = (passed / total_checks) * 100
print(f"通过项: {passed}/{total_checks} ({pass_rate:.1f}%)")

if pass_rate >= 90:
    print("\n[SUCCESS] OOP示例文件包含所有关键特性！")
elif pass_rate >= 70:
    print("\n[WARNING] OOP示例文件包含大部分特性，但可能缺少一些高级功能。")
else:
    print("\n[ERROR] OOP示例文件缺少重要特性，需要进一步完善。")

print("\n=== 示例文件内容预览 ===")
lines = content.splitlines()
print(f"前10行:")
for i, line in enumerate(lines[:10]):
    print(f"  {i+1:3d}: {line}")

print(f"\n最后10行:")
for i, line in enumerate(lines[-10:]):
    print(f"  {len(lines)-9+i:3d}: {line}")

print("\n=== 测试完成 ===")
