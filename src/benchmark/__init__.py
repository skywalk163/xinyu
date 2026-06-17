"""
性能基准测试框架

提供执行时间、内存使用、CPU使用率等性能指标的测量功能。
支持多轮测试、统计分析、可视化报告生成。
"""

from .profiler import PerformanceProfiler
from .reporter import BenchmarkReporter
from .runner import BenchmarkResult, BenchmarkRunner
from .utils import format_memory, format_percentage, format_time

__all__ = [
    "BenchmarkRunner",
    "BenchmarkResult",
    "PerformanceProfiler",
    "BenchmarkReporter",
    "format_time",
    "format_memory",
    "format_percentage",
]
