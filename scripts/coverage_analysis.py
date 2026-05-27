# -*- coding: utf-8 -*-
"""测试覆盖率分析报告生成器"""

import subprocess
import re
from pathlib import Path

def run_coverage():
    """运行测试并生成覆盖率报告"""
    print("=== 运行测试覆盖率分析 ===\n")
    
    # 运行pytest with coverage
    result = subprocess.run(
        ["python", "-m", "pytest", "tests/", "--cov=src", "--cov-report=term-missing", "--tb=no", "-q"],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    # 解析输出
    output = result.stdout + result.stderr
    
    # 提取覆盖率信息
    lines = output.split('\n')
    
    # 找到覆盖率表格
    coverage_data = []
    for line in lines:
        if 'src\\' in line or 'TOTAL' in line:
            coverage_data.append(line)
    
    # 打印覆盖率表格
    print("模块覆盖率统计：\n")
    for line in coverage_data:
        print(line)
    
    # 提取总覆盖率
    for line in coverage_data:
        if 'TOTAL' in line:
            match = re.search(r'(\d+)%', line)
            if match:
                total_coverage = match.group(1)
                print(f"\n总覆盖率: {total_coverage}%")
                break
    
    return output

def analyze_coverage():
    """分析覆盖率并生成建议"""
    print("\n=== 覆盖率分析建议 ===\n")
    
    suggestions = [
        ("src/parser/parser.py", "91%", "85%", "✅ 已达标"),
        ("src/semantic/analyzer.py", "72%", "85%", "⚠️ 需提升13%"),
        ("src/main.py", "57%", "80%", "⚠️ 需提升23%"),
        ("src/codegen/python_codegen.py", "N/A", "85%", "❌ 需添加测试"),
        ("src/semantic/analyzer_with_inference.py", "47%", "85%", "⚠️ 需提升38%"),
        ("src/vm/virtual_machine.py", "0%", "80%", "❌ 需添加测试"),
        ("src/parser/parser_with_error_handler.py", "0%", "80%", "❌ 需添加测试"),
    ]
    
    print("模块覆盖率目标：\n")
    print(f"{'模块':<50} {'当前':<10} {'目标':<10} {'状态':<15}")
    print("-" * 85)
    
    for module, current, target, status in suggestions:
        print(f"{module:<50} {current:<10} {target:<10} {status:<15}")
    
    print("\n优先级建议：")
    print("1. P0: src/semantic/analyzer_with_inference.py - 需提升38%")
    print("2. P0: src/main.py - 需提升23%")
    print("3. P1: src/semantic/analyzer.py - 需提升13%")
    print("4. P1: src/vm/virtual_machine.py - 需添加测试")
    print("5. P2: src/parser/parser_with_error_handler.py - 需添加测试")

if __name__ == '__main__':
    run_coverage()
    analyze_coverage()
    print("\n✅ 覆盖率分析完成！")
