# -*- coding: utf-8 -*-
"""输入验证模块

提供全面的输入验证机制，防止代码注入攻击。
"""

import re
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class ValidationResult:
    """验证结果"""

    is_valid: bool
    errors: List[str]
    warnings: List[str]

    def __bool__(self) -> bool:
        return self.is_valid


class SourceCodeValidator:
    """源代码验证器

    验证心语源代码的安全性和有效性。
    """

    # 配置参数
    MAX_SOURCE_LENGTH = 1024 * 1024  # 1MB
    MAX_LINE_LENGTH = 10000  # 单行最大长度
    MAX_NESTING_DEPTH = 100  # 最大嵌套深度

    # 危险模式（Python代码层面）
    DANGEROUS_PYTHON_PATTERNS = [
        (r"__import__\s*\(", "禁止使用__import__"),
        (r"eval\s*\(", "禁止使用eval"),
        (r"exec\s*\(", "禁止使用exec"),
        (r"compile\s*\(", "禁止使用compile"),
        (r"os\.", "禁止使用os模块"),
        (r"sys\.", "禁止使用sys模块"),
        (r"subprocess\.", "禁止使用subprocess模块"),
        (r"__builtins__\s*\[", "禁止访问__builtins__"),
    ]

    # 危险模式（心语代码层面）
    DANGEROUS_XINYU_PATTERNS = [
        (r"导入\s+os", "禁止导入os模块"),
        (r"导入\s+sys", "禁止导入sys模块"),
        (r"导入\s+subprocess", "禁止导入subprocess模块"),
    ]

    @classmethod
    def validate(cls, source: str, strict: bool = True) -> ValidationResult:
        """验证源代码

        Args:
            source: 源代码字符串
            strict: 是否启用严格模式

        Returns:
            ValidationResult对象
        """
        errors = []
        warnings = []

        # 1. 基础验证
        base_result = cls._validate_base(source)
        errors.extend(base_result[0])
        warnings.extend(base_result[1])

        # 2. 编码验证
        encoding_result = cls._validate_encoding(source)
        errors.extend(encoding_result[0])
        warnings.extend(encoding_result[1])

        # 3. 安全模式验证
        security_result = cls._validate_security(source)
        errors.extend(security_result[0])
        warnings.extend(security_result[1])

        # 4. 结构验证（严格模式）
        if strict:
            structure_result = cls._validate_structure(source)
            errors.extend(structure_result[0])
            warnings.extend(structure_result[1])

        is_valid = len(errors) == 0
        return ValidationResult(is_valid, errors, warnings)

    @classmethod
    def _validate_base(cls, source: str) -> Tuple[List[str], List[str]]:
        """基础验证"""
        errors = []
        warnings = []

        # 检查是否为空
        if not source or not source.strip():
            errors.append("源代码为空")
            return errors, warnings

        # 检查长度限制
        if len(source) > cls.MAX_SOURCE_LENGTH:
            errors.append(f"源代码过长（当前{len(source)}字节，最大{cls.MAX_SOURCE_LENGTH}字节）")

        # 检查单行长度
        lines = source.split("\n")
        for i, line in enumerate(lines, 1):
            if len(line) > cls.MAX_LINE_LENGTH:
                warnings.append(f"第{i}行过长（{len(line)}字符），可能影响可读性")

        return errors, warnings

    @classmethod
    def _validate_encoding(cls, source: str) -> Tuple[List[str], List[str]]:
        """编码验证"""
        errors = []
        warnings = []

        try:
            # 尝试UTF-8编码
            encoded = source.encode("utf-8")

            # 检查是否有BOM标记
            if encoded.startswith(b"\xef\xbb\xbf"):
                warnings.append("源代码包含UTF-8 BOM标记，建议移除")

        except UnicodeEncodeError as e:
            errors.append(f"编码错误: {e}")

        return errors, warnings

    @classmethod
    def _validate_security(cls, source: str) -> Tuple[List[str], List[str]]:
        """安全模式验证"""
        errors = []
        warnings = []

        # 检查Python层面的危险模式
        for pattern, message in cls.DANGEROUS_PYTHON_PATTERNS:
            if re.search(pattern, source):
                errors.append(f"安全风险: {message}")

        # 检查心语层面的危险模式
        for pattern, message in cls.DANGEROUS_XINYU_PATTERNS:
            if re.search(pattern, source):
                errors.append(f"安全风险: {message}")

        return errors, warnings

    @classmethod
    def _validate_structure(cls, source: str) -> Tuple[List[str], List[str]]:
        """结构验证"""
        errors = []
        warnings = []

        # 检查括号匹配
        brackets = {"(": ")", "[": "]", "{": "}"}
        stack = []
        for i, char in enumerate(source):
            if char in brackets:
                stack.append((char, i))
            elif char in brackets.values():
                if not stack:
                    errors.append(f"位置{i}处括号不匹配")
                else:
                    open_char, open_pos = stack.pop()
                    if brackets[open_char] != char:
                        errors.append(f"位置{open_pos}和{i}处括号不匹配")

        if stack:
            for char, pos in stack:
                warnings.append(f"位置{pos}处括号未闭合")

        # 检查嵌套深度
        max_depth = 0
        current_depth = 0
        for char in source:
            if char in brackets:
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char in brackets.values():
                current_depth -= 1

        if max_depth > cls.MAX_NESTING_DEPTH:
            warnings.append(f"嵌套深度过深（{max_depth}层），可能影响性能")

        return errors, warnings


class InputSanitizer:
    """输入清理器

    清理和规范化用户输入。
    """

    @classmethod
    def sanitize(cls, source: str) -> str:
        """清理源代码

        Args:
            source: 原始源代码

        Returns:
            清理后的源代码
        """
        # 移除BOM标记
        if source.startswith("\ufeff"):
            source = source[1:]

        # 规范化换行符
        source = source.replace("\r\n", "\n").replace("\r", "\n")

        # 移除尾部空白
        lines = source.split("\n")
        lines = [line.rstrip() for line in lines]
        source = "\n".join(lines)

        # 移除多余的空行（保留最多2个连续空行）
        while "\n\n\n" in source:
            source = source.replace("\n\n\n", "\n\n")

        return source.strip()


# 便捷函数
def validate_source(source: str, strict: bool = True) -> ValidationResult:
    """验证源代码

    Args:
        source: 源代码字符串
        strict: 是否启用严格模式

    Returns:
        ValidationResult对象
    """
    return SourceCodeValidator.validate(source, strict)


def sanitize_source(source: str) -> str:
    """清理源代码

    Args:
        source: 原始源代码

    Returns:
        清理后的源代码
    """
    return InputSanitizer.sanitize(source)
