# -*- coding: utf-8 -*-
"""心语语言字符串模块

提供字符串处理函数。
"""

from typing import List, Union


def 长度(s: str) -> int:
    """计算字符串长度

    Args:
        s: 字符串

    Returns:
        字符串长度

    Example:
        长度("你好")  # 返回 2
    """
    return len(s)


def 大写(s: str) -> str:
    """转换为大写

    Args:
        s: 字符串

    Returns:
        大写字符串

    Example:
        大写("hello")  # 返回 "HELLO"
    """
    return s.upper()


def 小写(s: str) -> str:
    """转换为小写

    Args:
        s: 字符串

    Returns:
        小写字符串

    Example:
        小写("HELLO")  # 返回 "hello"
    """
    return s.lower()


def 去空白(s: str) -> str:
    """去除首尾空白

    Args:
        s: 字符串

    Returns:
        去除空白后的字符串

    Example:
        去空白("  hello  ")  # 返回 "hello"
    """
    return s.strip()


def 分割(s: str, sep: str = None) -> List[str]:
    """分割字符串

    Args:
        s: 字符串
        sep: 分隔符（默认为空白）

    Returns:
        分割后的字符串列表

    Example:
        分割("a,b,c", ",")  # 返回 ["a", "b", "c"]
    """
    return s.split(sep)


def 连接(lst: List[str], sep: str = "") -> str:
    """连接字符串列表

    Args:
        lst: 字符串列表
        sep: 分隔符（默认为空）

    Returns:
        连接后的字符串

    Example:
        连接(["a", "b", "c"], ",")  # 返回 "a,b,c"
    """
    return sep.join(lst)


def 替换(s: str, old: str, new: str, count: int = -1) -> str:
    """替换子字符串

    Args:
        s: 原字符串
        old: 要替换的子字符串
        new: 新子字符串
        count: 替换次数（默认全部）

    Returns:
        替换后的字符串

    Example:
        替换("hello world", "world", "心语")  # 返回 "hello 心语"
    """
    return s.replace(old, new, count)


def 查找(s: str, sub: str, start: int = 0, end: int = None) -> int:
    """查找子字符串位置

    Args:
        s: 原字符串
        sub: 子字符串
        start: 起始位置
        end: 结束位置

    Returns:
        子字符串位置，未找到返回-1

    Example:
        查找("hello", "ll")  # 返回 2
    """
    return s.find(sub, start, end)


def 计数(s: str, sub: str, start: int = 0, end: int = None) -> int:
    """计算子字符串出现次数

    Args:
        s: 原字符串
        sub: 子字符串
        start: 起始位置
        end: 结束位置

    Returns:
        出现次数

    Example:
        计数("hello", "l")  # 返回 2
    """
    return s.count(sub, start, end)


def 开头为(s: str, prefix: str) -> bool:
    """检查是否以指定字符串开头

    Args:
        s: 原字符串
        prefix: 前缀

    Returns:
        是否以prefix开头

    Example:
        开头为("hello", "he")  # 返回 True
    """
    return s.startswith(prefix)


def 结尾为(s: str, suffix: str) -> bool:
    """检查是否以指定字符串结尾

    Args:
        s: 原字符串
        suffix: 后缀

    Returns:
        是否以suffix结尾

    Example:
        结尾为("hello", "lo")  # 返回 True
    """
    return s.endswith(suffix)


def 包含(s: str, sub: str) -> bool:
    """检查是否包含子字符串

    Args:
        s: 原字符串
        sub: 子字符串

    Returns:
        是否包含sub

    Example:
        包含("hello", "ell")  # 返回 True
    """
    return sub in s


def 重复(s: str, n: int) -> str:
    """重复字符串

    Args:
        s: 原字符串
        n: 重复次数

    Returns:
        重复后的字符串

    Example:
        重复("ab", 3)  # 返回 "ababab"
    """
    return s * n


def 首字母大写(s: str) -> str:
    """首字母大写

    Args:
        s: 原字符串

    Returns:
        首字母大写的字符串

    Example:
        首字母大写("hello")  # 返回 "Hello"
    """
    return s.capitalize()


def 标题格式(s: str) -> str:
    """转换为标题格式（每个单词首字母大写）

    Args:
        s: 原字符串

    Returns:
        标题格式的字符串

    Example:
        标题格式("hello world")  # 返回 "Hello World"
    """
    return s.title()


def 是否数字(s: str) -> bool:
    """检查是否为数字

    Args:
        s: 字符串

    Returns:
        是否为数字

    Example:
        是否数字("123")  # 返回 True
    """
    return s.isdigit()


def 是否字母(s: str) -> bool:
    """检查是否为字母

    Args:
        s: 字符串

    Returns:
        是否为字母

    Example:
        是否字母("abc")  # 返回 True
    """
    return s.isalpha()


def 是否空白(s: str) -> bool:
    """检查是否为空白

    Args:
        s: 字符串

    Returns:
        是否为空白

    Example:
        是否空白("   ")  # 返回 True
    """
    return s.isspace()


# 导出所有函数
__all__ = [
    "长度",
    "大写",
    "小写",
    "去空白",
    "分割",
    "连接",
    "替换",
    "查找",
    "计数",
    "开头为",
    "结尾为",
    "包含",
    "重复",
    "首字母大写",
    "标题格式",
    "是否数字",
    "是否字母",
    "是否空白",
]
