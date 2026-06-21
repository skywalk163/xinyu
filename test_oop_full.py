#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""完整测试OOP和模块系统"""

import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.codegen.python_codegen import PythonCodegen
from src.error_handling import ErrorHandler
from src.lexer.lexer_with_error_handler import LexerWithErrorHandler
from src.parser.parser_with_error_handler import ParserWithErrorHandler


def test_oop_compilation():
    """测试OOP编译"""
    print("=== 测试OOP编译 ===")

    # 测试代码
    test_code = """
# 基本类定义
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

    函数 介绍()：
        打印 "我是" 自身.名字 "，今年" 自身.年龄 "岁。"。
    。
。

# 创建对象
定义 我的宠物 = 新建 动物("小白", 3)。
我的宠物.介绍()。
打印 我的宠物.叫()。

# 继承
定义 类 狗 继承 动物：
    函数 叫()：
        返回 "汪汪"。
    。

    函数 摇尾巴()：
        打印 自身.名字 "正在摇尾巴..."。
    。
。

定义 我的狗 = 新建 狗("旺财", 2)。
我的狗.介绍()。
打印 我的狗.叫()。
我的狗.摇尾巴()。

# 静态方法和属性
定义 类 数学工具：
    静态 定义 圆周率 = 3.14159。

    静态 函数 平方(参数 x)：
        返回 x 相乘 x。
    。

    类函数 创建实例(参数 值)：
        返回 数学工具(值)。
    。

    函数 初始化(参数 值)：
        自身.值 = 值。
    。

    函数 计算面积(参数 半径)：
        返回 数学工具.圆周率 相乘 半径 相乘 半径。
    。
。

打印 "圆周率：" 数学工具.圆周率。
打印 "5的平方：" 数学工具.平方(5)。

定义 工具 = 数学工具.创建实例(10)。
打印 "半径为3的圆面积：" 工具.计算面积(3)。
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

    if error_handler.has_errors():
        print("词法错误：")
        for error in error_handler.get_errors():
            print(f"  {error}")
        return

    # 语法分析
    print("\n2. 语法分析...")
    parser = ParserWithErrorHandler(tokens, error_handler)
    ast = parser.parse()

    if error_handler.has_errors():
        print("语法错误：")
        for error in error_handler.get_errors():
            print(f"  {error}")
        return

    print("语法分析成功！")

    # 代码生成
    print("\n3. 代码生成...")
    codegen = PythonCodegen()
    python_code = codegen.generate(ast)

    print("生成的Python代码：")
    print(python_code)

    # 执行生成的代码
    print("\n4. 执行生成的代码...")
    try:
        # 创建局部命名空间
        local_vars = {}

        # 执行代码
        exec(python_code, {}, local_vars)

        print("执行成功！")
        print(f"局部变量: {list(local_vars.keys())}")

    except Exception as e:
        print(f"执行错误: {e}")
        import traceback

        traceback.print_exc()


def test_module_system():
    """测试模块系统"""
    print("\n" + "=" * 50 + "\n")
    print("=== 测试模块系统 ===")

    # 测试代码
    test_code = """
# 模块导出测试
定义 类 工具类：
    静态 函数 帮助()：
        打印 "这是一个工具类"。
    。
。

定义 函数 工具函数()：
    返回 "工具函数"。
。

定义 常量 = 42。

导出 工具类, 工具函数, 常量。
导出 工具类 为 工具。
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

    if error_handler.has_errors():
        print("词法错误：")
        for error in error_handler.get_errors():
            print(f"  {error}")
        return

    # 语法分析
    print("\n2. 语法分析...")
    parser = ParserWithErrorHandler(tokens, error_handler)
    ast = parser.parse()

    if error_handler.has_errors():
        print("语法错误：")
        for error in error_handler.get_errors():
            print(f"  {error}")
        return

    print("语法分析成功！")

    # 代码生成
    print("\n3. 代码生成...")
    codegen = PythonCodegen()
    python_code = codegen.generate(ast)

    print("生成的Python代码：")
    print(python_code)


def test_interface_and_polymorphism():
    """测试接口和多态"""
    print("\n" + "=" * 50 + "\n")
    print("=== 测试接口和多态 ===")

    # 测试代码
    test_code = """
# 接口定义
定义 接口 可发声：
    函数 发声()。
。

# 实现接口的类
定义 类 猫 实现 可发声：
    函数 发声()：
        返回 "喵喵"。
    。
。

定义 类 鸟 实现 可发声：
    函数 发声()：
        返回 "叽叽喳喳"。
    。
。

# 多态测试
定义 动物列表 = 列表(新建 猫(), 新建 鸟())。
循环 动物 遍历 动物列表：
    打印 动物.发声()。
。
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

    if error_handler.has_errors():
        print("词法错误：")
        for error in error_handler.get_errors():
            print(f"  {error}")
        return

    # 语法分析
    print("\n2. 语法分析...")
    parser = ParserWithErrorHandler(tokens, error_handler)
    ast = parser.parse()

    if error_handler.has_errors():
        print("语法错误：")
        for error in error_handler.get_errors():
            print(f"  {error}")
        return

    print("语法分析成功！")

    # 代码生成
    print("\n3. 代码生成...")
    codegen = PythonCodegen()
    python_code = codegen.generate(ast)

    print("生成的Python代码：")
    print(python_code)

    # 执行生成的代码
    print("\n4. 执行生成的代码...")
    try:
        # 需要导入abc模块
        import abc

        # 创建局部命名空间
        local_vars = {"abc": abc}

        # 执行代码
        exec(python_code, {}, local_vars)

        print("执行成功！")

    except Exception as e:
        print(f"执行错误: {e}")
        import traceback

        traceback.print_exc()


def main():
    """主函数"""
    print("心语编程语言 - OOP和模块系统测试")
    print("=" * 50)

    # 测试OOP编译
    test_oop_compilation()

    # 测试模块系统
    test_module_system()

    # 测试接口和多态
    test_interface_and_polymorphism()

    print("\n" + "=" * 50)
    print("所有测试完成！")


if __name__ == "__main__":
    main()
