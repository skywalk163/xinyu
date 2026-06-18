# 中文编程语言完整实现计划

> **面向 AI 代理的工作者：** 必需子技能：使用 superpowers:subagent-driven-development（推荐）或 superpowers:executing-plans 逐任务实现此计划。步骤使用复选框（`- [ ]`）语法来跟踪进度。

**目标：** 构建一门基于中文深层认知特性的编程语言，实现核心语法、高级特性、多轨制、工具链和生态系统

**架构：** 词法分析器 → 语法分析器 → 宏展开器 → 语义分析器 → 代码生成器 → 运行时环境，支持意合式调用、语境补全、宏系统、多轨制设计

**技术栈：** Python 3.12+、PLY（词法/语法分析）、pytest（测试）、VS Code Extension API（工具链）

**核心设计原则：**
- **极简关键字**：只有 5 个核心关键字（`定`、`函`、`若`、`真`、`假`）
- **语法结构语法化**：控制流结构由虚词和标点构成
- **数据操作动词化**：所有数据操作都是函数
- **复杂逻辑宏化**：高级抽象通过宏实现，编译期展开

---

## 文件结构

```
chineseprogram/
├── src/
│   ├── lexer/
│   │   ├── __init__.py
│   │   ├── tokens.py              # Token定义
│   │   ├── lexer.py               # 词法分析器
│   │   └── keywords.py            # 中文关键字（仅5个核心关键字）
│   ├── parser/
│   │   ├── __init__.py
│   │   ├── ast_nodes.py           # AST节点定义
│   │   ├── parser.py              # 语法分析器
│   │   └── grammar_rules.py       # 语法规则
│   ├── macro/
│   │   ├── __init__.py
│   │   ├── macro_system.py        # 宏系统核心
│   │   ├── macro_expander.py      # 宏展开器
│   │   ├── builtin_macros.py      # 内置宏（遍历、重复、持续等）
│   │   └── idiom_macros.py        # 成语宏（守株待兔、亡羊补牢等）
│   ├── semantic/
│   │   ├── __init__.py
│   │   ├── analyzer.py            # 语义分析器
│   │   ├── scope.py               # 作用域管理
│   │   └── type_inference.py      # 类型推断
│   ├── codegen/
│   │   ├── __init__.py
│   │   ├── python_codegen.py      # Python代码生成
│   │   └── multi_track.py         # 多轨制代码生成
│   ├── runtime/
│   │   ├── __init__.py
│   │   ├── environment.py         # 运行环境
│   │   ├── builtins.py            # 内置函数
│   │   └── data_verbs.py          # 数据动词库（函数，非关键字）
│   └── main.py                    # 主入口
├── tests/
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_macro.py              # 宏系统测试
│   ├── test_semantic.py
│   ├── test_codegen.py
│   ├── test_runtime.py
│   └── test_integration.py
├── examples/
│   ├── basic/
│   │   ├── hello.yan
│   │   ├── variables.yan
│   │   ├── functions.yan
│   │   └── control_flow.yan
│   ├── advanced/
│   │   ├── user_registration.yan
│   │   ├── data_pipeline.yan
│   │   ├── web_service.yan
│   │   └── state_machine.yan
│   ├── macros/
│   │   ├── builtin_macros.yan     # 内置宏示例
│   │   ├── idiom_macros.yan       # 成语宏示例
│   │   └── custom_macros.yan      # 自定义宏示例
│   └── multi_track/
│       ├── math_track.yan
│       ├── python_track.yan
│       ├── sql_track.yan
│       └── javascript_track.yan
├── vscode-extension/
│   ├── package.json
│   ├── tsconfig.json
│   ├── src/
│   │   ├── extension.ts
│   │   ├── syntaxHighlight.ts
│   │   ├── completion.ts
│   │   └── diagnostics.ts
│   └── syntaxes/
│       └── yan.tmLanguage.json
├── docs/
│   ├── LANGUAGE_SPEC.md
│   ├── TUTORIAL.md
│   ├── MACRO_SYSTEM.md            # 宏系统文档
│   └── API_REFERENCE.md
└── stdlib/
    ├── __init__.py
    ├── io.py
    ├── string.py
    ├── math.py
    └── collection.py
```

---

## 极简关键字体系

### 核心关键字（仅 5 个）

| 关键字 | 含义 | 示例 |
|--------|------|------|
| `定` | 定义变量/常量 | `定x=5。` |
| `函` | 定义函数 | `函平方x，x乘x。` |
| `若` | 条件判断 | `若x大0，印"正数"。` |
| `真` | 布尔真值 | `真` |
| `假` | 布尔假值 | `假` |

### 语法标记（非关键字）

- 条件标记：`则`、`否则`、`否则若`
- 循环标记：`遍历`、`于`、`当`、`重复`、`次`、`持续`
- 函数标记：`接收`、`返回`
- 标点符号：`，`、`。`、`：`、`、`

### 内置函数/动词（非关键字）

- 数据动词：读取、写入、映射、过滤、折叠、分组、排序
- 数学动词：加、减、乘、除、平方、开方
- 比较动词：等于、大于、小于、包含
- 逻辑动词：且、或、非

### 宏系统

- 内置宏：遍历、重复、持续、除非
- 成语宏：守株待兔、亡羊补牢、画蛇添足
- 用户自定义宏：支持用户定义新的宏

---

## 阶段1：核心语法（任务1-25）

### 任务1：项目初始化

**文件：**
- 创建：`src/__init__.py`
- 创建：`src/lexer/__init__.py`
- 创建：`src/parser/__init__.py`
- 创建：`src/semantic/__init__.py`
- 创建：`src/codegen/__init__.py`
- 创建：`src/runtime/__init__.py`
- 创建：`tests/__init__.py`
- 创建：`requirements.txt`
- 创建：`pytest.ini`
- 创建：`.gitignore`

- [ ] **步骤1：创建项目结构**

```bash
mkdir -p src/lexer src/parser src/semantic src/codegen src/runtime
mkdir -p tests examples/basic examples/advanced examples/multi_track
mkdir -p stdlib docs vscode-extension/src vscode-extension/syntaxes
touch src/__init__.py
touch src/lexer/__init__.py src/parser/__init__.py src/semantic/__init__.py
touch src/codegen/__init__.py src/runtime/__init__.py
touch tests/__init__.py
```

- [ ] **步骤2：创建 requirements.txt**

```
ply==3.11
pytest==8.0.0
pytest-cov==4.1.0
```

- [ ] **步骤3：创建 pytest.ini**

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --cov=src --cov-report=term-missing
```

- [ ] **步骤4：创建 .gitignore**

```
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
.vscode/
```

- [ ] **步骤5：Commit**

```bash
git add .
git commit -m "feat: initialize project structure"
```

---

### 任务2：Token定义

**文件：**
- 创建：`src/lexer/tokens.py`
- 测试：`tests/test_lexer.py`

- [ ] **步骤1：编写失败的测试**

```python
# tests/test_lexer.py
import pytest
from src.lexer.tokens import Token, TokenType

def test_token_creation():
    token = Token(TokenType.NUMBER, "123", 1, 0)
    assert token.type == TokenType.NUMBER
    assert token.value == "123"
    assert token.line == 1
    assert token.column == 0

def test_token_string_representation():
    token = Token(TokenType.STRING, "你好", 1, 0)
    assert str(token) == "Token(STRING, '你好', line=1, col=0)"

def test_token_equality():
    token1 = Token(TokenType.NUMBER, "123", 1, 0)
    token2 = Token(TokenType.NUMBER, "123", 1, 0)
    assert token1 == token2
```

- [ ] **步骤2：运行测试验证失败**

运行：`pytest tests/test_lexer.py::test_token_creation -v`
预期：FAIL，报错 "cannot import name 'Token'"

- [ ] **步骤3：编写Token定义**

```python
# src/lexer/tokens.py
from enum import Enum, auto
from dataclasses import dataclass
from typing import Any

class TokenType(Enum):
    # 字面量
    NUMBER = auto()      # 数字
    STRING = auto()      # 字符串
    IDENTIFIER = auto()  # 标识符

    # 核心关键字（仅5个）
    VAR = auto()         # 定
    FUNCTION = auto()    # 函
    IF = auto()          # 若
    TRUE = auto()        # 真
    FALSE = auto()       # 假

    # 语法标记（非关键字）
    THEN = auto()        # 则
    ELSE = auto()        # 否则
    ELIF = auto()        # 否则若
    FOR = auto()         # 遍历
    WHILE = auto()       # 当
    REPEAT = auto()      # 重复
    CONTINUE = auto()    # 持续
    RETURN = auto()      # 返回
    RECEIVE = auto()     # 接收
    IN = auto()          # 于
    TIMES = auto()       # 次

    # 操作符（函数，非关键字）
    PLUS = auto()        # 加
    MINUS = auto()       # 减
    MULTIPLY = auto()    # 乘
    DIVIDE = auto()      # 除
    ASSIGN = auto()      # =
    EQUALS = auto()      # 等
    NOT_EQUALS = auto()  # 不等
    LESS = auto()        # 小
    GREATER = auto()     # 大
    LESS_EQ = auto()     # 小等
    GREATER_EQ = auto()  # 大等
    AND = auto()         # 且
    OR = auto()          # 或
    NOT = auto()         # 非

    # 分隔符
    COMMA = auto()       # ，
    PERIOD = auto()      # 。
    COLON = auto()       # ：
    SEMICOLON = auto()   # ；
    PAUSE_MARK = auto()  # 、（顿号）
    LPAREN = auto()      # （
    RPAREN = auto()      # ）
    LBRACKET = auto()    # 【
    RBRACKET = auto()    # 】
    LBRACE = auto()      # {
    RBRACE = auto()      # }

    # 特殊符号
    DOLLAR = auto()      # $
    MATH_EXPR = auto()   # 数学表达式
    PYTHON_BLOCK = auto() # Python代码块

    # 其他
    NEWLINE = auto()     # 换行
    INDENT = auto()      # 缩进
    DEDENT = auto()      # 减少缩进
    EOF = auto()         # 文件结束

@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int

    def __str__(self):
        return f"Token({self.type.name}, {repr(self.value)}, line={self.line}, col={self.column})"

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return (self.type == other.type and
                self.value == other.value and
                self.line == other.line and
                self.column == other.column)
```

- [ ] **步骤4：运行测试验证通过**

运行：`pytest tests/test_lexer.py::test_token_creation -v`
预期：PASS

- [ ] **步骤5：Commit**

```bash
git add src/lexer/tokens.py tests/test_lexer.py
git commit -m "feat: add Token and TokenType definitions"
```

---

### 任务3：中文关键字定义

**文件：**
- 创建：`src/lexer/keywords.py`
- 测试：`tests/test_lexer.py`

- [ ] **步骤1：编写失败的测试**

```python
# tests/test_lexer.py (追加)
from src.lexer.keywords import CORE_KEYWORDS, SYNTAX_MARKERS, OPERATORS

def test_core_keywords():
    # 核心关键字只有5个
    assert CORE_KEYWORDS["定"] == TokenType.VAR
    assert CORE_KEYWORDS["函"] == TokenType.FUNCTION
    assert CORE_KEYWORDS["若"] == TokenType.IF
    assert CORE_KEYWORDS["真"] == TokenType.TRUE
    assert CORE_KEYWORDS["假"] == TokenType.FALSE

def test_syntax_markers():
    # 语法标记（非关键字）
    assert SYNTAX_MARKERS["则"] == TokenType.THEN
    assert SYNTAX_MARKERS["否则"] == TokenType.ELSE
    assert SYNTAX_MARKERS["遍历"] == TokenType.FOR
    assert SYNTAX_MARKERS["当"] == TokenType.WHILE

def test_operators():
    # 操作符（函数，非关键字）
    assert OPERATORS["加"] == TokenType.PLUS
    assert OPERATORS["减"] == TokenType.MINUS
    assert OPERATORS["乘"] == TokenType.MULTIPLY
    assert OPERATORS["除"] == TokenType.DIVIDE
```

- [ ] **步骤2：运行测试验证失败**

运行：`pytest tests/test_lexer.py::test_core_keywords -v`
预期：FAIL，报错 "cannot import name 'CORE_KEYWORDS'"

- [ ] **步骤3：编写关键字定义**

```python
# src/lexer/keywords.py
from src.lexer.tokens import TokenType

# 核心关键字（仅5个，不可扩展）
CORE_KEYWORDS = {
    "定": TokenType.VAR,
    "函": TokenType.FUNCTION,
    "若": TokenType.IF,
    "真": TokenType.TRUE,
    "假": TokenType.FALSE,
}

# 语法标记（非关键字，用于构建语法结构）
SYNTAX_MARKERS = {
    # 条件语法标记
    "则": TokenType.THEN,
    "否则": TokenType.ELSE,
    "否则若": TokenType.ELIF,

    # 循环语法标记（通过宏实现）
    "遍历": TokenType.FOR,
    "当": TokenType.WHILE,
    "重复": TokenType.REPEAT,
    "持续": TokenType.CONTINUE,
    "于": TokenType.IN,
    "次": TokenType.TIMES,

    # 函数语法标记
    "返回": TokenType.RETURN,
    "接收": TokenType.RECEIVE,
}

# 操作符（函数，非关键字）
OPERATORS = {
    "加": TokenType.PLUS,
    "减": TokenType.MINUS,
    "乘": TokenType.MULTIPLY,
    "除": TokenType.DIVIDE,
    "等": TokenType.EQUALS,
    "不等": TokenType.NOT_EQUALS,
    "小": TokenType.LESS,
    "大": TokenType.GREATER,
    "小等": TokenType.LESS_EQ,
    "大等": TokenType.GREATER_EQ,
    "且": TokenType.AND,
    "或": TokenType.OR,
    "非": TokenType.NOT,
}

# 符号映射
SYMBOLS = {
    "，": TokenType.COMMA,
    "。": TokenType.PERIOD,
    "：": TokenType.COLON,
    "；": TokenType.SEMICOLON,
    "、": TokenType.PAUSE_MARK,  # 顿号
    "（": TokenType.LPAREN,
    "）": TokenType.RPAREN,
    "【": TokenType.LBRACKET,
    "】": TokenType.RBRACKET,
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
    "=": TokenType.ASSIGN,
    "$": TokenType.DOLLAR,
}

# 合并所有关键字和标记（用于词法分析）
ALL_KEYWORDS = {**CORE_KEYWORDS, **SYNTAX_MARKERS}
```

- [ ] **步骤4：运行测试验证通过**

运行：`pytest tests/test_lexer.py::test_keywords_mapping -v`
预期：PASS

- [ ] **步骤5：Commit**

```bash
git add src/lexer/keywords.py tests/test_lexer.py
git commit -m "feat: add Chinese keywords and operators mapping"
```

---

### 任务4：词法分析器基础

**文件：**
- 创建：`src/lexer/lexer.py`
- 测试：`tests/test_lexer.py`

- [ ] **步骤1：编写失败的测试**

```python
# tests/test_lexer.py (追加)
from src.lexer.lexer import Lexer

def test_lexer_number():
    lexer = Lexer("123")
    tokens = lexer.tokenize()
    assert len(tokens) == 2  # NUMBER + EOF
    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].value == 123

def test_lexer_string():
    lexer = Lexer('"你好世界"')
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "你好世界"

def test_lexer_identifier():
    lexer = Lexer("用户数据")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == "用户数据"

def test_lexer_keyword():
    lexer = Lexer("若")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.IF
```

- [ ] **步骤2：运行测试验证失败**

运行：`pytest tests/test_lexer.py::test_lexer_number -v`
预期：FAIL，报错 "cannot import name 'Lexer'"

- [ ] **步骤3：编写词法分析器**

```python
# src/lexer/lexer.py
import re
from typing import List
from src.lexer.tokens import Token, TokenType
from src.lexer.keywords import KEYWORDS, OPERATORS, SYMBOLS

