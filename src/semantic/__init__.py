# -*- coding: utf-8 -*-
"""语义分析模块

提供语义分析器和作用域管理。
"""

from src.semantic.analyzer import SemanticAnalyzer, SemanticError
from src.semantic.scope import Scope

__all__ = ["Scope", "SemanticAnalyzer", "SemanticError"]
