# -*- coding: utf-8 -*-
"""心语语言主入口

提供完整的编译流程：
- 词法分析 → 语法分析 → 语义分析 → 代码生成 → 执行

支持两种运行模式：
- 交互式模式：REPL
- 文件模式：执行.心语文件
"""

import sys
import os
from typing import Any, Dict, Optional, NoReturn

from src.lexer.lexer import Lexer, LexerError
from src.parser.parser import Parser, ParseError
from src.semantic.analyzer import SemanticAnalyzer, SemanticError
from src.codegen.python_codegen import PythonCodegen, CodegenError


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
    
    def __init__(self):
        """初始化心语语言环境"""
        self.env = self._create_exec_globals()
    
    def run(self, source: str) -> Optional[Any]:
        """编译并执行心语代码
        
        Args:
            source: 心语源代码
            
        Returns:
            执行结果（如果有），或 None（如果出错）
            
        Security Warning:
            本方法使用 exec() 执行生成的 Python 代码。
            请勿执行不可信的代码来源，可能存在安全风险。
            在生产环境中，建议：
            1. 仅执行经过审查的代码
            2. 使用沙箱环境隔离执行
            3. 限制可用的模块和函数
        """
        try:
            # 1. 词法分析
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            
            # 2. 语法分析
            parser = Parser(tokens)
            ast = parser.parse()
            
            # 3. 语义分析
            analyzer = SemanticAnalyzer()
            if not analyzer.analyze(ast):
                for error in analyzer.errors:
                    print(f"语义错误: {error.message} (行 {error.line}, 列 {error.column})")
                return None
            
            # 4. 代码生成
            codegen = PythonCodegen()
            python_code = codegen.generate(ast)
            
            # 5. 执行
            exec_globals = self._create_exec_globals()
            exec(python_code, exec_globals)
            
            return exec_globals.get('__result__')
            
        except LexerError as e:
            print(f"词法错误: {e.message} (行 {e.line}, 列 {e.column})")
            return None
        except ParseError as e:
            print(f"语法错误: {e.message} (行 {e.token.line}, 列 {e.token.column})")
            return None
        except CodegenError as e:
            print(f"代码生成错误: {e}")
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
            # 1. 词法分析
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            
            # 2. 语法分析
            parser = Parser(tokens)
            ast = parser.parse()
            
            # 3. 语义分析（可选，只检查错误）
            analyzer = SemanticAnalyzer()
            if not analyzer.analyze(ast):
                for error in analyzer.errors:
                    print(f"语义警告: {error.message} (行 {error.line}, 列 {error.column})")
            
            # 4. 代码生成
            codegen = PythonCodegen()
            python_code = codegen.generate(ast)
            
            return python_code
            
        except (LexerError, ParseError, CodegenError) as e:
            print(f"编译错误: {e}")
            return ""
    
    def _create_exec_globals(self) -> Dict[str, Any]:
        """创建执行环境
        
        包含：
        - Python 内置函数
        - Python 标准模块（math, random, json, re, datetime）
        - 心语内置函数
        
        Returns:
            执行环境字典
        """
        import math
        import random
        import json
        import re
        from datetime import datetime, date, time, timedelta
        
        # 基础环境
        exec_globals = {
            '__builtins__': __builtins__,
            '__name__': '__main__',
            '__doc__': None,
            '__package__': None,
            '__loader__': None,
            '__spec__': None,
        }
        
        # Python 标准模块
        exec_globals['math'] = math
        exec_globals['random'] = random
        exec_globals['json'] = json
        exec_globals['re'] = re
        exec_globals['datetime'] = datetime
        exec_globals['date'] = date
        exec_globals['time'] = time
        exec_globals['timedelta'] = timedelta
        
        # 心语内置值
        exec_globals['真'] = True
        exec_globals['假'] = False
        
        return exec_globals


def main() -> None:
    """主函数：支持交互式模式和文件模式"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='心语语言 - 极简中文编程语言',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例：
  python -m src.main                    # 交互式模式
  python -m src.main program.心语       # 执行文件
  python -m src.main -c '印"你好"。'    # 执行代码
  python -m src.main --compile program.心语  # 编译为 Python
        '''
    )
    
    parser.add_argument(
        'file',
        nargs='?',
        help='要执行的心语文件'
    )
    
    parser.add_argument(
        '-c', '--code',
        help='直接执行代码字符串'
    )
    
    parser.add_argument(
        '--compile',
        action='store_true',
        help='只编译为 Python 代码，不执行'
    )
    
    args = parser.parse_args()
    
    program = ChineseProgram()
    
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
            with open(args.file, 'r', encoding='utf-8') as f:
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
    
    # 交互式模式（REPL）
    print(WELCOME_MESSAGE)
    print()
    
    while True:
        try:
            # 读取输入
            line = input(REPL_PROMPT)
            
            # 检查退出命令
            if line.strip() in ('退出', 'exit', 'quit'):
                print("再见！")
                break
            
            # 检查帮助命令
            if line.strip() in ('帮助', 'help'):
                print_help()
                continue
            
            # 执行代码
            if line.strip():
                program.run(line)
        
        except EOFError:
            print("\n再见！")
            break
        except KeyboardInterrupt:
            print("\n使用 '退出' 或 'exit' 退出")
        except Exception as e:
            print(f"错误：{e}")


def print_help() -> None:
    """打印帮助信息"""
    help_text = '''
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
'''
    print(help_text)


if __name__ == '__main__':
    main()
