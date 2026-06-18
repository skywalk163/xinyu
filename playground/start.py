#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""心语 Playground 启动脚本

支持自定义端口配置：
    python start.py              # 默认端口5000
    python start.py 8080         # 使用端口8080
    python start.py --port 3000  # 使用端口3000
"""

import argparse
import os
import sys

# 确保能找到项目模块
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 切换到playground目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 启动服务器
from server import app


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="心语 Playground - 中文编程语言在线体验",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python start.py              # 默认端口5000
    python start.py 8080         # 使用端口8080
    python start.py --port 3000  # 使用端口3000
    python start.py -p 8000      # 使用端口8000
        """,
    )

    parser.add_argument("port_positional", nargs="?", type=int, default=None, help="端口号（位置参数）")

    parser.add_argument("-p", "--port", type=int, default=5000, help="端口号（默认：5000）")

    parser.add_argument("--host", default="0.0.0.0", help="主机地址（默认：0.0.0.0）")

    parser.add_argument("--no-debug", action="store_true", help="禁用调试模式")

    args = parser.parse_args()

    # 位置参数优先级更高
    if args.port_positional is not None:
        args.port = args.port_positional

    return args


if __name__ == "__main__":
    args = parse_args()

    print("=" * 60)
    print("心语 Playground - 中文编程语言在线体验")
    print("=" * 60)
    print()
    print(f"访问地址: http://localhost:{args.port}")
    if args.host != "0.0.0.0":
        print(f"主机地址: {args.host}")
    print()
    print("功能:")
    print("  [OK] 在线编写和执行心语代码")
    print("  [OK] 查看语法文档")
    print("  [OK] 加载示例代码")
    print("  [OK] 实时输出结果")
    print()
    print("快捷键:")
    print("  Ctrl+Enter - 运行代码")
    print("  Esc - 关闭文档")
    print()
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    print()

    debug_mode = not args.no_debug
    app.run(host=args.host, port=args.port, debug=debug_mode)
