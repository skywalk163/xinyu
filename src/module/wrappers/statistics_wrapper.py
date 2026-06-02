"""
statistics模块中文封装（统计函数）
"""

import statistics
from .base_wrapper import ChineseModuleWrapper


class StatisticsWrapper(ChineseModuleWrapper):
    """statistics模块中文封装"""
    
    NAME_MAP = {
        '平均值': 'mean',
        '中位数': 'median',
        '众数': 'mode',
        '标准差': 'stdev',
        '方差': 'variance',
        '调和平均': 'harmonic_mean',
        '几何平均': 'geometric_mean',
        '分位数': 'quantiles',
        '相关系数': 'correlation',
        '线性回归': 'linear_regression',
    }
    
    def __init__(self):
        super().__init__(module=statistics, name_map=self.NAME_MAP)
