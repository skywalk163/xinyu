"""
time模块中文封装（时间访问）
"""

import time

from .base_wrapper import ChineseModuleWrapper


class TimeWrapper(ChineseModuleWrapper):
    """time模块中文封装"""

    NAME_MAP = {
        "当前时间": "time",
        "时间戳转时间": "ctime",
        "格式化时间": "strftime",
        "解析时间": "strptime",
        "睡眠": "sleep",
        "本地时间": "localtime",
        "格林威治时间": "gmtime",
    }

    def __init__(self):
        super().__init__(module=time, name_map=self.NAME_MAP)
