# -*- coding: utf-8 -*-
"""添加函数定义解析方法"""

# 读取文件
with open("src/parser/parser.py", "r", encoding="utf-8") as f:
    content = f.read()

# 检查是否已经有这个方法
if "_parse_function_def_statement" in content:
    print("方法已存在")
else:
    # 找到 _parse_var_def 方法的结束位置
    lines = content.split("\n")
    insert_index = -1

    for i, line in enumerate(lines):
        if "def _parse_var_def" in line:
            # 找到下一个方法定义
            for j in range(i + 1, len(lines)):
                if lines[j].startswith("    def ") and lines[j].strip().endswith(":"):
                    insert_index = j
                    break
            break

    if insert_index > 0:
        # 插入新方法
        new_method = '''    def _parse_function_def_statement(self):
        """解析函数定义语句"""
        token = self._advance()  # 消费 函数

        # 解析函数名
        name_token = self._expect(TokenType.IDENTIFIER, "Expected function name")
        name = name_token.value

        # 解析参数列表
        params = []
        while self._check(TokenType.PARAM):
            self._advance()  # 消费 参数
            if self._check(TokenType.IDENTIFIER):
                param_token = self._advance()
                params.append(param_token.value)
                if self._check(TokenType.PERIOD):
                    self._advance()

        # 期望 ：
        self._expect(TokenType.COLON, "Expected '：' after function parameters")

        # 解析函数体
        body = self._parse_block()

        # 消费结尾的 。
        if self._check(TokenType.PERIOD):
            self._advance()

        return FunctionDefNode(
            line=token.line,
            column=token.column,
            name=name,
            params=params,
            body=body
        )

'''
        lines.insert(insert_index, new_method)

        # 写回文件
        with open("src/parser/parser.py", "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print("已添加函数定义解析方法")
    else:
        print("找不到插入位置")
