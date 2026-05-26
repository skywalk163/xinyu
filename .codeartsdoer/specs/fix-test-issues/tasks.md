# 编码任务文档

## 文档信息
- **特性名称**: fix-test-issues
- **创建日期**: 2026-05-25
- **版本**: 1.0
- **状态**: 待执行
- **关联文档**: spec.md v1.0, design.md v1.0

## 任务概述

本文档定义了修复测试问题的详细实施任务，共4个主任务，11个子任务。所有任务按照编译器流水线顺序组织，确保前置依赖完成后才执行后续任务。

**任务统计**:
- 主任务: 4个
- 子任务: 11个
- 覆盖需求: 9个（REQ-001 至 REQ-009）

---

## 任务 1: 词法分析器修复

**任务描述**: 修复词法分析器中中文操作符识别问题，确保"加"、"减"、"乘"、"除"等中文操作符被正确识别为对应的TokenType，而非IDENTIFIER。

**优先级**: 高
**预估工时**: 2小时
**关联需求**: REQ-001, REQ-002
**输入**: 源代码字符串，包含中文操作符
**输出**: 正确的Token序列，中文操作符识别为对应TokenType

### 子任务 1.1: 分析现有 _read_chinese 方法逻辑

**任务描述**:
深入分析 `src/lexer/lexer.py` 中 `_read_chinese()` 方法（第199-286行）的现有逻辑，识别导致中文操作符被错误识别为标识符的根本原因。

**执行步骤**:
1. 阅读 `_read_chinese()` 方法完整代码
2. 理解操作符匹配逻辑（第223-263行）
3. 分析上下文判断条件 `prev_is_declaration`、`prev_is_operand`、`next_is_operand`
4. 使用调试或日志追踪测试用例 "3 加 5" 的词法分析过程
5. 定位问题：为何"加"被识别为IDENTIFIER而非PLUS

**验收标准**:
- [ ] 完成问题根因分析文档（可注释形式）
- [ ] 明确指出需要修改的代码行号和逻辑
- [ ] 理解现有逻辑的设计意图

**代码生成提示**:
```
分析 src/lexer/lexer.py 的 _read_chinese 方法，重点关注：
- 第223-263行的操作符匹配和上下文判断逻辑
- prev_is_declaration、prev_is_operand、next_is_operand 的判断条件
- 为何在表达式 "3 加 5" 中，"加" 没有被识别为操作符
```

---

### 子任务 1.2: 修改操作符识别的上下文判断逻辑

**任务描述**:
根据分析结果，修改 `_read_chinese()` 方法中的上下文判断逻辑，确保中文操作符在表达式上下文中被正确识别。

**执行步骤**:
1. 定位第233-263行的操作符上下文判断代码块
2. 调整 `prev_is_declaration` 的判断逻辑，避免过度限制操作符识别
3. 简化操作符识别条件：当前后有操作数上下文时，优先识别为操作符
4. 保留变量声明场景下的标识符识别逻辑
5. 添加必要的注释说明修改原因

**验收标准**:
- [ ] 中文操作符"加"在表达式"3 加 5"中被识别为TokenType.PLUS
- [ ] 中文操作符"减"、"乘"、"除"同样被正确识别
- [ ] 变量声明"定 加 为 5"中，"加"仍被识别为IDENTIFIER
- [ ] 不影响其他现有词法分析测试

**代码生成提示**:
```
修改 src/lexer/lexer.py 的 _read_chinese 方法（第233-263行）：

原逻辑问题：
if prev_is_declaration:
    pass  # 继续作为标识符处理
elif prev_is_operand or next_is_operand:
    # 识别为操作符

修改方案：
- 调整 prev_is_declaration 的判断，仅在真正的声明关键字后跳过操作符识别
- 优化操作符识别条件，确保在表达式上下文中正确识别
- 保持向后兼容，不影响现有功能

关键修改点：
1. 检查 prev_is_declaration 的设置逻辑（第244-245行）
2. 调整第256-263行的条件判断
3. 添加注释说明修改原因
```

---

### 子任务 1.3: 运行词法分析器测试验证修复

**任务描述**:
运行词法分析器相关测试，验证修复是否正确，确保没有引入回归问题。

**执行步骤**:
1. 运行测试：`pytest tests/test_lexer.py::test_lexer_chinese_operators -v`
2. 检查测试输出，确认所有断言通过
3. 运行完整的词法分析器测试套件：`pytest tests/test_lexer.py -v`
4. 分析任何失败的测试，判断是否由本次修改引起
5. 如有回归问题，调整修改并重新测试

