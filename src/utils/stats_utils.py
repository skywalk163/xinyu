"""
统计工具模块

提供统一的统计计算功能，减少重复的统计计算代码。
"""

import math
import statistics
import time
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple


def calculate_statistics(data: List[float]) -> Dict[str, float]:
    """
    计算基本统计信息

    Args:
        data: 数据列表

    Returns:
        统计信息字典
    """
    if not data:
        return {
            "count": 0,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "min": 0.0,
            "max": 0.0,
            "sum": 0.0,
        }

    try:
        return {
            "count": len(data),
            "mean": statistics.mean(data),
            "median": statistics.median(data),
            "std": statistics.stdev(data) if len(data) > 1 else 0.0,
            "min": min(data),
            "max": max(data),
            "sum": sum(data),
        }
    except (statistics.StatisticsError, ValueError):
        # 如果数据有问题，返回简单统计
        return {
            "count": len(data),
            "mean": sum(data) / len(data) if data else 0.0,
            "median": sorted(data)[len(data) // 2] if data else 0.0,
            "std": 0.0,
            "min": min(data) if data else 0.0,
            "max": max(data) if data else 0.0,
            "sum": sum(data),
        }


def calculate_percentiles(
    data: List[float], percentiles: List[float] = [25, 50, 75, 90, 95, 99]
) -> Dict[str, float]:
    """
    计算百分位数

    Args:
        data: 数据列表
        percentiles: 百分位数列表

    Returns:
        百分位数字典
    """
    if not data:
        return {f"p{p}": 0.0 for p in percentiles}

    sorted_data = sorted(data)
    n = len(sorted_data)

    result = {}
    for p in percentiles:
        if p < 0 or p > 100:
            continue

        # 计算百分位数的位置
        pos = (p / 100) * (n - 1)

        if pos.is_integer():
            # 位置是整数，直接取该位置的值
            idx = int(pos)
            result[f"p{p}"] = sorted_data[idx]
        else:
            # 位置不是整数，进行线性插值
            idx_low = int(math.floor(pos))
            idx_high = int(math.ceil(pos))
            weight_high = pos - idx_low
            weight_low = 1 - weight_high

            result[f"p{p}"] = (
                sorted_data[idx_low] * weight_low + sorted_data[idx_high] * weight_high
            )

    return result


def calculate_confidence_interval(
    data: List[float], confidence: float = 0.95
) -> Tuple[float, float, float]:
    """
    计算置信区间

    Args:
        data: 数据列表
        confidence: 置信水平（0-1）

    Returns:
        (均值, 下限, 上限)
    """
    if len(data) < 2:
        mean_val = data[0] if data else 0.0
        return mean_val, mean_val, mean_val

    try:
        mean_val = statistics.mean(data)
        std_val = statistics.stdev(data)
        n = len(data)

        # 使用t分布计算置信区间
        # 对于大样本，可以使用z分数，这里使用t分布更保守
        from scipy import stats

        try:
            t_value = stats.t.ppf((1 + confidence) / 2, n - 1)
        except (ImportError, AttributeError):
            # 如果没有scipy，使用近似值
            t_value = 1.96  # 95%置信水平的z值

        margin_of_error = t_value * (std_val / math.sqrt(n))

        return mean_val, mean_val - margin_of_error, mean_val + margin_of_error

    except Exception:
        # 如果计算失败，返回简单结果
        mean_val = sum(data) / len(data)
        return mean_val, mean_val, mean_val


def format_statistics(
    stats: Dict[str, Any], precision: int = 4, include_percentiles: bool = True
) -> str:
    """
    格式化统计信息为字符串

    Args:
        stats: 统计信息字典
        precision: 小数精度
        include_percentiles: 是否包含百分位数

    Returns:
        格式化的字符串
    """
    lines = []

    # 基本统计信息
    lines.append(f"数量: {stats.get('count', 0)}")
    lines.append(f"平均值: {stats.get('mean', 0.0):.{precision}f}")
    lines.append(f"中位数: {stats.get('median', 0.0):.{precision}f}")
    lines.append(f"标准差: {stats.get('std', 0.0):.{precision}f}")
    lines.append(f"最小值: {stats.get('min', 0.0):.{precision}f}")
    lines.append(f"最大值: {stats.get('max', 0.0):.{precision}f}")
    lines.append(f"总和: {stats.get('sum', 0.0):.{precision}f}")

    # 百分位数
    if include_percentiles:
        percentiles = stats.get("percentiles", {})
        if percentiles:
            lines.append("\n百分位数:")
            for p_name, p_value in sorted(percentiles.items()):
                lines.append(f"  {p_name}: {p_value:.{precision}f}")

    # 置信区间
    ci = stats.get("confidence_interval", None)
    if ci:
        mean_val, lower, upper = ci
        lines.append(f"\n置信区间 ({stats.get('confidence_level', 0.95)*100:.0f}%):")
        lines.append(f"  均值: {mean_val:.{precision}f}")
        lines.append(f"  下限: {lower:.{precision}f}")
        lines.append(f"  上限: {upper:.{precision}f}")
        lines.append(f"  范围: ±{(upper - lower)/2:.{precision}f}")

    return "\n".join(lines)


def calculate_execution_stats(times: List[float]) -> Dict[str, Any]:
    """
    计算执行时间统计信息

    Args:
        times: 执行时间列表（秒）

    Returns:
        执行统计信息
    """
    if not times:
        return {
            "count": 0,
            "total_time": 0.0,
            "avg_time": 0.0,
            "min_time": 0.0,
            "max_time": 0.0,
            "std_time": 0.0,
            "throughput": 0.0,
        }

    total = sum(times)
    avg = total / len(times)
    min_time = min(times)
    max_time = max(times)

    # 计算标准差
    if len(times) > 1:
        variance = sum((t - avg) ** 2 for t in times) / (len(times) - 1)
        std = math.sqrt(variance)
    else:
        std = 0.0

    # 计算吞吐量（操作/秒）
    throughput = len(times) / total if total > 0 else 0.0

    # 计算百分位数
    percentiles = calculate_percentiles(times)

    # 计算置信区间
    ci = calculate_confidence_interval(times)

    return {
        "count": len(times),
        "total_time": total,
        "avg_time": avg,
        "min_time": min_time,
        "max_time": max_time,
        "std_time": std,
        "throughput": throughput,
        "percentiles": percentiles,
        "confidence_interval": ci,
        "confidence_level": 0.95,
    }


def calculate_memory_stats(memory_samples: List[float]) -> Dict[str, Any]:
    """
    计算内存使用统计信息

    Args:
        memory_samples: 内存样本列表（MB）

    Returns:
        内存统计信息
    """
    if not memory_samples:
        return {
            "samples": 0,
            "avg_memory": 0.0,
            "min_memory": 0.0,
            "max_memory": 0.0,
            "peak_memory": 0.0,
            "memory_growth": 0.0,
        }

    avg_memory = sum(memory_samples) / len(memory_samples)
    min_memory = min(memory_samples)
    max_memory = max(memory_samples)
    peak_memory = max_memory
    memory_growth = memory_samples[-1] - memory_samples[0] if len(memory_samples) > 1 else 0.0

    # 计算百分位数
    percentiles = calculate_percentiles(memory_samples)

    return {
        "samples": len(memory_samples),
        "avg_memory": avg_memory,
        "min_memory": min_memory,
        "max_memory": max_memory,
        "peak_memory": peak_memory,
        "memory_growth": memory_growth,
        "percentiles": percentiles,
    }


def calculate_correlation(x: List[float], y: List[float]) -> Dict[str, float]:
    """
    计算两个变量的相关性

    Args:
        x: 第一个变量列表
        y: 第二个变量列表

    Returns:
        相关性统计信息
    """
    if len(x) != len(y) or len(x) < 2:
        return {"correlation": 0.0, "covariance": 0.0, "r_squared": 0.0}

    try:
        # 计算均值
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)

        # 计算协方差和方差
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / (len(x) - 1)
        var_x = sum((xi - mean_x) ** 2 for xi in x) / (len(x) - 1)
        var_y = sum((yi - mean_y) ** 2 for yi in y) / (len(y) - 1)

        # 计算相关系数
        if var_x > 0 and var_y > 0:
            correlation = cov_xy / math.sqrt(var_x * var_y)
        else:
            correlation = 0.0

        # 计算R平方
        r_squared = correlation**2

        return {"correlation": correlation, "covariance": cov_xy, "r_squared": r_squared}

    except Exception:
        return {"correlation": 0.0, "covariance": 0.0, "r_squared": 0.0}


