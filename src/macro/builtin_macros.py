"""
内置宏

提供语言内置的标准宏，如遍历、重复、持续、除非等。
"""

from src.macro.macro_system import Macro, MacroType


def register_builtin_macros(macro_system):
    """
    注册内置宏到宏系统

    Args:
        macro_system: 宏系统实例
    """

    # 遍历宏：遍历列表中的每个元素
    macro_system.register(
        "遍历",
        Macro(
            name="遍历",
            type=MacroType.SYNTAX,
            params=["变量", "列表", "循环体"],
            body="定迭代器=列表的迭代器。当迭代器有下一个：定变量=迭代器下一个。循环体。",
            description="遍历列表中的每个元素",
        ),
    )

    # 重复宏：重复执行指定次数
    macro_system.register(
        "重复",
        Macro(
            name="重复",
            type=MacroType.SYNTAX,
            params=["次数", "循环体"],
            body="定计数器=0。当计数器小于次数：循环体。计数器=计数器加1。",
            description="重复执行指定次数",
        ),
    )

    # 持续宏：持续执行（无限循环）
    macro_system.register(
        "持续",
        Macro(
            name="持续",
            type=MacroType.SYNTAX,
            params=["循环体"],
            body="若真：循环体。持续：循环体。",
            description="持续执行（无限循环）",
        ),
    )

    # 除非宏：除非条件成立，否则执行动作
    macro_system.register(
        "除非",
        Macro(
            name="除非",
            type=MacroType.SYNTAX,
            params=["条件", "动作"],
            body="若非(条件)：动作。",
            description="除非条件成立，否则执行动作",
        ),
    )

    # 当...时宏：当条件成立时重复执行
    macro_system.register(
        "当",
        Macro(
            name="当",
            type=MacroType.SYNTAX,
            params=["条件", "循环体"],
            body="若条件：循环体。当条件：循环体。",
            description="当条件成立时重复执行",
        ),
    )

    # 断言宏：断言条件为真
    macro_system.register(
        "断言",
        Macro(
            name="断言",
            type=MacroType.SYNTAX,
            params=["条件", "消息"],
            body="若非条件：印消息。抛出异常。",
            description="断言条件为真，否则抛出异常",
        ),
    )

    # 调试宏：打印调试信息
    macro_system.register(
        "调试",
        Macro(
            name="调试",
            type=MacroType.SYNTAX,
            params=["表达式"],
            body='印"调试: 表达式 = "。印表达式。',
            description="打印调试信息",
        ),
    )

    # 计时宏：测量执行时间
    macro_system.register(
        "计时",
        Macro(
            name="计时",
            type=MacroType.SYNTAX,
            params=["代码块"],
            body='定开始时间=当前时间。代码块。定结束时间=当前时间。印"耗时: "。印(结束时间减开始时间)。',
            description="测量代码块执行时间",
        ),
    )
