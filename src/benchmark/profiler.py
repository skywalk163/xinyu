"""
性能分析器

提供函数级性能分析，包括执行时间、内存分配、调用关系等。
"""

import cProfile
import inspect
import io
import json
import pstats
import time
import tracemalloc
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, List

# 使用统一的日志工具
from src.utils.logging_utils import get_logger


@dataclass
class ProfileResult:
    """性能分析结果"""

    function_name: str
    total_time: float
    total_calls: int
    primitive_calls: int
    percall_time: float
    cumulative_time: float
    cumulative_percall: float
    file_name: str
    line_number: int
    memory_allocated: int = 0
    memory_peak: int = 0
    callers: List[Dict[str, Any]] = None
    callees: List[Dict[str, Any]] = None

    def __post_init__(self):
        if self.callers is None:
            self.callers = []
        if self.callees is None:
            self.callees = []

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "function_name": self.function_name,
            "total_time": self.total_time,
            "total_calls": self.total_calls,
            "primitive_calls": self.primitive_calls,
            "percall_time": self.percall_time,
            "cumulative_time": self.cumulative_time,
            "cumulative_percall": self.cumulative_percall,
            "file_name": self.file_name,
            "line_number": self.line_number,
            "memory_allocated": self.memory_allocated,
            "memory_peak": self.memory_peak,
            "callers": self.callers,
            "callees": self.callees,
        }


