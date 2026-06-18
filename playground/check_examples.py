#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 查找const examples的位置
start = content.find("const examples = {")
if start != -1:
    print(f"Examples object starts at position: {start}")

    # 找到对应的结束}
    brace_count = 0
    pos = start + len("const examples = {")
    found = False

    for i in range(pos, len(content)):
        if content[i] == "{":
            brace_count += 1
        elif content[i] == "}":
            if brace_count == 0:
                # 找到了结束位置
                end = i
                found = True
                break
            brace_count -= 1

    if found:
        examples_content = content[start : end + 1]
        print(f"Examples object length: {len(examples_content)}")

        # 提取示例名称
        examples = re.findall(r"(\w+):\s*`", examples_content)
        print(f"\nFound {len(examples)} examples:")
        for ex in examples:
            print(f"  - {ex}")
    else:
        print("Could not find closing brace")
else:
    print("Examples object not found!")

# 检查loadExample函数
if "function loadExample" in content:
    print("\nloadExample function found")
else:
    print("\nloadExample function NOT found!")

# 检查onclick绑定
onclick_matches = re.findall(r"onclick=\"loadExample\('(\w+)'\)\"", content)
print(f"\nFound {len(onclick_matches)} onclick bindings:")
for match in onclick_matches:
    print(f"  - {match}")
