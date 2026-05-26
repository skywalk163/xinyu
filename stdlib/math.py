# -*- coding: utf-8 -*-
"""心语语言数学模块

提供数学运算函数。
"""

import math as _math
from typing import Union, List

Number = Union[int, float]


def 绝对值(x: Number) -> Number:
    """计算绝对值
    
    Args:
        x: 数值
        
    Returns:
        绝对值
        
    Example:
        绝对值(-5)  # 返回 5
    """
    return abs(x)


def 最大值(*args: Number) -> Number:
    """返回最大值
    
    Args:
        *args: 数值列表
        
    Returns:
        最大值
        
    Example:
        最大值(1, 2, 3)  # 返回 3
    """
    return max(args)


def 最小值(*args: Number) -> Number:
    """返回最小值
    
    Args:
        *args: 数值列表
        
    Returns:
        最小值
        
    Example:
        最小值(1, 2, 3)  # 返回 1
    """
    return min(args)


def 平方根(x: Number) -> float:
    """计算平方根
    
    Args:
        x: 数值（必须非负）
        
    Returns:
        平方根
        
    Raises:
        ValueError: 如果x为负数
        
    Example:
        平方根(16)  # 返回 4.0
    """
    return _math.sqrt(x)


def 幂(x: Number, y: Number) -> Number:
    """计算x的y次幂
    
    Args:
        x: 底数
        y: 指数
        
    Returns:
        x的y次幂
        
    Example:
        幂(2, 3)  # 返回 8
    """
    return _math.pow(x, y)


def 对数(x: Number, base: Number = _math.e) -> float:
    """计算对数
    
    Args:
        x: 数值（必须为正）
        base: 底数（默认为e）
        
    Returns:
        对数值
        
    Raises:
        ValueError: 如果x或base不合法
        
    Example:
        对数(10, 10)  # 返回 1.0
    """
    return _math.log(x, base)


def 正弦(x: Number) -> float:
    """计算正弦值
    
    Args:
        x: 弧度值
        
    Returns:
        正弦值
        
    Example:
        正弦(0)  # 返回 0.0
    """
    return _math.sin(x)


def 余弦(x: Number) -> float:
    """计算余弦值
    
    Args:
        x: 弧度值
        
    Returns:
        余弦值
        
    Example:
        余弦(0)  # 返回 1.0
    """
    return _math.cos(x)


def 正切(x: Number) -> float:
    """计算正切值
    
    Args:
        x: 弧度值
        
    Returns:
        正切值
        
    Example:
        正切(0)  # 返回 0.0
    """
    return _math.tan(x)


def 向下取整(x: Number) -> int:
    """向下取整
    
    Args:
        x: 数值
        
    Returns:
        不大于x的最大整数
        
    Example:
        向下取整(3.7)  # 返回 3
    """
    return _math.floor(x)


def 向上取整(x: Number) -> int:
    """向上取整
    
    Args:
        x: 数值
        
    Returns:
        不小于x的最小整数
        
    Example:
        向上取整(3.2)  # 返回 4
    """
    return _math.ceil(x)


def 四舍五入(x: Number, n: int = 0) -> Number:
    """四舍五入
    
    Args:
        x: 数值
        n: 保留小数位数（默认为0）
        
    Returns:
        四舍五入后的值
        
    Example:
        四舍五入(3.14159, 2)  # 返回 3.14
    """
    return round(x, n)


def 弧度转角度(x: Number) -> float:
    """弧度转角度
    
    Args:
        x: 弧度值
        
    Returns:
        角度值
        
    Example:
        弧度转角度(π)  # 返回 180.0
    """
    return _math.degrees(x)


def 角度转弧度(x: Number) -> float:
    """角度转弧度
    
    Args:
        x: 角度值
        
    Returns:
        弧度值
        
    Example:
        角度转弧度(180)  # 返回 π
    """
    return _math.radians(x)


# 常量
π = _math.pi
e = _math.e
无穷 = _math.inf
非数 = _math.nan


# 导出所有函数和常量
__all__ = [
    '绝对值', '最大值', '最小值', '平方根', '幂', '对数',
    '正弦', '余弦', '正切', '向下取整', '向上取整', '四舍五入',
    '弧度转角度', '角度转弧度',
    'π', 'e', '无穷', '非数',
]
