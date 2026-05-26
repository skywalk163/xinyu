# 技术设计文档

## 文档信息
- **特性名称**: code-structure-optimization-phase2
- **创建日期**: 2025-01-23
- **版本**: 1.0
- **状态**: 草稿
- **关联需求文档**: spec.md v1.0

## 1. 设计概述

### 1.1 设计目标
本设计旨在优化中文编程语言编译器的代码结构，通过以下三个核心目标提升代码质量：
1. **统一错误处理机制**：将分散的异常抛出统一为 ErrorHandler 集中管理，提高错误报告的一致性和可维护性
2. **集成类型推断系统**：将 TypeInferencer 集成到语义分析器中，提供更准确的类型信息
3. **完善代码文档**：为所有公开方法添加符合 PEP 257 规范的文档字符串，提升代码可读性

### 1.2 设计原则
- **单一职责原则**：每个模块专注于单一功能，ErrorHandler 负责错误收集，TypeInferencer 负责类型推断
- **开闭原则**：通过集成而非修改现有实现，保持向后兼容性
- **依赖倒置原则**：高层模块（分析器）依赖抽象接口（ErrorHandler、TypeInferencer）
- **最小侵入原则**：仅修改错误报告方式，不改变错误处理逻辑和类型推断算法

### 1.3 技术栈
- **语言**: Python 3.7+
- **核心依赖**:
  - `dataclass`：用于数据结构定义
  - `typing`：用于类型注解
  - `enum`：用于错误类型枚举
- **现有组件**:
  - `ErrorHandler`：统一错误处理器（src/error_handling.py）
  - `TypeInferencer`：类型推断器（src/semantic/type_inference.py）
  - `Lexer`：词法分析器（src/lexer/lexer.py）
  - `Parser`：语法分析器（src/parser/parser.py）
  - `SemanticAnalyzer`：语义分析器（src/semantic/analyzer.py）

## 2. 架构设计

### 2.1 整体架构

#### 架构图
```
┌─────────────────────────────────────────────────────────────┐
│                    编译器管道架构                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  ErrorHandler (统一错误处理中心)                               │
│  - 收集所有编译阶段错误                                         │
│  - 提供错误统计和格式化                                         │
└─────────────────────────────────────────────────────────────┘
         ▲                    ▲                    ▲
         │                    │                    │
    ┌────┴────┐          ┌────┴────┐          ┌────┴────┐
    │  Lexer  │          │  Parser │          │Semantic │
    │         │          │         │          │Analyzer │
    └─────────┘          └─────────┘          └─────────┘
         │                    │                    │
         │                    │                    ▼
         │                    │          ┌─────────────────┐
         │                    │          │ TypeInferencer  │
         │                    │          │ (类型推断服务)   │
         │                    │          └─────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
    Token序列              AST节点              符号表+类型信息
```

### 2.2 模块划分

| 模块名称 | 职责描述 | 关键接口 |
|----------|----------|----------|
| ErrorHandler | 统一错误收集、格式化和统计 | `report()`, `get_errors()`, `has_errors()` |
| TypeInferencer | AST节点类型推断 | `infer()`, `check_type_compatibility()` |
| Lexer | 词法分析，集成ErrorHandler | `tokenize()`, `_report_error()` |
| Parser | 语法分析，集成ErrorHandler | `parse()`, `_report_error()` |
| SemanticAnalyzer | 语义分析，集成ErrorHandler和TypeInferencer | `analyze()`, `_report_error()`, `_infer_type()` |

### 2.3 组件交互
- **错误处理流程**：各分析器通过 `_report_error()` 方法将错误统一报告给 ErrorHandler
- **类型推断流程**：SemanticAnalyzer 在分析变量定义和表达式时调用 TypeInferencer.infer()
- **数据流向**：源代码 → Lexer → Token序列 → Parser → AST → SemanticAnalyzer → 符号表

## 3. 详细设计

### 3.1 词法分析器错误处理集成

