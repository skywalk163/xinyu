"""
内存工具函数

提供内存使用估算、跟踪、泄漏检测等实用函数。
"""

import gc
import inspect
import linecache
import sys
import time
import tracemalloc
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple

# 使用统一的导入工具
from src.utils.imports import import_optional, with_gc, with_psutil, with_time, with_tracemalloc
from src.utils.logging_utils import get_logger

# 导入可选模块
psutil = import_optional("psutil")
objgraph = import_optional("objgraph")
OBJGRAPH_AVAILABLE = objgraph is not None


@dataclass
class MemoryUsage:
    """内存使用信息"""

    rss_mb: float  # 常驻内存
    vms_mb: float  # 虚拟内存
    shared_mb: float  # 共享内存
    text_mb: float  # 代码段内存
    data_mb: float  # 数据段内存
    lib_mb: float  # 库内存
    dirty_mb: float  # 脏页内存
    percent: float  # 内存使用百分比


@dataclass
class ObjectInfo:
    """对象信息"""

    type_name: str
    count: int
    total_size: int
    average_size: float
    references: List[str] = None


def get_memory_usage() -> Optional[MemoryUsage]:
    """
    获取当前进程的内存使用情况

    Returns:
        MemoryUsage: 内存使用信息，如果psutil不可用则返回None
    """
    if psutil is None:
        return None

    try:
        process = psutil.Process()
        memory_info = process.memory_info()

        # 在Windows上，有些字段可能不可用
        try:
            shared = memory_info.shared
        except AttributeError:
            shared = 0

        try:
            text = memory_info.text
        except AttributeError:
            text = 0

        try:
            data = memory_info.data
        except AttributeError:
            data = 0

        try:
            lib = memory_info.lib
        except AttributeError:
            lib = 0

        try:
            dirty = memory_info.dirty
        except AttributeError:
            dirty = 0

        return MemoryUsage(
            rss_mb=memory_info.rss / 1024 / 1024,
            vms_mb=memory_info.vms / 1024 / 1024,
            shared_mb=shared / 1024 / 1024,
            text_mb=text / 1024 / 1024,
            data_mb=data / 1024 / 1024,
            lib_mb=lib / 1024 / 1024,
            dirty_mb=dirty / 1024 / 1024,
            percent=process.memory_percent(),
        )
    except Exception:
        return None


def estimate_memory_usage(obj: Any, seen: Optional[set] = None) -> int:
    """
    估算对象的内存使用量

    Args:
        obj: 要估算的对象
        seen: 已处理对象的集合（用于避免循环引用）

    Returns:
        int: 估算的内存使用量（字节）
    """
    if seen is None:
        seen = set()

    # 避免循环引用
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)

    size = sys.getsizeof(obj)

    # 递归估算容器对象
    if isinstance(obj, dict):
        size += sum(
            estimate_memory_usage(k, seen) + estimate_memory_usage(v, seen) for k, v in obj.items()
        )
    elif isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(estimate_memory_usage(item, seen) for item in obj)

    return size


def track_memory_allocation(func: Callable, *args, **kwargs) -> Tuple[Any, int]:
    """
    跟踪函数执行期间的内存分配

    Args:
        func: 要跟踪的函数
        *args: 函数参数
        **kwargs: 函数关键字参数

    Returns:
        Tuple[Any, int]: (函数返回值, 分配的内存字节数)
    """
    # 启用tracemalloc
    tracemalloc.start()

    # 获取初始快照
    snapshot1 = tracemalloc.take_snapshot()

    # 执行函数
    _ = (*args, **kwargs)  # 未使用变量

    # 获取结束快照
    snapshot2 = tracemalloc.take_snapshot()

    # 计算内存分配差异
    stats = snapshot2.compare_to(snapshot1, "lineno")

    # 停止tracemalloc
    tracemalloc.stop()

    # 计算总分配内存
    total_allocated = sum(stat.size for stat in stats if stat.size_diff > 0)

    return result, total_allocated


