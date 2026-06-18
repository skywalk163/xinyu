# -*- coding: utf-8 -*-
"""心语语言REPL（交互式解释器）

提供交互式编程环境：
- 实时代码执行
- 命令历史
- 多行输入
- 自动补全
- 特殊命令
"""

import os
import readline  # 支持命令历史和编辑
import sys
from pathlib import Path
from typing import List, Optional


class XinyuREPL:
    """心语语言REPL"""

    def __init__(self):
        """初始化REPL"""
        self.history_file = Path.home() / ".xinyu_history"
        self.variables = {}
        self.functions = {}
        self.running = True

        # 加载命令历史
        self._load_history()

        # 欢迎信息
        self.welcome_message = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   心语 (Xīn Yǔ) - 中文编程语言                            ║
║   版本: 2.0                                               ║
║   输入 .help 查看帮助，.exit 退出                         ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""

    def _load_history(self):
        """加载命令历史"""
        try:
            if self.history_file.exists():
                readline.read_history_file(str(self.history_file))
        except Exception:
            pass

    def _save_history(self):
        """保存命令历史"""
        try:
            readline.write_history_file(str(self.history_file))
        except Exception:
            pass

    def start(self):
        """启动REPL"""
        print(self.welcome_message)

        while self.running:
            try:
                # 读取输入
                line = input("心语> ")

                # 处理特殊命令
                if line.startswith("."):
                    self._handle_command(line)
                    continue

                # 处理空行
                if not line.strip():
                    continue

                # 处理多行输入
                if line.endswith("：") or line.endswith(":"):
                    code = self._read_multiline(line)
                else:
                    code = line

                # 执行代码
                self._execute(code)

            except KeyboardInterrupt:
                print("\n使用 .exit 退出")
            except EOFError:
                print("\n再见！")
                break
            except Exception as e:
                print(f"错误: {e}")

        # 保存历史
        self._save_history()

    def _read_multiline(self, first_line: str) -> str:
        """读取多行输入

        Args:
            first_line: 第一行

        Returns:
            完整的代码
        """
        lines = [first_line]
        print("... ", end="", flush=True)

        while True:
            try:
                line = input()

                # 空行结束多行输入
                if not line.strip():
                    break

                lines.append(line)
                print("... ", end="", flush=True)

            except KeyboardInterrupt:
                print("\n取消多行输入")
                return ""
            except EOFError:
                break

        return "\n".join(lines)

    def _handle_command(self, command: str):
        """处理特殊命令

        Args:
            command: 命令字符串
        """
        cmd = command.strip().lower()

        if cmd == ".exit" or cmd == ".quit":
            print("再见！")
            self.running = False

        elif cmd == ".help":
            self._show_help()

        elif cmd == ".vars" or cmd == ".variables":
            self._show_variables()

        elif cmd == ".funcs" or cmd == ".functions":
            self._show_functions()

        elif cmd == ".clear":
            self._clear()

        elif cmd == ".version":
            print("心语 v2.0")

        elif cmd.startswith(".load "):
            filename = command[6:].strip()
            self._load_file(filename)

        elif cmd.startswith(".save "):
            filename = command[6:].strip()
            self._save_file(filename)

        else:
            print(f"未知命令: {command}")
            print("输入 .help 查看可用命令")

    def _show_help(self):
        """显示帮助信息"""
        help_text = """
心语REPL帮助：

特殊命令：
  .help           显示帮助信息
  .exit           退出REPL
  .quit           退出REPL
  .vars           显示所有变量
  .funcs          显示所有函数
  .clear          清除所有变量和函数
  .version        显示版本信息
  .load <文件>    加载文件
  .save <文件>    保存当前会话

语法示例：
  定义 x = 5。
  函数 平方：
    参数 x。
    返回 x 相乘 x。
  打印 平方 5。

快捷键：
  Ctrl+C          取消当前输入
  Ctrl+D          退出REPL
  ↑/↓             浏览命令历史
  Tab             自动补全（待实现）
"""
        print(help_text)

    def _show_variables(self):
        """显示所有变量"""
        if not self.variables:
            print("没有定义变量")
            return

        print("变量列表：")
        for name, value in self.variables.items():
            print(f"  {name} = {value}")

    def _show_functions(self):
        """显示所有函数"""
        if not self.functions:
            print("没有定义函数")
            return

        print("函数列表：")
        for name, info in self.functions.items():
            params = info.get("params", [])
            print(f"  {name}({', '.join(params)})")

    def _clear(self):
        """清除所有变量和函数"""
        self.variables.clear()
        self.functions.clear()
        print("已清除所有变量和函数")

    def _load_file(self, filename: str):
        """加载文件

        Args:
            filename: 文件名
        """
        try:
            filepath = Path(filename)
            if not filepath.exists():
                print(f"文件不存在: {filename}")
                return

            with open(filepath, "r", encoding="utf-8") as f:
                code = f.read()

            print(f"加载文件: {filename}")
            self._execute(code)

        except Exception as e:
            print(f"加载文件失败: {e}")

    def _save_file(self, filename: str):
        """保存当前会话

        Args:
            filename: 文件名
        """
        try:
            code_lines = []

            # 保存变量
            for name, value in self.variables.items():
                code_lines.append(f"定义 {name} = {value}。")

            # 保存函数
            for name, info in self.functions.items():
                params = info.get("params", [])
                body = info.get("body", "")
                params_str = " ".join(params)
                code_lines.append(f"定义 {name} = 函数 {params_str}：")
                code_lines.append(f"  {body}")

            with open(filename, "w", encoding="utf-8") as f:
                f.write("\n".join(code_lines))

            print(f"已保存到: {filename}")

        except Exception as e:
            print(f"保存文件失败: {e}")

    def _execute(self, code: str):
        """执行代码

        Args:
            code: 代码字符串
        """
        try:
            # 导入必要的模块
            from src.codegen.python_codegen import PythonCodegen
            from src.lexer.lexer import Lexer
            from src.parser.parser import Parser

            # 词法分析
            lexer = Lexer(code)
            tokens = lexer.tokenize()

            # 语法分析
            parser = Parser(tokens)
            ast = parser.parse()

            # 代码生成
            codegen = PythonCodegen()
            python_code = codegen.generate(ast)

            # 执行Python代码
            exec_globals = {
                "__builtins__": __builtins__,
                **self.variables,
            }
            exec(python_code, exec_globals)

            # 更新变量
            for key, value in exec_globals.items():
                if not key.startswith("_"):
                    self.variables[key] = value

        except Exception as e:
            print(f"执行错误: {e}")


def main():
    """主函数"""
    repl = XinyuREPL()
    repl.start()


if __name__ == "__main__":
    main()
