# 心语代码格式化工具使用文档

## 概述

心语代码格式化工具是一个用于自动格式化心语(Xin Yu)源代码的工具，提供代码格式化、格式检查和预提交钩子集成功能。

## 安装

### 自动安装
运行设置脚本自动安装：
```bash
python tools/setup_formatter.py
```

### 手动安装
1. 确保以下文件存在：
   - `tools/simple_formatter.py` - 简单格式化器
   - `tools/xinyu_format.py` - 命令行接口
   - `.xinyu-formatter.yaml` - 配置文件
   - `.pre-commit-config.yaml` - 预提交配置

2. 安装预提交钩子（可选）：
```bash
pip install pre-commit
pre-commit install
```

## 使用方法

### 基本使用

#### 1. 格式化单个文件
```bash
# 直接修改文件
python tools/xinyu_format.py --in-place example.xinyu

# 输出格式化后的代码到控制台
python tools/xinyu_format.py example.xinyu
```

#### 2. 检查格式问题
```bash
# 只检查不修改
python tools/xinyu_format.py --check example.xinyu
```

#### 3. 格式化目录下所有文件
```bash
python tools/xinyu_format.py --in-place src/
```

#### 4. 使用自定义配置
```bash
python tools/xinyu_format.py --config custom-config.yaml example.xinyu
```

### 命令行选项

| 选项 | 简写 | 描述 |
|------|------|------|
| `--check` | `-c` | 只检查格式问题，不修改文件 |
| `--in-place` | `-i` | 直接修改文件 |
| `--config` | | 指定配置文件路径 |
| `--verbose` | `-v` | 详细输出 |
| `--version` | | 显示版本信息 |
| `--help` | `-h` | 显示帮助信息 |

## 配置

### 配置文件
默认配置文件：`.xinyu-formatter.yaml`

### 配置选项

```yaml
# 行长度限制
line_length: 100

# 缩进大小（空格数）
indent_size: 4

# 引号风格：single（单引号）或 double（双引号）
quote_style: "double"

# 是否在多行结构中添加尾随逗号
trailing_comma: true

# 最大连续空行数
max_empty_lines: 2

# 操作符周围添加空格
spaces_around_operators: true

# 逗号后添加空格
spaces_after_comma: true

# 冒号后添加空格
spaces_after_colon: true

# 自定义规则
custom_rules:
  # 函数定义和调用中的空格
  function_spacing: true

  # 列表和字典中的空格
  collection_spacing: true

  # 注释格式
  comment_format: true

  # 导入语句排序
  import_sorting: true

  # 空行位置规则
  blank_line_rules:
    # 在函数定义前添加空行
    before_function: true

    # 在类定义前添加空行
    before_class: true

    # 在导入语句后添加空行
    after_imports: true

    # 在逻辑块之间添加空行
    between_blocks: true

# 文件排除模式
exclude_patterns:
  - "**/__pycache__/**"
  - "**/.git/**"
  - "**/.venv/**"
  - "**/venv/**"
  - "**/node_modules/**"
  - "**/dist/**"
  - "**/build/**"

# 文件包含模式（默认：所有 .xinyu 文件）
include_patterns:
  - "**/*.xinyu"

# 格式化模式
# auto: 自动检测并应用最佳格式
# strict: 严格模式，强制所有规则
# minimal: 最小化模式，只应用基本规则
format_mode: "auto"

# 是否在格式化时保留原始文件的换行符
preserve_line_breaks: false

# 是否在格式化时保留原始文件的注释位置
preserve_comment_positions: true

# 错误处理级别
# error: 遇到错误时停止
# warn: 显示警告但继续
# ignore: 忽略错误
error_level: "warn"
```

## 预提交钩子集成

### 安装预提交钩子
```bash
pip install pre-commit
pre-commit install
```

### 使用预提交钩子

#### 1. 提交前检查所有文件
```bash
pre-commit run --all-files
```

#### 2. 自动修复格式问题
```bash
# 添加文件到暂存区
git add example.xinyu

# 运行格式化修复钩子
pre-commit run xinyu-format-fix
```

#### 3. 只检查特定文件
```bash
pre-commit run xinyu-format --files example.xinyu
```

### 预提交配置
在 `.pre-commit-config.yaml` 中添加以下配置：

```yaml
# 心语代码格式化
- repo: local
  hooks:
    - id: xinyu-format
      name: Format Xinyu code
      entry: python tools/simple_formatter.py --check
      language: system
      types: [file]
      files: \.xinyu$
      pass_filenames: true
      args: [--check]

    - id: xinyu-format-fix
      name: Format Xinyu code (auto-fix)
      entry: python tools/simple_formatter.py --in-place
      language: system
      types: [file]
      files: \.xinyu$
      pass_filenames: true
      args: [--in-place]
      stages: [commit]
```