#### 3.1.1 类设计
**Lexer 类修改**：
- 添加 `error_handler: ErrorHandler` 属性
- 添加 `_report_error()` 私有方法
- 移除所有 `LexerError` 异常抛出，改为调用 `_report_error()`

#### 3.1.2 接口定义
```python
class Lexer:
    def __init__(self, source: str, error_handler: ErrorHandler = None):
        """初始化词法分析器
        
        Args:
            source: 源代码字符串
            error_handler: 错误处理器实例（可选）
        """
        self.source = source
        self.error_handler = error_handler or ErrorHandler()
        # ... 其他初始化
    
    def _report_error(
        self, 
        message: str, 
        line: int, 
        column: int, 
        suggestion: Optional[str] = None
    ) -> None:
        """统一报告词法错误
        
        Args:
            message: 错误消息
            line: 行号
            column: 列号
            suggestion: 修复建议（可选）
        """
        self.error_handler.report(
            error_type=ErrorType.LEXER_ERROR,
            message=message,
            line=line,
            column=column,
            suggestion=suggestion
        )
```

#### 3.1.3 数据结构
无需新增数据结构，复用现有的 `Error` 和 `ErrorType`。

### 3.2 语法分析器错误处理集成

#### 3.2.1 类设计
**Parser 类修改**：
- 添加 `error_handler: ErrorHandler` 属性
- 添加 `_report_error()` 私有方法
- 移除所有 `ParseError` 异常抛出，改为调用 `_report_error()`

#### 3.2.2 接口定义
```python
class Parser:
    def __init__(self, tokens: List[Token], error_handler: ErrorHandler = None):
        """初始化语法分析器
        
        Args:
            tokens: Token序列
            error_handler: 错误处理器实例（可选）
        """
        self.tokens = tokens
        self.error_handler = error_handler or ErrorHandler()
        # ... 其他初始化
    
    def _report_error(
        self, 
        message: str, 
        token: Token, 
        suggestion: Optional[str] = None
    ) -> None:
        """统一报告语法错误
        
        Args:
            message: 错误消息
            token: 相关Token
            suggestion: 修复建议（可选）
        """
        self.error_handler.report(
            error_type=ErrorType.PARSER_ERROR,
            message=message,
            line=token.line,
            column=token.column,
            suggestion=suggestion
        )
```

### 3.3 语义分析器错误处理集成

#### 3.3.1 类设计
**SemanticAnalyzer 类修改**：
- 将 `errors: List[SemanticError]` 替换为 `error_handler: ErrorHandler`
- 添加 `_report_error()` 私有方法
- 修改 `has_errors()` 和 `get_errors()` 方法适配新机制

#### 3.3.2 接口定义
```python
class SemanticAnalyzer:
    def __init__(self, error_handler: ErrorHandler = None):
        """初始化语义分析器
        
        Args:
            error_handler: 错误处理器实例（可选）
        """
        self.error_handler = error_handler or ErrorHandler()
        # ... 其他初始化
    
    def _report_error(
        self, 
        message: str, 
        line: int, 
        column: int, 
        suggestion: Optional[str] = None
    ) -> None:
        """统一报告语义错误
        
        Args:
            message: 错误消息
            line: 行号
            column: 列号
            suggestion: 修复建议（可选）
        """
        self.error_handler.report(
            error_type=ErrorType.SEMANTIC_ERROR,
            message=message,
            line=line,
            column=column,
            suggestion=suggestion
        )
    
    def has_errors(self) -> bool:
        """检查是否存在错误
        
        Returns:
            是否存在错误
        """
        return self.error_handler.has_errors()
    
    def get_errors(self) -> List[Error]:
        """获取所有错误
        
        Returns:
            错误列表
        """
        return self.error_handler.get_errors()
```

### 3.4 类型推断集成设计

#### 3.4.1 类设计
**SemanticAnalyzer 类扩展**：
- 添加 `type_inferencer: TypeInferencer` 属性
- 添加 `_infer_type()` 私有方法
- 在 `_visit_var_def()` 和 `_visit_assign()` 中调用类型推断

