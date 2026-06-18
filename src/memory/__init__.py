"""
内存优化模块

提供内存使用优化工具和策略，包括对象池、缓存优化、内存监控等。
"""

from .memory_monitor import MemoryMonitor
from .memory_utils import estimate_memory_usage, find_memory_leaks, optimize_memory_usage, track_memory_allocation
from .object_pool import LexerPool, ObjectPool, ParserPool
from .optimization_strategies import (
    ASTNodePoolStrategy,
    CacheMemoryLimitStrategy,
    MemoryOptimizationStrategy,
    TokenFlyweightStrategy,
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
