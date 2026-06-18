# 函数定义解析修复方案

## 问题分析

当前解析器在 `_parse_statement()` 方法中没有检查 `TokenType.FUNCTION`，导致函数定义被当作表达式语句处理。

## 修复方案

在 `src/parser/parser.py` 的 `_parse_statement()` 方法中添加函数定义检查：

```python
def _parse_statement(self) -> ASTNode:
    """解析语句"""
    # 变量定义：定 x = ...
    if self._check(TokenType.VAR):
        return self._parse_var_def()

    # 函数定义：函数 ...
    if self._check(TokenType.FUNCTION):
        return self._parse_function_def_statement()

    # 条件语句：若 ... 则 ...
    if self._check(TokenType.IF):
        return self._parse_if()

    # ... 其他语句
```

## 新增方法

添加 `_parse_function_def_statement()` 方法：

```python
def _parse_function_def_statement(self) -> FunctionDefNode:
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
```

## 测试验证

测试代码：
```python
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.codegen.python_codegen import PythonCodegen

code = """函数 平方：
  参数 n。
  返回 n 相乘 n。
"""

lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

codegen = PythonCodegen()
python_code = codegen.generate(ast)

print(python_code)
```

预期输出：
```python
def 平方(n):
    return (n * n)
```

## 实施步骤

1. 在 `_parse_statement()` 中添加函数定义检查
2. 实现 `_parse_function_def_statement()` 方法
3. 运行测试验证
4. 修复其他相关问题
