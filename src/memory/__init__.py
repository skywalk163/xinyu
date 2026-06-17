"""
内存优化模块

提供内存使用优化工具和策略，包括对象池、缓存优化、内存监控等。
"""

from .object_pool import ObjectPool, LexerPool, ParserPool, TokenFlyweight, get_lexer_pool, get_parser_pool, clear_all_pools, get_pool_stats
from .memory_monitor import MemoryMonitor, get_memory_monitor, start_memory_monitoring, stop_memory_monitoring, get_memory_usage, check_for_memory_leaks
from .optimization_strategies import (
    MemoryOptimizationStrategy,
    TokenFlyweightStrategy,
    ASTNodePoolStrategy,
    CacheMemoryLimitStrategy,
    StringInterningStrategy,
    MemoryOptimizer,
    get_memory_optimizer
)
from .memory_utils import (
    estimate_memory_usage,
    track_memory_allocation,
    find_memory_leaks,
    optimize_memory_usage,
    monitor_memory_growth,
    generate_memory_report,
    profile_memory_usage,
    MemoryUsage,
    ObjectInfo
)

__all__ = [
    'ObjectPool',
    'LexerPool',
    'ParserPool',
    'MemoryMonitor',
    'MemoryOptimizationStrategy',
    'TokenFlyweightStrategy',
    'ASTNodePoolStrategy',
    'CacheMemoryLimitStrategy',
    'estimate_memory_usage',
    'track_memory_allocation',
    'find_memory_leaks',
    'optimize_memory_usage'
]