"""
内存工具模块

提供统一的内存管理功能，减少重复的内存操作代码。
"""

import gc
import time
import tracemalloc
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class MemoryUsage:
    """内存使用信息"""

    rss_mb: float  # 常驻内存大小（MB）
    vms_mb: float  # 虚拟内存大小（MB）
    shared_mb: float  # 共享内存大小（MB）
    text_mb: float  # 文本段大小（MB）
    data_mb: float  # 数据段大小（MB）
    timestamp: float = field(default_factory=time.time)


@dataclass
class MemorySnapshot:
    """内存快照"""

    timestamp: float
    usage: MemoryUsage
    gc_stats: Dict[str, Any]
    object_counts: Dict[str, int]


def get_memory_usage() -> Optional[MemoryUsage]:
    """
    获取当前进程的内存使用情况

    Returns:
        内存使用信息，如果psutil不可用则返回None
    """
    try:
        import psutil

        process = psutil.Process()
        memory_info = process.memory_info()

        return MemoryUsage(
            rss_mb=memory_info.rss / 1024 / 1024,
            vms_mb=memory_info.vms / 1024 / 1024,
            shared_mb=memory_info.shared / 1024 / 1024 if hasattr(memory_info, "shared") else 0.0,
            text_mb=memory_info.text / 1024 / 1024 if hasattr(memory_info, "text") else 0.0,
            data_mb=memory_info.data / 1024 / 1024 if hasattr(memory_info, "data") else 0.0,
        )
    except ImportError:
        return None


def track_memory_allocation(
    func: Callable = None, *, track_calls: bool = True, track_lines: bool = False
) -> Callable:
    """
    跟踪函数内存分配的装饰器

    Args:
        func: 被装饰的函数
        track_calls: 是否跟踪函数调用
        track_lines: 是否跟踪行号

    Returns:
        装饰器或装饰后的函数
    """

    def decorator(f):
        def wrapper(*args, **kwargs):
            # 开始跟踪内存分配
            tracemalloc.start()

            # 获取初始快照
            snapshot1 = tracemalloc.take_snapshot()

            # 执行函数
            result = f(*args, **kwargs)

            # 获取结束快照
            snapshot2 = tracemalloc.take_snapshot()

            # 停止跟踪
            tracemalloc.stop()

            # 比较快照
            if track_calls:
                stats = snapshot2.compare_to(snapshot1, "lineno")
            else:
                stats = snapshot2.compare_to(snapshot1, "traceback")

            # 收集统计信息
            total_allocated = 0
            allocation_stats = []

            for stat in stats[:10]:  # 只显示前10个
                total_allocated += stat.size_diff
                allocation_stats.append(
                    {
                        "size_diff": stat.size_diff,
                        "size_diff_kb": stat.size_diff / 1024,
                        "count_diff": stat.count_diff,
                        "traceback": stat.traceback,
                    }
                )

            # 打印内存分配信息
            print(f"函数 {f.__name__} 内存分配统计:")
            print(f"  总分配内存: {total_allocated / 1024:.2f} KB")
            print(f"  分配热点 ({len(allocation_stats)} 个):")

            for i, stat in enumerate(allocation_stats[:5], 1):
                traceback_str = str(stat["traceback"])
                if len(traceback_str) > 100:
                    traceback_str = traceback_str[:97] + "..."

                print(f"    热点 {i}: {traceback_str}")
                print(f"      大小: {stat['size_diff_kb']:.2f} KB, 数量: {stat['count_diff']}")

            return result

        return wrapper

    if func is None:
        return decorator
    return decorator(func)


def find_memory_leaks(
    snapshot1: Any = None, snapshot2: Any = None, limit: int = 10
) -> List[Dict[str, Any]]:
    """
    查找内存泄漏

    Args:
        snapshot1: 第一个内存快照
        snapshot2: 第二个内存快照
        limit: 返回结果数量限制

    Returns:
        内存泄漏信息列表
    """
    if snapshot1 is None or snapshot2 is None:
        # 如果没有提供快照，创建新的
        tracemalloc.start()
        snapshot1 = tracemalloc.take_snapshot()
        # 执行一些操作或等待一段时间
        time.sleep(0.1)
        snapshot2 = tracemalloc.take_snapshot()
        tracemalloc.stop()

    # 比较快照
    stats = snapshot2.compare_to(snapshot1, "traceback")

    # 收集泄漏信息
    leaks = []
    for stat in stats[:limit]:
        if stat.size_diff > 0:  # 只关注内存增长
            leaks.append(
                {
                    "size_diff": stat.size_diff,
                    "size_diff_kb": stat.size_diff / 1024,
                    "size_diff_mb": stat.size_diff / 1024 / 1024,
                    "count_diff": stat.count_diff,
                    "traceback": stat.traceback,
                }
            )

    return leaks


