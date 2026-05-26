# 心语 (Xīn Yǔ)

**一门极简的中文编程语言**

心语，寓意"从心而发，自然表达"。这是一门只有5个核心关键字的中文编程语言，让代码如心声般自然流淌。

## 核心特性

### 极简关键字

只有5个核心关键字，其他功能通过函数和宏实现：

- `定` - 定义变量
- `函` - 定义函数
- `若` - 条件判断
- `真值` - 布尔真值值
- `假值` - 布尔假值值

### 语境驱动

支持语境省略，让代码更贴近自然语言：

```
# 传统方式
定义 x = 5。
打印 x。

# 语境驱动
x = 5。
打印 x。
```

### 中文操作符

使用中文操作符，更符合中文思维：

```
1相加2      # 相加法
3相乘4      # 相乘法
x大于遍历5    # 比较
真值并且假值    # 逻辑运算
```

### 函数式编程

支持高阶函数和管道操作：

```
定义 平方 = 函数 x：x相乘x。

列表。映射(平方)。过滤(函数 x：x大于遍历10)。打印。
```

## 快速开始

### 安装

```bash
git clone https://github.com/yourname/xinyu.git
cd xinyu
pip install -r requirements.txt
```

### 运行

```python
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.codegen.python_codegen import PythonCodegen

# 编译心语代码
source = """
定义 x = 5。
打印 x。
"""

lexer = Lexer(source)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
codegen = PythonCodegen()
python_code = codegen.generate(ast)

# 执行生成的Python代码
exec(python_code)  # 输出: 5
```

### 安全限制

**重要安全提示：**

心语语言使用 `exec()` 执行生成的 Python 代码。在生产环境中使用时，请注意以下安全限制：

1. **代码来源审查**：仅执行经过审查的代码，避免执行不可信来源的代码
2. **沙箱隔离**：建议在沙箱环境（如 Docker 容器）中隔离执行
3. **权限限制**：限制可用的 Python 模块和函数，避免访问敏感资源
4. **输入验证**：对用户输入进行严格验证，防止代码注入攻击

在受信任的环境中（如本地开发、教育场景），心语语言是安全的。但在面向公众的服务中，务必实施额外的安全措施。

## 示例代码

### Hello World

```
打印 "你好，心语！"。
```

### 斐波那契数列

```
定义 斐波那契 = 函数 n：
  如果 n小于遍历2：
    返回 n。
  否那么：
    返回 斐波那契(n相减1)相加斐波那契(n相减2)。

打印 斐波那契(10)。
```

### 遍历循环

```
遍历 i 遍历 【1， 2， 3， 4， 5】：
  打印 i。
```

### 条件判断

```
定义 x = 10。

如果 x大于遍历0：
  打印 "正数"。
否那么如果 x小于遍历0：
  打印 "负数"。
否那么：
  打印 "零"。
```

## 项目架构

```
src/
├── lexer/          # 词法分析器
│   ├── tokens.py   # Token定义
│   ├── keywords.py # 关键字映射
│   └── lexer.py    # 词法分析器实现
├── parser/         # 语法分析器
│   ├── ast_nodes.py # AST节点定义
│   └── parser.py   # 语法分析器实现
├── semantic/       # 语义分析器
│   ├── scope.py    # 作用域管理
│   └── analyzer.py # 语义分析器实现
├── codegen/        # 代码生成器
│   └── python_codegen.py # Python代码生成
└── runtime/        # 运行时环境（待实现）
```

## 开发状态

- ✅ 词法分析器（支持中文标识符、关键字、操作符）
- ✅ 语法分析器（支持表达式、控制流、函数定义）
- ✅ 语义分析器（作用域管理、类型推断、错误检测）
- ✅ Python代码生成器（生成可执行Python代码）
- ✅ 错误处理系统（统一错误处理和报告）
- ✅ 类型推断系统（自动类型推断）
- ✅ 宏系统（内置宏和成语宏）
- ⏳ 运行时环境（开发中）
- ⏳ 标准库（规划中）
- ⏳ 示例程序（规划中）

## 开发指南

### 环境设置

```bash
# 克隆仓库
git clone https://github.com/yourname/xinyu.git
cd xinyu

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖
pip install pytest pytest-cov pytest-asyncio
```

### 项目结构

