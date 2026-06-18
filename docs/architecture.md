# 心语语言架构设计文档

## 1. 架构概述

心语语言采用经典的**多阶段编译器架构**，将编译过程分为前端（分析）和后端（生成）两部分。

### 1.1 编译流程

```
源代码 (str)
    ↓ 词法分析 (Lexer)
Token序列 (List[Token])
    ↓ 语法分析 (Parser)
抽象语法树 (AST)
    ↓ 语义分析 (SemanticAnalyzer)
验证的AST + 符号表
    ↓ 宏展开 (MacroExpander)
变换的AST
    ↓ 代码生成 (PythonCodegen)
Python代码 (str)
    ↓ 执行 (Runtime)
执行结果 (Any)
```

### 1.2 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        心语编译器                            │
├─────────────────────────────────────────────────────────────┤
│  前端（分析阶段）                                             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐                │
│  │  Lexer   │──▶│  Parser  │──▶│ Semantic │                │
│  │ 词法分析 │   │ 语法分析 │   │ 语义分析 │                │
│  └──────────┘   └──────────┘   └──────────┘                │
│       │              │              │                       │
│       ▼              ▼              ▼                       │
│    Tokens          AST         验证的AST                    │
├─────────────────────────────────────────────────────────────┤
│  中间层（变换阶段）                                           │
│  ┌──────────┐                                               │
│  │  Macro   │  宏展开、代码变换                              │
│  │  System  │                                               │
│  └──────────┘                                               │
├─────────────────────────────────────────────────────────────┤
│  后端（生成阶段）                                             │
│  ┌──────────┐   ┌──────────┐                               │
│  │ Codegen  │──▶│ Runtime  │                               │
│  │ 代码生成 │   │ 运行时   │                               │
│  └──────────┘   └──────────┘                               │
│       │              │                                      │
│       ▼              ▼                                      │
│  Python代码      执行结果                                   │
└─────────────────────────────────────────────────────────────┘
```

## 2. 模块划分

### 2.1 核心模块

| 模块名称 | 路径 | 职责描述 | 关键接口 | 依赖模块 |
|----------|------|----------|----------|----------|
| **lexer** | src/lexer/ | 词法分析，将源代码转换为Token序列 | `tokenize() -> List[Token]` | tokens, keywords |
| **parser** | src/parser/ | 语法分析，将Token序列转换为AST | `parse() -> ProgramNode` | ast_nodes, lexer |
| **semantic** | src/semantic/ | 语义分析，检查AST的语义正确性 | `analyze(ast) -> bool` | scope, type_inference |
| **codegen** | src/codegen/ | 代码生成，将AST转换为目标代码 | `generate(ast) -> str` | ast_nodes |
| **macro** | src/macro/ | 宏系统，代码变换和展开 | `expand(ast) -> AST` | macro_system, builtin_macros |
| **runtime** | src/runtime/ | 运行时环境，执行生成的代码 | `execute(code) -> Any` | - |
| **security** | src/security/ | 安全模块，输入验证和清理 | `validate(source) -> bool` | - |
| **error_handling** | src/error_handling.py | 统一错误处理和报告 | `report(error)` | - |

### 2.2 模块职责边界

#### Lexer（词法分析器）
**职责**：
- 将源代码字符串转换为Token序列
- 识别中文关键字、操作符、标识符
- 处理缩进和换行
- 报告词法错误

**不负责**：
- 语法结构验证（由Parser负责）
- 语义检查（由SemanticAnalyzer负责）

**公共接口**：
```python
class Lexer:
    def tokenize(self) -> List[Token]: ...
    def get_errors(self) -> List[LexerError]: ...
```

#### Parser（语法分析器）
**职责**：
- 将Token序列转换为抽象语法树（AST）
- 验证语法结构正确性
- 构建AST节点
- 报告语法错误

**不负责**：
- 词法分析（由Lexer负责）
- 语义检查（由SemanticAnalyzer负责）
- 代码生成（由Codegen负责）

**公共接口**：
```python
class Parser:
    def parse(self) -> ProgramNode: ...
    def get_errors(self) -> List[ParseError]: ...
```

#### SemanticAnalyzer（语义分析器）
**职责**：
- 作用域管理和符号表构建
- 类型检查和推断
- 变量定义和使用检查
- 函数调用验证
- 报告语义错误

**不负责**：
- 语法分析（由Parser负责）
- 代码生成（由Codegen负责）

**公共接口**：
```python
class SemanticAnalyzer:
    def analyze(self, ast: ProgramNode) -> bool: ...
    def get_errors(self) -> List[SemanticError]: ...
    def get_symbol_table(self) -> Dict: ...
