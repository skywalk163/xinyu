"""
datetime模块中文封装
"""

import datetime
from .base_wrapper import ChineseModuleWrapper


class DatetimeWrapper(ChineseModuleWrapper):
    """datetime模块中文封装"""
    
    NAME_MAP = {
        '当前时间': 'datetime.now',
        '今天': 'date.today',
        '日期': 'date',
        '时间': 'time',
        '时间间隔': 'timedelta',
    }
    
    def __init__(self):
        super().__init__(module=datetime, name_map=self.NAME_MAP)