def calculate_frequency_distribution(data: List[Any], bins: Optional[int] = None) -> Dict[str, Any]:
    """
    计算频率分布

    Args:
        data: 数据列表
        bins: 分组数量（仅对数值数据有效）

    Returns:
        频率分布信息
    """
    if not data:
        return {"count": 0, "unique": 0, "distribution": {}, "is_numeric": False}

    # 检查是否为数值数据
    is_numeric = all(isinstance(x, (int, float)) for x in data)

    if is_numeric and bins:
        # 数值数据，计算直方图
        min_val = min(data)
        max_val = max(data)
        bin_width = (max_val - min_val) / bins if max_val > min_val else 1

        distribution = {}
        for i in range(bins):
            bin_start = min_val + i * bin_width
            bin_end = min_val + (i + 1) * bin_width
            bin_label = f"{bin_start:.2f}-{bin_end:.2f}"
            distribution[bin_label] = 0

        for value in data:
            if max_val == min_val:
                bin_idx = 0
            else:
                bin_idx = min(int((value - min_val) / bin_width), bins - 1)
            bin_start = min_val + bin_idx * bin_width
            bin_end = min_val + (bin_idx + 1) * bin_width
            bin_label = f"{bin_start:.2f}-{bin_end:.2f}"
            distribution[bin_label] = distribution.get(bin_label, 0) + 1
    else:
        # 分类数据或不分组的数值数据
        counter = Counter(data)
        distribution = dict(counter)

    return {
        "count": len(data),
        "unique": len(distribution),
        "distribution": distribution,
        "is_numeric": is_numeric,
    }


