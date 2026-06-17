"""
xml.etree.ElementTree模块中文封装（XML处理）
"""

import xml.etree.ElementTree as ET

from .base_wrapper import ChineseModuleWrapper


class XmlEtreeWrapper(ChineseModuleWrapper):
    """xml.etree.ElementTree模块中文封装"""

    NAME_MAP = {
        "解析": "parse",
        "从字符串解析": "fromstring",
        "转字符串": "tostring",
        "元素": "Element",
        "子元素": "SubElement",
        "查找": "find",
        "查找所有": "findall",
        "写入": "ElementTree",
    }

    def __init__(self):
        super().__init__(module=ET, name_map=self.NAME_MAP)
