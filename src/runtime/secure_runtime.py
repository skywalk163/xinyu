# -*- coding: utf-8 -*-
"""安全运行时环境

使用RestrictedPython实现安全的代码执行环境，防止代码注入攻击。

安全措施：
1. 使用RestrictedPython编译受限代码
2. 创建受限的全局环境，禁用危险函数
3. 限制可用的模块和函数
4. 提供输入验证机制
"""

import re
from typing import Any, Dict, Optional, Set, Tuple

from RestrictedPython import compile_restricted
from RestrictedPython.Guards import guarded_iter_unpack_sequence, safe_builtins


class SecurityError(Exception):
    """安全错误"""

    pass


class InputValidator:
    """输入验证器

    验证源代码的安全性，防止代码注入攻击。
    """

    # 最大源代码长度（1MB）
    MAX_SOURCE_LENGTH = 1024 * 1024

    # 危险模式列表
    DANGEROUS_PATTERNS = [
        r"__import__\s*\(",  # 禁止动态导入
        r"eval\s*\(",  # 禁止eval
        r"exec\s*\(",  # 禁止exec
        r"compile\s*\(",  # 禁止compile
        r"open\s*\(",  # 禁止文件操作（将在受限环境中提供安全版本）
        r"os\.",  # 禁止os模块
        r"sys\.",  # 禁止sys模块
        r"subprocess\.",  # 禁止subprocess模块
        r"__builtins__\s*\[",  # 禁止访问__builtins__
        r'getattr\s*\([^,]+,\s*[\'"]__class__[\'"]',  # 禁止通过getattr访问__class__
    ]

    @classmethod
    def validate_source(cls, source: str) -> Tuple[bool, Optional[str]]:
        """验证源代码安全性

        Args:
            source: 源代码字符串

        Returns:
            (是否安全, 错误信息)
        """
        # 检查长度限制
        if len(source) > cls.MAX_SOURCE_LENGTH:
            return False, f"源代码过长（最大{cls.MAX_SOURCE_LENGTH}字节）"

        # 检查编码格式
        try:
            source.encode("utf-8")
        except UnicodeEncodeError:
            return False, "源代码包含无效的UTF-8字符"

        # 检查危险模式
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, source):
                return False, f"检测到危险模式: {pattern}"

        return True, None

    @classmethod
    def validate_encoding(cls, source: str) -> Tuple[bool, Optional[str]]:
        """验证编码格式

        Args:
            source: 源代码字符串

        Returns:
            (是否有效, 错误信息)
        """
        try:
            source.encode("utf-8")
            return True, None
        except UnicodeEncodeError as e:
            return False, f"编码错误: {e}"


