# 心语编程语言 API 参考文档

## 概述

心语（Xin Yu）是一个面向中文使用者的编程语言，支持中文关键字和语法。本文档提供了心语编程语言的完整API参考。

## 核心模块

### 编译器接口 (`src/core/compiler.py`)

#### `XinyuCompiler` 类

心语编译器的主接口，提供完整的编译和执行功能。

**构造函数**
```python
def __init__(self, enable_safety: bool = True, enable_inference: bool = True)
```
- `enable_safety`: 是否启用安全执行环境（默认：True）
- `enable_inference`: 是否启用类型推断（默认：True）

**方法**

1. `compile(source: str) -> str`
   - 将心语源代码编译为Python代码
   - 参数：`source` - 心语源代码字符串
   - 返回：生成的Python代码字符串

2. `execute(source: str, context: Optional[Dict] = None) -> Any`
   - 编译并执行心语代码
   - 参数：
     - `source` - 心语源代码字符串
     - `context` - 执行上下文（可选）
   - 返回：执行结果

3. `get_diagnostics() -> List[Diagnostic]`
   - 获取编译过程中的诊断信息
   - 返回：诊断信息列表

4. `clear_diagnostics()`
   - 清除所有诊断信息

### 词法分析器 (`src/lexer/`)

#### `Lexer` 类

将源代码转换为词法标记。

**构造函数**
```python
def __init__(self, source: str)
```

**方法**
- `tokenize() -> List[Token]`: 将源代码转换为标记列表
- `get_errors() -> List[LexicalError]`: 获取词法错误

### 语法分析器 (`src/parser/`)

#### `Parser` 类

将词法标记转换为抽象语法树（AST）。

**构造函数**
```python
def __init__(self, tokens: List[Token])
```

**方法**
- `parse() -> ProgramNode`: 解析标记为AST
- `get_errors() -> List[ParseError]`: 获取语法错误

### 语义分析器 (`src/semantic/`)

#### `SemanticAnalyzerWithInference` 类

执行语义分析和类型推断。

**构造函数**
```python
def __init__(self, enable_inference: bool = True)
```

**方法**
- `analyze(ast: ProgramNode) -> Dict[str, Any]`: 分析AST并返回符号表
- `get_errors() -> List[SemanticError]`: 获取语义错误

### 代码生成器 (`src/codegen/`)

#### `PythonCodegen` 类

将AST转换为Python代码。

**构造函数**
```python
def __init__(self)
```

**方法**
- `generate(ast: ProgramNode) -> str`: 生成Python代码

### 运行时 (`src/runtime/`)

#### `SecureExecutor` 类

安全执行环境，替换不安全的`exec()`调用。

**构造函数**
```python
def __init__(self, allowed_modules: Optional[List[str]] = None)
```

**方法**
- `execute(code: str, context: Optional[Dict] = None) -> Any`: 安全执行代码
- `is_safe() -> bool`: 检查执行器是否安全
- `add_module(module_name: str) -> bool`: 添加允许的模块
- `remove_module(module_name: str) -> bool`: 移除允许的模块

## 错误处理系统 (`src/error_handling/`)

### `EnhancedErrorMessages` 类

提供增强的错误消息和修复建议。

**方法**
- `get_error_message(error_code: ErrorCode, **kwargs) -> str`: 获取错误消息
- `get_suggestion(error_code: ErrorCode, **kwargs) -> Optional[str]`: 获取修复建议
- `get_debug_info(error_code: ErrorCode, **kwargs) -> Optional[str]`: 获取调试信息

### `ErrorCode` 枚举

定义所有错误代码：
- `SYNTAX_ERROR`: 语法错误
- `LEXICAL_ERROR`: 词法错误
- `SEMANTIC_ERROR`: 语义错误
- `TYPE_ERROR`: 类型错误
- `NAME_ERROR`: 名称错误
- `RUNTIME_ERROR`: 运行时错误

## 数据类型

### 基本类型
- `数`: 整数或浮点数
- `文`: 字符串
- `真`: 布尔值 True
- `假`: 布尔值 False
- `空`: None 值
- `列表`: 列表
- `字典`: 字典
- `元组`: 元组

### 复合类型
- `函数`: 函数定义
- `类`: 类定义
- `模块`: 模块

## 内置函数

### 输入输出
- `印(...)`: 打印输出
- `输入(...)`: 读取输入

### 数学运算
- `加(a, b)`: 加法
- `减(a, b)`: 减法
- `乘(a, b)`: 乘法
- `除(a, b)`: 除法
- `取余(a, b)`: 取余
- `幂(a, b)`: 幂运算

