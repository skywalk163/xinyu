"""
内置函数文档管理

提供内置函数的中文文档查询功能。
"""

from typing import Dict, Optional


class BuiltinDocs:
    """内置函数文档管理类"""

    def __init__(self):
        """初始化文档管理器"""
        self._docs: Dict[str, str] = {}

    def get_doc(self, name: str) -> Optional[str]:
        """获取函数文档"""
        return self._docs.get(name)

    def register_doc(self, name: str, doc: str) -> None:
        """注册函数文档"""
        self._docs[name] = doc
