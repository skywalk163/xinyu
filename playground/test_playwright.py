#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""使用Playwright测试Playground示例加载功能"""

import sys
import os
import time

# 安装playwright
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("正在安装playwright...")
    os.system("pip install playwright")
    os.system("python -m playwright install chromium")
    from playwright.sync_api import sync_playwright

def test_playground():
    """测试Playground示例加载"""

    print("=" * 80)
    print("Playwright 自动化测试 - Playground示例加载")
    print("=" * 80)
    print()

    # 启动服务器（假设已经在运行）
    print("提示：请确保Playground服务器正在运行（python server.py）")
    print()

    with sync_playwright() as p:
        # 启动浏览器
        print("1. 启动浏览器...")
        browser = p.chromium.launch(headless=False)  # headless=False可以看到浏览器
        page = browser.new_page()

        # 启用控制台日志
        console_messages = []
        def handle_console(msg):
            console_messages.append(f"[{msg.type}] {msg.text}")
            print(f"控制台: [{msg.type}] {msg.text}")

        page.on("console", handle_console)

        # 访问页面
        print("\n2. 访问Playground页面...")
        try:
            page.goto("http://localhost:5000", timeout=10000)
            print("[OK] 页面加载成功")
        except Exception as e:
            print(f"[FAIL] 页面加载失败: {e}")
            print("请确保服务器正在运行：python server.py")
            browser.close()
            return

        # 等待页面加载
        time.sleep(2)

        # 检查页面元素
        print("\n3. 检查页面元素...")

        # 检查编辑器
        editor = page.query_selector("#editor")
        if editor:
            print("[OK] 找到编辑器元素")
        else:
            print("[FAIL] 未找到编辑器元素")

        # 检查字符计数
        char_count = page.query_selector("#charCount")
        if char_count:
            initial_count = char_count.inner_text()
            print(f"[OK] 初始字符数: {initial_count}")
        else:
            print("[FAIL] 未找到字符计数元素")

        # 检查示例按钮
        print("\n4. 检查示例按钮...")
        example_buttons = page.query_selector_all(".example-item")
        print(f"找到 {len(example_buttons)} 个示例按钮")

        # 测试点击第一个示例（Hello World）
        print("\n5. 测试点击'你好，世界'示例...")

        # 清空控制台消息
        console_messages.clear()

        # 点击第一个示例按钮
        first_example = page.query_selector(".example-item")
        if first_example:
            first_example.click()
            print("[OK] 已点击示例按钮")

            # 等待一下让JavaScript执行
            time.sleep(1)

            # 检查编辑器内容
            if editor:
                editor_value = editor.input_value()
                print(f"\n编辑器内容长度: {len(editor_value)}")
                print(f"编辑器前100字符: {editor_value[:100]}")

                if len(editor_value) > 0:
                    print("[OK] 示例已成功加载到编辑器")
                else:
                    print("[FAIL] 编辑器为空，示例未加载")

            # 检查字符计数
            if char_count:
                current_count = char_count.inner_text()
                print(f"当前字符数: {current_count}")

            # 检查控制台消息
            print(f"\n控制台消息数量: {len(console_messages)}")
            for msg in console_messages:
                print(f"  {msg}")
        else:
            print("[FAIL] 未找到示例按钮")

        # 测试其他示例
        print("\n6. 测试其他示例...")

        test_examples = [
            ("变量定义", 1),
            ("函数定义", 2),
            ("数学运算", 8),
        ]

        for name, index in test_examples:
            print(f"\n测试 '{name}' 示例:")
            console_messages.clear()

            # 点击对应的示例按钮
            example_button = page.query_selector_all(".example-item")[index]
            if example_button:
                example_button.click()
                time.sleep(0.5)

                if editor:
                    editor_value = editor.input_value()
                    if len(editor_value) > 0:
                        print(f"  [OK] 加载成功，长度: {len(editor_value)}")
                    else:
                        print(f"  [FAIL] 加载失败，编辑器为空")

        # 测试运行代码
        print("\n7. 测试运行代码...")

        # 加载Hello示例
        first_example = page.query_selector(".example-item")
        if first_example:
            first_example.click()
            time.sleep(0.5)

            # 点击运行按钮
            run_button = page.query_selector("#runBtn")
            if run_button:
                run_button.click()
                print("[OK] 已点击运行按钮")

                # 等待执行完成
                time.sleep(2)

                # 检查输出
                output = page.query_selector("#output")
                if output:
                    output_text = output.inner_text()
                    print(f"\n输出内容:")
                    print(output_text[:200])
            else:
                print("[FAIL] 未找到运行按钮")

        # 截图保存
        print("\n8. 保存截图...")
        page.screenshot(path="playground_test.png")
        print("[OK] 截图已保存: playground_test.png")

        # 保持浏览器打开一段时间以便观察
        print("\n测试完成，浏览器将在5秒后关闭...")
        time.sleep(5)

        # 关闭浏览器
        browser.close()

        print("\n" + "=" * 80)
        print("测试完成")
        print("=" * 80)

if __name__ == "__main__":
    test_playground()
