"""函数元数表测试

测试src/parser/function_arity.py模块的功能。
"""

import pytest
from src.parser.function_arity import (
    FunctionArity,
    ArityType,
    get_arity,
    is_fixed_arity,
    get_expected_args,
    register_function,
    FUNCTION_ARITY_TABLE
)


class TestFunctionArityClass:
    """测试FunctionArity类"""
    
    def test_function_arity_creation(self):
        """测试FunctionArity对象创建"""
        # 测试固定元数
        arity = FunctionArity("相加", ArityType.FIXED, 2, 2, "加法")
        assert arity.name == "相加"
        assert arity.arity_type == ArityType.FIXED
        assert arity.min_args == 2
        assert arity.max_args == 2
        assert arity.description == "加法"
        assert arity.arity == 2
        
        # 测试可变元数
        arity = FunctionArity("打印", ArityType.VARIABLE, 0, None, "打印任意数量参数")
        assert arity.name == "打印"
        assert arity.arity_type == ArityType.VARIABLE
        assert arity.min_args == 0
        assert arity.max_args is None
        assert arity.description == "打印任意数量参数"
        assert arity.arity == "可变"
        
        # 测试未知元数
        arity = FunctionArity("未知函数", ArityType.UNKNOWN, 0, None, "未知函数")
        assert arity.name == "未知函数"
        assert arity.arity_type == ArityType.UNKNOWN
        assert arity.arity == "未知"
    
    def test_function_arity_repr(self):
        """测试FunctionArity的字符串表示"""
        arity = FunctionArity("相加", ArityType.FIXED, 2, 2, "加法")
        repr_str = repr(arity)
        assert "FunctionArity" in repr_str
        assert "相加" in repr_str
        assert "2" in repr_str


class TestFunctionArityTable:
    """测试函数元数表"""
    
    def test_builtin_functions_in_table(self):
        """测试内置函数是否在表中"""
        # 测试一些关键内置函数
        assert "打印" in FUNCTION_ARITY_TABLE
        assert "相加" in FUNCTION_ARITY_TABLE
        assert "平方根" in FUNCTION_ARITY_TABLE
        assert "长度" in FUNCTION_ARITY_TABLE
        assert "范围" in FUNCTION_ARITY_TABLE
        
        # 检查元数类型
        assert FUNCTION_ARITY_TABLE["打印"].arity_type == ArityType.VARIABLE
        assert FUNCTION_ARITY_TABLE["相加"].arity_type == ArityType.FIXED
        assert FUNCTION_ARITY_TABLE["范围"].arity_type == ArityType.VARIABLE
    
    def test_operator_functions_in_table(self):
        """测试操作符函数是否在表中"""
        assert "相加" in FUNCTION_ARITY_TABLE
        assert "相减" in FUNCTION_ARITY_TABLE
        assert "相乘" in FUNCTION_ARITY_TABLE
        assert "相除" in FUNCTION_ARITY_TABLE
        assert "取余" in FUNCTION_ARITY_TABLE
        
        # 检查都是固定元数
        assert FUNCTION_ARITY_TABLE["相加"].arity_type == ArityType.FIXED
        assert FUNCTION_ARITY_TABLE["相加"].min_args == 2
        assert FUNCTION_ARITY_TABLE["相加"].max_args == 2
    
    def test_comparison_functions_in_table(self):
        """测试比较函数是否在表中"""
        assert "等于" in FUNCTION_ARITY_TABLE
        assert "不等" in FUNCTION_ARITY_TABLE
        assert "大于" in FUNCTION_ARITY_TABLE
        assert "小于" in FUNCTION_ARITY_TABLE
        assert "大等" in FUNCTION_ARITY_TABLE
        assert "小等" in FUNCTION_ARITY_TABLE
        
        # 检查都是固定元数
        for func_name in ["等于", "不等", "大于", "小于", "大等", "小等"]:
            arity = FUNCTION_ARITY_TABLE[func_name]
            assert arity.arity_type == ArityType.FIXED
            assert arity.min_args == 2
            assert arity.max_args == 2
    
    def test_logical_functions_in_table(self):
        """测试逻辑函数是否在表中"""
        assert "并且" in FUNCTION_ARITY_TABLE
        assert "或者" in FUNCTION_ARITY_TABLE
        assert "非也" in FUNCTION_ARITY_TABLE
        
        # 检查元数
        assert FUNCTION_ARITY_TABLE["并且"].min_args == 2
        assert FUNCTION_ARITY_TABLE["并且"].max_args == 2
        assert FUNCTION_ARITY_TABLE["或者"].min_args == 2
        assert FUNCTION_ARITY_TABLE["或者"].max_args == 2
        assert FUNCTION_ARITY_TABLE["非也"].min_args == 1
        assert FUNCTION_ARITY_TABLE["非也"].max_args == 1


