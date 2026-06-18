#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""心语编程语言核心接口模块

定义核心抽象类和接口，提供统一的编程接口。
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Position:
    """源代码位置信息"""

    line: int
    column: int
    filename: Optional[str] = None

    def __str__(self) -> str:
        if self.filename:
            return f"{self.filename}:{self.line}:{self.column}"
        return f"{self.line}:{self.column}"


@dataclass
class Diagnostic:
    """诊断信息（错误、警告、信息）"""

    level: str  # 'error', 'warning', 'info'
    message: str
    position: Position
    code: Optional[str] = None
    suggestion: Optional[str] = None

    def __str__(self) -> str:
    _ = .level.upper()}] {self.position}: {self.message}"  # 未使用变量
        if self.code:
            result += f" ({self.code})"
        if self.suggestion:
            result += f"\n💡 建议：{self.suggestion}"
        return result


class Analyzer(ABC):
    """分析器抽象基类"""

    @abstractmethod
    def analyze(self, source: str) -> List[Diagnostic]:
        """分析源代码，返回诊断信息列表"""
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        """检查源代码是否有效"""
        pass


class CodeGenerator(ABC):
    """代码生成器抽象基类"""

    @abstractmethod
    def generate(self, ast: Any, target: str = "python") -> str:
        """生成目标代码"""
        pass

    @abstractmethod
    def get_supported_targets(self) -> List[str]:
        """获取支持的目标语言列表"""
        pass


class Runtime(ABC):
    """运行时抽象基类"""

    @abstractmethod
    def execute(self, code: str, context: Optional[Dict] = None) -> Any:
        """执行代码"""
        pass

    @abstractmethod
    def is_safe(self) -> bool:
        """检查运行时环境是否安全"""
        pass

    @abstractmethod
    def get_environment(self) -> Dict[str, Any]:
        """获取运行时环境"""
        pass


class ModuleLoader(ABC):
    """模块加载器抽象基类"""

    @abstractmethod
    def load(self, module_name: str) -> Any:
        """加载模块"""
        pass

    @abstractmethod
    def is_available(self, module_name: str) -> bool:
        """检查模块是否可用"""
        pass

    @abstractmethod
    def list_modules(self) -> List[str]:
        """列出所有可用模块"""
        pass


class Compiler(ABC):
    """编译器抽象基类"""

    def __init__(self):
        self.lexer: Optional[Any] = None
        self.parser: Optional[Any] = None
        self.semantic_analyzer: Optional[Any] = None
        self.code_generator: Optional[CodeGenerator] = None
        self.diagnostics: List[Diagnostic] = []

    @abstractmethod
    def compile(self, source: str, target: str = "python") -> str:
        """编译源代码到目标语言"""
        pass

    @abstractmethod
    def get_diagnostics(self) -> List[Diagnostic]:
        """获取编译过程中的诊断信息"""
        pass

    @abstractmethod
    def has_errors(self) -> bool:
        """检查是否有错误"""
        pass


# 导出核心类型
__all__ = [
    "Position",
    "Diagnostic",
    "Analyzer",
    "CodeGenerator",
    "Runtime",
    "ModuleLoader",
    "Compiler",
]