**验收标准**:
- [ ] test_lexer_chinese_operators 测试通过
- [ ] 所有现有词法分析器测试通过
- [ ] 无回归问题

**代码生成提示**:
```
执行测试命令：
pytest tests/test_lexer.py::test_lexer_chinese_operators -v
pytest tests/test_lexer.py -v

验证点：
- "加"、"减"、"乘"、"除" 被识别为对应TokenType
- 其他词法分析测试不受影响
```

---

## 任务 2: 语法分析器修复

**任务描述**: 修复语法分析器中一元操作符"非"的解析问题和多分号处理问题，确保正确生成AST结构。

**优先级**: 高
**预估工时**: 2.5小时
**关联需求**: REQ-003, REQ-004
**依赖**: 任务1完成
**输入**: Token序列，包含"非"操作符或多分号
**输出**: 正确的AST，UnaryOpNode或正确解析的语句序列

### 子任务 2.1: 在 _parse_unary 方法中添加"非"操作符处理

**任务描述**:
修改 `src/parser/parser.py` 中的 `_parse_unary()` 方法，添加对中文一元操作符"非"的识别和处理逻辑。

**执行步骤**:
1. 定位 `_parse_unary()` 方法（第295-317行）
2. 在现有 NOT 和 MINUS 处理逻辑后，添加对"非"的检查
3. 检查当前token是否为IDENTIFIER类型且value为"非"
4. 如果匹配，前进token并递归解析操作数
5. 构造 UnaryOpNode，operator设为"not"

**验收标准**:
- [ ] 表达式"非 x"被解析为UnaryOpNode(operator="not", operand=IdentifierNode("x"))
- [ ] 不被错误解析为FunctionCallNode
- [ ] 支持嵌套一元操作符（如"非 非 x"）
- [ ] test_parse_unary_not 测试通过

**代码生成提示**:
```
修改 src/parser/parser.py 的 _parse_unary 方法（第295-317行）：

在现有逻辑后添加：

# 处理中文"非"操作符
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

注意：
- 添加在 MINUS 处理之后，_parse_primary() 调用之前
- 确保正确处理嵌套情况
```

---

### 子任务 2.2: 在语句解析中添加多分号跳过逻辑

**任务描述**:
修改语法分析器的语句解析逻辑，在遇到多个连续分号时正确跳过，而不引发解析错误。

**执行步骤**:
1. 定位语句解析方法（可能是 `_parse_statement()` 或 `_parse_program()`）
2. 在语句解析循环开始处，添加分号跳过逻辑
3. 使用while循环跳过所有连续的SEMICOLON类型token
4. 确保不影响单分号的正常处理
5. 添加注释说明处理逻辑

**验收标准**:
- [ ] 源代码"定 x 为 1;;定 y 为 2"正确解析
- [ ] 多个连续分号不引发解析错误
- [ ] 单分号处理不受影响
- [ ] test_multiple_semicolons 测试通过

**代码生成提示**:
```
修改 src/parser/parser.py 的语句解析方法：

在语句解析循环开始处添加：

def _parse_statement(self) -> ASTNode:
    """解析语句"""
    # 跳过多余的分号
    while self._check(TokenType.SEMICOLON):
        self._advance()

    # 原有语句解析逻辑...

或者修改 _parse_program 方法中的语句循环：

while not self._is_at_end():
    # 跳过空语句（分号）
    while self._check(TokenType.SEMICOLON):
        self._advance()
    if self._is_at_end():
        break

    stmt = self._parse_statement()
    statements.append(stmt)
```

---

### 子任务 2.3: 运行语法分析器测试验证修复

**任务描述**:
运行语法分析器相关测试，验证一元操作符和多分号修复是否正确。

**执行步骤**:
1. 运行测试：`pytest tests/test_parser.py::test_parse_unary_not -v`
2. 运行测试：`pytest tests/test_parser.py::test_multiple_semicolons -v`
3. 运行完整的语法分析器测试套件：`pytest tests/test_parser.py -v`
4. 检查是否有回归问题
5. 如有问题，调整并重新测试

**验收标准**:
- [ ] test_parse_unary_not 测试通过
- [ ] test_multiple_semicolons 测试通过
- [ ] 所有现有语法分析器测试通过
- [ ] 无回归问题

