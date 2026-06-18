#!/usr/bin/env python3
"""
测试基准测试框架
"""

import math
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.benchmark import BenchmarkReporter, BenchmarkRunner, PerformanceProfiler
from src.benchmark.utils import (
    benchmark_decorator,
    calculate_statistics,
    create_benchmark_suite,
    format_memory,
    format_percentage,
    format_time,
    human_readable_time,
    profile_decorator,
)


def fibonacci_recursive(n: int) -> int:
    """递归计算斐波那契数列（性能较差）"""
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_iterative(n: int) -> int:
    """迭代计算斐波那契数列（性能较好）"""
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def fibonacci_memoization(n: int, memo=None) -> int:
    """使用记忆化计算斐波那契数列"""
    if memo is None:
        memo = {}

    if n in memo:
        return memo[n]

    if n <= 1:
        result = n
    else:
        result = fibonacci_memoization(n - 1, memo) + fibonacci_memoization(n - 2, memo)

    memo[n] = result
    return result


def bubble_sort(arr: list) -> list:
    """冒泡排序"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def quick_sort(arr: list) -> list:
    """快速排序"""
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


def matrix_multiplication(n: int) -> list:
    """矩阵乘法"""
    # 创建两个 n x n 矩阵
    A = [[random.random() for _ in range(n)] for _ in range(n)]
    B = [[random.random() for _ in range(n)] for _ in range(n)]
    C = [[0 for _ in range(n)] for _ in range(n)]

    # 矩阵乘法
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]

    return C


def string_concatenation(n: int) -> str:
    """字符串拼接"""
    result = ""
    for i in range(n):
        result += f"string_{i}"
    return result


def list_comprehension(n: int) -> list:
    """列表推导式"""
    return [i * i for i in range(n)]


def generator_expression(n: int) -> list:
    """生成器表达式"""
    return list(i * i for i in range(n))


@benchmark_decorator(warmup_iterations=2, test_iterations=5)
def test_fibonacci_recursive():
    """测试递归斐波那契"""
    import sys

    sys.setrecursionlimit(2000)  # 增加递归深度限制
    return fibonacci_recursive(20)


@benchmark_decorator(warmup_iterations=2, test_iterations=5)
def test_fibonacci_iterative():
    """测试迭代斐波那契"""
    return fibonacci_iterative(1000)


@benchmark_decorator(warmup_iterations=2, test_iterations=5)
def test_fibonacci_memoization():
    """测试记忆化斐波那契"""
    import sys

    sys.setrecursionlimit(2000)  # 增加递归深度限制
    return fibonacci_memoization(100)


@profile_decorator(sort_by="time", limit=10)
def test_performance_profiler():
    """测试性能分析器"""
    # 运行一些操作进行性能分析
    result = []
    for i in range(1000):
        result.append(math.sqrt(i))

    arr = [random.randint(1, 1000) for _ in range(1000)]
    sorted_arr = quick_sort(arr.copy())

    matrix = matrix_multiplication(50)

    return result, sorted_arr, matrix


@create_benchmark_suite("算法性能测试套件")
class AlgorithmBenchmarks:
    """算法基准测试套件"""

    def benchmark_bubble_sort(self):
        """冒泡排序基准测试"""
        arr = [random.randint(1, 1000) for _ in range(500)]
        return bubble_sort(arr)

    def benchmark_quick_sort(self):
        """快速排序基准测试"""
        arr = [random.randint(1, 1000) for _ in range(500)]
        return quick_sort(arr)

    def benchmark_matrix_multiplication_small(self):
        """小矩阵乘法基准测试"""
        return matrix_multiplication(20)

    def benchmark_matrix_multiplication_medium(self):
        """中矩阵乘法基准测试"""
        return matrix_multiplication(50)

    def benchmark_string_concatenation(self):
        """字符串拼接基准测试"""
        return string_concatenation(1000)

    def benchmark_list_comprehension(self):
        """列表推导式基准测试"""
        return list_comprehension(10000)

    def benchmark_generator_expression(self):
        """生成器表达式基准测试"""
        return generator_expression(10000)


def test_benchmark_runner():
    """测试基准测试运行器"""
    print("=" * 80)
    print("测试基准测试运行器")
    print("=" * 80)

    # 创建基准测试运行器
    runner = BenchmarkRunner(
        warmup_iterations=2,
        test_iterations=5,
        enable_gc=True,
        collect_cpu=True,
        collect_memory=True,
    )

    # 运行单个基准测试
    print("\n1. 运行单个基准测试:")
    result = runner.run_benchmark(fibonacci_iterative, "斐波那契迭代", 1000)
    print(result.summary())

    # 运行基准测试套件
    print("\n2. 运行基准测试套件:")
    benchmarks = [
        (fibonacci_recursive, "斐波那契递归", (20,), {}),
        (fibonacci_iterative, "斐波那契迭代", (1000,), {}),
        (fibonacci_memoization, "斐波那契记忆化", (100,), {}),  # 减少n值避免递归深度问题
        (bubble_sort, "冒泡排序", ([random.randint(1, 1000) for _ in range(500)],), {}),
        (quick_sort, "快速排序", ([random.randint(1, 1000) for _ in range(500)],), {}),
    ]

    results = runner.run_benchmark_suite(benchmarks, "算法性能测试")

    # 生成报告
    print("\n3. 生成报告:")
    reporter = BenchmarkReporter()
    filepaths = reporter.save_report(results, "算法性能基准测试", formats=["txt", "html", "json"])

    print(f"文本报告已保存到: {filepaths.get('txt', 'N/A')}")
    print(f"HTML报告已保存到: {filepaths.get('html', 'N/A')}")
    print(f"JSON报告已保存到: {filepaths.get('json', 'N/A')}")

    # 比较结果
    if len(results) >= 2:
        print("\n4. 比较结果:")
        comparison = runner.compare_results(results[0], results[1], "time_mean")
        print(f"比较 {results[0].name} 和 {results[1].name}:")
        print(f"  指标: {comparison['metric']}")
        print(f"  值1: {comparison['value1']:.6f}")
        print(f"  值2: {comparison['value2']:.6f}")
        print(f"  差异: {comparison['difference']:.6f}")
        print(f"  百分比: {comparison['percentage']:.2f}%")
        print(f"  更快: {comparison['faster']}")

    return results


def test_performance_profiler_demo():
    """测试性能分析器演示"""
    print("\n" + "=" * 80)
    print("测试性能分析器")
    print("=" * 80)

    profiler = PerformanceProfiler(sort_by="cumulative", limit=10)

    # 分析单个函数
    print("\n分析单个函数性能:")
    result = profiler.profile_function(fibonacci_recursive, 20)
    print(f"函数: {result.function_name}")
    print(f"总时间: {result.total_time:.6f}s")
    print(f"总调用次数: {result.total_calls}")
    print(f"内存分配: {result.memory_allocated / 1024:.2f}KB")

    # 生成报告
    print("\n性能分析报告:")
    report = profiler.generate_report()
    print(report)

    # 保存报告
    profiler.save_report("performance_profile.txt")
    profiler.save_json_report("performance_profile.json")
    print("报告已保存到 performance_profile.txt 和 performance_profile.json")

    return profiler


def test_benchmark_decorator():
    """测试基准测试装饰器"""
    print("\n" + "=" * 80)
    print("测试基准测试装饰器")
    print("=" * 80)

    # 使用装饰器
    print("\n使用 @benchmark_decorator:")
    result1 = test_fibonacci_recursive()
    result2 = test_fibonacci_iterative()
    result3 = test_fibonacci_memoization()

    return [result1, result2, result3]


def test_benchmark_suite():
    """测试基准测试套件"""
    print("\n" + "=" * 80)
    print("测试基准测试套件")
    print("=" * 80)

    # 创建测试套件实例
    suite = AlgorithmBenchmarks()

    # 运行套件
    print("\n运行算法基准测试套件:")
    results = suite.run_benchmark_suite(warmup_iterations=2, test_iterations=5)

    # 生成报告
    reporter = BenchmarkReporter()
    text_report = reporter.generate_text_report(results, "算法基准测试套件报告")
    print("\n" + text_report)

    return results


def test_utils_functions():
    """测试工具函数"""
    print("\n" + "=" * 80)
    print("测试工具函数")
    print("=" * 80)

    # 测试格式化函数
    print("\n格式化函数测试:")
    time_str = format_time(0.000123456)
    print(f"时间格式化: 0.000123456 -> {time_str}")

    memory_str = format_memory(1234567)
    print(f"内存格式化: 1234567 -> {memory_str}")

    percent_str = format_percentage(12.3456)
    print(f"百分比格式化: 12.3456 -> {percent_str}")

    human_time_str = human_readable_time(3661.5)
    print(f"人类可读时间: 3661.5 -> {human_time_str}")

    # 测试统计计算
    print("\n统计计算测试:")
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    stats = calculate_statistics(data)
    print(f"数据: {data}")
    print(f"平均值: {stats['mean']}")
    print(f"标准差: {stats['std']}")
    print(f"最小值: {stats['min']}")
    print(f"最大值: {stats['max']}")
    print(f"中位数: {stats['median']}")
    print(f"95百分位: {stats['p95']}")
    print(f"99百分位: {stats['p99']}")

    return True


def main():
    """主测试函数"""
    print("=" * 80)
    print("基准测试框架测试")
    print("=" * 80)

    all_passed = True

    try:
        # 测试基准测试运行器
        print("\n[1/5] 测试基准测试运行器...")
        test_benchmark_runner()
        print("通过 基准测试运行器测试通过")
    except Exception as e:
        print(f"失败 基准测试运行器测试失败: {e}")
        all_passed = False

    try:
        # 测试性能分析器
        print("\n[2/5] 测试性能分析器...")
        test_performance_profiler_demo()
        print("通过 性能分析器测试通过")
    except Exception as e:
        print(f"失败 性能分析器测试失败: {e}")
        all_passed = False

    try:
        # 测试基准测试装饰器
        print("\n[3/5] 测试基准测试装饰器...")
        test_benchmark_decorator()
        print("通过 基准测试装饰器测试通过")
    except Exception as e:
        print(f"失败 基准测试装饰器测试失败: {e}")
        all_passed = False

    try:
        # 测试基准测试套件
        print("\n[4/5] 测试基准测试套件...")
        test_benchmark_suite()
        print("通过 基准测试套件测试通过")
    except Exception as e:
        print(f"失败 基准测试套件测试失败: {e}")
        all_passed = False

    try:
        # 测试工具函数
        print("\n[5/5] 测试工具函数...")
        test_utils_functions()
        print("通过 工具函数测试通过")
    except Exception as e:
        print(f"失败 工具函数测试失败: {e}")
        all_passed = False

    print("\n" + "=" * 80)
    if all_passed:
        print("通过 所有测试通过！基准测试框架功能正常。")
    else:
        print("失败 部分测试失败，请检查实现。")
    print("=" * 80)

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
