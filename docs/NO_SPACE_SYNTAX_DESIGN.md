# 心语语言完全无空格语法设计方案

## 目标

实现**完全无空格**的中文编程语法，让代码更加简洁流畅。

---

## 1. 核心设计思路

### 1.1 字典驱动的Token识别

**原理**：使用字典匹配最长关键字

```python
# 关键字字典（按长度排序）
KEYWORDS = {
    # 4字关键字
    "大于等于": ">=",
    "小于等于": "<=",
    
    # 3字关键字
    "定义": "VAR",
    "函数": "FUNCTION",
    "如果": "IF",
    "那么": "THEN",
    "否则": "ELSE",
    "当满足": "WHILE",
    "重复": "REPEAT",
    "次数": "TIMES",
    "遍历": "IN",
    "返回": "RETURN",
    "循环": "FOR",
    "可选": "ELIF",
    "继续": "CONTINUE",
    "跳出": "BREAK",
    "结束": "END",
    
    # 2字操作符动词
    "相加": "+",
    "相减": "-",
    "相乘": "*",
    "相除": "/",
    "取余": "%",
    "等于": "==",
    "不等": "!=",
    "大于": ">",
    "小于": "<",
    "并且": "AND",
    "或者": "OR",
    
    # 2字内置函数
    "打印": "PRINT",
    "输入": "INPUT",
    "长度": "LEN",
    "列表": "LIST",
    "范围": "RANGE",
    "追加": "APPEND",
    "弹出": "POP",
    
    # 3字内置函数
    "平方根": "SQRT",
    "绝对值": "ABS",
    "最大值": "MAX",
    "最小值": "MIN",
    "求和": "SUM",
    "转整数": "INT",
    "转浮点": "FLOAT",
    "转字符串": "STR",
}
```

### 1.2 最长匹配算法

**算法**：从当前位置开始，尝试匹配最长的关键字

```python
def tokenize_no_space(source: str) -> List[Token]:
    """无空格词法分析"""
    tokens = []
    pos = 0
    
    while pos < len(source):
        # 跳过空白字符
        if source[pos].isspace():
            pos += 1
            continue
        
        # 尝试匹配最长关键字
        matched = False
        for length in range(4, 0, -1):  # 从4到1
            if pos + length <= len(source):
                substring = source[pos:pos+length]
                if substring in KEYWORDS:
                    tokens.append(Token(KEYWORDS[substring], substring))
                    pos += length
                    matched = True
                    break
        
        if not matched:
            # 匹配数字
            if source[pos].isdigit():
                num_start = pos
                while pos < len(source) and (source[pos].isdigit() or source[pos] == '.'):
                    pos += 1
                tokens.append(Token('NUMBER', source[num_start:pos]))
                continue
            
            # 匹配字符串
            if source[pos] == '"':
                str_start = pos
                pos += 1
                while pos < len(source) and source[pos] != '"':
                    pos += 1
                pos += 1
                tokens.append(Token('STRING', source[str_start:pos]))
                continue
            
            # 匹配标识符
            if is_chinese_char(source[pos]) or source[pos].isalpha():
                id_start = pos
                while pos < len(source) and (is_chinese_char(source[pos]) or source[pos].isalnum() or source[pos] == '_'):
                    pos += 1
                tokens.append(Token('IDENTIFIER', source[id_start:pos]))
                continue
            
            # 匹配符号
            if source[pos] in '()[]{}。，：=+-*/%<>!':
                tokens.append(Token('SYMBOL', source[pos]))
                pos += 1
                continue
            
            # 未知字符
            raise LexicalError(f"未知字符: {source[pos]}")
    
    return tokens
```

---

## 2. 无空格语法示例

### 2.1 基础示例

```yan
# 有空格版本
定义 x = 5。
打印 x。

# 无空格版本
定义x=5。
打印x。
```

### 2.2 函数定义

```yan
# 有空格版本
定义 平方 = 函 x：
  返回 x 相乘 x。
。

# 无空格版本
定义平方=函x：
  返回x相乘x。
。
```

### 2.3 条件语句

```yan
# 有空格版本
如果 x 大于 5 那么：
  打印 "大"。
否则：
  打印 "小"。
。

# 无空格版本
如果x大于5那么：
  打印"大"。
否则：
  打印"小"。
。
```

### 2.4 复杂表达式

```yan
# 有空格版本
定义 结果 = (3 相加 5) 相乘 2。
定义 最大 = 最大值 1 5 3 2。

# 无空格版本
定义结果=(3相加5)相乘2。
定义最大=最大值1 5 3 2。
```

---

## 3. 实现方案

### 3.1 新词法分析器

**文件**：`src/lexer/no_space_lexer.py`