**代码生成提示**:
```
执行测试命令：
pytest tests/test_parser.py::test_parse_unary_not -v
pytest tests/test_parser.py::test_multiple_semicolons -v
pytest tests/test_parser.py -v

验证点：
- "非 x" 正确解析为 UnaryOpNode
- 多分号情况正确处理
- 其他语法分析测试不受影响
```

---

## 任务 3: 语义分析器修复

**任务描述**: 为语义分析器添加错误检测方法，使其能够正确报告语义分析过程中的错误。

**优先级**: 高
**预估工时**: 1小时
**关联需求**: REQ-005, REQ-006
**依赖**: 任务2完成
**输入**: AST，包含语义错误（如未定义变量）
**输出**: 错误检测结果，has_errors()返回True

### 子任务 3.1: 在 SemanticAnalyzer 类中添加 has_errors 方法

**任务描述**:
修改 `src/semantic/analyzer.py` 中的 `SemanticAnalyzer` 类，添加错误检测相关方法。

**执行步骤**:
1. 打开 `src/semantic/analyzer.py`
2. 定位 `SemanticAnalyzer` 类定义
3. 确认 `self.errors` 列表已在 `__init__` 中初始化（第67行）
4. 在类中添加 `has_errors()` 方法，返回 `len(self.errors) > 0`
5. 可选：添加 `error_count()` 和 `get_errors()` 方法
6. 添加方法文档字符串

**验收标准**:
- [ ] SemanticAnalyzer 类包含 has_errors() 方法
- [ ] has_errors() 返回布尔值
- [ ] 有错误时返回True，无错误时返回False
- [ ] test_undefined_variable_in_expression 测试通过

**代码生成提示**:
```
修改 src/semantic/analyzer.py 的 SemanticAnalyzer 类：

在类中添加以下方法（建议在 __init__ 方法之后）：

def has_errors(self) -> bool:
    """
    检查语义分析过程中是否检测到错误

    Returns:
        bool: True表示存在错误，False表示无错误
    """
    return len(self.errors) > 0

def error_count(self) -> int:
    """
    返回错误数量

    Returns:
        int: 错误数量
    """
    return len(self.errors)

def get_errors(self) -> List[SemanticError]:
    """
    返回所有错误列表

    Returns:
        List[SemanticError]: 错误列表
    """
    return self.errors

注意：
- self.errors 已在 __init__ 中初始化为空列表
- 方法应添加适当的文档字符串
```

---

### 子任务 3.2: 运行语义分析器测试验证修复

**任务描述**:
运行语义分析器相关测试，验证错误检测方法是否正确工作。

**执行步骤**:
1. 运行测试：`pytest tests/test_semantic.py::test_undefined_variable_in_expression -v`
2. 运行完整的语义分析器测试套件：`pytest tests/test_semantic.py -v`
3. 检查测试输出，确认has_errors方法正确工作
4. 验证错误收集和报告机制
5. 如有问题，调整并重新测试

**验收标准**:
- [ ] test_undefined_variable_in_expression 测试通过
- [ ] has_errors() 在检测到未定义变量时返回True
- [ ] 所有现有语义分析器测试通过
- [ ] 无回归问题

**代码生成提示**:
```
执行测试命令：
pytest tests/test_semantic.py::test_undefined_variable_in_expression -v
pytest tests/test_semantic.py -v

验证点：
- has_errors() 方法存在且正确工作
- 未定义变量被正确检测
- 错误信息包含位置和建议
```

---

## 任务 4: 宏展开器修复

**任务描述**: 修复宏展开器中的宏调用识别、参数映射和AST节点生成问题，确保所有宏展开测试通过。

**优先级**: 高
**预估工时**: 3小时
**关联需求**: REQ-007, REQ-008, REQ-009
**依赖**: 任务3完成
**输入**: AST，包含宏调用
**输出**: 正确展开的AST，节点类型正确

### 子任务 4.1: 分析宏展开器现有逻辑和测试失败原因

**任务描述**:
深入分析 `src/macro/macro_expander.py` 的现有逻辑，运行失败的宏展开测试，定位问题根因。

**执行步骤**:
1. 运行宏展开测试：`pytest tests/test_macro.py -v`，记录失败的测试
2. 运行详细测试：`pytest tests/test_macro_expander_detailed.py -v`
3. 阅读 `_expand_macro_call()` 方法代码
4. 分析宏调用识别逻辑（第59-71行）
5. 追踪失败测试用例的执行流程，定位问题

**验收标准**:
- [ ] 明确识别6个失败测试的具体失败原因
- [ ] 定位需要修改的代码位置
- [ ] 理解宏展开的完整流程

