"""
增强REPL实现
支持代码补全、语法高亮、历史记录等功能
"""

import atexit
import os
import readline
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .history_manager import CommandType, HistoryEntry, HistoryManager


class CodeCompletionProvider:
    """代码补全提供器"""

    def __init__(self, compiler=None):
        self.compiler = compiler
        self.keywords = [
            "如果",
            "否则",
            "循环",
            "当",
            "为",
            "在",
            "定义",
            "返回",
            "导入",
            "从",
            "作为",
            "类",
            "尝试",
            "捕获",
            "最终",
            "引发",
            "断言",
            "通过",
            "继续",
            "中断",
            "打印",
            "输入",
        ]
        self.builtin_functions = [
            "打印",
            "输入",
            "长度",
            "类型",
            "整数",
            "浮点数",
            "字符串",
            "列表",
            "字典",
            "范围",
            "枚举",
            "排序",
            "反转",
            "求和",
            "最大值",
            "最小值",
            "绝对值",
            "四舍五入",
            "向上取整",
            "向下取整",
        ]

    def complete(self, text: str, pos: int) -> List[str]:
        """提供代码补全建议

        Args:
            text: 输入的文本
            pos: 光标位置

        Returns:
            补全建议列表
        """
        # 获取当前单词
        line = text[:pos]
        word_start = (
            max(
                line.rfind(" "),
                line.rfind("\t"),
                line.rfind("\n"),
                line.rfind("("),
                line.rfind("["),
                line.rfind("{"),
            )
            + 1
        )
        current_word = line[word_start:]

        if not current_word:
            return []

        suggestions = []

        # 关键字补全
        suggestions.extend([kw for kw in self.keywords if kw.startswith(current_word)])

        # 内置函数补全
        suggestions.extend(
            [func for func in self.builtin_functions if func.startswith(current_word)]
        )

        # 变量补全（如果有编译器上下文）
        if self.compiler:
            # 这里可以添加从编译器获取变量名的逻辑
            pass

        return suggestions[:10]  # 限制返回数量


class SyntaxHighlighter:
    """语法高亮器"""

    def __init__(self):
        self.keyword_colors = {
            "如果": "\033[91m",  # 红色
            "否则": "\033[91m",
            "循环": "\033[91m",
            "当": "\033[91m",
            "为": "\033[91m",
            "在": "\033[91m",
            "定义": "\033[92m",  # 绿色
            "返回": "\033[92m",
            "导入": "\033[92m",
            "从": "\033[92m",
            "作为": "\033[92m",
            "类": "\033[92m",
            "尝试": "\033[93m",  # 黄色
            "捕获": "\033[93m",
            "最终": "\033[93m",
            "引发": "\033[93m",
            "断言": "\033[93m",
            "通过": "\033[93m",
            "继续": "\033[93m",
            "中断": "\033[93m",
        }

        self.function_colors = {
            "打印": "\033[94m",  # 蓝色
            "输入": "\033[94m",
            "长度": "\033[94m",
            "类型": "\033[94m",
        }

        self.string_color = "\033[92m"  # 绿色
        self.number_color = "\033[93m"  # 黄色
        self.comment_color = "\033[90m"  # 灰色
        self.reset_color = "\033[0m"

    def highlight(self, code: str) -> str:
        """对代码进行语法高亮

        Args:
            code: 要高亮的代码

        Returns:
            高亮后的代码
        """
        if not code:
            return code

        lines = code.split("\n")
        highlighted_lines = []

        for line in lines:
            highlighted_line = self._highlight_line(line)
            highlighted_lines.append(highlighted_line)

        return "\n".join(highlighted_lines)

    def _highlight_line(self, line: str) -> str:
        """高亮单行代码"""
        if not line.strip():
            return line

        # 处理注释
        if "#" in line:
            comment_start = line.find("#")
            code_part = line[:comment_start]
            comment_part = line[comment_start:]
            highlighted = (
                self._highlight_code(code_part)
                + self.comment_color
                + comment_part
                + self.reset_color
            )
            return highlighted

        return self._highlight_code(line)

    def _highlight_code(self, code: str) -> str:
        """高亮代码部分（不含注释）"""
        import re

        # 高亮字符串
        code = self._highlight_strings(code)

        # 高亮数字
        code = self._highlight_numbers(code)

        # 高亮关键字
        code = self._highlight_keywords(code)

        # 高亮函数名
        code = self._highlight_functions(code)

        return code

    def _highlight_strings(self, code: str) -> str:
        """高亮字符串"""
        import re

        # 匹配单引号字符串
        def replace_single_quote(match):
            return self.string_color + match.group(0) + self.reset_color

        code = re.sub(r"'.*?'", replace_single_quote, code)

        # 匹配双引号字符串
        def replace_double_quote(match):
            return self.string_color + match.group(0) + self.reset_color

        code = re.sub(r'".*?"', replace_double_quote, code)

        return code

    def _highlight_numbers(self, code: str) -> str:
        """高亮数字"""
        import re

        def replace_number(match):
            return self.number_color + match.group(0) + self.reset_color

        # 匹配整数和小数
        code = re.sub(r"\b\d+(\.\d+)?\b", replace_number, code)

        return code

    def _highlight_keywords(self, code: str) -> str:
        """高亮关键字"""
        for keyword, color in self.keyword_colors.items():
            pattern = r"\b" + re.escape(keyword) + r"\b"
            code = re.sub(pattern, color + keyword + self.reset_color, code)

        return code

    def _highlight_functions(self, code: str) -> str:
        """高亮函数名"""
        for func, color in self.function_colors.items():
            pattern = r"\b" + re.escape(func) + r"\b"
            code = re.sub(pattern, color + func + self.reset_color, code)

        return code


