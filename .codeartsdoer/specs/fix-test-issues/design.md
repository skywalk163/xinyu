# 技术设计文档

## 文档信息
- **特性名称**: fix-test-issues
- **创建日期**: 2026-05-25
- **版本**: 1.0
- **状态**: 草稿
- **关联需求文档**: spec.md v1.0

## 1. 设计概述

### 1.1 设计目标
本设计旨在修复中文编程语言编译器中的四个核心模块测试失败问题，通过最小化修改实现功能正确性：
- 确保词法分析器正确识别中文操作符（加、减、乘、除等）
- 确保语法分析器正确解析一元操作符"非"和处理多分号情况
- 确保语义分析器提供完整的错误检测接口
- 确保宏展开器正确识别和展开宏调用

### 1.2 设计原则
- **最小修改原则**: 仅修改必要的代码，避免大规模重构
- **向后兼容**: 保持现有功能和API不变
- **单一职责**: 每个修复点聚焦单一问题
- **可测试性**: 所有修改必须通过现有测试用例

### 1.3 技术栈
- **语言**: Python 3.x
- **测试框架**: pytest
- **核心模块**:
  - 词法分析器 (src/lexer/lexer.py)
  - 语法分析器 (src/parser/parser.py)
  - 语义分析器 (src/semantic/analyzer.py)
  - 宏展开器 (src/macro/macro_expander.py)

## 2. 架构设计

### 2.1 整体架构
修复工作遵循编译器流水线架构，按模块优先级顺序进行修复：

#### 架构图
```
┌─────────────────────────────────────────────────────────────┐
│                    编译器流水线                               │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  词法分析器      │ ← 修复点1: 中文操作符识别
│  (Lexer)        │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  语法分析器      │ ← 修复点2: 一元操作符 + 多分号
│  (Parser)       │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  语义分析器      │ ← 修复点3: has_errors方法
│  (Analyzer)     │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  宏展开器        │ ← 修复点4: 宏调用识别与展开
│  (Expander)     │
└─────────────────┘
```

### 2.2 模块划分

| 模块名称 | 职责描述 | 关键接口 |
|----------|----------|----------|
| Lexer | 词法分析，将源代码转换为Token序列 | `_read_chinese()`, `_is_chinese()` |
| Parser | 语法分析，将Token序列转换为AST | `_parse_unary()`, `_parse_statement()` |
| SemanticAnalyzer | 语义分析，进行类型检查和作用域分析 | `has_errors()`, `analyze()` |
| MacroExpander | 宏展开，替换宏调用为具体AST | `_expand_macro_call()`, `expand_ast()` |

### 2.3 组件交互
- **Lexer → Parser**: Token序列传递
- **Parser → SemanticAnalyzer**: AST传递
- **SemanticAnalyzer → MacroExpander**: 语义分析后的AST传递
- **MacroExpander**: 独立处理宏展开

## 3. 详细设计

### 3.1 词法分析器修复设计

#### 3.1.1 问题分析
当前 `_read_chinese` 方法在识别中文操作符时存在上下文判断逻辑缺陷：
- 操作符"加"被错误识别为标识符
- 原因：上下文判断条件过于严格，导致操作符被当作标识符处理

#### 3.1.2 修复方案设计
**修改文件**: `src/lexer/lexer.py`
**修改方法**: `_read_chinese()` (第199-286行)

**修复策略**:
```
读取中文字符序列
    ↓
优先匹配内置函数（保持现有逻辑）
    ↓
使用最长匹配原则匹配操作符
    ↓
【关键修改】调整上下文判断逻辑：
  - 移除过于严格的 prev_is_declaration 检查限制
  - 简化操作符识别条件：只要前后有操作数上下文，即识别为操作符
  - 特殊处理：变量声明后的中文序列应为标识符
    ↓
若非操作符，读取完整标识符
    ↓
检查是否为关键字
    ↓
返回对应Token
```

#### 3.1.3 接口定义
```python
# 保持现有接口不变
def _read_chinese(self) -> None:
    """
    读取中文（关键字、操作符或标识符）

    修改点：
    - 调整操作符识别的上下文判断逻辑
    - 确保中文操作符（加、减、乘、除）被正确识别为TokenType
    """
    pass
```

#### 3.1.4 关键修改点
1. **第233-263行**: 操作符上下文判断逻辑
   - 问题：`prev_is_declaration` 条件导致操作符被跳过
   - 修复：调整条件判断，确保操作符在表达式上下文中被正确识别

### 3.2 语法分析器修复设计

