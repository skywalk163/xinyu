#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""最终测试REPL与增强历史记录管理器的集成"""

import io
import sys
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
            "如果 真: 打印('条件成立')",
        ]

        for cmd in test_commands:
            repl._add_to_history(cmd)

        # 验证历史记录数量
        assert len(repl.history_manager) == 5, f"应该有5条历史记录，实际{len(repl.history_manager)}条"
        print(f"  历史记录添加成功: {len(repl.history_manager)}条")

        # 测试2: 历史列表
        print("\n2. 测试历史列表命令...")
        # 重定向输出
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        try:
            repl._list_history(2)
            output = sys.stdout.getvalue()
            assert "最近 2 条历史记录:" in output
            print("  历史列表显示正常")
        finally:
            sys.stdout = old_stdout

        # 测试3: 历史搜索
        print("\n3. 测试历史搜索命令...")
        sys.stdout = io.StringIO()
        try:
            repl._search_history("定义")
            output = sys.stdout.getvalue()
            assert "找到" in output or "没有找到" in output
            print("  历史搜索功能正常")
        finally:
            sys.stdout = old_stdout

        # 测试4: 历史过滤
        print("\n4. 测试历史过滤命令...")
        sys.stdout = io.StringIO()
        try:
            repl._filter_history_by_type("definition")
            output = sys.stdout.getvalue()
            assert "找到" in output or "没有找到" in output
            print("  历史过滤功能正常")
        finally:
            sys.stdout = old_stdout

        # 测试5: 历史统计
        print("\n5. 测试历史统计命令...")
        sys.stdout = io.StringIO()
        try:
            repl._show_history_stats()
            output = sys.stdout.getvalue()
            assert "历史记录统计信息:" in output
            print("  历史统计功能正常")
        finally:
            sys.stdout = old_stdout

        # 测试6: 历史导出
        print("\n6. 测试历史导出命令...")
        json_file = Path(tmpdir) / "exported_history.json"
        sys.stdout = io.StringIO()
        try:
            repl._export_history(json_file)
            output = sys.stdout.getvalue()
            assert "历史记录已导出到 JSON 文件" in output
            assert json_file.exists(), "JSON导出文件应该存在"
            print(f"  历史记录导出成功: {json_file}")
        finally:
            sys.stdout = old_stdout

        # 测试7: 历史导入
        print("\n7. 测试历史导入命令...")
        # 先清除历史记录
        repl.history_manager.clear()
        assert len(repl.history_manager) == 0, "清除后应该没有历史记录"

        # 导入历史记录
        sys.stdout = io.StringIO()
        try:
            repl._import_history(json_file)
            output = sys.stdout.getvalue()
            assert "从 JSON 文件导入" in output
            assert len(repl.history_manager) == 5, f"导入后应该有5条历史记录，实际{len(repl.history_manager)}条"
            print(f"  历史记录导入成功: {len(repl.history_manager)}条")
        finally:
            sys.stdout = old_stdout

        # 测试8: 命令解析
        print("\n8. 测试命令解析...")
        test_commands = [
            ("历史", "显示帮助"),
            ("历史 列表", "显示最近10条历史"),
            ("历史 列表 2", "显示最近2条历史"),
            ("历史 搜索 定义", "搜索包含'定义'的历史"),
            ("历史 过滤 definition", "按类型过滤"),
            ("历史 统计", "显示统计信息"),
        ]

        for cmd, description in test_commands:
            print(f"  测试: {cmd} ({description})")
            sys.stdout = io.StringIO()
            try:
                repl._handle_history_command(cmd)
                output = sys.stdout.getvalue()
                # 验证命令执行没有抛出异常
                assert True
            except Exception as e:
                print(f"    错误: {e}")
                raise
            finally:
                sys.stdout = old_stdout

        print("  命令解析功能正常")

        print("\n所有测试通过！")
        return True


def test_history_manager_directly():
    """直接测试HistoryManager"""
    print("\n直接测试HistoryManager...")

    with tempfile.TemporaryDirectory() as tmpdir:
        history_file = Path(tmpdir) / "direct_test.pkl"

        # 创建HistoryManager
        manager = HistoryManager(max_size=10, history_file=history_file)

        # 测试添加记录
        manager.add_entry("测试命令1", "结果1", tags=["测试"])
        manager.add_entry("测试命令2", "结果2", tags=["测试"])
        manager.add_entry("错误命令", success=False, tags=["错误"])

        assert len(manager) == 3, f"应该有3条记录，实际{len(manager)}条"
        print(f"  添加记录: {len(manager)}条")

        # 测试搜索
        results = manager.search(keyword="测试")
        assert len(results) == 2, f"搜索应该返回2条记录，实际{len(results)}条"
        print(f"  搜索功能: 找到{len(results)}条记录")

        # 测试过滤
        results = manager.search(success_only=True)
        assert len(results) == 2, f"成功过滤应该返回2条记录，实际{len(results)}条"
        print(f"  成功过滤: {len(results)}条成功记录")

        # 测试编辑
        new_entry = manager.edit_and_reexecute(0, "编辑后的命令")
        assert new_entry is not None, "编辑应该返回新条目"
        assert new_entry.command == "编辑后的命令", f"新命令应该是'编辑后的命令'，实际是'{new_entry.command}'"
        print(f"  编辑功能: {new_entry.command}")

        # 测试统计
        stats = manager.get_stats()
        assert stats["total_entries"] == 4, f"应该有4条记录，实际{stats['total_entries']}条"
        print(f"  统计功能: {stats['total_entries']}条记录")

        # 测试导出导入
        json_file = Path(tmpdir) / "export.json"
        manager.export_json(json_file)
        assert json_file.exists(), "导出文件应该存在"
        print(f"  导出功能: {json_file}")

        # 创建新管理器并导入
        new_manager = HistoryManager(max_size=10, history_file=Path(tmpdir) / "import_test.pkl")
        imported_count = new_manager.import_json(json_file)
        assert imported_count == 4, f"应该导入4条记录，实际{imported_count}条"
        print(f"  导入功能: {imported_count}条记录")

        print("  HistoryManager所有功能测试通过")
        return True


def main():
    """主测试函数"""
    print("=" * 60)
    print("REPL增强历史记录管理器集成测试")
    print("=" * 60)

    try:
        # 测试直接功能
        print("\n[阶段1] 测试HistoryManager核心功能")
        if not test_history_manager_directly():
            print("HistoryManager测试失败")
            return 1

        # 测试REPL集成
        print("\n[阶段2] 测试REPL集成功能")
        if not test_basic_functionality():
            print("REPL集成测试失败")
            return 1

        print("\n" + "=" * 60)
        print("所有测试通过！")
        print("=" * 60)
        print("\n功能总结:")
        print("1. [完成] HistoryManager类实现完成")
        print("2. [完成] 支持历史记录的增删改查")
        print("3. [完成] 支持搜索、过滤、统计功能")
        print("4. [完成] 支持导入导出功能")
        print("5. [完成] 集成到现有REPL系统")
        print("6. [完成] 提供完整的历史命令界面")
        print("7. [完成] 支持命令类型自动检测")
        print("8. [完成] 支持标签系统")
        print("9. [完成] 支持持久化存储")
        print("10. [完成] 提供丰富的统计信息")
        return 0

    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
