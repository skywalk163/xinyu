#!/usr/bin/env python3
"""
部署脚本 - 自动化构建、测试和发布流程
"""

import subprocess
import sys
import os
import argparse
import json
import yaml
import tomli
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import shutil


class DeploymentSystem:
    """部署系统"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.version = self._get_version()
        self.config = self._load_config()
        
    def _get_version(self) -> str:
        """获取版本号"""
        pyproject_path = self.project_root / "pyproject.toml"
        if pyproject_path.exists():
            try:
                with open(pyproject_path, 'rb') as f:
                    data = tomli.load(f)
                    return data.get('project', {}).get('version', '0.1.0')
            except Exception as e:
                print(f"读取版本号失败: {e}")
        return "0.1.0"
    
    def _load_config(self) -> Dict:
        """加载配置"""
        config_path = self.project_root / ".github" / "deploy-config.yaml"
        default_config = {
            "environments": {
                "test": {
                    "pypi_url": "https://test.pypi.org/legacy/",
                    "api_token_env": "TEST_PYPI_API_TOKEN"
                },
                "production": {
                    "pypi_url": "https://upload.pypi.org/legacy/",
                    "api_token_env": "PYPI_API_TOKEN"
                }
            },
            "checks": {
                "code_quality": True,
                "tests": True,
                "security": True,
                "build": True,
                "docs": False
            },
            "notifications": {
                "slack": True,
                "email": False
            }
        }
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f)
                    # 合并配置
                    default_config.update(user_config)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
        
        return default_config
    
    def run_command(self, cmd: str, cwd: Optional[Path] = None, 
                   capture_output: bool = True, check: bool = True) -> Tuple[bool, str]:
        """运行命令"""
        if cwd is None:
            cwd = self.project_root
            
        print(f"运行命令: {cmd}")
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=cwd,
                capture_output=capture_output,
                text=True,
                check=check
            )
            
            if result.returncode != 0:
                print(f"命令失败: {cmd}")
                if capture_output:
                    print(f"标准输出: {result.stdout}")
                    print(f"标准错误: {result.stderr}")
                return False, result.stderr if capture_output else ""
                
            print(f"命令成功: {cmd}")
            if capture_output and result.stdout:
                print(f"输出: {result.stdout}")
            return True, result.stdout if capture_output else ""
                
        except subprocess.CalledProcessError as e:
            print(f"运行命令时出错: {e}")
            if capture_output:
                print(f"标准输出: {e.stdout}")
                print(f"标准错误: {e.stderr}")
            return False, e.stderr if capture_output else str(e)
        except Exception as e:
            print(f"运行命令时出错: {e}")
            return False, str(e)
    
    def check_prerequisites(self) -> bool:
        """检查前置条件"""
        print("检查前置条件...")
        
        checks = [
            ("Python 3.8+", self._check_python_version),
            ("Git", self._check_git),
            ("构建工具", self._check_build_tools),
            ("依赖管理", self._check_dependencies),
        ]
        
        all_passed = True
        for check_name, check_func in checks:
            print(f"  - 检查 {check_name}...", end=" ")
            passed, message = check_func()
            if passed:
                print("[通过]")
            else:
                print("[失败]")
                print(f"    错误: {message}")
                all_passed = False
        
        return all_passed
    
    def _check_python_version(self) -> Tuple[bool, str]:
        """检查Python版本"""
        import sys
        version = sys.version_info
        if version.major == 3 and version.minor >= 8:
            return True, f"Python {version.major}.{version.minor}.{version.micro}"
        return False, f"需要Python 3.8+，当前版本: {version.major}.{version.minor}.{version.micro}"
    
    def _check_git(self) -> Tuple[bool, str]:
        """检查Git"""
        success, output = self.run_command("git --version", capture_output=True, check=False)
        if success:
            return True, output.strip()
        return False, "Git未安装或不可用"
    
    def _check_build_tools(self) -> Tuple[bool, str]:
        """检查构建工具"""
        tools = ["pip", "build", "twine"]
        missing = []
        
        for tool in tools:
            success, _ = self.run_command(f"{tool} --version", capture_output=False, check=False)
            if not success:
                missing.append(tool)
        
        if missing:
            return False, f"缺少工具: {', '.join(missing)}"
        return True, "所有构建工具已安装"
    
    def _check_dependencies(self) -> Tuple[bool, str]:
        """检查依赖"""
        requirements_files = ["requirements.txt", "requirements-dev.txt"]
        missing = []
        
        for req_file in requirements_files:
            path = self.project_root / req_file
            if not path.exists():
                missing.append(req_file)
        
        if missing:
            return False, f"缺少依赖文件: {', '.join(missing)}"
        return True, "所有依赖文件存在"
    
    def run_code_quality_checks(self) -> bool:
        """运行代码质量检查"""
        print("运行代码质量检查...")
        
        checks = [
            ("代码格式化 (black)", "black --check --diff src/ tests/ tools/"),
            ("导入排序 (isort)", "isort --check-only --diff src/ tests/ tools/"),
            ("代码风格 (flake8)", "flake8 src/ tests/ tools/ --max-line-length=100 --ignore=E203,W503,E501"),
            ("心语代码格式化", "python tools/xinyu_format.py check src/ tests/ examples/"),
            ("类型检查 (mypy)", "mypy src/ --ignore-missing-imports"),
            ("安全扫描 (bandit)", "bandit -r src/ -ll --skip B101,B105,B106,B107,B108,B110,B112,B113,B404,B603,B607"),
            ("预提交钩子", "pre-commit run --all-files --show-diff-on-failure"),
        ]
        
        all_passed = True
        for check_name, command in checks:
            print(f"  - {check_name}...", end=" ")
            success, _ = self.run_command(command, check=False)
            if success:
                print("[通过]")
            else:
                print("[失败]")
                all_passed = False
        
        return all_passed
    
    def run_tests(self, test_type: str = "all") -> bool:
        """运行测试"""
        print(f"运行{test_type}测试...")
        
        test_commands = {
            "all": "pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=xml --cov-report=html",
            "unit": "pytest tests/ -v -m 'not integration and not functional'",
            "integration": "pytest tests/ -v -m integration",
            "functional": "pytest tests/ -v -m functional",
            "repl": "python test_repl_final.py && python test_repl_integration.py && python test_history_manager.py",
            "formatter": "python demo_formatter.py && python tools/xinyu_format.py check src/ tests/ examples/",
        }
        
        command = test_commands.get(test_type, test_commands["all"])
        success, output = self.run_command(command, check=False)
        
        if success:
            print("[成功] 所有测试通过")
            return True
        else:
            print("[失败] 测试失败")
            print(output)
            return False
    
    def build_package(self, clean: bool = True) -> bool:
        """构建包"""
        print("构建包...")
        
        if clean:
            # 清理旧的构建文件
            dist_dir = self.project_root / "dist"
            build_dir = self.project_root / "build"
            
            for dir_path in [dist_dir, build_dir]:
                if dir_path.exists():
                    print(f"  清理目录: {dir_path}")
                    shutil.rmtree(dir_path)
        
        # 构建包
        success, output = self.run_command("python -m build")
        if not success:
            return False
        
        # 验证包
        print("验证包...")
        success, output = self.run_command("twine check dist/*")
        if not success:
            return False
        
        # 列出构建的文件
        dist_dir = self.project_root / "dist"
        if dist_dir.exists():
            files = list(dist_dir.glob("*"))
            print(f"构建的文件: {[f.name for f in files]}")
        
        return True
    
    def publish_package(self, environment: str = "test") -> bool:
        """发布包"""
        print(f"发布包到 {environment}...")
        
        env_config = self.config["environments"].get(environment)
        if not env_config:
            print(f"[错误] 未知环境: {environment}")
            return False
        
        pypi_url = env_config["pypi_url"]
        api_token_env = env_config["api_token_env"]
        
        # 检查API令牌
        api_token = os.environ.get(api_token_env)
        if not api_token:
            print(f"[错误] 缺少API令牌环境变量: {api_token_env}")
            return False
        
        # 发布包
        env = os.environ.copy()
        env["TWINE_USERNAME"] = "__token__"
        env["TWINE_PASSWORD"] = api_token
        
        command = f"twine upload --repository-url {pypi_url} dist/*"
        success, output = self.run_command(command, env=env)
        
        if success:
            print(f"[成功] 包已成功发布到 {environment}")
            return True
        else:
            print(f"[失败] 发布到 {environment} 失败")
            return False
    
    def generate_docs(self) -> bool:
        """生成文档"""
        print("生成文档...")
        
        docs_dir = self.project_root / "docs"
        build_dir = docs_dir / "_build"
        
        # 清理旧的构建文件
        if build_dir.exists():
            shutil.rmtree(build_dir)
        
        # 安装文档依赖
        print("  安装文档工具...")
        success, _ = self.run_command("pip install sphinx sphinx-rtd-theme myst-parser sphinx-autobuild")
        if not success:
            return False
        
        # 构建文档
        print("  构建HTML文档...")
        success, _ = self.run_command("sphinx-build -b html docs docs/_build/html -W", check=False)
        
        if success:
            print("[成功] 文档生成成功")
            return True
        else:
            print("[失败] 文档生成失败")
            return False
    
    def create_release(self, version: str, changelog: str = "") -> bool:
        """创建发布"""
        print(f"创建发布 v{version}...")
        
        # 检查是否在Git仓库中
        success, _ = self.run_command("git status", check=False)
        if not success:
            print("[错误] 不在Git仓库中")
            return False
        
        # 检查是否有未提交的更改
        success, output = self.run_command("git status --porcelain", capture_output=True)
        if success and output.strip():
            print("[错误] 有未提交的更改")
            print(output)
            return False
        
        # 创建标签
        tag_name = f"v{version}"
        print(f"  创建标签 {tag_name}...")
        success, _ = self.run_command(f"git tag -a {tag_name} -m 'Release {tag_name}'")
        if not success:
            return False
        
        # 推送标签
        print(f"  推送标签 {tag_name}...")
        success, _ = self.run_command(f"git push origin {tag_name}")
        if not success:
            return False
        
        print(f"[成功] 发布 {tag_name} 已创建")
        
        # 生成发布说明
        if not changelog:
            # 获取最近的提交信息作为变更日志
            success, changelog = self.run_command(
                "git log --oneline --format='- %s' $(git describe --tags --abbrev=0 2>/dev/null || echo '')..HEAD",
                capture_output=True
            )
            if not success:
                changelog = "查看提交历史获取详细变更"
        
        # 保存发布说明到文件
        release_notes_path = self.project_root / f"RELEASE_{tag_name}.md"
        with open(release_notes_path, 'w', encoding='utf-8') as f:
            f.write(f"# 心语编程语言 {tag_name}\n\n")
            f.write(f"发布日期: {datetime.now().strftime('%Y-%m-%d')}\n\n")
            f.write("## 变更日志\n\n")
            f.write(changelog)
            f.write("\n\n## 安装\n\n")
            f.write(f"```bash\npip install xinyu-lang=={version}\n```\n")
        
        print(f"[成功] 发布说明已保存到 {release_notes_path}")
        return True
    
    def deploy(self, environment: str = "test", version: Optional[str] = None, 
               skip_tests: bool = False, skip_checks: bool = False) -> bool:
        """执行部署流程"""
        print(f"开始部署到 {environment} 环境")
        print(f"版本: {version or self.version}")
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        steps = []
        
        # 前置条件检查
        steps.append(("检查前置条件", self.check_prerequisites))
        
        # 代码质量检查
        if not skip_checks:
            steps.append(("代码质量检查", self.run_code_quality_checks))
        
        # 测试
        if not skip_tests:
            steps.append(("运行测试", lambda: self.run_tests("all")))
        
        # 构建
        steps.append(("构建包", lambda: self.build_package(clean=True)))
        
        # 发布
        if environment in ["test", "production"]:
            steps.append((f"发布到{environment}", lambda: self.publish_package(environment)))
        
        # 创建发布
        if environment == "production" and version:
            steps.append((f"创建发布v{version}", lambda: self.create_release(version)))
        
        # 生成文档
        if environment == "production":
            steps.append(("生成文档", self.generate_docs))
        
        # 执行所有步骤
        all_passed = True
        for step_name, step_func in steps:
            print(f"\n步骤: {step_name}")
            print("-" * 40)
            
            if not step_func():
                print(f"[失败] 步骤失败: {step_name}")
                all_passed = False
                break
            else:
                print(f"[成功] 步骤完成: {step_name}")
        
        print("\n" + "=" * 60)
        if all_passed:
            print(f"[成功] 部署到 {environment} 成功!")
            if environment == "production" and version:
                print(f"   版本: v{version}")
                print(f"   发布说明: RELEASE_v{version}.md")
        else:
            print(f"[失败] 部署到 {environment} 失败!")
        
        return all_passed


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="心语编程语言部署系统")
    parser.add_argument("--environment", "-e", choices=["test", "production"], 
                       default="test", help="部署环境")
    parser.add_argument("--version", "-v", help="发布版本号")
    parser.add_argument("--skip-tests", action="store_true", help="跳过测试")
    parser.add_argument("--skip-checks", action="store_true", help="跳过代码质量检查")
    parser.add_argument("--check-only", action="store_true", help="只运行检查")
    parser.add_argument("--test-only", action="store_true", help="只运行测试")
    parser.add_argument("--build-only", action="store_true", help="只构建包")
    parser.add_argument("--publish-only", action="store_true", help="只发布包")
    parser.add_argument("--docs-only", action="store_true", help="只生成文档")
    
    args = parser.parse_args()
    
    project_root = Path(__file__).parent.parent
    deploy_system = DeploymentSystem(project_root)
    
    # 设置版本号
    version = args.version or deploy_system.version
    
    # 执行特定任务
    if args.check_only:
        print("运行代码质量检查...")
        success = deploy_system.run_code_quality_checks()
        sys.exit(0 if success else 1)
    
    elif args.test_only:
        print("运行测试...")
        success = deploy_system.run_tests("all")
        sys.exit(0 if success else 1)
    
    elif args.build_only:
        print("构建包...")
        success = deploy_system.build_package(clean=True)
        sys.exit(0 if success else 1)
    
    elif args.publish_only:
        print(f"发布包到 {args.environment}...")
        success = deploy_system.publish_package(args.environment)
        sys.exit(0 if success else 1)
    
    elif args.docs_only:
        print("生成文档...")
        success = deploy_system.generate_docs()
        sys.exit(0 if success else 1)
    
    # 执行完整部署流程
    else:
        success = deploy_system.deploy(
            environment=args.environment,
            version=version,
            skip_tests=args.skip_tests,
            skip_checks=args.skip_checks
        )
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()