**代码生成提示**:
```
分析步骤：
1. 运行测试并记录失败信息：
   pytest tests/test_macro.py -v
   pytest tests/test_macro_expander_detailed.py -v

2. 阅读关键方法：
   - src/macro/macro_expander.py 的 _expand_macro_call 方法
   - expand_ast 方法中的宏调用识别逻辑（第59-71行）

3. 分析问题：
   - 宏调用是否被正确识别？
   - 参数映射是否正确？
   - 展开后的AST节点类型是否正确？

4. 记录问题清单，准备修复
```

---

### 子任务 4.2: 修复宏调用识别和参数映射逻辑

**任务描述**:
根据分析结果，修复宏展开器中的宏调用识别和参数映射逻辑。

**执行步骤**:
1. 检查宏调用识别条件：`self.macro_system.has(node.name)`
2. 确保宏名匹配逻辑正确（考虑大小写、别名等）
3. 检查参数映射逻辑，确保位置参数按顺序绑定
4. 处理参数数量验证和默认参数
5. 添加必要的调试日志或注释

**验收标准**:
- [ ] 宏调用被正确识别
- [ ] 参数按正确顺序映射
- [ ] 参数数量验证正确
- [ ] 默认参数处理正确

**代码生成提示**:
```
修改 src/macro/macro_expander.py：

关键修改点：

1. 宏调用识别（第59-71行）：
   - 确保 self.macro_system.has(node.name) 正确判断
   - 检查宏名匹配逻辑

2. 参数映射（_expand_macro_call 方法）：
   - 获取宏定义：macro = self.macro_system.get(node.name)
   - 检查参数数量：len(node.args) vs macro.param_count
   - 按顺序绑定参数
   - 处理默认参数

3. 添加验证逻辑：
   def _validate_params(self, macro, args):
       """验证参数数量和类型"""
       # 实现参数验证
       pass

注意：
- 保持向后兼容
- 添加适当的错误处理
- 记录修改原因
```

---

### 子任务 4.3: 修复AST节点类型生成和验证

**任务描述**:
确保宏展开后生成的AST节点类型正确，添加节点类型验证逻辑。

**执行步骤**:
1. 检查宏展开函数的返回值类型
2. 确保返回的AST节点类型与预期一致
3. 添加AST节点类型验证方法
4. 在展开后验证节点类型
5. 处理展开结果为列表的情况

**验收标准**:
- [ ] 展开后的AST节点类型正确
- [ ] 节点属性完整且正确
- [ ] 列表类型的展开结果正确处理
- [ ] 节点类型验证逻辑有效

**代码生成提示**:
```
修改 src/macro/macro_expander.py：

添加节点类型验证：

def _validate_expanded_ast(self, node: ASTNode) -> bool:
    """
    验证展开后的AST节点类型是否正确

    Args:
        node: 展开后的AST节点

    Returns:
        bool: 是否为有效的AST节点
    """
    from src.parser.ast_nodes import ASTNode

    if node is None:
        return False

    # 检查是否为有效的AST节点类型
    valid_types = (
        ProgramNode, NumberNode, StringNode, IdentifierNode,
        BinaryOpNode, UnaryOpNode, ListNode, DictNode,
        MemberAccessNode, IndexNode, AssignNode, VarDefNode,
        IfNode, ForNode, WhileNode, RepeatNode,
        FunctionDefNode, FunctionCallNode, ReturnNode,
        BlockNode
    )

    return isinstance(node, valid_types)

在 _expand_macro_call 方法中调用验证：
expanded = macro.expand(args)
if not self._validate_expanded_ast(expanded):
    raise ValueError(f"宏展开结果类型无效: {type(expanded)}")
```

---

### 子任务 4.4: 运行宏展开测试验证修复

**任务描述**:
运行所有宏展开相关测试，验证修复是否完全解决了问题。

**执行步骤**:
1. 运行测试：`pytest tests/test_macro.py -v`
2. 运行测试：`pytest tests/test_macro_expander_detailed.py -v`
3. 检查所有6个失败测试是否现在通过
4. 分析任何仍然失败的测试
5. 如有必要，进一步调整并重新测试

**验收标准**:
- [ ] 所有宏展开测试通过（6个测试）
- [ ] test_macro.py 中所有测试通过
- [ ] test_macro_expander_detailed.py 中所有测试通过
- [ ] 无回归问题