```python
"""无空格词法分析器

实现完全无空格的中文编程语法。
"""

from typing import List, Tuple
from src.lexer.tokens import Token, TokenType

class NoSpaceLexer:
    """无空格词法分析器"""
    
    # 关键字字典（按长度降序排列）
    KEYWORDS = {
        # 4字
        "大于等于": (TokenType.GREATER_EQ, ">="),
        "小于等于": (TokenType.LESS_EQ, "<="),
        
        # 3字
        "定义": (TokenType.VAR, "var"),
        "函数": (TokenType.FUNCTION, "function"),
        "如果": (TokenType.IF, "if"),
        "那么": (TokenType.THEN, "then"),
        "否则": (TokenType.ELSE, "else"),
        "当满足": (TokenType.WHILE, "while"),
        "重复": (TokenType.REPEAT, "repeat"),
        "次数": (TokenType.TIMES, "times"),
        "遍历": (TokenType.IN, "in"),
        "返回": (TokenType.RETURN, "return"),
        "循环": (TokenType.FOR, "for"),
        "可选": (TokenType.ELIF, "elif"),
        "继续": (TokenType.CONTINUE, "continue"),
        "跳出": (TokenType.BREAK, "break"),
        "结束": (TokenType.END, "end"),
        "平方根": (TokenType.IDENTIFIER, "sqrt"),
        "绝对值": (TokenType.IDENTIFIER, "abs"),
        "最大值": (TokenType.IDENTIFIER, "max"),
        "最小值": (TokenType.IDENTIFIER, "min"),
        "求和": (TokenType.IDENTIFIER, "sum"),
        "转整数": (TokenType.IDENTIFIER, "int"),
        "转浮点": (TokenType.IDENTIFIER, "float"),
        "转字符串": (TokenType.IDENTIFIER, "str"),
        
        # 2字
        "相加": (TokenType.PLUS, "+"),
        "相减": (TokenType.MINUS, "-"),
        "相乘": (TokenType.MULTIPLY, "*"),
        "相除": (TokenType.DIVIDE, "/"),
        "取余": (TokenType.MODULO, "%"),
        "等于": (TokenType.EQUALS, "=="),
        "不等": (TokenType.NOT_EQUALS, "!="),
        "大于": (TokenType.GREATER, ">"),
        "小于": (TokenType.LESS, "<"),
        "并且": (TokenType.AND, "and"),
        "或者": (TokenType.OR, "or"),
        "打印": (TokenType.IDENTIFIER, "print"),
        "输入": (TokenType.IDENTIFIER, "input"),
        "长度": (TokenType.IDENTIFIER, "len"),
        "列表": (TokenType.IDENTIFIER, "list"),
        "范围": (TokenType.IDENTIFIER, "range"),
        "追加": (TokenType.IDENTIFIER, "append"),
        "弹出": (TokenType.IDENTIFIER, "pop"),
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
    
    def tokenize(self) -> List[Token]:
        """词法分析"""
        tokens = []
        
        while self.pos < len(self.source):
            token = self._next_token()
            if token:
                tokens.append(token)
        
        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens
    
    def _next_token(self) -> Token:
        """获取下一个token"""
        self._skip_whitespace()
        
        if self.pos >= len(self.source):
            return None
        
        # 尝试匹配最长关键字
        for length in range(4, 0, -1):
            if self.pos + length <= len(self.source):
                substring = self.source[self.pos:self.pos+length]
                if substring in self.KEYWORDS:
                    token_type, value = self.KEYWORDS[substring]
                    token = Token(token_type, value, self.line, self.column)
                    self._advance(length)
                    return token
        
        # 匹配数字
        if self.source[self.pos].isdigit():
            return self._read_number()
        
        # 匹配字符串
        if self.source[self.pos] == '"':
            return self._read_string()
        
        # 匹配标识符
        if self._is_identifier_start():
            return self._read_identifier()
        
        # 匹配符号
        return self._read_symbol()
    
    def _skip_whitespace(self):
        """跳过空白字符"""
        while self.pos < len(self.source) and self.source[self.pos].isspace():
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def _advance(self, count: int = 1):
        """前进count个字符"""
        for _ in range(count):
            if self.pos < len(self.source):
                if self.source[self.pos] == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.pos += 1
    
    def _is_identifier_start(self) -> bool:
        """判断是否是标识符开始"""
        char = self.source[self.pos]
        return (char.isalpha() or 
                '\u4e00' <= char <= '\u9fff' or 
                char == '_')
    
    def _read_number(self) -> Token:
        """读取数字"""
        start = self.pos
        start_col = self.column
        
        while self.pos < len(self.source):
            char = self.source[self.pos]
            if char.isdigit() or char == '.':
                self._advance()
            else:
                break
        
        value = self.source[start:self.pos]
        return Token(TokenType.NUMBER, value, self.line, start_col)
    
    def _read_string(self) -> Token:
        """读取字符串"""
        start_col = self.column
        self._advance()  # 跳过开始引号
        
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos] != '"':
            self._advance()
        
        value = self.source[start:self.pos]
        self._advance()  # 跳过结束引号
        
        return Token(TokenType.STRING, value, self.line, start_col)
    
    def _read_identifier(self) -> Token:
        """读取标识符"""
        start = self.pos
        start_col = self.column
        
        while self.pos < len(self.source):
            char = self.source[self.pos]
            if (char.isalnum() or 
                '\u4e00' <= char <= '\u9fff' or 
                char == '_'):
                self._advance()
            else:
                break
        
        value = self.source[start:self.pos]
        return Token(TokenType.IDENTIFIER, value, self.line, start_col)
    
    def _read_symbol(self) -> Token:
        """读取符号"""
        char = self.source[self.pos]
        start_col = self.column
        
        symbol_map = {
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            '。': TokenType.PERIOD,
            '，': TokenType.COMMA,
            '：': TokenType.COLON,
            '=': TokenType.ASSIGN,
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '%': TokenType.MODULO,
            '<': TokenType.LESS,
            '>': TokenType.GREATER,
            '!': TokenType.NOT,
        }
        
        token_type = symbol_map.get(char, TokenType.UNKNOWN)
        token = Token(token_type, char, self.line, start_col)
        self._advance()
        
        return token
```