class StatisticsCollector:
    """统计收集器"""

    def __init__(self, name: str = "统计"):
        """
        初始化统计收集器

        Args:
            name: 统计名称
        """
        self.name = name
        self.data: List[float] = []
        self.timestamps: List[float] = []
        self.start_time = time.time()

    def add(self, value: float, timestamp: Optional[float] = None) -> None:
        """
        添加数据点

        Args:
            value: 数据值
            timestamp: 时间戳（可选，默认为当前时间）
        """
        self.data.append(value)
        self.timestamps.append(timestamp or time.time())

    def add_batch(self, values: List[float]) -> None:
        """
        批量添加数据

        Args:
            values: 数据值列表
        """
        current_time = time.time()
        self.data.extend(values)
        self.timestamps.extend([current_time] * len(values))

    def get_stats(self) -> Dict[str, Any]:
        """
        获取统计信息

        Returns:
            统计信息字典
        """
        if not self.data:
            return {"name": self.name, "count": 0, "duration": 0.0, "data": []}

        stats = calculate_statistics(self.data)
        stats["name"] = self.name
        stats["duration"] = self.timestamps[-1] - self.start_time if self.timestamps else 0.0

        # 添加时间信息
        if self.timestamps:
            calculate_statistics(self.timestamps)
            stats["timestamps"] = {
                "start": self.timestamps[0],
                "end": self.timestamps[-1],
                "duration": self.timestamps[-1] - self.timestamps[0],
            }

        # 添加百分位数
        stats["percentiles"] = calculate_percentiles(self.data)

        # 添加原始数据（限制大小）
        stats["data"] = self.data[:100]  # 只保留前100个数据点

        return stats

    def clear(self) -> None:
        """清空数据"""
        self.data.clear()
        self.timestamps.clear()
        self.start_time = time.time()

    def __str__(self) -> str:
        """字符串表示"""
        stats = self.get_stats()
        return format_statistics(stats)