def monitor_memory_growth(
    interval: float = 1.0, duration: float = 10.0, threshold_mb: float = 10.0
) -> Dict[str, Any]:
    """
    监控内存增长

    Args:
        interval: 监控间隔（秒）
        duration: 监控持续时间（秒）
        threshold_mb: 内存增长阈值（MB）

    Returns:
        监控结果
    """
    try:
        import psutil
    except ImportError:
        return {
            "success": False,
            "error": "psutil模块未安装",
            "growth_mb": 0.0,
            "exceeded_threshold": False,
        }

    process = psutil.Process()
    samples = []
    start_time = time.time()
    start_memory = process.memory_info().rss / 1024 / 1024

    print(f"开始监控内存增长，持续时间: {duration}秒，间隔: {interval}秒")
    print(f"初始内存: {start_memory:.2f} MB")
    print(f"阈值: {threshold_mb} MB")

    while time.time() - start_time < duration:
        current_memory = process.memory_info().rss / 1024 / 1024
        samples.append({"timestamp": time.time() - start_time, "memory_mb": current_memory})

        print(f"  时间: {samples[-1]['timestamp']:.1f}s, 内存: {current_memory:.2f} MB")
        time.sleep(interval)

    end_memory = process.memory_info().rss / 1024 / 1024
    growth_mb = end_memory - start_memory
    exceeded_threshold = growth_mb > threshold_mb

    result = {
        "success": True,
        "start_memory_mb": start_memory,
        "end_memory_mb": end_memory,
        "growth_mb": growth_mb,
        "exceeded_threshold": exceeded_threshold,
        "threshold_mb": threshold_mb,
        "duration": duration,
        "interval": interval,
        "samples": samples,
    }

    if exceeded_threshold:
        print(f"警告: 内存增长超过阈值 ({growth_mb:.2f}MB > {threshold_mb}MB)")
    else:
        print(f"内存增长在阈值内: {growth_mb:.2f}MB")

    return result


def get_object_counts(limit: int = 20) -> Dict[str, int]:
    """
    获取对象类型计数

    Args:
        limit: 返回的类型数量限制

    Returns:
        对象类型计数字典
    """
    objects = gc.get_objects()
    type_counts = defaultdict(int)

    for obj in objects:
        obj_type = type(obj).__name__
        type_counts[obj_type] += 1

    # 按数量排序并限制数量
    sorted_counts = dict(sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:limit])

    return sorted_counts


def take_memory_snapshot() -> MemorySnapshot:
    """
    获取内存快照

    Returns:
        内存快照
    """
    usage = get_memory_usage()
    gc_stats = {
        "collections": gc.get_count(),
        "threshold": gc.get_threshold(),
        "enabled": gc.isenabled(),
    }

    # 强制垃圾回收以获取准确计数
    gc.collect()

    object_counts = get_object_counts()

    return MemorySnapshot(
        timestamp=time.time(),
        usage=usage or MemoryUsage(0.0, 0.0, 0.0, 0.0, 0.0),
        gc_stats=gc_stats,
        object_counts=object_counts,
    )


def compare_snapshots(snapshot1: MemorySnapshot, snapshot2: MemorySnapshot) -> Dict[str, Any]:
    """
    比较两个内存快照

    Args:
        snapshot1: 第一个快照
        snapshot2: 第二个快照

    Returns:
        比较结果
    """
    # 计算内存使用变化
    memory_diff = {
        "rss_mb": snapshot2.usage.rss_mb - snapshot1.usage.rss_mb,
        "vms_mb": snapshot2.usage.vms_mb - snapshot1.usage.rss_mb,
        "shared_mb": snapshot2.usage.shared_mb - snapshot1.usage.shared_mb,
        "text_mb": snapshot2.usage.text_mb - snapshot1.usage.text_mb,
        "data_mb": snapshot2.usage.data_mb - snapshot1.usage.data_mb,
    }

    # 计算对象计数变化
    object_diffs = {}
    all_types = set(snapshot1.object_counts.keys()) | set(snapshot2.object_counts.keys())

    for obj_type in all_types:
        count1 = snapshot1.object_counts.get(obj_type, 0)
        count2 = snapshot2.object_counts.get(obj_type, 0)
        diff = count2 - count1
        if diff != 0:
            object_diffs[obj_type] = {"before": count1, "after": count2, "diff": diff}

    # 计算时间差
    time_diff = snapshot2.timestamp - snapshot1.timestamp

    return {
        "time_elapsed": time_diff,
        "memory_diff": memory_diff,
        "object_diffs": object_diffs,
        "gc_collections_diff": (
            snapshot2.gc_stats["collections"][0] - snapshot1.gc_stats["collections"][0],
            snapshot2.gc_stats["collections"][1] - snapshot1.gc_stats["collections"][1],
            snapshot2.gc_stats["collections"][2] - snapshot1.gc_stats["collections"][2],
        ),
    }


