# -*- coding: utf-8 -*-
"""心语语言模块导入系统

支持模块导入和使用：
- 导入标准库模块
- 导入用户自定义模块
- 模块路径搜索
- 模块缓存
"""

import importlib.util
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


class ModuleSystem:
    """模块导入系统"""

    def __init__(self, root_dir: str = None):
        """初始化模块系统

        Args:
            root_dir: 项目根目录
        """
        self.root_dir = Path(root_dir or os.getcwd())
        self.module_cache: Dict[str, Any] = {}
        self.search_paths: List[Path] = []

        # 初始化搜索路径
        self._init_search_paths()

    def _init_search_paths(self):
        """初始化模块搜索路径"""
        # 1. 标准库路径
        stdlib_path = self.root_dir / "stdlib"
        if stdlib_path.exists():
            self.search_paths.append(stdlib_path)

        # 2. 用户模块路径
        user_modules_path = self.root_dir / "modules"
        if user_modules_path.exists():
            self.search_paths.append(user_modules_path)

        # 3. 当前目录
        self.search_paths.append(self.root_dir)

        # 4. Python标准库（用于导入Python模块）
        self.search_paths.append(Path(sys.prefix) / "lib")

    def import_module(self, module_name: str) -> Optional[Any]:
        """导入模块

        Args:
            module_name: 模块名

        Returns:
            模块对象，如果导入失败则返回None
        """
        # 检查缓存
        if module_name in self.module_cache:
            return self.module_cache[module_name]

        # 搜索模块文件
        module_file = self._find_module_file(module_name)

        if module_file is None:
            # 尝试导入Python模块
            return self._import_python_module(module_name)

        # 加载心语模块
        module = self._load_xinyu_module(module_file)

        if module is not None:
            self.module_cache[module_name] = module

        return module

    def _find_module_file(self, module_name: str) -> Optional[Path]:
        """查找模块文件

        Args:
            module_name: 模块名

        Returns:
            模块文件路径，如果未找到则返回None
        """
        # 可能的文件名
        possible_names = [
            f"{module_name}.yan",
            f"{module_name}.py",
            f"{module_name}/__init__.yan",
            f"{module_name}/__init__.py",
        ]

        # 在搜索路径中查找
        for search_path in self.search_paths:
            for name in possible_names:
                module_file = search_path / name
                if module_file.exists():
                    return module_file

        return None

    def _import_python_module(self, module_name: str) -> Optional[Any]:
        """导入Python模块

        Args:
            module_name: 模块名

        Returns:
            Python模块对象
        """
        try:
            module = importlib.import_module(module_name)
            self.module_cache[module_name] = module
            return module
        except ImportError:
            return None

    def _load_xinyu_module(self, module_file: Path) -> Optional[Dict]:
        """加载心语模块

        Args:
            module_file: 模块文件路径

        Returns:
            模块字典（包含函数和变量）
        """
        try:
            # 读取模块代码
            with open(module_file, "r", encoding="utf-8") as f:
                code = f.read()

            # 编译和执行模块
            from src.codegen.python_codegen import PythonCodegen
            from src.lexer.lexer import Lexer
            from src.parser.parser import Parser

            # 词法分析
            lexer = Lexer(code)
    _ = ze()  # 未使用变量

            # 语法分析
            parser = Parser(tokens)
    _ = ()  # 未使用变量

            # 代码生成
            codegen = PythonCodegen()
            python_code = codegen.generate(ast)

            # 执行模块代码
            module_globals = {}
            exec(python_code, module_globals)

            # 移除内置属性
            module_dict = {k: v for k, v in module_globals.items() if not k.startswith("_")}

            return module_dict

        except Exception as e:
            print(f"加载模块失败: {e}")
            return None

    def get_module_attribute(self, module_name: str, attr_name: str) -> Optional[Any]:
        """获取模块属性

        Args:
            module_name: 模块名
            attr_name: 属性名

        Returns:
            属性值
        """
        module = self.import_module(module_name)

        if module is None:
            return None

        if isinstance(module, dict):
            return module.get(attr_name)
        else:
            return getattr(module, attr_name, None)

    def add_search_path(self, path: str):
        """添加搜索路径

        Args:
            path: 路径字符串
        """
        search_path = Path(path)
        if search_path.exists() and search_path not in self.search_paths:
            self.search_paths.append(search_path)

    def list_modules(self) -> List[str]:
        """列出所有可用模块

        Returns:
            模块名列表
        """
        modules = set()

        # 搜索.yan文件
        for search_path in self.search_paths:
            if search_path.exists():
                for file in search_path.glob("*.yan"):
                    modules.add(file.stem)

                # 搜索子目录
                for subdir in search_path.iterdir():
                    if subdir.is_dir():
                        init_file = subdir / "__init__.yan"
                        if init_file.exists():
                            modules.add(subdir.name)

        return sorted(list(modules))


# 全局模块系统实例
_module_system = None


def get_module_system(root_dir: str = None) -> ModuleSystem:
    """获取全局模块系统实例

    Args:
        root_dir: 项目根目录

    Returns:
        ModuleSystem实例
    """
    global _module_system

    if _module_system is None:
        _module_system = ModuleSystem(root_dir)

    return _module_system


def import_module(module_name: str) -> Optional[Any]:
    """导入模块（便捷函数）

    Args:
        module_name: 模块名

    Returns:
        模块对象
    """
    return get_module_system().import_module(module_name)


# 使用示例
if __name__ == "__main__":
    ms = ModuleSystem()

    print("=== 模块搜索路径 ===")
    for path in ms.search_paths:
        print(f"  {path}")

    print("\n=== 可用模块 ===")
    modules = ms.list_modules()
    for module in modules:
        print(f"  {module}")

    print("\n=== 导入模块 ===")
    # 导入标准库模块
    math_module = ms.import_module("math")
    if math_module:
        print(f"  math模块: {list(math_module.keys())[:5]}...")

    # 导入Python模块
    os_module = ms.import_module("os")
    if os_module:
        print(f"  os模块: {type(os_module)}")
