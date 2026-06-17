"""异常系统测试

测试src/runtime/exception_system.py模块的功能。
"""

import pytest
from src.runtime.exception_system import (
    XinyuExceptionType,
    XinyuException,
    TryBlock,
    xinyu_try,
    xinyu_except,
    xinyu_throw
)


class TestXinyuExceptionType:
    """测试XinyuExceptionType枚举"""
    
    def test_exception_type_values(self):
        """测试异常类型值"""
        assert XinyuExceptionType.语法错误.value == "SyntaxError"
        assert XinyuExceptionType.运行时错误.value == "RuntimeError"
        assert XinyuExceptionType.类型错误.value == "TypeError"
        assert XinyuExceptionType.值错误.value == "ValueError"
        assert XinyuExceptionType.索引错误.value == "IndexError"
        assert XinyuExceptionType.键错误.value == "KeyError"
        assert XinyuExceptionType.除零错误.value == "ZeroDivisionError"
        assert XinyuExceptionType.文件错误.value == "FileError"
        assert XinyuExceptionType.导入错误.value == "ImportError"
        assert XinyuExceptionType.自定义错误.value == "CustomError"
    
    def test_exception_type_names(self):
        """测试异常类型名称"""
        assert XinyuExceptionType.语法错误.name == "语法错误"
        assert XinyuExceptionType.运行时错误.name == "运行时错误"
        assert XinyuExceptionType.类型错误.name == "类型错误"
        assert XinyuExceptionType.值错误.name == "值错误"
        assert XinyuExceptionType.索引错误.name == "索引错误"
        assert XinyuExceptionType.键错误.name == "键错误"
        assert XinyuExceptionType.除零错误.name == "除零错误"
        assert XinyuExceptionType.文件错误.name == "文件错误"
        assert XinyuExceptionType.导入错误.name == "导入错误"
        assert XinyuExceptionType.自定义错误.name == "自定义错误"


class TestXinyuException:
    """测试XinyuException类"""
    
    def test_exception_creation(self):
        """测试异常创建"""
        # 基本异常
        exc = XinyuException("测试错误")
        assert exc.message == "测试错误"
        assert exc.exception_type == XinyuExceptionType.自定义错误
        assert exc.line is None
        assert exc.column is None
        assert exc.suggestion is None
        assert str(exc) == "CustomError: 测试错误"
        
        # 带位置信息的异常
        exc = XinyuException("语法错误", XinyuExceptionType.语法错误, line=10, column=5)
        assert exc.message == "语法错误"
        assert exc.exception_type == XinyuExceptionType.语法错误
        assert exc.line == 10
        assert exc.column == 5
        assert str(exc) == "SyntaxError: 语法错误 (行 10, 列 5)"
        
        # 带建议的异常
        exc = XinyuException("类型错误", XinyuExceptionType.类型错误, suggestion="请检查变量类型")
        assert exc.message == "类型错误"
        assert exc.exception_type == XinyuExceptionType.类型错误
        assert exc.suggestion == "请检查变量类型"
        assert str(exc) == "TypeError: 类型错误\n  建议: 请检查变量类型"
        
        # 完整异常
        exc = XinyuException("运行时错误", XinyuExceptionType.运行时错误, line=20, column=15, suggestion="请检查变量值")
        assert exc.message == "运行时错误"
        assert exc.exception_type == XinyuExceptionType.运行时错误
        assert exc.line == 20
        assert exc.column == 15
        assert exc.suggestion == "请检查变量值"
        assert str(exc) == "RuntimeError: 运行时错误 (行 20, 列 15)\n  建议: 请检查变量值"
    
    def test_exception_inheritance(self):
        """测试异常继承关系"""
        exc = XinyuException("测试")
        assert isinstance(exc, Exception)
        assert isinstance(exc, XinyuException)
        
        # 检查异常类型
        assert exc.exception_type == XinyuExceptionType.自定义错误