def find_memory_leaks(
    snapshot_interval: float = 1.0, duration: float = 10.0, top_n: int = 10
) -> List[Dict[str, Any]]:
    """
    查找内存泄漏

    Args:
        snapshot_interval: 快照间隔（秒）
        duration: 检查持续时间（秒）
        top_n: 返回前N个可疑泄漏

    Returns:
        List[Dict[str, Any]]: 可疑泄漏列表
    """
    # 启用tracemalloc
    tracemalloc.start()

    # 获取初始快照
    snapshot1 = tracemalloc.take_snapshot()

    # 等待一段时间
    time.sleep(duration)

    # 获取结束快照
    snapshot2 = tracemalloc.take_snapshot()

    # 比较快照
    top_stats = snapshot2.compare_to(snapshot1, "lineno")

    # 停止tracemalloc
    tracemalloc.stop()

    # 分析可疑泄漏
    leaks = []
    for stat in top_stats[:top_n]:
        if stat.size_diff > 0:  # 只关注内存增长
            # 获取代码位置信息
            frame = stat.traceback[0]
            filename = frame.filename
            lineno = frame.lineno

            # 获取代码行
            try:
                line = linecache.getline(filename, lineno).strip()
            except Exception:
                line = "无法获取代码行"

            leaks.append(
                {
                    "size_diff": stat.size_diff,
                    "size_diff_mb": stat.size_diff / 1024 / 1024,
                    "count_diff": stat.count_diff,
                    "filename": filename,
                    "lineno": lineno,
                    "line": line,
                    "traceback": [str(frame) for frame in stat.traceback],
                }
            )

    return leaks


def analyze_object_types(limit: int = 20) -> List[ObjectInfo]:
    """
    分析内存中的对象类型

    Args:
        limit: 返回的对象类型数量限制

    Returns:
        List[ObjectInfo]: 对象类型分析结果
    """
    # 获取所有对象
    all_objects = gc.get_objects()

    # 按类型分组
    type_counts = defaultdict(int)
    type_sizes = defaultdict(int)

    for obj in all_objects:
        obj_type = type(obj).__name__
        type_counts[obj_type] += 1
        type_sizes[obj_type] += sys.getsizeof(obj)

    # 计算统计信息
    object_infos = []
    for type_name, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:limit]:
        total_size = type_sizes[type_name]
        average_size = total_size / count if count > 0 else 0

        # 获取对象引用信息
        sample_objects = [obj for obj in all_objects if type(obj).__name__ == type_name][:5]
        references = []

        for obj in sample_objects:
            try:
                referrers = gc.get_referrers(obj)[:3]  # 只取前3个引用者
                ref_types = [type(ref).__name__ for ref in referrers]
                references.extend(ref_types)
            except Exception:
                pass

        object_infos.append(
            ObjectInfo(
                type_name=type_name,
                count=count,
                total_size=total_size,
                average_size=average_size,
                references=list(set(references))[:5] if references else [],
            )
        )

    return object_infos


