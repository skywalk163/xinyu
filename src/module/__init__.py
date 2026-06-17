"""
心语语言模块管理模块

该模块提供Python标准库模块的中文接口封装和模块管理功能。
"""

from .loader import ModuleLoader
from .manager import ModuleManager

__all__ = ["ModuleManager", "ModuleLoader"]
