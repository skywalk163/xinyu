"""
错误处理工具模块

提供统一的错误处理功能，减少重复的错误处理代码。
"""

import sys
import traceback
from typing import Any, Dict, List, Optional, Union, Callable
from dataclasses import dataclass, field
from enum import Enum, auto
import inspect


class ErrorSeverity(Enum):
    """错误严重程度"""
    INFO = auto()      # 信息
    WARNING = auto()   # 警告
    ERROR = auto()     # 错误
    FATAL = auto()     # 致命错误


@dataclass
class ErrorInfo:
    """错误信息"""
    code: str                    # 错误代码
    message: str                 # 错误消息
    severity: ErrorSeverity      # 严重程度
    suggestion: Optional[str] = None  # 修复建议
    category: Optional[str] = None    # 错误类别
    documentation: Optional[str] = None  # 文档链接


@dataclass
class ErrorContext:
    """错误上下文"""
    line: int                    # 行号
    column: int                  # 列号
    source: Optional[str] = None  # 源代码
    file_path: Optional[str] = None  # 文件路径
    function_name: Optional[str] = None  # 函数名
    variables: Dict[str, Any] = field(default_factory=dict)  # 变量值
    stack_trace: Optional[str] = None  # 堆栈跟踪


class BaseError(Exception):
    """基础错误类"""
    
    def __init__(self, 
                 message: str, 
                 code: Optional[str] = None,
                 severity: ErrorSeverity = ErrorSeverity.ERROR,
                 context: Optional[ErrorContext] = None,
                 suggestion: Optional[str] = None):
        """
        初始化基础错误
        
        Args:
            message: 错误消息
            code: 错误代码（可选）
            severity: 错误严重程度
            context: 错误上下文（可选）
            suggestion: 修复建议（可选）
        """
        self.message = message
        self.code = code
        self.severity = severity
        self.context = context
        self.suggestion = suggestion
        self.timestamp = field(default_factory=lambda: time.time())
        
        # 获取调用堆栈
        self.stack_trace = self._get_stack_trace()
        
        super().__init__(self._format_message())
    
    def _get_stack_trace(self) -> str:
        """获取堆栈跟踪"""
        try:
            # 跳过当前帧和BaseError的__init__帧
            frames = inspect.stack()[2:]
            stack_lines = []
            
            for frame in frames:
                filename = frame.filename
                lineno = frame.lineno
                function = frame.function
                code_context = frame.code_context[0].strip() if frame.code_context else ""
                
                stack_lines.append(f"  File \"{filename}\", line {lineno}, in {function}")
                if code_context:
                    stack_lines.append(f"    {code_context}")
            
            return "\n".join(stack_lines)
        except:
            return traceback.format_exc()
    
    def _format_message(self) -> str:
        """格式化错误消息"""
        # 严重程度表情符号
        severity_emoji = {
            ErrorSeverity.INFO: "[INFO]",
            ErrorSeverity.WARNING: "[WARN]",
            ErrorSeverity.ERROR: "[ERROR]",
            ErrorSeverity.FATAL: "[FATAL]",
        }.get(self.severity, "[UNKNOWN]")
        
        # 构建消息
        parts = [f"{severity_emoji} "]
        
        if self.code:
            parts.append(f"[{self.code}] ")
        
        parts.append(self.message)
        
        if self.context:
            if self.context.line and self.context.column:
                parts.append(f" (第 {self.context.line} 行, 第 {self.context.column} 列)")
            if self.context.file_path:
                parts.append(f" 文件: {self.context.file_path}")
            if self.context.function_name:
                parts.append(f" 函数: {self.context.function_name}")
        
        if self.suggestion:
            parts.append(f"\n[建议] {self.suggestion}")
        
        return "".join(parts)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'message': self.message,
            'code': self.code,
            'severity': self.severity.name,
            'timestamp': self.timestamp,
            'context': {
                'line': self.context.line if self.context else None,
                'column': self.context.column if self.context else None,
                'file_path': self.context.file_path if self.context else None,
                'function_name': self.context.function_name if self.context else None,
                'variables': self.context.variables if self.context else {},
            } if self.context else None,
            'suggestion': self.suggestion,
            'stack_trace': self.stack_trace
        }
    
    def __str__(self) -> str:
        return self._format_message()


