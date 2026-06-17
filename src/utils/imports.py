"""
导入工具模块

提供统一的导入管理，减少重复的导入语句。
"""

import sys
import importlib
import importlib.util
from typing import Any, Optional, Tuple, Union


def import_optional(module_name: str, package: str = None) -> Optional[Any]:
    """
    尝试导入可选模块，如果失败则返回None
    
    Args:
        module_name: 模块名
        package: 包名（可选）
        
    Returns:
        导入的模块或None
    """
    try:
        return importlib.import_module(module_name, package)
    except ImportError:
        return None


def import_with_fallback(primary_module: str, fallback_module: str, 
                        package: str = None) -> Tuple[Any, bool]:
    """
    尝试导入主要模块，如果失败则导入备用模块
    
    Args:
        primary_module: 主要模块名
        fallback_module: 备用模块名
        package: 包名（可选）
        
    Returns:
        (module, is_primary): 导入的模块和是否使用了主要模块
    """
    try:
        module = importlib.import_module(primary_module, package)
        return module, True
    except ImportError:
        try:
            module = importlib.import_module(fallback_module, package)
            return module, False
        except ImportError:
            raise ImportError(
                f"无法导入模块: {primary_module} 或 {fallback_module}"
            )


def check_module_exists(module_name: str) -> bool:
    """
    检查模块是否存在
    
    Args:
        module_name: 模块名
        
    Returns:
        模块是否存在
    """
    spec = importlib.util.find_spec(module_name)
    return spec is not None


def lazy_import(module_name: str, package: str = None):
    """
    延迟导入装饰器
    
    Args:
        module_name: 模块名
        package: 包名（可选）
        
    Returns:
        装饰器函数
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            module = importlib.import_module(module_name, package)
            return func(module, *args, **kwargs)
        return wrapper
    return decorator


# 常用模块的延迟导入装饰器
def with_psutil(func):
    """使用psutil模块的装饰器"""
    return lazy_import('psutil')(func)


def with_tracemalloc(func):
    """使用tracemalloc模块的装饰器"""
    return lazy_import('tracemalloc')(func)


def with_gc(func):
    """使用gc模块的装饰器"""
    return lazy_import('gc')(func)


def with_time(func):
    """使用time模块的装饰器"""
    return lazy_import('time')(func)


def with_json(func):
    """使用json模块的装饰器"""
    return lazy_import('json')(func)


def with_yaml(func):
    """使用yaml模块的装饰器"""
    return lazy_import('yaml')(func)


def with_dataclasses(func):
    """使用dataclasses模块的装饰器"""
    return lazy_import('dataclasses')(func)


def with_typing(func):
    """使用typing模块的装饰器"""
    return lazy_import('typing')(func)


def with_os(func):
    """使用os模块的装饰器"""
    return lazy_import('os')(func)


def with_sys(func):
    """使用sys模块的装饰器"""
    return lazy_import('sys')(func)


# 预检查常用模块是否存在
HAS_PSUTIL = check_module_exists('psutil')
HAS_TRACEMALLOC = check_module_exists('tracemalloc')
HAS_YAML = check_module_exists('yaml')
HAS_OBJGRAPH = check_module_exists('objgraph')


def get_available_modules() -> dict:
    """
    获取可用的模块列表
    
    Returns:
        模块可用性字典
    """
    return {
        'psutil': HAS_PSUTIL,
        'tracemalloc': HAS_TRACEMALLOC,
        'yaml': HAS_YAML,
        'objgraph': HAS_OBJGRAPH,
    }


# 常用导入的快捷方式
if HAS_PSUTIL:
    import psutil
if HAS_TRACEMALLOC:
    import tracemalloc
if HAS_YAML:
    import yaml
if HAS_OBJGRAPH:
    import objgraph

import os
import sys
import json
import time
import gc
import dataclasses
from typing import *