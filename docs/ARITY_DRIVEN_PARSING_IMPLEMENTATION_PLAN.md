# 元数驱动解析实施计划

**日期：** 2026-05-27  
**总工期：** 8天  
**目标：** 实现元数驱动解析，解决无括号函数调用歧义问题

---

## 实施概览

| 阶段 | 任务 | 工期 | 优先级 |
|------|------|------|--------|
| 阶段1 | 基础设施搭建 | 2天 | 最高 |
| 阶段2 | 解析器重构 | 3天 | 最高 |
| 阶段3 | AST和代码生成 | 1天 | 高 |
| 阶段4 | 用户定义函数 | 1天 | 高 |
| 阶段5 | 测试和优化 | 1天 | 高 |

---

## 阶段1：基础设施搭建（2天）

### Day 1

**任务1：创建元数定义模块**

**文件：** `src/parser/arity.py`

**内容：**
```python
from enum import Enum
from typing import Optional

class ArityType(Enum):
    """元数类型"""
    FIXED = "fixed"        # 固定数量
    VARIABLE = "variable"  # 可变数量
    MINIMUM = "minimum"    # 最小数量
    RANGE = "range"        # 范围数量

class Arity:
    """元数定义"""
    
    def __init__(
        self,
        type: ArityType,
        count: Optional[int] = None,
        min_count: Optional[int] = None,
        max_count: Optional[int] = None
    ):
        self.type = type
        self.count = count
        self.min_count = min_count
        self.max_count = max_count
    
    @classmethod
    def fixed(cls, count: int) -> 'Arity':
        """固定元数"""
        return cls(ArityType.FIXED, count=count)
    
    @classmethod
    def variable(cls, min: int = 0) -> 'Arity':
        """可变元数"""
        return cls(ArityType.VARIABLE, min_count=min)
    
    @classmethod
    def min(cls, min_count: int) -> 'Arity':
        """最小元数"""
        return cls(ArityType.MINIMUM, min_count=min_count)
    
    @classmethod
    def range(cls, min: int, max: int) -> 'Arity':
        """范围元数"""
        return cls(ArityType.RANGE, min_count=min, max_count=max)
    
    def is_satisfied(self, arg_count: int) -> bool:
        """检查参数数量是否满足要求"""
        # 实现详见解决方案文档
    
    def should_stop_collecting(self, arg_count: int) -> bool:
        """是否应该停止收集参数"""
        # 实现详见解决方案文档
```

**预期结果：**
- 文件创建成功
- 单元测试通过

---

**任务2：创建动词注册表**

**文件：** `src/parser/verb_registry.py`

**内容：**
```python
from typing import Dict, Optional, Set
from .arity import Arity

class VerbRegistry:
    """动词元数注册表"""
    
    def __init__(self):
        self._verbs: Dict[str, Arity] = {}
        self._operator_verbs: Set[str] = set()
        self._function_verbs: Set[str] = set()
    
    def register(
        self,
        name: str,
        arity: Arity,
        is_operator: bool = False,
        is_function: bool = False
    ) -> None:
        """注册动词"""
        self._verbs[name] = arity
        if is_operator:
            self._operator_verbs.add(name)
        if is_function:
            self._function_verbs.add(name)
    
    def get(self, name: str) -> Optional[Arity]:
        """获取动词元数"""
        return self._verbs.get(name)
    
    def is_operator(self, name: str) -> bool:
        """判断是否是操作符动词"""
        return name in self._operator_verbs
    
    def is_function(self, name: str) -> bool:
        """判断是否是函数动词"""
        return name in self._function_verbs
    
    def is_registered(self, name: str) -> bool:
        """判断动词是否已注册"""
        return name in self._verbs
    
    def register_builtin_verbs(self) -> None:
        """注册内置动词"""
        # 实现详见解决方案文档
```

**预期结果：**
- 文件创建成功
- 内置动词注册完成

---

**任务3：创建单元测试**

**文件：** `tests/test_arity.py`

**测试用例：**
```python
def test_fixed_arity():
    """测试固定元数"""
    arity = Arity.fixed(2)
    assert arity.is_satisfied(2) == True
    assert arity.is_satisfied(1) == False
    assert arity.should_stop_collecting(2) == True

def test_variable_arity():
    """测试可变元数"""
    arity = Arity.variable(min=0)
    assert arity.is_satisfied(0) == True
    assert arity.is_satisfied(5) == True
    assert arity.should_stop_collecting(3) == False

def test_minimum_arity():
    """测试最小元数"""
    arity = Arity.min(2)
    assert arity.is_satisfied(1) == False
    assert arity.is_satisfied(2) == True
    assert arity.is_satisfied(5) == True

def test_range_arity():
    """测试范围元数"""
    arity = Arity.range(min=1, max=3)
    assert arity.is_satisfied(0) == False
    assert arity.is_satisfied(1) == True
    assert arity.is_satisfied(3) == True
    assert arity.is_satisfied(4) == False
```

