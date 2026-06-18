"""动词元数注册表

管理所有动词（函数和操作符）的元数信息。

动词分类：
1. 操作符动词（Operator Verbs）：中缀位置，固定元数
   - 示例：相加、相减、相乘、相除
   - 特点：在表达式中作为操作符使用

2. 函数动词（Function Verbs）：前缀位置，元数可变
   - 示例：打印、求和、斐波那契
   - 特点：作为函数调用使用
"""

from typing import Dict, Optional, Set

from .arity import Arity


class VerbRegistry:
    """动词元数注册表

    管理所有动词的元数信息，支持：
    - 注册动词及其元数
    - 查询动词元数
    - 区分操作符动词和函数动词
    - 内置动词自动注册

    示例：
        registry = VerbRegistry()
        registry.register_builtin_verbs()

        # 查询元数
        arity = registry.get("相加")  # Arity.fixed(2)

        # 判断类型
        registry.is_operator("相加")  # True
        registry.is_function("打印")  # True
    """

    def __init__(self):
        """初始化动词注册表"""
        self._verbs: Dict[str, Arity] = {}
        self._operator_verbs: Set[str] = set()  # 操作符动词
        self._function_verbs: Set[str] = set()  # 函数动词

    def register(
        self, name: str, arity: Arity, is_operator: bool = False, is_function: bool = False
    ) -> None:
        """注册动词

        Args:
            name: 动词名称
            arity: 元数定义
            is_operator: 是否是操作符动词
            is_function: 是否是函数动词

        示例：
            registry.register("相加", Arity.fixed(2), is_operator=True)
            registry.register("打印", Arity.variable(min=1), is_function=True)
        """
        self._verbs[name] = arity
        if is_operator:
            self._operator_verbs.add(name)
        if is_function:
            self._function_verbs.add(name)

    def get(self, name: str) -> Optional[Arity]:
        """获取动词元数

        Args:
            name: 动词名称

        Returns:
            元数定义，如果未注册则返回None
        """
        return self._verbs.get(name)

    def is_operator(self, name: str) -> bool:
        """判断是否是操作符动词

        Args:
            name: 动词名称

        Returns:
            是否是操作符动词
        """
        return name in self._operator_verbs

    def is_function(self, name: str) -> bool:
        """判断是否是函数动词

        Args:
            name: 动词名称

        Returns:
            是否是函数动词
        """
        return name in self._function_verbs

    def is_registered(self, name: str) -> bool:
        """判断动词是否已注册

        Args:
            name: 动词名称

        Returns:
            是否已注册
        """
        return name in self._verbs

    def register_builtin_verbs(self) -> None:
        """注册内置动词

        包括：
        - 操作符动词（相加、相减、相乘、相除等）
        - 内置函数（打印、输入、求和等）
        - 数学函数（平方根、绝对值等）
        """
        # 操作符动词（固定2个参数，中缀）
        operators = [
            "相加",
            "相减",
            "相乘",
            "相除",
            "取余",
            "等于",
            "不等",
            "大于",
            "小于",
            "大于等于",
            "小于等于",
            "并且",
            "或者",
        ]
        for op in operators:
            self.register(op, Arity.fixed(2), is_operator=True)

        # 内置函数（可变参数）
        self.register("打印", Arity.variable(min=1), is_function=True)
        self.register("输入", Arity.fixed(1), is_function=True)

        # 数学函数
        self.register("平方根", Arity.fixed(1), is_function=True)
        self.register("绝对值", Arity.fixed(1), is_function=True)
        self.register("最大值", Arity.variable(min=1), is_function=True)
        self.register("最小值", Arity.variable(min=1), is_function=True)
        self.register("求和", Arity.variable(min=1), is_function=True)

        # 列表函数
        self.register("长度", Arity.fixed(1), is_function=True)
        self.register("范围", Arity.range(min=1, max=3), is_function=True)

        # 类型转换函数
        self.register("转整数", Arity.fixed(1), is_function=True)
        self.register("转浮点", Arity.fixed(1), is_function=True)
        self.register("转字符串", Arity.fixed(1), is_function=True)

        # 列表操作函数
        self.register("列表", Arity.variable(min=0), is_function=True)
        self.register("追加", Arity.fixed(2), is_function=True)
        self.register("弹出", Arity.fixed(1), is_function=True)

    def unregister(self, name: str) -> None:
        """注销动词

        Args:
            name: 动词名称
        """
        if name in self._verbs:
            del self._verbs[name]
        self._operator_verbs.discard(name)
        self._function_verbs.discard(name)

    def clear(self) -> None:
        """清空注册表"""
        self._verbs.clear()
        self._operator_verbs.clear()
        self._function_verbs.clear()

    def get_all_operators(self) -> Set[str]:
        """获取所有操作符动词

        Returns:
            操作符动词集合
        """
        return self._operator_verbs.copy()

    def get_all_functions(self) -> Set[str]:
        """获取所有函数动词

        Returns:
            函数动词集合
        """
        return self._function_verbs.copy()

    def get_all_verbs(self) -> Dict[str, Arity]:
        """获取所有动词

        Returns:
            动词字典（名称 -> 元数）
        """
        return self._verbs.copy()

    def __str__(self) -> str:
        """字符串表示"""
        return f"VerbRegistry(操作符={len(self._operator_verbs)}, 函数={len(self._function_verbs)})"

    def __repr__(self) -> str:
        """详细表示"""
        return (
            f"VerbRegistry(verbs={len(self._verbs)}, "
            f"operators={self._operator_verbs}, "
            f"functions={self._function_verbs})"
        )
