#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""使用Playwright测试算法示例是否真正运行"""

import sys
import os
import time
import subprocess
from pathlib import Path

# 启动服务器
print("启动Playground服务器...")
server_process = subprocess.Popen(
    ["python", "start.py", "--port", "5001"],
    cwd=os.path.dirname(os.path.abspath(__file__)),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# 等待服务器启动
time.sleep(3)

try:
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        print("访问Playground...")
        page.goto("http://localhost:5001", timeout=10000)
        time.sleep(2)
        
        # 检查页面是否加载成功
        title = page.title()
        print(f"页面标题: {title}")
        
        # 检查编辑器是否存在
        editor = page.query_selector("#editor")
        if not editor:
            print("错误: 找不到编辑器")
            browser.close()
            server_process.terminate()
            sys.exit(1)
        
        print("编辑器找到，开始测试算法示例...")
        
        # 测试汉诺塔
        print("\n=== 测试汉诺塔 ===")
        page.evaluate("""
            // 清空编辑器
            document.getElementById('editor').value = '';
            // 加载汉诺塔示例
            loadExample('hanoi');
        """)
        time.sleep(1)
        
        # 获取编辑器内容
        hanoi_code = page.evaluate("document.getElementById('editor').value")
        print(f"汉诺塔代码长度: {len(hanoi_code)} 字符")
        print("汉诺塔代码预览:")
        print(hanoi_code[:200] + "..." if len(hanoi_code) > 200 else hanoi_code)
        
        # 运行代码
        page.evaluate("""
            document.getElementById('runButton').click();
        """)
        time.sleep(2)
        
        # 获取输出
        output = page.evaluate("document.getElementById('output').textContent")
        print("汉诺塔输出:")
        print(output[:500] + "..." if len(output) > 500 else output)
        
        # 检查是否有计算输出
        if "个盘子需要" in output and "步移动" in output:
            print("✅ 汉诺塔示例有计算输出")
        else:
            print("❌ 汉诺塔示例可能只是打印固定文本")
        
        # 测试冒泡排序
        print("\n=== 测试冒泡排序 ===")
        page.evaluate("""
            // 清空编辑器
            document.getElementById('editor').value = '';
            // 加载冒泡排序示例
            loadExample('bubble');
        """)
        time.sleep(1)
        
        bubble_code = page.evaluate("document.getElementById('editor').value")
        print(f"冒泡排序代码长度: {len(bubble_code)} 字符")
        print("冒泡排序代码预览:")
        print(bubble_code[:200] + "..." if len(bubble_code) > 200 else bubble_code)
        
        # 运行代码
        page.evaluate("""
            document.getElementById('runButton').click();
        """)
        time.sleep(2)
        
        # 获取输出
        output = page.evaluate("document.getElementById('output').textContent")
        print("冒泡排序输出:")
        print(output[:500] + "..." if len(output) > 500 else output)
        
        # 检查是否有排序过程
        if "第1轮" in output and "第2轮" in output and "排序完成" in output:
            print("✅ 冒泡排序示例有排序过程")
        else:
            print("❌ 冒泡排序示例可能只是打印固定文本")
        
        # 测试图灵机
        print("\n=== 测试图灵机 ===")
        page.evaluate("""
            // 清空编辑器
            document.getElementById('editor').value = '';
            // 加载图灵机示例
            loadExample('turing');
        """)
        time.sleep(1)
        
        turing_code = page.evaluate("document.getElementById('editor').value")
        print(f"图灵机代码长度: {len(turing_code)} 字符")
        print("图灵机代码预览:")
        print(turing_code[:200] + "..." if len(turing_code) > 200 else turing_code)
        
        # 运行代码
        page.evaluate("""
            document.getElementById('runButton').click();
        """)
        time.sleep(2)
        
        # 获取输出
        output = page.evaluate("document.getElementById('output').textContent")
        print("图灵机输出:")
        print(output[:500] + "..." if len(output) > 500 else output)
        
        # 检查是否有计算过程
        if "步骤1" in output and "步骤2" in output and "步骤3" in output:
            print("✅ 图灵机示例有计算过程")
        else:
            print("❌ 图灵机示例可能只是打印固定文本")
        
        # 测试素数筛
        print("\n=== 测试素数筛 ===")
        page.evaluate("""
            // 清空编辑器
            document.getElementById('editor').value = '';
            // 加载素数筛示例
            loadExample('prime');
        """)
        time.sleep(1)
        
        prime_code = page.evaluate("document.getElementById('editor').value")
        print(f"素数筛代码长度: {len(prime_code)} 字符")
        print("素数筛代码预览:")
        print(prime_code[:200] + "..." if len(prime_code) > 200 else prime_code)
        
        # 运行代码
        page.evaluate("""
            document.getElementById('runButton').click();
        """)
        time.sleep(2)
        
        # 获取输出
        output = page.evaluate("document.getElementById('output').textContent")
        print("素数筛输出:")
        print(output[:500] + "..." if len(output) > 500 else output)
        
        # 检查是否有筛选过程
        if "第1步" in output and "第2步" in output and "第3步" in output and "第4步" in output:
            print("✅ 素数筛示例有筛选过程")
        else:
            print("❌ 素数筛示例可能只是打印固定文本")
        
        browser.close()
        
finally:
    # 关闭服务器
    print("\n关闭服务器...")
    server_process.terminate()
    server_process.wait()

print("\n测试完成！")