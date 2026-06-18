# 任务规划文档

## 文档信息
- **特性名称**: code-structure-optimization-phase2
- **创建日期**: 2025-01-23
- **版本**: 1.0
- **状态**: 草稿
- **关联需求文档**: spec.md v1.0
- **关联设计文档**: design.md v1.0

## 1. 任务概述

### 1.1 任务目标
本任务规划旨在将代码结构优化需求转化为具体的实施任务，包括统一错误处理机制、集成类型推断系统、完善代码文档三个核心部分。

### 1.2 任务统计
- **主任务数量**: 5
- **子任务数量**: 18
- **覆盖需求数量**: 10 (REQ-001 至 REQ-010)

### 1.3 任务依赖关系
```
任务1 (错误处理集成)
├── 任务1.1 (词法分析器)
├── 任务1.2 (语法分析器)
└── 任务1.3 (语义分析器)

任务2 (类型推断集成) [依赖: 任务1.3]
├── 任务2.1 (变量类型推断)
└── 任务2.2 (表达式类型推断)

任务3 (文档字符串添加)
├── 任务3.1 (词法分析器文档)
├── 任务3.2 (语法分析器文档)
├── 任务3.3 (语义分析器文档)
├── 任务3.4 (代码生成器文档)
└── 任务3.5 (宏系统文档)

任务4 (测试验证)
├── 任务4.1 (错误处理测试)
├── 任务4.2 (类型推断测试)
└── 任务4.3 (文档字符串测试)

任务5 (集成验证)
```

## 2. 主任务列表

### 任务1: 统一错误处理机制集成

**任务描述**: 在词法分析器、语法分析器、语义分析器中集成统一的 ErrorHandler，替换现有的异常抛出和错误列表管理方式。

**输入**:
- 现有的 Lexer、Parser、SemanticAnalyzer 类实现
- ErrorHandler 类实现 (src/error_handling.py)
- ErrorType 枚举定义

**输出**:
- 修改后的 Lexer 类，包含 error_handler 属性和 _report_error 方法
- 修改后的 Parser 类，包含 error_handler 属性和 _report_error 方法
- 修改后的 SemanticAnalyzer 类，使用 error_handler 替代 errors 列表

**验收标准**:
- 所有 LexerError 抛出点改为调用 _report_error 方法
- 所有 ParseError 抛出点改为调用 _report_error 方法
- 所有 SemanticError 创建点改为调用 _report_error 方法
- 错误报告包含正确的错误类型、消息、行号、列号
- 错误报告支持可选的建议信息
- has_errors() 和 get_errors() 方法正常工作

**优先级**: 高

**预估工作量**: 4小时

**子任务**:

#### 任务1.1: 词法分析器错误处理集成
**描述**: 在 Lexer 类中集成 ErrorHandler，替换所有 LexerError 异常抛出。

**实施步骤**:
1. 在 Lexer.__init__ 方法中添加 error_handler 参数和初始化
2. 添加 _report_error 私有方法，调用 error_handler.report
3. 查找所有 `raise LexerError` 语句
4. 将每个异常抛出替换为 _report_error 调用
5. 确保错误信息包含行号、列号和建议信息

**代码生成提示**:
```
在 Lexer 类中：
1. 修改 __init__ 方法签名：
   def __init__(self, source: str, error_handler: ErrorHandler = None):
       self.error_handler = error_handler or ErrorHandler()

2. 添加 _report_error 方法：
   def _report_error(self, message: str, line: int, column: int, suggestion: Optional[str] = None):
       self.error_handler.report(ErrorType.LEXER_ERROR, message, line, column, suggestion=suggestion)

3. 替换所有 raise LexerError(...) 为 self._report_error(...)
```

**覆盖需求**: REQ-001

---

#### 任务1.2: 语法分析器错误处理集成
**描述**: 在 Parser 类中集成 ErrorHandler，替换所有 ParseError 异常抛出。

**实施步骤**:
1. 在 Parser.__init__ 方法中添加 error_handler 参数和初始化
2. 添加 _report_error 私有方法，调用 error_handler.report
3. 查找所有 `raise ParseError` 语句
4. 将每个异常抛出替换为 _report_error 调用
5. 确保错误信息包含 Token 的行号、列号和建议信息

