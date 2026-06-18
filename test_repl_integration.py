#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试REPL与增强历史记录管理器的集成"""

import tempfile
from pathlib import Path

from src.repl.enhanced_repl import EnhancedREPL
from src.repl.history_manager import CommandType, HistoryManager


class MockCompiler:
    """模拟编译器用于测试"""

    def execute(self, code: str):
        """模拟执行代码"""
        if "错误" in code:
            raise ValueError("模拟错误")
        elif "定义" in code:
            return "定义成功"
        elif "计算" in code:
            return "计算结果"
        else:
            return f"执行: {code}"


def test_repl_history_integration():
    """测试REPL与历史记录管理器的集成"""
    print("测试REPL与历史记录管理器的集成...")

    with tempfile.TemporaryDirectory() as tmpdir:
        history_file = Path(tmpdir) / "test_repl_history.pkl"

        # 创建模拟编译器和REPL
        compiler = MockCompiler()
        repl = EnhancedREPL(compiler, history_file=str(history_file))

        # 测试添加历史记录
        print("1. 测试添加历史记录...")
        test_commands = [
            "定义 函数(): 返回 1",
            "计算 1 + 2 * 3",
            "打印('Hello, World!')",
            "导入 数学",
            "如果 真: 打印('条件成立')",
        ]

        for cmd in test_commands:
            repl._add_to_history(cmd)

        # 验证历史记录数量
        assert len(repl.history_manager) == 5, f"应该有5条历史记录，实际{len(repl.history_manager)}条"
        print(f"  历史记录添加成功: {len(repl.history_manager)}条")

        # 测试历史列表命令
        print("\n2. 测试历史列表命令...")
        repl._list_history(3)

        # 测试历史搜索命令
        print("\n3. 测试历史搜索命令...")
        repl._search_history("定义")

        # 测试历史过滤命令
        print("\n4. 测试历史过滤命令...")
        repl._filter_history_by_type("definition")

        # 测试历史统计命令
        print("\n5. 测试历史统计命令...")
        repl._show_history_stats()

        # 测试历史导出命令
        print("\n6. 测试历史导出命令...")
        json_file = Path(tmpdir) / "exported_history.json"
        repl._export_history(json_file)
        assert json_file.exists(), "JSON导出文件应该存在"
        print(f"  历史记录导出成功: {json_file}")

        # 测试历史导入命令
        print("\n7. 测试历史导入命令...")
        # 先清除历史记录
        repl.history_manager.clear()
        assert len(repl.history_manager) == 0, "清除后应该没有历史记录"

        # 导入历史记录
        repl._import_history(json_file)
        assert len(repl.history_manager) == 5, f"导入后应该有5条历史记录，实际{len(repl.history_manager)}条"
        print(f"  历史记录导入成功: {len(repl.history_manager)}条")

        # 测试历史编辑命令
        print("\n8. 测试历史编辑命令...")
        # 模拟用户输入
        import io
        import sys

        # 保存原始输入
        original_input = __builtins__.input

        # 模拟用户确认
        def mock_input(prompt):
            if "确定要清除所有历史记录吗" in prompt:
                return "n"  # 不确认清除
            return ""

        __builtins__.input = mock_input

        try:
            # 测试编辑命令（不实际执行，因为需要编译器）
            print("  注意: 编辑命令测试需要实际编译器，这里只测试接口")
        finally:
            # 恢复原始输入
            __builtins__.input = original_input

        # 测试历史清除命令（用户取消）
        print("\n9. 测试历史清除命令（用户取消）...")

        # 模拟用户输入"n"（取消）
        def mock_input_cancel(prompt):
            return "n"

        original_input = __builtins__.input
        __builtins__.input = mock_input_cancel

        try:
            repl._clear_history()
            assert len(repl.history_manager) == 5, "用户取消后历史记录应该保持不变"
            print("  历史清除取消成功")
        finally:
            __builtins__.input = original_input

        print("\n所有测试完成！")


def test_command_parsing():
    """测试命令解析"""
    print("\n测试命令解析...")

    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmpdir:
        history_file = Path(tmpdir) / "test_command_history.pkl"

        compiler = MockCompiler()
        repl = EnhancedREPL(compiler, history_file=str(history_file))

        # 添加一些测试数据
        test_commands = ["定义 函数(): 返回 1", "计算 1 + 2", "打印('测试')"]

        for cmd in test_commands:
            repl._add_to_history(cmd)

        test_cases = [
            ("历史", "显示帮助"),
            ("历史 列表", "显示最近10条历史"),
            ("历史 列表 2", "显示最近2条历史"),
            ("历史 搜索 定义", "搜索包含'定义'的历史"),
            ("历史 过滤 definition", "按类型过滤"),
            ("历史 统计", "显示统计信息"),
        ]

        for cmd, description in test_cases:
            print(f"  测试命令: {cmd} ({description})")
            repl._handle_history_command(cmd)

        # 测试导出（不测试导入，因为会重复）
        json_file = Path(tmpdir) / "test_export.json"
        repl._export_history(json_file)
        print(f"  测试导出: 历史记录已导出到 {json_file}")

        # 测试编辑命令
        print("  测试编辑命令: 历史 编辑 0 新命令")
        repl._handle_history_command("历史 编辑 0 新命令")

        # 测试清除命令（模拟用户取消）
        def mock_input_cancel(prompt):
            return "n"

        original_input = __builtins__.input
        __builtins__.input = mock_input_cancel

        try:
            print("  测试清除命令（用户取消）: 历史 清除")
            repl._handle_history_command("历史 清除")
        finally:
            __builtins__.input = original_input

    print("  命令解析测试完成")


def main():
    """主测试函数"""
    print("=" * 60)
    print("REPL与增强历史记录管理器集成测试")
    print("=" * 60)

    try:
        test_repl_history_integration()
        test_command_parsing()

        print("\n" + "=" * 60)
        print("所有测试通过！")
        print("=" * 60)

    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
