#!/usr/bin/env python3
"""
调试参数收集
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.parser.parser import Parser
from src.lexer.lexer import Lexer
from src.parser.verb_registry import VerbRegistry

# 测试代码
test_code = """定义 加法 = 函 x, y：
  返回 x 相加 y。
。

定义 结果 = 加法 (2) 3。
打印 结果。"""

print("测试代码:")
print(test_code)
print("\n" + "="*50 + "\n")

# 词法分析
lexer = Lexer(test_code)
tokens = lexer.tokenize()

print("词法分析结果:")
for i, token in enumerate(tokens):
    print(f"{i:3d}: {token.type.name:15} '{token.value}' (行{token.line}, 列{token.column})")

print("\n" + "="*50 + "\n")

# 创建解析器
parser = Parser(tokens)

# 手动模拟解析过程
print("模拟解析过程:")
print("1. 解析 '定义 加法 = 函 x, y：'")
# 跳过函数定义部分
for i in range(20):
    if i < len(tokens) and tokens[i].type.name == 'PERIOD' and tokens[i].value == '。':
        parser.pos = i + 1
        break

print(f"当前位置: {parser.pos}, 当前token: {tokens[parser.pos].type.name} '{tokens[parser.pos].value}'")

# 解析 '定义 结果 = 加法 (2) 3。'
print("\n2. 解析 '定义 结果 = 加法 (2) 3。'")
# 跳过 '定义 结果 ='
parser.pos += 3  # 跳过 VAR, IDENTIFIER, ASSIGN

print(f"当前位置: {parser.pos}, 当前token: {tokens[parser.pos].type.name} '{tokens[parser.pos].value}'")

# 现在应该解析 '加法 (2) 3'
# 调用 _parse_identifier_or_call_in_term
print("\n3. 调用 _parse_identifier_or_call_in_term 解析 '加法'")
# 保存当前位置
saved_pos = parser.pos

# 模拟 _parse_identifier_or_call_in_term
token = tokens[parser.pos]
print(f"  当前token: {token.type.name} '{token.value}'")
parser.pos += 1  # 消费 '加法'

print(f"  消费后位置: {parser.pos}, 当前token: {tokens[parser.pos].type.name} '{tokens[parser.pos].value}'")

# 检查下一个token
next_token = tokens[parser.pos]
print(f"  下一个token: {next_token.type.name} '{next_token.value}'")

# 检查是否是括号函数调用
if next_token.type.name == 'LPAREN':
    print("  检测到左括号，解析括号表达式")
    parser.pos += 1  # 消费 '('
    print(f"  消费 '(' 后位置: {parser.pos}, 当前token: {tokens[parser.pos].type.name} '{tokens[parser.pos].value}'")
    
    # 解析表达式
    print("  调用 _parse_term() 解析括号内的表达式")
    # 这里应该解析 '2'
    
    # 期望 ')'
    if tokens[parser.pos + 1].type.name == 'RPAREN':
        print(f"  找到 ')' 在位置 {parser.pos + 1}")
        parser.pos += 2  # 跳过 '2' 和 ')'
        print(f"  消费 '2' 和 ')' 后位置: {parser.pos}, 当前token: {tokens[parser.pos].type.name} '{tokens[parser.pos].value}'")
        
        # 现在应该收集参数 '3'
        print(f"  现在应该收集参数 '3'")
        print(f"  当前token: {tokens[parser.pos].type.name} '{tokens[parser.pos].value}'")
        
        # 检查 _should_stop_collecting_args
        print(f"  _should_stop_collecting_args 返回: {parser._should_stop_collecting_args()}")