**文件：** `tests/test_verb_registry.py`

**测试用例：**
```python
def test_register_operator():
    """测试注册操作符"""
    registry = VerbRegistry()
    registry.register("相加", Arity.fixed(2), is_operator=True)
    
    assert registry.is_operator("相加") == True
    assert registry.is_function("相加") == False
    assert registry.get("相加").count == 2

def test_register_function():
    """测试注册函数"""
    registry = VerbRegistry()
    registry.register("打印", Arity.variable(min=1), is_function=True)
    
    assert registry.is_function("打印") == True
    assert registry.is_operator("打印") == False

def test_builtin_verbs():
    """测试内置动词"""
    registry = VerbRegistry()
    registry.register_builtin_verbs()
    
    assert registry.is_operator("相加") == True
    assert registry.is_function("打印") == True
```

**预期结果：**
- 测试全部通过

---

### Day 2

**任务1：集成到解析器**

**修改文件：** `src/parser/parser.py`

**修改点：**
1. 在 `__init__` 中初始化 VerbRegistry
   ```python
   def __init__(self, tokens: List[Token]):
       self.tokens = tokens
       self.pos = 0
       self.verb_registry = VerbRegistry()
       self.verb_registry.register_builtin_verbs()
   ```

2. 添加辅助方法
   ```python
   def _is_operator_verb(self, name: str) -> bool:
       """判断是否是操作符动词"""
       return self.verb_registry.is_operator(name)
   
   def _get_verb_arity(self, name: str) -> Optional[Arity]:
       """获取动词元数"""
       return self.verb_registry.get(name)
   ```

**预期结果：**
- 解析器集成 VerbRegistry
- 现有测试仍然通过

---

**任务2：更新 AST 节点**

**修改文件：** `src/parser/ast_nodes.py`

**修改点：**
```python
@dataclass
class FunctionDefNode(ASTNode):
    """函数定义节点"""
    name: str
    params: List[str]
    body: List[ASTNode]
    arity: Optional[Arity] = None  # 新增：元数
```

**预期结果：**
- AST 节点支持元数字段

---

## 阶段2：解析器重构（3天）

### Day 3

**任务1：修改 `_parse_identifier_or_call`**

**核心逻辑：**
```python
def _parse_identifier_or_call(self) -> ASTNode:
    """解析标识符或函数调用（元数驱动）"""
    token = self._advance()
    name = token.value
    
    # 检查是否是操作符动词
    if self._is_operator_verb(name):
        # 操作符动词在中缀位置，不应该作为函数调用
        # 回退，让表达式解析器处理
        self.pos -= 1
        return IdentifierNode(line=token.line, column=token.column, name=name)
    
    # 获取动词元数
    arity = self._get_verb_arity(name)
    
    if arity is None:
        # 未注册的动词，可能是用户定义的函数
        arity = Arity.variable(min=0)
    
    # 根据元数收集参数
    args = self._collect_args_by_arity(arity)
    
    return FunctionCallNode(
        line=token.line,
        column=token.column,
        name=name,
        args=args
    )
```

**预期结果：**
- 函数调用支持元数驱动

---

**任务2：实现 `_collect_args_by_arity`**

**核心逻辑：**
```python
def _collect_args_by_arity(self, arity: Arity) -> List[ASTNode]:
    """根据元数收集参数"""
    args = []
    
    while not self._is_at_end():
        # 检查是否应该停止收集
        if self._should_stop_collecting():
            break
        
        # 检查元数是否已满足
        if arity.should_stop_collecting(len(args)):
            break
        
        # 解析参数（只解析基础表达式，不贪婪）
        arg = self._parse_primary()
        args.append(arg)
    
    # 验证参数数量
    if not arity.is_satisfied(len(args)):
        raise ParseError(
            f"参数数量错误：期望{arity}，实际{len(args)}",
            self._current_token()
        )
    
    return args
```

**预期结果：**
- 参数收集正确

---

**任务3：实现 `_should_stop_collecting`**

**核心逻辑：**
```python
def _should_stop_collecting(self) -> bool:
    """判断是否应该停止收集参数"""
    # 遇到操作符动词，停止收集
    current = self._current_token()
    if current.type == TokenType.IDENTIFIER:
        if self._is_operator_verb(current.value):
            return True
    
    # 遇到终止符，停止收集
    if self._check(TokenType.NEWLINE, TokenType.EOF, TokenType.PERIOD,
                  TokenType.THEN, TokenType.ELSE, TokenType.ELIF,
                  TokenType.RPAREN, TokenType.RBRACKET, TokenType.RBRACE,
                  TokenType.COMMA, TokenType.COLON):
        return True
    
    return False
```

