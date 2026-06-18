# 元数驱动解析解决方案

**日期：** 2026-05-27
**目标：** 实现元数驱动解析，解决无括号函数调用的歧义问题
**学习对象：** newlisp/yan

---

## 一、问题分析

### 1.1 当前问题

**歧义示例：**
```yan
斐波那契 n 相减 1 相加 斐波那契 n 相减 2
```

这行代码有**两种合法的解释**：
1. `斐波那契(整个表达式)` - 一个函数调用
2. `斐波那契(n-1) + 斐波那契(n-2)` - 两个函数调用相加

解析器无法确定何时停止参数收集。

### 1.2 根本原因

心语语言采用**无括号函数调用语法**：
```yan
函数名 参数1 参数2。
```

但没有明确参数边界，导致歧义。

---

## 二、解决方案：元数驱动解析

### 2.1 核心思想

**元数（Arity）** = 函数/动词的参数数量

**原理：**
- 每个动词声明参数数量（元数）
- 解析器根据元数自动收集参数
- 收集到足够参数后停止

### 2.2 元数类型

中文编程语言的特殊性：**参数数量不固定**

**设计的元数类型：**

1. **固定元数（Fixed Arity）**
   ```python
   Arity.fixed(2)  # 必须有2个参数
   ```
   示例：`相加 a b`，`相减 a b`

2. **可变元数（Variable Arity）**
   ```python
   Arity.variable(min=0)  # 可以有任意数量的参数
   ```
   示例：`打印 "你好" "世界" "！"`

3. **最小元数（Minimum Arity）**
   ```python
   Arity.min(2)  # 最少2个参数，可以更多
   ```
   示例：`求和 1 2 3 4 5`

4. **范围元数（Range Arity）**
   ```python
   Arity.range(min=1, max=3)  # 1-3个参数
   ```
   示例：`读取文件 文件名 编码？`

### 2.3 动词分类

在中文编程语言中，需要区分两类"动词"：

**1. 操作符动词（Operator Verbs）**
- 特点：中缀位置，固定元数
- 示例：`相加`、`相减`、`相乘`、`相除`
- 元数：`Arity.fixed(2)`

**2. 函数动词（Function Verbs）**
- 特点：前缀位置，元数可变
- 示例：`打印`、`求和`、`斐波那契`
- 元数：`Arity.variable()` 或 `Arity.fixed(n)`

---

## 三、实现设计

### 3.1 元数系统

```python
# src/parser/arity.py

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
        """可变元数（最少min个）"""
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
        if self.type == ArityType.FIXED:
            return arg_count == self.count
        elif self.type == ArityType.VARIABLE:
            return arg_count >= self.min_count
        elif self.type == ArityType.MINIMUM:
            return arg_count >= self.min_count
        elif self.type == ArityType.RANGE:
            return self.min_count <= arg_count <= self.max_count
        return False

    def should_stop_collecting(self, arg_count: int) -> bool:
        """是否应该停止收集参数"""
        if self.type == ArityType.FIXED:
            return arg_count >= self.count
        elif self.type == ArityType.RANGE:
            return arg_count >= self.max_count
        # VARIABLE 和 MINIMUM 类型不主动停止
        return False
```

### 3.2 动词元数注册表

```python
# src/parser/verb_registry.py

from typing import Dict, Optional
from .arity import Arity

class VerbRegistry:
    """动词元数注册表"""

    def __init__(self):
        self._verbs: Dict[str, Arity] = {}
        self._operator_verbs: set = set()  # 操作符动词

    def register(
        self,
        name: str,
        arity: Arity,
        is_operator: bool = False
    ) -> None:
        """注册动词"""
        self._verbs[name] = arity
        if is_operator:
            self._operator_verbs.add(name)

    def get(self, name: str) -> Optional[Arity]:
        """获取动词元数"""
        return self._verbs.get(name)

    def is_operator(self, name: str) -> bool:
        """判断是否是操作符动词"""
        return name in self._operator_verbs

    def is_registered(self, name: str) -> bool:
        """判断动词是否已注册"""
        return name in self._verbs

    def register_builtin_verbs(self) -> None:
        """注册内置动词"""
        # 操作符动词（固定2个参数，中缀）
        operators = [
            "相加", "相减", "相乘", "相除", "取余",
            "等于", "不等", "大于", "小于", "大于等于", "小于等于",
            "并且", "或者"
        ]
        for op in operators:
            self.register(op, Arity.fixed(2), is_operator=True)

        # 内置函数（可变参数）
        self.register("打印", Arity.variable(min=1))
        self.register("输入", Arity.fixed(1))

        # 数学函数
        self.register("平方根", Arity.fixed(1))
        self.register("绝对值", Arity.fixed(1))
        self.register("最大值", Arity.variable(min=1))
        self.register("最小值", Arity.variable(min=1))
        self.register("求和", Arity.variable(min=1))
```

