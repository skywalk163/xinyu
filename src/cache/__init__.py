# -*- coding: utf-8 -*-
"""缓存模块

提供编译缓存功能。
"""

    CachedLexer,
    CachedParser,
    CacheEntry,
    CompilationCache,
    clear_global_cache,
    get_global_cache,
    tokenize_cached,
)

__all__ = [
    "CompilationCache",
    "CachedLexer",
    "CachedParser",
    "CacheEntry",
    "get_global_cache",
    "clear_global_cache",
    "tokenize_cached",
]
