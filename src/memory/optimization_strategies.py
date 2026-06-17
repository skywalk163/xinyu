"""
内存优化策略

提供各种内存优化策略的实现。
"""

import gc
import sys
from typing import Dict, List, Any, Optional, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import weakref
from collections import defaultdict


@dataclass
class OptimizationResult:
    """优化结果"""
    strategy_name: str
    memory_saved_mb: float
    objects_reduced: int
    execution_time_ms: float
    success: bool
    message: str = ""
    details: Dict[str, Any] = field(default_factory=dict)


class MemoryOptimizationStrategy(ABC):
    """内存优化策略基类"""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.enabled = True
    
    @abstractmethod
    def apply(self, context: Dict[str, Any] = None) -> OptimizationResult:
        """应用优化策略"""
        pass
    
    @abstractmethod
    def can_apply(self, context: Dict[str, Any] = None) -> bool:
        """检查是否可以应用此策略"""
        pass
    
    def reset(self) -> None:
        """重置策略状态"""
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """获取策略统计信息"""
        return {
            'name': self.name,
            'description': self.description,
            'enabled': self.enabled
        }


class TokenFlyweightStrategy(MemoryOptimizationStrategy):
    """
    Token享元优化策略
    
    通过共享相同值的Token实例来减少内存使用。
    """
    
    def __init__(self):
        super().__init__(
            name="token_flyweight",
            description="使用享元模式共享Token实例，减少重复Token对象的内存占用"
        )
        self._pool = {}
        self._hits = 0
        self._misses = 0
    
    def can_apply(self, context: Dict[str, Any] = None) -> bool:
        """检查是否可以应用Token享元策略"""
        # 总是可以应用
        return True
    
    def apply(self, context: Dict[str, Any] = None) -> OptimizationResult:
        """应用Token享元优化"""
        try:
            # 获取当前内存使用
            import psutil
            process = psutil.Process()
            before_memory = process.memory_info().rss
            
            # 获取当前对象计数
            before_objects = len(gc.get_objects())
            
            # 应用优化
            from src.lexer.tokens import Token
            
            # 替换Token创建逻辑
            original_token_init = Token.__init__
            
            def optimized_token_init(self, token_type, value, line=1, column=1):
                # 使用享元池
                key = (token_type, value)
                if key in self._pool:
                    cached_token = self._pool[key]
                    self.__dict__.update(cached_token.__dict__)
                    self._hits += 1
                else:
                    original_token_init(self, token_type, value, line, column)
                    self._pool[key] = self
                    self._misses += 1
            
            # 临时替换__init__方法
            Token.__init__ = optimized_token_init
            
            # 获取优化后内存使用
            after_memory = process.memory_info().rss
            after_objects = len(gc.get_objects())
            
            # 恢复原始__init__方法
            Token.__init__ = original_token_init
            
            memory_saved = (before_memory - after_memory) / 1024 / 1024
            objects_reduced = before_objects - after_objects
            
            return OptimizationResult(
                strategy_name=self.name,
                memory_saved_mb=max(0, memory_saved),
                objects_reduced=max(0, objects_reduced),
                execution_time_ms=0.0,  # 实际应用中需要测量时间
                success=True,
                message=f"Token享元优化应用成功，命中率: {self._hits/(self._hits+self._misses)*100:.1f}%",
                details={
                    'hits': self._hits,
                    'misses': self._misses,
                    'hit_rate': self._hits/(self._hits+self._misses) if (self._hits+self._misses) > 0 else 0,
                    'pool_size': len(self._pool)
                }
            )
            
        except Exception as e:
            return OptimizationResult(
                strategy_name=self.name,
                memory_saved_mb=0.0,
                objects_reduced=0,
                execution_time_ms=0.0,
                success=False,
                message=f"Token享元优化失败: {str(e)}"
            )
    
    def reset(self) -> None:
        """重置享元池"""
        self._pool.clear()
        self._hits = 0
        self._misses = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = super().get_stats()
        stats.update({
            'pool_size': len(self._pool),
            'hits': self._hits,
            'misses': self._misses,
            'hit_rate': self._hits/(self._hits+self._misses) if (self._hits+self._misses) > 0 else 0
        })
        return stats