class TestTryBlock:
    """测试TryBlock类"""
    
    def test_try_block_initialization(self):
        """测试TryBlock初始化"""
        block = TryBlock()
        assert block.try_code is None
        assert block.except_handlers == {}
        assert block.finally_code is None
        assert block.else_code is None
    
    def test_set_try(self):
        """测试设置try代码"""
        block = TryBlock()
        
        def test_func():
            return "test"
        
        block.set_try(test_func)
        assert block.try_code == test_func
    
    def test_add_except(self):
        """测试添加异常处理器"""
        block = TryBlock()
        
        def handler(e):
            return "handled"
        
        block.add_except("ValueError", handler)
        assert "ValueError" in block.except_handlers
        assert block.except_handlers["ValueError"] == handler
        
        # 添加多个处理器
        def handler2(e):
            return "handled2"
        
        block.add_except("TypeError", handler2)
        assert "TypeError" in block.except_handlers
        assert block.except_handlers["TypeError"] == handler2
    
    def test_set_finally(self):
        """测试设置finally代码"""
        block = TryBlock()
        
        def finally_func():
            return "finally"
        
        block.set_finally(finally_func)
        assert block.finally_code == finally_func
    
    def test_set_else(self):
        """测试设置else代码"""
        block = TryBlock()
        
        def else_func():
            return "else"
        
        block.set_else(else_func)
        assert block.else_code == else_func
    
    def test_execute_no_exception(self):
        """测试执行无异常的try块"""
        block = TryBlock()
        
        def try_code():
            return "success"
        
        def else_code():
            return "no exception"
        
        def finally_code():
            return "always"
        
        block.set_try(try_code)
        block.set_else(else_code)
        
        # 测试finally代码
        finally_called = []
        def finally_test():
            finally_called.append(True)
        
        block.set_finally(finally_test)
        
        result = block.execute()
        assert result == "no exception"  # else代码的结果
        assert finally_called == [True]  # finally代码被调用
    
    def test_execute_with_exception_caught(self):
        """测试执行有异常但被捕获的try块"""
        block = TryBlock()
        
        def try_code():
            raise XinyuException("测试错误", XinyuExceptionType.值错误)
        
        def except_handler(e):
            return f"捕获到: {e.message}"
        
        def finally_code():
            return "finally executed"
        
        block.set_try(try_code)
        block.add_except("ValueError", except_handler)
        
        finally_called = []
        def finally_test():
            finally_called.append(True)
        
        block.set_finally(finally_test)
        
        result = block.execute()
        assert result == "捕获到: 测试错误"
        assert finally_called == [True]
    
    def test_execute_with_exception_uncaught(self):
        """测试执行有异常但未捕获的try块"""
        block = TryBlock()
        
        def try_code():
            raise XinyuException("测试错误", XinyuExceptionType.值错误)
        
        def except_handler(e):
            return "不会执行"
        
        block.set_try(try_code)
        block.add_except("TypeError", except_handler)  # 错误的异常类型
        
        with pytest.raises(XinyuException) as exc_info:
            block.execute()
        
        assert exc_info.value.message == "测试错误"
        assert exc_info.value.exception_type == XinyuExceptionType.值错误
    
    def test_execute_with_python_exception(self):
        """测试执行Python异常"""
        block = TryBlock()
        
        def try_code():
            raise ValueError("Python错误")
        
        def except_handler(e):
            return f"Python异常: {str(e)}"
        
        block.set_try(try_code)
        block.add_except("ValueError", except_handler)
        
        result = block.execute()
        assert result == "Python异常: Python错误"
    
    def test_execute_catch_all_exception(self):
        """测试捕获所有异常"""
        block = TryBlock()
        
        def try_code():
            raise XinyuException("任意错误", XinyuExceptionType.自定义错误)
        
        def except_handler(e):
            return "捕获所有异常"
        
        block.set_try(try_code)
        block.add_except("所有", except_handler)
        
        result = block.execute()
        assert result == "捕获所有异常"
        
        # 测试"异常"关键字
        block2 = TryBlock()
        block2.set_try(try_code)
        block2.add_except("异常", except_handler)
        
        result2 = block2.execute()
        assert result2 == "捕获所有异常"
    
    def test_execute_without_try_code(self):
        """测试执行没有try代码的块"""
        block = TryBlock()
        
        # 没有设置try代码，应该返回None
        result = block.execute()
        assert result is None