### 3.3 解析器修改

```python
# src/parser/parser.py (修改部分)

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.verb_registry = VerbRegistry()
        self.verb_registry.register_builtin_verbs()

    def _parse_identifier_or_call(self) -> ASTNode:
        """解析标识符或函数调用（元数驱动）"""
        token = self._advance()
        name = token.value

        # 检查是否是操作符动词
        if self.verb_registry.is_operator(name):
            # 操作符动词在中缀位置，不应该作为函数调用
            # 回退，让表达式解析器处理
            self.pos -= 1
            return IdentifierNode(line=token.line, column=token.column, name=name)

        # 获取动词元数
        arity = self.verb_registry.get(name)

        if arity is None:
            # 未注册的动词，可能是用户定义的函数
            # 尝试推断元数（默认收集到操作符或终止符）
            arity = Arity.variable(min=0)

        # 根据元数收集参数
        args = self._collect_args_by_arity(arity)

        return FunctionCallNode(
            line=token.line,
            column=token.column,
            name=name,
            args=args
        )

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

            # 解析参数
            arg = self._parse_primary()  # 只解析基础表达式，避免贪婪
            args.append(arg)

        # 验证参数数量
        if not arity.is_satisfied(len(args)):
            raise ParseError(
                f"参数数量错误：期望{arity}，实际{len(args)}",
                self._current_token()
            )

        return args

    def _should_stop_collecting(self) -> bool:
        """判断是否应该停止收集参数"""
        # 遇到操作符动词，停止收集
        current = self._current_token()
        if current.type == TokenType.IDENTIFIER:
            if self.verb_registry.is_operator(current.value):
                return True

        # 遇到终止符，停止收集
        if self._check(TokenType.NEWLINE, TokenType.EOF, TokenType.PERIOD,
                      TokenType.THEN, TokenType.ELSE, TokenType.ELIF,
                      TokenType.RPAREN, TokenType.RBRACKET, TokenType.RBRACE,
                      TokenType.COMMA, TokenType.COLON):
            return True

        return False
```

### 3.4 关键点：操作符动词的处理

**问题：** `相加` 既可以是操作符，也可以是函数调用

```yan
# 操作符用法（中缀）
a 相加 b

# 函数调用用法（前缀）
相加 a b
```

**解决方案：**

1. **根据上下文判断**
   - 如果前面有表达式，`相加` 是操作符
   - 如果前面没有表达式，`相加` 是函数调用

2. **修改表达式解析器**
   ```python
   def _parse_addition(self) -> ASTNode:
       """解析加减表达式"""
       left = self._parse_multiplication()

       while self._check(TokenType.PLUS, TokenType.MINUS):
           op = self._advance()
           right = self._parse_multiplication()
           left = BinaryOpNode(
               line=op.line,
               column=op.column,
               left=left,
               operator=self._get_operator(op),
               right=right
           )

       return left
   ```

---

## 四、实施计划

### 阶段1：基础设施（2天）

**任务：**
1. 创建 `src/parser/arity.py` - 元数定义
2. 创建 `src/parser/verb_registry.py` - 动词注册表
3. 修改 `src/parser/parser.py` - 添加元数系统
4. 添加单元测试

**预期结果：**
- 元数系统可用
- 内置动词注册完成

---

### 阶段2：修改解析器（3天）

**任务：**
1. 修改 `_parse_identifier_or_call` 方法
   - 实现元数驱动参数收集
   - 区分操作符动词和函数动词

2. 修改 `_parse_primary` 方法
   - 只解析基础表达式（不贪婪）

