#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试新的编译器接口"""

import sys
sys.path.insert(0, '.')

from src.core.compiler import XinyuCompiler

def test_basic_compilation():
    """测试基本编译功能"""
    print("测试基本编译功能...")
    
    # 创建编译器实例
    compiler = XinyuCompiler(enable_safety=True)
    
    # 测试简单的心语代码
    source = '印"你好，世界！"。'
    
    try:
        # 编译代码
        result = compiler.compile(source)
        print("[OK] 编译成功！")
        print(f"生成的Python代码长度: {len(result)} 字符")
        
        # 检查诊断信息
        diagnostics = compiler.get_diagnostics()
        if diagnostics:
            print(f"\n诊断信息 ({len(diagnostics)} 条):")
            for d in diagnostics:
                print(f"  - {d}")
        else:
            print("\n[OK] 无诊断信息")
            
        return True
        
    except Exception as e:
        print(f"[FAIL] 编译失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_error_handling():
    """测试错误处理"""
    print("\n测试错误处理...")
    
    compiler = XinyuCompiler(enable_safety=True)
    
    # 测试有语法错误的代码
    source = '印"未闭合的字符串'
    
    try:
        result = compiler.compile(source)
        print(f"生成的代码: {result[:50]}...")
        
        diagnostics = compiler.get_diagnostics()
        if diagnostics:
            print(f"[OK] 成功捕获错误 ({len(diagnostics)} 条):")
            for d in diagnostics:
                print(f"  - {d}")
            return True
        else:
            print("[FAIL] 未捕获到错误")
            return False
            
    except Exception as e:
        print(f"编译异常: {e}")
        return False

def test_safety_features():
    """测试安全特性"""
    print("\n测试安全特性...")
    
    compiler = XinyuCompiler(enable_safety=True)
    
    # 测试危险代码
    dangerous_code = """
    变量 = 打开("test.txt", "w")
    变量.写入("危险操作")
    变量.关闭()
    """
    
    try:
        result = compiler.compile(dangerous_code)
        print(f"生成的代码: {result[:100]}...")
        
        # 尝试执行
        output = compiler.execute(dangerous_code)
        print(f"执行结果: {output}")
        
        print("[FAIL] 危险代码应该被阻止")
        return False
        
    except Exception as e:
        print(f"[OK] 安全特性生效: {e}")
        return True

def main():
    """主测试函数"""
    print("=" * 60)
    print("心语编译器接口测试")
    print("=" * 60)
    
    results = []
    
    # 运行测试
    results.append(("基本编译", test_basic_compilation()))
    results.append(("错误处理", test_error_handling()))
    results.append(("安全特性", test_safety_features()))
    
    # 输出总结
    print("\n" + "=" * 60)
    print("测试总结:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "[OK] 通过" if success else "[FAIL] 失败"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("[SUCCESS] 所有测试通过！")
    else:
        print("[WARNING] 部分测试失败")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)