**代码生成提示**:
```
在 Parser 类中：
1. 修改 __init__ 方法签名：
   def __init__(self, tokens: List[Token], error_handler: ErrorHandler = None):
       self.error_handler = error_handler or ErrorHandler()

2. 添加 _report_error 方法：
   def _report_error(self, message: str, token: Token, suggestion: Optional[str] = None):
       self.error_handler.report(ErrorType.PARSER_ERROR, message, token.line, token.column, suggestion=suggestion)

3. 替换所有 raise ParseError(...) 为 self._report_error(...)
```

**覆盖需求**: REQ-002

---

#### 任务1.3: 语义分析器错误处理集成
**描述**: 在 SemanticAnalyzer 类中集成 ErrorHandler，替换 errors 列表管理方式。

**实施步骤**:
1. 在 SemanticAnalyzer.__init__ 方法中添加 error_handler 参数，移除 errors 列表
2. 添加 _report_error 私有方法，调用 error_handler.report
3. 查找所有 `self.errors.append` 语句
4. 将每个错误添加替换为 _report_error 调用
5. 修改 has_errors() 方法，调用 error_handler.has_errors()
6. 修改 get_errors() 方法，调用 error_handler.get_errors()

**代码生成提示**:
```
在 SemanticAnalyzer 类中：
1. 修改 __init__ 方法：
   def __init__(self, error_handler: ErrorHandler = None):
       self.error_handler = error_handler or ErrorHandler()
       # 移除 self.errors = []

2. 添加 _report_error 方法：
   def _report_error(self, message: str, line: int, column: int, suggestion: Optional[str] = None):
       self.error_handler.report(ErrorType.SEMANTIC_ERROR, message, line, column, suggestion=suggestion)

3. 替换所有 self.errors.append(...) 为 self._report_error(...)

4. 修改 has_errors() 和 get_errors() 方法：
   def has_errors(self) -> bool:
       return self.error_handler.has_errors()

   def get_errors(self) -> List[Error]:
       return self.error_handler.get_errors()
```

**覆盖需求**: REQ-003

---

### 任务2: 类型推断系统集成

**任务描述**: 在语义分析器中集成 TypeInferencer，为变量定义和表达式提供类型推断功能。

**输入**:
- 修改后的 SemanticAnalyzer 类（已完成任务1.3）
- TypeInferencer 类实现 (src/semantic/type_inference.py)
- AST 节点定义

**输出**:
- 扩展后的 SemanticAnalyzer 类，包含 type_inferencer 属性
- 新增的 _infer_type 和 _build_type_context 方法
- 更新后的符号表，包含类型信息

**验收标准**:
- SemanticAnalyzer 初始化时创建 type_inferencer 实例
- _visit_var_def 方法中使用类型推断器推断变量类型
- _visit_assign 方法中使用类型推断器推断赋值类型
- 类型推断结果正确更新到符号表
- 类型上下文包含当前作用域的变量类型信息

**优先级**: 中

**预估工作量**: 3小时

**依赖**: 任务1.3

**子任务**:

#### 任务2.1: 变量定义类型推断
**描述**: 在 _visit_var_def 方法中集成类型推断，推断变量类型并更新符号表。

**实施步骤**:
1. 在 SemanticAnalyzer.__init__ 中添加 type_inferencer 初始化
2. 添加 _build_type_context 方法，构建当前作用域类型映射
3. 添加 _infer_type 方法，调用 type_inferencer.infer
4. 在 _visit_var_def 中调用类型推断
5. 将推断结果存储到符号表的 value_type 字段

**代码生成提示**:
```
在 SemanticAnalyzer 类中：
1. 修改 __init__ 方法：
   def __init__(self, error_handler: ErrorHandler = None):
       self.error_handler = error_handler or ErrorHandler()
       self.type_inferencer = TypeInferencer()

2. 添加类型推断辅助方法：
   def _build_type_context(self) -> Dict[str, str]:
       context = {}
       scope = self.current_scope
       for name, symbol in scope.symbols.items():
           if symbol.get('value_type'):
               context[name] = symbol['value_type']
       return context

   def _infer_type(self, node: ASTNode, context: Optional[Dict[str, str]] = None) -> str:
       return self.type_inferencer.infer(node, context)

3. 修改 _visit_var_def 方法：
   def _visit_var_def(self, node: VarDefNode):
       # ... 现有逻辑
       if node.initial_value:
           context = self._build_type_context()
           inferred_type = self._infer_type(node.initial_value, context)
           symbol['value_type'] = inferred_type
```

