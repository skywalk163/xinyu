# 心语编程语言 CI/CD 系统

## 概述

心语编程语言的持续集成和持续部署（CI/CD）系统，提供自动化的构建、测试、质量检查和发布流程。

## 系统架构

### 工作流
```
代码提交 → 代码质量检查 → 测试套件 → 构建包 → 发布 → 文档部署
```

### 组件
1. **GitHub Actions工作流**
   - `quality.yml` - 代码质量检查
   - `test.yml` - 测试套件
   - `release.yml` - 构建和发布
   - `docs.yml` - 文档部署

2. **部署脚本**
   - `deploy.py` - 命令行部署工具
   - `build.py` - 构建脚本

3. **配置**
   - `deploy-config.yaml` - 部署配置
   - `dependabot.yml` - 依赖更新配置

## 快速开始

### 1. 本地开发

#### 运行代码质量检查
```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 运行代码质量检查
python scripts/deploy.py --check-only

# 或使用预提交钩子
pre-commit run --all-files
```

#### 运行测试
```bash
# 运行所有测试
python scripts/deploy.py --test-only

# 运行特定测试类型
pytest tests/ -v -m "unit"      # 单元测试
pytest tests/ -v -m "integration" # 集成测试
pytest tests/ -v -m "functional"  # 功能测试
```

#### 构建包
```bash
# 构建包（不发布）
python scripts/deploy.py --build-only

# 或使用构建脚本
python build.py --build
```

### 2. 本地部署

#### 测试环境部署
```bash
# 部署到TestPyPI（需要设置TEST_PYPI_API_TOKEN环境变量）
export TEST_PYPI_API_TOKEN=your_test_token
python scripts/deploy.py --environment test --version 0.1.0
```

#### 生产环境部署
```bash
# 部署到PyPI（需要设置PYPI_API_TOKEN环境变量）
export PYPI_API_TOKEN=your_production_token
python scripts/deploy.py --environment production --version 1.0.0
```

### 3. 使用构建脚本
```bash
# 运行完整构建流程
python build.py --all

# 只运行测试
python build.py --test

# 只格式化代码
python build.py --format

# 只安装依赖
python build.py --install

# 只生成文档
python build.py --docs
```

## GitHub Actions 工作流

### 代码质量检查 (`quality.yml`)
**触发条件**:
- 推送到 `main` 或 `develop` 分支
- 创建或更新拉取请求到 `main` 分支
- 每周一早上6点（定时任务）
- 手动触发

**检查项目**:
- 代码格式化 (black)
- 导入排序 (isort)
- 代码风格 (flake8)
- 心语代码格式化
- 类型检查 (mypy)
- 安全扫描 (bandit)
- 预提交钩子

### 测试套件 (`test.yml`)
**触发条件**:
- 推送到 `main` 或 `develop` 分支
- 创建或更新拉取请求到 `main` 分支
- 每天凌晨2点（定时任务）
- 手动触发

**测试项目**:
- 单元测试 (Python 3.8-3.12)
- 集成测试
- 功能测试
- REPL测试
- 格式化工具测试
- 性能测试（仅主分支）

### 构建和发布 (`release.yml`)
**触发条件**:
- 推送版本标签 (`v*`)
- 手动触发

**发布流程**:
1. 运行完整测试套件
2. 构建包（sdist 和 wheel）
3. 验证包
4. 发布到TestPyPI（测试环境）
5. 发布到PyPI（生产环境）
6. 创建GitHub Release

### 文档部署 (`docs.yml`)
**触发条件**:
- 推送到 `main` 分支
- 手动触发

**部署流程**:
1. 构建HTML文档
2. 部署到GitHub Pages
3. 测试文档中的代码示例
4. 检查文档质量

## 配置

### 环境变量
| 变量名 | 描述 | 必需 |
|--------|------|------|
| `TEST_PYPI_API_TOKEN` | TestPyPI API令牌 | 测试发布 |
| `PYPI_API_TOKEN` | PyPI API令牌 | 生产发布 |
| `SLACK_WEBHOOK_URL` | Slack Webhook URL | 通知 |
| `CODECOV_TOKEN` | Codecov令牌 | 覆盖率报告 |

### 部署配置 (`deploy-config.yaml`)
```yaml
# 环境配置
environments:
  test:
    pypi_url: "https://test.pypi.org/legacy/"
    api_token_env: "TEST_PYPI_API_TOKEN"

  production:
    pypi_url: "https://upload.pypi.org/legacy/"
    api_token_env: "PYPI_API_TOKEN"

# 检查配置
checks:
  code_quality: true
  tests: true
  security: true
  build: true
  docs: false
```

### 依赖更新 (`dependabot.yml`)
- 每周一自动检查依赖更新
- 自动创建Pull Request
- 分组更新（测试依赖、开发工具、运行时依赖）
- 安全更新自动标记

## 使用示例

### 1. 开发工作流
```bash
# 1. 创建功能分支
git checkout -b feature/new-feature

# 2. 开发代码...

# 3. 运行本地检查
python scripts/deploy.py --check-only
python scripts/deploy.py --test-only

# 4. 提交代码
git add .
git commit -m "feat: 添加新功能"

# 5. 推送到远程
git push origin feature/new-feature

# 6. 创建Pull Request
# GitHub Actions会自动运行检查
```

