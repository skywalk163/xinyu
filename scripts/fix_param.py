# -*- coding: utf-8 -*-
"""完整修复函数定义问题"""

# 读取文件
with open('src/parser/parser.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 修改1：添加参数声明处理
if "if self._check(TokenType.PARAM):" not in content:
    # 找到返回语句处理的位置
    lines = content.split('\n')
    insert_index = -1
    
    for i, line in enumerate(lines):
        if "return self._parse_return()" in line:
            insert_index = i + 1
            break
    
    if insert_index > 0:
        # 插入参数声明处理
        new_lines = [
            "",
            "        # 参数声明：参数 ...",
            "        if self._check(TokenType.PARAM):",
            "            return self._parse_param_decl()",
        ]
        
        lines = lines[:insert_index] + new_lines + lines[insert_index:]
        content = '\n'.join(lines)
        print("[OK] 已添加参数声明检查")

# 修改2：添加参数声明解析方法
if "_parse_param_decl" not in content:
    # 找到 _parse_return 方法的结束位置
    lines = content.split('\n')
    insert_index = -1
    
    for i, line in enumerate(lines):
        if "def _parse_return" in line:
            # 找到下一个方法定义
            for j in range(i+1, len(lines)):
                if lines[j].startswith("    def ") and lines[j].strip().endswith(':'):
                    insert_index = j
                    break
            break
    
    if insert_index > 0:
        # 插入新方法
        new_method = '''    def _parse_param_decl(self):
        """解析参数声明（参数 x。）"""
        token = self._advance()  # 消费 参数
        
        # 参数声明在函数定义中已经被处理，这里跳过
        # 消费参数名
        if self._check(TokenType.IDENTIFIER):
            self._advance()
        
        # 消费句号
        if self._check(TokenType.PERIOD):
            self._advance()
        
        return None  # 返回None，因为参数已经在函数定义中处理

'''
        lines = lines[:insert_index] + [new_method] + lines[insert_index:]
        content = '\n'.join(lines)
        print("[OK] 已添加参数声明解析方法")

# 写回文件
with open('src/parser/parser.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n修复完成！")