#### 3.2.1 一元操作符"非"修复

**修改文件**: `src/parser/parser.py`
**修改方法**: `_parse_unary()` (第295-317行)

**问题分析**:
- 当前仅处理 `TokenType.NOT` 和 `TokenType.MINUS`
- 中文"非"操作符可能被识别为其他Token类型或标识符

**修复方案**:
```python
def _parse_unary(self) -> ASTNode:
    """解析一元操作（not, -, 非）"""

    # 处理 NOT 操作符
    if self._check(TokenType.NOT):
        # 现有逻辑...

    # 处理减号
    if self._check(TokenType.MINUS):
        # 现有逻辑...

    # 【新增】处理中文"非"操作符
    # 检查当前token是否为标识符"非"
    if self._check(TokenType.IDENTIFIER):
        token = self._current_token()
        if token.value == "非":
            self._advance()
            operand = self._parse_unary()
            return UnaryOpNode(
                line=token.line,
                column=token.column,
                operator="not",
                operand=operand
            )

    return self._parse_primary()
```

#### 3.2.2 多分号处理修复

**修改文件**: `src/parser/parser.py`
**修改方法**: `_parse_statement()` 或相关语句解析方法

**修复方案**:
```
方案A（推荐）：在语法分析器中跳过多余分号
  - 在语句解析循环中，遇到SEMICOLON类型token时跳过
  - 不影响词法分析器逻辑

方案B：在词法分析器中允许多分号
  - 修改分号处理逻辑，允许多个连续分号
  - 风险：可能影响其他语法元素识别
```

**推荐实现**:
```python
def _parse_statement(self) -> ASTNode:
    """解析语句"""
    # 跳过多余的分号
    while self._check(TokenType.SEMICOLON):
        self._advance()

    # 原有语句解析逻辑...
```

### 3.3 语义分析器修复设计

#### 3.3.1 has_errors 方法补全

**修改文件**: `src/semantic/analyzer.py`
**修改类**: `SemanticAnalyzer`

**修复方案**:
```python
class SemanticAnalyzer:
    """语义分析器类"""

    def __init__(self):
        # 现有初始化逻辑...
        self.errors: List[SemanticError] = []

    # 【新增方法】
    def has_errors(self) -> bool:
        """
        检查语义分析过程中是否检测到错误

        Returns:
            bool: True表示存在错误，False表示无错误
        """
        return len(self.errors) > 0

    # 【可选】获取错误数量
    def error_count(self) -> int:
        """返回错误数量"""
        return len(self.errors)

    # 【可选】获取所有错误
    def get_errors(self) -> List[SemanticError]:
        """返回所有错误列表"""
        return self.errors
```

#### 3.3.2 接口定义
```python
class SemanticAnalyzer:
    def has_errors(self) -> bool:
        """检查是否存在语义错误"""
        pass

    def error_count(self) -> int:
        """返回错误数量"""
        pass

    def get_errors(self) -> List[SemanticError]:
        """返回所有错误"""
        pass
```

### 3.4 宏展开器修复设计

#### 3.4.1 问题分析
根据测试失败情况，宏展开器存在以下问题：
- 宏调用识别不准确
- 参数映射逻辑错误
- 展开后的AST节点类型不正确

#### 3.4.2 修复方案设计

**修改文件**: `src/macro/macro_expander.py`
**关键方法**: `_expand_macro_call()`, `expand_ast()`

**修复策略**:
```
1. 宏调用识别
   ↓
   检查 FunctionCallNode.name 是否在宏系统中注册
   ↓
2. 参数映射
   ↓
   按宏定义的参数顺序绑定实际参数
   处理位置参数和关键字参数
   ↓
3. AST节点生成
   ↓
   调用宏的展开函数
   确保返回正确的AST节点类型
   ↓
4. 递归展开
   ↓
   对展开结果继续进行宏展开（处理嵌套宏）
```

#### 3.4.3 接口定义
```python
class MacroExpander:
    def _expand_macro_call(self, node: FunctionCallNode) -> ASTNode:
        """
        展开宏调用

        Args:
            node: 函数调用节点

        Returns:
            展开后的AST节点

        修复点：
        - 正确获取宏定义
        - 准确映射参数
        - 确保返回正确的AST类型
        """
        pass

    def _validate_expanded_ast(self, node: ASTNode) -> bool:
        """
        验证展开后的AST节点类型是否正确

        Args:
            node: 展开后的AST节点

        Returns:
            bool: 是否为有效的AST节点
        """
        pass
```