### 2. 发布新版本
```bash
# 1. 更新版本号（在pyproject.toml中）
# version = "1.0.0"

# 2. 创建发布标签
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# 3. GitHub Actions会自动：
#    - 运行测试
#    - 构建包
#    - 发布到PyPI
#    - 创建GitHub Release
```

### 3. 手动部署
```bash
# 部署到测试环境
python scripts/deploy.py --environment test --version 0.1.0

# 部署到生产环境
python scripts/deploy.py --environment production --version 1.0.0

# 跳过测试
python scripts/deploy.py --environment test --version 0.1.0 --skip-tests

# 只运行检查
python scripts/deploy.py --check-only

# 只运行测试
python scripts/deploy.py --test-only

# 只构建包
python scripts/deploy.py --build-only

# 只发布包
python scripts/deploy.py --publish-only --environment test

# 只生成文档
python scripts/deploy.py --docs-only
```

## 故障排除

### 常见问题

#### 1. 构建失败
```bash
# 清理构建缓存
rm -rf dist/ build/

# 重新安装依赖
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 重新构建
python -m build
```

#### 2. 测试失败
```bash
# 运行特定测试
pytest tests/test_specific.py -v

# 运行测试并显示详细输出
pytest tests/ -v --tb=long

# 运行测试并生成覆盖率报告
pytest tests/ --cov=src --cov-report=html
```

#### 3. 发布失败
```bash
# 检查API令牌
echo $PYPI_API_TOKEN

# 验证包
twine check dist/*

# 手动发布
twine upload dist/*
```

#### 4. 文档构建失败
```bash
# 安装文档工具
pip install sphinx sphinx-rtd-theme myst-parser

# 清理文档构建
rm -rf docs/_build/

# 重新构建文档
sphinx-build -b html docs docs/_build/html
```

### 日志文件
- 构建日志: `logs/build.log`
- 测试日志: `logs/test.log`
- 部署日志: `logs/deploy.log`
- GitHub Actions日志: GitHub仓库的Actions页面

## 监控和报告

### 状态徽章
在README.md中添加以下徽章：

```markdown
![代码质量检查](https://github.com/yourusername/xinyu-lang/actions/workflows/quality.yml/badge.svg)
![测试套件](https://github.com/yourusername/xinyu-lang/actions/workflows/test.yml/badge.svg)
![发布状态](https://github.com/yourusername/xinyu-lang/actions/workflows/release.yml/badge.svg)
![文档部署](https://github.com/yourusername/xinyu-lang/actions/workflows/docs.yml/badge.svg)
![测试覆盖率](https://codecov.io/gh/yourusername/xinyu-lang/branch/main/graph/badge.svg)
![PyPI版本](https://img.shields.io/pypi/v/xinyu-lang)
![Python版本](https://img.shields.io/pypi/pyversions/xinyu-lang)
```

### 通知
- Slack: CI/CD状态通知
- 邮件: 发布成功/失败通知
- GitHub: Pull Request状态检查

## 最佳实践

### 1. 代码提交
- 使用有意义的提交信息
- 遵循Conventional Commits规范
- 在提交前运行预提交钩子
- 确保所有测试通过

### 2. 版本管理
- 使用语义化版本控制 (SemVer)
- 主版本号: 不兼容的API更改
- 次版本号: 向后兼容的功能性新增
- 修订号: 向后兼容的问题修正

### 3. 发布流程
1. 更新`pyproject.toml`中的版本号
2. 更新`CHANGELOG.md`
3. 创建发布标签
4. 推送标签触发自动发布
5. 验证发布结果

### 4. 依赖管理
- 定期更新依赖
- 审查安全更新
- 测试依赖更新
- 使用依赖分组

## 扩展和定制

### 添加新的检查
1. 在`quality.yml`中添加新的检查步骤
2. 在`deploy.py`中实现检查逻辑
3. 更新`deploy-config.yaml`配置

### 添加新的测试
1. 在`test.yml`中添加新的测试任务
2. 创建测试文件在`tests/`目录
3. 使用适当的测试标记

### 自定义部署流程
1. 修改`deploy.py`中的部署逻辑
2. 更新`deploy-config.yaml`配置
3. 添加新的环境配置

### 集成其他服务
1. **Codecov**: 测试覆盖率报告
2. **SonarCloud**: 代码质量分析
3. **Docker Hub**: 容器镜像发布
4. **Read the Docs**: 文档托管

## 支持

### 问题报告
- GitHub Issues: https://github.com/yourusername/xinyu-lang/issues
- 邮件: team@xinyu-lang.org

### 文档
- 用户指南: `docs/USER_GUIDE.md`
- API参考: `docs/API_REFERENCE.md`
- CI/CD设计: `docs/CI_CD_DESIGN.md`

### 贡献
欢迎贡献代码、文档或报告问题。请参考`CONTRIBUTING.md`了解详细信息。

## 许可证
MIT许可证 - 详见`LICENSE`文件