def generate_memory_report(snapshot: Optional[MemorySnapshot] = None) -> Dict[str, Any]:
    """
    生成内存报告

    Args:
        snapshot: 内存快照（可选）

    Returns:
        内存报告
    """
    if snapshot is None:
        snapshot = take_memory_snapshot()

    # 获取对象计数
    object_counts = snapshot.object_counts
    total_objects = sum(object_counts.values())

    # 获取前N个对象类型
    top_objects = dict(sorted(object_counts.items(), key=lambda x: x[1], reverse=True)[:10])

    # 计算百分比
    top_percentages = {
        obj_type: (count / total_objects * 100) if total_objects > 0 else 0
        for obj_type, count in top_objects.items()
    }

    # 检查潜在的内存泄漏
    potential_leaks = []
    for obj_type, count in object_counts.items():
        # 简单启发式：某些类型的对象数量过多可能表示泄漏
        if count > 1000 and obj_type in ["list", "dict", "tuple", "str", "bytes"]:
            potential_leaks.append(
                {
                    "type": obj_type,
                    "count": count,
                    "percentage": (count / total_objects * 100) if total_objects > 0 else 0,
                }
            )

    return {
        "timestamp": snapshot.timestamp,
        "memory_usage": {
            "rss_mb": snapshot.usage.rss_mb,
            "vms_mb": snapshot.usage.vms_mb,
            "shared_mb": snapshot.usage.shared_mb,
            "text_mb": snapshot.usage.text_mb,
            "data_mb": snapshot.usage.data_mb,
        },
        "gc_stats": snapshot.gc_stats,
        "object_stats": {
            "total_objects": total_objects,
            "unique_types": len(object_counts),
            "top_objects": top_objects,
            "top_percentages": top_percentages,
        },
        "potential_leaks": potential_leaks,
        "recommendations": _generate_memory_recommendations(snapshot),
    }


def _generate_memory_recommendations(snapshot: MemorySnapshot) -> List[str]:
    """生成内存优化建议"""
    recommendations = []

    # 分析对象计数
    object_counts = snapshot.object_counts
    total_objects = sum(object_counts.values())

    # 检查是否有大量重复的小对象
    if object_counts.get("str", 0) > 10000:
        recommendations.append("检测到大量字符串对象，考虑使用字符串驻留或缓存")

    if object_counts.get("list", 0) > 5000:
        recommendations.append("检测到大量列表对象，考虑使用数组或更高效的数据结构")

    if object_counts.get("dict", 0) > 5000:
        recommendations.append("检测到大量字典对象，考虑使用命名元组或数据类")

    # 检查内存使用
    if snapshot.usage.rss_mb > 100:  # 超过100MB
        recommendations.append("内存使用较高，考虑优化数据结构或使用内存分析工具")

    # 检查GC状态
    if not snapshot.gc_stats["enabled"]:
        recommendations.append("垃圾回收已禁用，建议启用以自动管理内存")

    # 通用建议
    if total_objects > 100000:
        recommendations.append("对象数量过多，考虑使用对象池或享元模式")

    if len(recommendations) == 0:
        recommendations.append("内存使用正常，无需特殊优化")

    return recommendations


class MemoryProfiler:
    """内存分析器"""

    def __init__(self, name: str = "内存分析"):
        """
        初始化内存分析器

        Args:
            name: 分析器名称
        """
        self.name = name
        self.snapshots: List[MemorySnapshot] = []
        self.start_time = time.time()

    def start(self) -> None:
        """开始分析"""
        self.snapshots.clear()
        self.start_time = time.time()
        self.take_snapshot("开始")

    def take_snapshot(self, label: str = "") -> MemorySnapshot:
        """
        获取内存快照

        Args:
            label: 快照标签

        Returns:
            内存快照
        """
        snapshot = take_memory_snapshot()
        snapshot.label = label
        snapshot.sequence = len(self.snapshots)
        self.snapshots.append(snapshot)
        return snapshot

    def stop(self) -> Dict[str, Any]:
        """
        停止分析并生成报告

        Returns:
            分析报告
        """
        self.take_snapshot("结束")

        if len(self.snapshots) < 2:
            return {
                "name": self.name,
                "duration": time.time() - self.start_time,
                "snapshots": len(self.snapshots),
                "error": "需要至少两个快照才能进行分析",
            }

        # 计算总体变化
        first_snapshot = self.snapshots[0]
        last_snapshot = self.snapshots[-1]
        overall_diff = compare_snapshots(first_snapshot, last_snapshot)

        # 计算每个阶段的变化
        stage_diffs = []
        for i in range(len(self.snapshots) - 1):
            diff = compare_snapshots(self.snapshots[i], self.snapshots[i + 1])
            stage_diffs.append(
                {"from": self.snapshots[i].label, "to": self.snapshots[i + 1].label, "diff": diff}
            )

        # 生成报告
        report = {
            "name": self.name,
            "duration": time.time() - self.start_time,
            "start_time": self.start_time,
            "end_time": time.time(),
            "snapshots": len(self.snapshots),
            "overall_diff": overall_diff,
            "stage_diffs": stage_diffs,
            "final_report": generate_memory_report(last_snapshot),
        }

        return report

    def __enter__(self):
        """上下文管理器入口"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.stop()
