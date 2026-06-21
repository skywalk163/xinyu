# -*- coding: utf-8 -*-
"""编译缓存模块

提供Token序列和AST的缓存机制，提升重复编译性能。
"""

import hashlib
import time
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, List, Optional


@dataclass
class CacheEntry:
    """缓存条目"""

    value: Any  # 缓存值
    timestamp: float  # 创建时间戳
    hits: int = 0  # 命中次数
    size: int = 0  # 大小（字节）


class CompilationCache:
    """编译缓存

    提供Token序列和AST的缓存，基于源代码哈希。
    """

    def __init__(self, max_size: int = 256):
        """初始化编译缓存

        Args:
            max_size: 最大缓存条目数
        """
        self.max_size = max_size
        self._token_cache: Dict[str, CacheEntry] = {}
        self._ast_cache: Dict[str, CacheEntry] = {}
        self._stats = {
            "token_hits": 0,
            "token_misses": 0,
            "ast_hits": 0,
            "ast_misses": 0,
        }

    @staticmethod
    def compute_hash(source: str) -> str:
        """计算源代码哈希

        Args:
            source: 源代码字符串

        Returns:
            哈希值（MD5）
        """
        return hashlib.md5(source.encode("utf-8")).hexdigest()

    def get_tokens(self, source: str) -> Optional[List]:
        """获取缓存的Token序列

        Args:
            source: 源代码字符串

        Returns:
            Token序列，如果未缓存则返回None
        """
        hash_key = self.compute_hash(source)

        if hash_key in self._token_cache:
            entry = self._token_cache[hash_key]
            entry.hits += 1
            self._stats["token_hits"] += 1
            return entry.value

        self._stats["token_misses"] += 1
        return None

    def set_tokens(self, source: str, tokens: List) -> None:
        """缓存Token序列

        Args:
            source: 源代码字符串
            tokens: Token序列
        """
        hash_key = self.compute_hash(source)

        # 检查缓存大小
        if len(self._token_cache) >= self.max_size:
            self._evict_oldest(self._token_cache)

        # 计算大小
        size = sum(len(str(t)) for t in tokens)

        self._token_cache[hash_key] = CacheEntry(value=tokens, timestamp=time.time(), size=size)

    def get_ast(self, source: str) -> Optional[Any]:
        """获取缓存的AST

        Args:
            source: 源代码字符串

        Returns:
            AST，如果未缓存则返回None
        """
        hash_key = self.compute_hash(source)

        if hash_key in self._ast_cache:
            entry = self._ast_cache[hash_key]
            entry.hits += 1
            self._stats["ast_hits"] += 1
            return entry.value

        self._stats["ast_misses"] += 1
        return None

    def set_ast(self, source: str, ast: Any) -> None:
        """缓存AST

        Args:
            source: 源代码字符串
            ast: AST
        """
        hash_key = self.compute_hash(source)

        # 检查缓存大小
        if len(self._ast_cache) >= self.max_size:
            self._evict_oldest(self._ast_cache)

        self._ast_cache[hash_key] = CacheEntry(value=ast, timestamp=time.time())

    def _evict_oldest(self, cache: Dict[str, CacheEntry]) -> None:
        """驱逐最旧的缓存条目（LRU策略）

        Args:
            cache: 缓存字典
        """
        if not cache:
            return

        # 找到最旧的条目
        oldest_key = min(cache.keys(), key=lambda k: cache[k].timestamp)
        del cache[oldest_key]

    def clear(self) -> None:
        """清空所有缓存"""
        self._token_cache.clear()
        self._ast_cache.clear()
        self._stats = {
            "token_hits": 0,
            "token_misses": 0,
            "ast_hits": 0,
            "ast_misses": 0,
        }

    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息

        Returns:
            统计信息字典
        """
        total_token_requests = self._stats["token_hits"] + self._stats["token_misses"]
        total_ast_requests = self._stats["ast_hits"] + self._stats["ast_misses"]

        return {
            "token_cache_size": len(self._token_cache),
            "ast_cache_size": len(self._ast_cache),
            "token_hit_rate": self._stats["token_hits"] / total_token_requests
            if total_token_requests > 0
            else 0,
            "ast_hit_rate": self._stats["ast_hits"] / total_ast_requests
            if total_ast_requests > 0
            else 0,
            **self._stats,
        }

    def get_memory_usage(self) -> Dict[str, int]:
        """获取内存使用情况

        Returns:
            内存使用字典
        """
        token_size = sum(entry.size for entry in self._token_cache.values())
        ast_size = len(self._ast_cache) * 1000  # 估算每个AST约1KB

        return {
            "token_cache_bytes": token_size,
            "ast_cache_bytes": ast_size,
            "total_bytes": token_size + ast_size,
        }


class CachedLexer:
    """带缓存的词法分析器

    包装Lexer，提供Token序列缓存。
    """

    def __init__(self, lexer_class, cache: Optional[CompilationCache] = None):
        """初始化带缓存的词法分析器

        Args:
            lexer_class: Lexer类
            cache: 编译缓存实例
        """
        self.lexer_class = lexer_class
        self.cache = cache or CompilationCache()

    def tokenize(self, source: str) -> List:
        """词法分析（带缓存）

        Args:
            source: 源代码字符串

        Returns:
            Token序列
        """
        # 尝试从缓存获取
        cached_tokens = self.cache.get_tokens(source)
        if cached_tokens is not None:
            return cached_tokens

        # 执行词法分析
        lexer = self.lexer_class(source)
        tokens = lexer.tokenize()

        # 缓存结果
        self.cache.set_tokens(source, tokens)

        return tokens


class CachedParser:
    """带缓存的语法分析器

    包装Parser，提供AST缓存。
    """

    def __init__(self, parser_class, cache: Optional[CompilationCache] = None):
        """初始化带缓存的语法分析器

        Args:
            parser_class: Parser类
            cache: 编译缓存实例
        """
        self.parser_class = parser_class
        self.cache = cache or CompilationCache()

    def parse(self, source: str, tokens: List) -> Any:
        """语法分析（带缓存）

        Args:
            source: 源代码字符串
            tokens: Token序列

        Returns:
            AST
        """
        # 尝试从缓存获取
        cached_ast = self.cache.get_ast(source)
        if cached_ast is not None:
            return cached_ast

        # 执行语法分析
        parser = self.parser_class(tokens)
        ast = parser.parse()

        # 缓存结果
        self.cache.set_ast(source, ast)

        return ast


# 全局缓存实例
_global_cache = CompilationCache()


def get_global_cache() -> CompilationCache:
    """获取全局缓存实例

    Returns:
        全局编译缓存
    """
    return _global_cache


def clear_global_cache() -> None:
    """清空全局缓存"""
    _global_cache.clear()


# 便捷函数：使用LRU缓存的词法分析
@lru_cache(maxsize=128)
def tokenize_cached(source: str) -> tuple:
    """词法分析（使用LRU缓存）

    注意：返回tuple而不是list，因为list不可哈希

    Args:
        source: 源代码字符串

    Returns:
        Token元组
    """
    from src.lexer.lexer import Lexer

    lexer = Lexer(source)
    return tuple(lexer.tokenize())