**代码生成提示**:
```
执行测试命令：
pytest tests/test_macro.py -v
pytest tests/test_macro_expander_detailed.py -v

验证点：
- 所有宏展开测试通过
- 宏调用正确识别
- 参数映射正确
- AST节点类型正确
```

---

## 任务 5: 集成测试和验证

**任务描述**: 运行完整的测试套件，验证所有修复工作正确完成，确保没有引入回归问题。

**优先级**: 高
**预估工时**: 1小时
**关联需求**: 所有需求（REQ-001 至 REQ-009）
**依赖**: 任务1-4全部完成
**输入**: 完整的测试套件
**输出**: 所有测试通过的确认

### 子任务 5.1: 运行完整测试套件

**任务描述**:
运行项目的完整测试套件，确保所有测试通过，没有引入任何回归问题。

**执行步骤**:
1. 运行所有测试：`pytest tests/ -v`
2. 检查测试摘要，确认所有测试通过
3. 如有失败测试，分析失败原因
4. 判断是否由本次修复引起
5. 如有问题，返回相应任务进行修复

**验收标准**:
- [ ] 所有测试通过
- [ ] 无回归问题
- [ ] 测试覆盖率未降低

**代码生成提示**:
```
执行完整测试：
pytest tests/ -v --tb=short

检查点：
- 测试总数和通过数
- 任何失败的测试
- 测试覆盖率报告（如有）

如有失败：
- 分析失败原因
- 判断是否为回归问题
- 返回相应任务修复
```

---

### 子任务 5.2: 代码审查和文档更新

**任务描述**:
对修改的代码进行最终审查，确保代码质量，更新必要的文档。

**执行步骤**:
1. 审查所有修改的代码文件
2. 检查代码风格一致性
3. 确认注释和文档字符串完整
4. 更新CHANGELOG或版本记录（如有）
5. 准备提交信息

**验收标准**:
- [ ] 代码风格一致
- [ ] 注释清晰完整
- [ ] 文档字符串规范
- [ ] 准备好提交

**代码生成提示**:
```
审查清单：
1. src/lexer/lexer.py - _read_chinese 方法修改
2. src/parser/parser.py - _parse_unary 和语句解析修改
3. src/semantic/analyzer.py - has_errors 方法添加
4. src/macro/macro_expander.py - 宏展开逻辑修改

检查点：
- 代码风格符合PEP8
- 注释说明修改原因
- 文档字符串完整
- 无调试代码残留
```

---

## 任务依赖关系图

```
任务1: 词法分析器修复
  ├─ 子任务1.1: 分析现有逻辑
  ├─ 子任务1.2: 修改上下文判断 ──→ 依赖 1.1
  └─ 子任务1.3: 运行测试验证 ──→ 依赖 1.2

任务2: 语法分析器修复 ──→ 依赖 任务1
  ├─ 子任务2.1: 添加"非"操作符处理
  ├─ 子任务2.2: 添加多分号跳过
  └─ 子任务2.3: 运行测试验证 ──→ 依赖 2.1, 2.2

任务3: 语义分析器修复 ──→ 依赖 任务2
  ├─ 子任务3.1: 添加has_errors方法
  └─ 子任务3.2: 运行测试验证 ──→ 依赖 3.1

任务4: 宏展开器修复 ──→ 依赖 任务3
  ├─ 子任务4.1: 分析现有逻辑
  ├─ 子任务4.2: 修复宏调用识别 ──→ 依赖 4.1
  ├─ 子任务4.3: 修复AST节点生成 ──→ 依赖 4.2
  └─ 子任务4.4: 运行测试验证 ──→ 依赖 4.3

任务5: 集成测试和验证 ──→ 依赖 任务1-4
  ├─ 子任务5.1: 运行完整测试套件
  └─ 子任务5.2: 代码审查和文档更新 ──→ 依赖 5.1
```

---

## 执行建议

### 执行顺序
严格按照任务编号顺序执行（1→2→3→4→5），确保前置依赖完成后再执行后续任务。

### 测试策略
- 每个子任务完成后立即运行相关测试
- 发现问题及时修复，避免问题累积
- 保持代码可提交状态

### 回滚策略
如遇到无法解决的问题：
1. 使用git保存当前进度
2. 回滚到上一个稳定状态
3. 重新分析问题
4. 调整修复方案

### 完成标准
- 所有测试通过
- 代码审查完成
- 文档更新完成
- 准备好提交到版本控制系统

---

## 变更历史

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|----------|
| 1.0 | 2026-05-25 | - | 初始版本 |