## 示例

### 示例1：格式化代码
**格式化前：**
```xinyu
# 测试格式化工具
定义 测试函数():
结果=1+2*3
返回 结果

如果 __名称__ == "__主__":
印 "Hello, World!"
```

**格式化后：**
```xinyu
# 测试格式化工具
定义 测试函数():
    结果 = 1 + 2 * 3
    返回 结果

如果 __名称__ == "__主__":
    印 "Hello, World!"
```

### 示例2：检查格式问题
```bash
$ python tools/xinyu_format.py --check example.xinyu
example.xinyu:
  warning:2:1: 缺少缩进
  info:3:10: 操作符周围缺少空格
  warning:6:1: 缺少缩进
```

### 示例3：批量格式化
```bash
# 格式化src目录下所有.xinyu文件
python tools/xinyu_format.py --in-place src/

# 检查所有文件格式
python tools/xinyu_format.py --check src/
```

## 高级功能

### 1. 自定义格式化规则
创建自定义配置文件 `custom-formatter.yaml`：
```yaml
line_length: 80
indent_size: 2
quote_style: "single"
max_empty_lines: 1
```

使用自定义配置：
```bash
python tools/xinyu_format.py --config custom-formatter.yaml --in-place example.xinyu
```

### 2. 集成到CI/CD流水线
在GitHub Actions中添加格式化检查：

```yaml
name: Code Format Check

on: [push, pull_request]

jobs:
  format-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Check code format
        run: |
          python tools/xinyu_format.py --check src/
```

### 3. 编辑器集成

#### VS Code
在 `.vscode/settings.json` 中添加：
```json
{
  "[xinyu]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "xinyu.formatter"
  },
  "xinyu.formatter.path": "python",
  "xinyu.formatter.args": [
    "tools/xinyu_format.py",
    "--in-place"
  ]
}
```

#### PyCharm/IntelliJ IDEA
1. 打开设置 → 工具 → 文件监视器
2. 添加新的文件监视器：
   - 文件类型：`*.xinyu`
   - 程序：`python`
   - 参数：`tools/xinyu_format.py --in-place $FilePath$`
   - 输出路径：`$FilePath$`
   - 工作目录：`$ProjectFileDir$`

## 故障排除

### 常见问题

#### 1. 格式化工具不工作
- 检查Python版本（需要Python 3.8+）
- 检查依赖：`pip install pyyaml`
- 检查文件权限

#### 2. 预提交钩子不生效
- 确保已安装pre-commit：`pip install pre-commit`
- 运行：`pre-commit install`
- 检查`.git/hooks/pre-commit`文件是否存在

#### 3. 配置不生效
- 检查配置文件路径
- 确保配置文件格式正确（YAML格式）
- 重启编辑器或终端

#### 4. 格式化结果不符合预期
- 检查配置文件中的规则设置
- 使用`--verbose`选项查看详细输出
- 手动检查格式化规则

### 调试模式
使用详细输出模式查看格式化过程：
```bash
python tools/xinyu_format.py --verbose --in-place example.xinyu
```

## 开发指南

### 扩展格式化规则
要添加新的格式化规则，修改 `tools/simple_formatter.py` 中的 `SimpleXinyuFormatter` 类：

1. 在 `_format_line` 方法中添加新的格式化逻辑
2. 在 `check_format` 方法中添加新的检查规则
3. 在配置文件中添加相应的配置选项

### 添加新的格式化器
要创建基于AST的完整格式化器：
1. 实现 `tools/formatter.py` 中的 `XinyuFormatter` 类
2. 实现 `tools/format_engine.py` 中的 `ASTFormatter` 类
3. 更新命令行接口以支持新的格式化器

### 测试
运行测试：
```bash
# 运行单元测试
python -m pytest tests/test_formatter.py

# 运行集成测试
python tools/test_formatter.py
```

## 版本历史

### v1.0.0 (2024-06-16)
- 初始版本发布
- 基本代码格式化功能
- 命令行接口
- 配置文件支持
- 预提交钩子集成
- 简单格式化规则（缩进、空格、引号等）

## 贡献指南

1. Fork项目
2. 创建功能分支：`git checkout -b feature/new-formatting-rule`
3. 提交更改：`git commit -am 'Add new formatting rule'`
4. 推送到分支：`git push origin feature/new-formatting-rule`
5. 创建Pull Request

## 许可证

MIT License
