"""动词注册表单元测试

测试动词注册和查询功能。
"""

import pytest

from src.parser.arity import Arity
from src.parser.verb_registry import VerbRegistry


class TestVerbRegistry:
    """动词注册表测试"""

    def test_register_operator(self):
        """测试注册操作符"""
        registry = VerbRegistry()
        registry.register("相加", Arity.fixed(2), is_operator=True)

        assert registry.is_operator("相加") == True
        assert registry.is_function("相加") == False
        assert registry.is_registered("相加") == True

        arity = registry.get("相加")
        assert arity is not None
        assert arity.count == 2

    def test_register_function(self):
        """测试注册函数"""
        registry = VerbRegistry()
        registry.register("打印", Arity.variable(min=1), is_function=True)

        assert registry.is_function("打印") == True
        assert registry.is_operator("打印") == False
        assert registry.is_registered("打印") == True

        arity = registry.get("打印")
        assert arity is not None
        assert arity.min_count == 1

    def test_register_both(self):
        """测试同时注册为操作符和函数"""
        registry = VerbRegistry()
        registry.register("相加", Arity.fixed(2), is_operator=True, is_function=True)

        assert registry.is_operator("相加") == True
        assert registry.is_function("相加") == True

    def test_get_unregistered_verb(self):
        """测试获取未注册的动词"""
        registry = VerbRegistry()
        arity = registry.get("未知动词")
        assert arity is None

    def test_is_registered(self):
        """测试判断是否已注册"""
        registry = VerbRegistry()
        assert registry.is_registered("相加") == False

        registry.register("相加", Arity.fixed(2), is_operator=True)
        assert registry.is_registered("相加") == True

    def test_unregister(self):
        """测试注销动词"""
        registry = VerbRegistry()
        registry.register("相加", Arity.fixed(2), is_operator=True)
        assert registry.is_registered("相加") == True

        registry.unregister("相加")
        assert registry.is_registered("相加") == False
        assert registry.is_operator("相加") == False

    def test_clear(self):
        """测试清空注册表"""
        registry = VerbRegistry()
        registry.register("相加", Arity.fixed(2), is_operator=True)
        registry.register("打印", Arity.variable(min=1), is_function=True)

        registry.clear()

        assert registry.is_registered("相加") == False
        assert registry.is_registered("打印") == False

    def test_builtin_verbs(self):
        """测试内置动词"""
        registry = VerbRegistry()
        registry.register_builtin_verbs()

        # 测试操作符动词
        assert registry.is_operator("相加") == True
        assert registry.is_operator("相减") == True
        assert registry.is_operator("相乘") == True
        assert registry.is_operator("相除") == True

        # 测试函数动词
        assert registry.is_function("打印") == True
        assert registry.is_function("输入") == True
        assert registry.is_function("求和") == True

        # 测试元数
        assert registry.get("相加").count == 2
        assert registry.get("打印").min_count == 1
        assert registry.get("输入").count == 1

    def test_get_all_operators(self):
        """测试获取所有操作符"""
        registry = VerbRegistry()
        registry.register_builtin_verbs()

        operators = registry.get_all_operators()
        assert "相加" in operators
        assert "相减" in operators
        assert "打印" not in operators  # 打印是函数，不是操作符

    def test_get_all_functions(self):
        """测试获取所有函数"""
        registry = VerbRegistry()
        registry.register_builtin_verbs()

        functions = registry.get_all_functions()
        assert "打印" in functions
        assert "输入" in functions
        assert "相加" not in functions  # 相加是操作符，不是函数

    def test_get_all_verbs(self):
        """测试获取所有动词"""
        registry = VerbRegistry()
        registry.register_builtin_verbs()

        verbs = registry.get_all_verbs()
        assert "相加" in verbs
        assert "打印" in verbs
        assert len(verbs) > 0

    def test_str_representation(self):
        """测试字符串表示"""
        registry = VerbRegistry()
        registry.register_builtin_verbs()
        result = str(registry)
        assert "VerbRegistry" in result
        assert "操作符" in result
        assert "函数" in result

    def test_repr_representation(self):
        """测试详细表示"""
        registry = VerbRegistry()
        registry.register_builtin_verbs()
        result = repr(registry)
        assert "VerbRegistry" in result
        assert "operators" in result
        assert "functions" in result

    def test_math_functions(self):
        """测试数学函数"""
        registry = VerbRegistry()
        registry.register_builtin_verbs()

        # 平方根：固定1个参数
        assert registry.is_function("平方根") == True
        assert registry.get("平方根").count == 1

        # 绝对值：固定1个参数
        assert registry.is_function("绝对值") == True
        assert registry.get("绝对值").count == 1

        # 最大值：可变参数（最少1个）
        assert registry.is_function("最大值") == True
        assert registry.get("最大值").min_count == 1

    def test_list_functions(self):
        """测试列表函数"""
        registry = VerbRegistry()
        registry.register_builtin_verbs()

        # 长度：固定1个参数
        assert registry.is_function("长度") == True
        assert registry.get("长度").count == 1

        # 范围：1-3个参数
        assert registry.is_function("范围") == True
        arity = registry.get("范围")
        assert arity.min_count == 1
        assert arity.max_count == 3

    def test_type_conversion_functions(self):
        """测试类型转换函数"""
        registry = VerbRegistry()
        registry.register_builtin_verbs()

        # 转整数：固定1个参数
        assert registry.is_function("转整数") == True
        assert registry.get("转整数").count == 1

        # 转浮点：固定1个参数
        assert registry.is_function("转浮点") == True
        assert registry.get("转浮点").count == 1

        # 转字符串：固定1个参数
        assert registry.is_function("转字符串") == True
        assert registry.get("转字符串").count == 1
