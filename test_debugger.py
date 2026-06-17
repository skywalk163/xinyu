#!/usr/bin/env python3
"""
测试调试器功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.debugger import DebuggerManager
from src.core.compiler import XinyuCompiler


def test_debugger_basic():
    """测试调试器基本功能"""
    print("测试调试器基本功能...")
    
    # 创建编译器
    compiler = XinyuCompiler(enable_safety=False)
    
    # 创建调试器管理器
    debugger_manager = DebuggerManager(compiler)
    
    # 开始调试会话
    if not debugger_manager.start_debug_session():
        print("启动调试会话失败")
        return False
        
    print("调试会话已启动")
    
    # 测试设置断点
    print("\n1. 测试设置断点...")
    success = debugger_manager.handle_command("break test.py:10")
    print(f"设置断点结果: {'成功' if success else '失败'}")
    
    # 测试列出断点
    print("\n2. 测试列出断点...")
    success = debugger_manager.handle_command("list")
    print(f"列出断点结果: {'成功' if success else '失败'}")
    
    # 测试清除断点
    print("\n3. 测试清除断点...")
    success = debugger_manager.handle_command("clear 1")
    print(f"清除断点结果: {'成功' if success else '失败'}")
    
    # 测试再次列出断点
    print("\n4. 测试再次列出断点...")
    success = debugger_manager.handle_command("list")
    print(f"列出断点结果: {'成功' if success else '失败'}")
    
    # 测试查看变量
    print("\n5. 测试查看变量...")
    success = debugger_manager.handle_command("vars")
    print(f"查看变量结果: {'成功' if success else '失败'}")
    
    # 测试查看调用栈
    print("\n6. 测试查看调用栈...")
    success = debugger_manager.handle_command("stack")
    print(f"查看调用栈结果: {'成功' if success else '失败'}")
    
    # 测试帮助命令
    print("\n7. 测试帮助命令...")
    success = debugger_manager.handle_command("help")
    print(f"帮助命令结果: {'成功' if success else '失败'}")
    
    # 停止调试会话
    print("\n8. 停止调试会话...")
    success = debugger_manager.stop_debug_session()
    print(f"停止调试会话结果: {'成功' if success else '失败'}")
    
    return True


def test_debugger_with_code():
    """测试调试器执行代码"""
    print("\n测试调试器执行代码...")
    
    # 创建编译器
    compiler = XinyuCompiler(enable_safety=False)
    
    # 创建调试器管理器
    debugger_manager = DebuggerManager(compiler)
    
    # 开始调试会话
    if not debugger_manager.start_debug_session():
        print("启动调试会话失败")
        return False
        
    # 简单的测试代码
    test_code = """
x = 10
y = 20
z = x + y
print(f"x={x}, y={y}, z={z}")
"""
    
    print(f"测试代码:\n{test_code}")
    
    # 执行代码
    print("执行代码...")
    result = debugger_manager.execute_with_debug(test_code)
    print(f"执行结果: {result}")
    
    # 停止调试会话
    debugger_manager.stop_debug_session()
    
    return True


def test_debugger_commands():
    """测试调试器命令"""
    print("\n测试调试器命令...")
    
    # 创建编译器
    compiler = XinyuCompiler(enable_safety=False)
    
    # 创建调试器管理器
    debugger_manager = DebuggerManager(compiler)
    
    # 开始调试会话
    if not debugger_manager.start_debug_session():
        print("启动调试会话失败")
        return False
        
    # 测试各种命令
    commands = [
        "break test.py:5",
        "break test.py:10 condition x > 5",
        "list",
        "clear 1",
        "list",
        "vars",
        "stack",
        "help"
    ]
    
    for cmd in commands:
        print(f"\n执行命令: {cmd}")
        success = debugger_manager.handle_command(cmd)
        print(f"结果: {'成功' if success else '失败'}")
    
    # 停止调试会话
    debugger_manager.stop_debug_session()
    
    return True


def main():
    """主测试函数"""
    print("开始测试调试器功能")
    print("=" * 50)
    
    tests = [
        ("基本功能测试", test_debugger_basic),
        ("代码执行测试", test_debugger_with_code),
        ("命令测试", test_debugger_commands)
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"\n{test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                print(f"✓ {test_name} 通过")
            else:
                print(f"✗ {test_name} 失败")
                all_passed = False
        except Exception as e:
            print(f"✗ {test_name} 异常: {e}")
            import traceback
            traceback.print_exc()
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("所有测试通过!")
    else:
        print("部分测试失败!")
        
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)