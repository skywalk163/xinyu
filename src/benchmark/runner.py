"""
基准测试运行器

负责运行基准测试，收集性能数据，计算统计信息。
"""

import time
from dataclasses import dataclass, field
from typing import Callable, Any, Dict, List, Optional, Tuple
from datetime import datetime

# 使用统一的导入工具
from src.utils.imports import import_optional, with_psutil, with_tracemalloc, with_gc, with_time, with_json
from src.utils.stats_utils import calculate_statistics, calculate_percentiles, calculate_confidence_interval
from src.utils.logging_utils import get_logger, Timer

# 导入可选模块
statistics = import_optional('statistics')
tracemalloc = import_optional('tracemalloc')
psutil = import_optional('psutil')
gc = import_optional('gc')
json = import_optional('json')


@dataclass
class BenchmarkResult:
    """基准测试结果"""
    name: str
    function_name: str
    execution_times: List[float]
    memory_usages: List[int]
    cpu_usages: List[float]
    statistics: Dict[str, Any]
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "function_name": self.function_name,
            "execution_times": self.execution_times,
            "memory_usages": self.memory_usages,
            "cpu_usages": self.cpu_usages,
            "statistics": self.statistics,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), indent=2, default=str)
    
    def summary(self) -> str:
        """生成摘要"""
        stats = self.statistics
        return (
            f"基准测试: {self.name}\n"
            f"函数: {self.function_name}\n"
            f"执行时间: {stats['time_mean']:.6f}s ± {stats['time_std']:.6f}s "
            f"(min: {stats['time_min']:.6f}s, max: {stats['time_max']:.6f}s)\n"
            f"内存使用: {stats['memory_mean'] / 1024:.2f}KB ± {stats['memory_std'] / 1024:.2f}KB "
            f"(min: {stats['memory_min'] / 1024:.2f}KB, max: {stats['memory_max'] / 1024:.2f}KB)\n"
            f"CPU使用率: {stats['cpu_mean']:.2f}% ± {stats['cpu_std']:.2f}% "
            f"(min: {stats['cpu_min']:.2f}%, max: {stats['cpu_max']:.2f}%)\n"
            f"测试次数: {len(self.execution_times)}\n"
            f"时间戳: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        )


class BenchmarkRunner:
    """基准测试运行器"""
    
    def __init__(
        self,
        warmup_iterations: int = 3,
        test_iterations: int = 10,
        enable_gc: bool = True,
        collect_cpu: bool = True,
        collect_memory: bool = True,
        logger_name: str = "benchmark"
    ):
        """
        初始化基准测试运行器
        
        Args:
            warmup_iterations: 预热迭代次数
            test_iterations: 测试迭代次数
            enable_gc: 是否启用垃圾回收
            collect_cpu: 是否收集CPU使用率
            collect_memory: 是否收集内存使用
            logger_name: 日志器名称
        """
        self.warmup_iterations = warmup_iterations
        self.test_iterations = test_iterations
        self.enable_gc = enable_gc
        self.collect_cpu = collect_cpu
        self.collect_memory = collect_memory
        self.logger = get_logger(logger_name)
        self.results: List[BenchmarkResult] = []
        
    def run_benchmark(
        self,
        func: Callable,
        name: str = None,
        *args,
        **kwargs
    ) -> BenchmarkResult:
        """
        运行基准测试
        
        Args:
            func: 要测试的函数
            name: 测试名称，默认为函数名
            *args: 函数参数
            **kwargs: 函数关键字参数
            
        Returns:
            BenchmarkResult: 基准测试结果
        """
        if name is None:
            name = func.__name__
            
        # 预热运行
        if self.enable_gc:
            gc.collect()
            
        for _ in range(self.warmup_iterations):
            func(*args, **kwargs)
        
        # 实际测试运行
        execution_times = []
        memory_usages = []
        cpu_usages = []
        
        for i in range(self.test_iterations):
            # 准备测量
            if self.enable_gc:
                gc.collect()
                
            if self.collect_memory:
                tracemalloc.start()
                
            if self.collect_cpu:
                process = psutil.Process()
                cpu_before = process.cpu_percent(interval=None)
            
            # 测量执行时间
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            
            # 收集测量数据
            execution_time = end_time - start_time
            execution_times.append(execution_time)
            
            if self.collect_memory:
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                memory_usages.append(current)
            
            if self.collect_cpu:
                cpu_after = process.cpu_percent(interval=None)
                cpu_usages.append(cpu_after - cpu_before)
            
            # 清理
            if self.enable_gc:
                gc.collect()
        
        # 计算统计信息
        stats = self._calculate_statistics(execution_times, memory_usages, cpu_usages)
        
        # 创建结果对象
        benchmark_result = BenchmarkResult(
            name=name,
            function_name=func.__name__,
            execution_times=execution_times,
            memory_usages=memory_usages,
            cpu_usages=cpu_usages,
            statistics=stats,
            timestamp=datetime.now(),
            metadata={
                "args": str(args),
                "kwargs": str(kwargs),
                "warmup_iterations": self.warmup_iterations,
                "test_iterations": self.test_iterations,
                "enable_gc": self.enable_gc,
                "collect_cpu": self.collect_cpu,
                "collect_memory": self.collect_memory,
            }
        )
        
        self.results.append(benchmark_result)
        return benchmark_result
    
    def run_benchmark_suite(
        self,
        benchmarks: List[Tuple[Callable, str, tuple, dict]],
        name: str = "基准测试套件"
    ) -> List[BenchmarkResult]:
        """
        运行基准测试套件
        
        Args:
            benchmarks: 基准测试列表，每个元素为(函数, 名称, 参数元组, 关键字参数字典)
            name: 套件名称
            
        Returns:
            List[BenchmarkResult]: 基准测试结果列表
        """
        results = []
        self.logger.info(f"开始运行基准测试套件: {name}")
        self.logger.info(f"包含 {len(benchmarks)} 个测试")
        self.logger.info("-" * 50)
        
        for i, (func, bench_name, args, kwargs) in enumerate(benchmarks, 1):
            self.logger.info(f"运行测试 {i}/{len(benchmarks)}: {bench_name}")
            result = self.run_benchmark(func, bench_name, *args, **kwargs)
            results.append(result)
            self.logger.info(f"  平均执行时间: {result.statistics['time_mean']:.6f}s")
            self.logger.info(f"  平均内存使用: {result.statistics['memory_mean'] / 1024:.2f}KB")
            if self.collect_cpu:
                self.logger.info(f"  平均CPU使用率: {result.statistics['cpu_mean']:.2f}%")
            self.logger.info("")
        
        self.logger.info("-" * 50)
        self.logger.info(f"基准测试套件完成: {name}")
        return results
    
    def _calculate_statistics(
        self,
        times: List[float],
        memories: List[int],
        cpus: List[float]
    ) -> Dict[str, Any]:
        """计算统计信息"""
        stats = {}
        
        # 使用统一的统计工具
        if times:
            time_stats = calculate_statistics(times)
            percentiles = calculate_percentiles(times, [95, 99])
            stats.update({
                "time_mean": time_stats.get('mean', 0.0),
                "time_std": time_stats.get('std', 0.0),
                "time_min": time_stats.get('min', 0.0),
                "time_max": time_stats.get('max', 0.0),
                "time_median": time_stats.get('median', 0.0),
                "time_p95": percentiles.get(95, times[0] if times else 0.0),
                "time_p99": percentiles.get(99, times[0] if times else 0.0),
            })
        else:
            stats.update({
                "time_mean": 0.0,
                "time_std": 0.0,
                "time_min": 0.0,
                "time_max": 0.0,
                "time_median": 0.0,
                "time_p95": 0.0,
                "time_p99": 0.0,
            })
        
        # 内存统计
        if memories:
            memory_stats = calculate_statistics(memories)
            stats.update({
                "memory_mean": memory_stats.get('mean', 0.0),
                "memory_std": memory_stats.get('std', 0.0),
                "memory_min": memory_stats.get('min', 0.0),
                "memory_max": memory_stats.get('max', 0.0),
                "memory_median": memory_stats.get('median', 0.0),
            })
        else:
            stats.update({
                "memory_mean": 0.0,
                "memory_std": 0.0,
                "memory_min": 0.0,
                "memory_max": 0.0,
                "memory_median": 0.0,
            })
        
        # CPU统计
        if cpus:
            cpu_stats = calculate_statistics(cpus)
            stats.update({
                "cpu_mean": cpu_stats.get('mean', 0.0),
                "cpu_std": cpu_stats.get('std', 0.0),
                "cpu_min": cpu_stats.get('min', 0.0),
                "cpu_max": cpu_stats.get('max', 0.0),
                "cpu_median": cpu_stats.get('median', 0.0),
            })
        else:
            stats.update({
                "cpu_mean": 0.0,
                "cpu_std": 0.0,
                "cpu_min": 0.0,
                "cpu_max": 0.0,
                "cpu_median": 0.0,
            })
        
        return stats
    
    def compare_results(
        self,
        result1: BenchmarkResult,
        result2: BenchmarkResult,
        metric: str = "time_mean"
    ) -> Dict[str, Any]:
        """
        比较两个基准测试结果
        
        Args:
            result1: 第一个结果
            result2: 第二个结果
            metric: 比较的指标（time_mean, memory_mean, cpu_mean）
            
        Returns:
            Dict[str, Any]: 比较结果
        """
        if metric not in result1.statistics or metric not in result2.statistics:
            raise ValueError(f"指标 {metric} 不存在于结果中")
        
        value1 = result1.statistics[metric]
        value2 = result2.statistics[metric]
        
        if value1 == 0:
            return {
                "metric": metric,
                "value1": value1,
                "value2": value2,
                "difference": float('inf'),
                "percentage": float('inf'),
                "faster": "N/A",
            }
        
        difference = value2 - value1
        percentage = (difference / value1) * 100
        
        return {
            "metric": metric,
            "value1": value1,
            "value2": value2,
            "difference": difference,
            "percentage": percentage,
            "faster": "result1" if value1 < value2 else "result2",
        }
    
    def clear_results(self) -> None:
        """清空结果"""
        self.results.clear()
    
    def save_results(self, filepath: str) -> None:
        """保存结果到文件"""
        data = {
            "results": [result.to_dict() for result in self.results],
            "metadata": {
                "total_tests": len(self.results),
                "generated_at": datetime.now().isoformat(),
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
    
    def load_results(self, filepath: str) -> List[BenchmarkResult]:
        """从文件加载结果"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        results = []
        for result_data in data.get("results", []):
            result = BenchmarkResult(
                name=result_data["name"],
                function_name=result_data["function_name"],
                execution_times=result_data["execution_times"],
                memory_usages=result_data["memory_usages"],
                cpu_usages=result_data["cpu_usages"],
                statistics=result_data["statistics"],
                timestamp=datetime.fromisoformat(result_data["timestamp"]),
                metadata=result_data.get("metadata", {})
            )
            results.append(result)
        
        self.results = results
        return results