```
chineseprogram/
├── src/                    # 源代码
│   ├── lexer/             # 词法分析器
│   │   ├── tokens.py      # Token定义
│   │   ├── keywords.py    # 关键字映射
│   │   ├── lexer.py       # 词法分析器实现
│   │   └── lexer_with_error_handler.py  # 增强版词法分析器
│   ├── parser/            # 语法分析器
│   │   ├── ast_nodes.py   # AST节点定义
│   │   ├── parser.py      # 语法分析器实现
│   │   └── parser_with_error_handler.py # 增强版语法分析器
│   ├── semantic/          # 语义分析器
│   │   ├── scope.py       # 作用域管理
│   │   ├── analyzer.py    # 语义分析器实现
│   │   ├── analyzer_with_inference.py  # 增强版语义分析器
│   │   └── type_inference.py  # 类型推断系统
│   ├── codegen/           # 代码生成器
│   │   └── python_codegen.py  # Python代码生成
│   ├── macro/             # 宏系统
│   │   ├── macro_system.py    # 宏系统核心
│   │   ├── macro_expander.py  # 宏展开器
│   │   ├── builtin_macros.py  # 内置宏
│   │   └── idiom_macros.py    # 成语宏
│   ├── error_handling.py  # 统一错误处理
│   └── main.py            # 主入口
├── tests/                 # 测试文件
│   ├── test_lexer.py      # 词法分析器测试
│   ├── test_parser.py     # 语法分析器测试
│   ├── test_semantic.py   # 语义分析器测试
│   ├── test_codegen.py    # 代码生成器测试
│   ├── test_main.py       # 主程序测试
│   └── ...                # 其他测试
├── docs/                  # 文档
│   └── integration_guide.md  # 集成版本使用指南
├── examples/              # 示例代码
└── README.md              # 项目说明
```

### 编译流程

心语语言的编译流程分为以下几个阶段：

1. **词法分析** (Lexer)
   - 将源代码转换为Token序列
   - 识别中文关键字、操作符、标识符

2. **语法分析** (Parser)
   - 将Token序列转换为抽象语法树(AST)
   - 支持递归下降解析

3. **语义分析** (Semantic Analyzer)
   - 作用域管理和符号表构建
   - 类型检查和推断
   - 错误检测

4. **宏展开** (Macro Expander)
   - 展开宏调用
   - 代码转换和优化

5. **代码生成** (Code Generator)
   - 将AST转换为目标代码（Python）
   - 生成可执行代码

### 添相加新功能

#### 添相加新的关键字

1. 在 `src/lexer/keywords.py` 中添相加关键字映射
2. 在 `src/lexer/tokens.py` 中添相加对应的TokenType
3. 在 `src/lexer/lexer.py` 中实现识别逻辑
4. 在 `src/parser/parser.py` 中实现解析逻辑
5. 添相加相应的测试

#### 添相加新的操作符

1. 在 `src/lexer/tokens.py` 中定义TokenType
2. 在 `src/lexer/lexer.py` 中实现识别逻辑
3. 在 `src/parser/parser.py` 中实现解析逻辑
4. 在 `src/codegen/python_codegen.py` 中实现代码生成
5. 添相加相应的测试

#### 添相加新的AST节点

1. 在 `src/parser/ast_nodes.py` 中定义节点类
2. 在 `src/parser/parser.py` 中实现解析逻辑
3. 在 `src/semantic/analyzer.py` 中实现语义分析
4. 在 `src/codegen/python_codegen.py` 中实现代码生成
5. 添相加相应的测试

### 代码规范

- 使用Python 3.8+特性
- 遵循PEP 8代码风格
- 使用类型注解
- 编写文档字符串（中文）
- 保持测试覆盖率在70%以上

### 提交代码

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 测试覆盖

- 总测试数：348个
- 通过率：100%（348通过，2跳过）
- 代码覆盖率：77%

### 运行测试

```bash
# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=src --cov-report=html

# 运行特定测试文件
pytest tests/test_lexer.py -v
```

## 设计哲学

### 极简主义

受Lisp启发，心语坚持"少即是多"的设计哲学。只有5个核心关键字，其他功能通过函数和宏扩展，让语言本身保持简洁优雅。

### 语境驱动

中文编程的独特之处在遍历语境。心语支持语境省略，让代码更贴近自然语言的表达方式，降低学习曲线。

### 自然流畅

代码应该像心声一样自然流淌。心语的语法设计遵循中文思维习惯，让编程成为一种愉悦的表达过程。

## 致谢

心语的设计灵感来源遍历：

- **Lisp** - 极简关键字和宏系统
- **Python** - 缩进语法和简洁哲学
- **文言** - 中文编程的先驱探索
- **言语言** - 元数驱动解析的创新

## 许可证

MIT License

## 贡献

欢迎贡献代码、报告问题或者提出建议！

---

**心语 - 从心而发，自然表达**