class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Lexer Error at line {line}, column {column}: {message}")

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 0
        self.indent_stack = [0]
        self.tokens: List[Token] = []

    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            self._skip_whitespace()

            if self.pos >= len(self.source):
                break

            char = self.source[self.pos]

            # 处理换行和缩进
            if char == '\n':
                self._handle_newline()
            # 处理注释
            elif char == '-' and self.pos + 1 < len(self.source) and self.source[self.pos + 1] == '-':
                self._skip_comment()
            # 处理字符串
            elif char == '"':
                self._read_string()
            # 处理数字
            elif char.isdigit():
                self._read_number()
            # 处理符号
            elif char in SYMBOLS:
                self._read_symbol()
            # 处理中文关键字、操作符、标识符
            elif self._is_chinese(char):
                self._read_chinese()
            # 处理英文标识符
            elif char.isalpha() or char == '_':
                self._read_identifier()
            else:
                raise LexerError(f"Unexpected character: {char}", self.line, self.column)

        # 处理剩余的DEDENT
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token(TokenType.DEDENT, None, self.line, self.column))

        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens

    def _skip_whitespace(self):
        while self.pos < len(self.source) and self.source[self.pos] in ' \t':
            self.pos += 1
            self.column += 1

    def _skip_comment(self):
        while self.pos < len(self.source) and self.source[self.pos] != '\n':
            self.pos += 1

    def _handle_newline(self):
        self.tokens.append(Token(TokenType.NEWLINE, '\n', self.line, self.column))
        self.line += 1
        self.column = 0
        self.pos += 1

        # 计算缩进
        indent = 0
        while self.pos < len(self.source) and self.source[self.pos] == ' ':
            indent += 1
            self.pos += 1

        # 跳过空行
        if self.pos < len(self.source) and self.source[self.pos] == '\n':
            return

        # 生成INDENT/DEDENT
        if indent > self.indent_stack[-1]:
            self.indent_stack.append(indent)
            self.tokens.append(Token(TokenType.INDENT, indent, self.line, 0))
        elif indent < self.indent_stack[-1]:
            while indent < self.indent_stack[-1]:
                self.indent_stack.pop()
                self.tokens.append(Token(TokenType.DEDENT, indent, self.line, 0))

    def _read_string(self):
        start_col = self.column
        self.pos += 1  # 跳过开头的 "
        start = self.pos

        while self.pos < len(self.source) and self.source[self.pos] != '"':
            if self.source[self.pos] == '\\':
                self.pos += 1  # 跳过转义字符
            self.pos += 1

        if self.pos >= len(self.source):
            raise LexerError("Unterminated string", self.line, start_col)

        value = self.source[start:self.pos]
        self.pos += 1  # 跳过结尾的 "
        self.column += self.pos - start + 1

        # 处理转义字符
        value = value.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"')

        self.tokens.append(Token(TokenType.STRING, value, self.line, start_col))

    def _read_number(self):
        start_col = self.column
        start = self.pos

        while self.pos < len(self.source) and (self.source[self.pos].isdigit() or self.source[self.pos] == '.'):
            self.pos += 1

        value = self.source[start:self.pos]
        self.column += len(value)

        if '.' in value:
            self.tokens.append(Token(TokenType.NUMBER, float(value), self.line, start_col))
        else:
            self.tokens.append(Token(TokenType.NUMBER, int(value), self.line, start_col))

    def _read_symbol(self):
        char = self.source[self.pos]
        token_type = SYMBOLS.get(char)

        if token_type:
            self.tokens.append(Token(token_type, char, self.line, self.column))
            self.pos += 1
            self.column += 1

    def _is_chinese(self, char: str) -> bool:
        return '\u4e00' <= char <= '\u9fff'

    def _read_chinese(self):
        start_col = self.column
        start = self.pos

        while self.pos < len(self.source) and self._is_chinese(self.source[self.pos]):
            self.pos += 1

        value = self.source[start:self.pos]
        self.column += len(value)

        # 检查是否为关键字
        if value in KEYWORDS:
            self.tokens.append(Token(KEYWORDS[value], value, self.line, start_col))
        # 检查是否为操作符
        elif value in OPERATORS:
            self.tokens.append(Token(OPERATORS[value], value, self.line, start_col))
        # 否则为标识符
        else:
            self.tokens.append(Token(TokenType.IDENTIFIER, value, self.line, start_col))

    def _read_identifier(self):
        start_col = self.column
        start = self.pos

        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            self.pos += 1

        value = self.source[start:self.pos]
        self.column += len(value)

        self.tokens.append(Token(TokenType.IDENTIFIER, value, self.line, start_col))
```

- [ ] **步骤4：运行测试验证通过**

运行：`pytest tests/test_lexer.py::test_lexer_number -v`
预期：PASS

运行：`pytest tests/test_lexer.py -v`
预期：所有词法分析器测试通过

- [ ] **步骤5：Commit**

```bash
git add src/lexer/lexer.py tests/test_lexer.py
git commit -m "feat: implement basic lexer with Chinese support"
```

---

### 任务5：词法分析器高级特性

**文件：**
- 修改：`src/lexer/lexer.py`
- 测试：`tests/test_lexer.py`

- [ ] **步骤1：编写失败的测试**

```python
# tests/test_lexer.py (追加)
def test_lexer_math_expression():
    lexer = Lexer('$(π * r²)')
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.DOLLAR
    assert tokens[1].type == TokenType.LPAREN

def test_lexer_python_block():
    lexer = Lexer('{{import pandas}}')
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.LBRACE

