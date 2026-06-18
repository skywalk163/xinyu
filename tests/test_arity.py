"""元数系统单元测试

测试元数定义和验证功能。
"""

from src.parser.arity import Arity, ArityType


class TestArity:
    """元数测试"""

    def test_fixed_arity_creation(self):
        """测试固定元数创建"""
        arity = Arity.fixed(2)
        assert arity.type == ArityType.FIXED
        assert arity.count == 2

    def test_fixed_arity_satisfied(self):
        """测试固定元数验证"""
        arity = Arity.fixed(2)
        assert arity.is_satisfied(2) is True
        assert arity.is_satisfied(1) is False
        assert arity.is_satisfied(3) is False

    def test_fixed_arity_stop_collecting(self):
        """测试固定元数停止收集"""
        arity = Arity.fixed(2)
        assert arity.should_stop_collecting(0) is False
        assert arity.should_stop_collecting(1) is False
        assert arity.should_stop_collecting(2) is True
        assert arity.should_stop_collecting(3) is True

    def test_variable_arity_creation(self):
        """测试可变元数创建"""
        arity = Arity.variable(min=0)
        assert arity.type == ArityType.VARIABLE
        assert arity.min_count == 0

    def test_variable_arity_satisfied(self):
        """测试可变元数验证"""
        arity = Arity.variable(min=0)
        assert arity.is_satisfied(0) is True
        assert arity.is_satisfied(1) is True
        assert arity.is_satisfied(5) is True

    def test_variable_arity_with_min(self):
        """测试可变元数（有最小值）"""
        arity = Arity.variable(min=1)
        assert arity.is_satisfied(0) is False
        assert arity.is_satisfied(1) is True
        assert arity.is_satisfied(5) is True

    def test_variable_arity_stop_collecting(self):
        """测试可变元数停止收集"""
        arity = Arity.variable(min=0)
        # 可变元数不主动停止
        assert arity.should_stop_collecting(0) is False
        assert arity.should_stop_collecting(5) is False

    def test_minimum_arity_creation(self):
        """测试最小元数创建"""
        arity = Arity.min(2)
        assert arity.type == ArityType.MINIMUM
        assert arity.min_count == 2

    def test_minimum_arity_satisfied(self):
        """测试最小元数验证"""
        arity = Arity.min(2)
        assert arity.is_satisfied(1) is False
        assert arity.is_satisfied(2) is True
        assert arity.is_satisfied(5) is True

    def test_minimum_arity_stop_collecting(self):
        """测试最小元数停止收集"""
        arity = Arity.min(2)
        # 最小元数不主动停止
        assert arity.should_stop_collecting(0) is False
        assert arity.should_stop_collecting(2) is False
        assert arity.should_stop_collecting(5) is False

    def test_range_arity_creation(self):
        """测试范围元数创建"""
        arity = Arity.range(min=1, max=3)
        assert arity.type == ArityType.RANGE
        assert arity.min_count == 1
        assert arity.max_count == 3

    def test_range_arity_satisfied(self):
        """测试范围元数验证"""
        arity = Arity.range(min=1, max=3)
        assert arity.is_satisfied(0) is False
        assert arity.is_satisfied(1) is True
        assert arity.is_satisfied(2) is True
        assert arity.is_satisfied(3) is True
        assert arity.is_satisfied(4) is False

    def test_range_arity_stop_collecting(self):
        """测试范围元数停止收集"""
        arity = Arity.range(min=1, max=3)
        assert arity.should_stop_collecting(0) is False
        assert arity.should_stop_collecting(1) is False
        assert arity.should_stop_collecting(2) is False
        assert arity.should_stop_collecting(3) is True
        assert arity.should_stop_collecting(4) is True

    def test_arity_str_representation(self):
        """测试元数字符串表示"""
        assert str(Arity.fixed(2)) == "固定2个参数"
        assert str(Arity.variable(min=0)) == "可变参数（最少0个）"
        assert str(Arity.min(2)) == "最少2个参数"
        assert str(Arity.range(min=1, max=3)) == "1-3个参数"

    def test_arity_repr_representation(self):
        """测试元数详细表示"""
        assert repr(Arity.fixed(2)) == "Arity.fixed(2)"
        assert repr(Arity.variable(min=0)) == "Arity.variable(min=0)"
        assert repr(Arity.min(2)) == "Arity.min(2)"
        assert repr(Arity.range(min=1, max=3)) == "Arity.range(min=1, max=3)"