#### 3.4.2 接口定义
```python
class SemanticAnalyzer:
    def __init__(self, error_handler: ErrorHandler = None):
        """初始化语义分析器"""
        self.error_handler = error_handler or ErrorHandler()
        self.type_inferencer = TypeInferencer()
        # ... 其他初始化
    
    def _infer_type(
        self, 
        node: ASTNode, 
        context: Optional[Dict[str, str]] = None
    ) -> str:
        """推断AST节点的类型
        
        Args:
            node: AST节点
            context: 类型上下文（变量名 -> 类型）
        
        Returns:
            推断的类型字符串
        """
        return self.type_inferencer.infer(node, context)
    
    def _build_type_context(self) -> Dict[str, str]:
        """构建当前作用域的类型上下文
        
        Returns:
            变量名到类型的映射
        """
        context = {}
        scope = self.current_scope
        for name, symbol in scope.symbols.items():
            if symbol.get('value_type'):
                context[name] = symbol['value_type']
        return context
```

#### 3.4.3 数据结构
```python
# 类型上下文：变量名 -> 类型字符串
TypeContext = Dict[str, str]

# 符号表扩展（在现有基础上添加类型信息）
Symbol = {
    'name': str,           # 符号名
    'kind': str,           # 种类（variable, function, etc.）
    'value_type': str,     # 值类型（number, string, boolean, etc.）
    'line': int,           # 定义行号
    'column': int,         # 定义列号
}
```

### 3.5 文档字符串设计

#### 3.5.1 文档字符串规范
遵循 PEP 257 规范，使用以下格式：

```python
def method_name(self, param1: Type1, param2: Type2) -> ReturnType:
    """方法功能简述
    
    详细描述（可选）。
    
    Args:
        param1: 参数1说明
        param2: 参数2说明
    
    Returns:
        返回值说明
    
    Raises:
        ExceptionType: 异常说明（如适用）
    
    Example:
        使用示例（可选）
    """
```

#### 3.5.2 需要添加文档字符串的方法

**Lexer 类**：
- `tokenize()`: 将源代码转换为Token序列
- `_read_string()`: 读取字符串字面量
- `_read_number()`: 读取数字字面量
- `_read_identifier()`: 读取标识符
- `_read_chinese()`: 读取中文关键字或标识符

**Parser 类**：
- `parse()`: 解析Token序列生成AST
- `_parse_statement()`: 解析语句
- `_parse_expression()`: 解析表达式
- `_parse_function_def()`: 解析函数定义
- `_parse_if_statement()`: 解析条件语句

**SemanticAnalyzer 类**：
- `analyze()`: 分析AST进行语义检查
- `_visit_program()`: 访问程序节点
- `_visit_var_def()`: 访问变量定义节点
- `_visit_function_def()`: 访问函数定义节点
- `_visit_expression()`: 访问表达式节点

**CodeGenerator 类**：
- `generate()`: 生成目标代码
- `_generate_program()`: 生成程序代码
- `_generate_function()`: 生成函数代码
- `_generate_expression()`: 生成表达式代码

**MacroExpander 类**：
- `expand()`: 展开宏
- `register_macro()`: 注册宏定义
- `is_macro()`: 检查是否为宏

## 4. 数据设计

### 4.1 数据模型

#### ER 图
```
┌──────────────┐
│    Error     │
├──────────────┤
│ error_type   │───┐
│ message      │   │
│ line         │   │
│ column       │   │
│ source       │   │
│ suggestion   │   │
└──────────────┘   │
                   │
┌──────────────┐   │
│  ErrorType   │◄──┘
├──────────────┤
│ LEXER_ERROR  │
│ PARSER_ERROR │
│SEMANTIC_ERROR│
│RUNTIME_ERROR │
└──────────────┘

┌──────────────┐
│   Symbol     │
├──────────────┤
│ name         │
│ kind         │
│ value_type   │◄── 类型推断结果
│ line         │
│ column       │
│ is_builtin   │
└──────────────┘
```