#### 3.4.4 关键修改点
1. **宏调用识别** (第59-71行)
   - 确保 `self.macro_system.has(node.name)` 正确判断
   - 处理宏名的大小写和别名

2. **参数映射**
   - 检查参数数量是否匹配
   - 正确处理位置参数和默认参数

3. **AST节点类型验证**
   - 展开后验证节点类型
   - 确保节点属性完整

## 4. 数据设计

### 4.1 数据模型
本次修复不涉及数据模型变更，使用现有的数据结构：

#### Token类型定义
```python
class TokenType(Enum):
    # 操作符
    PLUS = auto()        # 加
    MINUS = auto()       # 减
    MULTIPLY = auto()    # 乘
    DIVIDE = auto()      # 除
    NOT = auto()         # 非

    # 其他类型...
    IDENTIFIER = auto()
    SEMICOLON = auto()
```

#### AST节点类型
```python
class UnaryOpNode(ASTNode):
    operator: str      # "not", "-"
    operand: ASTNode

class FunctionCallNode(ASTNode):
    name: str
    args: List[ASTNode]
```

### 4.2 错误数据结构
```python
class SemanticError(Exception):
    message: str
    line: int
    column: int
    suggestion: Optional[str]
```

## 5. API 设计

### 5.1 内部 API
本次修复保持所有现有API不变，仅新增以下方法：

| 类 | 方法 | 签名 | 说明 |
|----|------|------|------|
| SemanticAnalyzer | has_errors | `def has_errors(self) -> bool` | 检查是否存在错误 |
| SemanticAnalyzer | error_count | `def error_count(self) -> int` | 获取错误数量 |
| SemanticAnalyzer | get_errors | `def get_errors(self) -> List[SemanticError]` | 获取所有错误 |

### 5.2 API 使用示例
```python
# 语义分析器使用示例
analyzer = SemanticAnalyzer()
analyzer.analyze(ast)

if analyzer.has_errors():
    print(f"发现 {analyzer.error_count()} 个错误:")
    for error in analyzer.get_errors():
        print(f"  - {error}")
```

## 6. 流程设计

### 6.1 词法分析修复流程

#### 流程图
```
开始读取中文字符
    ↓
尝试匹配内置函数
    ├─ 匹配成功 → 返回 IDENTIFIER Token
    └─ 匹配失败 → 继续
    ↓
尝试最长匹配操作符
    ├─ 找到操作符匹配
    │   ↓
    │   检查上下文
    │   ├─ 前面是声明关键字 → 作为标识符处理
    │   └─ 前后是操作数上下文 → 返回操作符Token
    └─ 未找到 → 继续
    ↓
读取完整标识符
    ↓
检查是否为关键字
    ├─ 是关键字 → 返回关键字Token
    └─ 不是 → 返回标识符Token
    ↓
结束
```

### 6.2 宏展开修复流程

#### 流程图
```
遇到 FunctionCallNode
    ↓
检查是否为宏调用
    ├─ 不是宏 → 递归展开参数，返回 FunctionCallNode
    └─ 是宏 → 继续
    ↓
获取宏定义
    ↓
参数映射
    ├─ 检查参数数量
    ├─ 绑定位置参数
    └─ 处理默认参数
    ↓
调用宏展开函数
    ↓
验证AST节点类型
    ├─ 类型正确 → 继续
    └─ 类型错误 → 抛出异常
    ↓
递归展开结果
    ↓
返回展开后的AST
```

### 6.3 异常处理流程
```
检测到错误
    ↓
创建错误对象（包含位置信息和建议）
    ↓
添加到 errors 列表
    ↓
继续分析（不中断）
    ↓
分析完成后
    ↓
用户调用 has_errors() 检查
    ↓
根据需要获取错误详情
```

## 7. 技术决策

### 7.1 关键决策记录

| 决策项 | 选项 | 最终决策 | 决策理由 |
|--------|------|----------|----------|
| 操作符识别策略 | 上下文判断 / 优先级表 | 上下文判断（优化） | 保持现有架构，仅调整判断条件 |
| 多分号处理位置 | 词法层 / 语法层 | 语法层 | 影响范围更小，易于测试 |
| has_errors 返回类型 | bool / int | bool | 符合常见API设计，int可通过error_count获取 |
| 宏展开验证时机 | 展开后 / 展开中 | 展开后 | 避免影响展开性能 |
| 修复顺序 | 按模块优先级 / 按测试顺序 | 按模块优先级 | 词法→语法→语义→宏，符合编译流程 |

### 7.2 技术风险

