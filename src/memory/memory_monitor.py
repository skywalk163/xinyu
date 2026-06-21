"""
内存监控器

监控内存使用情况，检测内存泄漏，提供内存使用报告。
"""

import threading
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

# 使用统一的导入工具
from src.utils.imports import import_optional
from src.utils.logging_utils import get_logger

# 导入可选模块
tracemalloc = import_optional("tracemalloc")
gc = import_optional("gc")
psutil = import_optional("psutil")
json = import_optional("json")
os = import_optional("os")


@dataclass
class MemorySnapshot:
    """内存快照"""

    timestamp: float
    current_memory_mb: float
    peak_memory_mb: float
    object_count: int
    gc_collected: int
    gc_uncollectable: int
    snapshot_data: Optional[Any] = None


@dataclass
class MemoryLeakReport:
    """内存泄漏报告"""

    timestamp: float
    duration_seconds: float
    memory_growth_mb: float
    suspicious_objects: List[Dict[str, Any]]
    recommendations: List[str]
    snapshot_comparison: Optional[Dict[str, Any]] = None


class MemoryMonitor:
    """
    内存监控器

    提供：
    1. 实时内存使用监控
    2. 内存泄漏检测
    3. 内存使用报告
    4. 自动垃圾回收触发
    """

    def __init__(
        self,
        check_interval: float = 5.0,
        memory_threshold_mb: float = 100.0,
        enable_auto_gc: bool = True,
        logger_name: str = "memory_monitor",
    ):
        """
        初始化内存监控器

        Args:
            check_interval: 检查间隔（秒）
            memory_threshold_mb: 内存阈值（MB），超过此值触发警告
            enable_auto_gc: 是否启用自动垃圾回收
            logger_name: 日志器名称
        """
        self.check_interval = check_interval
        self.memory_threshold_mb = memory_threshold_mb
        self.enable_auto_gc = enable_auto_gc
        self.logger = get_logger(logger_name)

        self._snapshots: List[MemorySnapshot] = []
        self._leak_reports: List[MemoryLeakReport] = []
        self._monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._lock = threading.RLock()

        # 回调函数
        self._on_memory_warning: Optional[Callable] = None
        self._on_leak_detected: Optional[Callable] = None

        # 启用tracemalloc
        if tracemalloc:
            tracemalloc.start()
            self.logger.info("tracemalloc已启用")
        else:
            self.logger.warning("tracemalloc不可用，内存跟踪功能受限")

    def start_monitoring(self) -> None:
        """开始监控内存"""
        if self._monitoring:
            return

        self._monitoring = True
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop, daemon=True, name="MemoryMonitor"
        )
        self._monitor_thread.start()

    def stop_monitoring(self) -> None:
        """停止监控内存"""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=2.0)
            self._monitor_thread = None

    def _monitor_loop(self) -> None:
        """监控循环"""
        while self._monitoring:
            try:
                self._check_memory()
                time.sleep(self.check_interval)
            except Exception as e:
                self.logger.error(f"内存监控错误: {e}")

    def _check_memory(self) -> None:
        """检查内存使用情况"""
        with self._lock:
            # 获取当前内存使用
            current_memory_mb = 0.0
            peak_memory_mb = 0.0
            object_count = 0
            total_collected = 0
            total_uncollectable = 0

            if psutil:
                try:
                    process = psutil.Process()
                    memory_info = process.memory_info()
                    current_memory_mb = memory_info.rss / 1024 / 1024
                    peak_memory_mb = process.memory_info().vms / 1024 / 1024
                except Exception as e:
                    self.logger.warning(f"获取内存信息失败: {e}")

            # 获取GC统计
            if gc:
                try:
                    gc.collect()
                    gc_stats = gc.get_stats()
                    total_collected = sum(stat["collected"] for stat in gc_stats)
                    total_uncollectable = sum(stat["uncollectable"] for stat in gc_stats)
                    object_count = len(gc.get_objects())
                except Exception as e:
                    self.logger.warning(f"获取GC统计失败: {e}")

            # 创建快照
            snapshot = MemorySnapshot(
                timestamp=time.time(),
                current_memory_mb=current_memory_mb,
                peak_memory_mb=peak_memory_mb,
                object_count=object_count,
                gc_collected=total_collected,
                gc_uncollectable=total_uncollectable,
                snapshot_data=tracemalloc.take_snapshot() if tracemalloc.is_tracing() else None,
            )

            self._snapshots.append(snapshot)

            # 检查内存阈值
            if current_memory_mb > self.memory_threshold_mb:
                self._handle_memory_warning(current_memory_mb)

            # 检查内存泄漏
            if len(self._snapshots) >= 3:
                self._check_for_leaks()

            # 自动垃圾回收
            if self.enable_auto_gc and current_memory_mb > self.memory_threshold_mb * 0.8:
                gc.collect()

    def _handle_memory_warning(self, memory_mb: float) -> None:
        """处理内存警告"""
        warning_msg = f"内存使用超过阈值: {memory_mb:.2f}MB > {self.memory_threshold_mb:.2f}MB"
        self.logger.warning(warning_msg)

        if self._on_memory_warning:
            try:
                self._on_memory_warning(memory_mb, self.memory_threshold_mb)
            except Exception as e:
                self.logger.error(f"内存警告回调错误: {e}")

    def _check_for_leaks(self) -> Optional[MemoryLeakReport]:
        """检查内存泄漏"""
        if len(self._snapshots) < 3:
            return None

        # 获取最近3个快照
        recent_snapshots = self._snapshots[-3:]

        # 计算内存增长
        memory_growth = (
            recent_snapshots[-1].current_memory_mb - recent_snapshots[0].current_memory_mb
        )
        time_diff = recent_snapshots[-1].timestamp - recent_snapshots[0].timestamp

        # 如果内存持续增长且时间间隔足够长，可能发生泄漏
        if memory_growth > 10.0 and time_diff > 30.0:  # 30秒内增长超过10MB
            # 分析可疑对象
            suspicious_objects = self._find_suspicious_objects()

            # 创建泄漏报告
            report = MemoryLeakReport(
                timestamp=time.time(),
                duration_seconds=time_diff,
                memory_growth_mb=memory_growth,
                suspicious_objects=suspicious_objects,
                recommendations=["检查循环引用", "检查缓存大小", "检查大对象分配", "考虑手动触发垃圾回收"],
            )

            self._leak_reports.append(report)

            if self._on_leak_detected:
                try:
                    self._on_leak_detected(report)
                except Exception as e:
                    self.logger.error(f"泄漏检测回调错误: {e}")

            return report

        return None

    def _find_suspicious_objects(self) -> List[Dict[str, Any]]:
        """查找可疑对象（可能的内存泄漏源）"""
        suspicious = []

        if not gc:
            self.logger.warning("GC不可用，无法查找可疑对象")
            return suspicious

        try:
            # 获取所有对象
            all_objects = gc.get_objects()

            # 按类型分组
            type_counts = {}
            for obj in all_objects:
                obj_type = type(obj).__name__
                type_counts[obj_type] = type_counts.get(obj_type, 0) + 1

            # 找出数量最多的类型
            for obj_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[
                :10
            ]:
                # 检查是否有异常多的对象
                if count > 1000:  # 阈值可以根据需要调整
                    suspicious.append(
                        {"type": obj_type, "count": count, "reason": f"对象数量异常多: {count}"}
                    )
        except Exception as e:
            self.logger.error(f"查找可疑对象失败: {e}")

        return suspicious

    def take_snapshot(self, name: str = "") -> MemorySnapshot:
        """
        手动创建内存快照

        Args:
            name: 快照名称

        Returns:
            内存快照
        """
        with self._lock:
            process = psutil.Process()
            memory_info = process.memory_info()

            gc.collect()
            gc_stats = gc.get_stats()
            total_collected = sum(stat["collected"] for stat in gc_stats)
            total_uncollectable = sum(stat["uncollectable"] for stat in gc_stats)

            snapshot = MemorySnapshot(
                timestamp=time.time(),
                current_memory_mb=memory_info.rss / 1024 / 1024,
                peak_memory_mb=process.memory_info().vms / 1024 / 1024,
                object_count=len(gc.get_objects()),
                gc_collected=total_collected,
                gc_uncollectable=total_uncollectable,
                snapshot_data=tracemalloc.take_snapshot() if tracemalloc.is_tracing() else None,
            )

            self._snapshots.append(snapshot)
            return snapshot

    def compare_snapshots(
        self, snapshot1: MemorySnapshot, snapshot2: MemorySnapshot
    ) -> Dict[str, Any]:
        """
        比较两个内存快照

        Args:
            snapshot1: 第一个快照
            snapshot2: 第二个快照

        Returns:
            比较结果
        """
        return {
            "time_diff_seconds": snapshot2.timestamp - snapshot1.timestamp,
            "memory_growth_mb": snapshot2.current_memory_mb - snapshot1.current_memory_mb,
            "object_growth": snapshot2.object_count - snapshot1.object_count,
            "gc_collected_dif": snapshot2.gc_collected - snapshot1.gc_collected,
            "gc_uncollectable_dif": snapshot2.gc_uncollectable - snapshot1.gc_uncollectable,
            "memory_growth_percent": (
                (snapshot2.current_memory_mb - snapshot1.current_memory_mb)
                / snapshot1.current_memory_mb
                * 100
                if snapshot1.current_memory_mb > 0
                else 0
            ),
        }

    def get_memory_stats(self) -> Dict[str, Any]:
        """
        获取当前内存统计

        Returns:
            内存统计信息
        """
        process = psutil.Process()
        memory_info = process.memory_info()

        return {
            "current_memory_mb": memory_info.rss / 1024 / 1024,
            "peak_memory_mb": process.memory_info().vms / 1024 / 1024,
            "available_memory_mb": psutil.virtual_memory().available / 1024 / 1024,
            "total_memory_mb": psutil.virtual_memory().total / 1024 / 1024,
            "memory_percent": process.memory_percent(),
            "object_count": len(gc.get_objects()),
            "gc_generation_counts": [len(gc.get_objects(i)) for i in range(3)],
            "timestamp": time.time(),
        }

    def generate_report(
        self, output_file: Optional[str] = None, format: str = "json"
    ) -> Dict[str, Any]:
        """
        生成内存使用报告

        Args:
            output_file: 输出文件路径（可选）
            format: 报告格式（'json' 或 'text'）

        Returns:
            报告数据
        """
        with self._lock:
            if not self._snapshots:
                return {"error": "没有可用的快照数据"}

            # 计算统计信息
            current_stats = self.get_memory_stats()
            first_snapshot = self._snapshots[0]
            last_snapshot = self._snapshots[-1]

            comparison = self.compare_snapshots(first_snapshot, last_snapshot)

            report = {
                "generated_at": datetime.now().isoformat(),
                "monitoring_duration_seconds": last_snapshot.timestamp - first_snapshot.timestamp,
                "current_stats": current_stats,
                "snapshot_comparison": comparison,
                "total_snapshots": len(self._snapshots),
                "leak_reports_count": len(self._leak_reports),
                "recent_leak_reports": [asdict(report) for report in self._leak_reports[-5:]]
                if self._leak_reports
                else [],
                "recommendations": self._generate_recommendations(current_stats, comparison),
            }

            # 输出报告
            if format == "json":
                report_str = json.dumps(report, indent=2, default=str)
            else:  # text格式
                report_str = self._format_text_report(report)

            if output_file:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(report_str)

            return report

    def _generate_recommendations(
        self, stats: Dict[str, Any], comparison: Dict[str, Any]
    ) -> List[str]:
        """生成优化建议"""
        recommendations = []

        # 内存使用建议
        memory_percent = stats["memory_percent"]
        if memory_percent > 80:
            recommendations.append("内存使用率超过80%，考虑优化内存使用")

        # 对象数量建议
        object_count = stats["object_count"]
        if object_count > 100000:
            recommendations.append(f"对象数量过多 ({object_count})，考虑使用对象池")

        # 内存增长建议
        if comparison["memory_growth_mb"] > 50:  # 增长超过50MB
            recommendations.append("内存持续增长，可能存在内存泄漏")

        # GC建议
        if comparison["gc_uncollectable_dif"] > 100:
            recommendations.append("不可回收对象数量增加，检查循环引用")

        return recommendations

    def _format_text_report(self, report: Dict[str, Any]) -> str:
        """格式化文本报告"""
        lines = []
        lines.append("=" * 80)
        lines.append("内存使用报告")
        lines.append("=" * 80)
        lines.append(f"生成时间: {report['generated_at']}")
        lines.append(f"监控时长: {report['monitoring_duration_seconds']:.2f}秒")
        lines.append(f"快照数量: {report['total_snapshots']}")
        lines.append(f"泄漏报告数量: {report['leak_reports_count']}")
        lines.append("")

        # 当前状态
        lines.append("当前内存状态:")
        lines.append("-" * 40)
        stats = report["current_stats"]
        lines.append(f"  当前内存: {stats['current_memory_mb']:.2f} MB")
        lines.append(f"  峰值内存: {stats['peak_memory_mb']:.2f} MB")
        lines.append(f"  可用内存: {stats['available_memory_mb']:.2f} MB")
        lines.append(f"  总内存: {stats['total_memory_mb']:.2f} MB")
        lines.append(f"  内存使用率: {stats['memory_percent']:.1f}%")
        lines.append(f"  对象数量: {stats['object_count']}")
        lines.append(f"  GC代0对象: {stats['gc_generation_counts'][0]}")
        lines.append(f"  GC代1对象: {stats['gc_generation_counts'][1]}")
        lines.append(f"  GC代2对象: {stats['gc_generation_counts'][2]}")
        lines.append("")

        # 比较结果
        lines.append("内存变化:")
        lines.append("-" * 40)
        comp = report["snapshot_comparison"]
        lines.append(f"  时间差: {comp['time_diff_seconds']:.2f}秒")
        lines.append(f"  内存增长: {comp['memory_growth_mb']:.2f} MB")
        lines.append(f"  内存增长率: {comp['memory_growth_percent']:.2f}%")
        lines.append(f"  对象增长: {comp['object_growth']}")
        lines.append(f"  GC回收增长: {comp['gc_collected_diff']}")
        lines.append(f"  不可回收增长: {comp['gc_uncollectable_diff']}")
        lines.append("")

        # 建议
        lines.append("优化建议:")
        lines.append("-" * 40)
        for i, rec in enumerate(report["recommendations"], 1):
            lines.append(f"  {i}. {rec}")

        lines.append("=" * 80)
        return "\n".join(lines)

    def set_memory_warning_callback(self, callback: Callable) -> None:
        """设置内存警告回调函数"""
        self._on_memory_warning = callback

    def set_leak_detection_callback(self, callback: Callable) -> None:
        """设置泄漏检测回调函数"""
        self._on_leak_detected = callback

    def __enter__(self):
        """上下文管理器支持"""
        self.start_monitoring()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出时停止监控"""
        self.stop_monitoring()
        if tracemalloc.is_tracing():
            tracemalloc.stop()


# 全局内存监控器实例
_global_monitor: Optional[MemoryMonitor] = None


def get_memory_monitor(
    check_interval: float = 5.0, memory_threshold_mb: float = 100.0
) -> MemoryMonitor:
    """获取全局内存监控器实例"""
    global _global_monitor
    if _global_monitor is None:
        _global_monitor = MemoryMonitor(
            check_interval=check_interval, memory_threshold_mb=memory_threshold_mb
        )
    return _global_monitor


def start_memory_monitoring(
    check_interval: float = 5.0, memory_threshold_mb: float = 100.0
) -> MemoryMonitor:
    """启动内存监控"""
    monitor = get_memory_monitor(check_interval, memory_threshold_mb)
    monitor.start_monitoring()
    return monitor


def stop_memory_monitoring() -> None:
    """停止内存监控"""
    global _global_monitor
    if _global_monitor:
        _global_monitor.stop_monitoring()


def get_memory_usage() -> Dict[str, float]:
    """获取当前内存使用情况"""
    process = psutil.Process()
    memory_info = process.memory_info()

    return {
        "rss_mb": memory_info.rss / 1024 / 1024,  # 常驻内存
        "vms_mb": memory_info.vms / 1024 / 1024,  # 虚拟内存
        "percent": process.memory_percent(),
        "available_mb": psutil.virtual_memory().available / 1024 / 1024,
        "total_mb": psutil.virtual_memory().total / 1024 / 1024,
    }


def check_for_memory_leaks(
    snapshot_interval: float = 10.0, duration: float = 60.0
) -> Optional[MemoryLeakReport]:
    """
    检查内存泄漏

    Args:
        snapshot_interval: 快照间隔（秒）
        duration: 检查持续时间（秒）

    Returns:
        泄漏报告或None
    """
    monitor = MemoryMonitor(check_interval=snapshot_interval)

    with monitor:
        time.sleep(duration)

    if monitor._leak_reports:
        return monitor._leak_reports[-1]

    return None
