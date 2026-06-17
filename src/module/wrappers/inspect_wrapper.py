"""
inspect模块中文封装（检查对象）
"""

import inspect

from .base_wrapper import ChineseModuleWrapper


class InspectWrapper(ChineseModuleWrapper):
    """inspect模块中文封装"""

    NAME_MAP = {
        "获取模块": "getmodule",
        "获取源代码": "getsource",
        "获取源文件": "getsourcefile",
        "获取参数": "signature",
        "获取成员": "getmembers",
        "是模块": "ismodule",
        "是类": "isclass",
        "是方法": "ismethod",
        "是函数": "isfunction",
        "栈": "stack",
    }

    def __init__(self):
        super().__init__(module=inspect, name_map=self.NAME_MAP)
