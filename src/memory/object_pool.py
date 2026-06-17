"""
对象池实现

提供对象复用机制，减少频繁的对象创建和销毁开销。
"""

import threading
import weakref
from collections import deque
from dataclasses import dataclass
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

T = TypeVar("T")


@dataclass
class PoolStats:
    """对象池统计信息"""

    total_created: int = 0
    total_reused: int = 0
    current_size: int = 0
    max_size: int = 0
    hit_rate: float = 0.0


class ObjectPool(Generic[T]):
    """
    通用对象池

    提供对象复用机制，支持：
    1. 对象缓存和复用
    2. 最大池大小限制
    3. 统计信息收集
    4. 线程安全
    """

    def __init__(self, factory_func, max_size: int = 100, reset_func=None, validate_func=None):
        """
        初始化对象池

        Args:
            factory_func: 对象工厂函数
            max_size: 最大池大小
            reset_func: 对象重置函数（可选）
            validate_func: 对象验证函数（可选）
        """
        self.factory_func = factory_func
        self.max_size = max_size
        self.reset_func = reset_func
        self.validate_func = validate_func

        self._pool = deque()
        self._lock = threading.RLock()
        self._stats = PoolStats(max_size=max_size)
        self._active_objects = weakref.WeakSet()

    def acquire(self, *args, **kwargs) -> T:
        """
        从池中获取对象

        Args:
            *args: 传递给工厂函数的参数
            **kwargs: 传递给工厂函数的关键字参数

        Returns:
            对象实例
        """
        with self._lock:
            # 尝试从池中获取对象
            while self._pool:
                obj = self._pool.pop()

                # 验证对象是否有效
                if self.validate_func and not self.validate_func(obj):
                    continue

                # 重置对象状态
                if self.reset_func:
                    self.reset_func(obj)

                self._stats.total_reused += 1
                self._stats.current_size = len(self._pool)
                self._active_objects.add(obj)
                return obj

            # 池为空，创建新对象
            obj = self.factory_func(*args, **kwargs)
            self._stats.total_created += 1
            self._stats.max_size = max(self._stats.max_size, self._stats.total_created)
            self._active_objects.add(obj)
            return obj

    def release(self, obj: T) -> None:
        """
        将对象释放回池中

        Args:
            obj: 要释放的对象
        """
        with self._lock:
            if obj in self._active_objects:
                self._active_objects.remove(obj)

            # 如果池已满，丢弃对象
            if len(self._pool) >= self.max_size:
                return

            # 验证对象是否有效
            if self.validate_func and not self.validate_func(obj):
                return

            # 重置对象状态
            if self.reset_func:
                self.reset_func(obj)

            self._pool.append(obj)
            self._stats.current_size = len(self._pool)

    def clear(self) -> None:
        """清空对象池"""
        with self._lock:
            self._pool.clear()
            self._stats.current_size = 0

    def get_stats(self) -> PoolStats:
        """
        获取统计信息

        Returns:
            统计信息对象
        """
        with self._lock:
            total_requests = self._stats.total_created + self._stats.total_reused
            if total_requests > 0:
                self._stats.hit_rate = self._stats.total_reused / total_requests * 100
            else:
                self._stats.hit_rate = 0.0

            return PoolStats(
                total_created=self._stats.total_created,
                total_reused=self._stats.total_reused,
                current_size=self._stats.current_size,
                max_size=self._stats.max_size,
                hit_rate=self._stats.hit_rate,
            )

    def get_active_count(self) -> int:
        """
        获取活跃对象数量

        Returns:
            活跃对象数量
        """
        with self._lock:
            return len(self._active_objects)

    def __enter__(self):
        """上下文管理器支持"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出时清空池"""
        self.clear()


