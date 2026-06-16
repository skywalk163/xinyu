#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""心语代码格式化命令行工具

用法:
    python xinyu_format.py [选项] <文件或目录>...

选项:
    --check, -c      只检查不修改
    --in-place, -i   直接修改文件
    --config FILE    配置文件路径
    --verbose, -v    详细输出
    --help, -h       显示帮助信息
    --version        显示版本信息

示例:
    # 检查文件格式
    python xinyu_format.py --check example.xinyu
    
    # 格式化文件
    python xinyu_format.py --in-place example.xinyu
    
    # 格式化目录下所有.xinyu文件
    python xinyu_format.py --in-place src/
    
    # 使用自定义配置
    python xinyu_format.py --config .xinyu-formatter.yaml example.xinyu
"""

import argparse
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from tools.formatter import XinyuFormatter, FormatterConfig
except ImportError:
    # 如果导入失败，尝试直接导入
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from formatter import XinyuFormatter, FormatterConfig


def find_xinyu_files(paths):
    """查找所有.xinyu文件"""
    xinyu_files = []
    
    for path_str in paths:
        path = Path(path_str)
        
        if not path.exists():
            print(f"警告: 路径不存在: {path}", file=sys.stderr)
            continue
        
        if path.is_file():
            if path.suffix == '.xinyu':
                xinyu_files.append(path)
            else:
                print(f"警告: 不是.xinyu文件: {path}", file=sys.stderr)
        elif path.is_dir():
            # 递归查找所有.xinyu文件
            for file_path in path.rglob('*.xinyu'):
                xinyu_files.append(file_path)
        else:
            print(f"警告: 不是文件或目录: {path}", file=sys.stderr)
    
    return xinyu_files


def format_files(files, formatter, in_place=False, check_only=False, verbose=False):
    """格式化文件"""
    changed_files = 0
    total_issues = 0
    
    for file_path in files:
        try:
            if check_only:
                # 只检查格式
                with open(file_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                
                issues = formatter.check_format(source)
                if issues:
                    print(f"{file_path}:")
                    for issue in issues:
                        print(f"  {issue}")
                    total_issues += len(issues)
                elif verbose:
                    print(f"{file_path}: ✓ 格式正确")
            
            elif in_place:
                # 直接修改文件
                changed = formatter.apply_format(file_path)
                if changed:
                    print(f"✓ 已格式化: {file_path}")
                    changed_files += 1
                elif verbose:
                    print(f"✓ 无需修改: {file_path}")
            
            else:
                # 输出格式化后的代码到标准输出
                with open(file_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                
                formatted = formatter.format_code(source)
                print(f"# {file_path}")
                print(formatted)
                print()  # 文件间空行
        
        except Exception as e:
            print(f"✗ 处理文件失败 {file_path}: {e}", file=sys.stderr)
    
    return changed_files, total_issues


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='心语代码格式化工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        'paths',
        nargs='+',
        help='要格式化的文件或目录'
    )
    
    parser.add_argument(
        '--check', '-c',
        action='store_true',
        help='只检查不修改'
    )
    
    parser.add_argument(
        '--in-place', '-i',
        action='store_true',
        help='直接修改文件'
    )
    
    parser.add_argument(
        '--config',
        help='配置文件路径（默认: .xinyu-formatter.yaml）'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='详细输出'
    )
    
    parser.add_argument(
        '--version',
        action='store_true',
        help='显示版本信息'
    )
    
    args = parser.parse_args()
    
    # 显示版本信息
    if args.version:
        print("心语代码格式化工具 v1.0.0")
        return 0
    
    # 验证参数
    if args.check and args.in_place:
        print("错误: --check 和 --in-place 不能同时使用", file=sys.stderr)
        return 1
    
    # 加载配置
    config_path = args.config or '.xinyu-formatter.yaml'
    config = FormatterConfig()
    
    if Path(config_path).exists():
        try:
            config = FormatterConfig.from_yaml(config_path)
            if args.verbose:
                print(f"使用配置文件: {config_path}")
        except Exception as e:
            print(f"警告: 加载配置文件失败 {config_path}: {e}", file=sys.stderr)
            print("使用默认配置", file=sys.stderr)
    elif args.config:
        print(f"警告: 配置文件不存在: {config_path}", file=sys.stderr)
        print("使用默认配置", file=sys.stderr)
    
    # 创建格式化器
    formatter = XinyuFormatter(config)
    
    # 查找文件
    xinyu_files = find_xinyu_files(args.paths)
    
    if not xinyu_files:
        print("错误: 没有找到.xinyu文件", file=sys.stderr)
        return 1
    
    if args.verbose:
        print(f"找到 {len(xinyu_files)} 个.xinyu文件")
    
    # 处理文件
    changed_files, total_issues = format_files(
        xinyu_files,
        formatter,
        in_place=args.in_place,
        check_only=args.check,
        verbose=args.verbose
    )
    
    # 输出统计信息
    if args.check:
        if total_issues > 0:
            print(f"\n发现 {total_issues} 个格式问题")
            return 1
        else:
            print(f"\n所有文件格式正确")
            return 0
    elif args.in_place:
        print(f"\n已格式化 {changed_files} 个文件")
        return 0
    else:
        # 输出到标准输出，不显示统计信息
        return 0


if __name__ == '__main__':
    sys.exit(main())