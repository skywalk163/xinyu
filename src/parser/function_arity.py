# -*- coding: utf-8 -*-
"""函数元数表

定义每个函数的参数数量（元数），用于元数驱动解析。
学习newlisp/yan的设计思想。

元数（Arity）：
- 函数的参数数量
- 用于无空格分词和参数解析
- 支持固定元数和可变元数
"""

from enum import Enum
from typing import Dict, Optional, Union


class ArityType(Enum):
    """元数类型"""

    FIXED = "fixed"  # 固定元数
    VARIABLE = "variable"  # 可变元数
    UNKNOWN = "unknown"  # 未知元数


class FunctionArity:
    """函数元数信息"""

    def __init__(
        self,
        name: str,
        arity_type: ArityType = ArityType.FIXED,
        min_args: int = 0,
        max_args: Optional[int] = None,
        description: str = "",
    ):
        """初始化函数元数

        Args:
            name: 函数名
            arity_type: 元数类型
            min_args: 最小参数数量
            max_args: 最大参数数量（None表示无限）
            description: 描述
        """
        self.name = name
        self.arity_type = arity_type
        self.min_args = min_args
        self.max_args = max_args
        self.description = description

    @property
    def arity(self) -> Union[int, str]:
        """获取元数

        Returns:
            元数（固定）或 "可变" 或 "未知"
        """
        if self.arity_type == ArityType.FIXED:
            return self.min_args
        elif self.arity_type == ArityType.VARIABLE:
            return "可变"
        else:
            return "未知"

    def __repr__(self):
        return f"FunctionArity({self.name}, {self.arity})"


# 函数元数表
FUNCTION_ARITY_TABLE: Dict[str, FunctionArity] = {
    # ===== 内置函数 =====
    # 输入输出
    "打印": FunctionArity("打印", ArityType.VARIABLE, 0, None, "打印任意数量参数"),
    "输入": FunctionArity("输入", ArityType.FIXED, 0, 0, "从控制台输入"),
    "输出": FunctionArity("输出", ArityType.VARIABLE, 0, None, "输出任意数量参数"),
    "写入": FunctionArity("写入", ArityType.VARIABLE, 0, None, "写入任意数量参数"),
    "读取": FunctionArity("读取", ArityType.FIXED, 0, 0, "读取"),
    # 类型转换
    "整数": FunctionArity("整数", ArityType.FIXED, 1, 1, "转换为整数"),
    "浮点": FunctionArity("浮点", ArityType.FIXED, 1, 1, "转换为浮点数"),
    "字符串": FunctionArity("字符串", ArityType.FIXED, 1, 1, "转换为字符串"),
    "列表": FunctionArity("列表", ArityType.FIXED, 1, 1, "转换为列表"),
    "字典": FunctionArity("字典", ArityType.FIXED, 1, 1, "转换为字典"),
    "类型": FunctionArity("类型", ArityType.FIXED, 1, 1, "获取类型"),
    # 数学函数
    "绝对值": FunctionArity("绝对值", ArityType.FIXED, 1, 1, "绝对值"),
    "最大值": FunctionArity("最大值", ArityType.VARIABLE, 1, None, "最大值"),
    "最小值": FunctionArity("最小值", ArityType.VARIABLE, 1, None, "最小值"),
    "求和": FunctionArity("求和", ArityType.FIXED, 1, 1, "求和"),
    "平方根": FunctionArity("平方根", ArityType.FIXED, 1, 1, "平方根"),
    "幂": FunctionArity("幂", ArityType.FIXED, 2, 2, "幂运算"),
    # 序列函数
    "长度": FunctionArity("长度", ArityType.FIXED, 1, 1, "长度"),
    "范围": FunctionArity("范围", ArityType.VARIABLE, 1, 3, "范围"),
    "排序": FunctionArity("排序", ArityType.FIXED, 1, 1, "排序"),
    "反转": FunctionArity("反转", ArityType.FIXED, 1, 1, "反转"),
    # ===== 高阶函数（待实现）=====
    "皆": FunctionArity("皆", ArityType.FIXED, 2, 2, "map - 映射"),
    "只": FunctionArity("只", ArityType.FIXED, 2, 2, "filter - 筛选"),
    "归": FunctionArity("归", ArityType.FIXED, 3, 3, "reduce - 归约"),
    # ===== 操作符（作为函数）=====
    "相加": FunctionArity("相加", ArityType.FIXED, 2, 2, "加法"),
    "相减": FunctionArity("相减", ArityType.FIXED, 2, 2, "减法"),
    "相乘": FunctionArity("相乘", ArityType.FIXED, 2, 2, "乘法"),
    "相除": FunctionArity("相除", ArityType.FIXED, 2, 2, "除法"),
    "取余": FunctionArity("取余", ArityType.FIXED, 2, 2, "取余"),
    "等于": FunctionArity("等于", ArityType.FIXED, 2, 2, "等于"),
    "不等": FunctionArity("不等", ArityType.FIXED, 2, 2, "不等于"),
    "大于": FunctionArity("大于", ArityType.FIXED, 2, 2, "大于"),
    "小于": FunctionArity("小于", ArityType.FIXED, 2, 2, "小于"),
    "大等": FunctionArity("大等", ArityType.FIXED, 2, 2, "大于等于"),
    "小等": FunctionArity("小等", ArityType.FIXED, 2, 2, "小于等于"),
    "并且": FunctionArity("并且", ArityType.FIXED, 2, 2, "逻辑与"),
    "或者": FunctionArity("或者", ArityType.FIXED, 2, 2, "逻辑或"),
    "非也": FunctionArity("非也", ArityType.FIXED, 1, 1, "逻辑非"),
}


