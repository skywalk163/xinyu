"""
math模块中文封装
"""

import math

from .base_wrapper import ChineseModuleWrapper


class MathWrapper(ChineseModuleWrapper):
    """math模块中文封装"""

    NAME_MAP = {
        "圆周率": "pi",
        "自然常数": "e",
        "平方根": "sqrt",
        "正弦": "sin",
        "余弦": "cos",
        "正切": "tan",
        "绝对值": "fabs",
        "对数": "log",
        "自然对数": "log",
        "常用对数": "log10",
        "指数": "exp",
        "向上取整": "ceil",
        "向下取整": "floor",
        "幂运算": "pow",
        "弧度转角度": "degrees",
        "角度转弧度": "radians",
    }

    def __init__(self):
        super().__init__(module=math, name_map=self.NAME_MAP)