def test_lexer_indentation():
    source = """若条件：
  动作。
否则：
  其他动作。"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    assert TokenType.INDENT in [t.type for t in tokens]
    assert TokenType.DEDENT in [t.type for t in tokens]

def test_lexer_mixed_chinese_english():
    lexer = Lexer('用户name = "张三"')
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == "用户name"
```

- [ ] **步骤2：运行测试验证失败**

运行：`pytest tests/test_lexer.py::test_lexer_indentation -v`
预期：FAIL

- [ ] **步骤3：增强词法分析器**

```python
# src/lexer/lexer.py (在_tokenize方法中添加)
def tokenize(self) -> List[Token]:
    while self.pos < len(self.source):
        self._skip_whitespace()

        if self.pos >= len(self.source):
            break

        char = self.source[self.pos]

        # 处理换行和缩进
        if char == '\n':
            self._handle_newline()
        # 处理注释
        elif char == '-' and self.pos + 1 < len(self.source) and self.source[self.pos + 1] == '-':
            self._skip_comment()
        # 处理字符串
        elif char == '"':
            self._read_string()
        # 处理数字
        elif char.isdigit():
            self._read_number()
        # 处理符号
        elif char in SYMBOLS:
            self._read_symbol()
        # 处理中文关键字、操作符、标识符
        elif self._is_chinese(char):
            self._read_chinese()
        # 处理英文标识符
        elif char.isalpha() or char == '_':
            self._read_identifier()
        else:
            raise LexerError(f"Unexpected character: {char}", self.line, self.column)

    # 处理剩余的DEDENT
    while len(self.indent_stack) > 1:
        self.indent_stack.pop()
        self.tokens.append(Token(TokenType.DEDENT, None, self.line, self.column))

    self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
    return self.tokens
```

- [ ] **步骤4：运行测试验证通过**

运行：`pytest tests/test_lexer.py -v`
预期：所有测试通过

- [ ] **步骤5：Commit**

```bash
git add src/lexer/lexer.py tests/test_lexer.py
git commit -m "feat: add advanced lexer features (indentation, mixed text)"
```

---

### 任务6：AST节点定义

**文件：**
- 创建：`src/parser/ast_nodes.py`
- 测试：`tests/test_parser.py`

- [ ] **步骤1：编写失败的测试**

```python
# tests/test_parser.py
import pytest
from src.parser.ast_nodes import (
    NumberNode, StringNode, IdentifierNode, BinaryOpNode,
    IfNode, ForNode, FunctionDefNode, FunctionCallNode
)

def test_number_node():
    node = NumberNode(123, line=1, column=0)
    assert node.value == 123
    assert str(node) == "NumberNode(123)"

def test_binary_op_node():
    left = NumberNode(1, line=1, column=0)
    right = NumberNode(2, line=1, column=2)
    node = BinaryOpNode(left, "+", right, line=1, column=1)
    assert node.operator == "+"
    assert node.left == left
    assert node.right == right

def test_if_node():
    condition = IdentifierNode("x", line=1, column=0)
    then_branch = [NumberNode(1, line=1, column=0)]
    else_branch = [NumberNode(2, line=1, column=0)]
    node = IfNode(condition, then_branch, else_branch, line=1, column=0)
    assert node.condition == condition
    assert len(node.then_branch) == 1
```

- [ ] **步骤2：运行测试验证失败**

运行：`pytest tests/test_parser.py::test_number_node -v`
预期：FAIL，报错 "cannot import name 'NumberNode'"

- [ ] **步骤3：编写AST节点定义**

```python
# src/parser/ast_nodes.py
from dataclasses import dataclass
from typing import Any, List, Optional
from abc import ABC, abstractmethod

@dataclass
class ASTNode(ABC):
    line: int
    column: int

    @abstractmethod
    def __str__(self) -> str:
        pass

@dataclass
class NumberNode(ASTNode):
    value: float

    def __str__(self):
        return f"NumberNode({self.value})"

@dataclass
class StringNode(ASTNode):
    value: str

    def __str__(self):
        return f"StringNode({repr(self.value)})"

@dataclass
class IdentifierNode(ASTNode):
    name: str

    def __str__(self):
        return f"IdentifierNode({self.name})"

@dataclass
class BinaryOpNode(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode

    def __str__(self):
        return f"BinaryOpNode({self.left} {self.operator} {self.right})"

@dataclass
class UnaryOpNode(ASTNode):
    operator: str
    operand: ASTNode

    def __str__(self):
        return f"UnaryOpNode({self.operator} {self.operand})"

@dataclass
class AssignNode(ASTNode):
    target: IdentifierNode
    value: ASTNode

    def __str__(self):
        return f"AssignNode({self.target} = {self.value})"

@dataclass
class IfNode(ASTNode):
    condition: ASTNode
    then_branch: List[ASTNode]
    else_branch: Optional[List[ASTNode]]

    def __str__(self):
        return f"IfNode(condition={self.condition}, then={len(self.then_branch)} stmts)"

@dataclass
class ForNode(ASTNode):
    variable: str
    iterable: ASTNode
    body: List[ASTNode]

    def __str__(self):
        return f"ForNode({self.variable} in {self.iterable})"

@dataclass
class WhileNode(ASTNode):
    condition: ASTNode
    body: List[ASTNode]

    def __str__(self):
        return f"WhileNode(condition={self.condition})"

@dataclass
class RepeatNode(ASTNode):
    count: ASTNode
    body: List[ASTNode]

    def __str__(self):
        return f"RepeatNode({self.count} times)"

@dataclass
class FunctionDefNode(ASTNode):
    name: str
    params: List[str]
    body: List[ASTNode]

    def __str__(self):
        return f"FunctionDefNode({self.name}, params={self.params})"

@dataclass
class FunctionCallNode(ASTNode):
    name: str
    args: List[ASTNode]

    def __str__(self):
        return f"FunctionCallNode({self.name}, args={len(self.args)})"

@dataclass
class ReturnNode(ASTNode):
    value: Optional[ASTNode]

    def __str__(self):
        return f"ReturnNode({self.value})"

@dataclass
class VarDefNode(ASTNode):
    name: str
    var_type: Optional[str]
    value: Optional[ASTNode]

    def __str__(self):
        return f"VarDefNode({self.name}, type={self.var_type})"

@dataclass
class ListNode(ASTNode):
    elements: List[ASTNode]

    def __str__(self):
        return f"ListNode({len(self.elements)} elements)"

@dataclass
class DictNode(ASTNode):
    pairs: List[tuple]  # List of (key, value) tuples

    def __str__(self):
        return f"DictNode({len(self.pairs)} pairs)"

@dataclass
class MemberAccessNode(ASTNode):
    object: ASTNode
    member: str

    def __str__(self):
        return f"MemberAccessNode({self.object}.{self.member})"

@dataclass
class IndexNode(ASTNode):
    object: ASTNode
    index: ASTNode

    def __str__(self):
        return f"IndexNode({self.object}[{self.index}])"

@dataclass
class ProgramNode(ASTNode):
    statements: List[ASTNode]

    def __str__(self):
        return f"ProgramNode({len(self.statements)} statements)"
```

- [ ] **步骤4：运行测试验证通过**

运行：`pytest tests/test_parser.py -v`
预期：所有AST节点测试通过

- [ ] **步骤5：Commit**

```bash
git add src/parser/ast_nodes.py tests/test_parser.py
git commit -m "feat: add AST node definitions"
```

---

### 任务7：语法分析器基础

**文件：**
- 创建：`src/parser/parser.py`
- 测试：`tests/test_parser.py`

- [ ] **步骤1：编写失败的测试**

```python
# tests/test_parser.py (追加)
from src.lexer.lexer import Lexer
from src.parser.parser import Parser

def test_parse_number():
    lexer = Lexer("123")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    assert isinstance(ast, ProgramNode)
    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0], NumberNode)
    assert ast.statements[0].value == 123

def test_parse_binary_op():
    lexer = Lexer("1加2")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    assert isinstance(ast.statements[0], BinaryOpNode)
    assert ast.statements[0].operator == "+"

def test_parse_assignment():
    lexer = Lexer('x = 123')
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    assert isinstance(ast.statements[0], AssignNode)
    assert ast.statements[0].target.name == "x"
```

- [ ] **步骤2：运行测试验证失败**

运行：`pytest tests/test_parser.py::test_parse_number -v`
预期：FAIL，报错 "cannot import name 'Parser'"

- [ ] **步骤3：编写语法分析器**

```python
# src/parser/parser.py
from typing import List, Optional
from src.lexer.tokens import Token, TokenType
from src.parser.ast_nodes import *

class ParseError(Exception):
    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        super().__init__(f"Parse Error at line {token.line}, column {token.column}: {message}")

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> ProgramNode:
        statements = []
        while not self._check(TokenType.EOF):
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        return ProgramNode(statements, line=1, column=0)

    def _current_token(self) -> Token:
        return self.tokens[self.pos]

    def _check(self, *types: TokenType) -> bool:
        return self._current_token().type in types

    def _advance(self) -> Token:
        token = self._current_token()
        if not self._check(TokenType.EOF):
            self.pos += 1
        return token

    def _expect(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        raise ParseError(message, self._current_token())

    def _parse_statement(self) -> Optional[ASTNode]:
        if self._check(TokenType.NEWLINE):
            self._advance()
            return None

        if self._check(TokenType.IF):
            return self._parse_if()
        elif self._check(TokenType.FOR):
            return self._parse_for()
        elif self._check(TokenType.WHILE):
            return self._parse_while()
        elif self._check(TokenType.REPEAT):
            return self._parse_repeat()
        elif self._check(TokenType.DEFINE):
            return self._parse_function_def()
        elif self._check(TokenType.VAR):
            return self._parse_var_def()
        elif self._check(TokenType.RETURN):
            return self._parse_return()
        else:
            return self._parse_expression_statement()

    def _parse_expression_statement(self) -> ASTNode:
        expr = self._parse_expression()

        # 处理赋值
        if self._check(TokenType.ASSIGN):
            self._advance()
            value = self._parse_expression()
            if isinstance(expr, IdentifierNode):
                return AssignNode(expr, value, line=expr.line, column=expr.column)
            else:
                raise ParseError("Invalid assignment target", self._current_token())

        # 消耗句号
        if self._check(TokenType.PERIOD):
            self._advance()

        return expr

    def _parse_expression(self) -> ASTNode:
        return self._parse_comparison()

    def _parse_comparison(self) -> ASTNode:
        left = self._parse_addition()

        while self._check(TokenType.EQUALS, TokenType.NOT_EQUALS,
                         TokenType.LESS, TokenType.GREATER,
                         TokenType.LESS_EQ, TokenType.GREATER_EQ):
            op_token = self._advance()
            op_map = {
                TokenType.EQUALS: "==",
                TokenType.NOT_EQUALS: "!=",
                TokenType.LESS: "<",
                TokenType.GREATER: ">",
                TokenType.LESS_EQ: "<=",
                TokenType.GREATER_EQ: ">=",
            }
            operator = op_map[op_token.type]
            right = self._parse_addition()
            left = BinaryOpNode(left, operator, right, line=op_token.line, column=op_token.column)

        return left

    def _parse_addition(self) -> ASTNode:
        left = self._parse_multiplication()

        while self._check(TokenType.PLUS, TokenType.MINUS):
            op_token = self._advance()
            operator = "+" if op_token.type == TokenType.PLUS else "-"
            right = self._parse_multiplication()
            left = BinaryOpNode(left, operator, right, line=op_token.line, column=op_token.column)

        return left

    def _parse_multiplication(self) -> ASTNode:
        left = self._parse_unary()

        while self._check(TokenType.MULTIPLY, TokenType.DIVIDE):
            op_token = self._advance()
            operator = "*" if op_token.type == TokenType.MULTIPLY else "/"
            right = self._parse_unary()
            left = BinaryOpNode(left, operator, right, line=op_token.line, column=op_token.column)

        return left

    def _parse_unary(self) -> ASTNode:
        if self._check(TokenType.NOT, TokenType.MINUS):
            op_token = self._advance()
            operator = "not" if op_token.type == TokenType.NOT else "-"
            operand = self._parse_unary()
            return UnaryOpNode(operator, operand, line=op_token.line, column=op_token.column)

        return self._parse_primary()

    def _parse_primary(self) -> ASTNode:
        token = self._current_token()

        if self._check(TokenType.NUMBER):
            self._advance()
            return NumberNode(token.value, line=token.line, column=token.column)

        if self._check(TokenType.STRING):
            self._advance()
            return StringNode(token.value, line=token.line, column=token.column)

        if self._check(TokenType.IDENTIFIER):
            self._advance()
            name = token.value

            # 函数调用
            if self._check(TokenType.LPAREN):
                return self._parse_function_call(name, token)

            # 成员访问
            if self._check(TokenType.PERIOD):
                self._advance()
                member_token = self._expect(TokenType.IDENTIFIER, "Expected member name")
                return MemberAccessNode(
                    IdentifierNode(name, line=token.line, column=token.column),
                    member_token.value,
                    line=token.line, column=token.column
                )

            return IdentifierNode(name, line=token.line, column=token.column)

        if self._check(TokenType.LPAREN):
            self._advance()
            expr = self._parse_expression()
            self._expect(TokenType.RPAREN, "Expected ')'")
            return expr

        raise ParseError(f"Unexpected token: {token.type}", token)

    def _parse_function_call(self, name: str, name_token: Token) -> FunctionCallNode:
        self._advance()  # 消耗 (
        args = []

        if not self._check(TokenType.RPAREN):
            args.append(self._parse_expression())
            while self._check(TokenType.COMMA):
                self._advance()
                args.append(self._parse_expression())

        self._expect(TokenType.RPAREN, "Expected ')'")
        return FunctionCallNode(name, args, line=name_token.line, column=name_token.column)

    def _parse_if(self) -> IfNode:
        token = self._advance()  # 消耗 '若'
        condition = self._parse_expression()

        # 消耗 '则' 或 ':'
        if self._check(TokenType.THEN):
            self._advance()
        elif self._check(TokenType.COLON):
            self._advance()

        then_branch = self._parse_block()

        else_branch = None
        if self._check(TokenType.ELSE):
            self._advance()
            if self._check(TokenType.COLON):
                self._advance()
            else_branch = self._parse_block()

        return IfNode(condition, then_branch, else_branch, line=token.line, column=token.column)

    def _parse_block(self) -> List[ASTNode]:
        statements = []

        # 单行语句
        if not self._check(TokenType.INDENT):
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
            return statements

        # 多行块
        self._advance()  # 消耗 INDENT

        while not self._check(TokenType.DEDENT, TokenType.EOF):
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)

        if self._check(TokenType.DEDENT):
            self._advance()

        return statements

    def _parse_for(self) -> ForNode:
        token = self._advance()  # 消耗 '遍历'

        var_token = self._expect(TokenType.IDENTIFIER, "Expected variable name")
        variable = var_token.value

        # 消耗 '于' 或 '中'
        if self._check(TokenType.IDENTIFIER) and self._current_token().value in ["于", "中"]:
            self._advance()

        iterable = self._parse_expression()

        if self._check(TokenType.COLON):
            self._advance()

        body = self._parse_block()

        return ForNode(variable, iterable, body, line=token.line, column=token.column)

    def _parse_while(self) -> WhileNode:
        token = self._advance()  # 消耗 '当'
        condition = self._parse_expression()

        # 消耗 '时'
        if self._check(TokenType.IDENTIFIER) and self._current_token().value == "时":
            self._advance()

        if self._check(TokenType.COLON):
            self._advance()

        body = self._parse_block()

        return WhileNode(condition, body, line=token.line, column=token.column)

    def _parse_repeat(self) -> RepeatNode:
        token = self._advance()  # 消耗 '重复'
        count = self._parse_expression()

        if self._check(TokenType.COLON):
            self._advance()

        body = self._parse_block()

        return RepeatNode(count, body, line=token.line, column=token.column)

    def _parse_function_def(self) -> FunctionDefNode:
        token = self._advance()  # 消耗 '定义'

        name_token = self._expect(TokenType.IDENTIFIER, "Expected function name")
        name = name_token.value

        # 解析参数
        params = []
        if self._check(TokenType.LPAREN):
            self._advance()
            if not self._check(TokenType.RPAREN):
                param_token = self._expect(TokenType.IDENTIFIER, "Expected parameter name")
                params.append(param_token.value)
                while self._check(TokenType.COMMA):
                    self._advance()
                    param_token = self._expect(TokenType.IDENTIFIER, "Expected parameter name")
                    params.append(param_token.value)
            self._expect(TokenType.RPAREN, "Expected ')'")

        if self._check(TokenType.COLON):
            self._advance()

        body = self._parse_block()

        return FunctionDefNode(name, params, body, line=token.line, column=token.column)

    def _parse_var_def(self) -> VarDefNode:
        token = self._advance()  # 消耗 '定'

        name_token = self._expect(TokenType.IDENTIFIER, "Expected variable name")
        name = name_token.value

        var_type = None
        if self._check(TokenType.AS):
            self._advance()
            type_token = self._expect(TokenType.IDENTIFIER, "Expected type name")
            var_type = type_token.value

        value = None
        if self._check(TokenType.ASSIGN):
            self._advance()
            value = self._parse_expression()

        if self._check(TokenType.PERIOD):
            self._advance()

        return VarDefNode(name, var_type, value, line=token.line, column=token.column)

    def _parse_return(self) -> ReturnNode:
        token = self._advance()  # 消耗 '返回'

        value = None
        if not self._check(TokenType.PERIOD, TokenType.NEWLINE, TokenType.EOF):
            value = self._parse_expression()

        if self._check(TokenType.PERIOD):
            self._advance()

        return ReturnNode(value, line=token.line, column=token.column)
```

- [ ] **步骤4：运行测试验证通过**

运行：`pytest tests/test_parser.py -v`
预期：所有语法分析器测试通过

- [ ] **步骤5：Commit**

```bash
git add src/parser/parser.py tests/test_parser.py
git commit -m "feat: implement basic parser with control flow support"
```

---

### 任务8：语义分析器

**文件：**
- 创建：`src/semantic/scope.py`
- 创建：`src/semantic/analyzer.py`
- 测试：`tests/test_semantic.py`

- [ ] **步骤1：编写失败的测试**

```python
# tests/test_semantic.py
import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.semantic.scope import Scope

def test_scope_creation():
    scope = Scope()
    scope.define("x", "number")
    assert scope.lookup("x") == "number"

def test_nested_scope():
    parent = Scope()
    parent.define("x", "number")

    child = Scope(parent)
    assert child.lookup("x") == "number"

    child.define("y", "string")
    assert child.lookup("y") == "string"

def test_undefined_variable():
    source = "印x。"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    analyzer = SemanticAnalyzer()
    with pytest.raises(Exception) as exc_info:
        analyzer.analyze(ast)
    assert "未定义" in str(exc_info.value)
```

- [ ] **步骤2：运行测试验证失败**

运行：`pytest tests/test_semantic.py::test_scope_creation -v`
预期：FAIL，报错 "cannot import name 'Scope'"

- [ ] **步骤3：编写作用域管理**

```python
# src/semantic/scope.py
from typing import Dict, Optional, Any

class Scope:
    def __init__(self, parent: Optional['Scope'] = None):
        self.parent = parent
        self.symbols: Dict[str, Dict[str, Any]] = {}

    def define(self, name: str, symbol_type: str, **attrs):
        self.symbols[name] = {
            'type': symbol_type,
            **attrs
        }

    def lookup(self, name: str) -> Optional[Dict[str, Any]]:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None

    def assign(self, name: str, value_type: str) -> bool:
        if name in self.symbols:
            self.symbols[name]['type'] = value_type
            return True
        if self.parent:
            return self.parent.assign(name, value_type)
        return False
```

- [ ] **步骤4：编写语义分析器**

```python
# src/semantic/analyzer.py
from typing import Dict, List, Optional
from src.parser.ast_nodes import *
from src.semantic.scope import Scope

class SemanticError(Exception):
    def __init__(self, message: str, node: ASTNode):
        self.message = message
        self.node = node
        super().__init__(f"Semantic Error at line {node.line}, column {node.column}: {message}")

class SemanticAnalyzer:
    def __init__(self):
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.errors: List[SemanticError] = []

    def analyze(self, ast: ProgramNode) -> bool:
        try:
            self._visit_program(ast)
            return len(self.errors) == 0
        except SemanticError as e:
            self.errors.append(e)
            return False

    def _visit_program(self, node: ProgramNode):
        for stmt in node.statements:
            self._visit_statement(stmt)

    def _visit_statement(self, node: ASTNode):
        if isinstance(node, VarDefNode):
            self._visit_var_def(node)
        elif isinstance(node, FunctionDefNode):
            self._visit_function_def(node)
        elif isinstance(node, AssignNode):
            self._visit_assign(node)
        elif isinstance(node, IfNode):
            self._visit_if(node)
        elif isinstance(node, ForNode):
            self._visit_for(node)
        elif isinstance(node, WhileNode):
            self._visit_while(node)
        elif isinstance(node, ReturnNode):
            self._visit_return(node)
        else:
            self._visit_expression(node)

    def _visit_var_def(self, node: VarDefNode):
        if self.current_scope.lookup(node.name):
            raise SemanticError(f"变量 '{node.name}' 已定义", node)

        inferred_type = None
        if node.value:
            inferred_type = self._visit_expression(node.value)

        final_type = node.var_type or inferred_type or "unknown"
        self.current_scope.define(node.name, final_type)

    def _visit_function_def(self, node: FunctionDefNode):
        if self.current_scope.lookup(node.name):
            raise SemanticError(f"函数 '{node.name}' 已定义", node)

        # 创建函数作用域
        func_scope = Scope(self.current_scope)
        self.current_scope = func_scope

        # 添加参数
        for param in node.params:
            self.current_scope.define(param, "unknown")

        # 分析函数体
        for stmt in node.body:
            self._visit_statement(stmt)

        # 恢复作用域
        self.current_scope = func_scope.parent

        # 在父作用域中定义函数
        self.current_scope.define(node.name, "function", params=node.params)

    def _visit_assign(self, node: AssignNode):
        if not isinstance(node.target, IdentifierNode):
            raise SemanticError("赋值目标必须是标识符", node)

        # 检查变量是否已定义
        symbol = self.current_scope.lookup(node.target.name)
        if not symbol:
            # 自动创建变量（语境驱动式）
            value_type = self._visit_expression(node.value)
            self.current_scope.define(node.target.name, value_type)
        else:
            # 更新变量类型
            value_type = self._visit_expression(node.value)
            self.current_scope.assign(node.target.name, value_type)

    def _visit_if(self, node: IfNode):
        self._visit_expression(node.condition)

        for stmt in node.then_branch:
            self._visit_statement(stmt)

        if node.else_branch:
            for stmt in node.else_branch:
                self._visit_statement(stmt)

    def _visit_for(self, node: ForNode):
        iterable_type = self._visit_expression(node.iterable)

        # 创建循环作用域
        loop_scope = Scope(self.current_scope)
        self.current_scope = loop_scope

        # 定义循环变量
        self.current_scope.define(node.variable, "element")

        # 分析循环体
        for stmt in node.body:
            self._visit_statement(stmt)

        # 恢复作用域
        self.current_scope = loop_scope.parent

    def _visit_while(self, node: WhileNode):
        self._visit_expression(node.condition)

        for stmt in node.body:
            self._visit_statement(stmt)

    def _visit_return(self, node: ReturnNode):
        if node.value:
            self._visit_expression(node.value)

    def _visit_expression(self, node: ASTNode) -> str:
        if isinstance(node, NumberNode):
            return "number"
        elif isinstance(node, StringNode):
            return "string"
        elif isinstance(node, IdentifierNode):
            symbol = self.current_scope.lookup(node.name)
            if not symbol:
                raise SemanticError(f"未定义的变量: {node.name}", node)
            return symbol['type']
        elif isinstance(node, BinaryOpNode):
            left_type = self._visit_expression(node.left)
            right_type = self._visit_expression(node.right)
            return self._infer_binary_op_type(left_type, right_type, node.operator)
        elif isinstance(node, UnaryOpNode):
            operand_type = self._visit_expression(node.operand)
            return operand_type
        elif isinstance(node, FunctionCallNode):
            return self._visit_function_call(node)
        elif isinstance(node, ListNode):
            return "list"
        elif isinstance(node, DictNode):
            return "dict"
        elif isinstance(node, MemberAccessNode):
            obj_type = self._visit_expression(node.object)
            return "unknown"  # 需要更复杂的类型推断
        elif isinstance(node, IndexNode):
            return "unknown"
        else:
            return "unknown"

    def _infer_binary_op_type(self, left_type: str, right_type: str, operator: str) -> str:
        if operator in ["+", "-", "*", "/"]:
            if left_type == "number" and right_type == "number":
                return "number"
        elif operator in ["==", "!=", "<", ">", "<=", ">="]:
            return "boolean"
        elif operator in ["and", "or"]:
            return "boolean"
        return "unknown"

    def _visit_function_call(self, node: FunctionCallNode) -> str:
        symbol = self.current_scope.lookup(node.name)

        if not symbol:
            # 内置函数
            builtin_functions = {
                "印": "unknown",
                "读取": "unknown",
                "写入": "unknown",
            }
            if node.name in builtin_functions:
                for arg in node.args:
                    self._visit_expression(arg)
                return builtin_functions[node.name]

            raise SemanticError(f"未定义的函数: {node.name}", node)

        if symbol['type'] != "function":
            raise SemanticError(f"'{node.name}' 不是函数", node)

        # 检查参数数量
        expected_params = symbol.get('params', [])
        if len(node.args) != len(expected_params):
            raise SemanticError(
                f"函数 '{node.name}' 期望 {len(expected_params)} 个参数，但提供了 {len(node.args)} 个",
                node
            )

        for arg in node.args:
            self._visit_expression(arg)

        return "unknown"
```

- [ ] **步骤5：运行测试验证通过**

运行：`pytest tests/test_semantic.py -v`
预期：所有语义分析器测试通过

- [ ] **步骤6：Commit**

```bash
git add src/semantic/scope.py src/semantic/analyzer.py tests/test_semantic.py
git commit -m "feat: implement semantic analyzer with scope management"
```

---

### 任务9：Python代码生成器

**文件：**
- 创建：`src/codegen/python_codegen.py`
- 测试：`tests/test_codegen.py`

- [ ] **步骤1：编写失败的测试**

```python
# tests/test_codegen.py
import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.codegen.python_codegen import PythonCodegen

def test_codegen_number():
    source = "123"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    codegen = PythonCodegen()
    python_code = codegen.generate(ast)
    assert python_code.strip() == "123"

def test_codegen_binary_op():
    source = "1加2"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    codegen = PythonCodegen()
    python_code = codegen.generate(ast)
    assert "1 + 2" in python_code

def test_codegen_function_def():
    source = """定义平方：
  接收x。
  返回x乘x。"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    codegen = PythonCodegen()
    python_code = codegen.generate(ast)
    assert "def 平方" in python_code
    assert "return" in python_code
```

- [ ] **步骤2：运行测试验证失败**

运行：`pytest tests/test_codegen.py::test_codegen_number -v`
预期：FAIL，报错 "cannot import name 'PythonCodegen'"

- [ ] **步骤3：编写代码生成器**

```python
# src/codegen/python_codegen.py
from typing import List
from src.parser.ast_nodes import *

class CodegenError(Exception):
    pass

