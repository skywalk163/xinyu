"""
性能工具模块

提供统一的性能分析功能，减少重复的性能测试代码。
"""

import cProfile
import functools
import io
import pstats
import signal
import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple


@dataclass
class PerformanceResult:
    """性能测试结果"""

    function_name: str
    execution_time: float  # 秒
    memory_usage_mb: float  # MB
    cpu_percent: float  # CPU使用率百分比
    call_count: int
    success: bool
    error: Optional[str] = None
    timestamp: float = field(default_factory=time.time)


@dataclass
class BenchmarkResult:
    """基准测试结果"""

    name: str
    iterations: int
    total_time: float
    avg_time: float
    min_time: float
    max_time: float
    std_time: float
    throughput: float  # 操作/秒
    memory_growth_mb: float
    cpu_usage_percent: float
    results: List[PerformanceResult] = field(default_factory=list)


def measure_execution_time(
    func: Callable = None, *, iterations: int = 1, warmup: int = 0
) -> Callable:
    """
    测量函数执行时间的装饰器

    Args:
        func: 被装饰的函数
        iterations: 迭代次数
        warmup: 预热次数

    Returns:
        装饰器或装饰后的函数
    """

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            # 预热
            for _ in range(warmup):
                f(*args, **kwargs)

            # 测量执行时间
            execution_times = []
            for _ in range(iterations):
                start_time = time.perf_counter()
    _ = s)  # 未使用变量
                end_time = time.perf_counter()
                execution_times.append(end_time - start_time)

            # 计算统计信息
            total_time = sum(execution_times)
            avg_time = total_time / iterations if iterations > 0 else 0
            min_time = min(execution_times) if execution_times else 0
            max_time = max(execution_times) if execution_times else 0

            # 计算标准差
            if iterations > 1:
                variance = sum((t - avg_time) ** 2 for t in execution_times) / (iterations - 1)
                std_time = variance**0.5
            else:
                std_time = 0.0

            # 计算吞吐量
            throughput = iterations / total_time if total_time > 0 else 0.0

            # 打印结果
            print(f"函数 {f.__name__} 性能测试结果:")
            print(f"  迭代次数: {iterations}")
            print(f"  总时间: {total_time:.6f} 秒")
            print(f"  平均时间: {avg_time:.6f} 秒")
            print(f"  最短时间: {min_time:.6f} 秒")
            print(f"  最长时间: {max_time:.6f} 秒")
            print(f"  标准差: {std_time:.6f} 秒")
            print(f"  吞吐量: {throughput:.2f} 操作/秒")

            return result

        return wrapper

    if func is None:
        return decorator
    return decorator(func)


def profile_function(
    func: Callable = None, *, sort_by: str = "cumulative", limit: int = 10
) -> Callable:
    """
    分析函数性能的装饰器

    Args:
        func: 被装饰的函数
        sort_by: 排序方式（'cumulative', 'time', 'calls'等）
        limit: 显示结果数量限制

    Returns:
        装饰器或装饰后的函数
    """

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            # 创建性能分析器
            profiler = cProfile.Profile()

            # 运行函数并分析性能
            profiler.enable()
    _ = wargs)  # 未使用变量
            profiler.disable()

            # 获取分析结果
            stream = io.StringIO()
            stats = pstats.Stats(profiler, stream=stream).sort_stats(sort_by)
            stats.print_stats(limit)

            # 打印分析结果
            print(f"函数 {f.__name__} 性能分析:")
            print(stream.getvalue())

            return result

        return wrapper

    if func is None:
        return decorator
    return decorator(func)


@contextmanager
def performance_monitor(name: str = "操作", track_memory: bool = True, track_cpu: bool = True):
    """
    性能监控上下文管理器

    Args:
        name: 操作名称
        track_memory: 是否跟踪内存
        track_cpu: 是否跟踪CPU

    Yields:
        性能监控器
    """
    monitor = PerformanceMonitor(name, track_memory, track_cpu)
    monitor.start()

    try:
        yield monitor
    finally:
        monitor.stop()
        monitor.print_report()


