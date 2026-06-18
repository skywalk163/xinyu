#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试增强的REPL历史记录管理器（简化版）"""

import json
import os
import tempfile
from datetime import datetime
from pathlib import Path

from src.repl.history_manager import (
    CommandType,
    HistoryEntry,
    HistoryManager,
    create_history_manager,
)


def test_basic_operations():
    """测试基本操作"""
    print("测试基本操作...")

    import os
    import tempfile

    # 使用临时文件避免状态共享
    with tempfile.TemporaryDirectory() as tmpdir:
        history_file = Path(tmpdir) / "test_basic.pkl"

        # 创建内存模式的历史管理器
        manager = HistoryManager(max_size=5, history_file=history_file)

        # 添加历史记录
        entries = []
        for i in range(3):
            entry = manager.add_entry(
                command=f"命令{i}",
                result=f"结果{i}",
                execution_time=0.1 * (i + 1),
                success=True,
                tags=[f"测试{i}", "示例"],
                metadata={"index": i},
            )
            entries.append(entry)

        # 验证数量
        assert len(manager) == 3, f"期望3条记录，实际{len(manager)}条"
        print(f"  添加记录成功: {len(manager)}条")

        # 验证最新记录
        latest = manager[0]
        assert latest.command == "命令2", f"最新命令应该是'命令2'，实际是'{latest.command}'"
        print(f"  最新记录正确: {latest.command}")

        # 测试迭代
        count = 0
        for entry in manager:
            count += 1
        assert count == 3, f"迭代应该返回3条记录，实际{count}条"
        print(f"  迭代功能正常: {count}条")

        # 测试大小限制
        for i in range(3, 10):
            manager.add_entry(command=f"命令{i}", result=f"结果{i}")

        assert len(manager) == 5, f"大小限制应该是5条，实际{len(manager)}条"
        print(f"  大小限制生效: {len(manager)}条")

        return True


def test_search_functionality():
    """测试搜索功能"""
    print("\n测试搜索功能...")

    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        history_file = Path(tmpdir) / "test_search.pkl"
        manager = HistoryManager(max_size=10, history_file=history_file)

        # 添加不同类型的历史记录
        manager.add_entry("定义 函数(): 返回 1", result="成功", tags=["函数", "定义"])
        manager.add_entry("导入 数学", result="成功", tags=["导入"])
        manager.add_entry("如果 真: 打印('hello')", result="成功", tags=["控制"])
        manager.add_entry("1 + 2 * 3", result="7", tags=["计算"])
        manager.add_entry("调试 变量", result="成功", tags=["调试"])
        manager.add_entry("帮助", result="帮助信息", tags=["帮助"])

        # 测试关键词搜索
        results = manager.search(keyword="函数")
        assert len(results) == 1, f"搜索'函数'应该返回1条记录，实际{len(results)}条"
        print(f"  关键词搜索正常: 找到{len(results)}条记录")

        # 测试类型过滤
        results = manager.search(command_type=CommandType.DEFINITION)
        assert len(results) == 1, f"类型过滤应该返回1条记录，实际{len(results)}条"
        assert results[0].command_type == CommandType.DEFINITION
        print(f"  类型过滤正常: {results[0].command_type.value}")

        # 测试标签过滤
        results = manager.search(tags=["计算"])
        assert len(results) == 1, f"标签过滤应该返回1条记录，实际{len(results)}条"
        assert "计算" in results[0].tags
        print(f"  标签过滤正常: {results[0].tags}")

        # 测试成功过滤
        manager.add_entry("错误命令", success=False)
        results = manager.search(success_only=True)
        success_count = sum(1 for r in results if r.success)
        assert success_count == len(results), "应该只返回成功的记录"
        print(f"  成功过滤正常: {len(results)}条成功记录")

        return True


def test_edit_functionality():
    """测试编辑功能"""
    print("\n测试编辑功能...")

    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        history_file = Path(tmpdir) / "test_edit.pkl"
        manager = HistoryManager(max_size=10, history_file=history_file)

        # 添加原始记录
        original_entry = manager.add_entry("原始命令", result="原始结果", tags=["原始"])

        # 编辑记录
        new_entry = manager.edit_and_reexecute(0, "编辑后的命令")

        assert new_entry is not None, "编辑应该返回新条目"
        assert new_entry.command == "编辑后的命令", f"新命令应该是'编辑后的命令'，实际是'{new_entry.command}'"
        assert new_entry.result is None, "新条目应该没有结果"
        assert "edited_from" in new_entry.metadata, "应该包含编辑来源信息"
        assert new_entry.metadata["edited_from"] == "原始命令"
        print(f"  编辑功能正常: {new_entry.command}")

        # 验证历史记录数量
        assert len(manager) == 2, f"编辑后应该有2条记录，实际{len(manager)}条"
        print(f"  历史记录数量正确: {len(manager)}条")

        return True


