"""
threading模块中文封装（多线程）
"""

import threading

from .base_wrapper import ChineseModuleWrapper


class ThreadingWrapper(ChineseModuleWrapper):
    """threading模块中文封装"""

    NAME_MAP = {
        "线程": "Thread",
        "锁": "Lock",
        "递归锁": "RLock",
        "条件变量": "Condition",
        "信号量": "Semaphore",
        "事件": "Event",
        "定时器": "Timer",
        "屏障": "Barrier",
        "当前线程": "current_thread",
        "活跃线程数": "active_count",
        "枚举线程": "enumerate",
        "主线程": "main_thread",
    }

    def __init__(self):
        super().__init__(module=threading, name_map=self.NAME_MAP)