### 3.2 配置选项

**文件**：`src/config.py`

```python
"""配置选项"""

class LexerMode:
    """词法分析器模式"""
    STANDARD = "standard"    # 标准模式（需要空格）
    NO_SPACE = "no_space"    # 无空格模式
    AUTO = "auto"            # 自动检测

# 全局配置
LEXER_MODE = LexerMode.STANDARD
```

### 3.3 自动检测

```python
def detect_lexer_mode(source: str) -> str:
    """自动检测词法分析器模式
    
    检测规则：
    - 如果包含"定义x"这样的模式，使用无空格模式
    - 否则使用标准模式
    """
    # 检测无空格模式特征
    no_space_patterns = [
        "定义x", "定义y", "定义z",
        "如果x", "如果y", "如果z",
        "打印x", "打印y", "打印z",
    ]
    
    for pattern in no_space_patterns:
        if pattern in source:
            return LexerMode.NO_SPACE
    
    return LexerMode.STANDARD
```

---

## 4. 测试用例

### 4.1 基础测试

```python
def test_no_space_variable():
    """测试无空格变量定义"""
    source = "定义x=5。"
    lexer = NoSpaceLexer(source)
    tokens = lexer.tokenize()
    
    assert len(tokens) == 5
    assert tokens[0].type == TokenType.VAR
    assert tokens[1].type == TokenType.IDENTIFIER
    assert tokens[2].type == TokenType.ASSIGN
    assert tokens[3].type == TokenType.NUMBER
    assert tokens[4].type == TokenType.PERIOD

def test_no_space_function():
    """测试无空格函数定义"""
    source = "定义平方=函x：返回x相乘x。。"
    lexer = NoSpaceLexer(source)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.VAR
    assert tokens[1].value == "平方"
    assert tokens[3].type == TokenType.FUNCTION

def test_no_space_condition():
    """测试无空格条件语句"""
    source = "如果x大于5那么：打印\"大\"。"
    lexer = NoSpaceLexer(source)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.IF
    assert tokens[2].type == TokenType.GREATER
```

---

## 5. 优势与挑战

### 5.1 优势

- ✅ **代码简洁** - 减少空格，代码更紧凑
- ✅ **输入高效** - 减少按键次数
- ✅ **视觉清晰** - 无空格干扰，结构更清晰
- ✅ **符合习惯** - 类似易语言等中文编程语言

### 5.2 挑战

- ❌ **实现复杂** - 需要最长匹配算法
- ❌ **性能开销** - 字典查找有性能开销
- ❌ **歧义风险** - 可能存在识别歧义
- ❌ **可读性** - 部分人认为有空格更易读

---

## 6. 实施计划

### 阶段1：原型实现（1天）
- 实现NoSpaceLexer
- 添加基础测试
- 验证可行性

### 阶段2：完善功能（2天）
- 处理所有关键字
- 处理边界情况
- 优化性能

### 阶段3：集成测试（1天）
- 集成到主系统
- 添加配置选项
- 完善文档

### 阶段4：发布（1天）
- 更新文档
- 发布新版本
- 收集反馈

---

## 7. 总结

**完全无空格语法是可行的！**

**关键点**：
1. 字典驱动的最长匹配
2. 智能token识别
3. 配置选项支持
4. 向后兼容

**预期效果**：
```yan
# 无空格版本
定义x=5。
定义平方=函x：返回x相乘x。。
如果x大于5那么：打印"大"。否则：打印"小"。。
```

**代码更简洁，输入更高效！**

---

**文档版本**：v1.0
**最后更新**：2026-05-27
