"""
公共工具模块

提供项目中重复使用的工具函数和类，减少代码重复。
"""

from .config_utils import *  # noqa: F403, F405
from .error_utils import *  # noqa: F403, F405
from .file_utils import *  # noqa: F403, F405
from .imports import *  # noqa: F403, F405
from .logging_utils import *  # noqa: F403, F405
from .memory_tools import *  # noqa: F403, F405
from .performance_tools import *  # noqa: F403, F405
from .stats_utils import *  # noqa: F403, F405

__all__ = [  # noqa: F405
    # 导入工具
    "import_optional",  # noqa: F405
    "import_with_fallback",  # noqa: F405
    "check_module_exists",  # noqa: F405
    "lazy_import",  # noqa: F405
    "with_psutil",  # noqa: F405
    "with_tracemalloc",  # noqa: F405
    "with_gc",  # noqa: F405
    "with_time",  # noqa: F405
    "with_json",  # noqa: F405
    "with_yaml",  # noqa: F405
    "with_dataclasses",  # noqa: F405
    "with_typing",  # noqa: F405
    "with_os",  # noqa: F405
    "with_sys",  # noqa: F405
    "get_available_modules",  # noqa: F405
    # 文件工具
    "read_json_file",  # noqa: F405
    "write_json_file",  # noqa: F405
    "read_yaml_file",  # noqa: F405
    "write_yaml_file",  # noqa: F405
    "ensure_directory",  # noqa: F405
    "get_file_hash",  # noqa: F405
    "copy_file_with_backup",  # noqa: F405
    "find_files_by_pattern",  # noqa: F405
    "read_file_lines",  # noqa: F405
    "write_file_lines",  # noqa: F405
    "create_temp_file",  # noqa: F405
    "get_file_size",  # noqa: F405
    "get_file_extension",  # noqa: F405
    "is_binary_file",  # noqa: F405
    # 日志工具
    "setup_logging",  # noqa: F405
    "get_logger",  # noqa: F405
    "log_exception",  # noqa: F405
    "log_function_call",  # noqa: F405
    "log_performance",  # noqa: F405
    "log_memory_usage",  # noqa: F405
    "format_log_message",  # noqa: F405
    "print_progress",  # noqa: F405
    "Timer",  # noqa: F405
    # 配置工具
    "ConfigManager",  # noqa: F405
    "get_global_config",  # noqa: F405
    "load_config",  # noqa: F405
    "save_config",  # noqa: F405
    "get_config_value",  # noqa: F405
    "set_config_value",  # noqa: F405
    "merge_configs",  # noqa: F405
    "load_from_env",  # noqa: F405
    "config_to_env",  # noqa: F405
    # 统计工具
    "calculate_statistics",  # noqa: F405
    "calculate_percentiles",  # noqa: F405
    "calculate_confidence_interval",  # noqa: F405
    "format_statistics",  # noqa: F405
    "calculate_execution_stats",  # noqa: F405
    "calculate_memory_stats",  # noqa: F405
    "calculate_correlation",  # noqa: F405
    "calculate_frequency_distribution",  # noqa: F405
    "StatisticsCollector",  # noqa: F405
    # 内存工具
    "MemoryUsage",  # noqa: F405
    "MemorySnapshot",  # noqa: F405
    "get_memory_usage",  # noqa: F405
    "track_memory_allocation",  # noqa: F405
    "find_memory_leaks",  # noqa: F405
    "monitor_memory_growth",  # noqa: F405
    "get_object_counts",  # noqa: F405
    "take_memory_snapshot",  # noqa: F405
    "compare_snapshots",  # noqa: F405
    "generate_memory_report",  # noqa: F405
    "MemoryProfiler",  # noqa: F405
    # 性能工具
    "PerformanceResult",  # noqa: F405
    "BenchmarkResult",  # noqa: F405
    "measure_execution_time",  # noqa: F405
    "profile_function",  # noqa: F405
    "performance_monitor",  # noqa: F405
    "PerformanceMonitor",  # noqa: F405
    "run_benchmark",  # noqa: F405
    "print_benchmark_result",  # noqa: F405
    "TimeoutException",  # noqa: F405
    "timeout",  # noqa: F405
    "timeout_context",  # noqa: F405
    # 错误处理工具
    "ErrorSeverity",  # noqa: F405
    "ErrorInfo",  # noqa: F405
    "ErrorContext",  # noqa: F405
    "BaseError",  # noqa: F405
    "ErrorRegistry",  # noqa: F405
    "register_error",  # noqa: F405
    "get_error_info",  # noqa: F405
    "create_error",  # noqa: F405
    "error_handler",  # noqa: F405
    "format_exception",  # noqa: F405
    "safe_execute",  # noqa: F405
    "retry_on_error",  # noqa: F405
]
