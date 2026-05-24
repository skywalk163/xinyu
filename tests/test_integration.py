# -*- coding: utf-8 -*-
"""集成测试

测试完整的编译流程：词法分析 → 语法分析 → 语义分析 → 代码生成 → 执行
"""
import pytest
import sys
import io
from contextlib import redirect_stdout


# 测试模块不存在，应该失败
def test_main_module_exists():
    """测试主入口模块存在"""
    try:
        from src.main import ChineseProgram
        assert ChineseProgram is not None
    except ImportError:
        pytest.fail("主入口模块 src.main 不存在")


class TestHelloWorld:
    """Hello World 程序测试"""
    
    def test_hello_world(self):
        """测试 Hello World 程序"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '印"你好，世界！"。'
        
        # 捕获输出
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        assert "你好，世界！" in output
    
    def test_hello_world_with_variable(self):
        """测试使用变量的 Hello World"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '''
定 消息 = "你好，世界！"。
印消息。
'''
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        assert "你好，世界！" in output


class TestArithmetic:
    """算术运算测试"""
    
    def test_addition(self):
        """测试加法"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '定 结果 = 3 加 5。印结果。'
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        assert "8" in output
    
    def test_subtraction(self):
        """测试减法"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '定 结果 = 10 减 3。印结果。'
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        assert "7" in output
    
    def test_multiplication(self):
        """测试乘法"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '定 结果 = 4 乘 5。印结果。'
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        assert "20" in output
    
    def test_division(self):
        """测试除法"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '定 结果 = 20 除以 4。印结果。'
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        assert "5" in output
    
    def test_complex_expression(self):
        """测试复杂表达式"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '定 结果 = (2 加 3) 乘 4。印结果。'
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        assert "20" in output


class TestFunction:
    """函数定义和调用测试"""
    
    def test_simple_function(self):
        """测试简单函数"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '''
定 问候 = 函：
    印"你好！"。
问候。
'''
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        assert "你好！" in output
    
    def test_function_with_params(self):
        """测试带参数的函数"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '''
定 问候 = 函 名字：
    定 消息 = "你好，" 加 名字 加 "！"。
    印消息。
问候"世界"。
'''
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        assert "你好，世界！" in output
    
    def test_function_with_return(self):
        """测试带返回值的函数"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '''
定 加法 = 函 甲 乙：
    返回 甲 加 乙。
定 结果 = 加法 3 5。
印结果。
'''
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        assert "8" in output
    
    def test_recursive_function(self):
        """测试递归函数（阶乘）"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '''
定 阶乘 = 函 n：
    若 n 等于 1 则：
        返回 1。
    否则：
        返回 n 乘 阶乘(n 减 1)。
定 结果 = 阶乘 5。
印结果。
'''
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        assert "120" in output


class TestControlFlow:
    """控制流测试"""
    
    def test_if_then(self):
        """测试 if-then"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '''
定 x = 10。
若 x 大于 5 则：
    印"x 大于 5"。
'''
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        assert "x 大于 5" in output
    
    def test_if_then_else(self):
        """测试 if-then-else"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '''
定 x = 3。
若 x 大于 5 则：
    印"x 大于 5"。
否则：
    印"x 小于等于 5"。
'''
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        assert "x 小于等于 5" in output
    
    def test_nested_if(self):
        """测试嵌套 if"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '''
定 x = 10。
若 x 大于 5 则：
    若 x 大于 8 则：
        印"x 大于 8"。
'''
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        assert "x 大于 8" in output


class TestLoop:
    """循环测试"""
    
    def test_for_loop(self):
        """测试遍历循环"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '''
遍历 i 于 [1, 2, 3]：
    印i。
'''
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        assert "1" in output
        assert "2" in output
        assert "3" in output
    
    def test_while_loop(self):
        """测试当循环"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '''
定 n = 1。
当 n 小于等于 3：
    印n。
    n = n 加 1。
'''
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        assert "1" in output
        assert "2" in output
        assert "3" in output
    
    def test_repeat_loop(self):
        """测试重复循环"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '''
重复 3 次：
    印"你好"。
'''
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        assert output.count("你好") == 3


class TestComplexPrograms:
    """复杂程序测试"""
    
    def test_fibonacci(self):
        """测试斐波那契数列"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '''
定 斐波那契 = 函 n：
    若 n 小于等于 1 则：
        返回 n。
    否则：
        返回 斐波那契(n 减 1) 加 斐波那契(n 减 2)。

定 结果 = 斐波那契 10。
印结果。
'''
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        assert "55" in output  # fib(10) = 55
    
    def test_sum_list(self):
        """测试列表求和"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '''
定 数字列表 = [1, 2, 3, 4, 5]。
定 总和 = 0。
遍历 num 于 数字列表：
    总和 = 总和 加 num。
印总和。
'''
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        assert "15" in output
    
    def test_factorial_iterative(self):
        """测试迭代阶乘"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '''
定 阶乘 = 函 n：
    定 结果 = 1。
    定 i = 1。
    当 i 小于等于 n：
        结果 = 结果 乘 i。
        i = i 加 1。
    返回 结果。

定 答案 = 阶乘 5。
印答案。
'''
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        assert "120" in output


class TestCompile:
    """编译功能测试"""
    
    def test_compile_to_python(self):
        """测试编译为 Python 代码"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '定 x = 5。印x。'
        
        python_code = program.compile(source)
        
        assert "x = 5" in python_code
        assert "print(x)" in python_code
    
    def test_compile_function(self):
        """测试编译函数"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '''
定 加法 = 函 a b：
    返回 a 加 b。
'''
        
        python_code = program.compile(source)
        
        assert "def 加法(a, b):" in python_code
        assert "return" in python_code
        assert "a" in python_code
        assert "b" in python_code


class TestErrorHandling:
    """错误处理测试"""
    
    def test_lexer_error(self):
        """测试词法错误"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '定 x = @。'  # @ 是非法字符
        
        result = program.run(source)
        assert result is None or "错误" in str(result)
    
    def test_syntax_error(self):
        """测试语法错误"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '若 则。'  # 缺少条件
        
        result = program.run(source)
        assert result is None or "错误" in str(result)
    
    def test_semantic_error(self):
        """测试语义错误"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '印未定义的变量。'
        
        result = program.run(source)
        # 语义分析应该检测到未定义的变量
        assert result is None or "错误" in str(result)


class TestBuiltinFunctions:
    """内置函数测试"""
    
    def test_print_multiple_args(self):
        """测试 print 多个参数"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '印"你好" "世界" 123。'
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        assert "你好" in output
        assert "世界" in output
        assert "123" in output
    
    def test_boolean_values(self):
        """测试布尔值"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '''
定 a = 真。
定 b = 假。
印a。
印b。
'''
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        assert "True" in output
        assert "False" in output


class TestPythonModules:
    """Python 模块集成测试"""
    
    def test_math_module(self):
        """测试 math 模块"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '''
定 pi = math.pi。
印pi。
'''
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        assert "3.14" in output
    
    def test_random_module(self):
        """测试 random 模块"""
        from src.main import ChineseProgram
        
        program = ChineseProgram()
        source = '''
定 num = random.randint(1, 10)。
印num。
'''
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)
        
        output = captured_output.getvalue()
        # 应该输出一个数字
        assert any(char.isdigit() for char in output)
