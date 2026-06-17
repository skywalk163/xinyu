"""
公共工具模块

提供项目中重复使用的工具函数和类，减少代码重复。
"""

from .imports import *
from .file_utils import *
from .logging_utils import *
from .config_utils import *
from .stats_utils import *
from .memory_tools import *
from .performance_tools import *
from .error_utils import *

__all__ = [
    # 导入工具
    'import_optional',
    'import_with_fallback',
    'check_module_exists',
    'lazy_import',
    'with_psutil',
    'with_tracemalloc',
    'with_gc',
    'with_time',
    'with_json',
    'with_yaml',
    'with_dataclasses',
    'with_typing',
    'with_os',
    'with_sys',
    'get_available_modules',
    
    # 文件工具
    'read_json_file',
    'write_json_file',
    'read_yaml_file',
    'write_yaml_file',
    'ensure_directory',
    'get_file_hash',
    'copy_file_with_backup',
    'find_files_by_pattern',
    'read_file_lines',
    'write_file_lines',
    'create_temp_file',
    'get_file_size',
    'get_file_extension',
    'is_binary_file',
    
    # 日志工具
    'setup_logging',
    'get_logger',
    'log_exception',
    'log_function_call',
    'log_performance',
    'log_memory_usage',
    'format_log_message',
    'print_progress',
    'Timer',
    
    # 配置工具
    'ConfigManager',
    'get_global_config',
    'load_config',
    'save_config',
    'get_config_value',
    'set_config_value',
    'merge_configs',
    'load_from_env',
    'config_to_env',
    
    # 统计工具
    'calculate_statistics',
    'calculate_percentiles',
    'calculate_confidence_interval',
    'format_statistics',
    'calculate_execution_stats',
    'calculate_memory_stats',
    'calculate_correlation',
    'calculate_frequency_distribution',
    'StatisticsCollector',
    
    # 内存工具
    'MemoryUsage',
    'MemorySnapshot',
    'get_memory_usage',
    'track_memory_allocation',
    'find_memory_leaks',
    'monitor_memory_growth',
    'get_object_counts',
    'take_memory_snapshot',
    'compare_snapshots',
    'generate_memory_report',
    'MemoryProfiler',
    
    # 性能工具
    'PerformanceResult',
    'BenchmarkResult',
    'measure_execution_time',
    'profile_function',
    'performance_monitor',
    'PerformanceMonitor',
    'run_benchmark',
    'print_benchmark_result',
    'TimeoutException',
    'timeout',
    'timeout_context',
    
    # 错误处理工具
    'ErrorSeverity',
    'ErrorInfo',
    'ErrorContext',
    'BaseError',
    'ErrorRegistry',
    'register_error',
    'get_error_info',
    'create_error',
    'error_handler',
    'format_exception',
    'safe_execute',
    'retry_on_error',
]