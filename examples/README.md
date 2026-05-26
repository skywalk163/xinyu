# 心语语言示例

本目录包含心语语言的各种示例程序，展示语言的不同特性和用法。

## 目录结构

```
examples/
├── basic/              # 基础示例
│   ├── hello.心语      # Hello World
│   ├── variables.心语  # 变量定义
│   ├── operators.心语  # 操作符使用
│   └── control.心语    # 控制流
├── advanced/           # 高级示例
│   ├── functions.心语  # 函数定义
│   ├── recursion.心语  # 递归
│   ├── macros.心语     # 宏使用
│   └── closures.心语   # 闭包
└── README.md           # 本文档
```

## 基础示例

### 1. Hello World

文件：`basic/hello.心语`

```心语
印 "你好，心语！"。
```

这是最简单的心语程序，输出问候语。

### 2. 变量定义

文件：`basic/variables.心语`

```心语
# 定义数字变量
定 数字 = 42。

# 定义字符串变量
定 消息 = "欢迎使用心语"。

# 定义布尔变量
定 是真的 = 真。

# 输出变量
印 数字。
印 消息。
印 是真的。
```

展示如何定义不同类型的变量。

### 3. 操作符使用

文件：`basic/operators.心语`

```心语
# 算术运算
定 加法结果 = 10 加 20。
定 减法结果 = 30 减 15。
定 乘法结果 = 5 乘 6。
定 除法结果 = 20 除 4。

# 比较运算
定 大于结果 = 10 大 5。
定 小于结果 = 3 小 8。
定 等于结果 = 5 等于 5。

# 逻辑运算
定 且结果 = 真 且 假。
定 或结果 = 真 或 假。
定 非结果 = 非 真。

# 输出结果
印 加法结果。
印 乘法结果。
印 大于结果。
印 且结果。
```

展示各种中文操作符的使用。

### 4. 控制流

文件：`basic/control.心语`

```心语
# 条件语句
定 分数 = 85。

若 分数 大 90 则：
    印 "优秀"。
否则若 分数 大 80 则：
    印 "良好"。
否则若 分数 大 60 则：
    印 "及格"。
否则：
    印 "不及格"。

# 当循环
定 计数 = 0。
当 计数 小 5：
    印 计数。
    计数 = 计数 加 1。

# 遍历循环
遍历 项目 于 【1， 2， 3， 4， 5】：
    印 项目。
```

展示条件语句和循环的使用。

## 高级示例

### 1. 函数定义

文件：`advanced/functions.心语`

```心语
# 定义简单函数
定义 问候(名字)：
    印 "你好，" 加 名字 加 "！"。

# 定义带返回值的函数
定义 平方(x)：
    返回 x 乘 x。

# 定义多参数函数
定义 加法(a, b)：
    返回 a 加 b。

# 调用函数
问候("心语")。
定 结果 = 平方(5)。
印 结果。
印 加法(10, 20)。
```

展示函数的定义和调用。

### 2. 递归

文件：`advanced/recursion.心语`

```心语
# 斐波那契数列
定义 斐波那契(n)：
    若 n 小 2 则：
        返回 n。
    否则：
        返回 斐波那契(n 减 1) 加 斐波那契(n 减 2)。

# 阶乘
定义 阶乘(n)：
    若 n 等于 0 则：
        返回 1。
    否则：
        返回 n 乘 阶乘(n 减 1)。

# 测试
印 斐波那契(10)。
印 阶乘(5)。
```

展示递归函数的实现。

### 3. 宏使用

文件：`advanced/macros.心语`

```心语
# 使用内置宏
重复 5 次：
    印 "重复执行"。

# 使用成语宏
胸有成竹：
    定 x = 10。
    定 y = 20。
    印 x 加 y。

# 自定义宏
定义宏 简化打印(内容)：
    印 内容。

简化打印 "使用宏简化代码"。
```

展示宏系统的使用。

### 4. 闭包

文件：`advanced/closures.心语`

```心语
# 创建计数器
定义 创建计数器()：
    定 计数 = 0。
    定义 增加()：
        计数 = 计数 加 1。
        返回 计数。
    返回 增加。

# 使用闭包
定 我的计数器 = 创建计数器()。
印 我的计数器()。
印 我的计数器()。
印 我的计数器()。
```

展示闭包和高阶函数的使用。

## 运行示例

### 方法一：使用主程序

```python
from src.main import ChineseProgram

# 创建程序实例
program = ChineseProgram()

# 读取示例文件
with open('examples/basic/hello.心语', 'r', encoding='utf-8') as f:
    source = f.read()

# 运行代码
program.run(source)
```

### 方法二：使用命令行

```bash
# 运行单个文件
python -m src.main examples/basic/hello.心语

# 进入交互模式
python -m src.main
```

### 方法三：手动编译

```python
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.codegen.python_codegen import PythonCodegen

# 读取源代码
with open('examples/basic/hello.心语', 'r', encoding='utf-8') as f:
    source = f.read()

# 编译流程
lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

analyzer = SemanticAnalyzer()
analyzer.analyze(ast)

codegen = PythonCodegen()
python_code = codegen.generate(ast)

# 执行生成的Python代码
exec(python_code)
```

## 示例说明

### 基础示例

基础示例展示了心语语言的基本语法和功能：

- **hello.心语** - 最简单的程序，输出问候语
- **variables.心语** - 变量定义和使用
- **operators.心语** - 各种操作符的使用
- **control.心语** - 控制流语句

这些示例适合初学者，帮助理解语言的基本概念。

### 高级示例

高级示例展示了心语语言的高级特性：

- **functions.心语** - 函数定义和调用
- **recursion.心语** - 递归函数
- **macros.心语** - 宏系统
- **closures.心语** - 闭包和高阶函数

这些示例适合有一定编程经验的用户，展示语言的强大功能。

## 学习路径

建议按照以下顺序学习：

1. **基础语法** (1-2天)
   - hello.心语
   - variables.心语
   - operators.心语

2. **控制流** (1-2天)
   - control.心语
   - 理解条件语句和循环

3. **函数** (2-3天)
   - functions.心语
   - recursion.心语
   - 理解函数定义和调用

4. **高级特性** (3-5天)
   - macros.心语
   - closures.心语
   - 理解宏和闭包

## 贡献示例

欢迎贡献新的示例！请遵循以下规范：

1. **文件命名**：使用有意义的名称，如 `fibonacci.心语`
2. **代码注释**：添加中文注释说明代码功能
3. **测试验证**：确保示例可以正常运行
4. **文档更新**：在本README中添加示例说明

## 常见问题

### Q: 如何调试示例代码？

A: 可以使用以下方法：

```python
from src.main import ChineseProgram

program = ChineseProgram()

# 编译但不执行
source = "定 x = 42。"
python_code = program.compile(source)
print(python_code)  # 查看生成的Python代码
```

### Q: 示例运行出错怎么办？

A: 请检查：
1. 文件编码是否为UTF-8
2. 语法是否正确
3. 是否使用了支持的功能

### Q: 如何创建自己的示例？

A: 参考 `basic/` 目录中的示例，创建新的 `.心语` 文件。

## 更多资源

- [语言文档](../README.md)
- [开发指南](../README.md#开发指南)
- [集成指南](../docs/integration_guide.md)

---

**心语 - 从心而发，自然表达**
