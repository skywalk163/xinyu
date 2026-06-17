#!/usr/bin/env python3
"""
测试增强REPL功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.compiler import XinyuCompiler
from src.repl import EnhancedREPL, SyntaxHighlighter, CodeCompletionProvider, HistoryManager


def test_syntax_highlighter():
    """测试语法高亮器"""
    print("测试语法高亮器...")
    
    highlighter = SyntaxHighlighter()
    
    test_cases = [
        ("定 x = 10。", "关键字高亮测试"),
        ("印\"你好世界\"。", "字符串高亮测试"),
        ("若 x 大于 5 则：\n    印\"大于5\"。\n否则：\n    印\"小于等于5\"。", "多行代码高亮测试"),
        ("# 这是一条注释\n定 y = 20。", "注释高亮测试"),
        ("定 结果 = x 加 y 乘 2。", "数字和运算符高亮测试"),
    ]
    
    for code, description in test_cases:
        print(f"\n{description}:")
        print("-" * 40)
        print("原始代码:")
        print(code)
        print("\n高亮后:")
        highlighted = highlighter.highlight(code)
        print(highlighted)
        
    return True


def test_code_completion():
    """测试代码补全"""
    print("\n\n测试代码补全...")
    
    compiler = XinyuCompiler()
    completion_provider = CodeCompletionProvider(compiler)
    
    test_cases = [
        ("如", ["如果"]),
        ("定", ["定义"]),
        ("返", ["返回"]),
        ("打", ["打印"]),
        ("输", ["输入"]),
    ]
    
    for input_text, expected_suggestions in test_cases:
        suggestions = completion_provider.complete(input_text, len(input_text))
        print(f"输入: '{input_text}'")
        print(f"期望: {expected_suggestions}")
        print(f"实际: {suggestions}")
        print(f"匹配: {'是' if set(suggestions) == set(expected_suggestions) else '否'}")
        print()
        
    return True


def test_history_manager():
    """测试历史记录管理器"""
    print("\n\n测试历史记录管理器...")
    
    # 使用临时文件
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.history') as f:
        history_file = f.name
        
    try:
        history_manager = HistoryManager(history_file)
        
        # 添加历史记录
        commands = [
            "定 x = 10。",
            "印 x。",
            "若 x 大于 5 则：印\"大于5\"。",
            "遍历 i 于 [1, 2, 3]：印 i。",
        ]
        
        print("添加历史记录:")
        for cmd in commands:
            history_manager.add(cmd)
            print(f"  {cmd}")
            
        # 测试获取上一条
        print("\n测试获取上一条历史记录:")
        for i in range(len(commands)):
            prev = history_manager.get_previous()
            print(f"  上一条 {i+1}: {prev}")
            
        # 测试获取下一条
        print("\n测试获取下一条历史记录:")
        for i in range(len(commands)):
            next_cmd = history_manager.get_next()
            print(f"  下一条 {i+1}: {next_cmd}")
            
        # 测试搜索
        print("\n测试搜索历史记录:")
        search_results = history_manager.search("印")
        print(f"  搜索 '印': {search_results}")
        
        # 测试保存和加载
        print("\n测试保存和加载历史记录:")
        history_manager._save_history()
        
        # 创建新的历史管理器加载相同文件
        history_manager2 = HistoryManager(history_file)
        print(f"  加载的历史记录: {history_manager2.history}")
        
        return True
        
    finally:
        # 清理临时文件
        os.unlink(history_file)


def test_enhanced_repl_basic():
    """测试增强REPL基本功能"""
    print("\n\n测试增强REPL基本功能...")
    
    compiler = XinyuCompiler(enable_safety=False)
    repl = EnhancedREPL(compiler)
    
    # 测试代码补全
    print("测试代码补全功能:")
    suggestions = repl.autocomplete("如", 1)
    print(f"  输入 '如' 的补全建议: {suggestions}")
    
    # 测试语法高亮
    print("\n测试语法高亮功能:")
    code = "定 x = 10。\n若 x 大于 5 则：印\"大于5\"。"
    highlighted = repl.highlight_code(code)
    print(f"  原始代码:\n{code}")
    print(f"  高亮后:\n{highlighted}")
    
    return True


def main():
    """主测试函数"""
    print("开始测试增强REPL功能")
    print("=" * 60)
    
    tests = [
        ("语法高亮器测试", test_syntax_highlighter),
        ("代码补全测试", test_code_completion),
        ("历史记录管理器测试", test_history_manager),
        ("增强REPL基本功能测试", test_enhanced_repl_basic),
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"\n{test_name}")
        print("-" * 40)
        
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
    
    print("\n" + "=" * 60)
    if all_passed:
        print("所有测试通过!")
    else:
        print("部分测试失败!")
        
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)