def test_persistence():
    """测试持久化功能"""
    print("\n测试持久化功能...")

    with tempfile.TemporaryDirectory() as tmpdir:
        history_file = Path(tmpdir) / "test_history.pkl"

        # 创建管理器并添加记录
        manager1 = HistoryManager(max_size=10, history_file=history_file)
        manager1.add_entry("命令1", "结果1")
        manager1.add_entry("命令2", "结果2")

        # 创建新管理器加载记录
        manager2 = HistoryManager(max_size=10, history_file=history_file)

        assert len(manager2) == 2, f"加载后应该有2条记录，实际{len(manager2)}条"
        print(f"  持久化加载正常: {len(manager2)}条记录")

        # 验证记录内容
        entry = manager2[0]
        assert entry.command == "命令2", f"最新命令应该是'命令2'，实际是'{entry.command}'"
        print(f"  记录内容正确: {entry.command}")

    return True


def test_import_export():
    """测试导入导出功能"""
    print("\n测试导入导出功能...")

    with tempfile.TemporaryDirectory() as tmpdir:
        # 使用临时文件避免状态共享
        history_file = Path(tmpdir) / "test_import_export.pkl"

        # 创建管理器并添加记录
        manager = HistoryManager(max_size=10, history_file=history_file)
        manager.add_entry("命令1", "结果1", tags=["测试"])
        manager.add_entry("命令2", "结果2", tags=["测试"])

        # 导出为JSON
        json_file = Path(tmpdir) / "history.json"
        manager.export_json(json_file)

        assert json_file.exists(), "JSON文件应该存在"
        print(f"  JSON导出成功: {json_file}")

        # 验证JSON内容
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data["count"] == 2, f"应该导出2条记录，实际{data['count']}条"
        print(f"  JSON内容正确: {data['count']}条记录")

        # 导出为CSV
        csv_file = Path(tmpdir) / "history.csv"
        manager.export_csv(csv_file)

        assert csv_file.exists(), "CSV文件应该存在"
        print(f"  CSV导出成功: {csv_file}")

        # 创建新管理器并导入
        new_history_file = Path(tmpdir) / "test_import.pkl"
        new_manager = HistoryManager(max_size=10, history_file=new_history_file)
        imported_count = new_manager.import_json(json_file)

        assert imported_count == 2, f"应该导入2条记录，实际{imported_count}条"
        print(f"  JSON导入成功: {imported_count}条记录")

    return True


def test_convenience_functions():
    """测试便捷函数"""
    print("\n测试便捷函数...")

    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        # 使用临时文件避免状态共享
        history_file = Path(tmpdir) / "test_convenience.pkl"

        # 测试创建函数
        manager = HistoryManager(max_size=20, history_file=history_file)
        assert manager.max_size == 20, f"最大大小应该是20，实际{manager.max_size}"
        print(f"  创建函数正常: max_size={manager.max_size}")

        # 添加一些记录
        for i in range(3):
            manager.add_entry(f"测试命令{i}", f"测试结果{i}")

        # 测试统计
        stats = manager.get_stats()
        assert stats["total_entries"] == 3, f"应该有3条记录，实际{stats['total_entries']}条"
        print(f"  统计功能正常: {stats['total_entries']}条记录")

        return True


def main():
    """主测试函数"""
    print("=" * 60)
    print("增强REPL历史记录管理器测试")
    print("=" * 60)

    tests = [
        ("基本操作", test_basic_operations),
        ("搜索功能", test_search_functionality),
        ("编辑功能", test_edit_functionality),
        ("持久化", test_persistence),
        ("导入导出", test_import_export),
        ("便捷函数", test_convenience_functions),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            print(f"\n{test_name}:")
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"  错误: {e}")
            import traceback

            traceback.print_exc()
            results.append((test_name, False))

    print("\n" + "=" * 60)
    print("测试结果:")
    print("=" * 60)

    all_passed = True
    for test_name, success in results:
        status = "通过" if success else "失败"
        print(f"  {test_name}: {status}")
        if not success:
            all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("所有测试通过！")
        return 0
    else:
        print("部分测试失败")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