### 类型转换
- `转整数(x)`: 转换为整数
- `转浮点数(x)`: 转换为浮点数
- `转字符串(x)`: 转换为字符串
- `转布尔值(x)`: 转换为布尔值

### 集合操作
- `长度(x)`: 获取长度
- `范围(...)`: 生成范围
- `排序(x)`: 排序
- `反转(x)`: 反转

## 语法参考

### 变量声明
```
变量 名称 = 值。
```

### 条件语句
```
若 条件 {
    # 代码块
} 否则 {
    # 代码块
}
```

### 循环语句
```
当 条件 {
    # 循环体
}

对于 变量 在 可迭代对象 {
    # 循环体
}
```

### 函数定义
```
函数 函数名(参数1, 参数2) {
    # 函数体
    返回 值
}
```

### 类定义
```
类 类名 {
    构造(参数) {
        # 构造函数
    }
    
    方法名(参数) {
        # 方法体
    }
}
```

## 示例代码

### Hello World
```
印"你好，世界！"。
```

### 计算阶乘
```
函数 阶乘(n) {
    若 n <= 1 {
        返回 1
    } 否则 {
        返回 n * 阶乘(n - 1)
    }
}

结果 = 阶乘(5)。
印"5的阶乘是：" + 转字符串(结果)。
```

### 列表操作
```
数字列表 = [1, 2, 3, 4, 5]。
和 = 0。

对于 数字 在 数字列表 {
    和 = 和 + 数字。
}

印"列表总和：" + 转字符串(和)。
```

## 错误代码参考

### 语法错误 (SYNTAX_ERROR)
- `SYNTAX_UNEXPECTED_TOKEN`: 意外的标记
- `SYNTAX_MISSING_TOKEN`: 缺少标记
- `SYNTAX_INVALID_EXPRESSION`: 无效表达式

### 词法错误 (LEXICAL_ERROR)
- `LEXICAL_UNKNOWN_CHAR`: 未知字符
- `LEXICAL_UNTERMINATED_STRING`: 未终止的字符串
- `LEXICAL_INVALID_NUMBER`: 无效数字

### 语义错误 (SEMANTIC_ERROR)
- `SEMANTIC_UNDEFINED_VARIABLE`: 未定义变量
- `SEMANTIC_DUPLICATE_DEFINITION`: 重复定义
- `SEMANTIC_TYPE_MISMATCH`: 类型不匹配

### 类型错误 (TYPE_ERROR)
- `TYPE_INVALID_OPERATION`: 无效操作
- `TYPE_INCOMPATIBLE_TYPES`: 不兼容类型
- `TYPE_MISSING_ATTRIBUTE`: 缺少属性

### 名称错误 (NAME_ERROR)
- `NAME_NOT_DEFINED`: 名称未定义
- `NAME_ALREADY_DEFINED`: 名称已定义
- `NAME_NOT_CALLABLE`: 名称不可调用

### 运行时错误 (RUNTIME_ERROR)
- `RUNTIME_DIVISION_BY_ZERO`: 除以零
- `RUNTIME_INDEX_OUT_OF_RANGE`: 索引越界
- `RUNTIME_KEY_ERROR`: 键错误

## 安全特性

### 安全执行环境
心语编译器默认启用安全执行环境，限制以下操作：
1. 文件系统访问
2. 网络访问
3. 系统命令执行
4. 危险的内置函数
5. 模块导入

### 允许的模块
默认只允许以下模块：
- `math`: 数学函数

可以通过`SecureExecutor.add_module()`添加其他模块。

## 性能优化

### 编译优化
- 常量折叠
- 死代码消除
- 内联优化

### 执行优化
- 即时编译（JIT）
- 缓存编译结果
- 内存管理优化

## 扩展性

### 自定义函数
可以通过上下文参数添加自定义函数：
```python
compiler = XinyuCompiler()
context = {
    '自定义函数': lambda x: x * 2
}
result = compiler.execute('印自定义函数(5)。', context)
```

### 模块系统
支持导入自定义模块：
```python
compiler = XinyuCompiler()
compiler.add_module('custom_module')
```

## 故障排除

### 常见问题

1. **编码问题**
   - 确保文件使用UTF-8编码
   - 在文件开头添加`# -*- coding: utf-8 -*-`

2. **导入错误**
   - 检查Python路径设置
   - 确保所有依赖已安装

3. **执行错误**
   - 检查安全限制
   - 验证上下文参数

### 调试技巧