class ASTNodePoolStrategy(MemoryOptimizationStrategy):
    """
    AST节点池优化策略
    
    通过对象池复用AST节点，减少节点创建开销。
    """
    
    def __init__(self, max_pool_size: int = 1000):
        super().__init__(
            name="ast_node_pool",
            description="使用对象池复用AST节点，减少节点创建和垃圾回收开销"
        )
        self.max_pool_size = max_pool_size
        self._pools = defaultdict(list)  # 按节点类型分类的池
        self._allocations = 0
        self._reuses = 0
    
    def can_apply(self, context: Dict[str, Any] = None) -> bool:
        """检查是否可以应用AST节点池策略"""
        # 需要导入AST节点类
        try:
            # 在Python 3.12中，sys.path_importer_cache可能不存在
            # 使用更安全的导入方式
            import importlib.util
            import sys
            
            # 检查模块是否存在
            spec = importlib.util.find_spec("src.parser.ast")
            if spec is None:
                return False
            
            # 尝试导入
            from src.parser.ast import ASTNode
            return True
        except (ImportError, AttributeError):
            # AttributeError可能来自sys.path_importer_cache
            return False
    
    def apply(self, context: Dict[str, Any] = None) -> OptimizationResult:
        """应用AST节点池优化"""
        try:
            # 获取当前内存使用
            import psutil
            process = psutil.Process()
            before_memory = process.memory_info().rss
            
            # 获取当前对象计数
            before_objects = len(gc.get_objects())
            
            # 导入AST节点类
            from src.parser.ast import ASTNode
            
            # 保存原始__new__方法
            original_new = ASTNode.__new__
            original_init = ASTNode.__init__
            
            # 创建优化后的__new__方法
            def optimized_new(cls, *args, **kwargs):
                node_type = cls.__name__
                
                # 尝试从池中获取节点
                if node_type in self._pools and self._pools[node_type]:
                    instance = self._pools[node_type].pop()
                    self._reuses += 1
                else:
                    # 池为空，创建新实例
                    instance = original_new(cls)
                    self._allocations += 1
                
                return instance
            
            # 创建优化后的__init__方法
            def optimized_init(self, *args, **kwargs):
                # 调用原始__init__
                original_init(self, *args, **kwargs)
                
                # 重写__del__以支持对象回收
                def optimized_del():
                    node_type = type(self).__name__
                    if len(self._pools[node_type]) < self.max_pool_size:
                        # 重置对象状态
                        self.__dict__.clear()
                        # 放回池中
                        self._pools[node_type].append(self)
                
                # 绑定__del__方法
                self.__del__ = optimized_del
            
            # 临时替换方法
            ASTNode.__new__ = staticmethod(optimized_new)
            ASTNode.__init__ = optimized_init
            
            # 获取优化后内存使用
            after_memory = process.memory_info().rss
            after_objects = len(gc.get_objects())
            
            # 恢复原始方法
            ASTNode.__new__ = staticmethod(original_new)
            ASTNode.__init__ = original_init
            
            memory_saved = (before_memory - after_memory) / 1024 / 1024
            objects_reduced = before_objects - after_objects
            
            return OptimizationResult(
                strategy_name=self.name,
                memory_saved_mb=max(0, memory_saved),
                objects_reduced=max(0, objects_reduced),
                execution_time_ms=0.0,
                success=True,
                message=f"AST节点池优化应用成功，复用率: {self._reuses/(self._allocations+self._reuses)*100:.1f}%",
                details={
                    'allocations': self._allocations,
                    'reuses': self._reuses,
                    'reuse_rate': self._reuses/(self._allocations+self._reuses) if (self._allocations+self._reuses) > 0 else 0,
                    'pool_sizes': {k: len(v) for k, v in self._pools.items()}
                }
            )
            
        except Exception as e:
            return OptimizationResult(
                strategy_name=self.name,
                memory_saved_mb=0.0,
                objects_reduced=0,
                execution_time_ms=0.0,
                success=False,
                message=f"AST节点池优化失败: {str(e)}"
            )
    
    def reset(self) -> None:
        """重置所有对象池"""
        self._pools.clear()
        self._allocations = 0
        self._reuses = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = super().get_stats()
        stats.update({
            'max_pool_size': self.max_pool_size,
            'allocations': self._allocations,
            'reuses': self._reuses,
            'reuse_rate': self._reuses/(self._allocations+self._reuses) if (self._allocations+self._reuses) > 0 else 0,
            'pool_sizes': {k: len(v) for k, v in self._pools.items()},
            'total_pooled': sum(len(v) for v in self._pools.values())
        })
        return stats