class PerformanceProfiler:
    """性能分析器"""

    def __init__(self, sort_by: str = "cumulative", limit: int = 20):
        """
        初始化性能分析器

        Args:
            sort_by: 排序方式（time, cumulative, calls, name）
            limit: 显示结果数量限制
        """
        self.sort_by = sort_by
        self.limit = limit
        self.profiler = cProfile.Profile()
        self.results: List[ProfileResult] = []
        self.logger = get_logger("benchmark.profiler")

    def profile_function(self, func: Callable, *args, **kwargs) -> ProfileResult:
        """
        分析单个函数性能

        Args:
            func: 要分析的函数
            *args: 函数参数
            **kwargs: 函数关键字参数

        Returns:
            ProfileResult: 性能分析结果
        """
        # 开始内存跟踪
        tracemalloc.start()

        # 运行性能分析
        self.profiler.enable()
        start_time = time.perf_counter()
        _ = func(*args, **kwargs)  # 忽略返回值，只用于性能分析
        end_time = time.perf_counter()
        self.profiler.disable()

        # 获取内存统计
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # 获取分析结果
        s = io.StringIO()
        ps = pstats.Stats(self.profiler, stream=s).sort_stats(self.sort_by)
        ps.print_stats(self.limit)

        # 解析分析结果
        profile_text = s.getvalue()
        profile_data = self._parse_profile_output(profile_text, func)

        # 创建结果对象
        profile_result = ProfileResult(
            function_name=func.__name__,
            total_time=end_time - start_time,
            total_calls=profile_data.get("total_calls", 0),
            primitive_calls=profile_data.get("primitive_calls", 0),
            percall_time=profile_data.get("percall_time", 0),
            cumulative_time=profile_data.get("cumulative_time", 0),
            cumulative_percall=profile_data.get("cumulative_percall", 0),
            file_name=profile_data.get("file_name", ""),
            line_number=profile_data.get("line_number", 0),
            memory_allocated=current,
            memory_peak=peak,
            callers=profile_data.get("callers", []),
            callees=profile_data.get("callees", []),
        )

        self.results.append(profile_result)
        return profile_result

    def profile_module(self, module_name: str, function_pattern: str = "*") -> List[ProfileResult]:
        """
        分析模块中所有匹配函数的性能

        Args:
            module_name: 模块名
            function_pattern: 函数名模式（支持通配符）

        Returns:
            List[ProfileResult]: 性能分析结果列表
        """
        import fnmatch
        import importlib

        module = importlib.import_module(module_name)
        results = []

        # 获取模块中所有函数
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) and fnmatch.fnmatch(name, function_pattern):
                try:
                    # 尝试获取函数签名
                    sig = inspect.signature(obj)
                    # 创建默认参数
                    args = []
                    kwargs = {}
                    for param_name, param in sig.parameters.items():
                        if param.default != inspect.Parameter.empty:
                            kwargs[param_name] = param.default
                        elif param.kind in (
                            inspect.Parameter.POSITIONAL_ONLY,
                            inspect.Parameter.POSITIONAL_OR_KEYWORD,
                        ):
                            args.append(None)

                    self.logger.info(f"分析函数: {name}")
                    result = self.profile_function(obj, *args, **kwargs)
                    results.append(result)

                except Exception as e:
                    self.logger.error(f"分析函数 {name} 时出错: {e}")

        return results

    def _parse_profile_output(self, profile_text: str, func: Callable) -> Dict[str, Any]:
        """解析cProfile输出"""
        lines = profile_text.strip().split("\n")
        data = {
            "total_calls": 0,
            "primitive_calls": 0,
            "percall_time": 0,
            "cumulative_time": 0,
            "cumulative_percall": 0,
            "file_name": "",
            "line_number": 0,
            "callers": [],
            "callees": [],
        }

        # 获取函数信息
        try:
            file_name = inspect.getfile(func)
            line_number = inspect.getsourcelines(func)[1]
            data["file_name"] = file_name
            data["line_number"] = line_number
        except Exception:
            pass

        # 解析输出行
        for line in lines:
            line = line.strip()

            # 跳过空行和标题行
            if not line or line.startswith("ncalls") or line.startswith("---"):
                continue

            # 解析数据行
            parts = line.split()
            if len(parts) >= 6:
                try:
                    ncalls = parts[0]
                    if "/" in ncalls:
                        total_calls, primitive_calls = ncalls.split("/")
                        data["total_calls"] = int(total_calls)
                        data["primitive_calls"] = int(primitive_calls)
                    else:
                        data["total_calls"] = int(ncalls)
                        data["primitive_calls"] = int(ncalls)

                    data["percall_time"] = float(parts[1])
                    data["cumulative_time"] = float(parts[2])
                    data["cumulative_percall"] = float(parts[3])

                    # 提取函数名
                    func_info = " ".join(parts[4:])
                    if func.__name__ in func_info:
                        # 这是我们要找的函数
                        pass
                    elif ":" in func_info:
                        # 这是调用者或被调用者
                        caller_info = func_info.split(":")
                        if len(caller_info) >= 2:
                            caller_name = caller_info[0].strip()
                            caller_location = caller_info[1].strip()

                            # 判断是调用者还是被调用者
                            if func.__name__ in caller_name:
                                # 被调用者
                                data["callees"].append(
                                    {
                                        "name": caller_name,
                                        "location": caller_location,
                                        "calls": data["total_calls"],
                                        "time": data["percall_time"],
                                    }
                                )
                            else:
                                # 调用者
                                data["callers"].append(
                                    {
                                        "name": caller_name,
                                        "location": caller_location,
                                        "calls": data["total_calls"],
                                        "time": data["percall_time"],
                                    }
                                )
                except (ValueError, IndexError):
                    continue

        return data

    def get_hotspots(self, limit: int = 10) -> List[ProfileResult]:
        """
        获取热点函数

        Args:
            limit: 返回的热点数量

        Returns:
            List[ProfileResult]: 热点函数列表
        """
        sorted_results = sorted(self.results, key=lambda x: x.cumulative_time, reverse=True)
        return sorted_results[:limit]

    def get_memory_hotspots(self, limit: int = 10) -> List[ProfileResult]:
        """
        获取内存热点函数

        Args:
            limit: 返回的热点数量

        Returns:
            List[ProfileResult]: 内存热点函数列表
        """
        sorted_results = sorted(self.results, key=lambda x: x.memory_allocated, reverse=True)
        return sorted_results[:limit]

    def generate_report(self) -> str:
        """生成性能分析报告"""
        if not self.results:
            return "没有性能分析数据"

        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("性能分析报告")
        report_lines.append("=" * 80)
        report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"分析函数数量: {len(self.results)}")
        report_lines.append("")

        # 热点函数
        hotspots = self.get_hotspots(5)
        if hotspots:
            report_lines.append("热点函数（按累计时间排序）:")
            report_lines.append("-" * 80)
            for i, hotspot in enumerate(hotspots, 1):
                report_lines.append(f"{i}. {hotspot.function_name}")
                report_lines.append(f"   累计时间: {hotspot.cumulative_time:.6f}s")
                report_lines.append(f"   调用次数: {hotspot.total_calls}")
                report_lines.append(f"   每次调用: {hotspot.percall_time:.6f}s")
                report_lines.append(f"   文件位置: {hotspot.file_name}:{hotspot.line_number}")
                report_lines.append("")

        # 内存热点
        memory_hotspots = self.get_memory_hotspots(5)
        if memory_hotspots:
            report_lines.append("内存热点函数（按内存分配排序）:")
            report_lines.append("-" * 80)
            for i, hotspot in enumerate(memory_hotspots, 1):
                report_lines.append(f"{i}. {hotspot.function_name}")
                report_lines.append(f"   内存分配: {hotspot.memory_allocated / 1024:.2f}KB")
                report_lines.append(f"   内存峰值: {hotspot.memory_peak / 1024:.2f}KB")
                report_lines.append(f"   文件位置: {hotspot.file_name}:{hotspot.line_number}")
                report_lines.append("")

        # 总体统计
        total_time = sum(r.total_time for r in self.results)
        total_memory = sum(r.memory_allocated for r in self.results)
        total_calls = sum(r.total_calls for r in self.results)

        report_lines.append("总体统计:")
        report_lines.append("-" * 80)
        report_lines.append(f"总执行时间: {total_time:.6f}s")
        report_lines.append(f"总内存分配: {total_memory / 1024:.2f}KB")
        report_lines.append(f"总调用次数: {total_calls}")
        report_lines.append(
            f"平均每次调用时间: {total_time / total_calls:.6f}s" if total_calls > 0 else "平均每次调用时间: N/A"
        )
        report_lines.append(
            f"平均每次调用内存: {total_memory / total_calls / 1024:.2f}KB"
            if total_calls > 0
            else "平均每次调用内存: N/A"
        )

        report_lines.append("=" * 80)
        return "\n".join(report_lines)

    def save_report(self, filepath: str) -> None:
        """保存报告到文件"""
        report = self.generate_report()
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(report)

    def save_json_report(self, filepath: str) -> None:
        """保存JSON格式报告"""
        data = {
            "generated_at": datetime.now().isoformat(),
            "total_functions": len(self.results),
            "results": [r.to_dict() for r in self.results],
            "hotspots": [r.to_dict() for r in self.get_hotspots(10)],
            "memory_hotspots": [r.to_dict() for r in self.get_memory_hotspots(10)],
            "summary": {
                "total_time": sum(r.total_time for r in self.results),
                "total_memory": sum(r.memory_allocated for r in self.results),
                "total_calls": sum(r.total_calls for r in self.results),
            },
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)

    def clear_results(self) -> None:
        """清空结果"""
        self.results.clear()
        self.profiler = cProfile.Profile()
