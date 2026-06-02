"""
类型推断

推断值的类型信息。
"""

from typing import Any


class TypeInference:
    """类型推断器"""
    
    def infer(self, value: Any) -> type:
        """推断值的类型"""
        return type(value)