class ErrorRegistry:
    """错误注册表"""
    
    def __init__(self):
        self._errors: Dict[str, ErrorInfo] = {}
        self._categories: Dict[str, List[str]] = {}
    
    def register(self, error_info: ErrorInfo) -> None:
        """
        注册错误信息
        
        Args:
            error_info: 错误信息
        """
        self._errors[error_info.code] = error_info
        
        # 按类别分组
        if error_info.category:
            if error_info.category not in self._categories:
                self._categories[error_info.category] = []
            self._categories[error_info.category].append(error_info.code)
    
    def get(self, code: str) -> Optional[ErrorInfo]:
        """
        获取错误信息
        
        Args:
            code: 错误代码
            
        Returns:
            错误信息或None
        """
        return self._errors.get(code)
    
    def get_by_category(self, category: str) -> List[ErrorInfo]:
        """
        获取指定类别的所有错误
        
        Args:
            category: 错误类别
            
        Returns:
            错误信息列表
        """
        codes = self._categories.get(category, [])
        return [self._errors[code] for code in codes if code in self._errors]
    
    def get_all(self) -> List[ErrorInfo]:
        """获取所有错误信息"""
        return list(self._errors.values())
    
    def create_error(self, 
                    code: str, 
                    context: Optional[ErrorContext] = None,
                    **format_args) -> BaseError:
        """
        创建错误对象
        
        Args:
            code: 错误代码
            context: 错误上下文
            **format_args: 格式化参数
            
        Returns:
            基础错误对象
        """
        error_info = self.get(code)
        if not error_info:
            return BaseError(
                message=f"未知错误代码: {code}",
                code=code,
                severity=ErrorSeverity.ERROR,
                context=context
            )
        
        # 格式化消息
        try:
            message = error_info.message.format(**format_args)
        except KeyError:
            message = error_info.message
        
        return BaseError(
            message=message,
            code=code,
            severity=error_info.severity,
            context=context,
            suggestion=error_info.suggestion
        )


# 全局错误注册表实例
_error_registry = ErrorRegistry()


def register_error(error_info: ErrorInfo) -> None:
    """
    注册错误信息（快捷函数）
    
    Args:
        error_info: 错误信息
    """
    _error_registry.register(error_info)


def get_error_info(code: str) -> Optional[ErrorInfo]:
    """
    获取错误信息（快捷函数）
    
    Args:
        code: 错误代码
        
    Returns:
        错误信息或None
    """
    return _error_registry.get(code)


def create_error(code: str, 
                context: Optional[ErrorContext] = None,
                **format_args) -> BaseError:
    """
    创建错误对象（快捷函数）
    
    Args:
        code: 错误代码
        context: 错误上下文
        **format_args: 格式化参数
        
    Returns:
        基础错误对象
    """
    return _error_registry.create_error(code, context, **format_args)


def error_handler(func: Callable = None, *, 
                  log_errors: bool = True,
                  reraise: bool = True,
                  default_return: Any = None):
    """
    错误处理装饰器
    
    Args:
        func: 被装饰的函数
        log_errors: 是否记录错误
        reraise: 是否重新抛出错误
        default_return: 错误时的默认返回值
        
    Returns:
        装饰器或装饰后的函数
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                # 记录错误
                if log_errors:
                    _log_exception(e, f.__name__, args, kwargs)
                
                # 重新抛出或返回默认值
                if reraise:
                    raise
                else:
                    return default_return
        
        return wrapper
    
    if func is None:
        return decorator
    return decorator(func)


def _log_exception(exception: Exception, 
                  function_name: str,
                  args: tuple,
                  kwargs: dict) -> None:
    """记录异常"""
    import logging
    
    logger = logging.getLogger(__name__)
    
    # 构建错误消息
    error_msg = f"函数 {function_name} 执行失败: {exception}"
    
    # 添加参数信息
    if args:
        error_msg += f"\n  位置参数: {args}"
    if kwargs:
        error_msg += f"\n  关键字参数: {kwargs}"
    
    # 添加堆栈跟踪
    error_msg += f"\n  堆栈跟踪:\n{traceback.format_exc()}"
    
    # 记录错误
    logger.error(error_msg)


def format_exception(exception: Exception, 
                    include_traceback: bool = True) -> str:
    """
    格式化异常信息
    
    Args:
        exception: 异常对象
        include_traceback: 是否包含堆栈跟踪
        
    Returns:
        格式化的异常信息
    """
    # 获取异常类型和消息
    exc_type = type(exception).__name__
    exc_msg = str(exception)
    
    # 构建基本消息
    parts = [f"{exc_type}: {exc_msg}"]
    
    # 添加堆栈跟踪
    if include_traceback:
        tb_lines = traceback.format_exception(type(exception), exception, exception.__traceback__)
        parts.append("\n堆栈跟踪:")
        parts.extend(tb_lines)
    
    return "\n".join(parts)


def safe_execute(func: Callable, 
                *args, 
                default: Any = None,
                log_errors: bool = True,
                **kwargs) -> Any:
    """
    安全执行函数
    
    Args:
        func: 要执行的函数
        default: 错误时的默认返回值
        log_errors: 是否记录错误
        *args: 位置参数
        **kwargs: 关键字参数
        
    Returns:
        函数结果或默认值
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if log_errors:
            _log_exception(e, func.__name__, args, kwargs)
        return default


