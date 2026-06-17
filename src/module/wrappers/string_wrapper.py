"""
string模块中文封装（字符串操作）
"""

import string

from .base_wrapper import ChineseModuleWrapper


class StringWrapper(ChineseModuleWrapper):
    """string模块中文封装"""

    NAME_MAP = {
        "数字": "digits",
        "十六进制数字": "hexdigits",
        "八进制数字": "octdigits",
        "字母": "ascii_letters",
        "小写字母": "ascii_lowercase",
        "大写字母": "ascii_uppercase",
        "标点符号": "punctuation",
        "空白字符": "whitespace",
        "可打印字符": "printable",
        "大写": "capwords",
        "模板": "Template",
    }

    def __init__(self):
        super().__init__(module=string, name_map=self.NAME_MAP)
