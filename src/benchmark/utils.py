"""
基准测试工具函数

提供格式化、转换、辅助函数等工具。
"""

import math
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple


def format_time(seconds: float, precision: int = 6) -> str:
    """
    格式化时间

    Args:
        seconds: 秒数
        precision: 小数精度

    Returns:
        str: 格式化后的时间字符串
    """
    if seconds < 1e-6:  # 纳秒级
        return f"{seconds * 1e9:.{precision}f} ns"
    elif seconds < 1e-3:  # 微秒级
        return f"{seconds * 1e6:.{precision}f} us"  # 使用us代替µs避免编码问题
    elif seconds < 1:  # 毫秒级
        return f"{seconds * 1e3:.{precision}f} ms"
    else:  # 秒级
        return f"{seconds:.{precision}f} s"


def format_memory(bytes_value: int, precision: int = 2) -> str:
    """
    格式化内存大小

    Args:
        bytes_value: 字节数
        precision: 小数精度

    Returns:
        str: 格式化后的内存字符串
    """
    if bytes_value < 1024:  # 字节
        return f"{bytes_value} B"
    elif bytes_value < 1024 * 1024:  # KB
        return f"{bytes_value / 1024:.{precision}f} KB"
    elif bytes_value < 1024 * 1024 * 1024:  # MB
        return f"{bytes_value / (1024 * 1024):.{precision}f} MB"
    else:  # GB
        return f"{bytes_value / (1024 * 1024 * 1024):.{precision}f} GB"


def format_percentage(value: float, precision: int = 2) -> str:
    """
    格式化百分比

    Args:
        value: 百分比值（0-100）
        precision: 小数精度

    Returns:
        str: 格式化后的百分比字符串
    """
    return f"{value:.{precision}f}%"


def human_readable_time(seconds: float) -> str:
    """
    将秒数转换为人类可读的时间

    Args:
        seconds: 秒数

    Returns:
        str: 人类可读的时间字符串
    """
    if seconds < 1:
        return format_time(seconds)

    td = timedelta(seconds=seconds)
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds:.2f}s")

    return " ".join(parts)


def calculate_statistics(data: List[float]) -> Dict[str, float]:
    """
    计算统计信息

    Args:
        data: 数据列表

    Returns:
        Dict[str, float]: 统计信息字典
    """
    if not data:
        return {
            "mean": 0.0,
            "std": 0.0,
            "min": 0.0,
            "max": 0.0,
            "median": 0.0,
            "p95": 0.0,
            "p99": 0.0,
        }

    import statistics

    sorted_data = sorted(data)
    n = len(data)

    return {
        "mean": statistics.mean(data),
        "std": statistics.stdev(data) if n > 1 else 0.0,
        "min": min(data),
        "max": max(data),
        "median": statistics.median(data),
        "p95": sorted_data[int(n * 0.95)] if n > 1 else data[0],
        "p99": sorted_data[int(n * 0.99)] if n > 1 else data[0],
    }


def confidence_interval(data: List[float], confidence: float = 0.95) -> Tuple[float, float, float]:
    """
    计算置信区间

    Args:
        data: 数据列表
        confidence: 置信水平（0-1）

    Returns:
        Tuple[float, float, float]: (均值, 下限, 上限)
    """
    if len(data) < 2:
        mean = data[0] if data else 0.0
        return mean, mean, mean

    import statistics

    import scipy.stats

    mean = statistics.mean(data)
    std = statistics.stdev(data)
    n = len(data)

    # 计算t值
    t_value = scipy.stats.t.ppf((1 + confidence) / 2, n - 1)

    # 计算置信区间
    margin = t_value * std / math.sqrt(n)
    lower = mean - margin
    upper = mean + margin

    return mean, lower, upper