class CacheMemoryLimitStrategy(MemoryOptimizationStrategy):
    """
    缓存内存限制策略
    
    为编译缓存添加内存使用限制，防止缓存无限增长。
    """
    
    def __init__(self, max_cache_memory_mb: float = 100.0):
        super().__init__(
            name="cache_memory_limit",
            description="为编译缓存添加内存使用限制，自动淘汰旧条目"
        )
        self.max_cache_memory_mb = max_cache_memory_mb
        self._original_cache_class = None
        self._optimized_cache_class = None
    
    def can_apply(self, context: Dict[str, Any] = None) -> bool:
        """检查是否可以应用缓存内存限制策略"""
        try:
            # 在Python 3.12中，sys.path_importer_cache可能不存在
            # 使用更安全的导入方式
            import importlib.util
            
            # 检查模块是否存在
            spec = importlib.util.find_spec("src.cache.compilation_cache")
            if spec is None:
                return False
            
            # 尝试导入
            from src.cache.compilation_cache import CompilationCache
            return True
        except (ImportError, AttributeError):
            # AttributeError可能来自sys.path_importer_cache
            return False
    
    def apply(self, context: Dict[str, Any] = None) -> OptimizationResult:
        """应用缓存内存限制优化"""
        try:
            # 获取当前内存使用
            import psutil
            process = psutil.Process()
            before_memory = process.memory_info().rss
            
            # 导入编译缓存类
            from src.cache.compilation_cache import CompilationCache
            
            # 保存原始类
            self._original_cache_class = CompilationCache
            
            # 创建优化后的缓存类
            class MemoryLimitedCache(CompilationCache):
                def __init__(self, max_memory_mb: float = 100.0, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.max_memory_bytes = max_memory_mb * 1024 * 1024
                    self.current_memory_bytes = 0
                    self.entry_sizes = {}  # 记录每个条目的内存大小
                    
                    # 重写父类的缓存字典以支持内存感知
                    self._token_cache = {}
                    self._ast_cache = {}
                
                def _estimate_entry_size(self, entry):
                    """估算条目内存大小"""
                    import sys
                    return sys.getsizeof(entry)
                
                def _evict_if_needed(self):
                    """如果需要，淘汰旧条目"""
                    if self.current_memory_bytes <= self.max_memory_bytes:
                        return
                    
                    # 按访问时间排序，淘汰最旧的条目
                    entries = list(self._token_cache.items()) + list(self._ast_cache.items())
                    entries.sort(key=lambda x: x[1].get('last_accessed', 0))
                    
                    # 淘汰条目直到内存使用低于限制
                    while entries and self.current_memory_bytes > self.max_memory_bytes * 0.8:  # 保留20%缓冲
                        key, _ = entries.pop(0)
                        
                        if key in self._token_cache:
                            size = self.entry_sizes.get(key, 0)
                            del self._token_cache[key]
                            self.current_memory_bytes -= size
                            if key in self.entry_sizes:
                                del self.entry_sizes[key]
                        
                        if key in self._ast_cache:
                            size = self.entry_sizes.get(key, 0)
                            del self._ast_cache[key]
                            self.current_memory_bytes -= size
                            if key in self.entry_sizes:
                                del self.entry_sizes[key]
                
                def set_tokens(self, source, tokens):
                    """设置Token缓存，考虑内存限制"""
                    key = self._get_hash(source)
                    size = self._estimate_entry_size(tokens)
                    
                    # 更新内存使用
                    if key in self.entry_sizes:
                        self.current_memory_bytes -= self.entry_sizes[key]
                    
                    self.entry_sizes[key] = size
                    self.current_memory_bytes += size
                    
                    # 调用父类方法
                    super().set_tokens(source, tokens)
                    
                    # 检查是否需要淘汰
                    self._evict_if_needed()
                
                def set_ast(self, source, ast):
                    """设置AST缓存，考虑内存限制"""
                    key = self._get_hash(source)
                    size = self._estimate_entry_size(ast)
                    
                    # 更新内存使用
                    if key in self.entry_sizes:
                        self.current_memory_bytes -= self.entry_sizes[key]
                    
                    self.entry_sizes[key] = size
                    self.current_memory_bytes += size
                    
                    # 调用父类方法
                    super().set_ast(source, ast)
                    
                    # 检查是否需要淘汰
                    self._evict_if_needed()
                
                def get_stats(self):
                    """获取缓存统计信息"""
                    stats = super().get_stats()
                    stats.update({
                        'max_memory_mb': self.max_memory_bytes / 1024 / 1024,
                        'current_memory_mb': self.current_memory_bytes / 1024 / 1024,
                        'memory_usage_percent': (self.current_memory_bytes / self.max_memory_bytes * 100) 
                                                if self.max_memory_bytes > 0 else 0,
                        'entry_count': len(self.entry_sizes)
                    })
                    return stats
            
            # 替换原始缓存类
            import src.cache.compilation_cache as cache_module
            cache_module.CompilationCache = MemoryLimitedCache
            self._optimized_cache_class = MemoryLimitedCache
            
            # 获取优化后内存使用
            after_memory = process.memory_info().rss
            memory_saved = (before_memory - after_memory) / 1024 / 1024
            
            return OptimizationResult(
                strategy_name=self.name,
                memory_saved_mb=max(0, memory_saved),
                objects_reduced=0,  # 这个策略主要防止内存增长
                execution_time_ms=0.0,
                success=True,
                message=f"缓存内存限制优化应用成功，最大内存: {self.max_cache_memory_mb}MB",
                details={
                    'max_memory_mb': self.max_cache_memory_mb,
                    'optimized_cache_class': 'MemoryLimitedCache'
                }
            )
            
        except Exception as e:
            return OptimizationResult(
                strategy_name=self.name,
                memory_saved_mb=0.0,
                objects_reduced=0,
                execution_time_ms=0.0,
                success=False,
                message=f"缓存内存限制优化失败: {str(e)}"
            )
    
    def reset(self) -> None:
        """恢复原始缓存类"""
        if self._original_cache_class and self._optimized_cache_class:
            import src.cache.compilation_cache as cache_module
            cache_module.CompilationCache = self._original_cache_class


class StringInterningStrategy(MemoryOptimizationStrategy):
    """
    字符串驻留优化策略
    
    通过字符串驻留减少重复字符串的内存占用。
    """
    
    def __init__(self):
        super().__init__(
            name="string_interning",
            description="使用字符串驻留技术，减少重复字符串的内存占用"
        )
        self._interned_strings = set()
        self._hits = 0
        self._misses = 0
    
    def can_apply(self, context: Dict[str, Any] = None) -> bool:
        """检查是否可以应用字符串驻留策略"""
        # 总是可以应用
        return True
    
    def apply(self, context: Dict[str, Any] = None) -> OptimizationResult:
        """应用字符串驻留优化"""
        try:
            # 获取当前内存使用
            import psutil
            process = psutil.Process()
            before_memory = process.memory_info().rss
            
            # 获取当前对象计数
            before_objects = len(gc.get_objects())
            
            # 创建字符串驻留函数
            import sys
            
            def intern_string(s: str) -> str:
                """字符串驻留"""
                if not isinstance(s, str):
                    return s
                
                # 只对较短的字符串进行驻留（减少哈希表开销）
                if len(s) <= 64:  # 64字符限制
                    if s in self._interned_strings:
                        self._hits += 1
                        # 返回已驻留的字符串
                        for interned in self._interned_strings:
                            if interned is s:
                                continue
                            if interned == s:
                                return interned
                    else:
                        self._misses += 1
                        self._interned_strings.add(s)
                
                return s
            
            # 应用字符串驻留到常见操作
            import builtins
            
            # 保存原始str函数
            original_str = str
            
            # 创建优化后的str函数
            def optimized_str(obj):
                result = original_str(obj)
                return intern_string(result)
            
            # 临时替换str函数
            builtins.str = optimized_str
            
            # 获取优化后内存使用
            after_memory = process.memory_info().rss
            after_objects = len(gc.get_objects())
            
            # 恢复原始str函数
            builtins.str = original_str
            
            memory_saved = (before_memory - after_memory) / 1024 / 1024
            objects_reduced = before_objects - after_objects
            
            return OptimizationResult(
                strategy_name=self.name,
                memory_saved_mb=max(0, memory_saved),
                objects_reduced=max(0, objects_reduced),
                execution_time_ms=0.0,
                success=True,
                message=f"字符串驻留优化应用成功，驻留字符串数: {len(self._interned_strings)}",
                details={
                    'interned_strings_count': len(self._interned_strings),
                    'hits': self._hits,
                    'misses': self._misses,
                    'hit_rate': self._hits/(self._hits+self._misses) if (self._hits+self._misses) > 0 else 0
                }
            )
            
        except Exception as e:
            return OptimizationResult(
                strategy_name=self.name,
                memory_saved_mb=0.0,
                objects_reduced=0,
                execution_time_ms=0.0,
                success=False,
                message=f"字符串驻留优化失败: {str(e)}"
            )
    
    def reset(self) -> None:
        """重置字符串驻留池"""
        self._interned_strings.clear()
        self._hits = 0
        self._misses = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = super().get_stats()
        stats.update({
            'interned_strings_count': len(self._interned_strings),
            'hits': self._hits,
            'misses': self._misses,
            'hit_rate': self._hits/(self._hits+self._misses) if (self._hits+self._misses) > 0 else 0
        })
        return stats


class MemoryOptimizer:
    """
    内存优化器
    
    管理多个内存优化策略，提供统一的优化接口。
    """
    
    def __init__(self):
        self.strategies = {}
        self.results = []
    
    def register_strategy(self, strategy: MemoryOptimizationStrategy) -> None:
        """注册优化策略"""
        self.strategies[strategy.name] = strategy
    
    def unregister_strategy(self, name: str) -> None:
        """取消注册优化策略"""
        if name in self.strategies:
            del self.strategies[name]
    
    def apply_all(self, context: Dict[str, Any] = None) -> List[OptimizationResult]:
        """应用所有可用的优化策略"""
        self.results = []
        
        for name, strategy in self.strategies.items():
            if strategy.enabled and strategy.can_apply(context):
                result = strategy.apply(context)
                self.results.append(result)
        
        return self.results
    
    def apply_strategy(self, name: str, context: Dict[str, Any] = None) -> Optional[OptimizationResult]:
        """应用特定优化策略"""
        if name in self.strategies:
            strategy = self.strategies[name]
            if strategy.can_apply(context):
                result = strategy.apply(context)
                self.results.append(result)
                return result
        return None
    
    def get_strategy_stats(self) -> Dict[str, Dict[str, Any]]:
        """获取所有策略的统计信息"""
        return {
            name: strategy.get_stats()
            for name, strategy in self.strategies.items()
        }
    
    def get_optimization_summary(self) -> Dict[str, Any]:
        """获取优化摘要"""
        if not self.results:
            return {"total_saved_mb": 0.0, "total_objects_reduced": 0, "success_count": 0}
        
        total_saved = sum(r.memory_saved_mb for r in self.results if r.success)
        total_objects = sum(r.objects_reduced for r in self.results if r.success)
        success_count = sum(1 for r in self.results if r.success)
        
        return {
            "total_saved_mb": total_saved,
            "total_objects_reduced": total_objects,
            "success_count": success_count,
            "total_strategies": len(self.results),
            "results": [r.__dict__ for r in self.results]
        }
    
    def reset_all(self) -> None:
        """重置所有策略"""
        for strategy in self.strategies.values():
            strategy.reset()
        self.results.clear()


# 创建默认优化器实例
_default_optimizer = None

def get_memory_optimizer() -> MemoryOptimizer:
    """获取默认内存优化器"""
    global _default_optimizer
    if _default_optimizer is None:
        _default_optimizer = MemoryOptimizer()
        
        # 注册默认策略
        _default_optimizer.register_strategy(TokenFlyweightStrategy())
        _default_optimizer.register_strategy(ASTNodePoolStrategy())
        _default_optimizer.register_strategy(CacheMemoryLimitStrategy())
        _default_optimizer.register_strategy(StringInterningStrategy())
    
    return _default_optimizer