1. 启用详细日志：
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. 检查诊断信息：
```python
compiler = XinyuCompiler()
compiler.compile(source)
diagnostics = compiler.get_diagnostics()
for d in diagnostics:
    print(d)
```

## 开发工具 API

### 代码格式化工具 (`tools/formatter.py`)

#### `XinyuFormatter` 类
心语代码格式化器，支持自定义格式化规则。

**构造函数**
```python
def __init__(self, config: Optional[FormatterConfig] = None)
```
- `config`: 格式化配置对象（可选）

**方法**

1. `format_code(source: str) -> str`
   - 格式化心语源代码
   - 参数：`source` - 心语源代码字符串
   - 返回：格式化后的代码字符串

2. `format_file(file_path: str) -> str`
   - 格式化文件中的心语代码
   - 参数：`file_path` - 文件路径
   - 返回：格式化后的代码字符串

3. `check_format(source: str) -> bool`
   - 检查代码格式是否符合规范
   - 参数：`source` - 心语源代码字符串
   - 返回：是否符合格式规范

#### `FormatterConfig` 类
格式化配置类，支持自定义格式化规则。

**属性**
- `indent_size: int` - 缩进大小（默认：4）
- `use_tabs: bool` - 是否使用制表符（默认：False）
- `space_around_operators: bool` - 操作符周围是否加空格（默认：True）
- `max_line_length: int` - 最大行长度（默认：100）
- `remove_trailing_whitespace: bool` - 是否删除行尾空格（默认：True）
- `ensure_newline_at_eof: bool` - 是否确保文件末尾有换行（默认：True）

### 格式化引擎 (`tools/format_engine.py`)

#### `ASTFormatter` 类
基于AST的代码格式化器。

**方法**
1. `visit(node: ASTNode) -> str`
   - 访问AST节点并返回格式化后的代码
   - 参数：`node` - AST节点
   - 返回：格式化后的代码字符串

2. `format_ast(ast: ASTNode) -> str`
   - 格式化整个AST
   - 参数：`ast` - AST根节点
   - 返回：格式化后的代码字符串

#### `FormatEngine` 类
格式化引擎，协调格式化过程。

**方法**
1. `format(source: str) -> str`
   - 格式化源代码
   - 参数：`source` - 源代码字符串
   - 返回：格式化后的代码字符串

2. `check(source: str) -> bool`
   - 检查代码格式
   - 参数：`source` - 源代码字符串
   - 返回：是否符合格式规范

### REPL历史管理器 (`src/repl/history_manager.py`)

#### `HistoryEntry` 数据类
历史记录条目。

**属性**
- `timestamp: datetime` - 时间戳
- `command: str` - 命令内容
- `result: Optional[str]` - 执行结果
- `command_type: CommandType` - 命令类型
- `execution_time: Optional[float]` - 执行时间（秒）
- `success: bool` - 是否成功
- `tags: List[str]` - 标签列表
- `metadata: Dict[str, Any]` - 元数据

#### `CommandType` 枚举
命令类型枚举。
- `EXPRESSION` - 表达式求值
- `STATEMENT` - 语句执行
- `DEFINITION` - 定义（函数、变量等）
- `IMPORT` - 导入语句
- `CONTROL` - 控制语句
- `DEBUG` - 调试命令
- `HELP` - 帮助命令
- `OTHER` - 其他命令

#### `HistoryManager` 类
历史记录管理器，支持增删改查、搜索、过滤等功能。

**构造函数**
```python
def __init__(self, max_size: int = 1000, history_file: Optional[Union[str, Path]] = None, use_database: bool = False)
```
- `max_size`: 最大历史记录数量（默认：1000）
- `history_file`: 历史记录文件路径（可选）
- `use_database`: 是否使用数据库存储（默认：False）

**方法**

1. `add_entry(command: str, result: Optional[str] = None, command_type: Optional[CommandType] = None, execution_time: Optional[float] = None, success: bool = True, tags: Optional[List[str]] = None, metadata: Optional[Dict[str, Any]] = None) -> HistoryEntry`
   - 添加历史记录条目
   - 返回：创建的HistoryEntry对象

2. `search(keyword: Optional[str] = None, command_type: Optional[CommandType] = None, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None, tags: Optional[List[str]] = None, success_only: bool = False, limit: Optional[int] = None) -> List[HistoryEntry]`
   - 搜索历史记录
   - 支持多种过滤条件
   - 返回：匹配的历史记录列表

3. `edit_and_reexecute(index: int, new_command: str) -> Optional[HistoryEntry]`
   - 编辑历史记录并重新执行
   - 参数：
     - `index`: 历史记录索引
     - `new_command`: 新命令
   - 返回：新创建的历史记录条目

