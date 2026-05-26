#!/usr/bin/env python3
"""
心语 (Xīn Yǔ) 中文编程语言 - 代码质量检查脚本
用法: python quality_check.py
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def run_command(cmd, cwd=None):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd or Path.cwd(),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

def check_imports():
    """检查Python导入"""
    print("检查Python导入...")
    modules = [
        ("Lexer", "from src.lexer.lexer import Lexer"),
        ("Parser", "from src.parser.parser import Parser"),
        ("SemanticAnalyzer", "from src.semantic.analyzer import SemanticAnalyzer"),
        ("PythonCodegen", "from src.codegen.python_codegen import PythonCodegen"),
    ]
    
    all_ok = True
    for name, import_stmt in modules:
        cmd = ["python", "-c", f"{import_stmt}; print('OK: {name}')"]
        returncode, stdout, stderr = run_command(cmd)
        if returncode == 0:
            print(f"  [OK] {name} 导入成功")
        else:
            print(f"  [FAIL] {name} 导入失败: {stderr[:100]}")
            all_ok = False
    
    return all_ok

def run_tests():
    """运行测试"""
    print("\n运行测试...")
    returncode, stdout, stderr = run_command([
        "python", "-m", "pytest", "tests/", "-q", "--tb=no"
    ])
    
    if returncode == 0:
        print("  [OK] 所有测试通过")
        return True, 0, 0
    
    # 解析输出
    lines = stdout.split('\n')
    for line in lines:
        if "failed" in line and "passed" in line:
            print(f"  测试结果: {line}")
            # 提取数字
            import re
            match = re.search(r'(\d+)\s+failed,\s+(\d+)\s+passed', line)
            if match:
                failed = int(match.group(1))
                passed = int(match.group(2))
                print(f"  通过: {passed}, 失败: {failed}")
                return False, passed, failed
    
    print(f"  输出: {stdout[:200]}...")
    return False, 0, 0

def check_trailing_whitespace():
    """检查尾部空白"""
    print("\n检查尾部空白...")
    
    # 检查主要文件
    files = [
        "src/lexer/lexer.py",
        "src/parser/parser.py",
        "src/semantic/analyzer.py",
        "src/codegen/python_codegen.py",
        "src/main.py"
    ]
    
    issues = []
    for file in files:
        file_path = Path(file)
        if not file_path.exists():
            continue
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        trailing_lines = []
        for i, line in enumerate(lines, 1):
            if line.rstrip() + '\n' != line and line.strip():
                trailing_lines.append(i)
        
        if trailing_lines:
            issues.append(f"{file}: 行 {trailing_lines[:5]}")
            print(f"  [FAIL] {file}: 有尾部空白 (行 {trailing_lines[:5]})")
        else:
            print(f"  [OK] {file}: 无尾部空白")
    
    return len(issues) == 0, issues

def main():
    """主函数"""
    print("="*50)
    print("心语 (Xīn Yǔ) - 代码质量检查")
    print("="*50)
    
    start_time = time.time()
    
    # 1. 检查导入
    if not check_imports():
        print("\n[FAIL] 导入检查失败，无法继续")
        return 1
    
    # 2. 检查尾部空白
    whitespace_ok, issues = check_trailing_whitespace()
    
    # 3. 运行测试
    tests_ok, passed, failed = run_tests()
    
    end_time = time.time()
    
    print("\n" + "="*50)
    print("检查结果")
    print("="*50)
    
    print(f"1. 导入检查: [OK] 通过")
    print(f"2. 尾部空白: [OK] 通过" if whitespace_ok else f"[FAIL] 失败 ({len(issues)} 个文件)")
    if issues:
        for issue in issues[:3]:
            print(f"   - {issue}")
    
    print(f"3. 测试套件: [OK] 通过" if tests_ok else f"[FAIL] 失败 ({failed} 个测试失败)")
    if passed > 0:
        print(f"   通过测试: {passed} 个")
    
    print(f"\n总用时: {end_time - start_time:.2f} 秒")
    
    if whitespace_ok and tests_ok:
        print("\n[SUCCESS] 所有检查通过！")
        return 0
    else:
        print("\n[FAILURE] 需要修复的问题:")
        if not whitespace_ok:
            print("  - 修复尾部空白问题")
        if not tests_ok:
            print(f"  - 修复 {failed} 个失败的测试")
        return 1

if __name__ == "__main__":
    sys.exit(main())
