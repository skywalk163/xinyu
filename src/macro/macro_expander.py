"""
宏展开器

负责展开宏调用，处理嵌套宏和递归展开。
"""


class MacroExpander:
    """宏展开器"""

    def __init__(self, macro_system):
        self.macro_system = macro_system
        self.max_depth = 100  # 防止无限递归
        self.current_depth = 0

    def expand(self, ast):
        """展开 AST 中的所有宏调用"""
        if self.current_depth >= self.max_depth:
            raise RecursionError("宏展开深度超过限制")

        self.current_depth += 1
        try:
            return self._expand_node(ast)
        finally:
            self.current_depth -= 1

    def _expand_node(self, node):
        """展开单个节点"""
        # TODO: 实现具体的展开逻辑
        return node
