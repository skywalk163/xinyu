"""
心语语言内置函数模块

该模块提供Python内置函数的中文接口封装，支持中英文双语调用。
"""

from .name_mapper import NameMapper
from .registry import BuiltinRegistry

__all__ = ["BuiltinRegistry", "NameMapper"]
