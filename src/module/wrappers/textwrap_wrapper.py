"""
textwrap模块中文封装（文本格式化）
"""

import textwrap

from .base_wrapper import ChineseModuleWrapper


class TextwrapWrapper(ChineseModuleWrapper):
    """textwrap模块中文封装"""

    NAME_MAP = {
        "填充": "fill",
        "包裹": "wrap",
        "缩短": "shorten",
        "缩进": "indent",
        "删除缩进": "dedent",
        "文本包裹器": "TextWrapper",
    }

    def __init__(self):
        super().__init__(module=textwrap, name_map=self.NAME_MAP)
