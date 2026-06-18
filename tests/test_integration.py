# -*- coding: utf-8 -*-
"""集成测试

测试完整的编译流程：词法分析 → 语法分析 → 语义分析 → 代码生成 → 执行
"""
import io
import sys
from contextlib import redirect_stdout

import pytest


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
        source = '打印"你好，世界！"。'

        # 捕获输出
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "你好，世界！" in output

    def test_hello_world_with_variable(self):
        """测试使用变量的 Hello World"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 消息 = "你好，世界！"。
打印消息。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "你好，世界！" in output


class TestArithmetic:
    """算术运算测试"""

    def test_addition(self):
        """测试相加法"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = "定义 结果 = 3 相加 5。打印结果。"

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "8" in output

    def test_subtraction(self):
        """测试相减法"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = "定义 结果 = 10 相减 3。打印结果。"

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "7" in output

    def test_multiplication(self):
        """测试相乘法"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = "定义 结果 = 4 相乘 5。打印结果。"

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "20" in output

    def test_division(self):
        """测试相除法"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = "定义 结果 = 20 相除以 4。打印结果。"

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "5" in output

    def test_complex_expression(self):
        """测试复杂表达式"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = "定义 结果 = (2 相加 3) 相乘 4。打印结果。"

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "20" in output


class TestFunction:
    """函数定义和调用测试"""

    def test_simple_function(self):
        """测试简单函数"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 问候 = 函数：
    打印"你好！"。
问候。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "你好！" in output

    def test_function_with_params(self):
        """测试带参数的函数"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 问候 = 函数 名字：
    定义 消息 = "你好，" 相加 名字 相加 "！"。
    打印消息。
问候"世界"。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "你好，世界！" in output

    def test_function_with_return(self):
        """测试带返回值的函数"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 相加法 = 函数 甲 乙：
    返回 甲 相加 乙。
定义 结果 = 相加法 3 5。
打印结果。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "8" in output

    def test_recursive_function(self):
        """测试递归函数（阶相乘）"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 阶相乘 = 函数 n：
    如果 n 等于 1 那么：
        返回 1。
    否则：
        返回 n 相乘 阶相乘 n 相减 1。
定义 结果 = 阶相乘 5。
打印 结果。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "120" in output


class TestControlFlow:
    """控制流测试"""

    def test_if_then(self):
        """测试 if-then"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 x = 10。
如果 x 大于 5 那么：
    打印"x 大于 5"。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "x 大于 5" in output

    def test_if_then_else(self):
        """测试 if-then-else"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 x = 3。
如果 x 大于 5 那么：
    打印"x 大于 5"。
否则：
    打印"x 小于等于 5"。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "x 小于等于 5" in output

    def test_nested_if(self):
        """测试嵌套 if"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 x = 10。
如果 x 大于 5 那么：
    如果 x 大于 8 那么：
        打印"x 大于 8"。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "x 大于 8" in output


class TestLoop:
    """循环测试"""

    def test_for_loop(self):
        """测试遍历循环"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
循环 i 于 [1, 2, 3]：
    打印 i。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "1" in output
        assert "2" in output
        assert "3" in output

    def test_while_loop(self):
        """测试当满足循环"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 n = 1。
当满足 n 小于等于 3：
    打印 n。
    n = n 相加 1。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "1" in output
        assert "2" in output
        assert "3" in output

    def test_repeat_loop(self):
        """测试重复循环"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
重复 3 次数：
    打印"你好"。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert output.count("你好") == 3


class TestComplexPrograms:
    """复杂程序测试"""

    def test_fibonacci(self):
        """测试斐波那契数列"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 斐波那契 = 函数 n：
    如果 n 小于等于 1 那么：
        返回 n。
    否则：
        返回 斐波那契 n 相减 1 相加 斐波那契 n 相减 2。

定义 结果 = 斐波那契 7。
打印 结果。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "13" in output  # fib(7) = 13

    def test_sum_list(self):
        """测试列表求和"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 数字列表 = [1, 2, 3, 4, 5]。
定义 总和 = 0。
循环 num 于 数字列表：
    总和 = 总和 相加 num。
打印总和。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "15" in output

    def test_factorial_iterative(self):
        """测试迭代阶相乘"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 阶相乘 = 函数 n：
    定义 结果 = 1。
    定义 i = 1。
    当满足 i 小于等于 n：
        结果 = 结果 相乘 i。
        i = i 相加 1。
    返回 结果。

定义 答案 = 阶相乘 5。
打印答案。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "120" in output


class TestCompile:
    """编译功能测试"""

    def test_compile_to_python(self):
        """测试编译为 Python 代码"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = "定义 x = 5。打印x。"

        python_code = program.compile(source)

        assert "x = 5" in python_code
        assert "print(x)" in python_code

    def test_compile_function(self):
        """测试编译函数"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 相加法 = 函数 a b：
    返回 a 相加 b。
"""

        python_code = program.compile(source)

        assert "def 相加法(a, b):" in python_code
        assert "return" in python_code
        assert "a" in python_code
        assert "b" in python_code


class TestErrorHandling:
    """错误处理测试"""

    def test_lexer_error(self):
        """测试词法错误"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = "定义 x = @。"  # @ 是非也也法字符

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert result is None
        assert "词法错误" in output or "错误" in output

    def test_syntax_error(self):
        """测试语法错误"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = "如果 则。"  # 缺少条件

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert result is None
        assert "语法错误" in output or "错误" in output

    def test_semantic_error(self):
        """测试语义错误"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = "打印未定义的变量。"

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        # 语义分析应该检测到未定义的变量
        assert result is None
        assert "语义错误" in output or "错误" in output


class TestBuiltinFunctions:
    """内置函数测试"""

    def test_print_multiple_args(self):
        """测试 print 多个参数"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = '打印"你好" "世界" 123。'

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "你好" in output
        assert "世界" in output
        assert "123" in output

    def test_boolean_values(self):
        """测试布尔值"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 a = 真值。
定义 b = 假值。
打印a。
打印b。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "True" in output
        assert "False" in output


class TestPythonModules:
    """Python 模块集成测试"""

    def test_math_module(self):
        """测试 math 模块"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 pi = math.pi。
打印pi。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        assert "3.14" in output

    def test_random_module(self):
        """测试 random 模块"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
定义 num = random.randint(1, 10)。
打印num。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
    _ = source)  # 未使用变量

        output = captured_output.getvalue()
        # 应该输出一个数字
        assert any(char.isdigit() for char in output)
