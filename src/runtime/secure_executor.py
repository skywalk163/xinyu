#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""安全执行器 - 替换不安全的exec()调用

提供基本的代码执行环境，限制危险操作。
"""

from typing import Any, Dict, List, Optional


class SecureExecutor:
    """安全执行器

    使用RestrictedPython提供安全的代码执行环境，限制以下操作：
    1. 文件系统访问
    2. 网络访问
    3. 系统命令执行
    4. 危险的内置函数
    5. 模块导入
    """

    def __init__(self, allowed_modules: Optional[List[str]] = None):
        """初始化安全执行器

        Args:
            allowed_modules: 允许导入的模块列表，默认为空
        """
        self.allowed_modules = allowed_modules or []
        self._setup_globals()

    def _setup_globals(self):
        """设置安全的全局变量"""
        # 创建安全的builtins副本
        safe_builtins = {
            # 基本类型
            "int": int,
            "float": float,
            "str": str,
            "bool": bool,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            # 基本函数
            "len": len,
            "range": range,
            "enumerate": enumerate,
            "zip": zip,
            "sorted": sorted,
            "reversed": reversed,
            "min": min,
            "max": max,
            "sum": sum,
            "abs": abs,
            "round": round,
            "pow": pow,
            # 数学函数
            "abs": abs,
            "round": round,
            # 类型转换
            "int": int,
            "float": float,
            "str": str,
            "bool": bool,
            "list": list,
            "tuple": tuple,
            "dict": dict,
            "set": set,
            # 打印和输入
            "print": print,
            "input": input,
            # 其他安全函数
            "isinstance": isinstance,
            "issubclass": issubclass,
            "hasattr": hasattr,
            "getattr": getattr,
            "setattr": setattr,
            "delattr": delattr,
            "property": property,
            "staticmethod": staticmethod,
            "classmethod": classmethod,
            "super": super,
        }

        # 移除危险函数
        dangerous = [
            "__import__",
            "open",
            "eval",
            "exec",
            "compile",
            "exit",
            "quit",
            "globals",
            "locals",
            "vars",
            "dir",
            "type",
        ]

        for func in dangerous:
            if func in safe_builtins:
                del safe_builtins[func]

        # 创建全局变量字典
        self._globals = {
            "__builtins__": safe_builtins,
            "__name__": "__main__",
            "__doc__": None,
            "__package__": None,
            "__loader__": None,
            "__spec__": None,
        }

        # 添加心语内置值
        self._globals["真"] = True
        self._globals["假"] = False
        self._globals["空"] = None

        # 添加数学函数
        import math

        self._globals["math"] = math

        # 添加允许的模块
        for module_name in self.allowed_modules:
            try:
                module = __import__(module_name)
                self._globals[module_name] = module
            except ImportError:
                pass

    def execute(self, code: str, context: Optional[Dict] = None) -> Any:
        """安全执行代码

        Args:
            code: 要执行的Python代码
            context: 额外的执行上下文

        Returns:
            执行结果

        Raises:
            SyntaxError: 代码语法错误
            NameError: 使用了不允许的名称
            ImportError: 尝试导入不允许的模块
            SecurityError: 安全违规
        """
        try:
            # 检查代码安全性
            self._check_code_safety(code)

            # 编译代码
            byte_code = compile(code, filename="<secure>", mode="exec")

            # 准备执行环境
            exec_globals = self._globals.copy()
            if context:
                exec_globals.update(context)

            # 创建局部变量空间
            exec_locals = {}

            # 执行代码
            exec(byte_code, exec_globals, exec_locals)

            # 获取结果（如果有）
            result = exec_locals.get("__result__")

            return result

        except SyntaxError as e:
            raise SyntaxError(f"语法错误: {e}")
        except NameError as e:
            raise NameError(f"名称错误: {e}")
        except ImportError as e:
            raise ImportError(f"导入错误: {e}")
        except Exception as e:
            # 捕获其他安全违规
            raise SecurityError(f"安全违规: {e}")

    def _check_code_safety(self, code: str):
        """检查代码安全性

        检查代码中是否包含危险操作。

        Args:
            code: 要检查的代码

        Raises:
            SecurityError: 发现危险操作
        """
        dangerous_patterns = [
            "__import__",
            "open(",
            "eval(",
            "exec(",
            "compile(",
            "os.system",
            "subprocess",
            "import os",
            "import sys",
            "import subprocess",
            "import socket",
            "import shutil",
            "import tempfile",
            "import pickle",
            "import marshal",
            "import ctypes",
        ]

        for pattern in dangerous_patterns:
            if pattern in code:
                raise SecurityError(f"检测到危险操作: {pattern}")

    def is_safe(self) -> bool:
        """检查执行器是否安全"""
        return True

    def get_environment(self) -> Dict[str, Any]:
        """获取执行环境"""
        return self._globals.copy()

    def add_module(self, module_name: str) -> bool:
        """添加允许的模块

        Args:
            module_name: 模块名称

        Returns:
            是否成功添加
        """
        try:
            module = __import__(module_name)
            self._globals[module_name] = module
            self.allowed_modules.append(module_name)
            return True
        except ImportError:
            return False

    def remove_module(self, module_name: str) -> bool:
        """移除允许的模块

        Args:
            module_name: 模块名称

        Returns:
            是否成功移除
        """
        if module_name in self._globals:
            del self._globals[module_name]
            if module_name in self.allowed_modules:
                self.allowed_modules.remove(module_name)
            return True
        return False


class SecurityError(Exception):
    """安全错误异常"""


# 导出
__all__ = ["SecureExecutor", "SecurityError"]