**覆盖需求**: REQ-004

---

#### 任务2.2: 表达式类型推断
**描述**: 在表达式分析方法中集成类型推断，推断表达式类型用于语义检查。

**实施步骤**:
1. 在 _visit_expression 方法中调用类型推断
2. 在二元运算分析中使用类型推断
3. 在一元运算分析中使用类型推断
4. 在函数调用分析中推断返回类型
5. 使用推断的类型进行类型兼容性检查

**代码生成提示**:
```
在 SemanticAnalyzer 类中：
1. 修改 _visit_expression 方法：
   def _visit_expression(self, node: ExpressionNode) -> str:
       context = self._build_type_context()
       inferred_type = self._infer_type(node, context)
       # 使用推断类型进行语义检查
       return inferred_type

2. 在二元运算分析中：
   def _visit_binary_op(self, node: BinaryOpNode) -> str:
       left_type = self._visit_expression(node.left)
       right_type = self._visit_expression(node.right)
       # 使用 TypeInferencer 检查类型兼容性
       result_type = self.type_inferencer.infer_binary_result(node.operator, left_type, right_type)
       return result_type

3. 在函数调用分析中：
   def _visit_function_call(self, node: FunctionCallNode) -> str:
       # ... 参数检查
       return_type = self.type_inferencer.infer_call_return(node.function_name, arg_types)
       return return_type
```

**覆盖需求**: REQ-005

---

### 任务3: 代码文档字符串完善

**任务描述**: 为词法分析器、语法分析器、语义分析器、代码生成器、宏系统的所有公开方法添加符合 PEP 257 规范的文档字符串。

**输入**:
- 现有的 Lexer、Parser、SemanticAnalyzer、CodeGenerator、MacroExpander 类
- PEP 257 文档字符串规范

**输出**:
- 所有公开方法添加完整的文档字符串
- 文档字符串包含功能描述、参数说明、返回值说明

**验收标准**:
- 所有公开方法添加文档字符串
- 文档字符串使用三重双引号格式
- 文档字符串包含功能描述、参数说明、返回值说明
- 文档字符串使用中文，与项目风格一致

**优先级**: 中

**预估工作量**: 3小时

**子任务**:

#### 任务3.1: 词法分析器文档字符串
**描述**: 为 Lexer 类的所有公开方法添加文档字符串。

**实施步骤**:
1. 为 tokenize 方法添加文档字符串
2. 为所有公开方法添加文档字符串
3. 确保格式符合 PEP 257 规范

**代码生成提示**:
```
在 Lexer 类中添加文档字符串：
def tokenize(self) -> List[Token]:
    """将源代码转换为 Token 序列

    对源代码进行词法分析，识别并提取所有的词法单元（Token）。

    Args:
        无（使用初始化时传入的 source）

    Returns:
        List[Token]: Token 序列列表

    Raises:
        无（错误通过 ErrorHandler 报告）

    Example:
        >>> lexer = Lexer("变量 x 为 42")
        >>> tokens = lexer.tokenize()
    """
    pass
```

**覆盖需求**: REQ-006

---

#### 任务3.2: 语法分析器文档字符串
**描述**: 为 Parser 类的所有解析方法添加文档字符串。

**实施步骤**:
1. 为 parse 方法添加文档字符串
2. 为所有 _parse_* 方法添加文档字符串
3. 确保格式符合 PEP 257 规范