```

#### PythonCodegen（代码生成器）
**职责**：
- 将AST转换为Python代码
- 映射中文操作符到Python操作符
- 处理缩进和代码格式
- 生成可执行代码

**不负责**：
- 语义分析（由SemanticAnalyzer负责）
- 代码执行（由Runtime负责）

**公共接口**：
```python
class PythonCodegen:
    def generate(self, ast: ProgramNode) -> str: ...
```

#### MacroSystem（宏系统）
**职责**：
- 宏定义和注册
- 宏展开和代码变换
- 内置宏管理
- 成语宏支持

**不负责**：
- 语法分析（由Parser负责）
- 语义分析（由SemanticAnalyzer负责）

**公共接口**：
```python
class MacroSystem:
    def register(self, name: str, macro: Macro) -> None: ...
    def expand(self, name: str, args: Dict) -> str: ...
```

#### Runtime（运行时环境）
**职责**：
- 执行生成的Python代码
- 提供执行环境（内置模块、函数）
- 安全隔离和权限控制
- 错误处理和报告

**不负责**：
- 代码生成（由Codegen负责）
- 语义分析（由SemanticAnalyzer负责）

**公共接口**：
```python
class SecureRuntime:
    def execute(self, code: str) -> Tuple[bool, Any, str]: ...
    def compile_restricted_code(self, code: str) -> Tuple[bool, Any, str]: ...
```

## 3. 数据流

### 3.1 编译数据流

```
源代码 (str)
    │
    ├─▶ InputValidator.validate(source)
    │       └─▶ ValidationResult
    │
    ├─▶ Lexer.tokenize(source)
    │       └─▶ List[Token]
    │
    ├─▶ Parser.parse(tokens)
    │       └─▶ ProgramNode (AST)
    │
    ├─▶ SemanticAnalyzer.analyze(ast)
    │       ├─▶ SymbolTable
    │       └─▶ List[SemanticError]
    │
    ├─▶ MacroExpander.expand(ast)
    │       └─▶ ProgramNode (变换的AST)
    │
    ├─▶ PythonCodegen.generate(ast)
    │       └─▶ str (Python代码)
    │
    └─▶ SecureRuntime.execute(python_code)
            └─▶ Any (执行结果)
```

### 3.2 错误处理数据流

```
错误发生
    │
    ├─▶ 创建Error对象
    │       ├─▶ LexerError
    │       ├─▶ ParseError
    │       ├─▶ SemanticError
    │       └─▶ RuntimeError
    │
    ├─▶ ErrorHandler.report(error)
    │       └─▶ 格式化错误信息
    │
    └─▶ 输出到用户
            └─▶ str (错误消息)
```

## 4. 接口契约

### 4.1 词法分析器接口

```python
from typing import List, Protocol
from src.lexer.tokens import Token

class ILexer(Protocol):
    """词法分析器接口"""

    def tokenize(self) -> List[Token]:
        """将源代码转换为Token序列

        Returns:
            Token列表
        """
        ...

    def get_errors(self) -> List['LexerError']:
        """获取词法错误列表

        Returns:
            错误列表
        """
        ...
```

### 4.2 语法分析器接口

```python
from typing import List, Protocol
from src.parser.ast_nodes import ProgramNode

class IParser(Protocol):
    """语法分析器接口"""

    def parse(self) -> ProgramNode:
        """将Token序列转换为AST

        Returns:
            程序根节点
        """
        ...

    def get_errors(self) -> List['ParseError']:
        """获取语法错误列表

        Returns:
            错误列表
        """
        ...
```

### 4.3 语义分析器接口

```python
from typing import List, Dict, Protocol
from src.parser.ast_nodes import ProgramNode

class ISemanticAnalyzer(Protocol):
    """语义分析器接口"""

    def analyze(self, ast: ProgramNode) -> bool:
        """分析AST的语义正确性

        Args:
            ast: 抽象语法树

        Returns:
            是否通过分析
        """
        ...

    def get_errors(self) -> List['SemanticError']:
        """获取语义错误列表

        Returns:
            错误列表
        """
        ...

    def get_symbol_table(self) -> Dict:
        """获取符号表

        Returns:
            符号表字典
        """
        ...
```

### 4.4 代码生成器接口

```python
from typing import Protocol
from src.parser.ast_nodes import ProgramNode

class ICodegen(Protocol):
    """代码生成器接口"""

    def generate(self, ast: ProgramNode) -> str:
        """将AST转换为目标代码

        Args:
            ast: 抽象语法树

        Returns:
            生成的代码字符串
        """
        ...
