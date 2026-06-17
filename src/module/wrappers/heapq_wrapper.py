"""
heapq模块中文封装（堆队列）
"""

import heapq

from .base_wrapper import ChineseModuleWrapper


class HeapqWrapper(ChineseModuleWrapper):
    """heapq模块中文封装"""

    NAME_MAP = {
        "堆化": "heapify",
        "推入": "heappush",
        "弹出": "heappop",
        "推入弹出": "heappushpop",
        "替换": "heapreplace",
        "最大n个": "nlargest",
        "最小n个": "nsmallest",
        "合并": "merge",
    }

    def __init__(self):
        super().__init__(module=heapq, name_map=self.NAME_MAP)
