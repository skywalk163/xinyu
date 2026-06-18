# 心语 (Xin Yu) - 中文编程语言

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://github.com/yourusername/xinyu/actions)
[![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen.svg)](https://github.com/yourusername/xinyu/actions)

心语是一个专为中文使用者设计的编程语言，使用中文关键字和语法，让编程更加直观易懂。

## ✨ 特性

- **中文语法**：使用中文关键字和语法，降低学习门槛
- **类型推断**：自动推断变量类型，减少类型声明
- **安全执行**：内置安全沙箱，防止危险操作
- **错误友好**：中文错误信息和修复建议
- **模块化架构**：清晰的组件分离和接口设计
- **高性能**：优化的编译和执行性能
- **增强的REPL**：支持历史记录管理、搜索、过滤、编辑和重新执行
- **代码格式化工具**：自动格式化心语代码，支持自定义规则
- **开发工具链**：完整的开发工具支持，提升开发效率

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/xinyu.git
cd xinyu

# 安装依赖
pip install -r requirements.txt
```

### 第一个程序

创建 `hello.xinyu` 文件：
```
印"你好，世界！"。
```

运行程序：
```bash
python src/main.py hello.xinyu
```

输出：
```
你好，世界！
```

### 交互式使用

```bash
# 启动交互式解释器
python src/main.py

# 或直接运行代码
python src/main.py -c '印"你好，心语！"。'

# 使用增强的REPL（支持历史记录管理）
python src/repl/enhanced_repl.py
```

### 使用代码格式化工具

```bash
# 格式化单个文件
python tools/xinyu_format.py format example.xinyu

# 检查代码格式
python tools/xinyu_format.py check example.xinyu

# 格式化目录下所有文件
python tools/xinyu_format.py format src/

# 查看格式化工具帮助
python tools/xinyu_format.py --help
```

### 使用增强的REPL历史功能

启动增强REPL后，可以使用以下历史命令：

```
心语> 历史 列表          # 显示历史记录
心语> 历史 搜索 定义     # 搜索包含"定义"的历史
心语> 历史 过滤 definition  # 按类型过滤
心语> 历史 统计          # 显示统计信息
心语> 历史 导出 history.json  # 导出历史记录
心语> 历史 导入 history.json  # 导入历史记录
心语> 历史 编辑 0 新命令  # 编辑历史记录并重新执行
心语> 历史 清除          # 清除所有历史记录
```

## 📖 语言特性

### 变量和类型
```
变量 姓名 = "张三"
变量 年龄 = 25
变量 身高 = 1.75
变量 是学生 = 真
```

### 控制流
```
若 分数 >= 90 {
    印"优秀"
} 否则若 分数 >= 80 {
    印"良好"
} 否则 {
    印"继续努力"
}

当 计数 < 10 {
    印计数
    计数 = 计数 + 1
}

对于 水果 在 ["苹果", "香蕉", "橙子"] {
    印"我喜欢" + 水果
}
```

### 函数
```
函数 问候(姓名) {
    返回 "你好，" + 姓名 + "！"
}

印问候("世界")  # 输出：你好，世界！
```

### 类和对象
```
类 学生 {
    构造(姓名, 年龄) {
        自我.姓名 = 姓名
        自我.年龄 = 年龄
    }

    函数 介绍() {
        返回 "我是" + 自我.姓名 + "，今年" + 转字符串(自我.年龄) + "岁"
    }
}

张三 = 学生("张三", 20)
印张三.介绍()  # 输出：我是张三，今年20岁
```

## 📁 项目结构

```
xinyu/
├── src/                    # 源代码
│   ├── core/              # 核心接口
│   │   ├── __init__.py    # 核心接口定义
│   │   └── compiler.py    # 编译器主类
│   ├── lexer/             # 词法分析
│   ├── parser/            # 语法分析
│   ├── semantic/          # 语义分析
│   ├── codegen/           # 代码生成
│   ├── runtime/           # 运行时
│   ├── error_handling/    # 错误处理
│   └── repl/              # REPL交互式解释器
│       ├── __init__.py
│       ├── enhanced_repl.py      # 增强的REPL（支持历史记录管理）
│       └── history_manager.py    # 历史记录管理器
├── tools/                  # 开发工具
│   ├── __init__.py
│   ├── formatter.py       # 代码格式化器
│   ├── format_engine.py   # 格式化引擎
│   ├── xinyu_format.py    # 格式化命令行工具
│   └── setup_formatter.py # 格式化工具安装脚本
├── tests/                 # 测试代码
├── docs/                  # 文档
│   ├── API_REFERENCE.md   # API参考
│   ├── USER_GUIDE.md      # 用户指南
│   ├── formatter_usage.md # 格式化工具使用指南
│   └── repl_history_enhancement.md  # REPL历史增强功能文档
├── examples/              # 示例代码
├── .xinyu-formatter.yaml  # 代码格式化配置
├── .pre-commit-config.yaml # 预提交钩子配置
├── requirements.txt       # 依赖列表
└── README.md             # 本文件
```

## 🔧 开发指南

### 环境设置

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装开发依赖
pip install -r requirements-dev.txt
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_lexer.py

# 带覆盖率报告
pytest --cov=src --cov-report=html
```

### 代码规范

```bash
# 代码格式化
black src/ tests/

# 导入排序
isort src/ tests/

# 类型检查
mypy src/

# 心语代码格式化
python tools/xinyu_format.py format src/ tests/

# 检查心语代码格式
python tools/xinyu_format.py check src/ tests/
```

### 预提交钩子

项目已配置预提交钩子，自动检查代码质量：

```bash
# 安装预提交钩子
pre-commit install

# 手动运行所有钩子
pre-commit run --all-files

# 运行特定钩子
pre-commit run xinyu-format --all-files
```

预提交钩子包括：
- `xinyu-format`: 自动格式化心语代码
- `black`: Python代码格式化
- `isort`: 导入排序
- `mypy`: 类型检查
- `pytest`: 运行测试

### CI/CD 流水线

项目配置了完整的CI/CD流水线，自动化构建、测试和发布流程：

#### 状态徽章
[![代码质量检查](https://github.com/yourusername/xinyu-lang/actions/workflows/quality.yml/badge.svg)](https://github.com/yourusername/xinyu-lang/actions/workflows/quality.yml)
[![测试套件](https://github.com/yourusername/xinyu-lang/actions/workflows/test.yml/badge.svg)](https://github.com/yourusername/xinyu-lang/actions/workflows/test.yml)
[![发布状态](https://github.com/yourusername/xinyu-lang/actions/workflows/release.yml/badge.svg)](https://github.com/yourusername/xinyu-lang/actions/workflows/release.yml)
[![文档部署](https://github.com/yourusername/xinyu-lang/actions/workflows/docs.yml/badge.svg)](https://github.com/yourusername/xinyu-lang/actions/workflows/docs.yml)
[![测试覆盖率](https://codecov.io/gh/yourusername/xinyu-lang/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/xinyu-lang)
[![PyPI版本](https://img.shields.io/pypi/v/xinyu-lang)](https://pypi.org/project/xinyu-lang/)
[![Python版本](https://img.shields.io/pypi/pyversions/xinyu-lang)](https://pypi.org/project/xinyu-lang/)

#### 工作流
1. **代码质量检查** (`quality.yml`): 每次提交时运行代码格式化、风格检查和类型检查
2. **测试套件** (`test.yml`): 在多个Python版本上运行单元测试、集成测试和功能测试
3. **构建和发布** (`release.yml`): 创建版本标签时自动构建和发布到PyPI
4. **文档部署** (`docs.yml`): 自动构建和部署文档到GitHub Pages
5. **依赖更新** (`dependabot.yml`): 自动更新依赖并创建Pull Request

#### 本地部署
```bash
# 运行完整部署流程
python scripts/deploy.py --environment test --version 0.1.0

# 只运行代码质量检查
python scripts/deploy.py --check-only

# 只运行测试
python scripts/deploy.py --test-only

# 只构建包
python scripts/deploy.py --build-only

# 发布到生产环境
python scripts/deploy.py --environment production --version 1.0.0
```

#### 自动化构建脚本
```bash
# 运行完整构建流程
python build.py --all

# 只运行测试
python build.py --test

# 只格式化代码
python build.py --format

# 只安装依赖
python build.py --install
```

## 📚 文档

- [用户指南](docs/USER_GUIDE.md) - 完整的使用教程和示例
- [API参考](docs/API_REFERENCE.md) - 详细的API文档
- [格式化工具使用指南](docs/formatter_usage.md) - 代码格式化工具使用说明
- [REPL历史增强功能](docs/repl_history_enhancement.md) - 增强的REPL历史记录管理
- [示例代码](examples/) - 各种使用示例

## 🛡️ 安全特性

心语内置安全执行环境，限制以下操作：
- 文件系统访问
- 网络操作
- 系统命令执行
- 危险的内置函数
- 未经授权的模块导入

```python
from src.core.compiler import XinyuCompiler

# 启用安全模式（默认）
compiler = XinyuCompiler(enable_safety=True)

# 安全执行代码
result = compiler.execute('印"安全代码"')
```

## 🎯 错误处理

心语提供友好的中文错误信息：

```
语义错误: 变量'x'未定义 (行 5, 列 10)
[建议] 请在使用前声明变量
[调试] 检查变量作用域和拼写
```

## 📊 性能优化

### 编译优化
- 常量折叠
- 死代码消除
- 内联优化

### 执行优化
- 即时编译（JIT）
- 缓存编译结果
- 内存管理优化

## 🤝 贡献

欢迎贡献代码、文档或报告问题！

### 贡献步骤

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 开发规范

- 遵循 PEP 8 代码风格
- 添加适当的测试用例
- 更新相关文档
- 使用 Conventional Commits 提交信息

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢所有为这个项目做出贡献的人！

## 📞 联系方式

- 项目主页：https://github.com/yourusername/xinyu
- 问题反馈：https://github.com/yourusername/xinyu/issues
- 讨论区：https://github.com/yourusername/xinyu/discussions

## 🚀 路线图

### v1.0.0 (已完成)
- [x] 基础语言特性实现
- [x] 中文语法支持
- [x] 类型推断系统
- [x] 安全执行环境
- [x] 友好的错误处理
- [x] 增强的REPL历史记录管理
- [x] 代码格式化工具
- [x] 开发工具链集成
- [x] 预提交钩子支持

### v1.1.0 (计划中)
- [ ] 更多内置函数
- [ ] 标准库扩展
- [ ] 性能优化
- [ ] IDE插件
- [ ] 调试器增强

### v1.2.0 (规划中)
- [ ] WebAssembly支持
- [ ] 多线程支持
- [ ] 数据库集成
- [ ] 图形界面
- [ ] 包管理器

---

**心语 - 让编程更贴近中文思维**