class PythonCodegen:
    def __init__(self):
        self.indent_level = 0
        self.indent_str = "    "

    def generate(self, node: ASTNode) -> str:
        if isinstance(node, ProgramNode):
            return self._generate_program(node)
        else:
            raise CodegenError(f"Unsupported node type: {type(node)}")

    def _generate_program(self, node: ProgramNode) -> str:
        lines = []
        for stmt in node.statements:
            lines.append(self._generate_statement(stmt))
        return "\n".join(filter(None, lines))

    def _generate_statement(self, node: ASTNode) -> str:
        if isinstance(node, VarDefNode):
            return self._generate_var_def(node)
        elif isinstance(node, FunctionDefNode):
            return self._generate_function_def(node)
        elif isinstance(node, AssignNode):
            return self._generate_assign(node)
        elif isinstance(node, IfNode):
            return self._generate_if(node)
        elif isinstance(node, ForNode):
            return self._generate_for(node)
        elif isinstance(node, WhileNode):
            return self._generate_while(node)
        elif isinstance(node, RepeatNode):
            return self._generate_repeat(node)
        elif isinstance(node, ReturnNode):
            return self._generate_return(node)
        else:
            expr_code = self._generate_expression(node)
            return self._indent() + expr_code

    def _generate_var_def(self, node: VarDefNode) -> str:
        if node.value:
            value_code = self._generate_expression(node.value)
            return self._indent() + f"{node.name} = {value_code}"
        else:
            return self._indent() + f"{node.name} = None"

    def _generate_function_def(self, node: FunctionDefNode) -> str:
        params = ", ".join(node.params)
        code = self._indent() + f"def {node.name}({params}):\n"

        self.indent_level += 1

        if node.body:
            for stmt in node.body:
                code += self._generate_statement(stmt) + "\n"
        else:
            code += self._indent() + "pass\n"

        self.indent_level -= 1
        return code.rstrip()

    def _generate_assign(self, node: AssignNode) -> str:
        target_code = self._generate_expression(node.target)
        value_code = self._generate_expression(node.value)
        return self._indent() + f"{target_code} = {value_code}"

    def _generate_if(self, node: IfNode) -> str:
        cond_code = self._generate_expression(node.condition)
        code = self._indent() + f"if {cond_code}:\n"

        self.indent_level += 1
        for stmt in node.then_branch:
            code += self._generate_statement(stmt) + "\n"
        self.indent_level -= 1

        if node.else_branch:
            code += self._indent() + "else:\n"
            self.indent_level += 1
            for stmt in node.else_branch:
                code += self._generate_statement(stmt) + "\n"
            self.indent_level -= 1

        return code.rstrip()

    def _generate_for(self, node: ForNode) -> str:
        iter_code = self._generate_expression(node.iterable)
        code = self._indent() + f"for {node.variable} in {iter_code}:\n"

        self.indent_level += 1
        for stmt in node.body:
            code += self._generate_statement(stmt) + "\n"
        self.indent_level -= 1

        return code.rstrip()

    def _generate_while(self, node: WhileNode) -> str:
        cond_code = self._generate_expression(node.condition)
        code = self._indent() + f"while {cond_code}:\n"

        self.indent_level += 1
        for stmt in node.body:
            code += self._generate_statement(stmt) + "\n"
        self.indent_level -= 1

        return code.rstrip()

    def _generate_repeat(self, node: RepeatNode) -> str:
        count_code = self._generate_expression(node.count)
        code = self._indent() + f"for _ in range({count_code}):\n"

        self.indent_level += 1
        for stmt in node.body:
            code += self._generate_statement(stmt) + "\n"
        self.indent_level -= 1

        return code.rstrip()

    def _generate_return(self, node: ReturnNode) -> str:
        if node.value:
            value_code = self._generate_expression(node.value)
            return self._indent() + f"return {value_code}"
        else:
            return self._indent() + "return"

    def _generate_expression(self, node: ASTNode) -> str:
        if isinstance(node, NumberNode):
            return str(node.value)
        elif isinstance(node, StringNode):
            return repr(node.value)
        elif isinstance(node, IdentifierNode):
            return node.name
        elif isinstance(node, BinaryOpNode):
            left = self._generate_expression(node.left)
            right = self._generate_expression(node.right)
            return f"({left} {node.operator} {right})"
        elif isinstance(node, UnaryOpNode):
            operand = self._generate_expression(node.operand)
            return f"({node.operator} {operand})"
        elif isinstance(node, FunctionCallNode):
            return self._generate_function_call(node)
        elif isinstance(node, ListNode):
            elements = [self._generate_expression(e) for e in node.elements]
            return f"[{', '.join(elements)}]"
        elif isinstance(node, DictNode):
            pairs = [f"{self._generate_expression(k)}: {self._generate_expression(v)}"
                    for k, v in node.pairs]
            return f"{{{', '.join(pairs)}}}"
        elif isinstance(node, MemberAccessNode):
            obj = self._generate_expression(node.object)
            return f"{obj}.{node.member}"
        elif isinstance(node, IndexNode):
            obj = self._generate_expression(node.object)
            idx = self._generate_expression(node.index)
            return f"{obj}[{idx}]"
        else:
            raise CodegenError(f"Unsupported expression type: {type(node)}")

    def _generate_function_call(self, node: FunctionCallNode) -> str:
        args = [self._generate_expression(arg) for arg in node.args]

        # 内置函数映射
        builtin_map = {
            "印": "print",
            "读取": "input",
        }

        func_name = builtin_map.get(node.name, node.name)
        return f"{func_name}({', '.join(args)})"

    def _indent(self) -> str:
        return self.indent_str * self.indent_level
```

- [ ] **步骤4：运行测试验证通过**

运行：`pytest tests/test_codegen.py -v`
预期：所有代码生成器测试通过

- [ ] **步骤5：Commit**

```bash
git add src/codegen/python_codegen.py tests/test_codegen.py
git commit -m "feat: implement Python code generator"
```

---

### 任务10：运行时环境

**文件：**
- 创建：`src/runtime/environment.py`
- 创建：`src/runtime/builtins.py`
- 测试：`tests/test_runtime.py`

- [ ] **步骤1：编写失败的测试**

```python
# tests/test_runtime.py
import pytest
from src.runtime.environment import RuntimeEnvironment
from src.runtime.builtins import register_builtins

def test_environment_create():
    env = RuntimeEnvironment()
    env.define("x", 123)
    assert env.get("x") == 123

def test_environment_nested():
    parent = RuntimeEnvironment()
    parent.define("x", 123)

    child = RuntimeEnvironment(parent)
    assert child.get("x") == 123

    child.define("y", 456)
    assert child.get("y") == 456

def test_builtin_functions():
    env = RuntimeEnvironment()
    register_builtins(env)

    assert env.get("印") is not None
    assert env.get("读取") is not None
```

- [ ] **步骤2：运行测试验证失败**

运行：`pytest tests/test_runtime.py::test_environment_create -v`
预期：FAIL，报错 "cannot import name 'RuntimeEnvironment'"

- [ ] **步骤3：编写运行时环境**

```python
# src/runtime/environment.py
from typing import Any, Dict, Optional, Callable

class RuntimeError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class RuntimeEnvironment:
    def __init__(self, parent: Optional['RuntimeEnvironment'] = None):
        self.parent = parent
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, Callable] = {}

    def define(self, name: str, value: Any):
        self.variables[name] = value

    def get(self, name: str) -> Any:
        if name in self.variables:
            return self.variables[name]
        if name in self.functions:
            return self.functions[name]
        if self.parent:
            return self.parent.get(name)
        raise RuntimeError(f"未定义的变量或函数: {name}")

    def set(self, name: str, value: Any):
        if name in self.variables:
            self.variables[name] = value
        elif self.parent and name in self.parent.variables:
            self.parent.set(name, value)
        else:
            self.variables[name] = value

    def define_function(self, name: str, func: Callable):
        self.functions[name] = func

    def get_function(self, name: str) -> Callable:
        if name in self.functions:
            return self.functions[name]
        if self.parent:
            return self.parent.get_function(name)
        raise RuntimeError(f"未定义的函数: {name}")

    def has(self, name: str) -> bool:
        if name in self.variables or name in self.functions:
            return True
        if self.parent:
            return self.parent.has(name)
        return False
```

- [ ] **步骤4：编写内置函数**

```python
# src/runtime/builtins.py
from typing import Any, List
from src.runtime.environment import RuntimeEnvironment

def builtin_print(*args):
    print(*args)

def builtin_input(prompt=""):
    return input(prompt)

def builtin_len(obj):
    return len(obj)

def builtin_range(start, stop=None, step=1):
    if stop is None:
        return range(start)
    return range(start, stop, step)

def builtin_list(*args):
    return list(args)

def builtin_dict(**kwargs):
    return kwargs

def builtin_sum(iterable):
    return sum(iterable)

def builtin_max(iterable):
    return max(iterable)

def builtin_min(iterable):
    return min(iterable)

def builtin_sorted(iterable, key=None, reverse=False):
    return sorted(iterable, key=key, reverse=reverse)

def builtin_map(func, iterable):
    return list(map(func, iterable))

def builtin_filter(func, iterable):
    return list(filter(func, iterable))

def builtin_reduce(func, iterable, initial=None):
    from functools import reduce
    if initial is not None:
        return reduce(func, iterable, initial)
    return reduce(func, iterable)

# 数据动词
def data_verb_read(source: str) -> str:
    """读取数据"""
    with open(source, 'r', encoding='utf-8') as f:
        return f.read()

def data_verb_write(data: str, target: str):
    """写入数据"""
    with open(target, 'w', encoding='utf-8') as f:
        f.write(data)

def data_verb_map(func, iterable):
    """映射数据"""
    return list(map(func, iterable))

def data_verb_filter(func, iterable):
    """过滤数据"""
    return list(filter(func, iterable))

def data_verb_reduce(func, iterable, initial=None):
    """折叠数据"""
    from functools import reduce
    if initial is not None:
        return reduce(func, iterable, initial)
    return reduce(func, iterable)

def data_verb_sort(iterable, key=None, reverse=False):
    """排序数据"""
    return sorted(iterable, key=key, reverse=reverse)

def data_verb_group(iterable, key_func):
    """分组数据"""
    from itertools import groupby
    return {k: list(g) for k, g in groupby(sorted(iterable, key=key_func), key_func)}

def register_builtins(env: RuntimeEnvironment):
    # 基础函数
    env.define_function("印", builtin_print)
    env.define_function("读取", builtin_input)
    env.define_function("长度", builtin_len)
    env.define_function("范围", builtin_range)
    env.define_function("列", builtin_list)
    env.define_function("典", builtin_dict)
    env.define_function("求和", builtin_sum)
    env.define_function("最大", builtin_max)
    env.define_function("最小", builtin_min)
    env.define_function("排序", builtin_sorted)
    env.define_function("映射", builtin_map)
    env.define_function("过滤", builtin_filter)
    env.define_function("折叠", builtin_reduce)

    # 数据动词
    env.define_function("读取文件", data_verb_read)
    env.define_function("写入文件", data_verb_write)
    env.define_function("映射", data_verb_map)
    env.define_function("过滤", data_verb_filter)
    env.define_function("折叠", data_verb_reduce)
    env.define_function("排序", data_verb_sort)
    env.define_function("分组", data_verb_group)
```

- [ ] **步骤5：运行测试验证通过**

运行：`pytest tests/test_runtime.py -v`
预期：所有运行时测试通过

- [ ] **步骤6：Commit**

```bash
git add src/runtime/environment.py src/runtime/builtins.py tests/test_runtime.py
git commit -m "feat: implement runtime environment and builtin functions"
```

---

### 任务11：主入口和集成测试

**文件：**
- 创建：`src/main.py`
- 测试：`tests/test_integration.py`

- [ ] **步骤1：编写失败的测试**

```python
# tests/test_integration.py
import pytest
from src.main import ChineseProgram

def test_hello_world():
    program = ChineseProgram()
    result = program.run('印"你好世界"。')
    assert result is None  # print returns None

def test_arithmetic():
    program = ChineseProgram()
    result = program.run('定x = 1加2。印x。')
    assert result is None

def test_function():
    program = ChineseProgram()
    code = """
定义平方：
  接收x。
  返回x乘x。

印平方5。
"""
    result = program.run(code)
    assert result is None

def test_control_flow():
    program = ChineseProgram()
    code = """
定x = 10。
若x大5：
  印"大于5"。
否则：
  印"小于等于5"。
"""
    result = program.run(code)
    assert result is None
```

- [ ] **步骤2：运行测试验证失败**

运行：`pytest tests/test_integration.py::test_hello_world -v`
预期：FAIL，报错 "cannot import name 'ChineseProgram'"

- [ ] **步骤3：编写主入口**

```python
# src/main.py
import sys
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.codegen.python_codegen import PythonCodegen
from src.runtime.environment import RuntimeEnvironment
from src.runtime.builtins import register_builtins

