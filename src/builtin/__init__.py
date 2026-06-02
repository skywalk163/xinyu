"""
心语语言内置函数模块

该模块提供Python内置函数的中文接口封装，支持中英文双语调用。
"""

from .registry import BuiltinRegistry
from .name_mapper import NameMapper

__all__ = ['BuiltinRegistry', 'NameMapper']