4. `export_json(file_path: Union[str, Path]) -> bool`
   - 导出历史记录到JSON文件
   - 返回：是否成功

5. `import_json(file_path: Union[str, Path]) -> int`
   - 从JSON文件导入历史记录
   - 返回：导入的记录数量

6. `export_csv(file_path: Union[str, Path]) -> bool`
   - 导出历史记录到CSV文件
   - 返回：是否成功

7. `import_csv(file_path: Union[str, Path]) -> int`
   - 从CSV文件导入历史记录
   - 返回：导入的记录数量

8. `get_stats() -> Dict[str, Any]`
   - 获取历史记录统计信息
   - 返回：统计信息字典

9. `clear() -> None`
   - 清除所有历史记录

10. `__len__() -> int`
    - 获取历史记录数量

### 增强的REPL (`src/repl/enhanced_repl.py`)

#### `EnhancedREPL` 类
增强的REPL，支持历史记录管理。

**构造函数**
```python
def __init__(self, compiler: Any, history_file: Optional[str] = None, max_history_size: int = 1000)
```
- `compiler`: 编译器实例
- `history_file`: 历史记录文件路径（可选）
- `max_history_size`: 最大历史记录数量（默认：1000）

**方法**

1. `run_interactive() -> None`
   - 运行交互式REPL

2. `run_script(file_path: str) -> None`
   - 运行脚本文件

3. `run_command(command: str) -> Optional[str]`
   - 运行单个命令
   - 返回：执行结果

**历史命令接口**

REPL支持以下历史命令：
- `历史 列表 [数量]` - 显示历史记录
- `历史 搜索 <关键词>` - 搜索历史记录
- `历史 过滤 <类型>` - 按类型过滤历史记录
- `历史 统计` - 显示统计信息
- `历史 导出 <文件>` - 导出历史记录
- `历史 导入 <文件>` - 导入历史记录
- `历史 编辑 <编号> <新命令>` - 编辑历史记录并重新执行
- `历史 清除` - 清除所有历史记录

## 命令行工具

### 代码格式化工具 (`tools/xinyu_format.py`)

**使用方法**
```bash
# 格式化文件
python tools/xinyu_format.py format <文件或目录>

# 检查格式
python tools/xinyu_format.py check <文件或目录>

# 显示格式差异
python tools/xinyu_format.py diff <文件>

# 查看帮助
python tools/xinyu_format.py --help
```

**选项**
- `--config <文件>`: 指定配置文件路径
- `--in-place`: 原地修改文件
- `--verbose`: 显示详细信息
- `--quiet`: 静默模式

### 格式化工具安装脚本 (`tools/setup_formatter.py`)

**功能**
- 安装格式化工具到系统路径
- 创建配置文件模板
- 设置预提交钩子

**使用方法**
```bash
python tools/setup_formatter.py
```

## 预提交钩子

项目已配置预提交钩子，支持以下检查：

1. **xinyu-format**: 自动格式化心语代码
2. **black**: Python代码格式化
3. **isort**: 导入排序
4. **mypy**: 类型检查
5. **pytest**: 运行测试

**配置示例** (`.pre-commit-config.yaml`)
```yaml
repos:
  - repo: local
    hooks:
      - id: xinyu-format
        name: Format Xinyu code
        entry: python tools/xinyu_format.py format
        language: system
        files: \.xinyu$
        pass_filenames: true
```

## 版本历史

### v1.0.0 (当前)
- 基础语法支持
- 类型推断系统
- 安全执行环境
- 增强错误处理
- 模块化架构
- **增强的REPL历史记录管理**
- **代码格式化工具**
- **开发工具链集成**
- **预提交钩子支持**

### v1.1.0 (计划中)
- 更多内置函数
- 标准库扩展
- 性能优化
- IDE插件
- 调试器增强

### v1.2.0 (规划中)
- WebAssembly支持
- 多线程支持
- 数据库集成
- 图形界面
- 包管理器

## 贡献指南

### 开发环境设置
1. 克隆仓库
2. 安装依赖：`pip install -r requirements.txt`
3. 运行测试：`pytest`

### 代码规范
- 使用Black进行代码格式化
- 使用isort整理导入顺序
- 使用mypy进行类型检查
- 遵循PEP 8规范

### 提交规范
- 使用Conventional Commits格式
- 包含测试用例
- 更新相关文档

## 许可证

本项目采用MIT许可证。详见LICENSE文件。