**预期结果：**
- 停止条件正确

---

### Day 4

**任务1：处理操作符动词**

**问题：** `相加` 既可以是操作符，也可以是函数调用

**解决方案：**

1. **在 `_parse_addition` 中处理操作符动词**
   ```python
   def _parse_addition(self) -> ASTNode:
       """解析加减表达式"""
       left = self._parse_multiplication()
       
       # 检查当前token是否是操作符动词
       while self._check(TokenType.PLUS, TokenType.MINUS) or \
             (self._check(TokenType.IDENTIFIER) and 
              self._is_operator_verb(self._current_token().value)):
           
           op = self._advance()
           
           # 映射操作符动词到符号
           if op.type == TokenType.IDENTIFIER:
               op_symbol = self._get_operator_symbol(op.value)
           else:
               op_symbol = self._get_operator(op)
           
           right = self._parse_multiplication()
           left = BinaryOpNode(
               line=op.line,
               column=op.column,
               left=left,
               operator=op_symbol,
               right=right
           )
       
       return left
   ```

2. **添加操作符映射**
   ```python
   def _get_operator_symbol(self, verb_name: str) -> str:
       """将操作符动词映射到符号"""
       mapping = {
           "相加": "+",
           "相减": "-",
           "相乘": "*",
           "相除": "/",
           "等于": "==",
           "大于": ">",
           "小于": "<",
           # ...
       }
       return mapping.get(verb_name, verb_name)
   ```

**预期结果：**
- 操作符动词正确处理

---

**任务2：修改 `_parse_primary`**

**修改点：** 只解析基础表达式，不贪婪

```python
def _parse_primary(self) -> ASTNode:
    """解析基础表达式（不贪婪）"""
    # 数值
    if self._check(TokenType.NUMBER):
        token = self._advance()
        return NumberNode(line=token.line, column=token.column, value=token.value)
    
    # 字符串
    if self._check(TokenType.STRING):
        token = self._advance()
        return StringNode(line=token.line, column=token.column, value=token.value)
    
    # 标识符或函数调用
    if self._check(TokenType.IDENTIFIER):
        return self._parse_identifier_or_call()
    
    # 括号
    if self._check(TokenType.LPAREN):
        self._advance()
        expr = self._parse_expression()
        self._expect(TokenType.RPAREN, "Expected ')' after expression")
        return expr
    
    # 列表
    if self._check(TokenType.LBRACKET):
        return self._parse_list()
    
    raise ParseError(f"Unexpected token: {self._current_token().type.name}", 
                     self._current_token())
```

**预期结果：**
- 不贪婪解析

---

### Day 5

**任务1：添加解析器测试**

**文件：** `tests/test_parser_arity.py`

**测试用例：**
```python
def test_fixed_arity_function_call():
    """测试固定元数函数调用"""
    source = "斐波那契 5。"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    assert isinstance(ast.statements[0], FunctionCallNode)
    assert ast.statements[0].name == "斐波那契"
    assert len(ast.statements[0].args) == 1

def test_variable_arity_function_call():
    """测试可变元数函数调用"""
    source = '打印 "你好" "世界" "！"。'
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    assert isinstance(ast.statements[0], FunctionCallNode)
    assert len(ast.statements[0].args) == 3

def test_operator_verb_in_expression():
    """测试操作符动词在表达式中"""
    source = "a 相加 b。"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    assert isinstance(ast.statements[0], BinaryOpNode)
    assert ast.statements[0].operator == "+"

def test_function_call_with_operator_args():
    """测试函数调用参数包含操作符"""
    source = "斐波那契 n 相减 1 相加 斐波那契 n 相减 2。"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    # 应该解析为：(斐波那契(n-1)) + (斐波那契(n-2))
    expr = ast.statements[0]
    assert isinstance(expr, BinaryOpNode)
    assert expr.operator == "+"
    assert isinstance(expr.left, FunctionCallNode)
    assert isinstance(expr.right, FunctionCallNode)
```

**预期结果：**
- 测试通过

---

## 阶段3：AST和代码生成（1天）

### Day 6

**任务1：修改 FunctionCallNode**

**修改文件：** `src/parser/ast_nodes.py`

```python
@dataclass
class FunctionCallNode(ASTNode):
    """函数调用节点"""
    name: str
    args: List[ASTNode]
    arity: Optional[Arity] = None  # 新增
```

**预期结果：**
- AST 支持元数

---

**任务2：修改代码生成器**

**修改文件：** `src/codegen/python_codegen.py`

