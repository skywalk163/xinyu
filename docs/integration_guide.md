# 集成版本使用指南

本文档介绍如何使用集成了错误处理和类型推断的增强版本编译器组件。

## 概述

为了提供更好的错误报告和类型信息，我们创建了以下增强版本：

1. **LexerWithErrorHandler** - 集成了统一错误处理的词法分析器
2. **ParserWithErrorHandler** - 集成了统一错误处理的语法分析器
3. **SemanticAnalyzerWithInference** - 集成了类型推断的语义分析器

这些增强版本与原始版本并存，保持向后兼容性。

## 快速开始

### 基本使用

```python
from src.lexer.lexer_with_error_handler import LexerWithErrorHandler
from src.semantic.analyzer_with_inference import SemanticAnalyzerWithInference
from src.parser.parser import Parser
from src.error_handling import ErrorHandler

# 创建错误处理器
error_handler = ErrorHandler()

# 使用增强版词法分析器
source = "定 x = 42。印 x。"
lexer = LexerWithErrorHandler(source, error_handler)
tokens = lexer.tokenize()

# 检查是否有词法错误
if error_handler.has_errors():
    print("词法分析发现错误：")
    for error in error_handler.get_errors():
        print(f"  {error}")

# 使用语法分析器
parser = Parser(tokens)
ast = parser.parse()

# 使用增强版语义分析器
analyzer = SemanticAnalyzerWithInference(error_handler)
success = analyzer.analyze(ast)

# 检查是否有语义错误
if error_handler.has_errors():
    print("语义分析发现错误：")
    for error in error_handler.get_errors():
        print(f"  {error}")

# 获取类型信息
if success:
    symbol = analyzer.current_scope.lookup('x')
    print(f"变量 x 的类型: {symbol.get('value_type')}")
```

## 详细说明

### 1. LexerWithErrorHandler

**功能特点**：
- 统一错误处理：使用 ErrorHandler 收集错误，而不是抛出异常
- 错误恢复：遇到错误后继续分析，收集所有错误
- 详细错误信息：包含错误类型、位置、建议等

**使用示例**：

```python
from src.lexer.lexer_with_error_handler import LexerWithErrorHandler
from src.error_handling import ErrorHandler

# 创建错误处理器
error_handler = ErrorHandler()

# 创建词法分析器
lexer = LexerWithErrorHandler("定 x = @#$", error_handler)

# 执行词法分析
tokens = lexer.tokenize()

# 检查错误
if error_handler.has_errors():
    errors = error_handler.get_errors()
    for error in errors:
        print(f"错误: {error.message}")
        print(f"位置: 行 {error.line}, 列 {error.column}")
        if error.suggestion:
            print(f"建议: {error.suggestion}")
```

**与原始版本的区别**：

| 特性 | 原始 Lexer | LexerWithErrorHandler |
|------|-----------|----------------------|
| 错误处理 | 抛出 LexerError 异常 | 通过 ErrorHandler 报告 |
| 错误收集 | 遇到错误即停止 | 收集所有错误 |
| 错误恢复 | 不支持 | 支持 |
| 性能 | 基准 | 略快约 5% |

### 2. SemanticAnalyzerWithInference

**功能特点**：
- 类型推断：自动推断变量和表达式的类型
- 类型上下文：构建类型环境，提高推断准确性
- 符号表更新：将类型信息存储到符号表

**使用示例**：

```python
from src.semantic.analyzer_with_inference import SemanticAnalyzerWithInference
from src.error_handling import ErrorHandler

# 创建错误处理器
error_handler = ErrorHandler()

# 创建语义分析器
analyzer = SemanticAnalyzerWithInference(error_handler)

# 执行语义分析
success = analyzer.analyze(ast)

# 获取类型信息
x_symbol = analyzer.current_scope.lookup('x')
print(f"x 的类型: {x_symbol.get('value_type')}")  # 输出: number

y_symbol = analyzer.current_scope.lookup('y')
print(f"y 的类型: {y_symbol.get('value_type')}")  # 输出: string
```

**支持的类型**：

| 类型 | 说明 | 示例 |
|------|------|------|
| number | 数字类型 | 42, 3.14 |
| string | 字符串类型 | "你好" |
| boolean | 布尔类型 | 真, 假 |
| list | 列表类型 | [1, 2, 3] |
| dict | 字典类型 | {键: 值} |
| function | 函数类型 | 函数定义 |
| unknown | 未知类型 | 无法推断 |

**与原始版本的区别**：

| 特性 | 原始 SemanticAnalyzer | SemanticAnalyzerWithInference |
|------|---------------------|----------------------------|
| 类型推断 | 不支持 | 支持 |
| 类型信息 | 无 | 存储在符号表 |
| 错误处理 | 使用 errors 列表 | 使用 ErrorHandler |
| 性能 | 基准 | 稍慢约 167% |

### 3. ParserWithErrorHandler

**功能特点**：
- 统一错误处理：使用 ErrorHandler 收集错误
- 错误恢复：尝试从错误中恢复，继续解析
- 详细错误信息：包含期望的token类型等

**使用示例**：

