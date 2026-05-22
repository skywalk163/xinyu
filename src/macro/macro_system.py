"""
宏系统核心

提供宏的注册、查找和管理功能。
"""


class MacroSystem:
    """宏系统核心类"""

    def __init__(self):
        self.macros = {}
        self.macro_stack = []  # 用于检测递归展开

    def register(self, name, macro):
        """注册宏"""
        self.macros[name] = macro

    def unregister(self, name):
        """注销宏"""
        if name in self.macros:
            del self.macros[name]

    def get(self, name):
        """获取宏"""
        return self.macros.get(name)

    def has(self, name):
        """检查宏是否存在"""
        return name in self.macros

    def list_macros(self):
        """列出所有宏"""
        return list(self.macros.keys())