**修改点：** 支持可变参数函数调用

```python
def _generate_functioncall(self, node: FunctionCallNode) -> str:
    """生成函数调用表达式"""
    # 映射内置函数名
    func_name = self.BUILTIN_FUNCTIONS.get(node.name, node.name)
    
    # 生成参数列表
    args = [self.generate(arg) for arg in node.args]
    
    return f"{func_name}({', '.join(args)})"
```

**预期结果：**
- 代码生成正确

---

**任务3：添加代码生成测试**

**文件：** `tests/test_codegen_arity.py`

**测试用例：**
```python
def test_generate_function_call_with_arity():
    """测试生成函数调用（元数驱动）"""
    node = FunctionCallNode(
        line=1, column=0,
        name="打印",
        args=[
            StringNode(line=1, column=3, value="你好"),
            StringNode(line=1, column=9, value="世界")
        ]
    )
    
    codegen = PythonCodegen()
    result = codegen.generate(node)
    
    assert result == 'print("你好", "世界")'
```

**预期结果：**
- 测试通过

---

## 阶段4：用户定义函数（1天）

### Day 7

**任务1：实现用户定义函数的元数推断**

**修改文件：** `src/parser/parser.py`

**修改点：**
```python
def _parse_function_def(self, name: str, line: int, column: int) -> FunctionDefNode:
    """解析函数定义"""
    self._advance()  # 消费 函数
    
    # 解析参数列表
    params = []
    while not self._check(TokenType.COLON, TokenType.NEWLINE, TokenType.EOF):
        if self._check(TokenType.IDENTIFIER):
            param_token = self._advance()
            params.append(param_token.value)
        else:
            break
    
    # 推断元数
    arity = Arity.fixed(len(params))  # 固定元数
    
    # 期望 ：
    self._expect(TokenType.COLON, "Expected '：' after function parameters")
    
    # 解析函数体
    body = self._parse_block()
    
    # 注册动词
    self.verb_registry.register(name, arity, is_function=True)
    
    return FunctionDefNode(
        line=line,
        column=column,
        name=name,
        params=params,
        body=body,
        arity=arity
    )
```

**预期结果：**
- 用户定义函数自动注册元数

---

**任务2：添加元数声明语法（可选）**

**新增语法：**
```yan
定义 斐波那契 = 函数 n：元数 1。
  如果 n 小于等于 1 那么：
    返回 n。
  否则：
    返回 斐波那契 n 相减 1 相加 斐波那契 n 相减 2。
```

**修改点：**
```python
# 在解析函数定义后，检查是否有"元数"关键字
if self._check(TokenType.IDENTIFIER) and self._current_token().value == "元数":
    self._advance()  # 消费 元数
    arity_count = self._expect(TokenType.NUMBER, "Expected number after '元数'")
    arity = Arity.fixed(int(arity_count.value))
    node.arity = arity
    self.verb_registry.register(name, arity, is_function=True)
```

**预期结果：**
- 支持显式元数声明

---

## 阶段5：测试和优化（1天）

### Day 8

**任务1：运行完整测试套件**

```bash
python -m pytest tests/ -v
```

**目标：**
- 测试通过率 > 95%

---

**任务2：修复回归问题**

如果测试失败：
1. 分析失败原因
2. 修复代码
3. 重新测试

---

**任务3：性能优化**

- 优化 VerbRegistry 查询
- 添加缓存
- 性能测试

---

**任务4：文档更新**

**更新文件：**
- `README.md`
- `docs/LANGUAGE_SPEC.md`
- `docs/GETTING_STARTED.md`

**内容：**
- 元数驱动解析说明
- 内置动词元数列表
- 用户定义函数元数声明

---

## 验收标准

### 功能验收

- [ ] 固定元数函数调用正确
- [ ] 可变元数函数调用正确
- [ ] 操作符动词正确处理
- [ ] 用户定义函数元数推断正确
- [ ] 显式元数声明支持

### 质量验收

- [ ] 测试通过率 > 95%
- [ ] 无性能回归
- [ ] 代码覆盖率 > 80%
- [ ] 文档完整

---

## 风险管理

### 技术风险

**风险：解析器重构破坏现有功能**
- **缓解：** 分阶段实施，每阶段运行测试
- **回滚：** 保留旧代码，可以快速回滚

### 时间风险

**风险：工期延误**
- **缓解：** 优先完成核心功能，可选功能可以延后

---

## 总结

**总工期：** 8天  
**预期结果：**
- 测试通过率 > 95%
- 无歧义解析
- 支持可变参数

**关键点：**
1. 元数系统设计合理
2. 解析器重构彻底
3. 测试覆盖完整

---

**文档版本：** v1.0  
**最后更新：** 2026-05-27