3. 修改表达式解析器
   - 处理操作符动词的中缀用法

4. 添加单元测试

**预期结果：**
- 解析器支持元数驱动解析
- 测试通过率 > 95%

---

### 阶段3：AST和代码生成（1天）

**任务：**
1. 修改 FunctionCallNode
   - 添加元数字段

2. 修改 PythonCodegen
   - 支持可变参数函数调用

3. 添加测试

**预期结果：**
- 代码生成正确
- 测试通过

---

### 阶段4：用户定义函数（1天）

**任务：**
1. 实现用户定义函数的元数推断
   - 从函数定义中提取参数数量
   - 注册到 VerbRegistry

2. 添加元数声明语法（可选）
   ```yan
   定义 斐波那契 = 函数 n：元数 1。
   ```

3. 添加测试

**预期结果：**
- 用户定义函数支持元数系统

---

### 阶段5：测试和优化（1天）

**任务：**
1. 运行完整测试套件
2. 修复回归问题
3. 性能优化
4. 文档更新

**预期结果：**
- 测试通过率 99%+
- 无性能回归

---

## 五、示例对比

### 5.1 修复前

**代码：**
```yan
斐波那契 n 相减 1 相加 斐波那契 n 相减 2
```

**解析结果：**
```python
FunctionCallNode(
    name="斐波那契",
    args=[
        BinaryOpNode(
            left=BinaryOpNode(left=IdentifierNode("n"), op="-", right=NumberNode(1)),
            op="+",
            right=FunctionCallNode(name="斐波那契", args=[...])
        )
    ]
)
```

**问题：** 歧义，解析错误

---

### 5.2 修复后

**代码：**
```yan
斐波那契 n 相减 1 相加 斐波那契 n 相减 2
```

**解析结果：**
```python
BinaryOpNode(
    left=FunctionCallNode(
        name="斐波那契",
        args=[BinaryOpNode(left=IdentifierNode("n"), op="-", right=NumberNode(1))]
    ),
    op="+",
    right=FunctionCallNode(
        name="斐波那契",
        args=[BinaryOpNode(left=IdentifierNode("n"), op="-", right=NumberNode(2))]
    )
)
```

**正确：** 无歧义，符合预期

---

## 六、关键优势

1. **无歧义解析**
   - 元数明确参数边界
   - 解决无括号函数调用的根本问题

2. **灵活支持可变参数**
   - 支持固定、可变、最小、范围四种元数类型
   - 适应中文编程的特殊需求

3. **符合中文习惯**
   - 无需括号
   - 无需特殊分隔符
   - 自然流畅

4. **可扩展**
   - 支持用户定义函数
   - 支持元数声明
   - 支持元数推断

---

## 七、风险与缓解

### 7.1 技术风险

**风险1：解析器重构影响现有功能**
- **缓解：** 分阶段实施，每阶段运行完整测试

**风险2：用户定义函数的元数推断不准确**
- **缓解：** 提供元数声明语法，允许用户显式声明

**风险3：性能下降**
- **缓解：** 优化 VerbRegistry 查询，使用字典缓存

### 7.2 兼容性风险

**风险：破坏现有代码**
- **缓解：**
  - 保持向后兼容
  - 未注册的动词使用默认元数
  - 提供迁移指南

---

## 八、测试计划

### 8.1 单元测试

- `test_arity.py` - 元数系统测试
- `test_verb_registry.py` - 动词注册表测试
- `test_parser_arity.py` - 解析器元数驱动测试

### 8.2 集成测试

- 递归函数测试
- 可变参数函数测试
- 操作符动词测试
- 用户定义函数测试

### 8.3 回归测试

- 运行现有测试套件
- 确保测试通过率 > 95%

---

## 九、总结

元数驱动解析是解决无括号函数调用歧义问题的**最佳方案**：

1. **学习 newlisp/yan 的成功经验**
2. **支持中文编程的特殊需求**（可变参数）
3. **分阶段实施，风险可控**
4. **测试驱动，确保质量**

**预计时间：** 8天
**预期结果：** 测试通过率 99%+，无歧义解析

---

**文档版本：** v1.0
**最后更新：** 2026-05-27
