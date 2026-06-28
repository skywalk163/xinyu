# 项目目录结构说明

## 根目录文件

```
chineseprogram/
├── .autocoderignore          # 自动编码器忽略文件
├── .coverage                 # 测试覆盖率报告
├── .gitignore                # Git忽略文件
├── .pre-commit-config.yaml   # Pre-commit配置
├── CONTRIBUTING.md           # 贡献指南
├── mypy.ini                  # MyPy类型检查配置
├── pyproject.toml            # 项目配置
├── pytest.ini                # Pytest配置
├── README.md                 # 项目主README
├── README_BUILTIN.md         # 内置函数模块README
└── requirements.txt          # 依赖列表
```

## 主要目录

### 1. src/ - 源代码目录

```
src/
├── builtin/                  # 内置函数模块
│   ├── __init__.py
│   ├── registry.py          # 内置函数注册表
│   ├── name_mapper.py       # 中文命名映射器
│   ├── docs.py              # 文档管理
│   ├── builtin_docs.py      # 内置函数详细文档
│   ├── chinese_help.py      # 中文帮助系统
│   └── functions/           # 内置函数实现
│       ├── __init__.py
│       ├── math_funcs.py    # 数学函数
│       ├── type_funcs.py    # 类型转换函数
│       ├── sequence_funcs.py # 序列操作函数
│       ├── object_funcs.py  # 对象操作函数
│       ├── io_funcs.py      # IO函数
│       └── other_funcs.py   # 其他函数
│
├── module/                   # 模块管理
│   ├── __init__.py
│   ├── manager.py           # 模块管理器
│   ├── loader.py            # 模块加载器
│   └── wrappers/            # 标准库模块中文封装（57个）
│       ├── __init__.py
│       ├── base_wrapper.py
│       ├── math_wrapper.py
│       ├── os_wrapper.py
│       ├── sys_wrapper.py
│       ├── json_wrapper.py
│       ├── datetime_wrapper.py
│       ├── re_wrapper.py
│       ├── collections_wrapper.py
│       ├── itertools_wrapper.py
│       ├── functools_wrapper.py
│       ├── random_wrapper.py
│       ├── pathlib_wrapper.py
│       ├── time_wrapper.py
│       ├── string_wrapper.py
│       ├── textwrap_wrapper.py
│       ├── copy_wrapper.py
│       ├── pprint_wrapper.py
│       ├── pickle_wrapper.py
│       ├── csv_wrapper.py
│       ├── hashlib_wrapper.py
│       ├── shutil_wrapper.py
│       ├── glob_wrapper.py
│       ├── argparse_wrapper.py
│       ├── logging_wrapper.py
│       ├── threading_wrapper.py
│       ├── queue_wrapper.py
│       ├── decimal_wrapper.py
│       ├── statistics_wrapper.py
│       ├── socket_wrapper.py
│       ├── ssl_wrapper.py
│       ├── http_wrapper.py
│       ├── urllib_wrapper.py
│       ├── zlib_wrapper.py
│       ├── gzip_wrapper.py
│       ├── zipfile_wrapper.py
│       ├── tarfile_wrapper.py
│       ├── sqlite3_wrapper.py
│       ├── dbm_wrapper.py
│       ├── unittest_wrapper.py
│       ├── doctest_wrapper.py
│       ├── asyncio_wrapper.py
│       ├── tkinter_wrapper.py
│       ├── base64_wrapper.py
│       ├── configparser_wrapper.py
│       ├── subprocess_wrapper.py
│       ├── secrets_wrapper.py
│       ├── typing_wrapper.py
│       ├── inspect_wrapper.py
│       ├── traceback_wrapper.py
│       ├── gettext_wrapper.py
│       ├── locale_wrapper.py
│       ├── xml_etree_wrapper.py
│       ├── struct_wrapper.py
│       ├── tempfile_wrapper.py
│       ├── fnmatch_wrapper.py
│       ├── linecache_wrapper.py
│       ├── bisect_wrapper.py
│       └── heapq_wrapper.py
│
├── validation/               # 参数验证
│   ├── __init__.py
│   ├── param_validator.py   # 参数验证器
│   └── type_inference.py    # 类型推断
│
├── exception/                # 异常处理
│   ├── __init__.py
│   ├── translator.py        # 异常转换器
│   └── xinyu_exceptions.py  # 心语异常类
│
└── config/                   # 配置文件
    └── builtin_config.py    # 内置函数配置
```

### 2. tests/ - 测试目录

```
tests/
└── builtin_tests/            # 内置函数测试
    ├── test_builtin_implementation.py  # 基础测试
    ├── test_enhanced_features.py       # 增强功能测试
    ├── test_all_stdlib_modules.py      # 所有模块测试
    ├── test_extended_modules.py        # 扩展模块测试
    ├── test_utility_modules.py         # 实用模块测试
    └── test_new_modules.py             # 新增模块测试
```

### 3. docs/ - 文档目录

```
docs/
└── builtin_docs/             # 内置函数文档
    ├── USER_MANUAL.md                    # 用户手册
    ├── STDLIB_INDEX.md                   # 标准库索引
    ├── BUILTIN_IMPLEMENTATION_SUMMARY.md # 实现总结
    └── DOCUMENTATION_INDEX.md            # 文档索引
```

### 4. examples/ - 示例目录

```
examples/
└── chinese_builtin_demo.py   # 中文编程示例
```

### 5. config/ - 配置目录

```
config/
└── builtin_config.py         # 内置函数配置
```

## 文件统计

| 类别 | 数量 |
|------|------|
| 源代码文件 | ~70个 |
| 测试文件 | 6个 |
| 文档文件 | 4个 |
| 配置文件 | 2个 |
| Wrapper文件 | 57个 |

## 关键文件说明

### 核心实现文件

1. **src/builtin/registry.py** - 内置函数注册表，管理所有69个内置函数
2. **src/builtin/name_mapper.py** - 中文命名映射器，提供中英文双向映射
3. **src/module/manager.py** - 模块管理器，管理所有57个标准库模块
4. **src/module/wrappers/base_wrapper.py** - 基础封装类，所有模块封装的基类

### 核心文档文件

1. **docs/builtin_docs/USER_MANUAL.md** - 完整的用户使用手册
2. **docs/builtin_docs/STDLIB_INDEX.md** - 所有57个模块的详细说明
3. **docs/builtin_docs/BUILTIN_IMPLEMENTATION_SUMMARY.md** - 技术实现总结
4. **docs/builtin_docs/DOCUMENTATION_INDEX.md** - 文档总索引

### 核心测试文件

1. **tests/builtin_tests/test_builtin_implementation.py** - 69个内置函数测试
2. **tests/builtin_tests/test_all_stdlib_modules.py** - 57个模块测试

## 使用指南

### 查看文档

```bash
# 查看用户手册
cat docs/builtin_docs/USER_MANUAL.md

# 查看标准库索引
cat docs/builtin_docs/STDLIB_INDEX.md
```

### 运行测试

```bash
# 运行所有测试
python -m pytest tests/builtin_tests/

# 运行特定测试
python tests/builtin_tests/test_builtin_implementation.py
```

### 查看示例

```bash
# 运行示例
python examples/chinese_builtin_demo.py
```

---

**目录结构清晰，文件组织有序！**
