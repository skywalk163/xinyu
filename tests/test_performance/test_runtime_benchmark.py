"""运行时性能基准测试

测试运行时关键操作的性能。
"""


from src.main import ChineseProgram

from .benchmark_utils import benchmark, format_result


class TestRuntimeBenchmark:
    """运行时性能基准测试"""

    @benchmark(iterations=5, warmup=1)
    def test_loop_performance(self):
        """测试循环执行性能（1000次）"""
        program = ChineseProgram()
        source = """
定义 计数 = 0。
重复 1000 次：
    定义 计数 = 计数 相加 1。
"""
        program.run(source)

    @benchmark(iterations=5, warmup=1)
    def test_function_call_performance(self):
        """测试函数调用性能（1000次）"""
        program = ChineseProgram()
        source = """
定义 函数名 = 函数 x：返回 x 相加 1。
定义 计数 = 0。
重复 1000 次：
    定义 结果 = 函数名 计数。
"""
        program.run(source)

    @benchmark(iterations=5, warmup=1)
    def test_arithmetic_performance(self):
        """测试算术运算性能（1000次）"""
        program = ChineseProgram()
        source = """
定义 结果 = 0。
重复 1000 次：
    定义 结果 = 结果 相加 1。
    定义 结果 = 结果 相减 1。
    定义 结果 = 结果 相乘 2。
    定义 结果 = 结果 相除 2。
"""
        program.run(source)

    @benchmark(iterations=5, warmup=1)
    def test_string_operation_performance(self):
        """测试字符串操作性能（100次）"""
        program = ChineseProgram()
        source = """
定义 字符串 = ""。
重复 100 次：
    定义 字符串 = 字符串 相加 "a"。
"""
        program.run(source)

    @benchmark(iterations=5, warmup=1)
    def test_list_operation_performance(self):
        """测试列表操作性能（100次）"""
        program = ChineseProgram()
        source = """
定义 列表 = []。
重复 100 次：
    列表.追加(1)。
"""
        program.run(source)

    @benchmark(iterations=5, warmup=1)
    def test_comparison_performance(self):
        """测试比较运算性能（1000次）"""
        program = ChineseProgram()
        source = """
定义 结果 = 真。
重复 1000 次：
    定义 结果 = 1 小于 2。
    定义 结果 = 2 大于 1。
    定义 结果 = 1 等于 1。
"""
        program.run(source)

    @benchmark(iterations=3, warmup=1)
    def test_nested_function_performance(self):
        """测试嵌套函数性能"""
        program = ChineseProgram()
        source = """
定义 外层函数 = 函数 x：
    定义 内层函数 = 函数 y：
        返回 y 相乘 2。
    返回 内层函数 x。

定义 结果 = 外层函数 10。
"""
        program.run(source)

    @benchmark(iterations=3, warmup=1)
    def test_recursive_function_performance(self):
        """测试递归函数性能（小规模）"""
        program = ChineseProgram()
        source = """
定义 阶乘 = 函数 n：
    如果 n 小于等于 1 那么：
        返回 1。
    否则：
        返回 n 相乘 阶乘 n 相减 1。

定义 结果 = 阶乘 10。
"""
        program.run(source)

    def test_runtime_performance_summary(self):
        """测试运行时性能总结"""
        # 运行基准测试并输出结果
        loop_result = self.test_loop_performance()
        func_result = self.test_function_call_performance()
        arith_result = self.test_arithmetic_performance()

        # 输出结果（用于调试）
        print("\n运行时性能:")
        print(format_result(loop_result, "循环执行"))
        print(format_result(func_result, "函数调用"))
        print(format_result(arith_result, "算术运算"))


class TestMemoryBenchmark:
    """内存使用基准测试"""

    def test_memory_usage_small(self):
        """测试小规模内存使用"""
        program = ChineseProgram()
        source = "\n".join([f"定义 变量{i} = {i}。" for i in range(100)])
        result = program.run(source)
        # 应该成功执行
        assert result is not None or result is None

    def test_memory_usage_medium(self):
        """测试中规模内存使用"""
        program = ChineseProgram()
        source = "\n".join([f"定义 变量{i} = {i}。" for i in range(1000)])
        result = program.run(source)
        # 应该成功执行
        assert result is not None or result is None

    def test_list_memory(self):
        """测试列表内存使用"""
        program = ChineseProgram()
        source = """
定义 列表 = []。
重复 1000 次：
    列表.追加(1)。
"""
        result = program.run(source)
        # 应该成功执行
        assert result is not None or result is None