class TestXinyuTryExcept:
    """测试xinyu_try和xinyu_except函数"""
    
    def test_xinyu_try_decorator(self):
        """测试xinyu_try装饰器"""
        def try_code():
            return "test"
        
        block = xinyu_try(try_code)
        assert isinstance(block, TryBlock)
        assert block.try_code == try_code
    
    def test_xinyu_except_decorator(self):
        """测试xinyu_except装饰器"""
        block = TryBlock()
        
        @xinyu_except(block, "ValueError")
        def handler(e):
            return "handled"
        
        # 检查处理器已添加
        assert "ValueError" in block.except_handlers
        assert block.except_handlers["ValueError"] == handler
        
        # 测试处理器函数
        exc = XinyuException("测试", XinyuExceptionType.值错误)
        result = handler(exc)
        assert result == "handled"
    
    def test_xinyu_try_except_chain(self):
        """测试xinyu_try和xinyu_except链式使用"""
        block = xinyu_try(lambda: 1 / 0)
        
        @xinyu_except(block, "ZeroDivisionError")
        def handle_zero_div(e):
            return "除零错误已处理"
        
        result = block.execute()
        assert result == "除零错误已处理"


class TestXinyuThrow:
    """测试xinyu_throw函数"""
    
    def test_xinyu_throw_basic(self):
        """测试基本抛出异常"""
        with pytest.raises(XinyuException) as exc_info:
            xinyu_throw("测试错误")
        
        exc = exc_info.value
        assert exc.message == "测试错误"
        assert exc.exception_type == XinyuExceptionType.自定义错误
    
    def test_xinyu_throw_with_type(self):
        """测试带类型的抛出异常"""
        with pytest.raises(XinyuException) as exc_info:
            xinyu_throw("语法错误", XinyuExceptionType.语法错误)
        
        exc = exc_info.value
        assert exc.message == "语法错误"
        assert exc.exception_type == XinyuExceptionType.语法错误
    
    def test_xinyu_throw_in_try_block(self):
        """测试在try块中抛出异常"""
        block = TryBlock()
        
        def try_code():
            xinyu_throw("测试错误", XinyuExceptionType.值错误)
        
        def except_handler(e):
            return f"捕获: {e.message}"
        
        block.set_try(try_code)
        block.add_except("ValueError", except_handler)
        
        result = block.execute()
        assert result == "捕获: 测试错误"


class TestExceptionSystemIntegration:
    """测试异常系统集成"""
    
    def test_complete_try_except_finally(self):
        """测试完整的try-except-finally流程"""
        events = []
        
        block = TryBlock()
        
        def try_code():
            events.append("try")
            return "try_result"
        
        def except_handler(e):
            events.append("except")
            return "except_result"
        
        def else_code():
            events.append("else")
            return "else_result"
        
        def finally_code():
            events.append("finally")
        
        block.set_try(try_code)
        block.add_except("Exception", except_handler)
        block.set_else(else_code)
        block.set_finally(finally_code)
        
        result = block.execute()
        
        assert events == ["try", "else", "finally"]
        assert result == "else_result"
    
    def test_complete_try_except_finally_with_exception(self):
        """测试有异常的完整流程"""
        events = []
        
        block = TryBlock()
        
        def try_code():
            events.append("try")
            raise ValueError("测试错误")
        
        def except_handler(e):
            events.append("except")
            return "except_result"
        
        def else_code():
            events.append("else")  # 不应该执行
            return "else_result"
        
        def finally_code():
            events.append("finally")
        
        block.set_try(try_code)
        block.add_except("ValueError", except_handler)
        block.set_else(else_code)
        block.set_finally(finally_code)
        
        result = block.execute()
        
        assert events == ["try", "except", "finally"]
        assert result == "except_result"


if __name__ == "__main__":
    # 运行测试
    import sys
    sys.exit(pytest.main([__file__, "-v"]))