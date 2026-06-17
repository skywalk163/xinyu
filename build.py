#!/usr/bin/env python3
"""
构建脚本 - 一键构建、测试和打包
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime


class BuildSystem:
    """构建系统"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.version = self._get_version()
        
    def _get_version(self) -> str:
        """获取版本号"""
        # 从pyproject.toml读取版本号
        pyproject_path = self.project_root / "pyproject.toml"
        if pyproject_path.exists():
            import tomli
            with open(pyproject_path, 'rb') as f:
                data = tomli.load(f)
                return data.get('project', {}).get('version', '0.1.0')
        return "0.1.0"
        
    def run_command(self, cmd: str, cwd: Path = None) -> bool:
        """运行命令"""
        if cwd is None:
            cwd = self.project_root
            
        print(f"运行命令: {cmd}")
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"命令失败: {cmd}")
                print(f"标准输出: {result.stdout}")
                print(f"标准错误: {result.stderr}")
                return False
                
            print(f"命令成功: {cmd}")
            if result.stdout:
                print(f"输出: {result.stdout}")
            return True
                
        except Exception as e:
            print(f"运行命令时出错: {e}")
            return False
            
    def install_dependencies(self) -> bool:
        """安装依赖"""
        print("安装依赖...")
        
        # 安装生产依赖
        if not self.run_command("pip install -r requirements.txt"):
            return False
            
        # 安装开发依赖
        if not self.run_command("pip install -r requirements-dev.txt"):
            return False
            
        return True
        
    def run_tests(self) -> bool:
        """运行测试"""
        print("运行测试...")
        
        # 运行单元测试
        if not self.run_command("pytest tests/ -v --cov=src --cov-report=term-missing"):
            return False
            
        # 运行代码质量检查
        if not self.run_command("flake8 src/ tests/ --max-line-length=100 --ignore=E203,W503"):
            return False
            
        # 运行类型检查
        if not self.run_command("mypy src/ --ignore-missing-imports"):
            return False
            
        # 运行安全扫描
        if not self.run_command("bandit -r src/ -ll"):
            return False
            
        return True
        
    def format_code(self) -> bool:
        """格式化代码"""
        print("格式化代码...")
        
        # 运行black格式化
        if not self.run_command("black src/ tests/"):
            return False
            
        # 运行isort排序导入
        if not self.run_command("isort src/ tests/"):
            return False
            
        return True
        
    def build_package(self) -> bool:
        """构建包"""
        print("构建包...")
        
        # 清理旧的构建文件
        dist_dir = self.project_root / "dist"
        build_dir = self.project_root / "build"
        
        if dist_dir.exists():
            import shutil
            shutil.rmtree(dist_dir)
            
        if build_dir.exists():
            import shutil
            shutil.rmtree(build_dir)
            
        # 构建包
        if not self.run_command("python -m build"):
            return False
            
        return True
        
    def check_build(self) -> bool:
        """检查构建"""
        print("检查构建...")
        
        # 检查构建文件
        dist_dir = self.project_root / "dist"
        if not dist_dir.exists():
            print("构建目录不存在")
            return False
            
        # 列出构建文件
        files = list(dist_dir.glob("*"))
        if not files:
            print("没有构建文件")
            return False
            
        print(f"构建文件: {[f.name for f in files]}")
        return True
        
    def generate_docs(self) -> bool:
        """生成文档"""
        print("生成文档...")
        
        docs_dir = self.project_root / "docs"
        if not docs_dir.exists():
            docs_dir.mkdir(exist_ok=True)
            
        # 这里可以添加文档生成逻辑
        # 例如使用Sphinx生成API文档
        
        return True
        
    def run_all(self) -> bool:
        """运行所有构建步骤"""
        print(f"开始构建心语编程语言 v{self.version}")
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        steps = [
            ("安装依赖", self.install_dependencies),
            ("格式化代码", self.format_code),
            ("运行测试", self.run_tests),
            ("构建包", self.build_package),
            ("检查构建", self.check_build),
            ("生成文档", self.generate_docs),
        ]
        
        all_passed = True
        for step_name, step_func in steps:
            print(f"\n步骤: {step_name}")
            print("-" * 30)
            
            if not step_func():
                print(f"步骤失败: {step_name}")
                all_passed = False
                break
                
        print("\n" + "=" * 50)
        if all_passed:
            print(f"构建成功! 版本: v{self.version}")
            print(f"构建文件位于: {self.project_root / 'dist'}")
        else:
            print("构建失败!")
            
        return all_passed


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="心语编程语言构建系统")
    parser.add_argument("--install", action="store_true", help="安装依赖")
    parser.add_argument("--test", action="store_true", help="运行测试")
    parser.add_argument("--format", action="store_true", help="格式化代码")
    parser.add_argument("--build", action="store_true", help="构建包")
    parser.add_argument("--docs", action="store_true", help="生成文档")
    parser.add_argument("--all", action="store_true", help="运行所有步骤")
    
    args = parser.parse_args()
    
    build_system = BuildSystem()
    
    # 如果没有指定具体步骤，默认运行所有步骤
    run_all = args.all or not any([args.install, args.test, args.format, args.build, args.docs])
    
    if run_all:
        success = build_system.run_all()
        sys.exit(0 if success else 1)
    else:
        success = True
        
        if args.install:
            success = success and build_system.install_dependencies()
            
        if args.format:
            success = success and build_system.format_code()
            
        if args.test:
            success = success and build_system.run_tests()
            
        if args.build:
            success = success and build_system.build_package()
            
        if args.docs:
            success = success and build_system.generate_docs()
            
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()