"""
random模块中文封装（随机数）
"""

import random
from .base_wrapper import ChineseModuleWrapper


class RandomWrapper(ChineseModuleWrapper):
    """random模块中文封装"""
    
    NAME_MAP = {
        '随机数': 'random',
        '随机整数': 'randint',
        '随机范围': 'randrange',
        '随机选择': 'choice',
        '随机采样': 'sample',
        '随机打乱': 'shuffle',
        '均匀分布': 'uniform',
        '正态分布': 'gauss',
        '设置种子': 'seed',
    }
    
    def __init__(self):
        super().__init__(module=random, name_map=self.NAME_MAP)