**代码生成提示**:
```
在 Parser 类中添加文档字符串：
def parse(self) -> ProgramNode:
    """解析 Token 序列生成抽象语法树

    对 Token 序列进行语法分析，构建完整的抽象语法树（AST）。

    Args:
        无（使用初始化时传入的 tokens）

    Returns:
        ProgramNode: 程序根节点

    Raises:
        无（错误通过 ErrorHandler 报告）
    """
    pass

def _parse_statement(self) -> StatementNode:
    """解析语句

    根据当前 Token 类型选择相应的语句解析方法。

    Args:
        无

    Returns:
        StatementNode: 语句节点

    Raises:
        无（错误通过 ErrorHandler 报告）
    """
    pass
```

**覆盖需求**: REQ-007

---

#### 任务3.3: 语义分析器文档字符串
**描述**: 为 SemanticAnalyzer 类的所有访问方法添加文档字符串。

**实施步骤**:
1. 为 analyze 方法添加文档字符串
2. 为所有 _visit_* 方法添加文档字符串
3. 为新增的 _infer_type 和 _build_type_context 方法添加文档字符串
4. 确保格式符合 PEP 257 规范

**代码生成提示**:
```
在 SemanticAnalyzer 类中添加文档字符串：
def analyze(self, ast: ProgramNode) -> None:
    """分析抽象语法树进行语义检查

    对 AST 进行语义分析，包括符号表构建、类型检查、作用域检查等。

    Args:
        ast: 程序根节点

    Returns:
        无

    Raises:
        无（错误通过 ErrorHandler 报告）
    """
    pass

def _infer_type(self, node: ASTNode, context: Optional[Dict[str, str]] = None) -> str:
    """推断 AST 节点的类型

    使用类型推断器推断给定节点的类型。

    Args:
        node: AST 节点
        context: 类型上下文（变量名到类型的映射）

    Returns:
        str: 推断的类型字符串（如 'number', 'string', 'boolean'）
    """
    pass
```

**覆盖需求**: REQ-008

---

#### 任务3.4: 代码生成器文档字符串
**描述**: 为 CodeGenerator 类的所有生成方法添加文档字符串。

**实施步骤**:
1. 为 generate 方法添加文档字符串
2. 为所有 _generate_* 方法添加文档字符串
3. 确保格式符合 PEP 257 规范

**代码生成提示**:
```
在 CodeGenerator 类中添加文档字符串：
def generate(self, ast: ProgramNode) -> str:
    """生成目标代码

    将抽象语法树转换为目标代码（如 Python 代码）。

    Args:
        ast: 程序根节点

    Returns:
        str: 生成的目标代码字符串
    """
    pass
```

**覆盖需求**: REQ-009

---

#### 任务3.5: 宏系统文档字符串
**描述**: 为 MacroExpander 类和所有宏定义添加文档字符串。

**实施步骤**:
1. 为宏展开器的公开方法添加文档字符串
2. 为内置宏定义添加文档字符串
3. 为习语宏定义添加文档字符串
4. 确保格式符合 PEP 257 规范

**代码生成提示**:
```
在 MacroExpander 类中添加文档字符串：
def expand(self, ast: ProgramNode) -> ProgramNode:
    """展开宏

    递归展开 AST 中的所有宏调用。

    Args:
        ast: 程序根节点

    Returns:
        ProgramNode: 展开后的 AST
    """
    pass

def register_macro(self, name: str, definition: MacroDefinition) -> None:
    """注册宏定义

    将宏定义添加到宏表中。

    Args:
        name: 宏名称
        definition: 宏定义对象
    """
    pass
```

**覆盖需求**: REQ-010

---

### 任务4: 测试验证

**任务描述**: 为所有修改和新增的功能编写测试用例，确保功能正确性和向后兼容性。

**输入**:
- 修改后的 Lexer、Parser、SemanticAnalyzer 类
- 现有的测试框架和测试用例

**输出**:
- 错误处理集成测试用例
- 类型推断集成测试用例
- 文档字符串验证测试用例

**验收标准**:
- 所有测试用例通过
- 测试覆盖所有修改的功能
- 现有测试不受影响（回归测试通过）

**优先级**: 高

**预估工作量**: 3小时

**子任务**:

#### 任务4.1: 错误处理集成测试
**描述**: 测试错误处理集成功能，验证错误报告的正确性。

