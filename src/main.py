# -*- coding: utf-8 -*-
"""心语语言主入口

提供完整的编译流程：
- 词法分析 → 语法分析 → 语义分析 → 代码生成 → 执行

支持两种运行模式：
- 交互式模式：REPL
- 文件模式：执行.心语文件
"""

import os
import sys
from typing import Any, Dict, Optional

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.compiler import CompilationError, XinyuCompiler
from src.repl import EnhancedREPL
from src.runtime.secure_executor import SecureExecutor

# 常量定义
VERSION = "1.0"
REPL_PROMPT = "心语> "
WELCOME_MESSAGE = f"""心语语言 v{VERSION}
输入 '退出' 或 'exit' 退出
输入 '帮助' 或 'help' 查看帮助
"""


class ChineseProgram:
    """心语语言主类

    提供完整的编译和执行功能。

    属性：
        env: 执行环境（包含内置模块和函数）
    """

    def __init__(self, enable_safety: bool = True):
        """初始化心语语言环境

        Args:
            enable_safety: 是否启用安全限制
        """
        self.enable_safety = enable_safety
        self.compiler = XinyuCompiler(enable_safety=enable_safety)
        self.runtime = SecureExecutor() if enable_safety else None

    def run(self, source: str) -> Optional[Any]:
        """编译并执行心语代码

        Args:
            source: 心语源代码

        Returns:
            执行结果（如果有），或 None（如果出错）

        Security Warning:
            本方法使用安全执行器执行生成的 Python 代码。
            如果启用安全限制，会限制可用的模块和函数。
        """
        try:
            # 使用编译器进行编译
            result = self.compiler.execute(source)
            return result

        except CompilationError as e:
            print(f"编译错误: {e}")
            return None
        except Exception as e:
            print(f"运行时错误: {e}")
            return None

    def compile(self, source: str) -> str:
        """编译心语代码为 Python 代码

        Args:
            source: 心语源代码

        Returns:
            生成的 Python 代码字符串，如果出错则返回空字符串
        """
        try:
            python_code = self.compiler.compile(source)

            # 输出诊断信息
            for diagnostic in self.compiler.get_diagnostics():
                print(diagnostic)

            return python_code

        except CompilationError as e:
            print(f"编译错误: {e}")
            return ""

    def _create_exec_globals(self) -> Dict[str, Any]:
        """创建执行环境（已弃用，使用安全执行器替代）

        注意：此方法已不再使用，保留用于向后兼容。
        新的实现使用 SecureExecutor 提供安全执行环境。
        """
        import warnings

        warnings.warn(
            "_create_exec_globals 已弃用，请使用 SecureExecutor", DeprecationWarning, stacklevel=2
        )

        # 返回空字典，实际执行由 SecureExecutor 处理
        return {}


def main() -> None:
    """主函数：支持交互式模式和文件模式"""
    import argparse

    parser = argparse.ArgumentParser(
        description="心语语言 - 极简中文编程语言",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python -m src.main                    # 交互式模式（安全）
  python -m src.main program.心语       # 执行文件（安全）
  python -m src.main -c '印"你好"。'    # 执行代码（安全）
  python -m src.main --compile program.心语  # 编译为 Python
  python -m src.main --unsafe program.心语  # 禁用安全限制（不推荐）
        """,
    )

    parser.add_argument("file", nargs="?", help="要执行的心语文件")

    parser.add_argument("-c", "--code", help="直接执行代码字符串")

    parser.add_argument("--compile", action="store_true", help="只编译为 Python 代码，不执行")

    parser.add_argument("--unsafe", action="store_true", help="禁用安全限制（不推荐）")

    args = parser.parse_args()

    # 根据参数决定是否启用安全限制
    enable_safety = not args.unsafe
    if not enable_safety:
        print("⚠️  警告：已禁用安全限制，可能存在安全风险！")

    program = ChineseProgram(enable_safety=enable_safety)

    # 直接执行代码字符串
    if args.code:
        if args.compile:
            python_code = program.compile(args.code)
            print(python_code)
        else:
            program.run(args.code)
        return

    # 执行文件
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                source = f.read()

            if args.compile:
                python_code = program.compile(source)
                print(python_code)
            else:
                program.run(source)
        except FileNotFoundError:
            print(f"错误：文件 '{args.file}' 不存在")
        except Exception as e:
            print(f"错误：{e}")
        return

    # 交互式模式（增强REPL）
    print(WELCOME_MESSAGE)
    print("提示: 使用增强REPL，支持语法高亮、代码补全和历史记录")
    print("-" * 50)

    # 创建增强REPL
    repl = EnhancedREPL(program.compiler, history_file=".xinyu_history")

    # 运行REPL
    repl.run_interactive()


def print_help() -> None:
    """打印帮助信息"""
    help_text = """
心语语言帮助

核心关键字（5个）：
  定 - 定义变量或函数
  函 - 定义函数
  若 - 条件判断
  遍历 - 遍历循环
  返回 - 返回值

语法标记：
  则 - if 的 then 分支
  否则 - if 的 else 分支
  当 - while 循环
  重复 - repeat 循环
  次 - repeat 的次数标记

操作符：
  加、减、乘、除以 - 算术运算
  大于、小于、等于、不等于 - 比较运算
  且、或、非 - 逻辑运算

示例：
  定 x = 5。
  印x。

  定 加法 = 函 a b：
      返回 a 加 b。

  若 x 大于 0 则：
      印"正数"。
  否则：
      印"非正数"。

  遍历 i 于 [1, 2, 3]：
      印i。
"""
    print(help_text)


if __name__ == "__main__":
    main()