def optimize_memory_usage(
    target_mb: Optional[float] = None, aggressive: bool = False
) -> Dict[str, Any]:
    """
    优化内存使用

    Args:
        target_mb: 目标内存使用量（MB），如果为None则尽可能优化
        aggressive: 是否使用激进优化策略

    Returns:
        Dict[str, Any]: 优化结果
    """
    results = {
        "before_memory_mb": get_memory_usage().rss_mb,
        "after_memory_mb": 0.0,
        "memory_saved_mb": 0.0,
        "objects_collected": 0,
        "optimizations_applied": [],
    }

    # 记录初始对象数量
    initial_objects = len(gc.get_objects())

    # 应用优化策略
    optimizations = []

    # 1. 强制垃圾回收
    if aggressive:
        collected = gc.collect(2)  # 收集所有代
        optimizations.append(
            {
                "name": "强制垃圾回收",
                "description": f"回收了 {collected} 个对象",
                "memory_saved_mb": 0.0,  # 实际节省的内存需要测量
            }
        )

    # 2. 清除模块缓存（在Python 3.12中跳过，因为sys.path_importer_cache已移除）
    if aggressive:
        try:
            cleared_modules = clear_module_caches()
            optimizations.append(
                {
                    "name": "清除模块缓存",
                    "description": f"清除了 {cleared_modules} 个模块的缓存",
                    "memory_saved_mb": 0.0,
                }
            )
        except AttributeError as e:
            # 在Python 3.12中，sys.path_importer_cache可能不存在
            optimizations.append(
                {"name": "清除模块缓存", "description": f"跳过：{str(e)}", "memory_saved_mb": 0.0}
            )

    # 3. 清除循环引用
    if aggressive:
        cleared_cycles = clear_cyclic_references()
        optimizations.append(
            {"name": "清除循环引用", "description": f"清除了 {cleared_cycles} 个循环引用", "memory_saved_mb": 0.0}
        )

    # 4. 清除大对象
    if target_mb is not None:
        current_memory = get_memory_usage().rss_mb
        if current_memory > target_mb:
            cleared = clear_large_objects(target_mb)
            optimizations.append(
                {
                    "name": "清除大对象",
                    "description": f"清除了 {cleared} 个大对象",
                    "memory_saved_mb": current_memory - get_memory_usage().rss_mb,
                }
            )

    # 记录最终对象数量
    final_objects = len(gc.get_objects())
    results["objects_collected"] = initial_objects - final_objects

    # 记录最终内存使用
    results["after_memory_mb"] = get_memory_usage().rss_mb
    results["memory_saved_mb"] = results["before_memory_mb"] - results["after_memory_mb"]
    results["optimizations_applied"] = optimizations

    return results


def clear_module_caches() -> int:
    """
    清除模块缓存

    Returns:
        int: 清除的模块数量
    """
    cleared = 0

    # 清除模块的缓存属性
    for module_name, module in list(sys.modules.items()):
        try:
            if module is None:
                continue

            if hasattr(module, "__dict__"):
                cache_attrs = []
                for attr_name in module.__dict__.keys():
                    # 查找缓存属性
                    if (
                        attr_name.startswith("_cache_")
                        or attr_name.endswith("_cache")
                        or attr_name == "__cache__"
                        or attr_name.startswith("cache_")
                    ):
                        cache_attrs.append(attr_name)

                for attr_name in cache_attrs:
                    try:
                        delattr(module, attr_name)
                        cleared += 1
                    except (AttributeError, TypeError):
                        # 某些属性可能无法删除
                        pass
        except (AttributeError, TypeError):
            # 某些模块可能无法访问__dict__
            pass

    return cleared


def clear_cyclic_references() -> int:
    """
    清除循环引用

    Returns:
        int: 清除的循环引用数量
    """
    # 查找循环引用
    cycles = gc.collect()

    # 获取无法回收的对象
    garbage = gc.garbage
    cleared = len(garbage)

    # 尝试清除循环引用
    for obj in garbage:
        # 断开循环引用
        if hasattr(obj, "__dict__"):
            obj.__dict__.clear()
        if hasattr(obj, "__weakref__"):
            obj.__weakref__ = None

    # 清空垃圾列表
    gc.garbage.clear()

    return cleared


def clear_large_objects(target_mb: float) -> int:
    """
    清除大对象以达到目标内存使用量

    Args:
        target_mb: 目标内存使用量（MB）

    Returns:
        int: 清除的大对象数量
    """
    cleared = 0
    current_memory = get_memory_usage().rss_mb

    while current_memory > target_mb and cleared < 100:  # 最多清除100个对象
        # 查找大对象
        large_objects = []
        for obj in gc.get_objects():
            try:
                size = sys.getsizeof(obj)
                if size > 1024 * 1024:  # 大于1MB的对象
                    large_objects.append((obj, size))
            except Exception:
                pass

        if not large_objects:
            break

        # 按大小排序
        large_objects.sort(key=lambda x: x[1], reverse=True)

        # 清除最大的对象
        obj, size = large_objects[0]

        # 尝试删除对象引用
        try:
            # 查找并删除引用
            referrers = gc.get_referrers(obj)
            for referrer in referrers:
                if isinstance(referrer, dict):
                    for key, value in list(referrer.items()):
                        if value is obj:
                            del referrer[key]
                            cleared += 1
                elif isinstance(referrer, (list, tuple, set)):
                    if obj in referrer:
                        referrer.remove(obj)
                        cleared += 1
        except Exception:
            pass

        # 更新当前内存使用
        current_memory = get_memory_usage().rss_mb

    return cleared


