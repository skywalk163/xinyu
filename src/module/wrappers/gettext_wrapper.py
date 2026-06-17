"""
gettext模块中文封装（国际化）
"""

import gettext

from .base_wrapper import ChineseModuleWrapper


class GettextWrapper(ChineseModuleWrapper):
    """gettext模块中文封装"""

    NAME_MAP = {
        "翻译": "gettext",
        "查找翻译": "find",
        "安装": "install",
        "绑定文本域": "bindtextdomain",
        "文本域": "textdomain",
    }

    def __init__(self):
        super().__init__(module=gettext, name_map=self.NAME_MAP)
