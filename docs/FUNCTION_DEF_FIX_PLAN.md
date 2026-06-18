# 函数定义问题分析和修复方案

## 问题分析

### 当前问题

**测试失败**：
```
测试 1: 完整函数定义
------------------------------------------------------------
1. 词法分析...
   Token数量: 17
2. 语法分析...
[FAIL] 测试失败: 语法错误: Unexpected token: FUNCTION (行 1, 列 0)
```

**问题原因**：
解析器在遇到 `函数` 关键字时，没有正确识别为函数定义语句。

### 根本原因

**当前解析流程**：
1. `_parse_statement()` 检查 TokenType
2. 检查 `TokenType.VAR`（定义）
3. 检查 `TokenType.RETURN`（返回）
4. 默认：`_parse_expression_statement()`

**问题**：
- 没有检查 `TokenType.FUNCTION`
- 函数定义被当作表达式语句处理
- 导致语法错误

---

## 修复方案

### 方案1：添加函数定义检查

**修改位置**：`src/parser/parser.py` 的 `_parse_statement()` 方法

**修改内容**：
```python
def _parse_statement(self) -> ASTNode:
    """解析语句"""
    # 变量定义：定义 ...
    if self._check(TokenType.VAR):
        return self._parse_var_def()

    # 函数定义：函数 ...
    if self._check(TokenType.FUNCTION):
        return self._parse_function_statement()

    # 返回语句：返回 ...
    if self._check(TokenType.RETURN):
        return self._parse_return()

    # 表达式语句（包括赋值）
    return self._parse_expression_statement()
```

**新增方法**：
```python
def _parse_function_statement(self) -> FunctionDefNode:
    """解析函数定义语句"""
    token = self._advance()  # 消费 函数

    # 解析函数名
    name_token = self._expect(TokenType.IDENTIFIER, "Expected function name")
    name = name_token.value

    # 解析参数列表
    params = []
    while not self._check(TokenType.COLON, TokenType.NEWLINE, TokenType.EOF):
        if self._check(TokenType.IDENTIFIER):
            param_token = self._advance()
            params.append(param_token.value)
        else:
            break

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

---

### 方案2：修改词法分析器

**问题**：
当前词法分析器可能没有正确识别 `函数` 关键字。

**检查**：
```python
# src/lexer/keywords.py
CORE_KEYWORDS = {
    "定义": TokenType.VAR,
    "函数": TokenType.FUNCTION,
    "如果": TokenType.IF,
    "真值": TokenType.TRUE,
    "假值": TokenType.FALSE,
}
```

**验证**：
- 确认 `函数` 映射到 `TokenType.FUNCTION`
- 确认词法分析器正确识别

---

## 实施步骤

### 步骤1：验证词法分析

**测试代码**：
```python
from src.lexer.lexer import Lexer

code = "函数 平方：\n  参数 n。\n  返回 n 相乘 n。"
lexer = Lexer(code)
tokens = lexer.tokenize()

for token in tokens:
    print(f"{token.type}: {token.value}")
```

**预期输出**：
```
FUNCTION: 函数
IDENTIFIER: 平方
COLON: ：
NEWLINE:
INDENT:
PARAM: 参数
IDENTIFIER: n
PERIOD: 。
NEWLINE:
RETURN: 返回
IDENTIFIER: n
MULTIPLY: 相乘
IDENTIFIER: n
PERIOD: 。
DEDENT:
```

### 步骤2：修改解析器

**修改文件**：`src/parser/parser.py`

**修改内容**：
1. 在 `_parse_statement()` 中添加函数定义检查
2. 实现 `_parse_function_statement()` 方法

### 步骤3：测试验证

**测试代码**：
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

**预期输出**：
```python
def 平方(n):
    return (n * n)
```

---

## 其他问题

### 问题1：参数解析

**当前实现**：
```python
params = []
while not self._check(TokenType.COLON, TokenType.NEWLINE, TokenType.EOF):
    if self._check(TokenType.IDENTIFIER):
        param_token = self._advance()
        params.append(param_token.value)
    else:
        break
```

**问题**：
- 没有处理 `参数` 关键字
- 参数列表可能包含 `参数` 关键字

**修复**：
```python
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
```

### 问题2：函数体解析

**当前实现**：
```python
body = self._parse_block()
```

**问题**：
- 块解析可能不正确
- 需要验证 `_parse_block()` 实现

---

## 测试用例

### 测试1：简单函数定义

**心语代码**：
```yan
函数 平方：
  参数 n。
  返回 n 相乘 n。
```

**预期Python代码**：
```python
def 平方(n):
    return (n * n)
```

### 测试2：多参数函数

**心语代码**：
```yan
函数 相加：
  参数 a。
  参数 b。
  返回 a 相加 b。
```

**预期Python代码**：
```python
def 相加(a, b):
    return (a + b)
```

### 测试3：无参数函数

**心语代码**：
```yan
函数 获取时间：
  返回 当前时间。
```

**预期Python代码**：
```python
def 获取时间():
    return 当前时间
```

---

## 总结

### 问题根源
- 解析器没有检查 `TokenType.FUNCTION`
- 函数定义被当作表达式语句处理

### 修复方案
1. 在 `_parse_statement()` 中添加函数定义检查
2. 实现 `_parse_function_statement()` 方法
3. 正确处理参数关键字
4. 验证块解析实现

### 预期结果
- 函数定义正确解析
- 测试通过率提升
- 自举编译器功能完善
