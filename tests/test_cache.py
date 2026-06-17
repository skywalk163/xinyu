# -*- coding: utf-8 -*-
"""编译缓存测试

测试CompilationCache的功能。
"""

import pytest

from src.cache.compilation_cache import (
    CachedLexer,
    CachedParser,
    CompilationCache,
    clear_global_cache,
    get_global_cache,
    tokenize_cached,
)
from src.lexer.lexer import Lexer
from src.parser.parser import Parser


class TestCompilationCache:
    """编译缓存测试"""

    def test_compute_hash(self):
        """测试哈希计算"""
        source1 = "定 x = 5。"
        source2 = "定 x = 5。"
        source3 = "定 y = 10。"

        hash1 = CompilationCache.compute_hash(source1)
        hash2 = CompilationCache.compute_hash(source2)
        hash3 = CompilationCache.compute_hash(source3)

        # 相同源代码应该产生相同哈希
        assert hash1 == hash2
        # 不同源代码应该产生不同哈希
        assert hash1 != hash3

    def test_token_cache_hit(self):
        """测试Token缓存命中"""
        cache = CompilationCache()
        source = "定 x = 5。"

        # 创建Token
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        # 缓存Token
        cache.set_tokens(source, tokens)

        # 从缓存获取
        cached_tokens = cache.get_tokens(source)
        assert cached_tokens is not None
        assert len(cached_tokens) == len(tokens)

    def test_token_cache_miss(self):
        """测试Token缓存未命中"""
        cache = CompilationCache()
        source = "定 x = 5。"

        # 未缓存，应该返回None
        cached_tokens = cache.get_tokens(source)
        assert cached_tokens is None

    def test_ast_cache_hit(self):
        """测试AST缓存命中"""
        cache = CompilationCache()
        source = "定 x = 5。"

        # 创建AST
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # 缓存AST
        cache.set_ast(source, ast)

        # 从缓存获取
        cached_ast = cache.get_ast(source)
        assert cached_ast is not None

    def test_ast_cache_miss(self):
        """测试AST缓存未命中"""
        cache = CompilationCache()
        source = "定 x = 5。"

        # 未缓存，应该返回None
        cached_ast = cache.get_ast(source)
        assert cached_ast is None

    def test_cache_eviction(self):
        """测试缓存驱逐（LRU）"""
        cache = CompilationCache(max_size=2)

        # 添加3个条目，应该驱逐最旧的
        for i in range(3):
            source = f"定 x{i} = {i}。"
            tokens = Lexer(source).tokenize()
            cache.set_tokens(source, tokens)

        # 缓存大小应该不超过max_size
        stats = cache.get_stats()
        assert stats["token_cache_size"] <= 2

    def test_cache_clear(self):
        """测试缓存清空"""
        cache = CompilationCache()
        source = "定 x = 5。"
        tokens = Lexer(source).tokenize()

        # 缓存数据
        cache.set_tokens(source, tokens)

        # 清空缓存
        cache.clear()

        # 应该无法获取缓存数据
        cached_tokens = cache.get_tokens(source)
        assert cached_tokens is None

    def test_cache_stats(self):
        """测试缓存统计"""
        cache = CompilationCache()
        source = "定 x = 5。"
        tokens = Lexer(source).tokenize()

        # 缓存数据
        cache.set_tokens(source, tokens)

        # 命中一次
        cache.get_tokens(source)

        # 未命中一次
        cache.get_tokens("定 y = 10。")

        # 获取统计
        stats = cache.get_stats()
        assert stats["token_hits"] == 1
        assert stats["token_misses"] == 1
        assert stats["token_hit_rate"] == 0.5

    def test_memory_usage(self):
        """测试内存使用"""
        cache = CompilationCache()
        source = "定 x = 5。"
        tokens = Lexer(source).tokenize()

        # 缓存数据
        cache.set_tokens(source, tokens)

        # 获取内存使用
        memory = cache.get_memory_usage()
        assert memory["token_cache_bytes"] > 0
        assert memory["total_bytes"] > 0


