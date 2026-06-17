"""
asyncio模块中文封装（异步IO）
"""

import asyncio

from .base_wrapper import ChineseModuleWrapper


class AsyncioWrapper(ChineseModuleWrapper):
    """asyncio模块中文封装"""

    NAME_MAP = {
        "运行": "run",
        "创建任务": "create_task",
        "等待": "wait",
        "等待全部": "gather",
        "睡眠": "sleep",
        "事件循环": "get_event_loop",
        "新事件循环": "new_event_loop",
        "当前任务": "current_task",
        "所有任务": "all_tasks",
        "队列": "Queue",
        "锁": "Lock",
        "事件": "Event",
        "条件": "Condition",
        "信号量": "Semaphore",
    }

    def __init__(self):
        super().__init__(module=asyncio, name_map=self.NAME_MAP)
