# 贡献指南

感谢您对心语语言项目的关注！我们欢迎任何形式的贡献。

## 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [提交Issue](#提交issue)
- [提交Pull Request](#提交pull-request)
- [代码规范](#代码规范)
- [测试规范](#测试规范)
- [文档规范](#文档规范)

## 行为准则

### 我们的承诺

为了营造一个开放和友好的环境，我们承诺：

- 使用包容和友好的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

### 不可接受的行为

- 使用性化的语言或图像
- 发表侮辱性/贬损性评论
- 进行人身攻击或政治攻击
- 公开或私下骚扰
- 未经许可发布他人的私人信息
- 其他不道德或不专业的行为

## 如何贡献

### 贡献类型

我们欢迎以下类型的贡献：

- **Bug修复** - 修复已知问题
- **功能增强** - 添加新功能或改进现有功能
- **文档改进** - 改进文档、添加示例
- **代码优化** - 提高代码质量和性能
- **测试补充** - 增加测试覆盖率

### 贡献流程

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 进行更改
4. 运行测试确保通过
5. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
6. 推送到分支 (`git push origin feature/AmazingFeature`)
7. 创建Pull Request

## 提交Issue

### Issue类型

- **Bug报告** - 报告程序错误
- **功能请求** - 建议新功能
- **文档问题** - 报告文档错误或改进建议
- **问题讨论** - 讨论技术问题

### Bug报告模板

提交Bug报告时，请包含以下信息：

```markdown
## Bug描述
清晰简洁地描述bug。

## 复现步骤
1. 执行 '...'
2. 输入 '....'
3. 查看错误

## 期望行为
描述你期望发生的事情。

## 实际行为
描述实际发生的事情。

## 环境信息
- 操作系统: [如 Windows 10]
- Python版本: [如 3.9.0]
- 心语版本: [如 1.0.0]

## 代码示例
```心语
# 提供最小复现代码
```

## 其他信息
添加任何其他有助于解决问题的信息。
```

### 功能请求模板

提交功能请求时，请包含以下信息：

```markdown
## 功能描述
清晰简洁地描述你想要的功能。

## 使用场景
描述这个功能的使用场景。

## 示例代码
```心语
# 展示功能如何使用
```

## 替代方案
描述你考虑过的替代方案。

## 其他信息
添加任何其他有助于理解功能的信息。
```

## 提交Pull Request

### PR检查清单

提交PR前，请确保：

- [ ] 代码遵循项目的代码规范
- [ ] 已添加必要的测试
- [ ] 所有测试都通过
- [ ] 已更新相关文档
- [ ] 提交消息清晰明确
- [ ] PR标题和描述清晰

### PR标题格式

使用以下格式：

- `feat: 添加新功能` - 新功能
- `fix: 修复bug` - Bug修复
- `docs: 更新文档` - 文档更新
- `test: 添加测试` - 测试相关
- `refactor: 重构代码` - 代码重构
- `perf: 性能优化` - 性能优化
- `chore: 其他更改` - 其他更改

### PR描述模板

```markdown
## 更改类型
- [ ] Bug修复
- [ ] 功能增强
- [ ] 文档更新
- [ ] 代码重构
- [ ] 测试补充

## 更改描述
清晰描述你的更改。

## 相关Issue
关闭 #(issue编号)

## 测试
描述你如何测试这些更改。

## 截图
如果适用，添加截图说明更改。

## 其他信息
添加任何其他相关信息。
```

## 代码规范

### Python代码规范

- **PEP 8** - 遵循PEP 8代码风格
- **类型注解** - 使用类型注解提高代码可读性
- **文档字符串** - 使用中文文档字符串
- **命名规范**：
  - 类名：大驼峰（如 `ChineseProgram`）
  - 函数名：小写+下划线（如 `parse_expression`）
  - 变量名：小写+下划线（如 `token_list`）
  - 常量名：大写+下划线（如 `MAX_DEPTH`）

### 代码示例

```python
def parse_expression(self) -> ASTNode:
    """解析表达式

    使用递归下降方法解析表达式，支持各种操作符。

    Returns:
        ASTNode: 解析后的表达式节点

    Raises:
        ParseError: 如果语法错误
    """
    # 实现代码
    pass
```

### 心语代码规范

- **文件编码** - 使用UTF-8编码
- **文件扩展名** - 使用 `.心语` 扩展名
- **注释** - 使用 `#` 添加注释
- **命名** - 使用有意义的中文命名

### 心语代码示例

```心语
# 计算斐波那契数列
定义 斐波那契(n)：
    若 n 小 2 则：
        返回 n。
    否则：
        返回 斐波那契(n 减 1) 加 斐波那契(n 减 2)。

# 测试函数
印 斐波那契(10)。
```

## 测试规范

### 测试原则

- **单元测试** - 每个功能都应该有单元测试
- **集成测试** - 测试模块之间的交互
- **边界测试** - 测试边界条件和异常情况
- **覆盖率** - 保持测试覆盖率在70%以上

### 测试命名

```python
def test_<功能>_<场景>_<期望结果>():
    """测试描述"""
    pass

# 示例
def test_parse_expression_with_addition_returns_binary_op():
    """测试解析加法表达式返回二元操作节点"""
    pass
```

### 测试结构

```python
class TestFeature:
    """功能测试"""

    def setup_method(self):
        """测试初始化"""
        pass

    def test_normal_case(self):
        """测试正常情况"""
        pass

    def test_edge_case(self):
        """测试边界情况"""
        pass

    def test_error_case(self):
        """测试错误情况"""
        pass
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_lexer.py

# 运行特定测试
pytest tests/test_lexer.py::TestLexer::test_tokenize_number

# 生成覆盖率报告
pytest --cov=src --cov-report=html
```

## 文档规范

### 文档类型

- **README.md** - 项目说明
- **CONTRIBUTING.md** - 贡献指南
- **docs/** - 详细文档
- **代码注释** - 内联注释
- **文档字符串** - 函数和类文档

### 文档风格

- **语言** - 使用中文编写文档
- **格式** - 使用Markdown格式
- **结构** - 清晰的标题层次
- **示例** - 提供代码示例
- **更新** - 保持文档与代码同步

### 文档字符串格式

```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """函数简述

    详细描述函数的功能和行为。

    Args:
        param1: 参数1说明
        param2: 参数2说明

    Returns:
        返回值说明

    Raises:
        ExceptionType: 异常说明

    Example:
        >>> result = function_name(value1, value2)
        >>> print(result)
        expected_output
    """
    pass
```

## 开发环境设置

### 环境要求

- Python 3.8+
- pytest
- pytest-cov
- pytest-asyncio

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/yourname/xinyu.git
cd xinyu

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖
pip install pytest pytest-cov pytest-asyncio

# 运行测试
pytest
```

## 项目结构

```
chineseprogram/
├── src/           # 源代码
├── tests/         # 测试文件
├── docs/          # 文档
├── examples/      # 示例代码
├── README.md      # 项目说明
├── CONTRIBUTING.md # 贡献指南
└── requirements.txt # 依赖列表
```

## 获取帮助

- **文档** - 查看README和docs目录
- **Issues** - 在GitHub Issues中提问
- **讨论** - 参与GitHub Discussions

## 许可证

通过贡献代码，您同意您的贡献将根据MIT许可证授权。

---

再次感谢您的贡献！您的参与让心语语言变得更好。
