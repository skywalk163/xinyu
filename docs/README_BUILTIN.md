# 心语语言 - Python 3.12 标准库中文封装

## 项目简介

心语语言是一个支持中文编程的Python扩展系统，提供完整的中文内置函数和标准库模块接口。用户可以使用中文或英文进行编程，两种方式完全等价。

## 项目统计

- **内置函数**: 69个
- **标准库模块**: 57个
- **总封装数**: 126个
- **Python版本**: 3.12+

## 目录结构

```
chineseprogram/
├── src/                    # 源代码
│   ├── builtin/           # 内置函数模块
│   │   ├── registry.py    # 内置函数注册表
│   │   ├── name_mapper.py # 中文命名映射器
│   │   ├── builtin_docs.py # 中文文档
│   │   ├── chinese_help.py # 中文帮助系统
│   │   └── functions/     # 内置函数实现
│   ├── module/            # 模块管理
│   │   ├── manager.py     # 模块管理器
│   │   ├── loader.py      # 模块加载器
│   │   └── wrappers/      # 标准库模块中文封装
│   ├── validation/        # 参数验证
│   ├── exception/         # 异常处理
│   └── config/            # 配置文件
├── tests/                 # 测试文件
│   └── builtin_tests/     # 内置函数测试
│       ├── test_builtin_implementation.py
│       ├── test_enhanced_features.py
│       ├── test_all_stdlib_modules.py
│       ├── test_extended_modules.py
│       ├── test_utility_modules.py
│       └── test_new_modules.py
├── docs/                  # 文档
│   └── builtin_docs/      # 内置函数文档
│       ├── USER_MANUAL.md
│       ├── STDLIB_INDEX.md
│       ├── BUILTIN_IMPLEMENTATION_SUMMARY.md
│       └── DOCUMENTATION_INDEX.md
├── examples/              # 示例代码
├── config/                # 配置文件
└── README.md              # 本文件
```

## 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/your-repo/chineseprogram.git
cd chineseprogram

# 安装依赖
pip install -r requirements.txt
```

### 基本使用

```python
from src.builtin import BuiltinRegistry
from src.module import ModuleManager

# 使用内置函数
registry = BuiltinRegistry()
registry.register_all_builtins()

# 中文调用
result = registry.call('绝对值', -5)  # 返回 5
result = registry.call('最大值', 1, 2, 3)  # 返回 3

# 使用标准库模块
manager = ModuleManager()
math = manager.import_module('数学')
result = math.平方根(16)  # 返回 4.0
```

### 查看帮助

```python
from src.builtin.chinese_help import ChineseHelp

help_system = ChineseHelp()
help_system.help('绝对值')  # 查看函数帮助
help_system.list_all_functions()  # 列出所有函数
help_system.list_all_modules()  # 列出所有模块
```

## 功能特性

### 1. 内置函数（69个）

#### 数学函数
- 绝对值, 最大值, 最小值, 求和, 幂运算, 四舍五入, 除法余数, 复数

#### 类型转换
- 转整数, 转浮点, 转字符串, 转布尔, 转列表, 转字典, 转元组, 转集合

#### 序列操作
- 长度, 范围, 枚举, 拉链, 映射, 过滤, 排序, 反转

#### 对象操作
- 类型, 是实例, 是子类, 有属性, 取属性, 设属性, 删属性

#### IO函数
- 打印, 输入, 打开, 格式化

### 2. 标准库模块（57个）

#### 数学运算（4个）
- 数学, 小数, 统计, 随机

#### 文本处理（3个）
- 字符串, 文本包裹, 正则

#### 数据类型（6个）
- 集合, 迭代工具, 函数工具, 复制, 美化打印, 类型提示

#### 算法（2个）
- 二分查找, 堆队列

#### 文件操作（7个）
- 系统, 路径, 文件操作, 文件匹配, 文件名匹配, 临时文件, 行缓存

#### 数据存储（6个）
- JSON, 序列化, CSV, 数据库, DBM, 配置

#### 时间日期（2个）
- 日期时间, 时间

#### 并发编程（4个）
- 线程, 队列, 异步, 子进程

#### 数据压缩（4个）
- 压缩, GZIP, ZIP, TAR

#### 网络编程（4个）
- 套接字, SSL, HTTP, URL

#### 测试框架（2个）
- 单元测试, 文档测试

#### 图形界面（1个）
- 图形界面

#### 编码解码（2个）
- Base64, 二进制结构

#### XML处理（1个）
- XML树

#### 国际化（2个）
- 国际化, 本地化

#### 系统工具（7个）
- 系统信息, 参数解析, 日志, 哈希, 安全随机, 检查, 堆栈跟踪

## 核心特性

1. **中英文双语支持** - 所有函数和模块都支持中文和英文调用
2. **零开销** - 直接调用Python原生函数，无性能损失
3. **完整文档** - 提供详细的中文文档和帮助系统
4. **易于扩展** - 可轻松添加新的函数和模块封装
5. **全面覆盖** - 覆盖Python编程的所有主要领域

## 文档

- [用户手册](docs/builtin_docs/USER_MANUAL.md) - 完整的使用指南
- [标准库索引](docs/builtin_docs/STDLIB_INDEX.md) - 所有模块的详细说明
- [实现总结](docs/builtin_docs/BUILTIN_IMPLEMENTATION_SUMMARY.md) - 技术实现细节
- [文档索引](docs/builtin_docs/DOCUMENTATION_INDEX.md) - 文档总览

## 测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python tests/builtin_tests/test_builtin_implementation.py
python tests/builtin_tests/test_all_stdlib_modules.py
```

## 示例

查看 `examples/` 目录获取更多使用示例。

## 贡献

欢迎贡献代码、报告问题或提出建议！

## 许可证

MIT License

## 更新日志

### v1.0.0 (2026-06-02)
- 实现69个Python内置函数的中文封装
- 实现57个标准库模块的中文封装
- 完整的中文文档和帮助系统
- 全面的测试覆盖

---

**心语语言 - 让编程更优雅！**