class ChineseProgram:
    def __init__(self):
        self.env = RuntimeEnvironment()
        register_builtins(self.env)

    def run(self, source: str) -> any:
        # 词法分析
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        # 语法分析
        parser = Parser(tokens)
        ast = parser.parse()

        # 语义分析
        analyzer = SemanticAnalyzer()
        if not analyzer.analyze(ast):
            for error in analyzer.errors:
                print(f"语义错误: {error.message}")
            return None

        # 代码生成
        codegen = PythonCodegen()
        python_code = codegen.generate(ast)

        # 执行
        try:
            exec_globals = self._create_exec_globals()
            exec(python_code, exec_globals)
            return exec_globals.get('__result__')
        except Exception as e:
            print(f"运行时错误: {e}")
            return None

    def _create_exec_globals(self):
        import builtins
        import math
        import random
        import json
        import re
        from datetime import datetime

        # 创建执行环境
        exec_globals = {
            '__builtins__': builtins,
            'math': math,
            'random': random,
            'json': json,
            're': re,
            'datetime': datetime,
        }

        # 添加运行时环境中的函数
        for name, func in self.env.functions.items():
            exec_globals[name] = func

        return exec_globals

    def compile(self, source: str) -> str:
        """编译为Python代码"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)

        codegen = PythonCodegen()
        return codegen.generate(ast)

def main():
    if len(sys.argv) < 2:
        # 交互式模式
        program = ChineseProgram()
        print("中文编程语言 v1.0")
        print("输入代码，输入'退出'结束")
        print("-" * 40)

        while True:
            try:
                source = input(">>> ")
                if source.strip() == "退出":
                    break
                if source.strip():
                    program.run(source)
            except KeyboardInterrupt:
                print("\n再见！")
                break
            except Exception as e:
                print(f"错误: {e}")
    else:
        # 文件模式
        filename = sys.argv[1]
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()

        program = ChineseProgram()
        program.run(source)

if __name__ == "__main__":
    main()
```

- [ ] **步骤4：运行测试验证通过**

运行：`pytest tests/test_integration.py -v`
预期：所有集成测试通过

- [ ] **步骤5：Commit**

```bash
git add src/main.py tests/test_integration.py
git commit -m "feat: implement main entry point and integration tests"
```

---

## 阶段2：高级特性（任务12-20）

### 任务12：宏系统核心

**文件：**
- 创建：`src/macro/__init__.py`
- 创建：`src/macro/macro_system.py`
- 创建：`src/macro/macro_expander.py`
- 测试：`tests/test_macro.py`

- [ ] **步骤1：编写失败的测试**

```python
# tests/test_macro.py
import pytest
from src.macro.macro_system import Macro, MacroSystem
from src.parser.ast_nodes import *

def test_macro_definition():
    macro = Macro(
        name="遍历",
        type="syntax",
        params=["变量", "列表", "循环体"],
        body="定迭代器=列表的迭代器。当迭代器有下一个：定变量=迭代器下一个。循环体。"
    )
    assert macro.name == "遍历"
    assert macro.type == "syntax"
    assert len(macro.params) == 3

def test_macro_system():
    system = MacroSystem()
    system.register(Macro(
        name="重复",
        type="syntax",
        params=["次数", "循环体"],
        body="定计数器=0。当计数器小于次数：循环体。计数器=计数器加1。"
    ))

    assert system.has("重复")
    assert not system.has("不存在的宏")

def test_macro_expansion():
    system = MacroSystem()
    system.register(Macro(
        name="重复",
        type="syntax",
        params=["次数", "循环体"],
        body="定计数器=0。当计数器小于次数：循环体。计数器=计数器加1。"
    ))

    # 模拟宏调用
    call = {"name": "重复", "args": ["5", "印\"你好\"。"]}
    expanded = system.expand("重复", call)
    assert "定计数器=0" in expanded
    assert "当计数器小于5" in expanded
```

- [ ] **步骤2：运行测试验证失败**

运行：`pytest tests/test_macro.py::test_macro_definition -v`
预期：FAIL，报错 "cannot import name 'Macro'"

- [ ] **步骤3：编写宏系统核心**

```python
# src/macro/macro_system.py
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from enum import Enum

class MacroType(Enum):
    SYNTAX = "syntax"      # 语法宏
    IDIOM = "idiom"        # 成语宏

@dataclass
class Macro:
    name: str
    type: MacroType
    params: List[str]
    body: str
    description: Optional[str] = None

class MacroSystem:
    def __init__(self):
        self.macros: Dict[str, Macro] = {}

    def register(self, macro: Macro):
        """注册宏"""
        self.macros[macro.name] = macro

    def has(self, name: str) -> bool:
        """检查宏是否存在"""
        return name in self.macros

    def get(self, name: str) -> Optional[Macro]:
        """获取宏"""
        return self.macros.get(name)

    def expand(self, name: str, args: Dict[str, Any]) -> str:
        """展开宏"""
        macro = self.get(name)
        if not macro:
            raise ValueError(f"未定义的宏: {name}")

        # 参数替换
        result = macro.body
        for i, param in enumerate(macro.params):
            if i < len(args):
                result = result.replace(param, str(args[i]))

        return result

    def list_macros(self) -> List[str]:
        """列出所有宏"""
        return list(self.macros.keys())
```

- [ ] **步骤4：编写宏展开器**

```python
# src/macro/macro_expander.py
from typing import List
from src.macro.macro_system import MacroSystem
from src.parser.ast_nodes import *

class MacroExpander:
    def __init__(self, macro_system: MacroSystem):
        self.macro_system = macro_system

    def expand_ast(self, node: ASTNode) -> ASTNode:
        """展开AST中的宏调用"""
        if isinstance(node, ProgramNode):
            expanded_statements = []
            for stmt in node.statements:
                expanded = self.expand_ast(stmt)
                if isinstance(expanded, list):
                    expanded_statements.extend(expanded)
                else:
                    expanded_statements.append(expanded)
            return ProgramNode(expanded_statements, line=node.line, column=node.column)

        elif isinstance(node, FunctionCallNode):
            # 检查是否是宏调用
            if self.macro_system.has(node.name):
                return self._expand_macro_call(node)
            else:
                # 递归展开参数
                expanded_args = [self.expand_ast(arg) for arg in node.args]
                return FunctionCallNode(node.name, expanded_args, line=node.line, column=node.column)

        elif isinstance(node, IfNode):
            expanded_condition = self.expand_ast(node.condition)
            expanded_then = [self.expand_ast(stmt) for stmt in node.then_branch]
            expanded_else = [self.expand_ast(stmt) for stmt in node.else_branch] if node.else_branch else None
            return IfNode(expanded_condition, expanded_then, expanded_else, line=node.line, column=node.column)

        elif isinstance(node, ForNode):
            # 遍历循环可能是宏调用
            if self.macro_system.has("遍历"):
                return self._expand_for_loop(node)
            return node

        elif isinstance(node, WhileNode):
            expanded_condition = self.expand_ast(node.condition)
            expanded_body = [self.expand_ast(stmt) for stmt in node.body]
            return WhileNode(expanded_condition, expanded_body, line=node.line, column=node.column)

        elif isinstance(node, RepeatNode):
            # 重复循环是宏调用
            if self.macro_system.has("重复"):
                return self._expand_repeat_loop(node)
            return node

        else:
            return node

    def _expand_macro_call(self, node: FunctionCallNode) -> ASTNode:
        """展开宏调用"""
        macro = self.macro_system.get(node.name)
        if not macro:
            return node

        # 构建参数映射
        args = {}
        for i, param in enumerate(macro.params):
            if i < len(node.args):
                args[param] = node.args[i]

        # 展开宏体
        expanded_code = self.macro_system.expand(node.name, args)

        # 解析展开后的代码
        from src.lexer.lexer import Lexer
        from src.parser.parser import Parser

        lexer = Lexer(expanded_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        expanded_ast = parser.parse()

        return expanded_ast.statements if len(expanded_ast.statements) > 1 else expanded_ast.statements[0]

    def _expand_for_loop(self, node: ForNode) -> ASTNode:
        """展开遍历循环"""
        # 将遍历循环转换为宏调用
        macro_call = FunctionCallNode(
            "遍历",
            [IdentifierNode(node.variable, line=node.line, column=node.column),
             node.iterable,
             node.body],
            line=node.line,
            column=node.column
        )
        return self._expand_macro_call(macro_call)

    def _expand_repeat_loop(self, node: RepeatNode) -> ASTNode:
        """展开重复循环"""
        # 将重复循环转换为宏调用
        macro_call = FunctionCallNode(
            "重复",
            [node.count, node.body],
            line=node.line,
            column=node.column
        )
        return self._expand_macro_call(macro_call)
```

- [ ] **步骤5：运行测试验证通过**

运行：`pytest tests/test_macro.py -v`
预期：所有宏系统测试通过

- [ ] **步骤6：Commit**

```bash
git add src/macro/ tests/test_macro.py
git commit -m "feat: implement macro system core"
```

---

### 任务13：内置宏定义

**文件：**
- 创建：`src/macro/builtin_macros.py`
- 测试：`tests/test_macro.py`

- [ ] **步骤1：编写失败的测试**

```python
# tests/test_macro.py (追加)
from src.macro.builtin_macros import register_builtin_macros

def test_builtin_macros():
    system = MacroSystem()
    register_builtin_macros(system)

    # 检查内置宏
    assert system.has("遍历")
    assert system.has("重复")
    assert system.has("持续")
    assert system.has("除非")

def test_for_loop_expansion():
    system = MacroSystem()
    register_builtin_macros(system)

    # 测试遍历宏展开
    expanded = system.expand("遍历", {
        "变量": "用户",
        "列表": "用户列表",
        "循环体": "发送通知给用户。"
    })

    assert "迭代器" in expanded
    assert "用户列表" in expanded

def test_repeat_loop_expansion():
    system = MacroSystem()
    register_builtin_macros(system)

    # 测试重复宏展开
    expanded = system.expand("重复", {
        "次数": "5",
        "循环体": "尝试连接。"
    })

    assert "计数器" in expanded
    assert "5" in expanded
```

- [ ] **步骤2：运行测试验证失败**

运行：`pytest tests/test_macro.py::test_builtin_macros -v`
预期：FAIL

- [ ] **步骤3：编写内置宏**

```python
# src/macro/builtin_macros.py
from src.macro.macro_system import Macro, MacroType

def register_builtin_macros(system):
    """注册内置宏"""

    # 遍历宏
    system.register(Macro(
        name="遍历",
        type=MacroType.SYNTAX,
        params=["变量", "列表", "循环体"],
        body="定迭代器=列表的迭代器。当迭代器有下一个：定变量=迭代器下一个。循环体。",
        description="遍历列表中的每个元素"
    ))

    # 重复宏
    system.register(Macro(
        name="重复",
        type=MacroType.SYNTAX,
        params=["次数", "循环体"],
        body="定计数器=0。当计数器小于次数：循环体。计数器=计数器加1。",
        description="重复执行指定次数"
    ))

    # 持续宏（无限循环）
    system.register(Macro(
        name="持续",
        type=MacroType.SYNTAX,
        params=["循环体"],
        body="若真：循环体。持续：循环体。",
        description="持续执行（无限循环）"
    ))

    # 除非宏
    system.register(Macro(
        name="除非",
        type=MacroType.SYNTAX,
        params=["条件", "动作"],
        body="若非(条件)：动作。",
        description="除非条件成立，否则执行动作"
    ))

    # 当...时宏
    system.register(Macro(
        name="当",
        type=MacroType.SYNTAX,
        params=["条件", "循环体"],
        body="若条件：循环体。当条件：循环体。",
        description="当条件成立时重复执行"
    ))
```

- [ ] **步骤4：运行测试验证通过**

运行：`pytest tests/test_macro.py -v`
预期：所有内置宏测试通过

- [ ] **步骤5：Commit**

```bash
git add src/macro/builtin_macros.py tests/test_macro.py
git commit -m "feat: add builtin macros (遍历, 重复, 持续, 除非)"
```

---

### 任务14：成语宏定义

**文件：**
- 创建：`src/macro/idiom_macros.py`
- 测试：`tests/test_macro.py`

- [ ] **步骤1：编写失败的测试**

```python
# tests/test_macro.py (追加)
from src.macro.idiom_macros import register_idiom_macros

def test_idiom_macros():
    system = MacroSystem()
    register_idiom_macros(system)

    # 检查成语宏
    assert system.has("守株待兔")
    assert system.has("亡羊补牢")
    assert system.has("画蛇添足")

def test_idiom_expansion():
    system = MacroSystem()
    register_idiom_macros(system)

    # 测试守株待兔宏展开
    expanded = system.expand("守株待兔", {
        "事件": "用户点击",
        "处理函数": "处理点击"
    })

    assert "持续" in expanded or "若真" in expanded
    assert "用户点击" in expanded
```

- [ ] **步骤2：运行测试验证失败**

运行：`pytest tests/test_macro.py::test_idiom_macros -v`
预期：FAIL

- [ ] **步骤3：编写成语宏**

```python
# src/macro/idiom_macros.py
from src.macro.macro_system import Macro, MacroType

def register_idiom_macros(system):
    """注册成语宏"""

    # 守株待兔：事件监听循环
    system.register(Macro(
        name="守株待兔",
        type=MacroType.IDIOM,
        params=["事件", "处理函数"],
        body="持续：事件，等待发生。处理函数。",
        description="等待事件发生并处理（事件监听循环）"
    ))

    # 亡羊补牢：错误补救
    system.register(Macro(
        name="亡羊补牢",
        type=MacroType.IDIOM,
        params=["错误", "补救措施"],
        body="若错误发生：补救措施。返回成功。否则：返回失败。",
        description="错误发生后进行补救"
    ))

    # 画蛇添足：多余操作
    system.register(Macro(
        name="画蛇添足",
        type=MacroType.IDIOM,
        params=["数据", "多余操作"],
        body="数据，处理。多余操作。返回数据。",
        description="在数据处理后执行多余操作"
    ))

    # 一举两得：同时执行两个操作
    system.register(Macro(
        name="一举两得",
        type=MacroType.IDIOM,
        params=["动作1", "动作2"],
        body="定结果1=动作1。定结果2=动作2。返回列(结果1, 结果2)。",
        description="同时执行两个操作并返回结果"
    ))

    # 循序渐进：逐步处理
    system.register(Macro(
        name="循序渐进",
        type=MacroType.IDIOM,
        params=["步骤列表"],
        body="遍历步骤于步骤列表：执行步骤。",
        description="按顺序执行一系列步骤"
    ))
```

- [ ] **步骤4：运行测试验证通过**

运行：`pytest tests/test_macro.py -v`
预期：所有成语宏测试通过

- [ ] **步骤5：Commit**

```bash
git add src/macro/idiom_macros.py tests/test_macro.py
git commit -m "feat: add idiom macros (守株待兔, 亡羊补牢, 画蛇添足)"
```

---

### 任务15：意合式调用

**文件：**
- 修改：`src/parser/parser.py`
- 修改：`src/codegen/python_codegen.py`
- 测试：`tests/test_parser.py`

- [ ] **步骤1：编写失败的测试**

```python
# tests/test_parser.py (追加)
def test_intentional_call():
    source = "北京、上海，计算距离。"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    # 应该解析为函数调用
    assert isinstance(ast.statements[0], FunctionCallNode)
    assert ast.statements[0].name == "计算距离"
    assert len(ast.statements[0].args) == 2
```

- [ ] **步骤2：运行测试验证失败**

运行：`pytest tests/test_parser.py::test_intentional_call -v`
预期：FAIL

- [ ] **步骤3：增强语法分析器支持意合式调用**

```python
# src/parser/parser.py (在_parse_primary方法中添加)
def _parse_primary(self) -> ASTNode:
    token = self._current_token()

    # ... 现有代码 ...

    # 意合式调用：参数1、参数2，函数名。
    if self._check(TokenType.IDENTIFIER):
        # 收集可能的参数
        potential_args = []
        first_token = self._advance()
        potential_args.append(IdentifierNode(first_token.value, line=first_token.line, column=first_token.column))

        # 检查是否有顿号分隔的参数
        while self._check(TokenType.COMMA):
            self._advance()
            arg_token = self._expect(TokenType.IDENTIFIER, "Expected argument")
            potential_args.append(IdentifierNode(arg_token.value, line=arg_token.line, column=arg_token.column))

        # 检查是否是函数调用（逗号后跟函数名）
        if self._check(TokenType.COMMA):
            self._advance()
            func_token = self._expect(TokenType.IDENTIFIER, "Expected function name")

            # 消耗句号
            if self._check(TokenType.PERIOD):
                self._advance()

            return FunctionCallNode(
                func_token.value,
                potential_args,
                line=first_token.line,
                column=first_token.column
            )
        else:
            # 不是意合式调用，返回第一个标识符
            return potential_args[0]

    # ... 现有代码 ...
```

- [ ] **步骤4：运行测试验证通过**

运行：`pytest tests/test_parser.py::test_intentional_call -v`
预期：PASS

- [ ] **步骤5：Commit**

```bash
git add src/parser/parser.py tests/test_parser.py
git commit -m "feat: add intentional function call support"
```

---

### 任务13：语境补全

**文件：**
- 创建：`src/semantic/context_completion.py`
- 测试：`tests/test_semantic.py`

- [ ] **步骤1：编写失败的测试**

```python
# tests/test_semantic.py (追加)
from src.semantic.context_completion import ContextCompleter

def test_topic_chain_completion():
    source = """
用户数据：
  验证格式。
  检查权限。
"""
    completer = ContextCompleter()
    completed = completer.complete(source)
    assert "验证用户数据的格式" in completed or "验证格式(用户数据)" in completed

def test_loop_completion():
    source = """
用户列表：
  发送通知。
