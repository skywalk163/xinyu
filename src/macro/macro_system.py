"""
宏系统核心

提供宏的定义、注册、查找和展开功能。
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class MacroType(Enum):
    """宏类型"""

    SYNTAX = "syntax"  # 语法宏
    IDIOM = "idiom"  # 成语宏


@dataclass
class Macro:
    """宏定义"""

    name: str
    type: MacroType
    params: List[str]
    body: str
    description: Optional[str] = None

    def __str__(self):
        return f"Macro({self.name}, type={self.type.value}, params={self.params})"


class MacroSystem:
    """宏系统核心类"""

    def __init__(self):
        self.macros: Dict[str, Macro] = {}
        self.macro_stack: List[str] = []  # 用于检测递归展开

    def register(self, name: str, macro: Macro):
        """注册宏"""
        self.macros[name] = macro

    def unregister(self, name: str):
        """注销宏"""
        if name in self.macros:
            del self.macros[name]

    def get(self, name: str) -> Optional[Macro]:
        """获取宏"""
        return self.macros.get(name)

    def has(self, name: str) -> bool:
        """检查宏是否存在"""
        return name in self.macros

    def expand(self, name: str, args: Dict[str, Any]) -> str:
        """展开宏

        Args:
            name: 宏名称
            args: 参数字典

        Returns:
            展开后的代码字符串
        """
        macro = self.get(name)
        if not macro:
            raise ValueError(f"未定义的宏: {name}")

        # 检测递归展开
        if name in self.macro_stack:
            raise ValueError(f"检测到宏递归展开: {name}")

        self.macro_stack.append(name)

        try:
            # 参数替换
    _ =   # 未使用变量
            for param in macro.params:
                if param in args:
                    # 获取参数的实际值（如果是AST节点，提取其值）
                    arg_value = args[param]

                    # 修改：检查节点类型，正确处理字符串字面量
                    from src.parser.ast_nodes import IdentifierNode, NumberNode, StringNode

                    if isinstance(arg_value, StringNode):
                        # 对于StringNode，保留引号，确保展开后仍是字符串字面量
                        replacement = f'"{arg_value.value}"'
                    elif isinstance(arg_value, NumberNode):
                        # 对于NumberNode，直接使用数值
                        replacement = str(arg_value.value)
                    elif isinstance(arg_value, IdentifierNode):
                        # 对于IdentifierNode，使用其name属性
                        replacement = arg_value.name
                    elif hasattr(arg_value, "value"):
                        # 其他有value属性的节点
                        replacement = str(arg_value.value)
                    elif hasattr(arg_value, "name"):
                        # 其他有name属性的节点
                        replacement = arg_value.name
                    elif isinstance(arg_value, list):
                        # 对于AST节点列表（如循环体），生成代码字符串
                        from src.codegen.python_codegen import PythonCodegen

                        codegen = PythonCodegen()
                        # 为每个语句生成代码
                        statements_code = []
                        for stmt in arg_value:
                            try:
                                code = codegen.generate(stmt)
                                statements_code.append(code)
                            except Exception:
                                # 如果无法生成代码，使用占位符
                                statements_code.append(f"/* {param} */")
                        replacement = "。".join(statements_code)
                    else:
                        # 其他情况使用字符串表示
                        replacement = str(arg_value)
    _ = , replacement)  # 未使用变量

            return result
        finally:
            self.macro_stack.pop()

    def list_macros(self) -> List[str]:
        """列出所有宏"""
        return list(self.macros.keys())

    def list_macros_by_type(self, macro_type: MacroType) -> List[str]:
        """列出指定类型的宏"""
        return [name for name, macro in self.macros.items() if macro.type == macro_type]