def get_arity(func_name: str) -> Optional[FunctionArity]:
    """获取函数的元数信息

    Args:
        func_name: 函数名

    Returns:
        FunctionArity对象，如果函数不在表中则返回None
    """
    return FUNCTION_ARITY_TABLE.get(func_name)


def is_fixed_arity(func_name: str) -> bool:
    """检查函数是否是固定元数

    Args:
        func_name: 函数名

    Returns:
        是否是固定元数
    """
    arity = get_arity(func_name)
    return arity is not None and arity.arity_type == ArityType.FIXED


def get_expected_args(func_name: str) -> Optional[int]:
    """获取函数期望的参数数量

    Args:
        func_name: 函数名

    Returns:
        期望的参数数量，如果是可变参数或未知则返回None
    """
    arity = get_arity(func_name)
    if arity and arity.arity_type == ArityType.FIXED:
        return arity.min_args
    return None


def register_function(
    name: str,
    arity_type: ArityType = ArityType.FIXED,
    min_args: int = 0,
    max_args: Optional[int] = None,
    description: str = "",
):
    """注册函数到元数表

    Args:
        name: 函数名
        arity_type: 元数类型
        min_args: 最小参数数量
        max_args: 最大参数数量
        description: 描述
    """
    FUNCTION_ARITY_TABLE[name] = FunctionArity(name, arity_type, min_args, max_args, description)


# 使用示例
if __name__ == "__main__":
    print("=== 函数元数表 ===\n")

    for name, arity in sorted(FUNCTION_ARITY_TABLE.items()):
        print(f"{name}: {arity.arity} - {arity.description}")

    print("\n=== 查询示例 ===\n")

    # 查询函数元数
    print(f"打印: {get_arity('打印')}")
    print(f"相加: {get_arity('相加')}")
    print(f"范围: {get_arity('范围')}")

    # 检查是否是固定元数
    print(f"\n相加是固定元数: {is_fixed_arity('相加')}")
    print(f"打印是固定元数: {is_fixed_arity('打印')}")

    # 获取期望参数数量
    print(f"\n相加期望参数: {get_expected_args('相加')}")
    print(f"打印期望参数: {get_expected_args('打印')}")