# 旧的HistoryManager类已被新的增强版HistoryManager替换
# 新的HistoryManager在history_manager.py中实现，提供更强大的功能：
# - 支持按时间戳、命令类型、标签过滤
# - 支持搜索和编辑历史记录
# - 支持持久化存储和导入导出
# - 支持统计信息


class EnhancedREPL:
    """增强REPL"""

    def __init__(self, compiler, history_file: Optional[str] = None, use_database: bool = False):
        self.compiler = compiler
        self.completion_provider = CodeCompletionProvider(compiler)
        self.syntax_highlighter = SyntaxHighlighter()

        # 使用增强的历史记录管理器
        history_path = Path(history_file) if history_file else Path.home() / ".xinyu_history"
        self.history_manager = HistoryManager(
            max_size=1000, history_file=history_path, use_database=use_database
        )

        self.multiline_buffer: List[str] = []
        self.in_multiline = False
        self.current_history_index = -1
        self.current_input = ""

        # 设置readline补全
        readline.set_completer(self._completer)
        readline.parse_and_bind("tab: complete")

        # 设置readline历史记录（向后兼容）
        if history_file:
            try:
                readline.read_history_file(history_file)
                readline.set_history_length(100)
            except FileNotFoundError:
                pass  # 历史文件不存在是正常的

    def _completer(self, text: str, state: int) -> Optional[str]:
        """readline补全函数"""
        suggestions = self.completion_provider.complete(text, len(text))

        if state < len(suggestions):
            return suggestions[state]
        return None

    def run_interactive(self) -> None:
        """运行交互式REPL会话"""
        print("心语增强REPL (输入 '退出' 或 'exit' 退出，输入 '帮助' 查看帮助)")
        print("支持功能: 语法高亮、代码补全(Tab键)、历史记录(上下箭头)")
        print("-" * 50)

        while True:
            try:
                # 获取用户输入
                code = self._get_input()

                # 检查退出命令
                if code.lower() in ["退出", "exit", "quit"]:
                    print("再见！")
                    break

                # 检查帮助命令
                if code.lower() in ["帮助", "help"]:
                    self._print_help()
                    continue

                # 检查调试命令
                if code.lower().startswith("调试"):
                    self._handle_debug_command(code)
                    continue

                # 检查历史命令
                if code.lower().startswith("历史"):
                    self._handle_history_command(code)
                    continue

                # 执行代码
                if code.strip():
                    result = self.compiler.execute(code)
                    if result is not None:
                        print(f"结果: {result}")

            except KeyboardInterrupt:
                print("\n中断执行")
                self.multiline_buffer.clear()
                self.in_multiline = False
            except EOFError:
                print("\n再见！")
                break
            except Exception as e:
                print(f"错误: {e}")
                # 错误恢复逻辑
                self.multiline_buffer.clear()
                self.in_multiline = False

    def _get_input(self) -> str:
        """获取用户输入，支持多行和补全"""
        if self.in_multiline:
            prompt = "... "
        else:
            prompt = "心语> "

        lines = []
        while True:
            try:
                # 获取输入
                line = input(prompt)

                # 保存当前输入（用于历史记录导航）
                if not self.in_multiline:
                    self.current_input = line

                # 检查是否是多行输入
                if line.endswith("\\"):
                    lines.append(line[:-1])
                    self.in_multiline = True
                    prompt = "... "
                else:
                    lines.append(line)
                    self.in_multiline = False
                    break

            except KeyboardInterrupt:
                # 清除多行缓冲区
                self.multiline_buffer.clear()
                self.in_multiline = False
                raise
            except EOFError:
                raise

        full_code = "\n".join(lines)

        # 添加到历史记录
        if full_code.strip():
            self._add_to_history(full_code)

        return full_code

    def _add_to_history(self, command: str) -> None:
        """添加命令到历史记录"""
        try:
            # 执行命令并获取结果
            start_time = time.time()
            result = self.compiler.execute(command)
            execution_time = time.time() - start_time

            # 添加到历史记录管理器
            self.history_manager.add_entry(
                command=command,
                result=str(result) if result is not None else None,
                execution_time=execution_time,
                success=True,  # 假设执行成功，实际应该根据异常处理
                tags=self._extract_tags(command),
                metadata={"multiline": self.in_multiline, "timestamp": time.time()},
            )

            # 同时添加到readline历史记录（向后兼容）
            readline.add_history(command)

        except Exception as e:
            # 执行失败，但仍然记录
            self.history_manager.add_entry(
                command=command,
                result=f"错误: {e}",
                execution_time=None,
                success=False,
                tags=self._extract_tags(command),
                metadata={
                    "multiline": self.in_multiline,
                    "timestamp": time.time(),
                    "error": str(e),
                },
            )

    def _extract_tags(self, command: str) -> List[str]:
        """从命令中提取标签"""
        tags = []
        command_lower = command.lower()

        # 根据命令内容添加标签
        if "定义" in command:
            tags.append("定义")
        if "如果" in command or "否则" in command:
            tags.append("条件")
        if "循环" in command or "当" in command or "为" in command:
            tags.append("循环")
        if "导入" in command:
            tags.append("导入")
        if "打印" in command:
            tags.append("输出")
        if "输入" in command:
            tags.append("输入")
        if "调试" in command:
            tags.append("调试")

        return tags

    def _print_help(self) -> None:
        """打印帮助信息"""
        help_text = """
心语增强REPL帮助:
  基本命令:
    退出/exit/quit    - 退出REPL
    帮助/help         - 显示此帮助
    调试 <命令>       - 调试命令
    历史 <命令>       - 历史记录管理

  历史记录命令:
    历史 列表 [数量]          - 显示历史记录（默认显示最近10条）
    历史 搜索 <关键词>        - 搜索历史记录
    历史 过滤 <类型>          - 按类型过滤历史记录
    历史 统计                 - 显示历史记录统计信息
    历史 导出 <文件>          - 导出历史记录到文件
    历史 导入 <文件>          - 从文件导入历史记录
    历史 编辑 <编号> <新命令> - 编辑历史记录并重新执行
    历史 清除                 - 清除所有历史记录

  调试命令:
    调试 开始         - 开始调试会话
    调试 停止         - 停止调试会话
    调试 断点 <位置>  - 设置断点
    调试 清除 <ID>    - 清除断点
    调试 列表         - 列出断点
    调试 步过         - 单步执行（步过）
    调试 步入         - 单步执行（步入）
    调试 继续         - 继续执行
    调试 变量         - 查看变量
    调试 调用栈       - 查看调用栈

  快捷键:
    Tab键            - 代码补全
    上箭头/下箭头     - 历史记录导航
    Ctrl+C           - 中断执行
    Ctrl+D           - 退出REPL

  多行输入:
    在行尾输入 \\ 可以继续输入下一行
    空行结束多行输入
        """
        print(help_text.strip())

    def _handle_debug_command(self, command: str) -> None:
        """处理调试命令"""
        # 这里可以集成调试器
        print("调试功能正在开发中...")

    def _handle_history_command(self, command: str) -> None:
        """处理历史命令"""
        parts = command.strip().split()
        if len(parts) < 2:
            self._print_history_help()
            return

        subcommand = parts[1].lower()

        if subcommand == "列表" or subcommand == "list":
            limit = 10
            if len(parts) > 2:
                try:
                    limit = int(parts[2])
                except ValueError:
                    print(f"错误: 无效的数量 '{parts[2]}'")
                    return
            self._list_history(limit)

        elif subcommand == "搜索" or subcommand == "search":
            if len(parts) < 3:
                print("用法: 历史 搜索 <关键词>")
                return
            keyword = " ".join(parts[2:])
            self._search_history(keyword)

        elif subcommand == "过滤" or subcommand == "filter":
            if len(parts) < 3:
                print("用法: 历史 过滤 <类型>")
                print(
                    "可用类型: expression, statement, definition, import, control, debug, help, other"
                )
                return
            command_type = parts[2]
            self._filter_history_by_type(command_type)

        elif subcommand == "统计" or subcommand == "stats":
            self._show_history_stats()

        elif subcommand == "导出" or subcommand == "export":
            if len(parts) < 3:
                print("用法: 历史 导出 <文件路径>")
                return
            filepath = Path(" ".join(parts[2:]))
            self._export_history(filepath)

        elif subcommand == "导入" or subcommand == "import":
            if len(parts) < 3:
                print("用法: 历史 导入 <文件路径>")
                return
            filepath = Path(" ".join(parts[2:]))
            self._import_history(filepath)

        elif subcommand == "编辑" or subcommand == "edit":
            if len(parts) < 4:
                print("用法: 历史 编辑 <编号> <新命令>")
                return
            try:
                index = int(parts[2])
                new_command = " ".join(parts[3:])
                self._edit_history(index, new_command)
            except ValueError:
                print(f"错误: 无效的编号 '{parts[2]}'")

        elif subcommand == "清除" or subcommand == "clear":
            self._clear_history()

        else:
            print(f"未知的历史命令: {subcommand}")
            self._print_history_help()

    def _print_history_help(self) -> None:
        """打印历史命令帮助"""
        help_text = """
历史记录命令帮助:
  历史 列表 [数量]          - 显示历史记录（默认显示最近10条）
  历史 搜索 <关键词>        - 搜索历史记录
  历史 过滤 <类型>          - 按类型过滤历史记录
  历史 统计                 - 显示历史记录统计信息
  历史 导出 <文件>          - 导出历史记录到文件
  历史 导入 <文件>          - 从文件导入历史记录
  历史 编辑 <编号> <新命令> - 编辑历史记录并重新执行
  历史 清除                 - 清除所有历史记录

类型说明:
  expression  - 表达式求值
  statement   - 语句执行
  definition  - 定义（函数、变量等）
  import      - 导入语句
  control     - 控制语句（if、for等）
  debug       - 调试命令
  help        - 帮助命令
  other       - 其他命令
        """
        print(help_text.strip())

    def _list_history(self, limit: int = 10) -> None:
        """显示历史记录列表"""
        entries = list(self.history_manager)[:limit]

        if not entries:
            print("没有历史记录")
            return

        print(f"最近 {len(entries)} 条历史记录:")
        print("-" * 80)

        for i, entry in enumerate(entries):
            timestamp = entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            success = "[成功]" if entry.success else "[失败]"
            exec_time = f"{entry.execution_time:.3f}s" if entry.execution_time else "N/A"

            print(f"{i:3d}. [{timestamp}] [{success}] [{entry.command_type.value}] ({exec_time})")
            print(f"     命令: {entry.command[:60]}{'...' if len(entry.command) > 60 else ''}")
            if entry.result:
                result_preview = entry.result[:40] + ("..." if len(entry.result) > 40 else "")
                print(f"     结果: {result_preview}")
            if entry.tags:
                print(f"     标签: {', '.join(entry.tags)}")
            print()

    def _search_history(self, keyword: str) -> None:
        """搜索历史记录"""
        results = self.history_manager.search(keyword=keyword, limit=20)

        if not results:
            print(f"没有找到包含 '{keyword}' 的历史记录")
            return

        print(f"找到 {len(results)} 条包含 '{keyword}' 的历史记录:")
        print("-" * 80)

        for i, entry in enumerate(results):
            timestamp = entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            success = "[成功]" if entry.success else "[失败]"

            print(f"{i:3d}. [{timestamp}] [{success}] [{entry.command_type.value}]")
            print(f"     命令: {entry.command}")
            if entry.result:
                result_preview = entry.result[:60] + ("..." if len(entry.result) > 60 else "")
                print(f"     结果: {result_preview}")
            print()

    def _filter_history_by_type(self, command_type: str) -> None:
        """按类型过滤历史记录"""
        try:
            cmd_type = CommandType(command_type)
        except ValueError:
            print(f"错误: 无效的命令类型 '{command_type}'")
            print("可用类型: expression, statement, definition, import, control, debug, help, other")
            return

        results = self.history_manager.search(command_type=cmd_type, limit=20)

        if not results:
            print(f"没有找到类型为 '{command_type}' 的历史记录")
            return

        print(f"找到 {len(results)} 条类型为 '{command_type}' 的历史记录:")
        print("-" * 80)

        for i, entry in enumerate(results):
            timestamp = entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            success = "[成功]" if entry.success else "[失败]"

            print(f"{i:3d}. [{timestamp}] [{success}]")
            print(f"     命令: {entry.command[:80]}{'...' if len(entry.command) > 80 else ''}")
            print()

    def _show_history_stats(self) -> None:
        """显示历史记录统计信息"""
        stats = self.history_manager.get_stats()

        print("历史记录统计信息:")
        print("-" * 40)
        print(f"总记录数: {stats['total_entries']}")
        print(f"成功记录: {stats['successful_entries']}")
        print(f"失败记录: {stats['failed_entries']}")
        print(f"成功率: {stats['success_rate']:.1%}")

        if stats["average_execution_time"] > 0:
            print(f"平均执行时间: {stats['average_execution_time']:.3f}秒")

        if stats["type_distribution"]:
            print("\n命令类型分布:")
            for type_name, count in stats["type_distribution"].items():
                percentage = count / stats["total_entries"] * 100
                print(f"  {type_name}: {count} ({percentage:.1f}%)")

        if stats["oldest_entry"]:
            print(f"\n最早记录: {stats['oldest_entry'].strftime('%Y-%m-%d %H:%M:%S')}")

        if stats["newest_entry"]:
            print(f"最新记录: {stats['newest_entry'].strftime('%Y-%m-%d %H:%M:%S')}")

    def _export_history(self, filepath: Path) -> None:
        """导出历史记录到文件"""
        try:
            if filepath.suffix.lower() == ".json":
                self.history_manager.export_json(filepath)
                print(f"历史记录已导出到 JSON 文件: {filepath}")
            elif filepath.suffix.lower() == ".csv":
                self.history_manager.export_csv(filepath)
                print(f"历史记录已导出到 CSV 文件: {filepath}")
            else:
                print("错误: 只支持 .json 或 .csv 格式")
        except Exception as e:
            print(f"导出历史记录失败: {e}")

    def _import_history(self, filepath: Path) -> None:
        """从文件导入历史记录"""
        try:
            if not filepath.exists():
                print(f"错误: 文件不存在: {filepath}")
                return

            if filepath.suffix.lower() == ".json":
                count = self.history_manager.import_json(filepath)
                print(f"从 JSON 文件导入 {count} 条历史记录")
            else:
                print("错误: 只支持 .json 格式导入")
        except Exception as e:
            print(f"导入历史记录失败: {e}")

    def _edit_history(self, index: int, new_command: str) -> None:
        """编辑历史记录并重新执行"""
        entry = self.history_manager.edit_and_reexecute(index, new_command)

        if entry:
            print(f"已编辑历史记录 #{index}:")
            print(f"  新命令: {new_command}")
            print("\n重新执行命令...")

            # 执行新命令
            try:
                result = self.compiler.execute(new_command)
                if result is not None:
                    print(f"结果: {result}")
            except Exception as e:
                print(f"错误: {e}")
        else:
            print(f"错误: 无效的历史记录索引 #{index}")

    def _clear_history(self) -> None:
        """清除所有历史记录"""
        confirm = input("确定要清除所有历史记录吗？(y/N): ")
        if confirm.lower() == "y":
            self.history_manager.clear()
            print("历史记录已清除")
        else:
            print("操作已取消")

    def run_script(self, script_path: str) -> None:
        """运行脚本文件"""
        try:
            with open(script_path, "r", encoding="utf-8") as f:
                code = f.read()

            print(f"运行脚本: {script_path}")
            print("-" * 50)

            # 显示语法高亮
            highlighted = self.syntax_highlighter.highlight(code)
            print(highlighted)
            print("-" * 50)

            # 执行代码
            result = self.compiler.execute(code)
            if result is not None:
                print(f"执行结果: {result}")

        except FileNotFoundError:
            print(f"错误: 文件 '{script_path}' 不存在")
        except Exception as e:
            print(f"错误: {e}")

    def autocomplete(self, text: str, pos: int) -> List[str]:
        """代码自动补全（供外部调用）"""
        return self.completion_provider.complete(text, pos)

    def highlight_code(self, code: str) -> str:
        """语法高亮代码（供外部调用）"""
        return self.syntax_highlighter.highlight(code)