**实施步骤**:
1. 编写词法错误处理测试用例
2. 编写语法错误处理测试用例
3. 编写语义错误处理测试用例
4. 编写多错误收集测试用例
5. 编写错误建议信息测试用例

**代码生成提示**:
```
测试用例示例：
def test_lexer_error_handling():
    """测试词法分析器错误处理"""
    source = "变量 x 为 @#$"  # 非法字符
    error_handler = ErrorHandler()
    lexer = Lexer(source, error_handler)
    tokens = lexer.tokenize()

    assert error_handler.has_errors()
    errors = error_handler.get_errors()
    assert len(errors) > 0
    assert errors[0].error_type == ErrorType.LEXER_ERROR
    assert errors[0].line > 0
    assert errors[0].column > 0

def test_multiple_errors():
    """测试多错误收集"""
    source = "变量 x 为 @ 变量 y 为 #"
    error_handler = ErrorHandler()
    lexer = Lexer(source, error_handler)
    lexer.tokenize()

    assert error_handler.has_errors()
    errors = error_handler.get_errors()
    assert len(errors) >= 2  # 应该收集所有错误
```

**覆盖需求**: REQ-001, REQ-002, REQ-003

---

#### 任务4.2: 类型推断集成测试
**描述**: 测试类型推断集成功能，验证类型推断的准确性。

**实施步骤**:
1. 编写数字字面量类型推断测试
2. 编写字符串字面量类型推断测试
3. 编写二元运算类型推断测试
4. 编写函数调用类型推断测试
5. 编写变量引用类型推断测试

**代码生成提示**:
```
测试用例示例：
def test_number_type_inference():
    """测试数字类型推断"""
    source = "变量 x 为 42"
    error_handler = ErrorHandler()
    lexer = Lexer(source, error_handler)
    tokens = lexer.tokenize()
    parser = Parser(tokens, error_handler)
    ast = parser.parse()
    analyzer = SemanticAnalyzer(error_handler)
    analyzer.analyze(ast)

    symbol = analyzer.symbol_table.lookup('x')
    assert symbol['value_type'] == 'number'

def test_binary_op_type_inference():
    """测试二元运算类型推断"""
    source = "变量 x 为 1 + 2"
    # ... 分析代码
    symbol = analyzer.symbol_table.lookup('x')
    assert symbol['value_type'] == 'number'
```

**覆盖需求**: REQ-004, REQ-005

---

#### 任务4.3: 文档字符串验证测试
**描述**: 验证所有公开方法的文档字符串符合规范。

**实施步骤**:
1. 编写文档字符串格式检查测试
2. 编写文档字符串内容检查测试
3. 编写参数说明检查测试
4. 编写返回值说明检查测试

**代码生成提示**:
```
测试用例示例：
def test_lexer_docstrings():
    """测试词法分析器文档字符串"""
    lexer = Lexer("")

    # 检查 tokenize 方法文档字符串
    assert lexer.tokenize.__doc__ is not None
    assert '"""' in lexer.tokenize.__doc__
    assert 'Token' in lexer.tokenize.__doc__
    assert 'Args' in lexer.tokenize.__doc__ or '参数' in lexer.tokenize.__doc__
    assert 'Returns' in lexer.tokenize.__doc__ or '返回' in lexer.tokenize.__doc__

def test_all_public_methods_have_docstrings():
    """测试所有公开方法都有文档字符串"""
    classes_to_check = [Lexer, Parser, SemanticAnalyzer, CodeGenerator]

    for cls in classes_to_check:
        for name, method in inspect.getmembers(cls, inspect.isfunction):
            if not name.startswith('_'):  # 公开方法
                assert method.__doc__ is not None, f"{cls.__name__}.{name} 缺少文档字符串"
```

**覆盖需求**: REQ-006, REQ-007, REQ-008, REQ-009, REQ-010

---

### 任务5: 集成验证

**任务描述**: 执行完整的集成测试，确保所有修改协同工作正常，不破坏现有功能。

**输入**:
- 所有修改后的组件
- 现有的编译器测试套件

**输出**:
- 集成测试报告
- 性能测试报告
- 向后兼容性验证报告

**验收标准**:
- 所有现有测试通过
- 编译器性能下降不超过 10%
- 公开 API 保持向后兼容
- 错误信息格式保持一致