### 4.2 数据存储
- **错误存储**：ErrorHandler 内部使用 `List[Error]` 存储所有错误
- **类型信息存储**：符号表中增加 `value_type` 字段存储类型推断结果
- **类型上下文**：临时使用 `Dict[str, str]` 存储当前作用域的变量类型映射

### 4.3 数据迁移
无需数据迁移，仅修改内部实现方式。

## 5. API 设计

### 5.1 内部 API

#### 错误报告 API
```python
# 统一错误报告接口
def _report_error(
    self,
    message: str,
    line: int,
    column: int,
    suggestion: Optional[str] = None
) -> None:
    """报告错误到 ErrorHandler"""
    pass
```

#### 类型推断 API
```python
# 类型推断接口
def _infer_type(
    self,
    node: ASTNode,
    context: Optional[Dict[str, str]] = None
) -> str:
    """推断 AST 节点类型"""
    pass

# 类型上下文构建接口
def _build_type_context(self) -> Dict[str, str]:
    """构建当前作用域类型上下文"""
    pass
```

### 5.2 外部 API

#### API 规范
| API 名称 | 方法 | 描述 | 请求参数 | 响应格式 |
|----------|------|------|----------|----------|
| Lexer.tokenize | 方法 | 词法分析 | source: str | List[Token] |
| Parser.parse | 方法 | 语法分析 | tokens: List[Token] | ProgramNode |
| SemanticAnalyzer.analyze | 方法 | 语义分析 | ast: ProgramNode | None |
| ErrorHandler.get_errors | 方法 | 获取错误 | None | List[Error] |
| ErrorHandler.has_errors | 方法 | 检查错误 | None | bool |

## 6. 流程设计

### 6.1 核心业务流程

#### 错误处理流程图
```
┌─────────────┐
│ 检测到错误   │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ 调用 _report_error  │
│ (message, line, col)│
└──────┬──────────────┘
       │
       ▼
┌─────────────────────────────┐
│ ErrorHandler.report()       │
│ - 创建 Error 对象            │
│ - 添加到 errors 列表         │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────┐
│ 继续分析过程     │
│ (不中断编译)     │
└─────────────────┘
```

#### 类型推断流程图
```
┌──────────────────┐
│ 分析变量定义/赋值  │
└────────┬─────────┘
         │
         ▼
┌──────────────────────┐
│ 构建类型上下文        │
│ _build_type_context()│
└────────┬─────────────┘
         │
         ▼
┌──────────────────────────┐
│ 调用类型推断              │
│ _infer_type(node, context)│
└────────┬─────────────────┘
         │
         ▼
┌───────────────────────┐
│ 更新符号表类型信息      │
│ symbol['value_type']   │
└───────────────────────┘
```

### 6.2 异常处理流程
- **错误不中断编译**：报告错误后继续分析，收集所有错误
- **错误统计**：编译结束后通过 ErrorHandler.get_statistics() 获取错误统计
- **错误输出**：通过 ErrorHandler.print_errors() 格式化输出所有错误

## 7. 技术决策

### 7.1 关键决策记录
| 决策项 | 选项 | 最终决策 | 决策理由 |
|--------|------|----------|----------|
| 错误处理方式 | A. 抛出异常 / B. 收集错误 | B | 收集错误可以继续分析，发现更多问题 |
| ErrorHandler 实例管理 | A. 全局单例 / B. 实例传递 | B | 实例传递更灵活，便于测试和隔离 |
| 类型推断时机 | A. 独立阶段 / B. 集成到语义分析 | B | 减少遍历次数，提高性能 |
| 文档字符串语言 | A. 英文 / B. 中文 | B | 与项目整体风格一致，便于中文用户理解 |

### 7.2 技术风险
| 风险项 | 影响程度 | 应对措施 |
|--------|----------|----------|
| 性能下降 | 中 | 类型推断仅在必要时调用，避免重复推断 |
| 向后兼容性破坏 | 高 | 保持公开 API 不变，仅修改内部实现 |
| 错误信息格式变化 | 低 | 保持错误信息格式一致，仅改变报告方式 |
| 文档字符串维护成本 | 低 | 使用统一格式，便于后续维护 |