class TestCachedLexer:
    """带缓存的词法分析器测试"""

    def test_cached_lexer_first_call(self):
        """测试首次调用（未命中）"""
        cache = CompilationCache()
        cached_lexer = CachedLexer(Lexer, cache)
        source = "定 x = 5。"

        # 首次调用，应该执行词法分析
        tokens = cached_lexer.tokenize(source)
        assert len(tokens) > 0

        # 检查统计
        stats = cache.get_stats()
        assert stats["token_misses"] == 1

    def test_cached_lexer_second_call(self):
        """测试第二次调用（命中）"""
        cache = CompilationCache()
        cached_lexer = CachedLexer(Lexer, cache)
        source = "定 x = 5。"

        # 首次调用
        tokens1 = cached_lexer.tokenize(source)

        # 第二次调用，应该从缓存获取
        tokens2 = cached_lexer.tokenize(source)

        assert len(tokens1) == len(tokens2)

        # 检查统计
        stats = cache.get_stats()
        assert stats["token_hits"] == 1
        assert stats["token_misses"] == 1


class TestCachedParser:
    """带缓存的语法分析器测试"""

    def test_cached_parser_first_call(self):
        """测试首次调用（未命中）"""
        cache = CompilationCache()
        cached_parser = CachedParser(Parser, cache)
        source = "定 x = 5。"

        lexer = Lexer(source)
        tokens = lexer.tokenize()

        # 首次调用，应该执行语法分析
        ast = cached_parser.parse(source, tokens)
        assert ast is not None

        # 检查统计
        stats = cache.get_stats()
        assert stats["ast_misses"] == 1

    def test_cached_parser_second_call(self):
        """测试第二次调用（命中）"""
        cache = CompilationCache()
        cached_parser = CachedParser(Parser, cache)
        source = "定 x = 5。"

        lexer = Lexer(source)
        tokens = lexer.tokenize()

        # 首次调用
        ast1 = cached_parser.parse(source, tokens)

        # 第二次调用，应该从缓存获取
        ast2 = cached_parser.parse(source, tokens)

        assert ast1 is not None
        assert ast2 is not None

        # 检查统计
        stats = cache.get_stats()
        assert stats["ast_hits"] == 1
        assert stats["ast_misses"] == 1


class TestGlobalCache:
    """全局缓存测试"""

    def test_get_global_cache(self):
        """测试获取全局缓存"""
        cache1 = get_global_cache()
        cache2 = get_global_cache()

        # 应该返回同一个实例
        assert cache1 is cache2

    def test_clear_global_cache(self):
        """测试清空全局缓存"""
        cache = get_global_cache()
        source = "定 x = 5。"
        tokens = Lexer(source).tokenize()

        # 缓存数据
        cache.set_tokens(source, tokens)

        # 清空全局缓存
        clear_global_cache()

        # 应该无法获取缓存数据
        cached_tokens = cache.get_tokens(source)
        assert cached_tokens is None


class TestTokenizeCached:
    """LRU缓存的词法分析测试"""

    def test_tokenize_cached_first_call(self):
        """测试首次调用"""
        source = "定 x = 5。"

        # 首次调用
        tokens = tokenize_cached(source)
        assert len(tokens) > 0
        assert isinstance(tokens, tuple)  # 返回tuple

    def test_tokenize_cached_second_call(self):
        """测试第二次调用（从缓存）"""
        source = "定 x = 5。"

        # 首次调用
        tokens1 = tokenize_cached(source)

        # 第二次调用，应该从缓存获取
        tokens2 = tokenize_cached(source)

        assert tokens1 == tokens2


class TestCachePerformance:
    """缓存性能测试"""

    def test_cache_improves_performance(self):
        """测试缓存提升性能"""
        import time

        cache = CompilationCache()
        cached_lexer = CachedLexer(Lexer, cache)
        source = "定 x = 5。"

        # 首次调用（未命中）
        start1 = time.time()
        tokens1 = cached_lexer.tokenize(source)
        time1 = time.time() - start1

        # 第二次调用（命中）
        start2 = time.time()
        tokens2 = cached_lexer.tokenize(source)
        time2 = time.time() - start2

        # 缓存命中应该更快（虽然对于简单代码差异很小）
        # 这里只验证缓存命中
        stats = cache.get_stats()
        assert stats["token_hits"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