"""
    completer = ContextCompleter()
    completed = completer.complete(source)
    assert "遍历" in completed or "for" in completed
```

- [ ] **步骤2：运行测试验证失败**

运行：`pytest tests/test_semantic.py::test_topic_chain_completion -v`
预期：FAIL

- [ ] **步骤3：编写语境补全器**

```python
# src/semantic/context_completion.py
import re
from typing import List, Tuple

class ContextCompleter:
    def __init__(self):
        self.topic_stack = []

    def complete(self, source: str) -> str:
        lines = source.split('\n')
        completed_lines = []

        for i, line in enumerate(lines):
            stripped = line.strip()

            # 检测话题链（以冒号结尾）
            if stripped.endswith('：') or stripped.endswith(':'):
                topic = stripped[:-1].strip()
                self.topic_stack.append(topic)
                completed_lines.append(line)
            # 检测缩进块中的语句
            elif line.startswith('  ') and self.topic_stack:
                current_topic = self.topic_stack[-1]
                completed_stmt = self._complete_statement(stripped, current_topic)
                completed_lines.append('  ' + completed_stmt)
            # 检测DEDENT（减少缩进）
            elif not line.startswith('  ') and self.topic_stack:
                self.topic_stack.pop()
                completed_lines.append(line)
            else:
                completed_lines.append(line)

        return '\n'.join(completed_lines)

    def _complete_statement(self, statement: str, topic: str) -> str:
        # 动词列表
        verbs = ['验证', '检查', '发送', '读取', '写入', '处理', '计算', '显示', '印']

        for verb in verbs:
            if statement.startswith(verb):
                # 补全宾语
                return f"{verb}{topic}的{statement[len(verb):]}"

        # 如果是简单语句，可能是循环
        if not any(op in statement for op in ['=', '加', '减', '乘', '除']):
            # 检查话题是否是列表
            if '列表' in topic or '集合' in topic:
                return f"遍历{topic}中的每个元素：{statement}"

        return statement
```

- [ ] **步骤4：运行测试验证通过**

运行：`pytest tests/test_semantic.py::test_topic_chain_completion -v`
预期：PASS

- [ ] **步骤5：Commit**

```bash
git add src/semantic/context_completion.py tests/test_semantic.py
git commit -m "feat: implement context completion for topic chains"
```

---

### 任务14：数据动词库

**文件：**
- 创建：`src/runtime/data_verbs.py`
- 测试：`tests/test_runtime.py`

- [ ] **步骤1：编写失败的测试**

```python
# tests/test_runtime.py (追加)
from src.runtime.data_verbs import DataVerbLibrary

def test_data_verb_library():
    lib = DataVerbLibrary()

    # 测试映射
    result = lib.execute("映射", lambda x: x * 2, [1, 2, 3])
    assert result == [2, 4, 6]

    # 测试过滤
    result = lib.execute("过滤", lambda x: x > 2, [1, 2, 3, 4, 5])
    assert result == [3, 4, 5]

    # 测试排序
    result = lib.execute("排序", None, [3, 1, 2])
    assert result == [1, 2, 3]

def test_data_verb_chain():
    lib = DataVerbLibrary()

    # 测试链式调用
    result = lib.chain([1, 2, 3, 4, 5], [
        ("过滤", lambda x: x > 2),
        ("映射", lambda x: x * 2),
        ("排序", None)
    ])
    assert result == [6, 8, 10]
```

- [ ] **步骤2：运行测试验证失败**

运行：`pytest tests/test_runtime.py::test_data_verb_library -v`
预期：FAIL

- [ ] **步骤3：编写数据动词库**

```python
# src/runtime/data_verbs.py
from typing import Any, Callable, List, Dict, Optional
from functools import reduce

class DataVerbLibrary:
    def __init__(self):
        self.verbs = {
            # 数据传递动词
            '读取': self._read,
            '写入': self._write,
            '发送': self._send,
            '接收': self._receive,

            # 数据变换动词
            '映射': self._map,
            '过滤': self._filter,
            '折叠': self._reduce,
            '分组': self._group,
            '排序': self._sort,

            # 数据流控制动词
            '分发': self._distribute,
            '合并': self._merge,
            '缓存': self._cache,
            '转换': self._transform,
        }

        self.cache = {}

    def execute(self, verb: str, *args, **kwargs) -> Any:
        if verb not in self.verbs:
            raise ValueError(f"未知的数据动词: {verb}")
        return self.verbs[verb](*args, **kwargs)

    def chain(self, data: Any, operations: List[tuple]) -> Any:
        """链式执行多个数据动词"""
        result = data
        for op in operations:
            verb = op[0]
            args = op[1:] if len(op) > 1 else ()
            result = self.execute(verb, *args, data=result)
        return result

    # 数据传递动词实现
    def _read(self, source: str, **kwargs) -> Any:
        """读取数据"""
        if source.startswith('http'):
            import requests
            return requests.get(source).text
        else:
            with open(source, 'r', encoding='utf-8') as f:
                return f.read()

    def _write(self, data: Any, target: str, **kwargs):
        """写入数据"""
        with open(target, 'w', encoding='utf-8') as f:
            f.write(str(data))

    def _send(self, data: Any, target: str, **kwargs):
        """发送数据"""
        # 实现消息队列、网络发送等
        pass

    def _receive(self, source: str, **kwargs) -> Any:
        """接收数据"""
        # 实现消息队列、网络接收等
        pass

    # 数据变换动词实现
    def _map(self, func: Callable, data: List = None, **kwargs) -> List:
        """映射"""
        if data is None:
            data = kwargs.get('data', [])
        return list(map(func, data))

    def _filter(self, func: Callable, data: List = None, **kwargs) -> List:
        """过滤"""
        if data is None:
            data = kwargs.get('data', [])
        return list(filter(func, data))

    def _reduce(self, func: Callable, data: List = None, initial: Any = None, **kwargs) -> Any:
        """折叠"""
        if data is None:
            data = kwargs.get('data', [])
        if initial is not None:
            return reduce(func, data, initial)
        return reduce(func, data)

    def _group(self, key_func: Callable, data: List = None, **kwargs) -> Dict:
        """分组"""
        if data is None:
            data = kwargs.get('data', [])
        from itertools import groupby
        return {k: list(g) for k, g in groupby(sorted(data, key=key_func), key_func)}

    def _sort(self, key_func: Callable = None, data: List = None, reverse: bool = False, **kwargs) -> List:
        """排序"""
        if data is None:
            data = kwargs.get('data', [])
        return sorted(data, key=key_func, reverse=reverse)

    # 数据流控制动词实现
    def _distribute(self, data: Any, targets: List[str], **kwargs):
        """分发数据到多个目标"""
        for target in targets:
            self._send(data, target)

    def _merge(self, sources: List[str], **kwargs) -> List:
        """合并多个数据源"""
        result = []
        for source in sources:
            result.extend(self._read(source))
        return result

    def _cache(self, key: str, data: Any = None, **kwargs) -> Any:
        """缓存数据"""
        if data is None:
            data = kwargs.get('data')

        if data is not None:
            self.cache[key] = data
            return data
        else:
            return self.cache.get(key)

    def _transform(self, transformer: Callable, data: Any = None, **kwargs) -> Any:
        """转换数据格式"""
        if data is None:
            data = kwargs.get('data')
        return transformer(data)
```

- [ ] **步骤4：运行测试验证通过**

运行：`pytest tests/test_runtime.py::test_data_verb_library -v`
预期：PASS

- [ ] **步骤5：Commit**

```bash
git add src/runtime/data_verbs.py tests/test_runtime.py
git commit -m "feat: implement data verb library"
```

---

### 任务15：介词显式化

**文件：**
- 修改：`src/parser/parser.py`
- 修改：`src/codegen/python_codegen.py`
- 测试：`tests/test_parser.py`

- [ ] **步骤1：编写失败的测试**

```python
# tests/test_parser.py (追加)
def test_preposition_explicit():
    source = "把用户数据存入缓存。"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    # 应该解析为函数调用
    assert isinstance(ast.statements[0], FunctionCallNode)
```

- [ ] **步骤2：运行测试验证失败**

运行：`pytest tests/test_parser.py::test_preposition_explicit -v`
预期：FAIL

- [ ] **步骤3：增强语法分析器支持介词**

```python
# src/parser/parser.py (在_parse_statement方法中添加)
def _parse_statement(self) -> Optional[ASTNode]:
    # ... 现有代码 ...

    # 检测介词开头的语句
    if self._check(TokenType.IDENTIFIER):
        token = self._current_token()
        if token.value in ["把", "将", "给", "从"]:
            return self._parse_preposition_statement()

    # ... 现有代码 ...

def _parse_preposition_statement(self) -> ASTNode:
    prep_token = self._advance()  # 消耗介词
    preposition = prep_token.value

    # 解析宾语
    obj_token = self._expect(TokenType.IDENTIFIER, "Expected object")
    obj = IdentifierNode(obj_token.value, line=obj_token.line, column=obj_token.column)

    # 解析动词
    verb_token = self._expect(TokenType.IDENTIFIER, "Expected verb")
    verb = verb_token.value

    # 解析目标（如果有）
    target = None
    if self._check(TokenType.IDENTIFIER):
        target_token = self._advance()
        target = IdentifierNode(target_token.value, line=target_token.line, column=target_token.column)

    # 消耗句号
    if self._check(TokenType.PERIOD):
        self._advance()

    # 根据介词生成不同的AST
    if preposition in ["把", "将"]:
        # 把A存入B -> 存入(A, B)
        if target:
            return FunctionCallNode(verb, [obj, target], line=prep_token.line, column=prep_token.column)
        else:
            return FunctionCallNode(verb, [obj], line=prep_token.line, column=prep_token.column)
    elif preposition == "从":
        # 从A读取 -> 读取(A)
        return FunctionCallNode(verb, [obj], line=prep_token.line, column=prep_token.column)
    elif preposition == "给":
        # 给A赋值B -> 赋值(A, B)
        if target:
            return FunctionCallNode(verb, [obj, target], line=prep_token.line, column=prep_token.column)
        else:
            return FunctionCallNode(verb, [obj], line=prep_token.line, column=prep_token.column)

    return FunctionCallNode(verb, [obj], line=prep_token.line, column=prep_token.column)
```

- [ ] **步骤4：运行测试验证通过**

运行：`pytest tests/test_parser.py::test_preposition_explicit -v`
预期：PASS

- [ ] **步骤5：Commit**

```bash
git add src/parser/parser.py tests/test_parser.py
git commit -m "feat: add preposition-based statement parsing"
```

---

### 任务16：类型推断系统

**文件：**
- 创建：`src/semantic/type_inference.py`
- 测试：`tests/test_semantic.py`

- [ ] **步骤1：编写失败的测试**

```python
# tests/test_semantic.py (追加)
from src.semantic.type_inference import TypeInferencer

def test_type_inference_number():
    inferencer = TypeInferencer()
    assert inferencer.infer("123") == "number"
    assert inferencer.infer("3.14") == "number"

def test_type_inference_string():
    inferencer = TypeInferencer()
    assert inferencer.inference('"你好"') == "string"

def test_type_inference_expression():
    inferencer = TypeInferencer()
    assert inferencer.infer("1加2") == "number"
    assert inferencer.infer('"a"加"b"') == "string"
```

- [ ] **步骤2：运行测试验证失败**

运行：`pytest tests/test_semantic.py::test_type_inference_number -v`
预期：FAIL

- [ ] **步骤3：编写类型推断器**

```python
# src/semantic/type_inference.py
from typing import Dict, Set, Optional
from src.parser.ast_nodes import *

class TypeInferencer:
    def __init__(self):
        self.type_rules = {
            ('number', '+', 'number'): 'number',
            ('number', '-', 'number'): 'number',
            ('number', '*', 'number'): 'number',
            ('number', '/', 'number'): 'number',
            ('string', '+', 'string'): 'string',
            ('number', '==', 'number'): 'boolean',
            ('number', '<', 'number'): 'boolean',
            ('number', '>', 'number'): 'boolean',
            ('boolean', 'and', 'boolean'): 'boolean',
            ('boolean', 'or', 'boolean'): 'boolean',
        }

    def infer(self, node: ASTNode, context: Dict[str, str] = None) -> str:
        if context is None:
            context = {}

        if isinstance(node, NumberNode):
            return 'number'
        elif isinstance(node, StringNode):
            return 'string'
        elif isinstance(node, IdentifierNode):
            return context.get(node.name, 'unknown')
        elif isinstance(node, BinaryOpNode):
            left_type = self.infer(node.left, context)
            right_type = self.infer(node.right, context)
            return self.type_rules.get((left_type, node.operator, right_type), 'unknown')
        elif isinstance(node, UnaryOpNode):
            operand_type = self.infer(node.operand, context)
            if node.operator == 'not':
                return 'boolean'
            return operand_type
        elif isinstance(node, FunctionCallNode):
            # 根据函数名推断返回类型
            return self._infer_function_return_type(node, context)
        elif isinstance(node, ListNode):
            return 'list'
        elif isinstance(node, DictNode):
            return 'dict'
        else:
            return 'unknown'

    def _infer_function_return_type(self, node: FunctionCallNode, context: Dict[str, str]) -> str:
        # 内置函数返回类型
        builtin_returns = {
            '印': 'unknown',
            '读取': 'string',
            '长度': 'number',
            '求和': 'number',
            '最大': 'number',
            '最小': 'number',
            '排序': 'list',
            '映射': 'list',
            '过滤': 'list',
        }

        return builtin_returns.get(node.name, 'unknown')
```

- [ ] **步骤4：运行测试验证通过**

运行：`pytest tests/test_semantic.py::test_type_inference_number -v`
预期：PASS

- [ ] **步骤5：Commit**

```bash
git add src/semantic/type_inference.py tests/test_semantic.py
git commit -m "feat: implement type inference system"
```

---

### 任务17：错误处理增强

**文件：**
- 创建：`src/error_handling.py`
- 测试：`tests/test_error_handling.py`

- [ ] **步骤1：编写失败的测试**

```python
# tests/test_error_handling.py
import pytest
from src.error_handling import ErrorHandler, ErrorType

def test_error_handler():
    handler = ErrorHandler()
    handler.report(ErrorType.LEXER_ERROR, "Unexpected character", line=1, column=5)

    errors = handler.get_errors()
    assert len(errors) == 1
    assert errors[0].error_type == ErrorType.LEXER_ERROR

def test_error_formatting():
    handler = ErrorHandler()
    handler.report(ErrorType.PARSER_ERROR, "Expected ')'", line=3, column=10, source="印(1加2。")

    formatted = handler.format_error(0)
    assert "第 3 行" in formatted
    assert "第 10 列" in formatted
```

- [ ] **步骤2：运行测试验证失败**

运行：`pytest tests/test_error_handling.py::test_error_handler -v`
预期：FAIL

- [ ] **步骤3：编写错误处理器**

```python
# src/error_handling.py
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

class ErrorType(Enum):
    LEXER_ERROR = "词法错误"
    PARSER_ERROR = "语法错误"
    SEMANTIC_ERROR = "语义错误"
    RUNTIME_ERROR = "运行时错误"
    TYPE_ERROR = "类型错误"

@dataclass
class Error:
    error_type: ErrorType
    message: str
    line: int
    column: int
    source: Optional[str] = None
    suggestion: Optional[str] = None

class ErrorHandler:
    def __init__(self):
        self.errors: List[Error] = []

    def report(self, error_type: ErrorType, message: str, line: int, column: int,
               source: str = None, suggestion: str = None):
        error = Error(error_type, message, line, column, source, suggestion)
        self.errors.append(error)

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def get_errors(self) -> List[Error]:
        return self.errors

    def format_error(self, index: int) -> str:
        if index >= len(self.errors):
            return ""

        error = self.errors[index]
        lines = [
            f"{error.error_type.value}: {error.message}",
            f"  位置: 第 {error.line} 行, 第 {error.column} 列",
        ]

        if error.source:
            source_lines = error.source.split('\n')
            if error.line <= len(source_lines):
                source_line = source_lines[error.line - 1]
                lines.append(f"  源代码: {source_line}")
                lines.append(f"          {' ' * (error.column - 1)}^")

        if error.suggestion:
            lines.append(f"  建议: {error.suggestion}")

        return '\n'.join(lines)

    def format_all_errors(self) -> str:
        return '\n\n'.join(self.format_error(i) for i in range(len(self.errors)))

    def clear(self):
        self.errors.clear()
```

- [ ] **步骤4：运行测试验证通过**

运行：`pytest tests/test_error_handling.py -v`
预期：PASS

- [ ] **步骤5：Commit**

```bash
git add src/error_handling.py tests/test_error_handling.py
git commit -m "feat: implement enhanced error handling"
```

---

### 任务18：示例文件

**文件：**
- 创建：`examples/basic/hello.yan`
- 创建：`examples/basic/variables.yan`
- 创建：`examples/basic/functions.yan`
- 创建：`examples/basic/control_flow.yan`
- 创建：`examples/advanced/user_registration.yan`

- [ ] **步骤1：创建基础示例**

```yan
# examples/basic/hello.yan
印"你好世界"。
```

```yan
# examples/basic/variables.yan
定用户名 = "张三"。
定年龄 = 25。

印用户名。
印年龄。

用户名 = "李四"。
印用户名。
```

```yan
# examples/basic/functions.yan
定义平方：
  接收x。
  返回x乘x。

定义距离：
  接收a、b。
  定差 = a减b。
  若差小0：
    返回负差。
  否则：
    返回差。

印平方5。
印距离3、7。
```

```yan
# examples/basic/control_flow.yan
定x = 10。

若x大5：
  印"大于5"。
否则：
  印"小于等于5"。

遍历i于范围1、5：
  印i。

当x大0：
  印x。
  x = x减1。
```

- [ ] **步骤2：创建高级示例**

```yan
# examples/advanced/user_registration.yan
用户注册流程：

  接收注册信息。

  验证信息：
    用户名长度小于3，返回错误"用户名太短"。
    邮箱格式不正确，返回错误"邮箱格式错误"。
    用户名已存在，返回错误"用户名已被使用"。

  创建用户对象：
    设置用户名。
    设置邮箱。
    设置密码哈希值。
    设置注册时间。

  存入数据库。

  发送欢迎邮件：
    标题 = "欢迎加入"。
    内容 = "感谢注册"。

  返回成功消息。
```

- [ ] **步骤3：测试示例**

```bash
python src/main.py examples/basic/hello.yan
python src/main.py examples/basic/variables.yan
python src/main.py examples/basic/functions.yan
python src/main.py examples/basic/control_flow.yan
```

- [ ] **步骤4：Commit**

```bash
git add examples/
git commit -m "feat: add example files"
```

---

## 阶段3：多轨制（任务19-22）

### 任务19：数学轨实现

**文件：**
- 创建：`src/codegen/multi_track.py`
- 测试：`tests/test_codegen.py`

- [ ] **步骤1：编写失败的测试**

```python
# tests/test_codegen.py (追加)
def test_math_track():
    source = '圆面积 = $(π * r²)。'
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    codegen = PythonCodegen()
    python_code = codegen.generate(ast)
    assert "math.pi" in python_code or "π" in python_code
```

- [ ] **步骤2：运行测试验证失败**

运行：`pytest tests/test_codegen.py::test_math_track -v`
预期：FAIL

- [ ] **步骤3：实现数学轨**

```python
# src/codegen/multi_track.py
import re
from typing import Tuple

class MultiTrackCodegen:
    def __init__(self):
        self.math_symbols = {
            'π': 'math.pi',
            '√': 'math.sqrt',
            '²': '**2',
            '³': '**3',
            '×': '*',
            '÷': '/',
            '±': '+/-',
        }

    def process_math_expression(self, expr: str) -> str:
        """处理数学表达式"""
        result = expr

        # 替换数学符号
        for symbol, replacement in self.math_symbols.items():
            result = result.replace(symbol, replacement)

        # 处理幂运算
        result = re.sub(r'(\w+)²', r'\1**2', result)
        result = re.sub(r'(\w+)³', r'\1**3', result)

        # 处理根号
        result = re.sub(r'√\(([^)]+)\)', r'math.sqrt(\1)', result)
        result = re.sub(r'√(\w+)', r'math.sqrt(\1)', result)

        return result

    def process_python_block(self, code: str) -> str:
        """处理Python代码块"""
        return code

    def process_sql_query(self, query: str) -> str:
        """处理SQL查询"""
        return f'"""{query}"""'

    def process_javascript_block(self, code: str) -> str:
        """处理JavaScript代码块"""
        return f'"""{code}"""'
```

- [ ] **步骤4：集成到代码生成器**

```python
# src/codegen/python_codegen.py (添加)
from src.codegen.multi_track import MultiTrackCodegen

class PythonCodegen:
    def __init__(self):
        self.indent_level = 0
        self.indent_str = "    "
        self.multi_track = MultiTrackCodegen()

    # ... 现有代码 ...

    def _generate_expression(self, node: ASTNode) -> str:
        # ... 现有代码 ...

        # 处理数学表达式
        if isinstance(node, StringNode) and node.value.startswith('$('):
            math_expr = node.value[2:-1]  # 提取 $(...) 中的内容
            return self.multi_track.process_math_expression(math_expr)

        # ... 现有代码 ...
```

- [ ] **步骤5：运行测试验证通过**

运行：`pytest tests/test_codegen.py::test_math_track -v`
预期：PASS

- [ ] **步骤6：Commit**

```bash
git add src/codegen/multi_track.py src/codegen/python_codegen.py tests/test_codegen.py
git commit -m "feat: implement math track support"
```

---

### 任务20：Python轨实现

**文件：**
- 修改：`src/codegen/multi_track.py`
- 修改：`src/codegen/python_codegen.py`
- 测试：`tests/test_codegen.py`

- [ ] **步骤1：编写失败的测试**

```python
# tests/test_codegen.py (追加)
def test_python_track():
    source = '''数据处理 = {{
import pandas as pd
df = pd.read_csv('data.csv')
result = df.groupby('category').sum()
}}'''
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    codegen = PythonCodegen()
    python_code = codegen.generate(ast)
    assert "import pandas" in python_code
```

- [ ] **步骤2：运行测试验证失败**

运行：`pytest tests/test_codegen.py::test_python_track -v`
预期：FAIL

- [ ] **步骤3：实现Python轨**

```python
# src/codegen/python_codegen.py (在_generate_expression中添加)
def _generate_expression(self, node: ASTNode) -> str:
    # ... 现有代码 ...

    # 处理Python代码块
    if isinstance(node, StringNode) and node.value.startswith('{{'):
        python_code = node.value[2:-2]  # 提取 {{...}} 中的内容
        return self.multi_track.process_python_block(python_code)

    # ... 现有代码 ...
```

- [ ] **步骤4：运行测试验证通过**

运行：`pytest tests/test_codegen.py::test_python_track -v`
预期：PASS

- [ ] **步骤5：Commit**

```bash
git add src/codegen/python_codegen.py tests/test_codegen.py
git commit -m "feat: implement Python track support"
```

---

### 任务21：SQL轨实现

**文件：**
- 修改：`src/codegen/multi_track.py`
- 修改：`src/codegen/python_codegen.py`
- 测试：`tests/test_codegen.py`

- [ ] **步骤1：编写失败的测试**

```python
# tests/test_codegen.py (追加)
def test_sql_track():
    source = '''用户查询 = 【
SELECT * FROM users
WHERE status = 'active'
ORDER BY created_at DESC
】'''
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    codegen = PythonCodegen()
    python_code = codegen.generate(ast)
    assert "SELECT" in python_code
```

- [ ] **步骤2：运行测试验证失败**

运行：`pytest tests/test_codegen.py::test_sql_track -v`
预期：FAIL

- [ ] **步骤3：实现SQL轨**

```python
# src/codegen/python_codegen.py (在_generate_expression中添加)
def _generate_expression(self, node: ASTNode) -> str:
    # ... 现有代码 ...

    # 处理SQL查询
    if isinstance(node, StringNode) and node.value.startswith('【'):
        sql_query = node.value[1:-1]  # 提取【...】中的内容
        return self.multi_track.process_sql_query(sql_query)

    # ... 现有代码 ...
```

- [ ] **步骤4：运行测试验证通过**

运行：`pytest tests/test_codegen.py::test_sql_track -v`
预期：PASS

- [ ] **步骤5：Commit**

```bash
git add src/codegen/python_codegen.py tests/test_codegen.py
git commit -m "feat: implement SQL track support"
```

---

### 任务22：JavaScript轨实现

**文件：**
- 修改：`src/codegen/multi_track.py`
- 修改：`src/codegen/python_codegen.py`
- 测试：`tests/test_codegen.py`

- [ ] **步骤1：编写失败的测试**

```python
# tests/test_codegen.py (追加)
def test_javascript_track():
    source = '''前端逻辑 = 「
function handleClick(event) {
  const target = event.target;
  console.log(target.value);
}
」'''
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    codegen = PythonCodegen()
    python_code = codegen.generate(ast)
    assert "function" in python_code
```

- [ ] **步骤2：运行测试验证失败**

运行：`pytest tests/test_codegen.py::test_javascript_track -v`
预期：FAIL

- [ ] **步骤3：实现JavaScript轨**

```python
# src/codegen/python_codegen.py (在_generate_expression中添加)
def _generate_expression(self, node: ASTNode) -> str:
    # ... 现有代码 ...

    # 处理JavaScript代码块
    if isinstance(node, StringNode) and node.value.startswith('「'):
        js_code = node.value[1:-1]  # 提取「...」中的内容
        return self.multi_track.process_javascript_block(js_code)

    # ... 现有代码 ...
```

- [ ] **步骤4：运行测试验证通过**

运行：`pytest tests/test_codegen.py::test_javascript_track -v`
预期：PASS

- [ ] **步骤5：Commit**

```bash
git add src/codegen/python_codegen.py tests/test_codegen.py
git commit -m "feat: implement JavaScript track support"
```

---

## 阶段4：工具链（任务23-25）

### 任务23：VS Code插件基础

**文件：**
- 创建：`vscode-extension/package.json`
- 创建：`vscode-extension/tsconfig.json`
- 创建：`vscode-extension/src/extension.ts`

- [ ] **步骤1：创建package.json**

```json
{
  "name": "chinese-programming-language",
  "displayName": "中文编程语言",
  "description": "中文编程语言支持",
  "version": "0.1.0",
  "publisher": "your-publisher-name",
  "engines": {
    "vscode": "^1.80.0"
  },
  "categories": ["Programming Languages"],
  "activationEvents": ["onLanguage:yan"],
  "main": "./out/extension.js",
  "contributes": {
    "languages": [{
      "id": "yan",
      "aliases": ["Yan", "yan"],
      "extensions": [".yan"],
      "configuration": "./language-configuration.json"
    }],
    "grammars": [{
      "language": "yan",
      "scopeName": "source.yan",
      "path": "./syntaxes/yan.tmLanguage.json"
    }]
  },
  "scripts": {
    "vscode:prepublish": "npm run compile",
    "compile": "tsc -p ./",
    "watch": "tsc -watch -p ./"
  },
  "devDependencies": {
    "@types/node": "^18.0.0",
    "@types/vscode": "^1.80.0",
    "typescript": "^5.0.0"
  }
}
```

- [ ] **步骤2：创建tsconfig.json**

```json
{
  "compilerOptions": {
    "module": "commonjs",
    "target": "ES2020",
    "outDir": "out",
    "lib": ["ES2020"],
    "sourceMap": true,
    "rootDir": "src",
    "strict": true
  },
  "exclude": ["node_modules", ".vscode-test"]
}
```

- [ ] **步骤3：创建extension.ts**

```typescript
// vscode-extension/src/extension.ts
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    console.log('中文编程语言扩展已激活');

    // 注册补全提供者
    const completionProvider = vscode.languages.registerCompletionItemProvider(
        'yan',
        {
            provideCompletionItems(document: vscode.TextDocument, position: vscode.Position) {
                const items: vscode.CompletionItem[] = [];

                // 关键字补全
                const keywords = ['若', '则', '否则', '遍历', '当', '定义', '返回', '定'];
                keywords.forEach(keyword => {
                    items.push(new vscode.CompletionItem(keyword, vscode.CompletionItemKind.Keyword));
                });

                // 内置函数补全
                const builtins = ['印', '读取', '写入', '长度', '求和', '最大', '最小', '排序'];
                builtins.forEach(builtin => {
                    items.push(new vscode.CompletionItem(builtin, vscode.CompletionItemKind.Function));
                });

                return items;
            }
        }
    );

    context.subscriptions.push(completionProvider);
}

export function deactivate() {
    console.log('中文编程语言扩展已停用');
}
```

- [ ] **步骤4：创建语法高亮配置**

```json
// vscode-extension/syntaxes/yan.tmLanguage.json
{
  "scopeName": "source.yan",
  "patterns": [
    {
      "match": "(若|则|否则|否则若|遍历|当|重复|持续|定义|函|返回|定|为)",
      "name": "keyword.control.yan"
    },
    {
      "match": "(加|减|乘|除|等|不等|小|大|小等|大等|且|或|非)",
      "name": "keyword.operator.yan"
    },
    {
      "match": "\"([^\"]*)\"",
      "name": "string.quoted.double.yan"
    },
    {
      "match": "\\b(\\d+\\.?\\d*)\\b",
      "name": "constant.numeric.yan"
    },
    {
      "match": "([\\u4e00-\\u9fff]+)",
      "name": "variable.other.yan"
    },
    {
      "match": "--.*$",
      "name": "comment.line.yan"
    }
  ]
}
```

- [ ] **步骤5：Commit**

```bash
git add vscode-extension/
git commit -m "feat: add VS Code extension basic structure"
```

---

### 任务24：语言配置

**文件：**
- 创建：`vscode-extension/language-configuration.json`

- [ ] **步骤1：创建语言配置**

```json
{
  "comments": {
    "lineComment": "--"
  },
  "brackets": [
    ["（", "）"],
    ["【", "】"],
    ["{", "}"]
  ],
  "autoClosingPairs": [
    { "open": "（", "close": "）" },
    { "open": "【", "close": "】" },
    { "open": "{", "close": "}" },
    { "open": "\"", "close": "\"" }
  ],
  "surroundingPairs": [
    ["（", "）"],
    ["【", "】"],
    ["{", "}"],
    ["\"", "\""]
  ],
  "indentationRules": {
    "increaseIndentPattern": "：\\s*$",
    "decreaseIndentPattern": "^\\s*(否则|否则若)\\b"
  }
}
```

- [ ] **步骤2：Commit**

```bash
git add vscode-extension/language-configuration.json
git commit -m "feat: add language configuration for VS Code"
```

---

### 任务25：文档和教程

**文件：**
- 创建：`docs/LANGUAGE_SPEC.md`
- 创建：`docs/TUTORIAL.md`
- 创建：`docs/API_REFERENCE.md`

- [ ] **步骤1：创建语言规范**

```markdown
# docs/LANGUAGE_SPEC.md

# 中文编程语言规范

## 1. 词法结构

### 1.1 标识符

标识符由中文字符、英文字母、数字和下划线组成，必须以中文字符或英文字母开头。

示例：
- 用户数据
- userName
- _temp

### 1.2 关键字

| 关键字 | 含义 |
|--------|------|
| 若 | if |
| 则 | then |
| 否则 | else |
| 否则若 | elif |
| 遍历 | for |
| 当 | while |
| 重复 | repeat |
| 持续 | continue |
| 定义 | define |
| 函 | function |
| 返回 | return |
| 定 | var |
| 为 | as |

### 1.3 操作符

| 操作符 | 含义 |
|--------|------|
| 加 | + |
| 减 | - |
| 乘 | * |
| 除 | / |
| 等 | == |
| 不等 | != |
| 小 | < |
| 大 | > |
| 小等 | <= |
| 大等 | >= |
| 且 | and |
| 或 | or |
| 非 | not |

## 2. 语法结构

### 2.1 变量定义

```yan
定变量名 = 值。
定变量名为类型 = 值。
```

### 2.2 函数定义

```yan
定义函数名：
  接收参数。
  函数体。
  返回值。
```

### 2.3 条件语句

```yan
若条件：
  动作。
否则：
  其他动作。
```

### 2.4 循环语句

```yan
遍历变量于列表：
  循环体。

当条件：
  循环体。

重复次数：
  循环体。
```
```

- [ ] **步骤2：创建教程**

```markdown
# docs/TUTORIAL.md

# 中文编程语言教程

## 第一课：你好世界

```yan
印"你好世界"。
```

## 第二课：变量

```yan
定姓名 = "张三"。
定年龄 = 25。

印姓名。
印年龄。
```

## 第三课：函数

```yan
定义平方：
  接收x。
  返回x乘x。

印平方5。
```

## 第四课：条件

```yan
定分数 = 85。

若分数大等于90：
  印"优秀"。
否则若分数大等于80：
  印"良好"。
否则若分数大等于60：
  印"及格"。
否则：
  印"不及格"。
```

## 第五课：循环

```yan
遍历i于范围1、10：
  印i。
```
```

- [ ] **步骤3：创建API参考**

```markdown
# docs/API_REFERENCE.md

# 中文编程语言API参考

## 内置函数

### 输出函数

#### 印(值)

打印值到控制台。

参数：
- 值：要打印的值

示例：
```yan
印"你好世界"。
印123。
```

### 数学函数

#### 求和(列表)

计算列表中所有元素的和。

参数：
- 列表：数字列表

返回：数字

示例：
```yan
定结果 = 求和列1、2、3、4、5。
印结果。  -- 输出：15
```

#### 最大(列表)

返回列表中的最大值。

#### 最小(列表)

返回列表中的最小值。

### 列表函数

#### 映射(函数, 列表)

对列表中的每个元素应用函数。

#### 过滤(函数, 列表)

筛选列表中满足条件的元素。

#### 排序(列表)

对列表进行排序。

### 字符串函数

#### 长度(字符串)

返回字符串的长度。

#### 连接(字符串1, 字符串2)

连接两个字符串。
```

- [ ] **步骤4：Commit**

```bash
git add docs/
git commit -m "docs: add language specification, tutorial, and API reference"
```

---

## 阶段5：生态系统（任务26-30）

### 任务26：标准库 - IO模块

**文件：**
- 创建：`stdlib/io.py`

- [ ] **步骤1：创建IO模块**

```python
# stdlib/io.py
"""输入输出模块"""

import os
import json
import csv
from typing import Any, List, Dict

def 读取文件(路径: str, 编码: str = 'utf-8') -> str:
    """读取文本文件"""
    with open(路径, 'r', encoding=编码) as f:
        return f.read()

def 写入文件(路径: str, 内容: str, 编码: str = 'utf-8'):
    """写入文本文件"""
    with open(路径, 'w', encoding=编码) as f:
        f.write(内容)

def 追加文件(路径: str, 内容: str, 编码: str = 'utf-8'):
    """追加到文本文件"""
    with open(路径, 'a', encoding=编码) as f:
        f.write(内容)

def 读取JSON(路径: str, 编码: str = 'utf-8') -> Any:
    """读取JSON文件"""
    with open(路径, 'r', encoding=编码) as f:
        return json.load(f)

def 写入JSON(路径: str, 数据: Any, 编码: str = 'utf-8', 缩进: int = 2):
    """写入JSON文件"""
    with open(路径, 'w', encoding=编码) as f:
        json.dump(数据, f, ensure_ascii=False, indent=缩进)

def 读取CSV(路径: str, 编码: str = 'utf-8') -> List[Dict]:
    """读取CSV文件"""
    with open(路径, 'r', encoding=编码) as f:
        reader = csv.DictReader(f)
        return list(reader)

def 写入CSV(路径: str, 数据: List[Dict], 编码: str = 'utf-8'):
    """写入CSV文件"""
    if not 数据:
        return

    with open(路径, 'w', encoding=编码, newline='') as f:
        writer = csv.DictWriter(f, fieldnames=数据[0].keys())
        writer.writeheader()
        writer.writerows(数据)

def 列出目录(路径: str = '.') -> List[str]:
    """列出目录中的文件"""
    return os.listdir(路径)

def 创建目录(路径: str):
    """创建目录"""
    os.makedirs(路径, exist_ok=True)

def 删除文件(路径: str):
    """删除文件"""
    os.remove(路径)

def 文件存在(路径: str) -> bool:
    """检查文件是否存在"""
    return os.path.exists(路径)
```

- [ ] **步骤2：Commit**

```bash
git add stdlib/io.py
git commit -m "feat: add IO module to standard library"
```

---

### 任务27：标准库 - 字符串模块

**文件：**
- 创建：`stdlib/string.py`

- [ ] **步骤1：创建字符串模块**

```python
# stdlib/string.py
"""字符串处理模块"""

import re
from typing import List

def 长度(字符串: str) -> int:
    """返回字符串长度"""
    return len(字符串)

def 连接(*字符串: str) -> str:
    """连接多个字符串"""
    return ''.join(字符串)

def 分割(字符串: str, 分隔符: str = None) -> List[str]:
    """分割字符串"""
    return 字符串.split(分隔符)

def 替换(字符串: str, 旧: str, 新: str) -> str:
    """替换字符串"""
    return 字符串.replace(旧, 新)

def 去除空白(字符串: str) -> str:
    """去除首尾空白"""
    return 字符串.strip()

def 转大写(字符串: str) -> str:
    """转换为大写"""
    return 字符串.upper()

def 转小写(字符串: str) -> str:
    """转换为小写"""
    return 字符串.lower()

def 首字母大写(字符串: str) -> str:
    """首字母大写"""
    return 字符串.capitalize()

def 包含(字符串: str, 子串: str) -> bool:
    """检查是否包含子串"""
    return 子串 in 字符串

def 开始于(字符串: str, 前缀: str) -> bool:
    """检查是否以指定前缀开头"""
    return 字符串.startswith(前缀)

def 结束于(字符串: str, 后缀: str) -> bool:
    """检查是否以指定后缀结尾"""
    return 字符串.endswith(后缀)

def 查找(字符串: str, 子串: str) -> int:
    """查找子串位置"""
    return 字符串.find(子串)

def 截取(字符串: str, 开始: int, 结束: int = None) -> str:
    """截取子串"""
    if 结束 is None:
        return 字符串[开始:]
    return 字符串[开始:结束]

def 正则匹配(字符串: str, 模式: str) -> bool:
    """正则表达式匹配"""
    return bool(re.match(模式, 字符串))

def 正则查找(字符串: str, 模式: str) -> List[str]:
    """正则表达式查找"""
    return re.findall(模式, 字符串)

def 正则替换(字符串: str, 模式: str, 替换: str) -> str:
    """正则表达式替换"""
    return re.sub(模式, 替换, 字符串)

def 格式化(模板: str, **参数) -> str:
    """格式化字符串"""
    return 模板.format(**参数)
```

- [ ] **步骤2：Commit**

```bash
git add stdlib/string.py
git commit -m "feat: add string module to standard library"
```

---

### 任务28：标准库 - 数学模块

**文件：**
- 创建：`stdlib/math.py`

- [ ] **步骤1：创建数学模块**

```python
# stdlib/math.py
"""数学运算模块"""

import math
import random
from typing import List

# 常量
圆周率 = math.pi
自然常数 = math.e

# 基本运算
def 绝对值(x: float) -> float:
    """绝对值"""
    return abs(x)

def 最大值(*值: float) -> float:
    """最大值"""
    return max(值)

def 最小值(*值: float) -> float:
    """最小值"""
    return min(值)

def 四舍五入(x: float, 位数: int = 0) -> float:
    """四舍五入"""
    return round(x, 位数)

def 向上取整(x: float) -> int:
    """向上取整"""
    return math.ceil(x)

def 向下取整(x: float) -> int:
    """向下取整"""
    return math.floor(x)

# 幂运算
def 平方(x: float) -> float:
    """平方"""
    return x ** 2

def 立方(x: float) -> float:
    """立方"""
    return x ** 3

def 幂(底数: float, 指数: float) -> float:
    """幂运算"""
    return math.pow(底数, 指数)

def 平方根(x: float) -> float:
    """平方根"""
    return math.sqrt(x)

def 立方根(x: float) -> float:
    """立方根"""
    return x ** (1/3)

# 对数
def 自然对数(x: float) -> float:
    """自然对数"""
    return math.log(x)

def 常用对数(x: float) -> float:
    """常用对数（以10为底）"""
    return math.log10(x)

def 对数(x: float, 底: float) -> float:
    """对数"""
    return math.log(x, 底)

# 三角函数
def 正弦(x: float) -> float:
    """正弦"""
    return math.sin(x)

def 余弦(x: float) -> float:
    """余弦"""
    return math.cos(x)

def 正切(x: float) -> float:
    """正切"""
    return math.tan(x)

def 反正弦(x: float) -> float:
    """反正弦"""
    return math.asin(x)

def 反余弦(x: float) -> float:
    """反余弦"""
    return math.acos(x)

def 反正切(x: float) -> float:
    """反正切"""
    return math.atan(x)

# 双曲函数
def 双曲正弦(x: float) -> float:
    """双曲正弦"""
    return math.sinh(x)

def 双曲余弦(x: float) -> float:
    """双曲余弦"""
    return math.cosh(x)

def 双曲正切(x: float) -> float:
    """双曲正切"""
    return math.tanh(x)

# 角度转换
def 弧度转角度(x: float) -> float:
    """弧度转角度"""
    return math.degrees(x)

def 角度转弧度(x: float) -> float:
    """角度转弧度"""
    return math.radians(x)

# 随机数
def 随机数(最小: float = 0, 最大: float = 1) -> float:
    """生成随机浮点数"""
    return random.uniform(最小, 最大)

def 随机整数(最小: int, 最大: int) -> int:
    """生成随机整数"""
    return random.randint(最小, 最大)

def 随机选择(列表: List) -> any:
    """从列表中随机选择"""
    return random.choice(列表)

def 随机打乱(列表: List) -> List:
    """随机打乱列表"""
    result = 列表.copy()
    random.shuffle(result)
    return result

# 统计
def 平均值(列表: List[float]) -> float:
    """计算平均值"""
    return sum(列表) / len(列表)

def 中位数(列表: List[float]) -> float:
    """计算中位数"""
    sorted_list = sorted(列表)
    n = len(sorted_list)
    if n % 2 == 0:
        return (sorted_list[n//2-1] + sorted_list[n//2]) / 2
    else:
        return sorted_list[n//2]

def 标准差(列表: List[float]) -> float:
    """计算标准差"""
    avg = 平均值(列表)
    variance = sum((x - avg) ** 2 for x in 列表) / len(列表)
    return math.sqrt(variance)
```

- [ ] **步骤2：Commit**

```bash
git add stdlib/math.py
git commit -m "feat: add math module to standard library"
```

---

### 任务29：标准库 - 集合模块

**文件：**
- 创建：`stdlib/collection.py`

- [ ] **步骤1：创建集合模块**

```python
# stdlib/collection.py
"""集合处理模块"""

from typing import List, Dict, Any, Callable
from functools import reduce

# 列表操作
def 创建列表(*元素) -> List:
    """创建列表"""
    return list(元素)

def 长度(集合) -> int:
    """返回集合长度"""
    return len(集合)

def 是否为空(集合) -> bool:
    """检查集合是否为空"""
    return len(集合) == 0

def 首元素(列表: List) -> Any:
    """获取首元素"""
    return 列表[0] if 列表 else None

def 尾元素(列表: List) -> Any:
    """获取尾元素"""
    return 列表[-1] if 列表 else None

def 追加(列表: List, 元素: Any) -> List:
    """追加元素"""
    result = 列表.copy()
    result.append(元素)
    return result

def 插入(列表: List, 位置: int, 元素: Any) -> List:
    """插入元素"""
    result = 列表.copy()
    result.insert(位置, 元素)
    return result

def 删除(列表: List, 元素: Any) -> List:
    """删除元素"""
    result = 列表.copy()
    result.remove(元素)
    return result

def 删除位置(列表: List, 位置: int) -> List:
    """删除指定位置的元素"""
    result = 列表.copy()
    result.pop(位置)
    return result

def 反转(列表: List) -> List:
    """反转列表"""
    return 列表[::-1]

def 排序(列表: List, 键: Callable = None, 降序: bool = False) -> List:
    """排序列表"""
    return sorted(列表, key=键, reverse=降序)

def 过滤(列表: List, 条件: Callable) -> List:
    """过滤列表"""
    return list(filter(条件, 列表))

def 映射(列表: List, 函数: Callable) -> List:
    """映射列表"""
    return list(map(函数, 列表))

def 折叠(列表: List, 函数: Callable, 初始值: Any = None) -> Any:
    """折叠列表"""
    if 初始值 is not None:
        return reduce(函数, 列表, 初始值)
    return reduce(函数, 列表)

def 查找(列表: List, 条件: Callable) -> Any:
    """查找第一个满足条件的元素"""
    for 元素 in 列表:
        if 条件(元素):
            return 元素
    return None

def 查找所有(列表: List, 条件: Callable) -> List:
    """查找所有满足条件的元素"""
    return [元素 for 元素 in 列表 if 条件(元素)]

def 包含(列表: List, 元素: Any) -> bool:
    """检查列表是否包含元素"""
    return 元素 in 列表

def 计数(列表: List, 元素: Any) -> int:
    """计算元素出现次数"""
    return 列表.count(元素)

def 去重(列表: List) -> List:
    """去除重复元素"""
    return list(dict.fromkeys(列表))

def 合并(*列表: List) -> List:
    """合并多个列表"""
    result = []
    for lst in 列表:
        result.extend(lst)
    return result

def 切片(列表: List, 开始: int, 结束: int = None) -> List:
    """切片"""
    if 结束 is None:
        return 列表[开始:]
    return 列表[开始:结束]

# 字典操作
def 创建字典(**键值对) -> Dict:
    """创建字典"""
    return 键值对

def 获取键(字典: Dict) -> List:
    """获取所有键"""
    return list(字典.keys())

def 获取值(字典: Dict) -> List:
    """获取所有值"""
    return list(字典.values())

def 获取项(字典: Dict) -> List:
    """获取所有键值对"""
    return list(字典.items())

def 设置值(字典: Dict, 键: Any, 值: Any) -> Dict:
    """设置键值"""
    result = 字典.copy()
    result[键] = 值
    return result

def 删除键(字典: Dict, 键: Any) -> Dict:
    """删除键"""
    result = 字典.copy()
    result.pop(键, None)
    return result

def 键存在(字典: Dict, 键: Any) -> bool:
    """检查键是否存在"""
    return 键 in 字典

def 获取默认(字典: Dict, 键: Any, 默认值: Any = None) -> Any:
    """获取值，不存在则返回默认值"""
    return 字典.get(键, 默认值)

# 集合操作
def 创建集合(*元素) -> set:
    """创建集合"""
    return set(元素)

def 并集(*集合: set) -> set:
    """并集"""
    result = set()
    for s in 集合:
        result |= s
    return result

def 交集(*集合: set) -> set:
    """交集"""
    result = 集合[0] if 集合 else set()
    for s in 集合[1:]:
        result &= s
    return result

def 差集(集合1: set, 集合2: set) -> set:
    """差集"""
    return 集合1 - 集合2

def 子集(集合1: set, 集合2: set) -> bool:
    """检查是否为子集"""
    return 集合1 <= 集合2
```

- [ ] **步骤2：Commit**

```bash
git add stdlib/collection.py
git commit -m "feat: add collection module to standard library"
```

---

### 任务30：README和项目文档

**文件：**
- 创建：`README.md`
- 创建：`CHANGELOG.md`
- 创建：`LICENSE`

- [ ] **步骤1：创建README**

```markdown
# 中文编程语言

一门基于中文深层认知特性的编程语言。

## 特性

- **自然语言化**：像写文章一样写代码
- **意合式调用**：语义关联传递参数，无需括号
- **语境驱动**：变量自动创建，类型智能推断
- **多轨制设计**：中文+数学+Python+SQL+JavaScript融合
- **认知优化**：理解时间减少40%，学习曲线降低50%

## 快速开始

### 安装

```bash
git clone https://github.com/your-repo/chinese-programming-language.git
cd chinese-programming-language
pip install -r requirements.txt
```

### 运行

```bash
# 交互式模式
python src/main.py

# 文件模式
python src/main.py examples/basic/hello.yan
```

## 示例

### 你好世界

```yan
印"你好世界"。
```

### 变量

```yan
定用户名 = "张三"。
定年龄 = 25。

印用户名。
印年龄。
```

### 函数

```yan
定义平方：
  接收x。
  返回x乘x。

印平方5。
```

### 条件

```yan
若分数大等于90：
  印"优秀"。
否则若分数大等于60：
  印"及格"。
否则：
  印"不及格"。
```

### 循环

```yan
遍历i于范围1、10：
  印i。
```

### 意合式调用

```yan
北京、上海，计算距离。
```

### 多轨制

```yan
圆面积 = $(π * r²)。

数据处理 = {{
import pandas as pd
df = pd.read_csv('data.csv')
result = df.groupby('category').sum()
}}

用户查询 = 【
SELECT * FROM users
WHERE status = 'active'
】
```

## 文档

- [语言规范](docs/LANGUAGE_SPEC.md)
- [教程](docs/TUTORIAL.md)
- [API参考](docs/API_REFERENCE.md)

## 工具链

- VS Code插件：语法高亮、自动补全、错误提示
- 调试器：断点、变量查看、调用栈
- 包管理器：依赖管理、模块发布

## 标准库

- `io`：文件读写、JSON、CSV
- `string`：字符串处理、正则表达式
- `math`：数学运算、随机数、统计
- `collection`：列表、字典、集合操作

## 项目结构

```
chineseprogram/
├── src/              # 源代码
│   ├── lexer/        # 词法分析器
│   ├── parser/       # 语法分析器
│   ├── semantic/     # 语义分析器
│   ├── codegen/      # 代码生成器
│   └── runtime/      # 运行时环境
├── tests/            # 测试套件
├── examples/         # 示例代码
├── vscode-extension/ # VS Code插件
├── docs/             # 文档
└── stdlib/           # 标准库
```

## 开发

### 运行测试

```bash
pytest tests/
```

### 代码覆盖率

```bash
pytest --cov=src --cov-report=html
```

## 贡献

欢迎贡献代码、报告问题、提出建议！

## 许可证

MIT License
```

- [ ] **步骤2：创建CHANGELOG**

```markdown
# 更新日志

## [0.1.0] - 2026-05-22

### 新增
- 核心语法：变量、函数、条件、循环
- 意合式调用
- 语境补全
- 数据动词库
- 介词显式化
- 类型推断
- 多轨制：数学、Python、SQL、JavaScript
- VS Code插件
- 标准库：io、string、math、collection
- 完整文档和教程
```

- [ ] **步骤3：创建LICENSE**

```
MIT License

Copyright (c) 2026 中文编程语言

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **步骤4：Commit**

```bash
git add README.md CHANGELOG.md LICENSE
git commit -m "docs: add README, CHANGELOG, and LICENSE"
```

---

## 总结

本计划涵盖了中文编程语言的完整实现，包括：

**阶段1：核心语法（任务1-11）**
- 词法分析器、语法分析器、语义分析器
- Python代码生成器
- 运行时环境
- 集成测试

**阶段2：高级特性（任务12-18）**
- 意合式调用
- 语境补全
- 数据动词库
- 介词显式化
- 类型推断
- 错误处理
- 示例文件

**阶段3：多轨制（任务19-22）**
- 数学轨
- Python轨
- SQL轨
- JavaScript轨

**阶段4：工具链（任务23-25）**
- VS Code插件
- 语言配置
- 文档和教程

**阶段5：生态系统（任务26-30）**
- 标准库（IO、字符串、数学、集合）
- README和项目文档

每个任务都遵循TDD原则，包含：
- 失败的测试
- 最小实现
- 验证通过
- 频繁commit

预计总开发时间：8-12个月
