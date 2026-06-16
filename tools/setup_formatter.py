#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""设置心语代码格式化工具

安装和配置格式化工具到开发环境。
"""

import os
import sys
import shutil
from pathlib import Path


def setup_formatter():
    """设置格式化工具"""
    print("设置心语代码格式化工具...")
    
    # 检查当前目录
    current_dir = Path.cwd()
    print(f"当前目录: {current_dir}")
    
    # 检查必要的文件
    required_files = [
        'tools/simple_formatter.py',
        'tools/xinyu_format.py',
        '.xinyu-formatter.yaml',
        '.pre-commit-config.yaml'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not (current_dir / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"警告: 缺少以下文件: {missing_files}")
        print("请确保所有必要的文件都存在。")
        return False
    
    print("所有必要文件都存在")
    
    # 创建符号链接或复制文件到可执行路径
    try:
        # 在Unix-like系统上创建符号链接，在Windows上复制文件
        if sys.platform == 'win32':
            # Windows: 复制文件到Scripts目录
            scripts_dir = Path(sys.prefix) / 'Scripts'
            if scripts_dir.exists():
                formatter_exe = scripts_dir / 'xinyu-format.exe'
                # 创建批处理文件
                batch_content = f'''@echo off
python "{current_dir / 'tools/xinyu_format.py'}" %*
'''
                with open(formatter_exe, 'w', encoding='utf-8') as f:
                    f.write(batch_content)
                print(f"创建格式化工具可执行文件: {formatter_exe}")
            else:
                print("未找到Scripts目录，跳过可执行文件创建")
        else:
            # Unix-like: 创建符号链接
            bin_dir = Path.home() / '.local' / 'bin'
            bin_dir.mkdir(parents=True, exist_ok=True)
            
            formatter_link = bin_dir / 'xinyu-format'
            if formatter_link.exists():
                formatter_link.unlink()
            
            # 创建可执行脚本
            script_content = f'''#!/usr/bin/env python3
import sys
sys.path.insert(0, '{current_dir}')
from tools.xinyu_format import main

if __name__ == '__main__':
    sys.exit(main())
'''
            
            with open(formatter_link, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            # 设置执行权限
            formatter_link.chmod(0o755)
            print(f"创建格式化工具符号链接: {formatter_link}")
        
        # 安装预提交钩子
        print("\n安装预提交钩子...")
        try:
            import subprocess
            result = subprocess.run(
                ['pre-commit', 'install'],
                capture_output=True,
                text=True,
                cwd=current_dir
            )
            
            if result.returncode == 0:
                print("预提交钩子安装成功")
            else:
                print(f"预提交钩子安装失败: {result.stderr}")
                print("请手动运行: pre-commit install")
        
        except FileNotFoundError:
            print("pre-commit未安装，跳过预提交钩子安装")
            print("请安装pre-commit: pip install pre-commit")
        
        # 创建使用说明
        print("\n" + "=" * 60)
        print("心语代码格式化工具设置完成！")
        print("=" * 60)
        print("\n使用方法:")
        print("1. 格式化单个文件:")
        print("   python tools/xinyu_format.py --in-place 文件.xinyu")
        print("")
        print("2. 检查格式问题:")
        print("   python tools/xinyu_format.py --check 文件.xinyu")
        print("")
        print("3. 格式化目录下所有文件:")
        print("   python tools/xinyu_format.py --in-place 目录/")
        print("")
        print("4. 使用自定义配置:")
        print("   python tools/xinyu_format.py --config 配置文件.yaml 文件.xinyu")
        print("")
        print("5. 预提交钩子:")
        print("   - 提交前自动检查格式: pre-commit run --all-files")
        print("   - 自动修复格式问题: git add 文件.xinyu && pre-commit run xinyu-format-fix")
        print("")
        print("配置说明:")
        print("   - 默认配置文件: .xinyu-formatter.yaml")
        print("   - 可配置项: 行长度、缩进大小、引号风格等")
        print("")
        print("示例配置:")
        print('''   line_length: 100
   indent_size: 4
   quote_style: "double"
   trailing_comma: true
   max_empty_lines: 2''')
        print("\n" + "=" * 60)
        
        return True
        
    except Exception as e:
        print(f"设置失败: {e}")
        return False


def create_example_config():
    """创建示例配置文件"""
    config_content = '''# 心语代码格式化配置
# 此文件用于配置心语代码格式化工具的规则

# 行长度限制
line_length: 100

# 缩进大小（空格数）
indent_size: 4

# 引号风格：single（单引号）或 double（双引号）
quote_style: "double"

# 是否在多行结构中添加尾随逗号
trailing_comma: true

# 最大连续空行数
max_empty_lines: 2

# 操作符周围添加空格
spaces_around_operators: true

# 逗号后添加空格
spaces_after_comma: true

# 冒号后添加空格
spaces_after_colon: true

# 自定义规则
custom_rules:
  # 函数定义和调用中的空格
  function_spacing: true
  
  # 列表和字典中的空格
  collection_spacing: true
  
  # 注释格式
  comment_format: true
  
  # 导入语句排序
  import_sorting: true
  
  # 空行位置规则
  blank_line_rules:
    # 在函数定义前添加空行
    before_function: true
    
    # 在类定义前添加空行
    before_class: true
    
    # 在导入语句后添加空行
    after_imports: true
    
    # 在逻辑块之间添加空行
    between_blocks: true

# 文件排除模式
exclude_patterns:
  - "**/__pycache__/**"
  - "**/.git/**"
  - "**/.venv/**"
  - "**/venv/**"
  - "**/node_modules/**"
  - "**/dist/**"
  - "**/build/**"

# 文件包含模式（默认：所有 .xinyu 文件）
include_patterns:
  - "**/*.xinyu"

# 格式化模式
# auto: 自动检测并应用最佳格式
# strict: 严格模式，强制所有规则
# minimal: 最小化模式，只应用基本规则
format_mode: "auto"

# 是否在格式化时保留原始文件的换行符
preserve_line_breaks: false

# 是否在格式化时保留原始文件的注释位置
preserve_comment_positions: true

# 错误处理级别
# error: 遇到错误时停止
# warn: 显示警告但继续
# ignore: 忽略错误
error_level: "warn"
'''
    
    config_file = Path('.xinyu-formatter.yaml')
    if not config_file.exists():
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config_content)
        print(f"创建示例配置文件: {config_file}")
        return True
    else:
        print(f"配置文件已存在: {config_file}")
        return False


if __name__ == '__main__':
    print("=" * 60)
    print("心语代码格式化工具设置")
    print("=" * 60)
    
    # 创建示例配置
    create_example_config()
    
    # 设置格式化工具
    success = setup_formatter()
    
    if success:
        print("\n设置完成！")
        sys.exit(0)
    else:
        print("\n设置失败")
        sys.exit(1)