def monitor_memory_growth(
    interval: float = 1.0, duration: float = 30.0, threshold_mb: float = 10.0
) -> Dict[str, Any]:
    """
    监控内存增长

    Args:
        interval: 检查间隔（秒）
        duration: 监控持续时间（秒）
        threshold_mb: 内存增长阈值（MB）

    Returns:
        Dict[str, Any]: 监控结果
    """
    start_time = time.time()
    start_memory = get_memory_usage().rss_mb
    measurements = []

    logger = get_logger("memory.utils")
    logger.info(f"开始监控内存增长，持续时间: {duration}秒，间隔: {interval}秒")

    while time.time() - start_time < duration:
        current_memory = get_memory_usage().rss_mb
        elapsed = time.time() - start_time

        measurements.append(
            {
                "time": elapsed,
                "memory_mb": current_memory,
                "growth_mb": current_memory - start_memory,
            }
        )

        # 检查是否超过阈值
        if current_memory - start_memory > threshold_mb:
            logger.warning(f"内存增长超过阈值 ({current_memory - start_memory:.2f}MB > {threshold_mb}MB)")

            # 分析对象类型
            object_analysis = analyze_object_types(limit=10)

            return {
                "memory_growth_mb": current_memory - start_memory,
                "duration_seconds": elapsed,
                "exceeded_threshold": True,
                "threshold_mb": threshold_mb,
                "measurements": measurements,
                "object_analysis": [obj.__dict__ for obj in object_analysis],
            }

        time.sleep(interval)

    end_memory = get_memory_usage().rss_mb
    growth = end_memory - start_memory

    return {
        "memory_growth_mb": growth,
        "duration_seconds": duration,
        "exceeded_threshold": False,
        "threshold_mb": threshold_mb,
        "measurements": measurements,
        "object_analysis": [],
    }


def generate_memory_report(output_file: Optional[str] = None) -> Dict[str, Any]:
    """
    生成内存使用报告

    Args:
        output_file: 输出文件路径（可选）

    Returns:
        Dict[str, Any]: 报告数据
    """
    # 获取内存使用信息
    memory_usage = get_memory_usage()

    # 分析对象类型
    object_analysis = analyze_object_types(limit=20)

    # 检查内存泄漏
    leaks = find_memory_leaks(duration=2.0, top_n=5)

    # 获取GC统计
    gc_stats = gc.get_stats()
    gc_counts = gc.get_count()

    # 构建报告
    report = {
        "timestamp": time.time(),
        "datetime": time.strftime("%Y-%m-%d %H:%M:%S"),
        "memory_usage": {
            "rss_mb": memory_usage.rss_mb,
            "vms_mb": memory_usage.vms_mb,
            "percent": memory_usage.percent,
            "available_mb": psutil.virtual_memory().available / 1024 / 1024,
            "total_mb": psutil.virtual_memory().total / 1024 / 1024,
        },
        "gc_stats": {
            "collections": gc_stats,
            "counts": gc_counts,
            "thresholds": gc.get_threshold(),
            "enabled": gc.isenabled(),
            "debug": gc.get_debug(),
        },
        "object_analysis": [obj.__dict__ for obj in object_analysis],
        "potential_leaks": leaks,
        "recommendations": generate_recommendations(memory_usage, object_analysis, leaks),
    }

    # 输出报告
    if output_file:
        import json

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, default=str)

    return report


