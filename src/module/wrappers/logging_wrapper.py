"""
logging模块中文封装（日志记录）
"""

import logging
from .base_wrapper import ChineseModuleWrapper


class LoggingWrapper(ChineseModuleWrapper):
    """logging模块中文封装"""
    
    NAME_MAP = {
        '获取记录器': 'getLogger',
        '调试': 'debug',
        '信息': 'info',
        '警告': 'warning',
        '错误': 'error',
        '严重': 'critical',
        '异常': 'exception',
        '基本配置': 'basicConfig',
        '记录器': 'Logger',
        '格式化器': 'Formatter',
        '处理器': 'Handler',
        '文件处理器': 'FileHandler',
        '流处理器': 'StreamHandler',
    }
    
    def __init__(self):
        super().__init__(module=logging, name_map=self.NAME_MAP)
