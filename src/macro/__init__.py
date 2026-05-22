"""
宏系统模块

提供编译时元编程能力，支持代码转换和领域特定语言扩展。
"""

from .macro_system import MacroSystem
from .macro_expander import MacroExpander
from .builtin_macros import register_builtin_macros
from .idiom_macros import register_idiom_macros

__all__ = [
    'MacroSystem',
    'MacroExpander',
    'register_builtin_macros',
    'register_idiom_macros',
]