class TestFunctionArityFunctions:
    """测试函数元数相关函数"""
    
    def test_get_arity(self):
        """测试获取函数元数"""
        # 测试存在的函数
        arity = get_arity("打印")
        assert arity is not None
        assert arity.name == "打印"
        assert arity.arity_type == ArityType.VARIABLE
        
        arity = get_arity("相加")
        assert arity is not None
        assert arity.name == "相加"
        assert arity.arity_type == ArityType.FIXED
        
        # 测试不存在的函数
        arity = get_arity("不存在的函数")
        assert arity is None
    
    def test_is_fixed_arity(self):
        """测试检查是否是固定元数"""
        # 固定元数函数
        assert is_fixed_arity("相加") is True
        assert is_fixed_arity("平方根") is True
        assert is_fixed_arity("长度") is True
        
        # 可变元数函数
        assert is_fixed_arity("打印") is False
        assert is_fixed_arity("范围") is False
        
        # 不存在的函数
        assert is_fixed_arity("不存在的函数") is False
    
    def test_get_expected_args(self):
        """测试获取期望参数数量"""
        # 固定元数函数
        assert get_expected_args("相加") == 2
        assert get_expected_args("平方根") == 1
        assert get_expected_args("非也") == 1
        
        # 可变元数函数
        assert get_expected_args("打印") is None
        assert get_expected_args("范围") is None
        
        # 不存在的函数
        assert get_expected_args("不存在的函数") is None
    
    def test_register_function(self):
        """测试注册新函数"""
        # 注册前不存在
        assert get_arity("自定义函数") is None
        
        # 注册新函数
        register_function("自定义函数", ArityType.FIXED, 3, 3, "自定义函数")
        
        # 注册后存在
        arity = get_arity("自定义函数")
        assert arity is not None
        assert arity.name == "自定义函数"
        assert arity.arity_type == ArityType.FIXED
        assert arity.min_args == 3
        assert arity.max_args == 3
        assert arity.description == "自定义函数"
        
        # 清理：从表中删除测试函数
        del FUNCTION_ARITY_TABLE["自定义函数"]
    
    def test_register_variable_function(self):
        """测试注册可变元数函数"""
        # 注册可变元数函数
        register_function("可变函数", ArityType.VARIABLE, 1, None, "可变参数函数")
        
        arity = get_arity("可变函数")
        assert arity is not None
        assert arity.arity_type == ArityType.VARIABLE
        assert arity.min_args == 1
        assert arity.max_args is None
        assert arity.arity == "可变"
        
        # 清理
        del FUNCTION_ARITY_TABLE["可变函数"]
    
    def test_arity_table_consistency(self):
        """测试元数表的一致性"""
        for name, arity in FUNCTION_ARITY_TABLE.items():
            # 检查名称一致性
            assert arity.name == name
            
            # 检查元数类型有效性
            assert arity.arity_type in [ArityType.FIXED, ArityType.VARIABLE, ArityType.UNKNOWN]
            
            # 检查参数数量有效性
            assert arity.min_args >= 0
            if arity.max_args is not None:
                assert arity.max_args >= arity.min_args
            
            # 检查arity属性
            if arity.arity_type == ArityType.FIXED:
                assert isinstance(arity.arity, int)
                assert arity.arity == arity.min_args
            elif arity.arity_type == ArityType.VARIABLE:
                assert arity.arity == "可变"
            else:
                assert arity.arity == "未知"


if __name__ == "__main__":
    # 运行测试
    import sys
    sys.exit(pytest.main([__file__, "-v"]))