"""
成语宏

提供中文成语风格的宏，使代码更符合中文表达习惯。
"""

from src.macro.macro_system import Macro, MacroType


def register_idiom_macros(macro_system):
    """
    注册成语宏到宏系统

    Args:
        macro_system: 宏系统实例
    """

    # 守株待兔：事件监听循环
    macro_system.register("守株待兔", Macro(
        name="守株待兔",
        type=MacroType.IDIOM,
        params=["事件", "处理函数"],
        body="持续：事件，等待发生。处理函数。",
        description="等待事件发生并处理（事件监听循环）"
    ))

    # 亡羊补牢：错误补救
    macro_system.register("亡羊补牢", Macro(
        name="亡羊补牢",
        type=MacroType.IDIOM,
        params=["错误", "补救措施"],
        body="若错误发生：补救措施。返回成功。否则：返回失败。",
        description="错误发生后进行补救"
    ))

    # 画蛇添足：多余操作
    macro_system.register("画蛇添足", Macro(
        name="画蛇添足",
        type=MacroType.IDIOM,
        params=["数据", "多余操作"],
        body="数据，处理。多余操作。返回数据。",
        description="在数据处理后执行多余操作"
    ))

    # 一举两得：同时执行两个操作
    macro_system.register("一举两得", Macro(
        name="一举两得",
        type=MacroType.IDIOM,
        params=["动作1", "动作2"],
        body="定结果1=动作1。定结果2=动作2。返回列(结果1, 结果2)。",
        description="同时执行两个操作并返回结果"
    ))

    # 循序渐进：逐步处理
    macro_system.register("循序渐进", Macro(
        name="循序渐进",
        type=MacroType.IDIOM,
        params=["步骤列表"],
        body="遍历步骤于步骤列表：执行步骤。",
        description="按顺序执行一系列步骤"
    ))

    # 未雨绸缪：提前准备
    macro_system.register("未雨绸缪", Macro(
        name="未雨绸缪",
        type=MacroType.IDIOM,
        params=["条件", "准备工作"],
        body="若条件：准备工作。否则：印\"无需准备\"。",
        description="提前做好准备"
    ))

    # 见机行事：根据情况执行
    macro_system.register("见机行事", Macro(
        name="见机行事",
        type=MacroType.IDIOM,
        params=["情况", "动作列表"],
        body="遍历情况于情况列表：若情况满足：执行对应动作。",
        description="根据情况执行相应动作"
    ))

    # 水到渠成：条件满足后自然完成
    macro_system.register("水到渠成", Macro(
        name="水到渠成",
        type=MacroType.IDIOM,
        params=["前置条件", "目标动作"],
        body="若前置条件：目标动作。返回成功。否则：返回失败。",
        description="条件满足后自然完成目标"
    ))

    # 按部就班：按步骤执行
    macro_system.register("按部就班", Macro(
        name="按部就班",
        type=MacroType.IDIOM,
        params=["步骤"],
        body="遍历步骤于步骤列表：执行步骤。检查结果。",
        description="按步骤有序执行"
    ))

    # 因地制宜：根据环境执行不同操作
    macro_system.register("因地制宜", Macro(
        name="因地制宜",
        type=MacroType.IDIOM,
        params=["环境", "操作映射"],
        body="定当前环境=环境。遍历操作于操作映射：若环境匹配：执行操作。",
        description="根据环境执行不同操作"
    ))
