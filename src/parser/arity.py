"""元数定义模块

元数（Arity）表示函数或动词的参数数量。

支持四种元数类型：
1. 固定元数（Fixed）：必须有固定数量的参数
2. 可变元数（Variable）：可以有任意数量的参数（最少min个）
3. 最小元数（Minimum）：最少需要min个参数，可以更多
4. 范围元数（Range）：参数数量在[min, max]范围内
"""

from enum import Enum
from typing import Optional


class ArityType(Enum):
    """元数类型"""

    FIXED = "fixed"  # 固定数量
    VARIABLE = "variable"  # 可变数量
    MINIMUM = "minimum"  # 最小数量
    RANGE = "range"  # 范围数量


class Arity:
    """元数定义

    表示函数或动词的参数数量要求。

    示例：
        # 固定元数：相加 a b（必须2个参数）
        Arity.fixed(2)

        # 可变元数：打印 "你好" "世界" "！"（任意数量参数）
        Arity.variable(min=0)

        # 最小元数：求和 1 2 3 4 5（最少1个参数）
        Arity.min(1)

        # 范围元数：读取文件 文件名 编码？（1-2个参数）
        Arity.range(min=1, max=2)
    """

    def __init__(
        self,
        type: ArityType,
        count: Optional[int] = None,
        min_count: Optional[int] = None,
        max_count: Optional[int] = None,
    ):
        """初始化元数

        Args:
            type: 元数类型
            count: 固定数量（仅用于FIXED类型）
            min_count: 最小数量（用于VARIABLE、MINIMUM、RANGE类型）
            max_count: 最大数量（仅用于RANGE类型）
        """
        self.type = type
        self.count = count
        self.min_count = min_count
        self.max_count = max_count

    @classmethod
    def fixed(cls, count: int) -> "Arity":
        """固定元数

        必须有固定数量的参数。

        Args:
            count: 参数数量

        Returns:
            固定元数实例

        示例：
            Arity.fixed(2)  # 必须有2个参数
        """
        return cls(ArityType.FIXED, count=count)

    @classmethod
    def variable(cls, min: int = 0) -> "Arity":
        """可变元数

        可以有任意数量的参数（最少min个）。

        Args:
            min: 最小参数数量，默认为0

        Returns:
            可变元数实例

        示例：
            Arity.variable(min=0)  # 可以有任意数量参数
            Arity.variable(min=1)  # 最少1个参数，可以更多
        """
        return cls(ArityType.VARIABLE, min_count=min)

    @classmethod
    def min(cls, min_count: int) -> "Arity":
        """最小元数

        最少需要min_count个参数，可以更多。

        Args:
            min_count: 最小参数数量

        Returns:
            最小元数实例

        示例：
            Arity.min(2)  # 最少2个参数，可以更多
        """
        return cls(ArityType.MINIMUM, min_count=min_count)

    @classmethod
    def range(cls, min: int, max: int) -> "Arity":
        """范围元数

        参数数量必须在[min, max]范围内。

        Args:
            min: 最小参数数量
            max: 最大参数数量

        Returns:
            范围元数实例

        示例：
            Arity.range(min=1, max=3)  # 1-3个参数
        """
        return cls(ArityType.RANGE, min_count=min, max_count=max)

    def is_satisfied(self, arg_count: int) -> bool:
        """检查参数数量是否满足要求

        Args:
            arg_count: 实际参数数量

        Returns:
            是否满足要求
        """
        if self.type == ArityType.FIXED:
            return arg_count == self.count
        elif self.type == ArityType.VARIABLE:
            return arg_count >= self.min_count
        elif self.type == ArityType.MINIMUM:
            return arg_count >= self.min_count
        elif self.type == ArityType.RANGE:
            return self.min_count <= arg_count <= self.max_count
        return False

    def should_stop_collecting(self, arg_count: int) -> bool:
        """是否应该停止收集参数

        Args:
            arg_count: 当前已收集的参数数量

        Returns:
            是否应该停止收集

        注意：
            - FIXED类型：收集到足够数量后停止
            - RANGE类型：收集到最大数量后停止
            - VARIABLE和MINIMUM类型：不主动停止（需要外部判断）
        """
        if self.type == ArityType.FIXED:
            return arg_count >= self.count
        elif self.type == ArityType.RANGE:
            return arg_count >= self.max_count
        # VARIABLE 和 MINIMUM 类型不主动停止
        return False

    def __str__(self) -> str:
        """字符串表示"""
        if self.type == ArityType.FIXED:
            return f"固定{self.count}个参数"
        elif self.type == ArityType.VARIABLE:
            return f"可变参数（最少{self.min_count}个）"
        elif self.type == ArityType.MINIMUM:
            return f"最少{self.min_count}个参数"
        elif self.type == ArityType.RANGE:
            return f"{self.min_count}-{self.max_count}个参数"
        return "未知元数类型"

    def __repr__(self) -> str:
        """详细表示"""
        if self.type == ArityType.FIXED:
            return f"Arity.fixed({self.count})"
        elif self.type == ArityType.VARIABLE:
            return f"Arity.variable(min={self.min_count})"
        elif self.type == ArityType.MINIMUM:
            return f"Arity.min({self.min_count})"
        elif self.type == ArityType.RANGE:
            return f"Arity.range(min={self.min_count}, max={self.max_count})"
        return f"Arity({self.type})"