class LexerPool(ObjectPool):
    """
    Lexer对象池

    专门用于复用Lexer对象，减少词法分析器的创建开销。
    """

    def __init__(self, max_size: int = 20):
        """
        初始化Lexer池

        Args:
            max_size: 最大池大小
        """
        from src.lexer.lexer import Lexer

        def factory_func(source: str = ""):
            return Lexer(source)

        def reset_func(lexer):
            lexer.reset()

        def validate_func(lexer):
            return hasattr(lexer, "reset") and callable(lexer.reset)

        super().__init__(
            factory_func=factory_func,
            max_size=max_size,
            reset_func=reset_func,
            validate_func=validate_func,
        )

    def acquire_lexer(self, source: str = "") -> Any:
        """
        获取Lexer对象

        Args:
            source: 源代码

        Returns:
            Lexer实例
        """
        return self.acquire(source)


class ParserPool(ObjectPool):
    """
    Parser对象池

    专门用于复用Parser对象，减少语法分析器的创建开销。
    """

    def __init__(self, max_size: int = 20):
        """
        初始化Parser池

        Args:
            max_size: 最大池大小
        """
        from src.parser.parser import Parser

        def factory_func(tokens=None):
            return Parser(tokens or [])

        def reset_func(parser):
            parser.reset()

        def validate_func(parser):
            return hasattr(parser, "reset") and callable(parser.reset)

        super().__init__(
            factory_func=factory_func,
            max_size=max_size,
            reset_func=reset_func,
            validate_func=validate_func,
        )

    def acquire_parser(self, tokens=None) -> Any:
        """
        获取Parser对象

        Args:
            tokens: Token列表

        Returns:
            Parser实例
        """
        return self.acquire(tokens)


class TokenFlyweight:
    """
    Token享元模式

    减少Token对象的内存占用，通过共享相同值的Token实例。
    """

    _pool: Dict[tuple, Any] = {}
    _lock = threading.RLock()

    @classmethod
    def get_token(cls, token_type: str, value: str, line: int = 1, column: int = 1):
        """
        获取或创建Token实例

        Args:
            token_type: Token类型
            value: Token值
            line: 行号
            column: 列号

        Returns:
            Token实例
        """
        from src.lexer.tokens import Token

        key = (token_type, value)

        with cls._lock:
            if key in cls._pool:
                token = cls._pool[key]
                # 更新位置信息
                token.line = line
                token.column = column
                return token
            else:
                token = Token(token_type, value, line, column)
                cls._pool[key] = token
                return token

    @classmethod
    def clear_pool(cls):
        """清空Token池"""
        with cls._lock:
            cls._pool.clear()

    @classmethod
    def get_pool_size(cls) -> int:
        """获取池大小"""
        with cls._lock:
            return len(cls._pool)

    @classmethod
    def get_memory_savings(cls) -> int:
        """
        估算内存节省量

        Returns:
            估算节省的内存字节数
        """
        with cls._lock:
            # 假设每个Token对象占用约100字节
            unique_tokens = len(cls._pool)
            # 如果没有共享，每个Token都是独立的
            # 这里我们无法知道总Token数，所以返回0
            return 0


# 全局对象池实例
_lexer_pool: Optional[LexerPool] = None
_parser_pool: Optional[ParserPool] = None


def get_lexer_pool() -> LexerPool:
    """获取全局Lexer池实例"""
    global _lexer_pool
    if _lexer_pool is None:
        _lexer_pool = LexerPool()
    return _lexer_pool


def get_parser_pool() -> ParserPool:
    """获取全局Parser池实例"""
    global _parser_pool
    if _parser_pool is None:
        _parser_pool = ParserPool()
    return _parser_pool


def clear_all_pools():
    """清空所有对象池"""
    global _lexer_pool, _parser_pool

    if _lexer_pool:
        _lexer_pool.clear()

    if _parser_pool:
        _parser_pool.clear()

    TokenFlyweight.clear_pool()


def get_pool_stats() -> Dict[str, Dict[str, Any]]:
    """
    获取所有对象池的统计信息

    Returns:
        统计信息字典
    """
    stats = {}

    if _lexer_pool:
        stats["lexer_pool"] = _lexer_pool.get_stats().__dict__

    if _parser_pool:
        stats["parser_pool"] = _parser_pool.get_stats().__dict__

    stats["token_flyweight"] = {
        "pool_size": TokenFlyweight.get_pool_size(),
        "memory_savings": TokenFlyweight.get_memory_savings(),
    }

    return stats
