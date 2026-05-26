# -*- coding: utf-8 -*-
"""心语语言列表模块

提供列表处理函数。
"""

from typing import List, Any, Callable, Optional


def 长度(lst: List) -> int:
    """计算列表长度
    
    Args:
        lst: 列表
        
    Returns:
        列表长度
        
    Example:
        长度([1, 2, 3])  # 返回 3
    """
    return len(lst)


def 添加(lst: List, item: Any) -> List:
    """添加元素到末尾
    
    Args:
        lst: 列表
        item: 要添加的元素
        
    Returns:
        新列表（不修改原列表）
        
    Example:
        添加([1, 2], 3)  # 返回 [1, 2, 3]
    """
    return lst + [item]


def 扩展(lst: List, items: List) -> List:
    """扩展列表
    
    Args:
        lst: 列表
        items: 要添加的元素列表
        
    Returns:
        新列表（不修改原列表）
        
    Example:
        扩展([1, 2], [3, 4])  # 返回 [1, 2, 3, 4]
    """
    return lst + items


def 插入(lst: List, index: int, item: Any) -> List:
    """在指定位置插入元素
    
    Args:
        lst: 列表
        index: 插入位置
        item: 要插入的元素
        
    Returns:
        新列表（不修改原列表）
        
    Example:
        插入([1, 2, 3], 1, 5)  # 返回 [1, 5, 2, 3]
    """
    result = lst.copy()
    result.insert(index, item)
    return result


def 移除(lst: List, item: Any) -> List:
    """移除第一个匹配元素
    
    Args:
        lst: 列表
        item: 要移除的元素
        
    Returns:
        新列表（不修改原列表）
        
    Raises:
        ValueError: 如果元素不存在
        
    Example:
        移除([1, 2, 3, 2], 2)  # 返回 [1, 3, 2]
    """
    result = lst.copy()
    result.remove(item)
    return result


def 弹出(lst: List, index: int = -1) -> Any:
    """弹出指定位置元素
    
    Args:
        lst: 列表
        index: 弹出位置（默认为末尾）
        
    Returns:
        弹出的元素
        
    Raises:
        IndexError: 如果索引越界
        
    Example:
        弹出([1, 2, 3])  # 返回 3
    """
    result = lst.copy()
    return result.pop(index)


def 排序(lst: List, reverse: bool = False) -> List:
    """排序列表
    
    Args:
        lst: 列表
        reverse: 是否降序（默认升序）
        
    Returns:
        排序后的新列表（不修改原列表）
        
    Example:
        排序([3, 1, 2])  # 返回 [1, 2, 3]
    """
    return sorted(lst, reverse=reverse)


def 反转(lst: List) -> List:
    """反转列表
    
    Args:
        lst: 列表
        
    Returns:
        反转后的新列表（不修改原列表）
        
    Example:
        反转([1, 2, 3])  # 返回 [3, 2, 1]
    """
    return lst[::-1]


def 索引(lst: List, item: Any, start: int = 0, end: int = None) -> int:
    """查找元素索引
    
    Args:
        lst: 列表
        item: 要查找的元素
        start: 起始位置
        end: 结束位置
        
    Returns:
        元素索引
        
    Raises:
        ValueError: 如果元素不存在
        
    Example:
        索引([1, 2, 3], 2)  # 返回 1
    """
    if end is None:
        return lst.index(item, start)
    return lst.index(item, start, end)


def 计数(lst: List, item: Any) -> int:
    """计算元素出现次数
    
    Args:
        lst: 列表
        item: 要计数的元素
        
    Returns:
        出现次数
        
    Example:
        计数([1, 2, 2, 3], 2)  # 返回 2
    """
    return lst.count(item)


def 包含(lst: List, item: Any) -> bool:
    """检查是否包含元素
    
    Args:
        lst: 列表
        item: 要检查的元素
        
    Returns:
        是否包含item
        
    Example:
        包含([1, 2, 3], 2)  # 返回 True
    """
    return item in lst


def 切片(lst: List, start: int = 0, end: int = None, step: int = 1) -> List:
    """切片列表
    
    Args:
        lst: 列表
        start: 起始位置
        end: 结束位置
        step: 步长
        
    Returns:
        切片后的列表
        
    Example:
        切片([1, 2, 3, 4, 5], 1, 4)  # 返回 [2, 3, 4]
    """
    if end is None:
        return lst[start::step]
    return lst[start:end:step]


def 连接(lst: List, sep: str = "") -> str:
    """连接列表元素为字符串
    
    Args:
        lst: 列表
        sep: 分隔符
        
    Returns:
        连接后的字符串
        
    Example:
        连接([1, 2, 3], ",")  # 返回 "1,2,3"
    """
    return sep.join(str(item) for item in lst)


def 求和(lst: List) -> Any:
    """求和
    
    Args:
        lst: 数值列表
        
    Returns:
        和
        
    Example:
        求和([1, 2, 3])  # 返回 6
    """
    return sum(lst)


def 最大值(lst: List) -> Any:
    """返回最大值
    
    Args:
        lst: 列表
        
    Returns:
        最大值
        
    Example:
        最大值([1, 2, 3])  # 返回 3
    """
    return max(lst)


def 最小值(lst: List) -> Any:
    """返回最小值
    
    Args:
        lst: 列表
        
    Returns:
        最小值
        
    Example:
        最小值([1, 2, 3])  # 返回 1
    """
    return min(lst)


def 去重(lst: List) -> List:
    """去重
    
    Args:
        lst: 列表
        
    Returns:
        去重后的列表
        
    Example:
        去重([1, 2, 2, 3])  # 返回 [1, 2, 3]
    """
    return list(dict.fromkeys(lst))


# 导出所有函数
__all__ = [
    '长度', '添加', '扩展', '插入', '移除', '弹出', '排序', '反转',
    '索引', '计数', '包含', '切片', '连接', '求和', '最大值', '最小值', '去重',
]
