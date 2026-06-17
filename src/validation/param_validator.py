"""
参数验证器

验证函数参数的类型和数量。
"""

from dataclasses import dataclass
from typing import Any, List, Optional, Tuple


@dataclass
class ValidationResult:
    """验证结果"""

    is_valid: bool
    error_message: Optional[str] = None


class ParamValidator:
    """参数验证器"""

    def validate(self, func_info: Any, args: Tuple, kwargs: dict) -> ValidationResult:
        """验证参数"""
        # 占位实现，将在任务3中完善
        return ValidationResult(is_valid=True)

    def check_count(self, args: Tuple, min_args: int, max_args: int) -> ValidationResult:
        """检查参数数量"""
        count = len(args)
        if count < min_args:
            return ValidationResult(
                is_valid=False, error_message=f"参数数量不足：需要至少{min_args}个参数，但只提供了{count}个"
            )
        if max_args is not None and count > max_args:
            return ValidationResult(
                is_valid=False, error_message=f"参数数量过多：最多接受{max_args}个参数，但提供了{count}个"
            )
        return ValidationResult(is_valid=True)

    def check_type(self, value: Any, expected_type: type) -> ValidationResult:
        """检查参数类型"""
        if not isinstance(value, expected_type):
            return ValidationResult(
                is_valid=False,
                error_message=f"参数类型错误：期望{expected_type.__name__}，实际{type(value).__name__}",
            )
        return ValidationResult(is_valid=True)