## 8. 性能设计

### 8.1 性能目标
- **错误处理性能**：错误报告开销 < 1ms/错误
- **类型推断性能**：类型推断开销 < 5ms/表达式
- **整体编译性能**：性能下降不超过 10%

### 8.2 优化策略
1. **延迟类型推断**：仅在需要类型信息时进行推断
2. **类型上下文缓存**：缓存当前作用域的类型上下文，避免重复构建
3. **批量错误报告**：使用列表存储错误，避免频繁 I/O
4. **避免重复推断**：符号表中存储已推断的类型，避免重复计算

## 9. 安全设计

### 9.1 安全措施
- **错误信息脱敏**：错误消息中不包含敏感信息（如文件路径、用户数据）
- **类型推断安全**：类型推断失败时返回 'unknown'，不抛出异常
- **输入验证**：ErrorHandler 验证错误参数的有效性

### 9.2 权限控制
本特性不涉及权限控制，所有修改均为内部实现。

## 10. 测试设计

### 10.1 测试策略
- **单元测试**：测试每个修改的方法和新增的功能
- **集成测试**：测试错误处理和类型推断的集成效果
- **回归测试**：确保现有功能不受影响

### 10.2 测试场景

#### 错误处理测试场景
| 场景 | 输入 | 期望输出 |
|------|------|----------|
| 词法错误 | 非法字符 | ErrorHandler 包含 LEXER_ERROR |
| 语法错误 | 缺少结束符 | ErrorHandler 包含 PARSER_ERROR |
| 语义错误 | 未定义变量 | ErrorHandler 包含 SEMANTIC_ERROR |
| 多个错误 | 多处错误 | ErrorHandler 包含所有错误 |
| 错误建议 | 可修复错误 | Error 包含 suggestion 字段 |

#### 类型推断测试场景
| 场景 | 输入 | 期望输出 |
|------|------|----------|
| 数字字面量 | 42 | 'number' |
| 字符串字面量 | "hello" | 'string' |
| 二元运算 | 1 + 2 | 'number' |
| 比较运算 | 1 < 2 | 'boolean' |
| 函数调用 | 长度([1,2,3]) | 'number' |
| 变量引用 | x (已知类型) | 已知类型 |

#### 文档字符串测试场景
| 场景 | 检查项 | 期望结果 |
|------|--------|----------|
| 格式检查 | 三重双引号 | 通过 |
| 内容检查 | 包含功能描述 | 通过 |
| 参数检查 | 包含参数说明 | 通过 |
| 返回值检查 | 包含返回值说明 | 通过 |

## 11. 部署设计

### 11.1 部署架构
本特性为代码结构优化，无需特殊部署。修改后的代码直接替换现有实现。

### 11.2 配置管理
无需新增配置项。

## 12. 附录

### 12.1 参考资料
- PEP 257 -- Docstring Conventions: https://www.python.org/dev/peps/pep-0257/
- ErrorHandler 实现文档: src/error_handling.py
- TypeInferencer 实现文档: src/semantic/type_inference.py
- Python 类型注解: https://docs.python.org/3/library/typing.html

### 12.2 术语表
| 术语 | 定义 |
|------|------|
| ErrorHandler | 统一错误处理器，用于收集和报告编译过程中的错误 |
| ErrorType | 错误类型枚举，包括词法错误、语法错误、语义错误、运行时错误 |
| TypeInferencer | 类型推断器，用于推断 AST 节点的类型 |
| PEP 257 | Python 文档字符串风格指南 |
| AST | 抽象语法树，表示源代码的语法结构 |
| 符号表 | 存储变量、函数等符号信息的表结构 |
| 类型上下文 | 变量名到类型的映射，用于类型推断 |

### 12.3 变更历史

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|----------|
| 1.0 | 2025-01-23 | - | 初始版本 |