**优先级**: 高

**预估工作量**: 2小时

**实施步骤**:
1. 运行完整的编译器测试套件
2. 执行性能基准测试，对比优化前后的性能
3. 验证公开 API 的向后兼容性
4. 检查错误信息格式的一致性
5. 生成集成测试报告

**代码生成提示**:
```
集成验证脚本：
def run_integration_tests():
    """运行集成测试"""
    # 1. 运行现有测试套件
    result = subprocess.run(['pytest', 'tests/'], capture_output=True)
    assert result.returncode == 0, "测试失败"

    # 2. 性能测试
    import time
    start = time.time()
    # 编译大型测试文件
    compile_large_test_file()
    elapsed = time.time() - start
    print(f"编译时间: {elapsed:.2f}s")

    # 3. API 兼容性检查
    # 检查所有公开 API 签名是否改变
    check_api_compatibility()

    # 4. 错误信息格式检查
    check_error_message_format()
```

**覆盖需求**: 所有需求 (REQ-001 至 REQ-010)

---

## 3. 任务执行顺序

### 3.1 推荐执行顺序
1. **阶段一**: 任务1.1 → 任务1.2 → 任务1.3 (错误处理集成)
2. **阶段二**: 任务2.1 → 任务2.2 (类型推断集成，依赖任务1.3)
3. **阶段三**: 任务3.1 → 任务3.2 → 任务3.3 → 任务3.4 → 任务3.5 (文档字符串添加，可并行)
4. **阶段四**: 任务4.1 → 任务4.2 → 任务4.3 (测试验证)
5. **阶段五**: 任务5 (集成验证)

### 3.2 并行执行建议
- 任务3.1、3.2、3.3、3.4、3.5 可以并行执行（文档字符串添加互不依赖）
- 任务4.1、4.2 可以在对应功能完成后立即开始

## 4. 风险与应对

### 4.1 潜在风险
| 风险项 | 影响程度 | 应对措施 |
|--------|----------|----------|
| 错误处理逻辑遗漏 | 高 | 使用代码搜索工具查找所有异常抛出点 |
| 类型推断性能下降 | 中 | 仅在必要时调用类型推断，添加缓存机制 |
| 文档字符串格式不一致 | 低 | 使用统一的文档字符串模板 |
| 测试覆盖不足 | 中 | 编写测试用例清单，逐项验证 |

### 4.2 回滚计划
如果集成验证失败，可以按以下顺序回滚：
1. 回滚任务2（类型推断集成）
2. 回滚任务1（错误处理集成）
3. 文档字符串修改不影响功能，可保留或回滚

## 5. 附录

### 5.1 代码修改清单
| 文件路径 | 修改类型 | 影响范围 |
|----------|----------|----------|
| src/lexer/lexer.py | 修改 | 添加 error_handler，修改错误报告方式 |
| src/parser/parser.py | 修改 | 添加 error_handler，修改错误报告方式 |
| src/semantic/analyzer.py | 修改 | 添加 error_handler 和 type_inferencer，修改错误报告和类型推断 |
| src/codegen/generator.py | 修改 | 添加文档字符串 |
| src/macro/expander.py | 修改 | 添加文档字符串 |
| tests/test_error_handling.py | 新增 | 错误处理集成测试 |
| tests/test_type_inference.py | 新增 | 类型推断集成测试 |
| tests/test_docstrings.py | 新增 | 文档字符串验证测试 |

### 5.2 验收检查清单
- [ ] 所有 LexerError 抛出已替换为 _report_error
- [ ] 所有 ParseError 抛出已替换为 _report_error
- [ ] 所有 SemanticError 创建已替换为 _report_error
- [ ] 类型推断在变量定义时正确调用
- [ ] 类型推断在表达式分析时正确调用
- [ ] 所有公开方法添加文档字符串
- [ ] 文档字符串符合 PEP 257 规范
- [ ] 所有测试用例通过
- [ ] 性能下降不超过 10%
- [ ] 向后兼容性验证通过

### 5.3 变更历史

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|----------|
| 1.0 | 2025-01-23 | - | 初始版本 |