class SecureRuntime:
    """安全运行时环境

    使用RestrictedPython限制危险操作，提供安全的代码执行环境。
    """

    def __init__(self, allowed_modules: Optional[Set[str]] = None):
        """初始化安全运行时环境

        Args:
            allowed_modules: 允许的模块集合，默认为安全模块
        """
        # 默认允许的安全模块
        self.DEFAULT_ALLOWED_MODULES = {
            # 数学相关
            "math",
            "random",
            "statistics",
            # 数据处理
            "json",
            "re",
            "csv",
            # 时间日期
            "datetime",
            "date",
            "time",
            "timedelta",
            # 集合和迭代
            "collections",
            "itertools",
            "functools",
            # 字符串处理
            "string",
            "textwrap",
            # 编码
            "base64",
            "hashlib",
            # 其他安全模块
            "copy",
            "pprint",
            "operator",
        }

        self.allowed_modules = (
            allowed_modules if allowed_modules is not None else self.DEFAULT_ALLOWED_MODULES
        )
        self.validator = InputValidator()

    def execute(
        self, code: str, validate: bool = True
    ) -> Tuple[bool, Optional[Any], Optional[str]]:
        """在受限环境中执行代码

        Args:
            code: Python代码字符串
            validate: 是否进行输入验证

        Returns:
            (是否成功, 执行结果, 错误信息)
        """
        try:
            # 输入验证
            if validate:
                is_valid, error_msg = self.validator.validate_source(code)
                if not is_valid:
                    return False, None, f"输入验证失败: {error_msg}"

            # 编译为受限代码
            result = compile_restricted(code, "<inline>", "exec")

            # RestrictedPython返回一个code对象或包含errors的对象
            # 检查是否有编译错误
            if hasattr(result, "errors") and result.errors:
                errors = (
                    result.errors if isinstance(result.errors, (list, tuple)) else [result.errors]
                )
                return False, None, f"编译错误: {', '.join(str(e) for e in errors)}"

            # 获取字节码
            byte_code = result.code if hasattr(result, "code") else result

            if byte_code is None:
                return False, None, "编译失败：未生成字节码"

            # 创建受限全局环境
            restricted_globals = self._create_restricted_globals()

            # 执行代码
            exec(byte_code, restricted_globals)

            # 返回结果（优先返回result变量，其次__result__）
            exec_result = restricted_globals.get("result") or restricted_globals.get("__result__")
            return True, exec_result, None

        except SyntaxError as e:
            return False, None, f"语法错误: {e}"
        except Exception as e:
            return False, None, f"执行错误: {e}"

    def _create_restricted_globals(self) -> Dict[str, Any]:
        """创建受限的全局环境

        Returns:
            受限的全局环境字典
        """
        # 导入允许的模块
        import json
        import math
        import random
        import re
        from datetime import date, datetime, time, timedelta

        # 创建打印守卫类
        class PrintGuard:
            """打印守卫，用于RestrictedPython"""

            def _call_print(self, *args, **kwargs):
                print(*args, **kwargs)
                return None

        # 创建打印守卫实例
        print_guard = PrintGuard()

        # 创建安全的内置函数集合
        safe_builtins_dict = {
            # 允许的内置函数
            "print": print,
            "len": len,
            "range": range,
            "list": list,
            "dict": dict,
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
            "tuple": tuple,
            "set": set,
            "abs": abs,
            "min": min,
            "max": max,
            "sum": sum,
            "sorted": sorted,
            "enumerate": enumerate,
            "zip": zip,
            "map": map,
            "filter": filter,
            "isinstance": isinstance,
            "hasattr": hasattr,
            "getattr": getattr,
            # RestrictedPython需要的守卫函数
            "_iter_unpack_sequence": guarded_iter_unpack_sequence,
            "_print_": lambda getattr_func: print_guard,  # 返回打印守卫
            "_getattr_": getattr,  # RestrictedPython的getattr守卫
            "_write_": lambda x: x,  # RestrictedPython的write守卫
        }

        # 创建受限全局环境
        restricted_globals = {
            "__builtins__": safe_builtins_dict,
            "__name__": "__main__",
            "__doc__": None,
        }

        # 添加允许的模块
        if "math" in self.allowed_modules:
            restricted_globals["math"] = math
        if "random" in self.allowed_modules:
            restricted_globals["random"] = random
        if "json" in self.allowed_modules:
            restricted_globals["json"] = json
        if "re" in self.allowed_modules:
            restricted_globals["re"] = re
        if "datetime" in self.allowed_modules:
            restricted_globals["datetime"] = datetime
            restricted_globals["date"] = date
            restricted_globals["time"] = time
            restricted_globals["timedelta"] = timedelta

        # 添加更多安全模块
        if "statistics" in self.allowed_modules:
            import statistics

            restricted_globals["statistics"] = statistics
        if "csv" in self.allowed_modules:
            import csv

            restricted_globals["csv"] = csv
        if "collections" in self.allowed_modules:
            import collections

            restricted_globals["collections"] = collections
        if "itertools" in self.allowed_modules:
            import itertools

            restricted_globals["itertools"] = itertools
        if "functools" in self.allowed_modules:
            import functools

            restricted_globals["functools"] = functools
        if "string" in self.allowed_modules:
            import string

            restricted_globals["string"] = string
        if "textwrap" in self.allowed_modules:
            import textwrap

            restricted_globals["textwrap"] = textwrap
        if "base64" in self.allowed_modules:
            import base64

            restricted_globals["base64"] = base64
        if "hashlib" in self.allowed_modules:
            import hashlib

            restricted_globals["hashlib"] = hashlib
        if "copy" in self.allowed_modules:
            import copy

            restricted_globals["copy"] = copy
        if "pprint" in self.allowed_modules:
            import pprint

            restricted_globals["pprint"] = pprint
        if "operator" in self.allowed_modules:
            import operator

            restricted_globals["operator"] = operator

        # 心语内置值
        restricted_globals["真"] = True
        restricted_globals["假"] = False

        return restricted_globals

    def compile_restricted_code(self, code: str) -> Tuple[bool, Optional[Any], Optional[str]]:
        """编译受限代码（不执行）

        Args:
            code: Python代码字符串

        Returns:
            (是否成功, 编译后的字节码, 错误信息)
        """
        try:
            result = compile_restricted(code, "<inline>", "exec")

            # 检查是否有编译错误
            if hasattr(result, "errors") and result.errors:
                errors = (
                    result.errors if isinstance(result.errors, (list, tuple)) else [result.errors]
                )
                return False, None, f"编译错误: {', '.join(str(e) for e in errors)}"

            # 获取字节码
            byte_code = result.code if hasattr(result, "code") else result

            if byte_code is None:
                return False, None, "编译失败：未生成字节码"

            return True, byte_code, None

        except SyntaxError as e:
            return False, None, f"语法错误: {e}"
        except Exception as e:
            return False, None, f"编译错误: {e}"


# 便捷函数
def create_safe_runtime(allowed_modules: Optional[Set[str]] = None) -> SecureRuntime:
    """创建安全运行时环境

    Args:
        allowed_modules: 允许的模块集合

    Returns:
        SecureRuntime实例
    """
    return SecureRuntime(allowed_modules)


def execute_safely(
    code: str, allowed_modules: Optional[Set[str]] = None
) -> Tuple[bool, Optional[Any], Optional[str]]:
    """安全执行代码

    Args:
        code: Python代码字符串
        allowed_modules: 允许的模块集合

    Returns:
        (是否成功, 执行结果, 错误信息)
    """
    runtime = SecureRuntime(allowed_modules)
    return runtime.execute(code)