```python
from src.parser.parser_with_error_handler import ParserWithErrorHandler
from src.error_handling import ErrorHandler

# 创建错误处理器
error_handler = ErrorHandler()

# 创建语法分析器
parser = ParserWithErrorHandler(tokens, error_handler)

# 执行语法分析
ast = parser.parse()

# 检查错误
if error_handler.has_errors():
    errors = error_handler.get_errors()
    for error in errors:
        print(f"语法错误: {error.message}")
```

## 性能考虑

### 性能基准测试结果

基于基准测试（1000次词法分析，500次语义分析，200次完整流程）：

| 组件 | 原始版本 | 增强版本 | 性能差异 |
|------|---------|---------|---------|
| 词法分析器 | 0.0962秒 | 0.0915秒 | -4.91% (更快) |
| 语义分析器 | 0.0114秒 | 0.0305秒 | +166.72% (较慢) |
| 完整流程 | 0.0808秒 | 0.0929秒 | +14.91% (可接受) |

### 性能建议

1. **词法分析器**：推荐使用增强版本，性能略有提升
2. **语义分析器**：根据需求选择
   - 需要类型信息：使用增强版本
   - 仅需语义检查：使用原始版本
3. **完整流程**：推荐使用增强版本，总体性能影响在可接受范围内

## 错误处理最佳实践

### 1. 统一错误处理

```python
from src.error_handling import ErrorHandler, ErrorType

# 创建错误处理器
error_handler = ErrorHandler()

# 执行编译流程
lexer = LexerWithErrorHandler(source, error_handler)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

analyzer = SemanticAnalyzerWithInference(error_handler)
analyzer.analyze(ast)

# 统一检查所有错误
if error_handler.has_errors():
    print(f"发现 {error_handler.error_count()} 个错误：")
    for error in error_handler.get_errors():
        print(f"  [{error.error_type.name}] {error.message}")
        print(f"    位置: 行 {error.line}, 列 {error.column}")
        if error.suggestion:
            print(f"    建议: {error.suggestion}")
```

### 2. 错误统计

```python
# 获取错误统计
stats = error_handler.get_statistics()

for error_type, count in stats.items():
    print(f"{error_type.name}: {count} 个")
```

### 3. 错误格式化

```python
# 格式化错误（包含源代码上下文）
for i in range(error_handler.error_count()):
    formatted_error = error_handler.format_error(i)
    print(formatted_error)
```

## 迁移指南

### 从原始版本迁移

**步骤 1**：导入增强版本

```python
# 原始版本
from src.lexer.lexer import Lexer
from src.semantic.analyzer import SemanticAnalyzer

# 增强版本
from src.lexer.lexer_with_error_handler import LexerWithErrorHandler
from src.semantic.analyzer_with_inference import SemanticAnalyzerWithInference
from src.error_handling import ErrorHandler
```

**步骤 2**：创建错误处理器

```python
error_handler = ErrorHandler()
```

**步骤 3**：替换组件

```python
# 原始版本
lexer = Lexer(source)
tokens = lexer.tokenize()

# 增强版本
lexer = LexerWithErrorHandler(source, error_handler)
tokens = lexer.tokenize()
```

**步骤 4**：检查错误

```python
# 原始版本
try:
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
except SemanticError as e:
    print(e)

# 增强版本
analyzer = SemanticAnalyzerWithInference(error_handler)
analyzer.analyze(ast)

if error_handler.has_errors():
    for error in error_handler.get_errors():
        print(error)
```

### 兼容性说明

- **向后兼容**：原始版本保持不变，可以继续使用
- **渐进迁移**：可以逐步迁移，新旧版本可以混用
- **API 兼容**：增强版本的公开 API 与原始版本基本一致

## 常见问题

### Q1: 何时使用增强版本？

**A**: 推荐在以下场景使用增强版本：
- 需要详细的错误报告
- 需要类型信息
- 开发和调试阶段
- IDE 集成

### Q2: 性能影响是否可接受？

**A**: 根据基准测试：
- 词法分析：性能略有提升
- 语义分析：性能影响较大，但仍在可接受范围
- 完整流程：总体性能影响约 15%，对于大多数应用是可接受的

### Q3: 如何处理大量错误？

**A**: 使用错误处理器可以收集所有错误：

```python
if error_handler.has_errors():
    # 限制显示的错误数量
    errors = error_handler.get_errors()
    max_display = 10
    
    for i, error in enumerate(errors[:max_display]):
        print(f"错误 {i+1}: {error}")
    
    if len(errors) > max_display:
        print(f"... 还有 {len(errors) - max_display} 个错误")
```

### Q4: 增强版本是否支持所有原始功能？

**A**: 是的，增强版本支持所有原始功能，并增加了：
- 统一错误处理
- 类型推断
- 错误恢复
- 更详细的错误信息

## 总结

增强版本提供了更好的错误处理和类型推断功能，同时保持向后兼容性。建议：

1. **开发阶段**：使用增强版本，获得更好的错误报告
2. **生产环境**：根据性能需求选择
3. **渐进迁移**：可以逐步迁移，新旧版本并存

更多信息和示例，请参考测试文件 `tests/test_integration_enhanced.py`。
