# -*- coding: utf-8 -*-
"""修复重复替换问题

修复批量替换脚本导致的重复替换问题。
"""

import re
from pathlib import Path

# 重复替换修复规则
FIXES = {
    # 修复重复的关键字
    '定义义': '定义',
    '函数数': '函数',
    '真值值': '真值',
    '假值值': '假值',
    '当满足满足': '当满足',
    
    # 修复重复的操作符
    '相相加': '相加',
    '相相减': '相减',
    '相相乘': '相乘',
    '相相除': '相除',
    
    # 修复注释中的重复
    '（定义义': '（定义',
    '（函数数': '（函数',
    '（真值值': '（真值',
    '（假值值': '（假值',
}

def fix_file(file_path: Path) -> tuple:
    """修复文件中的重复替换
    
    Args:
        file_path: 文件路径
        
    Returns:
        (是否修改, 修改次数)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        count = 0
        
        for wrong, correct in FIXES.items():
            if wrong in content:
                occurrences = content.count(wrong)
                count += occurrences
                content = content.replace(wrong, correct)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, count
        
        return False, 0
    
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return False, 0

def fix_all_files():
    """修复所有文件"""
    # 修复测试文件
    tests_dir = Path('g:/dumategithub/chineseprogram/tests')
    test_files = list(tests_dir.glob('test_*.py'))
    
    # 修复示例文件
    examples_dir = Path('g:/dumategithub/chineseprogram/examples')
    example_files = list(examples_dir.rglob('*.yan'))
    
    all_files = test_files + example_files
    
    total_files = 0
    total_fixes = 0
    
    print("=== 开始修复重复替换问题 ===\n")
    
    for file_path in all_files:
        modified, count = fix_file(file_path)
        
        if modified:
            total_files += 1
            total_fixes += count
            print(f"[FIX] {file_path.name}: {count} 处修复")
    
    print(f"\n=== 修复完成 ===")
    print(f"修改文件数: {total_files}")
    print(f"总修复次数: {total_fixes}")

if __name__ == '__main__':
    fix_all_files()
    print("\n[OK] 所有文件修复完成！")
