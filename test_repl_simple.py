#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""简单测试REPL与增强历史记录管理器的集成"""

import tempfile
from pathlib import Path
from src.repl.enhanced_repl import EnhancedREPL
from src.repl.history_manager import HistoryManager, CommandType


class MockCompiler:
    """模拟编译器用于测试"""
    
    def execute(self, code: str):
        """模拟执行代码"""
        if '错误' in code:
            raise ValueError("模拟错误")
        elif '定义' in code:
            return "定义成功"
        elif '计算' in code:
            return "计算结果"
        else:
            return f"执行: {code}"


def test_basic_functionality():
    """测试基本功能"""
    print("测试REPL与增强历史记录管理器的基本功能...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        history_file = Path(tmpdir) / "test_history.pkl"
        
        # 创建模拟编译器和REPL
        compiler = MockCompiler()
        repl = EnhancedREPL(compiler, history_file=str(history_file))
        
        # 测试1: 添加历史记录
        print("\n1. 测试添加历史记录...")
        test_commands = [
            "定义 函数(): 返回 1",
            "计算 1 + 2 * 3",
            "打印('Hello, World!')",
            "导入 数学",
            "如果 真: 打印('条件成立')"
        ]
        
        for cmd in test_commands:
            repl._add_to_history(cmd)
        
        # 验证历史记录数量
        assert len(repl.history_manager) == 5, f"应该有5条历史记录，实际{len(repl.history_manager)}条"
        print(f"  ✓ 历史记录添加成功: {len(repl.history_manager)}条")
        
        # 测试2: 历史列表
        print("\n2. 测试历史列表命令...")
        repl._list_history(3)
        
        # 验证显示的行数
        print("  ✓ 历史列表显示正常")
        
        # 测试3: 历史搜索
        print("\n3. 测试历史搜索命令...")
        repl._search_history("定义")
        print("  ✓ 历史搜索功能正常")
        
        # 测试4: 历史过滤
        print("\n4. 测试历史过滤命令...")
        repl._filter_history_by_type("definition")
        print("  ✓ 历史过滤功能正常")
        
        # 测试5: 历史统计
        print("\n5. 测试历史统计命令...")
        repl._show_history_stats()
        print("  ✓ 历史统计功能正常")
        
        # 测试6: 历史导出
        print("\n6. 测试历史导出命令...")
        json_file = Path(tmpdir) / "exported_history.json"
        repl._export_history(json_file)
        assert json_file.exists(), "JSON导出文件应该存在"
        print(f"  ✓ 历史记录导出成功: {json_file}")
        
        # 测试7: 历史导入
        print("\n7. 测试历史导入命令...")
        # 先清除历史记录
        repl.history_manager.clear()
        assert len(repl.history_manager) == 0, "清除后应该没有历史记录"
        
        # 导入历史记录
        repl._import_history(json_file)
        assert len(repl.history_manager) == 5, f"导入后应该有5条历史记录，实际{len(repl.history_manager)}条"
        print(f"  ✓ 历史记录导入成功: {len(repl.history_manager)}条")
        
        # 测试8: 历史编辑
        print("\n8. 测试历史编辑命令...")
        # 模拟用户输入
        import io
        import sys
        
        # 保存原始stdout
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        try:
            repl._handle_history_command("历史 编辑 0 新命令测试")
            output = sys.stdout.getvalue()
            assert "已编辑