def generate_recommendations(
    memory_usage: MemoryUsage, object_analysis: List[ObjectInfo], leaks: List[Dict[str, Any]]
) -> List[str]:
    """生成优化建议"""
    recommendations = []

    # 内存使用建议
    if memory_usage.percent > 80:
        recommendations.append("内存使用率超过80%，考虑优化内存使用或增加系统内存")

    if memory_usage.rss_mb > 500:  # 500MB阈值
        recommendations.append("进程内存使用超过500MB，检查是否有内存泄漏")

    # 对象数量建议
    total_objects = sum(obj.count for obj in object_analysis)
    if total_objects > 100000:
        recommendations.append(f"对象数量过多 ({total_objects})，考虑使用对象池或减少对象创建")

    # 大对象建议
    large_objects = [obj for obj in object_analysis if obj.average_size > 1024 * 1024]  # 大于1MB
    if large_objects:
        recommendations.append(f"发现 {len(large_objects)} 个大对象类型，考虑优化数据结构")

    # 泄漏检测建议
    if leaks:
        recommendations.append(f"检测到 {len(leaks)} 个潜在内存泄漏，请检查相关代码")

    # GC建议
    if not gc.isenabled():
        recommendations.append("垃圾回收未启用，建议启用GC以自动管理内存")

    # 一般建议
    recommendations.append("考虑使用内存分析工具（如memory_profiler）进行详细分析")
    recommendations.append("定期监控内存使用，特别是在处理大文件或长时间运行时")
    recommendations.append("使用对象池复用频繁创建的对象")
    recommendations.append("及时释放不再使用的大对象引用")

    return recommendations


def profile_memory_usage(func: Callable, *args, **kwargs) -> Dict[str, Any]:
    """
    分析函数的内存使用情况

    Args:
        func: 要分析的函数
        *args: 函数参数
        **kwargs: 函数关键字参数

    Returns:
        Dict[str, Any]: 内存分析结果
    """
    # 启用tracemalloc
    tracemalloc.start()

    # 获取初始内存使用
    start_memory = get_memory_usage()
    start_snapshot = tracemalloc.take_snapshot()

    # 执行函数
    start_time = time.time()
    _ = (*args, **kwargs)  # 未使用变量
    execution_time = time.time() - start_time

    # 获取结束内存使用
    end_memory = get_memory_usage()
    end_snapshot = tracemalloc.take_snapshot()

    # 分析内存分配
    stats = end_snapshot.compare_to(start_snapshot, "lineno")

    # 停止tracemalloc
    tracemalloc.stop()

    # 计算统计信息
    total_allocated = sum(stat.size for stat in stats if stat.size_diff > 0)
    total_freed = abs(sum(stat.size for stat in stats if stat.size_diff < 0))
    net_allocated = total_allocated - total_freed

    # 获取内存分配热点
    hotspots = []
    for stat in stats[:10]:  # 前10个热点
        if stat.size_diff > 1024:  # 只关注分配超过1KB的
            frame = stat.traceback[0]
            hotspots.append(
                {
                    "size_diff": stat.size_diff,
                    "size_diff_kb": stat.size_diff / 1024,
                    "count_diff": stat.count_diff,
                    "filename": frame.filename,
                    "lineno": frame.lineno,
                    "line": linecache.getline(frame.filename, frame.lineno).strip(),
                }
            )

    return {
        "function": func.__name__,
        "execution_time_seconds": execution_time,
        "memory_usage": {
            "start_rss_mb": start_memory.rss_mb,
            "end_rss_mb": end_memory.rss_mb,
            "rss_growth_mb": end_memory.rss_mb - start_memory.rss_mb,
            "start_vms_mb": start_memory.vms_mb,
            "end_vms_mb": end_memory.vms_mb,
            "vms_growth_mb": end_memory.vms_mb - start_memory.vms_mb,
        },
        "memory_allocation": {
            "total_allocated_bytes": total_allocated,
            "total_freed_bytes": total_freed,
            "net_allocated_bytes": net_allocated,
            "total_allocated_mb": total_allocated / 1024 / 1024,
            "total_freed_mb": total_freed / 1024 / 1024,
            "net_allocated_mb": net_allocated / 1024 / 1024,
        },
        "allocation_hotspots": hotspots,
        "result": result,
    }