```

### 4.5 运行时接口

```python
from typing import Tuple, Any, Optional, Protocol

class IRuntime(Protocol):
    """运行时接口"""

    def execute(self, code: str) -> Tuple[bool, Optional[Any], Optional[str]]:
        """执行代码

        Args:
            code: 代码字符串

        Returns:
            (是否成功, 结果, 错误信息)
        """
        ...
```

## 5. 依赖关系

### 5.1 模块依赖图

```
main.py
    ├─▶ lexer
    ├─▶ parser
    ├─▶ semantic
    ├─▶ codegen
    ├─▶ runtime
    └─▶ security

lexer
    ├─▶ tokens
    └─▶ keywords

parser
    ├─▶ ast_nodes
    └─▶ lexer (使用Token类型)

semantic
    ├─▶ scope
    ├─▶ type_inference
    └─▶ parser (使用AST类型)

codegen
    └─▶ parser (使用AST类型)

macro
    ├─▶ macro_system
    ├─▶ builtin_macros
    └─▶ idiom_macros

runtime
    └─▶ security

security
    └─▶ (无依赖)
```

### 5.2 依赖规则

1. **单向依赖**：高层模块依赖低层模块，不形成循环
2. **接口隔离**：模块间通过接口通信，不直接访问内部实现
3. **数据流清晰**：数据沿编译流程单向流动
4. **错误隔离**：每个模块独立处理自己的错误

## 6. 扩展点

### 6.1 添加新关键字

1. 在`src/lexer/keywords.py`中添加关键字映射
2. 在`src/lexer/tokens.py`中添加对应的TokenType
3. 在`src/lexer/lexer.py`中实现识别逻辑
4. 在`src/parser/parser.py`中实现解析逻辑
5. 添加相应的测试

### 6.2 添加新操作符

1. 在`src/lexer/tokens.py`中定义TokenType
2. 在`src/lexer/lexer.py`中实现识别逻辑
3. 在`src/parser/parser.py`中实现解析逻辑
4. 在`src/codegen/python_codegen.py`中实现代码生成
5. 添加相应的测试

### 6.3 添加新AST节点

1. 在`src/parser/ast_nodes.py`中定义节点类
2. 在`src/parser/parser.py`中实现解析逻辑
3. 在`src/semantic/analyzer.py`中实现语义分析
4. 在`src/codegen/python_codegen.py`中实现代码生成
5. 添加相应的测试

### 6.4 添加新宏

1. 在`src/macro/builtin_macros.py`或`src/macro/idiom_macros.py`中定义宏
2. 在`src/macro/macro_system.py`中注册宏
3. 添加相应的测试

## 7. 性能考虑

### 7.1 编译性能

- **词法分析**：O(n)，n为源代码长度
- **语法分析**：O(n)，递归下降解析
- **语义分析**：O(n)，单次AST遍历
- **代码生成**：O(n)，单次AST遍历

### 7.2 内存使用

- **Token序列**：O(n)，n为Token数量
- **AST**：O(n)，n为节点数量
- **符号表**：O(m)，m为符号数量

### 7.3 优化策略

1. **缓存机制**：缓存Token序列和AST
2. **增量编译**：仅重新编译修改的部分
3. **并行处理**：多文件并行编译
4. **流式处理**：大文件流式词法分析

## 8. 安全考虑

### 8.1 安全措施

1. **输入验证**：验证源代码安全性
2. **编译时检查**：检测危险操作
3. **运行时隔离**：RestrictedPython限制
4. **权限控制**：限制可用模块和函数

### 8.2 安全边界

- **可信区域**：编译器内部（Lexer、Parser、SemanticAnalyzer、Codegen）
- **不可信区域**：用户输入、执行环境
- **安全边界**：InputValidator、SecureRuntime

## 9. 测试策略

### 9.1 单元测试

- 每个模块独立测试
- 覆盖所有公共接口
- 测试边界条件和异常情况

### 9.2 集成测试

- 测试模块间交互
- 测试完整编译流程
- 测试错误处理流程

### 9.3 端到端测试

- 测试所有语言特性
- 测试实际程序执行
- 测试性能和内存使用

## 10. 维护指南

### 10.1 代码规范

- 遵循PEP 8规范
- 使用类型注解
- 编写文档字符串（中文）
- 保持测试覆盖率在85%以上

### 10.2 文档维护

- 保持架构文档更新
- 保持API文档更新
- 保持教程和示例更新

### 10.3 版本管理

- 使用语义化版本号
- 保持向后兼容
- 记录变更历史