| 风险项 | 影响程度 | 应对措施 |
|--------|----------|----------|
| 词法分析器修改影响其他Token识别 | 高 | 完整运行所有词法测试，确保无回归 |
| 语法分析器多分号处理影响语句边界 | 中 | 添加边界测试用例 |
| 宏展开递归深度过大 | 中 | 保持现有的max_depth限制（100） |
| 修复引入新的边界情况bug | 中 | 增加边界测试用例，代码审查 |

## 8. 性能设计

### 8.1 性能目标
- 词法分析时间复杂度：O(n)，n为源代码长度
- 语法分析时间复杂度：O(n)
- 宏展开时间复杂度：O(d×n)，d为展开深度
- 内存占用：不显著增加

### 8.2 优化策略
- **词法分析**: 使用最长匹配原则，减少回溯
- **语法分析**: 预读token数量最小化
- **宏展开**: 设置深度限制，避免无限递归
- **错误收集**: 使用列表追加，O(1)操作

## 9. 安全设计

### 9.1 安全措施
本次修复不涉及安全敏感操作，但需注意：
- 宏查所有用户输入处理路径
- 确保错误信息不泄露敏感信息
- 宏展开深度限制防止DoS攻击

### 9.2 错误处理
- 所有异常应包含位置信息，便于定位
- 错误消息应清晰、友好
- 提供修复建议（suggestion字段）

## 10. 测试设计

### 10.1 测试策略
- **单元测试**: 针对每个修复点编写独立测试
- **回归测试**: 运行所有现有测试，确保无破坏
- **边界测试**: 测试边界情况和异常输入
- **集成测试**: 测试完整的编译流程

### 10.2 测试场景

| 测试场景 | 测试文件 | 预期结果 |
|----------|----------|----------|
| 中文操作符识别 | test_lexer.py::test_lexer_chinese_operators | 所有中文操作符正确识别为对应TokenType |
| 一元非操作符解析 | test_parser.py::test_parse_unary_not | "非 x"解析为UnaryOpNode |
| 多分号处理 | test_parser.py::test_multiple_semicolons | 正确解析，不报错 |
| 未定义变量检测 | test_semantic.py::test_undefined_variable_in_expression | has_errors()返回True |
| 宏展开 | test_macro.py (6个测试) | 所有宏展开测试通过 |

### 10.3 测试用例示例
```python
# 词法分析器测试
def test_chinese_operators():
    lexer = Lexer("3 加 5")
    tokens = lexer.tokenize()
    assert tokens[1].type == TokenType.PLUS
    assert tokens[1].value == "加"

# 语法分析器测试
def test_unary_not():
    parser = Parser(lexer.tokenize("非 x"))
    ast = parser.parse()
    assert isinstance(ast, UnaryOpNode)
    assert ast.operator == "not"

# 语义分析器测试
def test_has_errors():
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast_with_undefined_var)
    assert analyzer.has_errors() == True
```

## 11. 部署设计

### 11.1 部署方案
本次修复为代码级修改，无需特殊部署流程：
1. 修改源代码文件
2. 运行测试验证
3. 提交代码变更

### 11.2 配置管理
无需新增配置项，使用现有配置。

## 12. 附录

### 12.1 参考资料
- **源代码文件**:
  - src/lexer/lexer.py (第191-286行: _read_chinese方法)
  - src/parser/parser.py (第295-317行: _parse_unary方法)
  - src/semantic/analyzer.py (SemanticAnalyzer类)
  - src/macro/macro_expander.py (MacroExpander类)

- **测试文件**:
  - tests/test_lexer.py
  - tests/test_parser.py
  - tests/test_semantic.py
  - tests/test_macro.py

- **相关文档**:
  - EARS格式说明: .codeartsdoer/skills/managing-sdd-spec-markdown/ears-format.md
  - 设计原则: .codeartsdoer/skills/managing-sdd-design-markdown/design-principles.md

### 12.2 术语表

| 术语 | 定义 |
|------|------|
| Token | 词法分析产生的最小单元，包含类型(TokenType)和值(value) |
| AST | 抽象语法树，表示源代码的语法结构 |
| 最长匹配原则 | 在词法分析中，优先匹配最长的可能token |
| 上下文判断 | 根据前后token判断当前token的语义 |
| 宏展开 | 将宏调用替换为具体的AST结构 |
| 递归下降解析 | 一种自顶向下的语法分析方法，每个非终结符对应一个解析函数 |

### 12.3 变更历史

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|----------|
| 1.0 | 2026-05-25 | - | 初始版本 |
