# -*- coding: utf-8 -*-
"""修复函数定义问题

在解析器中添加函数定义检查。
"""

import sys
from pathlib import Path

def fix_parser():
    """修复解析器"""
    
    parser_file = Path("src/parser/parser.py")
    
    if not parser_file.exists():
        print("错误：找不到解析器文件")
        return False
    
    # 读取文件
    with open(parser_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找需要修改的位置
    # 在 "if self._check(TokenType.VAR):" 后面添加函数定义检查
    
    # 检查是否已经添加过
    if "if self._check(TokenType.FUNCTION):" in content:
        print("函数定义检查已经存在，无需修改")
        return True
    
    # 找到插入位置
    lines = content.split('\n')
    insert_index = -1
    
    for i, line in enumerate(lines):
        if "if self._check(TokenType.VAR):" in line:
            # 找到下一个空行
            for j in range(i+1, min(i+10, len(lines))):
                if lines[j].strip() == "":
                    insert_index = j
                    break
            break
    
    if insert_index == -1:
        print("错误：找不到插入位置")
        return False
    
    # 插入函数定义检查
    new_lines = [
        "",
        "        # 函数定义：函数 ...",
        "        if self._check(TokenType.FUNCTION):",
        "            return self._parse_function_def_statement()",
    ]
    
    lines = lines[:insert_index] + new_lines + lines[insert_index:]
    
    # 写回文件
    with open(parser_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print("✓ 已添加函数定义检查")
    return True


def add_parse_method():
    """添加函数定义解析方法"""
    
    parser_file = Path("src/parser/parser.py")
    
    # 读取文件
    with open(parser_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经添加过
    if "_parse_function_def_statement" in content:
        print("函数定义解析方法已经存在，无需添加")
        return True
    
    # 找到插入位置（在 _parse_var_def 方法后面）
    lines = content.split('\n')
    insert_index = -1
    
    for i, line in enumerate(lines):
        if "def _parse_var_def" in line:
            # 找到方法结束位置
            for j in range(i+1, len(lines)):
                if lines[j].startswith("    def ") and not lines[j].startswith("    def _"):
                    insert_index = j
                    break
            break
    
    if insert_index == -1:
        print("错误：找不到插入位置")
        return False
    
    # 插入新方法
    new_method = '''    def _parse_function_def_statement(self) -> 'FunctionDefNode':
        """解析函数定义语句
        
        语法：函数 名字：
                参数 参数名。
                语句。
              结束。
        """
        token = self._advance()  # 消费 函数
        
        # 解析函数名
        name_token = self._expect(TokenType.IDENTIFIER, "Expected function name")
        name = name_token.value
        
        # 解析参数列表
        params = []
        # 跳过参数关键字
        while self._check(TokenType.PARAM):
            self._advance()  # 消费 参数
            if self._check(TokenType.IDENTIFIER):
                param_token = self._advance()
                params.append(param_token.value)
                # 消费句号
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
    
    lines = lines[:insert_index] + [new_method] + lines[insert_index:]
    
    # 写回文件
    with open(parser_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print("✓ 已添加函数定义解析方法")
    return True


def test_fix():
    """测试修复结果"""
    
    print("\n测试函数定义解析...")
    
    try:
        from src.lexer.lexer import Lexer
        from src.parser.parser import Parser
        from src.codegen.python_codegen import PythonCodegen
        
        code = """函数 平方：
  参数 n。
  返回 n 相乘 n。
"""
        
        # 词法分析
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print(f"Token数量: {len(tokens)}")
        
        # 语法分析
        parser = Parser(tokens)
        ast = parser.parse()
        print(f"AST节点数: {len(ast.statements)}")
        
        # 代码生成
        codegen = PythonCodegen()
        python_code = codegen.generate(ast)
        print(f"生成的Python代码:\n{python_code}")
        
        print("\n✓ 测试通过")
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    print("=" * 60)
    print("修复函数定义问题")
    print("=" * 60)
    
    # 步骤1：添加函数定义检查
    print("\n步骤1：添加函数定义检查...")
    if not fix_parser():
        sys.exit(1)
    
    # 步骤2：添加解析方法
    print("\n步骤2：添加函数定义解析方法...")
    if not add_parse_method():
        sys.exit(1)
    
    # 步骤3：测试修复结果
    print("\n步骤3：测试修复结果...")
    if not test_fix():
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("修复完成！")
    print("=" * 60)
