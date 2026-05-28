"""用户定义函数元数推断测试

测试用户定义函数的元数自动推断功能。
"""

import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.parser.ast_nodes import (
    FunctionDefNode, FunctionCallNode, VarDefNode
)


class TestUserDefinedFunctionArity:
    """用户定义函数元数推断测试"""

    def test_single_param_function(self):
        """测试单参数函数"""
        source = """
定义 平方 = 函 x：
  返回 x 相乘 x。
。
平方 5。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        # 检查变量定义（值为函数定义）
        var_def = ast.statements[0]
        assert isinstance(var_def, VarDefNode)
        assert var_def.name == "平方"
        assert isinstance(var_def.value, FunctionDefNode)
        assert len(var_def.value.params) == 1
        
        # 检查函数调用
        func_call = ast.statements[1]
        assert isinstance(func_call, FunctionCallNode)
        assert func_call.name == "平方"
        assert len(func_call.args) == 1

    def test_function_registered_in_verb_registry(self):
        """测试函数注册到动词注册表"""
        source = """
定义 自定义函数 = 函 a b c：
  返回 a 相加 b 相加 c。
。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        # 检查函数已注册
        assert parser.verb_registry.is_registered("自定义函数")
        assert parser.verb_registry.is_function("自定义函数")
        
        # 检查元数
        arity = parser.verb_registry.get("自定义函数")
        assert arity is not None
        assert arity.count == 3

    def test_no_param_function(self):
        """测试无参数函数"""
        source = """
定义 常量 = 函：
  返回 42。
。
"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        # 检查变量定义
        var_def = ast.statements[0]
        assert isinstance(var_def, VarDefNode)
        assert var_def.name == "常量"
        assert isinstance(var_def.value, FunctionDefNode)
        assert len(var_def.value.params) == 0
        
        # 检查元数为0
        arity = parser.verb_registry.get("常量")
        assert arity is not None
        assert arity.count == 0
