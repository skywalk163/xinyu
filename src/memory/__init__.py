"""
内存优化模块

提供内存使用优化工具和策略，包括对象池、缓存优化、内存监控等。
"""

from .memory_monitor import (
    MemoryMonitor,
    check_for_memory_leaks,
    get_memory_monitor,
    get_memory_usage,
    start_memory_monitoring,
    stop_memory_monitoring,
)
from .memory_utils import (
    MemoryUsage,
    ObjectInfo,
    estimate_memory_usage,
    find_memory_leaks,
    generate_memory_report,
    monitor_memory_growth,
    optimize_memory_usage,
    profile_memory_usage,
    track_memory_allocation,
)
from .object_pool import (
    LexerPool,
    ObjectPool,
    ParserPool,
    TokenFlyweight,
    clear_all_pools,
    get_lexer_pool,
    get_parser_pool,
    get_pool_stats,
)
from .optimization_strategies import (
    ASTNodePoolStrategy,
    CacheMemoryLimitStrategy,
    MemoryOptimizationStrategy,
    MemoryOptimizer,
    StringInterningStrategy,
    TokenFlyweightStrategy,
    get_memory_optimizer,
)

__all__ = [
    "ObjectPool",
    "LexerPool",
    "ParserPool",
    "MemoryMonitor",
    "MemoryOptimizationStrategy",
    "TokenFlyweightStrategy",
    "ASTNodePoolStrategy",
    "CacheMemoryLimitStrategy",
    "estimate_memory_usage",
    "track_memory_allocation",
    "find_memory_leaks",
    "optimize_memory_usage",
]
