"""
预提交钩子管理器
用于管理和运行预提交检查
"""

import subprocess
import sys
import yaml
from pathlib import Path
from typing import List, Dict, Any, Callable, Optional


class PreCommitHook:
    """预提交钩子管理器"""
    
    def __init__(self, config_path: str = ".pre-commit-config.yaml"):
        self.config = self._load_config(config_path)
        self.hooks: List[Callable[[], bool]] = []
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载预提交配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"配置文件 {config_path} 不存在")
            return {}
        except yaml.YAMLError as e:
            print(f"配置文件解析错误: {e}")
            return {}
            
    def add_hook(self, name: str, command: str, files: List[str]) -> None:
        """添加预提交检查钩子"""
        def hook_func() -> bool:
            print(f"运行钩子: {name}")
            try:
                result = subprocess.run(
                    command.split(),
                    capture_output=True,
                    text=True,
                    check=True
                )
                print(f"钩子 {name} 执行成功")
                return True
            except subprocess.CalledProcessError as e:
                print(f"钩子 {name} 执行失败:")
                print(e.stdout)
                print(e.stderr)
                return False
                
        self.hooks.append(hook_func)
        
    def run_hooks(self, staged_files: List[str]) -> bool:
        """运行所有预提交检查"""
        if not self.hooks:
            print("没有配置任何钩子")
            return True
            
        print(f"运行预提交检查，涉及文件: {len(staged_files)} 个")
        
        all_passed = True
        for hook in self.hooks:
            if not hook():
                all_passed = False
                
        return all_passed
        
    def format_code(self, files: List[str]) -> bool:
        """运行代码格式化检查"""
        if not files:
            print("没有需要格式化的文件")
            return True
            
        print(f"格式化 {len(files)} 个文件")
        
        # 运行black格式化
        try:
            result = subprocess.run(
                ["black", "--check"] + files,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print("代码格式化检查失败，需要运行 black 进行格式化:")
                print(result.stdout)
                print(result.stderr)
                return False
                
            print("代码格式化检查通过")
            return True
            
        except FileNotFoundError:
            print("black 未安装，跳过格式化检查")
            return True
            
    def type_check(self, files: List[str]) -> bool:
        """运行类型检查"""
        if not files:
            print("没有需要类型检查的文件")
            return True
            
        print(f"类型检查 {len(files)} 个文件")
        
        # 运行mypy类型检查
        try:
            result = subprocess.run(
                ["mypy", "--ignore-missing-imports"] + files,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print("类型检查失败:")
                print(result.stdout)
                print(result.stderr)
                return False
                
            print("类型检查通过")
            return True
            
        except FileNotFoundError:
            print("mypy 未安装，跳过类型检查")
            return True
            
    def run_tests(self) -> bool:
        """运行单元测试"""
        print("运行单元测试...")
        
        try:
            result = subprocess.run(
                ["pytest", "tests/", "-xvs", "--tb=short", "--cov=src", "--cov-report=term-missing"],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print("单元测试失败:")
                print(result.stdout)
                print(result.stderr)
                return False
                
            print("单元测试通过")
            return True
            
        except FileNotFoundError:
            print("pytest 未安装，跳过单元测试")
            return True
            
    def check_code_quality(self, files: List[str]) -> bool:
        """运行代码质量检查"""
        if not files:
            print("没有需要检查的文件")
            return True
            
        print(f"代码质量检查 {len(files)} 个文件")
        
        # 运行flake8检查
        try:
            result = subprocess.run(
                ["flake8", "--max-line-length=100", "--ignore=E203,W503"] + files,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print("代码质量检查失败:")
                print(result.stdout)
                print(result.stderr)
                return False
                
            print("代码质量检查通过")
            return True
            
        except FileNotFoundError:
            print("flake8 未安装，跳过代码质量检查")
            return True
            
    def security_scan(self, files: List[str]) -> bool:
        """运行安全扫描"""
        if not files:
            print("没有需要安全扫描的文件")
            return True
            
        print(f"安全扫描 {len(files)} 个文件")
        
        # 运行bandit安全扫描
        try:
            result = subprocess.run(
                ["bandit", "-r", "src/", "-ll"],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print("安全扫描发现潜在问题:")
                print(result.stdout)
                print(result.stderr)
                return False
                
            print("安全扫描通过")
            return True
            
        except FileNotFoundError:
            print("bandit 未安装，跳过高安全扫描")
            return True


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="预提交钩子管理器")
    parser.add_argument("--files", nargs="*", help="要检查的文件列表")
    parser.add_argument("--format", action="store_true", help="运行代码格式化检查")
    parser.add_argument("--type-check", action="store_true", help="运行类型检查")
    parser.add_argument("--test", action="store_true", help="运行单元测试")
    parser.add_argument("--quality", action="store_true", help="运行代码质量检查")
    parser.add_argument("--security", action="store_true", help="运行安全扫描")
    parser.add_argument("--all", action="store_true", help="运行所有检查")
    
    args = parser.parse_args()
    
    hook_manager = PreCommitHook()
    
    files = args.files or []
    
    # 如果没有指定具体检查，默认运行所有检查
    run_all = args.all or not any([args.format, args.type_check, args.test, args.quality, args.security])
    
    all_passed = True
    
    if run_all or args.format:
        if not hook_manager.format_code(files):
            all_passed = False
            
    if run_all or args.type_check:
        if not hook_manager.type_check(files):
            all_passed = False
            
    if run_all or args.test:
        if not hook_manager.run_tests():
            all_passed = False
            
    if run_all or args.quality:
        if not hook_manager.check_code_quality(files):
            all_passed = False
            
    if run_all or args.security:
        if not hook_manager.security_scan(files):
            all_passed = False
            
    if not all_passed:
        print("\n预提交检查失败，请修复问题后再提交")
        sys.exit(1)
    else:
        print("\n所有预提交检查通过")


if __name__ == "__main__":
    main()