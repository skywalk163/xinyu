#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统一编译器接口实现

提供标准化的编译器接口，整合词法分析、语法分析、语义分析和代码生成。
"""

from typing import Any, Dict, List, Optional

from src.codegen.python_codegen import PythonCodegen
from src.error_handling import ErrorHandler, ErrorType
from src.lexer.lexer_with_error_handler import LexerWithErrorHandler
from src.parser.parser_with_error_handler import ParserWithErrorHandler
from src.runtime.secure_executor import SecureExecutor
from src.semantic.analyzer_with_inference import SemanticAnalyzerWithInference

from . import Compiler, Diagnostic, Position


class XinyuCompiler(Compiler):
    """心语编程语言编译器实现"""

    def __init__(self, enable_safety: bool = True):
        """初始化编译器

        Args:
            enable_safety: 是否启用安全限制
        """
        super().__init__()
        self.enable_safety = enable_safety
        self.error_handler = ErrorHandler()
        self._initialize_components()

    def _initialize_components(self):
        """初始化各个组件"""
        # 词法分析器
        self.lexer = LexerWithErrorHandler

        # 语法分析器
        self.parser = ParserWithErrorHandler

        # 语义分析器
        self.semantic_analyzer = SemanticAnalyzerWithInference

        # 代码生成器
        self.code_generator = PythonCodegen()

        # 运行时（用于执行）
        self.runtime = SecureExecutor() if self.enable_safety else None

    def compile(self, source: str, target: str = "python") -> str:
        """编译源代码到目标语言

        Args:
            source: 源代码字符串
            target: 目标语言（目前只支持"python"）

        Returns:
            生成的目标代码

        Raises:
            CompilationError: 编译过程中出现错误
        """
        if target != "python":
            raise ValueError(f"不支持的目标语言: {target}")

        # 清空之前的诊断信息
        self.diagnostics.clear()

        try:
            # 1. 词法分析
            lexer = self.lexer(source, self.error_handler)
    _ = ze()  # 未使用变量

            # 收集词法错误
            self._collect_lexer_errors()

            # 2. 语法分析
            parser = self.parser(tokens, self.error_handler)
    _ = ()  # 未使用变量

            # 收集语法错误
            self._collect_parser_errors()

            # 如果有错误，提前返回
            if self.error_handler.has_errors():
                return ""

            # 3. 语义分析
            analyzer = self.semantic_analyzer()
            analyzer.analyze(ast)

            # 收集语义错误
            self._collect_semantic_errors(analyzer)

            # 如果有错误，提前返回
            if self.error_handler.has_errors():
                return ""

            # 4. 代码生成
            generated_code = self.code_generator.generate(ast)

            return generated_code

        except Exception as e:
            # 捕获未处理的异常
            self.diagnostics.append(
                Diagnostic(
                    level="error",
                    message=f"编译过程中发生未预期的错误: {str(e)}",
                    position=Position(line=0, column=0),
                    code="COMPILER_INTERNAL_ERROR",
                )
            )
            return ""

    def _collect_lexer_errors(self):
        """收集词法分析错误"""
        for error in self.error_handler.get_errors():
            if error.error_type == ErrorType.LEXER_ERROR:
                self.diagnostics.append(
                    Diagnostic(
                        level="error",
                        message=error.message,
                        position=Position(line=error.line, column=error.column),
                        code=error.error_code.name if hasattr(error, "error_code") else None,
                        suggestion=error.suggestion,
                    )
                )

    def _collect_parser_errors(self):
        """收集语法分析错误"""
        for error in self.error_handler.get_errors():
            if error.error_type == ErrorType.PARSER_ERROR:
                self.diagnostics.append(
                    Diagnostic(
                        level="error",
                        message=error.message,
                        position=Position(line=error.line, column=error.column),
                        code=error.error_code.name if hasattr(error, "error_code") else None,
                        suggestion=error.suggestion,
                    )
                )

    def _collect_semantic_errors(self, analyzer):
        """收集语义分析错误"""
        # 注意：当前语义分析器可能没有集成到错误处理器中
        # 这里需要根据实际实现调整
        pass

    def get_diagnostics(self) -> List[Diagnostic]:
        """获取编译过程中的诊断信息"""
        return self.diagnostics

    def has_errors(self) -> bool:
        """检查是否有错误"""
        return any(d.level == "error" for d in self.diagnostics)

    def execute(self, source: str, context: Optional[Dict] = None) -> Any:
        """编译并执行源代码

        Args:
            source: 源代码字符串
            context: 执行上下文（可选）

        Returns:
            执行结果

        Raises:
            CompilationError: 编译错误
            RuntimeError: 运行时错误
        """
        if not self.runtime:
            raise RuntimeError("未启用安全运行时环境")

        # 编译源代码
        python_code = self.compile(source)

        if self.has_errors():
            error_messages = "\n".join(str(d) for d in self.diagnostics)
            raise CompilationError(f"编译错误:\n{error_messages}")

        # 执行生成的代码
        return self.runtime.execute(python_code, context)

    def validate(self, source: str) -> bool:
        """验证源代码语法是否正确

        Args:
            source: 源代码字符串

        Returns:
            是否语法正确
        """
        try:
            # 只进行词法和语法分析
            lexer = self.lexer(source, self.error_handler)
    _ = ze()  # 未使用变量

            parser = self.parser(tokens, self.error_handler)
            parser.parse()

            return not self.error_handler.has_errors()

        except Exception:
            return False


class CompilationError(Exception):
    """编译错误异常"""

    pass


# 导出
__all__ = ["XinyuCompiler", "CompilationError"]
