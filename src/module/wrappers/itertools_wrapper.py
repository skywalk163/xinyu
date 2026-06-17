"""
itertools模块中文封装（迭代器工具）
"""

import itertools

from .base_wrapper import ChineseModuleWrapper


class ItertoolsWrapper(ChineseModuleWrapper):
    """itertools模块中文封装"""

    NAME_MAP = {
        "计数": "count",
        "循环": "cycle",
        "重复": "repeat",
        "累加": "accumulate",
        "链式": "chain",
        "压缩": "compress",
        "丢弃": "dropwhile",
        "过滤": "filterfalse",
        "分组": "groupby",
        "切片": "islice",
        "排列": "permutations",
        "组合": "combinations",
        "笛卡尔积": "product",
    }

    def __init__(self):
        super().__init__(module=itertools, name_map=self.NAME_MAP)
