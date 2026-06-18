# 变更日志

所有心语编程语言项目的显著变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 新增
- 完整的CI/CD流水线系统
- GitHub Actions工作流：
  - `quality.yml`: 代码质量检查工作流
  - `test.yml`: 测试套件工作流
  - `release.yml`: 构建和发布工作流
  - `docs.yml`: 文档部署工作流
- 自动化部署脚本 (`scripts/deploy.py`)
- 部署配置文件 (`.github/deploy-config.yaml`)
- Dependabot自动依赖更新配置
- 详细的CI/CD使用文档

### 改进
- 增强的构建脚本 (`build.py`) 支持更多选项
- 改进的预提交钩子配置
- 多Python版本测试支持 (3.8-3.12)
- 自动化的测试覆盖率报告
- 集成的安全扫描 (bandit)

### 修复
- 修复了Windows环境下的Unicode编码问题
- 修复了测试隔离问题
- 改进了错误处理和日志记录

## [0.1.0] - 2024-01-01

### 新增
- 心语编程语言核心功能
- 中文编程语法支持
- 基础REPL环境
- 代码格式化工具
- 增强的REPL历史管理
- 预提交钩子配置

### 改进
- 改进的语法解析器
- 增强的错误处理
- 更好的用户界面

### 修复
- 修复了语法解析错误
- 修复了REPL历史管理问题
- 修复了代码格式化工具的问题

## 版本管理

### 版本号格式
本项目使用语义化版本控制 (SemVer)：

- **主版本号**: 不兼容的API更改
- **次版本号**: 向后兼容的功能性新增
- **修订号**: 向后兼容的问题修正

### 发布流程
1. 更新`pyproject.toml`中的版本号
2. 更新`CHANGELOG.md`文件
3. 创建Git标签: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
4. 推送标签: `git push origin vX.Y.Z`
5. GitHub Actions会自动构建和发布

### 自动化发布
当创建版本标签时，GitHub Actions会自动：

1. 运行完整的测试套件
2. 构建Python包 (sdist 和 wheel)
3. 发布到TestPyPI进行测试
4. 发布到PyPI进行生产发布
5. 创建GitHub Release
6. 生成变更日志

## 贡献指南

### 提交变更
- 使用有意义的提交信息
- 遵循Conventional Commits规范
- 在提交前运行预提交钩子
- 确保所有测试通过

### 添加变更日志条目
当添加新功能、修复问题或进行重大更改时，请在`CHANGELOG.md`中添加相应的条目：

```markdown
## [版本号] - YYYY-MM-DD

### 新增
- 描述新功能

### 改进
- 描述改进

### 修复
- 描述修复的问题

### 废弃
- 描述废弃的功能

### 移除
- 描述移除的功能
```

### 版本发布
1. 确定下一个版本号（基于变更类型）
2. 更新`pyproject.toml`中的版本号
3. 在`CHANGELOG.md`中添加新版本条目
4. 提交更改: `git commit -m "chore: 发布vX.Y.Z"`
5. 创建标签: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
6. 推送标签: `git push origin vX.Y.Z`

## 链接
- [GitHub Releases](https://github.com/yourusername/xinyu-lang/releases)
- [PyPI项目页面](https://pypi.org/project/xinyu-lang/)
- [文档](https://yourusername.github.io/xinyu-lang/)
- [问题跟踪](https://github.com/yourusername/xinyu-lang/issues)
