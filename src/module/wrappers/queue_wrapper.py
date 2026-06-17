"""
queue模块中文封装（队列）
"""

import queue

from .base_wrapper import ChineseModuleWrapper


class QueueWrapper(ChineseModuleWrapper):
    """queue模块中文封装"""

    NAME_MAP = {
        "队列": "Queue",
        "优先队列": "PriorityQueue",
        "生命队列": "LifoQueue",
        "简单队列": "SimpleQueue",
    }

    def __init__(self):
        super().__init__(module=queue, name_map=self.NAME_MAP)
