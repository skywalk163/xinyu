"""
宏系统测试

测试宏的定义、注册、展开等功能。
"""


from src.macro.builtin_macros import register_builtin_macros
from src.macro.idiom_macros import register_idiom_macros
from src.macro.macro_expander import MacroExpander
from src.macro.macro_system import Macro, MacroSystem, MacroType


class TestMacro:
    """测试Macro类"""

    def test_macro_creation(self):
        """测试宏创建"""
        macro = Macro(
            name="重复",
            type=MacroType.SYNTAX,
            params=["次数", "循环体"],
            body="定计数器=0。当计数器小于次数：循环体。计数器=计数器加1。",
            description="重复执行指定次数",
        )
        assert macro.name == "重复"
        assert macro.type == MacroType.SYNTAX
        assert len(macro.params) == 2
        assert "计数器" in macro.body

    def test_macro_with_description(self):
        """测试带描述的宏"""
        macro = Macro(
            name="循环",
            type=MacroType.SYNTAX,
            params=["变量", "列表", "循环体"],
            body="定迭代器=列表的迭代器。当迭代器有下一个：定变量=迭代器下一个。循环体。",
            description="遍历列表中的每个元素",
        )
        assert macro.description == "遍历列表中的每个元素"


class TestMacroSystem:
    """测试MacroSystem类"""

    def test_macro_system_creation(self):
        """测试宏系统创建"""
        system = MacroSystem()
        assert len(system.list_macros()) == 0

    def test_macro_registration(self):
        """测试宏注册"""
        system = MacroSystem()
        macro = Macro(
            name="重复",
            type=MacroType.SYNTAX,
            params=["次数", "循环体"],
            body="定计数器=0。当计数器小于次数：循环体。计数器=计数器加1。",
        )
        system.register("重复", macro)
        assert system.has("重复")
        assert not system.has("不存在的宏")

    def test_macro_get(self):
        """测试获取宏"""
        system = MacroSystem()
        macro = Macro(
            name="重复",
            type=MacroType.SYNTAX,
            params=["次数", "循环体"],
            body="定计数器=0。当计数器小于次数：循环体。计数器=计数器加1。",
        )
        system.register("重复", macro)
        retrieved = system.get("重复")
        assert retrieved.name == "重复"

    def test_macro_unregister(self):
        """测试注销宏"""
        system = MacroSystem()
        macro = Macro(
            name="重复",
            type=MacroType.SYNTAX,
            params=["次数", "循环体"],
            body="定计数器=0。当计数器小于次数：循环体。计数器=计数器加1。",
        )
        system.register("重复", macro)
        assert system.has("重复")
        system.unregister("重复")
        assert not system.has("重复")

    def test_macro_expand(self):
        """测试宏展开"""
        system = MacroSystem()
        macro = Macro(
            name="重复",
            type=MacroType.SYNTAX,
            params=["次数", "循环体"],
            body="定计数器=0。当计数器小于次数：循环体。计数器=计数器加1。",
        )
        system.register("重复", macro)

        # 展开宏调用
        expanded = system.expand("重复", {"次数": "5", "循环体": '印"你好"。'})
        assert "定计数器=0" in expanded
        assert "当计数器小于5" in expanded
        assert '印"你好"。' in expanded

    def test_macro_expand_with_multiple_params(self):
        """测试多参数宏展开"""
        system = MacroSystem()
        macro = Macro(
            name="循环",
            type=MacroType.SYNTAX,
            params=["变量", "列表", "循环体"],
            body="定迭代器=列表的迭代器。当迭代器有下一个：定变量=迭代器下一个。循环体。",
        )
        system.register("循环", macro)

        expanded = system.expand("循环", {"变量": "用户", "列表": "用户列表", "循环体": "发送通知给用户。"})
        assert "迭代器" in expanded
        assert "用户列表" in expanded
        assert "定用户=迭代器下一个" in expanded


class TestBuiltinMacros:
    """测试内置宏"""

    def test_builtin_macros_registration(self):
        """测试内置宏注册"""
        system = MacroSystem()
        register_builtin_macros(system)

        # 检查内置宏
        assert system.has("遍历")
        assert system.has("重复")
        assert system.has("持续")
        assert system.has("除非")

    def test_for_loop_expansion(self):
        """测试遍历宏展开"""
        system = MacroSystem()
        register_builtin_macros(system)

        expanded = system.expand("遍历", {"变量": "用户", "列表": "用户列表", "循环体": "发送通知给用户。"})

        assert "迭代器" in expanded
        assert "用户列表" in expanded

    def test_repeat_loop_expansion(self):
        """测试重复宏展开"""
        system = MacroSystem()
        register_builtin_macros(system)

        expanded = system.expand("重复", {"次数": "5", "循环体": "尝试连接。"})

        assert "计数器" in expanded
        assert "5" in expanded


class TestMacroExpander:
    """测试宏展开器"""

    def test_expander_creation(self):
        """测试展开器创建"""
        system = MacroSystem()
        expander = MacroExpander(system)
        assert expander.macro_system == system

    def test_expand_simple_macro(self):
        """测试展开简单宏"""
        system = MacroSystem()
        macro = Macro(
            name="重复",
            type=MacroType.SYNTAX,
            params=["次数", "循环体"],
            body="定计数器=0。当计数器小于次数：循环体。计数器=计数器加1。",
        )
        system.register("重复", macro)
        MacroExpander(system)

        # 测试宏展开功能（通过宏系统直接展开）
        expanded_code = system.expand("重复", {"次数": "5", "循环体": '印"你好"。'})
        assert "定计数器=0" in expanded_code
        assert "当计数器小于5" in expanded_code
        assert '印"你好"。' in expanded_code


class TestIdiomMacros:
    """测试成语宏"""

    def test_idiom_macros_registration(self):
        """测试成语宏注册"""
        system = MacroSystem()
        register_idiom_macros(system)

        # 检查成语宏
        assert system.has("守株待兔")
        assert system.has("亡羊补牢")
        assert system.has("画蛇添足")
        assert system.has("一举两得")
        assert system.has("循序渐进")

    def test_idiom_expansion(self):
        """测试成语宏展开"""
        system = MacroSystem()
        register_idiom_macros(system)

        # 测试守株待兔宏展开
        expanded = system.expand("守株待兔", {"事件": "用户点击", "处理函数": "处理点击"})

        assert "持续" in expanded or "若真" in expanded
        assert "用户点击" in expanded

    def test_yi_ju_liang_de_expansion(self):
        """测试一举两得宏展开"""
        system = MacroSystem()
        register_idiom_macros(system)

        expanded = system.expand("一举两得", {"动作1": "保存数据", "动作2": "发送通知"})

        assert "定结果1=保存数据" in expanded
        assert "定结果2=发送通知" in expanded
        assert "返回" in expanded
