#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""参数验证器测试"""

import pytest

from src.validation.param_validator import ParamValidator, ValidationResult


class TestParamValidator:
    """参数验证器测试类"""

    def test_validation_result_initialization(self):
        """测试ValidationResult初始化"""
        # 有效结果
        valid_result = ValidationResult(is_valid=True)
        assert valid_result.is_valid is True
        assert valid_result.error_message is None

        # 无效结果
        error_msg = "参数数量不足"
        invalid_result = ValidationResult(is_valid=False, error_message=error_msg)
        assert invalid_result.is_valid is False
        assert invalid_result.error_message == error_msg

    def test_validation_result_dataclass(self):
        """测试ValidationResult数据类特性"""
        result1 = ValidationResult(is_valid=True)
        result2 = ValidationResult(is_valid=True)
        result3 = ValidationResult(is_valid=False, error_message="错误")

        # 相等性测试
        assert result1 == result2
        assert result1 != result3

        # 字符串表示
        assert "is_valid=True" in str(result1)
        assert "error_message='错误'" in str(result3)

    def test_param_validator_initialization(self):
        """测试ParamValidator初始化"""
        validator = ParamValidator()
        assert validator is not None

    def test_validate_default_implementation(self):
        """测试validate默认实现"""
        validator = ParamValidator()

        # 默认实现应该总是返回有效
        result = validator.validate(None, (), {})
        assert result.is_valid is True
        assert result.error_message is None

        # 带参数的测试
        result = validator.validate("func", (1, 2, 3), {"a": 1})
        assert result.is_valid is True
        assert result.error_message is None

    def test_check_count_valid(self):
        """测试检查有效参数数量"""
        validator = ParamValidator()

        # 正好在范围内
        args = (1, 2, 3)
        result = validator.check_count(args, min_args=1, max_args=3)
        assert result.is_valid is True
        assert result.error_message is None

        # 最小值边界
        args = (1,)
        result = validator.check_count(args, min_args=1, max_args=5)
        assert result.is_valid is True
        assert result.error_message is None

        # 最大值边界
        args = (1, 2, 3, 4, 5)
        result = validator.check_count(args, min_args=0, max_args=5)
        assert result.is_valid is True
        assert result.error_message is None

        # 无最大值限制
        args = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        result = validator.check_count(args, min_args=0, max_args=None)
        assert result.is_valid is True
        assert result.error_message is None

    def test_check_count_too_few_args(self):
        """测试参数数量不足"""
        validator = ParamValidator()

        args = (1, 2)  # 只有2个参数
        result = validator.check_count(args, min_args=3, max_args=5)

        assert result.is_valid is False
        assert result.error_message is not None
        assert "参数数量不足" in result.error_message
        assert "需要至少3个参数" in result.error_message
        assert "但只提供了2个" in result.error_message

        # 边界情况：0个参数但需要1个
        args = ()
        result = validator.check_count(args, min_args=1, max_args=3)
        assert result.is_valid is False
        assert "需要至少1个参数" in result.error_message
        assert "但只提供了0个" in result.error_message

    def test_check_count_too_many_args(self):
        """测试参数数量过多"""
        validator = ParamValidator()

        args = (1, 2, 3, 4, 5)  # 5个参数
        result = validator.check_count(args, min_args=1, max_args=3)

        assert result.is_valid is False
        assert result.error_message is not None
        assert "参数数量过多" in result.error_message
        assert "最多接受3个参数" in result.error_message
        assert "但提供了5个" in result.error_message

        # 边界情况：正好超过最大值
        args = (1, 2, 3, 4)
        result = validator.check_count(args, min_args=0, max_args=3)
        assert result.is_valid is False
        assert "最多接受3个参数" in result.error_message
        assert "但提供了4个" in result.error_message

    def test_check_type_valid(self):
        """测试检查有效类型"""
        validator = ParamValidator()

        # 整数类型
        result = validator.check_type(42, int)
        assert result.is_valid is True
        assert result.error_message is None

        # 字符串类型
        result = validator.check_type("hello", str)
        assert result.is_valid is True
        assert result.error_message is None

        # 浮点数类型
        result = validator.check_type(3.14, float)
        assert result.is_valid is True
        assert result.error_message is None

        # 布尔类型
        result = validator.check_type(True, bool)
        assert result.is_valid is True
        assert result.error_message is None

        # 列表类型
        result = validator.check_type([1, 2, 3], list)
        assert result.is_valid is True
        assert result.error_message is None

        # 字典类型
        result = validator.check_type({"a": 1}, dict)
        assert result.is_valid is True
        assert result.error_message is None

        # None类型
        result = validator.check_type(None, type(None))
        assert result.is_valid is True
        assert result.error_message is None

    def test_check_type_invalid(self):
        """测试检查无效类型"""
        validator = ParamValidator()

        # 期望整数但得到字符串
        result = validator.check_type("42", int)
        assert result.is_valid is False
        assert result.error_message is not None
        assert "参数类型错误" in result.error_message
        assert "期望int" in result.error_message
        assert "实际str" in result.error_message

        # 期望字符串但得到整数
        result = validator.check_type(42, str)
        assert result.is_valid is False
        assert "期望str" in result.error_message
        assert "实际int" in result.error_message

        # 期望列表但得到字典
        result = validator.check_type({"a": 1}, list)
        assert result.is_valid is False
        assert "期望list" in result.error_message
        assert "实际dict" in result.error_message

        # 期望布尔但得到整数
        result = validator.check_type(1, bool)
        assert result.is_valid is False
        assert "期望bool" in result.error_message
        assert "实际int" in result.error_message

    def test_check_type_with_subclasses(self):
        """测试检查类型与子类"""
        validator = ParamValidator()

        # 创建自定义类
        class BaseClass:
            pass

        class DerivedClass(BaseClass):
            pass

        # 子类实例应该通过基类检查
        derived = DerivedClass()
        result = validator.check_type(derived, BaseClass)
        assert result.is_valid is True
        assert result.error_message is None

        # 基类实例不应该通过子类检查
        base = BaseClass()
        result = validator.check_type(base, DerivedClass)
        assert result.is_valid is False
        assert "期望DerivedClass" in result.error_message
        assert "实际BaseClass" in result.error_message

    def test_check_type_with_none(self):
        """测试检查None类型"""
        validator = ParamValidator()

        # None应该通过None类型检查
        result = validator.check_type(None, type(None))
        assert result.is_valid is True

        # None不应该通过其他类型检查
        result = validator.check_type(None, int)
        assert result.is_valid is False
        assert "期望int" in result.error_message
        assert "实际NoneType" in result.error_message

    def test_check_type_error_message_format(self):
        """测试类型错误消息格式"""
        validator = ParamValidator()

        # 测试错误消息包含正确的类型名称
        result = validator.check_type("hello", int)
        assert result.is_valid is False
        error_msg = result.error_message

        # 检查消息格式
        assert "参数类型错误" in error_msg
        assert "期望int" in error_msg
        assert "实际str" in error_msg
        assert error_msg.startswith("参数类型错误：")

        # 测试自定义类型
        class CustomType:
            pass

        result = validator.check_type(42, CustomType)
        assert result.is_valid is False
        assert "期望CustomType" in result.error_message
        assert "实际int" in result.error_message

    def test_edge_cases(self):
        """测试边界情况"""
        validator = ParamValidator()

        # 空元组
        result = validator.check_count((), min_args=0, max_args=0)
        assert result.is_valid is True

        # 负最小值（不应该发生，但测试处理）
        result = validator.check_count((1, 2), min_args=-1, max_args=5)
        assert result.is_valid is True

        # 相同的最小值和最大值
        result = validator.check_count((1, 2, 3), min_args=3, max_args=3)
        assert result.is_valid is True

        result = validator.check_count((1, 2), min_args=3, max_args=3)
        assert result.is_valid is False
        assert "参数数量不足" in result.error_message

        result = validator.check_count((1, 2, 3, 4), min_args=3, max_args=3)
        assert result.is_valid is False
        assert "参数数量过多" in result.error_message

    def test_combined_validation_scenarios(self):
        """测试组合验证场景"""
        validator = ParamValidator()

        # 场景1：验证函数调用参数
        def example_func(a: int, b: str, c: float = 3.14):
            pass

        # 模拟函数信息
        func_info = {
            "name": "example_func",
            "min_args": 2,
            "max_args": 3,
            "arg_types": [int, str, float],
        }

        # 有效调用：提供所有必需参数
        args = (42, "hello")
        kwargs = {}
        result = validator.validate(func_info, args, kwargs)
        assert result.is_valid is True

        # 有效调用：提供所有参数（包括可选参数）
        args = (42, "hello", 2.71)
        result = validator.validate(func_info, args, kwargs)
        assert result.is_valid is True

        # 无效调用：参数不足
        args = (42,)  # 缺少第二个参数
        result = validator.validate(func_info, args, kwargs)
        # 注意：默认实现总是返回True，所以这里我们直接测试check_count
        count_result = validator.check_count(args, min_args=2, max_args=3)
        assert count_result.is_valid is False

        # 无效调用：参数过多
        args = (42, "hello", 2.71, "extra")
        count_result = validator.check_count(args, min_args=2, max_args=3)
        assert count_result.is_valid is False

    def test_type_checking_with_multiple_values(self):
        """测试多个值的类型检查"""
        validator = ParamValidator()

        # 测试多个值的类型检查
        values = [42, 100, 0, -5]
        for value in values:
            result = validator.check_type(value, int)
            assert result.is_valid is True

        # 混合类型测试
        mixed_values = [42, "hello", 3.14, True, None]
        expected_types = [int, str, float, bool, type(None)]

        for value, expected_type in zip(mixed_values, expected_types):
            result = validator.check_type(value, expected_type)
            assert result.is_valid is True

            # 测试错误类型
            wrong_type = str if expected_type != str else int
            result = validator.check_type(value, wrong_type)
            if type(value) != wrong_type:
                assert result.is_valid is False