class PerformanceMonitor:
    """性能监控器"""

    def __init__(self, name: str = "操作", track_memory: bool = True, track_cpu: bool = True):
        """
        初始化性能监控器

        Args:
            name: 监控器名称
            track_memory: 是否跟踪内存
            track_cpu: 是否跟踪CPU
        """
        self.name = name
        self.track_memory = track_memory
        self.track_cpu = track_cpu

        self.start_time = None
        self.end_time = None
        self.memory_samples = []
        self.cpu_samples = []
        self.thread = None
        self.running = False

        # 导入可选模块
        try:
            import psutil

            self.psutil = psutil
            self.has_psutil = True
        except ImportError:
            self.has_psutil = False
            self.psutil = None

    def start(self) -> None:
        """开始监控"""
        self.start_time = time.time()
        self.memory_samples = []
        self.cpu_samples = []
        self.running = True

        if self.track_memory or self.track_cpu:
            self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.thread.start()

    def stop(self) -> None:
        """停止监控"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        self.end_time = time.time()

    def _monitor_loop(self) -> None:
        """监控循环"""
        if not self.has_psutil:
            return

        process = self.psutil.Process()

        while self.running:
            if self.track_memory:
                memory_info = process.memory_info()
                self.memory_samples.append(
                    {
                        "timestamp": time.time() - self.start_time,
                        "rss_mb": memory_info.rss / 1024 / 1024,
                        "vms_mb": memory_info.vms / 1024 / 1024,
                    }
                )

            if self.track_cpu:
                cpu_percent = process.cpu_percent(interval=0.1)
                self.cpu_samples.append(
                    {"timestamp": time.time() - self.start_time, "cpu_percent": cpu_percent}
                )

            time.sleep(0.1)  # 100ms采样间隔

    def get_results(self) -> Dict[str, Any]:
        """
        获取监控结果

        Returns:
            监控结果字典
        """
        if self.start_time is None:
            return {}

        end_time = self.end_time or time.time()
        duration = end_time - self.start_time

        # 计算内存统计
        memory_stats = {}
        if self.memory_samples:
            rss_values = [s["rss_mb"] for s in self.memory_samples]
            vms_values = [s["vms_mb"] for s in self.memory_samples]

            memory_stats = {
                "duration": duration,
                "samples": len(self.memory_samples),
                "avg_rss_mb": sum(rss_values) / len(rss_values),
                "min_rss_mb": min(rss_values),
                "max_rss_mb": max(rss_values),
                "avg_vms_mb": sum(vms_values) / len(vms_values),
                "min_vms_mb": min(vms_values),
                "max_vms_mb": max(vms_values),
                "rss_growth_mb": rss_values[-1] - rss_values[0] if len(rss_values) > 1 else 0,
                "vms_growth_mb": vms_values[-1] - vms_values[0] if len(vms_values) > 1 else 0,
            }

        # 计算CPU统计
        cpu_stats = {}
        if self.cpu_samples:
            cpu_values = [s["cpu_percent"] for s in self.cpu_samples]

            cpu_stats = {
                "duration": duration,
                "samples": len(self.cpu_samples),
                "avg_cpu_percent": sum(cpu_values) / len(cpu_values),
                "min_cpu_percent": min(cpu_values),
                "max_cpu_percent": max(cpu_values),
            }

        return {
            "name": self.name,
            "start_time": self.start_time,
            "end_time": end_time,
            "duration": duration,
            "memory_stats": memory_stats,
            "cpu_stats": cpu_stats,
        }

    def print_report(self) -> None:
        """打印监控报告"""
        results = self.get_results()

        if not results:
            print(f"{self.name}: 无监控数据")
            return

        print(f"\n{'='*60}")
        print(f"性能监控报告: {self.name}")
        print(f"{'='*60}")
        print(f"持续时间: {results['duration']:.2f} 秒")

        if results["memory_stats"]:
            mem = results["memory_stats"]
            print("\n内存使用:")
            print(f"  采样数: {mem['samples']}")
            print(f"  RSS内存: {mem['avg_rss_mb']:.2f} MB (平均)")
            print(f"            {mem['min_rss_mb']:.2f} MB (最小)")
            print(f"            {mem['max_rss_mb']:.2f} MB (最大)")
            print(f"            {mem['rss_growth_mb']:+.2f} MB (增长)")
            print(f"  VMS内存: {mem['avg_vms_mb']:.2f} MB (平均)")
            print(f"            {mem['min_vms_mb']:.2f} MB (最小)")
            print(f"            {mem['max_vms_mb']:.2f} MB (最大)")
            print(f"            {mem['vms_growth_mb']:+.2f} MB (增长)")

        if results["cpu_stats"]:
            cpu = results["cpu_stats"]
            print("\nCPU使用:")
            print(f"  采样数: {cpu['samples']}")
            print(f"  CPU使用率: {cpu['avg_cpu_percent']:.1f}% (平均)")
            print(f"              {cpu['min_cpu_percent']:.1f}% (最小)")
            print(f"              {cpu['max_cpu_percent']:.1f}% (最大)")

        print(f"{'='*60}")


def run_benchmark(
    func: Callable,
    args_list: List[Tuple] = None,
    kwargs_list: List[Dict] = None,
    iterations: int = 100,
    warmup: int = 10,
    name: str = None,
) -> BenchmarkResult:
    """
    运行基准测试

    Args:
        func: 要测试的函数
        args_list: 参数列表（每个元素是一个参数元组）
        kwargs_list: 关键字参数列表（每个元素是一个参数字典）
        iterations: 迭代次数
        warmup: 预热次数
        name: 测试名称

    Returns:
        基准测试结果
    """
    if name is None:
        name = func.__name__

    if args_list is None:
        args_list = [()]

    if kwargs_list is None:
        kwargs_list = [{}]

    # 确保参数列表长度一致
    max_len = max(len(args_list), len(kwargs_list))
    if len(args_list) < max_len:
        args_list = args_list * (max_len // len(args_list) + 1)
        args_list = args_list[:max_len]

    if len(kwargs_list) < max_len:
        kwargs_list = kwargs_list * (max_len // len(kwargs_list) + 1)
        kwargs_list = kwargs_list[:max_len]

    # 预热
    for i in range(min(warmup, len(args_list))):
        func(*args_list[i], **kwargs_list[i])

    # 测量执行时间
    execution_times = []
    results = []

    try:
        import psutil

        process = psutil.Process()
        memory_before = process.memory_info().rss / 1024 / 1024
        cpu_before = process.cpu_percent(interval=None)
    except ImportError:
        psutil = None
        memory_before = 0
        cpu_before = 0

    for i in range(iterations):
        arg_idx = i % len(args_list)
        kwargs_idx = i % len(kwargs_list)

        start_time = time.perf_counter()
        try:
    _ = ist[arg_idx], **kwargs_list[kwargs_idx])  # 未使用变量
            success = True
            error = None
        except Exception as e:
    _ =   # 未使用变量
            success = False
            error = str(e)

        end_time = time.perf_counter()
        execution_time = end_time - start_time

        execution_times.append(execution_time)

        # 创建性能结果
        perf_result = PerformanceResult(
            function_name=func.__name__,
            execution_time=execution_time,
            memory_usage_mb=0,  # 将在后面计算
            cpu_percent=0,  # 将在后面计算
            call_count=1,
            success=success,
            error=error,
        )
        results.append(perf_result)

    # 计算内存和CPU使用
    try:
        if psutil:
            memory_after = process.memory_info().rss / 1024 / 1024
            cpu_after = process.cpu_percent(interval=None)
            memory_growth_mb = memory_after - memory_before
            cpu_usage_percent = (cpu_before + cpu_after) / 2
        else:
            memory_growth_mb = 0
            cpu_usage_percent = 0
    except Exception:
        memory_growth_mb = 0
        cpu_usage_percent = 0

    # 计算统计信息
    total_time = sum(execution_times)
    avg_time = total_time / iterations if iterations > 0 else 0
    min_time = min(execution_times) if execution_times else 0
    max_time = max(execution_times) if execution_times else 0

    # 计算标准差
    if iterations > 1:
        variance = sum((t - avg_time) ** 2 for t in execution_times) / (iterations - 1)
        std_time = variance**0.5
    else:
        std_time = 0.0

    # 计算吞吐量
    throughput = iterations / total_time if total_time > 0 else 0.0

    # 更新结果中的内存和CPU信息
    for result in results:
        result.memory_usage_mb = memory_growth_mb / iterations if iterations > 0 else 0
        result.cpu_percent = cpu_usage_percent

    return BenchmarkResult(
        name=name,
        iterations=iterations,
        total_time=total_time,
        avg_time=avg_time,
        min_time=min_time,
        max_time=max_time,
        std_time=std_time,
        throughput=throughput,
        memory_growth_mb=memory_growth_mb,
        cpu_usage_percent=cpu_usage_percent,
        results=results,
    )


def print_benchmark_result(result: BenchmarkResult, detailed: bool = False) -> None:
    """
    打印基准测试结果

    Args:
        result: 基准测试结果
        detailed: 是否打印详细结果
    """
    print(f"\n{'='*60}")
    print(f"基准测试: {result.name}")
    print(f"{'='*60}")
    print(f"迭代次数: {result.iterations}")
    print(f"总时间: {result.total_time:.6f} 秒")
    print(f"平均时间: {result.avg_time:.6f} 秒")
    print(f"最短时间: {result.min_time:.6f} 秒")
    print(f"最长时间: {result.max_time:.6f} 秒")
    print(f"标准差: {result.std_time:.6f} 秒")
    print(f"吞吐量: {result.throughput:.2f} 操作/秒")
    print(f"内存增长: {result.memory_growth_mb:.2f} MB")
    print(f"CPU使用率: {result.cpu_usage_percent:.1f}%")

    # 计算成功率
    success_count = sum(1 for r in result.results if r.success)
    success_rate = success_count / len(result.results) * 100 if result.results else 0
    print(f"成功率: {success_rate:.1f}% ({success_count}/{len(result.results)})")

    if detailed and result.results:
        print("\n详细结果:")
        for i, r in enumerate(result.results[:10]):  # 只显示前10个
            status = "✓" if r.success else "✗"
            print(f"  [{i+1}] {status} {r.execution_time:.6f}s")

        if len(result.results) > 10:
            print(f"  ... 还有 {len(result.results) - 10} 个结果")

    print(f"{'='*60}")


class TimeoutException(Exception):
    """超时异常"""

    pass


def timeout(seconds: float):
    """
    超时装饰器

    Args:
        seconds: 超时时间（秒）

    Returns:
        装饰器函数
    """

    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutException(f"函数 {func.__name__} 执行超时 ({seconds}秒)")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 设置信号处理（仅适用于Unix系统）
            try:
                signal.signal(signal.SIGALRM, _handle_timeout)
                signal.alarm(int(seconds))
    _ = args)  # 未使用变量
                signal.alarm(0)  # 取消警报
                return result
            except TimeoutException:
                raise
            except Exception as e:
                signal.alarm(0)  # 取消警报
                raise e

        return wrapper

    return decorator


@contextmanager
def timeout_context(seconds: float):
    """
    超时上下文管理器

    Args:
        seconds: 超时时间（秒）

    Yields:
        None
    """

    def _handle_timeout(signum, frame):
        raise TimeoutException(f"操作执行超时 ({seconds}秒)")

    try:
        signal.signal(signal.SIGALRM, _handle_timeout)
        signal.alarm(int(seconds))
        yield
    finally:
        signal.alarm(0)  # 取消警报