def retry_on_error(func: Callable = None, *,
                   max_attempts: int = 3,
                   delay: float = 1.0,
                   backoff_factor: float = 2.0,
                   exceptions: tuple = (Exception,)):
    """
    错误重试装饰器
    
    Args:
        func: 被装饰的函数
        max_attempts: 最大尝试次数
        delay: 初始延迟（秒）
        backoff_factor: 退避因子
        exceptions: 要捕获的异常类型
        
    Returns:
        装饰器或装饰后的函数
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    # 如果是最后一次尝试，重新抛出异常
                    if attempt == max_attempts - 1:
                        raise
                    
                    # 计算延迟时间
                    current_delay = delay * (backoff_factor ** attempt)
                    
                    # 记录重试信息
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning(
                        f"函数 {f.__name__} 执行失败，"
                        f"{attempt + 1}/{max_attempts} 次尝试，"
                        f"{current_delay:.1f}秒后重试: {e}"
                    )
                    
                    # 等待
                    import time
                    time.sleep(current_delay)
            
            # 理论上不会执行到这里
            raise last_exception
        
        return wrapper
    
    if func is None:
        return decorator
    return decorator(func)


# 导入必要的模块
import time
import functools

# 预定义一些常见的错误信息
_common_errors = [
    ErrorInfo(
        code="INTERNAL_ERROR",
        message="内部错误: {message}",
        severity=ErrorSeverity.FATAL,
        suggestion="请检查系统状态或联系支持",
        category="system"
    ),
    ErrorInfo(
        code="VALIDATION_ERROR",
        message="验证失败: {field} {message}",
        severity=ErrorSeverity.ERROR,
        suggestion="请检查输入数据格式",
        category="validation"
    ),
    ErrorInfo(
        code="CONFIG_ERROR",
        message="配置错误: {key}={value}",
        severity=ErrorSeverity.ERROR,
        suggestion="请检查配置文件格式和值",
        category="configuration"
    ),
    ErrorInfo(
        code="IO_ERROR",
        message="IO错误: {operation} {path} - {reason}",
        severity=ErrorSeverity.ERROR,
        suggestion="请检查文件权限和路径",
        category="io"
    ),
    ErrorInfo(
        code="NETWORK_ERROR",
        message="网络错误: {operation} {url} - {reason}",
        severity=ErrorSeverity.ERROR,
        suggestion="请检查网络连接和URL",
        category="network"
    ),
    ErrorInfo(
        code="TIMEOUT_ERROR",
        message="超时错误: {operation} 超过 {timeout}秒",
        severity=ErrorSeverity.ERROR,
        suggestion="请增加超时时间或优化操作",
        category="timeout"
    ),
    ErrorInfo(
        code="MEMORY_ERROR",
        message="内存错误: {operation} 使用 {memory}MB 超过限制",
        severity=ErrorSeverity.ERROR,
        suggestion="请优化内存使用或增加内存限制",
        category="memory"
    ),
    ErrorInfo(
        code="PERMISSION_ERROR",
        message="权限错误: {operation} {resource} - {reason}",
        severity=ErrorSeverity.ERROR,
        suggestion="请检查文件或资源权限",
        category="permission"
    ),
]

# 注册常见错误
for error_info in _common_errors:
    register_error(error_info)