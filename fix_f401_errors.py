#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复F401错误（未使用的导入）
"""

import os
import re
import ast
from pathlib import Path

def remove_unused_imports(filepath):
    """移除单个文件中未使用的导入"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        tree = ast.parse(content)
    except SyntaxError:
        print(f"语法错误，跳过文件: {filepath}")
        return False
    
    # 收集所有使用的名称
    used_names = set()
    
    class NameCollector(ast.NodeVisitor):
        def visit_Name(self, node):
            used_names.add(node.id)
            self.generic_visit(node)
        
        def visit_Attribute(self, node):
            # 处理属性访问，如 module.name
            if isinstance(node.value, ast.Name):
                used_names.add(node.value.id)
            self.generic_visit(node)
    
    collector = NameCollector()
    collector.visit(tree)
    
    # 分析导入语句
    imports_to_keep = []
    imports_to_remove = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in used_names or alias.asname in used_names:
                    imports_to_keep.append(node)
                    break
                else:
                    imports_to_remove.append((node.lineno, alias.name))
        
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                full_name = f"{module}.{alias.name}" if module else alias.name
                if alias.name in used_names or alias.asname in used_names:
                    imports_to_keep.append(node)
                    break
                else:
                    imports_to_remove.append((node.lineno, full_name))
    
    if not imports_to_remove:
        return False
    
    # 重新构建文件内容
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines, 1):
        keep_line = True
        for lineno, import_name in imports_to_remove:
            if i == lineno:
                # 检查是否是这一行的导入
                if f"import {import_name}" in line or f"from {import_name.split('.')[0]}" in line:
                    keep_line = False
                    break
        
        if keep_line:
            new_lines.append(line)
        else:
            print(f"  移除未使用的导入: {line.strip()}")
    
    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(new_lines))
    
    return True

def fix_common_unused_imports(filepath):
    """修复常见的未使用导入模式"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    modified = False
    
    # 常见的未使用导入模式
    patterns_to_remove = [
        # typing模块
        (r'^from typing import (List|Dict|Tuple|Optional|Any|Union|Callable|Type)(,.*)?$', 
         lambda m: not any(name in content for name in ['List', 'Dict', 'Tuple', 'Optional', 'Any', 'Union', 'Callable', 'Type'])),
        # 标准库
        (r'^import (sys|os|re|json|pathlib|inspect|gc|time|atexit|gzip|ast|types)(,.*)?$',
         lambda m: not any(name in content for name in ['sys', 'os', 're', 'json', 'pathlib', 'inspect', 'gc', 'time', 'atexit', 'gzip', 'ast', 'types'])),
    ]
    
    new_lines = []
    for line in lines:
        original_line = line
        remove = False
        
        for pattern, check_func in patterns_to_remove:
            match = re.match(pattern, line.strip())
            if match:
                if check_func(match):
                    remove = True
                    modified = True
                    print(f"  移除未使用的导入: {line.strip()}")
                    break
        
        if not remove:
            new_lines.append(line)
    
    if modified:
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(new_lines))
    
    return modified

def main():
    # 修复src目录下的文件
    src_dir = Path("src")
    
    files_fixed = 0
    
    # 先使用简单规则修复
    for filepath in src_dir.rglob("*.py"):
        if fix_common_unused_imports(filepath):
            files_fixed += 1
            print(f"修复了 {filepath}")
    
    # 然后使用AST分析修复
    for filepath in src_dir.rglob("*.py"):
        if remove_unused_imports(filepath):
            files_fixed += 1
            print(f"AST分析修复了 {filepath}")
    
    print(f"\n总共修复了 {files_fixed} 个文件中的F401错误")

if __name__ == "__main__":
    main()