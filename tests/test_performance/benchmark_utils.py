"""基准测试工具函数

提供性能基准测试的基础框架和工具函数。
"""
import statistics
import time
from functools import wraps
from typing import Any, Callable, Dict, List


def benchmark(iterations: int = 10, warmup: int = 2) -> Callable:
    """
    性能基准测试装饰器

    Args:
        iterations: 正式测量次数
        warmup: 预热次数

    Returns:
        装饰后的函数
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Dict[str, float]:
            # 预热
            for _ in range(warmup):
                try:
                    func(*args, **kwargs)
                except Exception:
                    pass

            # 正式测量
            times = []
            for _ in range(iterations):
                start = time.perf_counter()
                try:
                    func(*args, **kwargs)
                except Exception:
                    pass
                end = time.perf_counter()
                times.append(end - start)

            # 计算统计信息
            if times:
                return {
                    "mean": statistics.mean(times),
                    "median": statistics.median(times),
                    "stdev": statistics.stdev(times) if len(times) > 1 else 0.0,
                    "min": min(times),
                    "max": max(times),
                    "iterations": iterations,
                }
            else:
                return {
                    "mean": 0.0,
                    "median": 0.0,
                    "stdev": 0.0,
                    "min": 0.0,
                    "max": 0.0,
                    "iterations": 0,
                }

        return wrapper

    return decorator


def get_benchmark_result(times: List[float]) -> Dict[str, float]:
    """
    计算基准测试结果

    Args:
        times: 测量时间列表

    Returns:
        统计结果字典
    """
    if not times:
        return {"mean": 0.0, "median": 0.0, "stdev": 0.0, "min": 0.0, "max": 0.0}

    return {
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "stdev": statistics.stdev(times) if len(times) > 1 else 0.0,
        "min": min(times),
        "max": max(times),
    }


def format_result(result: Dict[str, float], operation: str) -> str:
    """
    格式化输出结果

    Args:
        result: 基准测试结果
        operation: 操作名称

    Returns:
        格式化的字符串
    """
    return (
        f"{operation}: mean={result['mean']*1000:.2f}ms, "
        f"median={result['median']*1000:.2f}ms, "
        f"min={result['min']*1000:.2f}ms, "
        f"max={result['max']*1000:.2f}ms"
    )


def compare_with_baseline(
    current: Dict[str, float], baseline: Dict[str, float], threshold: float = 0.2
) -> bool:
    """
    与基线对比

    Args:
        current: 当前结果
        baseline: 基线结果
        threshold: 允许的退化阈值（默认20%）

    Returns:
        是否在允许范围内
    """
    if baseline["mean"] == 0:
        return True

    ratio = current["mean"] / baseline["mean"]
    return ratio <= (1 + threshold)


class BenchmarkResult:
    """基准测试结果类"""

    def __init__(self, operation: str, iterations: int, times: List[float]):
        self.operation = operation
        self.iterations = iterations
        self.times = times
        self.result = get_benchmark_result(times)

    def __str__(self) -> str:
        return format_result(self.result, self.operation)

    def is_acceptable(self, baseline: Dict[str, float], threshold: float = 0.2) -> bool:
        """检查是否在可接受范围内"""
        return compare_with_baseline(self.result, baseline, threshold)