def format_confidence_interval(mean: float, lower: float, upper: float, unit: str = "") -> str:
    """
    格式化置信区间

    Args:
        mean: 均值
        lower: 下限
        upper: 上限
        unit: 单位

    Returns:
        str: 格式化后的置信区间字符串
    """
    return f"{mean:.6f}{unit} ({lower:.6f}{unit} - {upper:.6f}{unit})"


def benchmark_decorator(
    warmup_iterations: int = 3,
    test_iterations: int = 10,
    enable_gc: bool = True,
    collect_cpu: bool = True,
    collect_memory: bool = True,
):
    """
    基准测试装饰器

    Args:
        warmup_iterations: 预热迭代次数
        test_iterations: 测试迭代次数
        enable_gc: 是否启用垃圾回收
        collect_cpu: 是否收集CPU使用率
        collect_memory: 是否收集内存使用

    Returns:
        装饰器函数
    """
    from .runner import BenchmarkRunner

    def decorator(func):
        def wrapper(*args, **kwargs):
            runner = BenchmarkRunner(
                warmup_iterations=warmup_iterations,
                test_iterations=test_iterations,
                enable_gc=enable_gc,
                collect_cpu=collect_cpu,
                collect_memory=collect_memory,
            )

            result = runner.run_benchmark(func, func.__name__, *args, **kwargs)

            # 打印结果摘要
            print("=" * 60)
            print(f"基准测试结果: {func.__name__}")
            print("=" * 60)
            print(result.summary())
            print("=" * 60)

            return result

        return wrapper

    return decorator


def profile_decorator(sort_by: str = "cumulative", limit: int = 20):
    """
    性能分析装饰器

    Args:
        sort_by: 排序方式
        limit: 显示结果数量限制

    Returns:
        装饰器函数
    """
    from .profiler import PerformanceProfiler

    def decorator(func):
        def wrapper(*args, **kwargs):
            profiler = PerformanceProfiler(sort_by=sort_by, limit=limit)

            print(f"开始性能分析: {func.__name__}")
            result = profiler.profile_function(func, *args, **kwargs)

            # 打印分析报告
            print(profiler.generate_report())

            return result

        return wrapper

    return decorator


def create_benchmark_suite(name: str = "基准测试套件"):
    """
    创建基准测试套件装饰器

    Args:
        name: 套件名称

    Returns:
        装饰器函数
    """
    from .runner import BenchmarkRunner

    def decorator(cls):
        # 收集所有以"benchmark_"开头的方法
        benchmark_methods = []
        for attr_name in dir(cls):
            if attr_name.startswith("benchmark_"):
                attr = getattr(cls, attr_name)
                if callable(attr):
                    benchmark_methods.append(attr_name)

        # 添加运行套件的方法
        def run_suite(self, *args, **kwargs):
            runner = BenchmarkRunner(*args, **kwargs)
            benchmarks = []

            for method_name in benchmark_methods:
                method = getattr(self, method_name)
                benchmark_name = method_name.replace("benchmark_", "").replace("_", " ").title()
                benchmarks.append((method, benchmark_name, (), {}))

            return runner.run_benchmark_suite(benchmarks, name)

        setattr(cls, "run_benchmark_suite", run_suite)
        return cls

    return decorator


def export_results_to_csv(results: List[Dict[str, Any]], filepath: str) -> None:
    """
    导出结果到CSV文件

    Args:
        results: 结果列表
        filepath: 文件路径
    """
    import csv

    if not results:
        return

    # 获取所有字段
    fieldnames = set()
    for result in results:
        fieldnames.update(result.keys())

    fieldnames = sorted(fieldnames)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def load_results_from_csv(filepath: str) -> List[Dict[str, Any]]:
    """
    从CSV文件加载结果

    Args:
        filepath: 文件路径

    Returns:
        List[Dict[str, Any]]: 结果列表
    """
    import csv

    results = []
    with open(filepath, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 转换数据类型
            for key, value in row.items():
                if value.replace(".", "", 1).isdigit():
                    if "." in value:
                        row[key] = float(value)
                    else:
                        row[key] = int(value)
            results.append(row)

    return results
