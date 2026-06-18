# 心语 (Xin Yu) 中文编程语言文档

欢迎使用心语中文编程语言文档！这里汇集了所有相关的技术文档、使用指南和API参考。

## 📚 核心文档

### 入门指南
- [快速开始](../README.md) - 项目概述和快速入门
- [用户指南](USER_GUIDE.md) - 完整的使用教程和示例
- [语言规范](LANGUAGE_SPEC.md) - 心语语言语法规范

### 开发工具
- [代码格式化工具使用指南](formatter_usage.md) - 代码格式化工具详细说明
- [REPL历史增强功能](repl_history_enhancement.md) - 增强的REPL历史记录管理
- [预提交钩子配置](../.pre-commit-config.yaml) - 代码质量检查配置

### 技术文档
- [API参考](API_REFERENCE.md) - 详细的API文档
- [架构设计](architecture.md) - 系统架构设计
- [模块接口](module-interfaces.md) - 模块接口定义
- [标准库设计](stdlib-design.md) - 标准库设计文档

## 🔧 开发工具链

### 代码格式化工具
心语提供了强大的代码格式化工具，支持自定义规则和批量处理。

**主要功能：**
- 自动格式化心语代码
- 支持自定义格式化规则
- 批量处理目录和文件
- 集成到预提交钩子

**使用方法：**
```bash
# 格式化单个文件
python tools/xinyu_format.py format example.xinyu

# 检查代码格式
python tools/xinyu_format.py check example.xinyu

# 格式化目录下所有文件
python tools/xinyu_format.py format src/

# 查看帮助
python tools/xinyu_format.py --help
```

**配置文件：** `.xinyu-formatter.yaml`

### 增强的REPL历史管理
心语REPL现在支持强大的历史记录管理功能。

**主要功能：**
- 历史记录搜索和过滤
- 命令类型自动检测
- 编辑和重新执行历史命令
- 导入导出功能（JSON/CSV格式）
- 详细的统计信息

**使用方法：**
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

## 🏗️ 项目架构

### 核心组件
```
src/
├── core/              # 核心接口
├── lexer/             # 词法分析器
├── parser/            # 语法分析器
├── semantic/          # 语义分析器
├── codegen/           # 代码生成器
├── runtime/           # 运行时环境
├── error_handling/    # 错误处理
└── repl/              # REPL交互式解释器
```

### 开发工具
```
tools/
├── formatter.py       # 代码格式化器
├── format_engine.py   # 格式化引擎
├── xinyu_format.py    # 格式化命令行工具
└── setup_formatter.py # 格式化工具安装脚本
```

## 📖 示例代码

查看 [examples/](../examples/) 目录获取丰富的示例代码：

- **基础语法示例** - 变量、控制流、函数等基础用法
- **高级特性示例** - 类、模块、异常处理等高级特性
- **工具使用示例** - 格式化工具和REPL使用示例

## 🧪 测试

### 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_lexer.py

# 带覆盖率报告
pytest --cov=src --cov-report=html
```

### 测试文件
- `test_history_manager.py` - 历史管理器测试
- `test_repl_integration.py` - REPL集成测试
- `test_repl_final.py` - 完整功能测试
- `test_formatter.py` - 格式化工具测试

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
```bash
# 安装预提交钩子
pre-commit install

# 手动运行所有钩子
pre-commit run --all-files
```

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](../LICENSE) 文件了解详情。

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

## 📞 联系方式

- 项目主页：https://github.com/yourusername/xinyu
- 问题反馈：https://github.com/yourusername/xinyu/issues
- 讨论区：https://github.com/yourusername/xinyu/discussions

---

**心语 - 让编程更贴近中文思维**
