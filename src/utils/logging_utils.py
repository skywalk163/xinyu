"""
日志工具模块

提供统一的日志功能，减少重复的打印语句和日志代码。
"""

import inspect
import logging
import sys
import time
import traceback
from pathlib import Path
from typing import Any, Dict, Optional


def setup_logging(
    name: str = "app",
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    console: bool = True,
    format_str: Optional[str] = None,
    date_format: str = "%Y-%m-%d %H:%M:%S",
) -> logging.Logger:
    """
    设置日志配置

    Args:
        name: 日志器名称
        level: 日志级别
        log_file: 日志文件路径（可选）
        console: 是否输出到控制台
        format_str: 日志格式字符串
        date_format: 日期格式

    Returns:
        配置好的日志器
    """
    if format_str is None:
        format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # 创建格式化器
    formatter = logging.Formatter(format_str, date_format)

    # 创建日志器
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 清除现有的处理器
    logger.handlers.clear()

    # 添加控制台处理器
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # 添加文件处理器
    if log_file:
        # 确保日志目录存在
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "app") -> logging.Logger:
    """
    获取或创建日志器

    Args:
        name: 日志器名称

    Returns:
        日志器实例
    """
    return logging.getLogger(name)


def log_exception(
    logger: logging.Logger,
    exception: Exception,
    message: str = "发生异常",
    level: int = logging.ERROR,
    include_traceback: bool = True,
) -> None:
    """
    记录异常信息

    Args:
        logger: 日志器
        exception: 异常对象
        message: 自定义消息
        level: 日志级别
        include_traceback: 是否包含堆栈跟踪
    """
    if include_traceback:
        exc_info = (type(exception), exception, exception.__traceback__)
        logger.log(level, f"{message}: {exception}", exc_info=exc_info)
    else:
        logger.log(level, f"{message}: {exception}")


def log_function_call(
    logger: logging.Logger,
    level: int = logging.DEBUG,
    include_args: bool = True,
    include_kwargs: bool = True,
):
    """
    记录函数调用的装饰器

    Args:
        logger: 日志器
        level: 日志级别
        include_args: 是否包含位置参数
        include_kwargs: 是否包含关键字参数

    Returns:
        装饰器函数
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            # 获取函数信息
            func_name = func.__name__
            module_name = func.__module__

            # 构建日志消息
            log_parts = [f"调用函数: {module_name}.{func_name}"]

            if include_args and args:
                args_str = ", ".join(repr(arg) for arg in args)
                log_parts.append(f"位置参数: [{args_str}]")

            if include_kwargs and kwargs:
                kwargs_str = ", ".join(f"{k}={repr(v)}" for k, v in kwargs.items())
                log_parts.append(f"关键字参数: {{{kwargs_str}}}")

            log_message = " | ".join(log_parts)
            logger.log(level, log_message)

            # 执行函数
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time
                logger.log(level, f"函数 {func_name} 执行完成，耗时: {elapsed:.4f}秒")
                return result
            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(f"函数 {func_name} 执行失败，耗时: {elapsed:.4f}秒，异常: {e}")
                raise

        return wrapper

    return decorator


def log_performance(logger: logging.Logger, level: int = logging.INFO, threshold: float = 1.0):  # 秒
    """
    记录函数性能的装饰器

    Args:
        logger: 日志器
        level: 日志级别
        threshold: 性能阈值（秒），超过此值记录警告

    Returns:
        装饰器函数
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            module_name = func.__module__

            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time

                if elapsed > threshold:
                    logger.warning(
                        f"函数 {module_name}.{func_name} 执行缓慢: {elapsed:.4f}秒 " f"(阈值: {threshold}秒)"
                    )
                else:
                    logger.log(level, f"函数 {module_name}.{func_name} 执行时间: {elapsed:.4f}秒")

                return result
            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(f"函数 {module_name}.{func_name} 执行失败，耗时: {elapsed:.4f}秒，异常: {e}")
                raise

        return wrapper

    return decorator


def log_memory_usage(logger: logging.Logger, level: int = logging.DEBUG, include_gc: bool = True):
    """
    记录函数内存使用的装饰器

    Args:
        logger: 日志器
        level: 日志级别
        include_gc: 是否包含垃圾回收信息

    Returns:
        装饰器函数
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            module_name = func.__module__

            # 导入psutil（可选）
            try:
                import psutil

                has_psutil = True
            except ImportError:
                has_psutil = False
                logger.debug("psutil模块未安装，无法记录内存使用")

            if has_psutil:
                process = psutil.Process()
                memory_before = process.memory_info().rss / 1024 / 1024  # MB

            if include_gc:
                import gc

                gc_before = gc.get_count()

            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time

                log_parts = [f"函数 {module_name}.{func_name} 执行时间: {elapsed:.4f}秒"]

                if has_psutil:
                    memory_after = process.memory_info().rss / 1024 / 1024  # MB
                    memory_diff = memory_after - memory_before
                    log_parts.append(f"内存变化: {memory_diff:+.2f}MB")

                if include_gc:
                    gc_after = gc.get_count()
                    gc_diff = tuple(a - b for a, b in zip(gc_after, gc_before))
                    log_parts.append(f"GC变化: {gc_diff}")

                logger.log(level, " | ".join(log_parts))
                return result
            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(f"函数 {module_name}.{func_name} 执行失败，耗时: {elapsed:.4f}秒，异常: {e}")
                raise

        return wrapper

    return decorator


def format_log_message(
    level: str,
    message: str,
    module: Optional[str] = None,
    function: Optional[str] = None,
    line: Optional[int] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> str:
    """
    格式化日志消息

    Args:
        level: 日志级别
        message: 消息内容
        module: 模块名（可选）
        function: 函数名（可选）
        line: 行号（可选）
        extra: 额外信息（可选）

    Returns:
        格式化的日志消息
    """
    parts = []

    # 添加时间戳
    parts.append(time.strftime("%Y-%m-%d %H:%M:%S"))

    # 添加日志级别
    parts.append(level.upper())

    # 添加模块和函数信息
    if module or function:
        location_parts = []
        if module:
            location_parts.append(module)
        if function:
            location_parts.append(function)
        if line:
            location_parts.append(f"line {line}")
        parts.append(f"[{'.'.join(location_parts)}]")

    # 添加消息
    parts.append(message)

    # 添加额外信息
    if extra:
        extra_str = " ".join(f"{k}={v}" for k, v in extra.items())
        parts.append(f"({extra_str})")

    return " - ".join(parts)


def print_progress(
    current: int,
    total: int,
    prefix: str = "进度",
    suffix: str = "完成",
    length: int = 50,
    fill: str = "█",
    print_end: str = "\r",
) -> None:
    """
    打印进度条

    Args:
        current: 当前进度
        total: 总进度
        prefix: 前缀文本
        suffix: 后缀文本
        length: 进度条长度
        fill: 填充字符
        print_end: 打印结束字符
    """
    percent = f"{100 * (current / float(total)):.1f}"
    filled_length = int(length * current // total)
    bar = fill * filled_length + "-" * (length - filled_length)

    print(f"\r{prefix} |{bar}| {percent}% {suffix}", end=print_end, flush=True)

    # 完成后换行
    if current == total:
        print()


class Timer:
    """计时器上下文管理器"""

    def __init__(self, name: str = "操作", logger: Optional[logging.Logger] = None):
        self.name = name
        self.logger = logger
        self.start_time = None
        self.elapsed = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.time() - self.start_time

        if self.logger:
            if exc_type is None:
                self.logger.info(f"{self.name} 完成，耗时: {self.elapsed:.4f}秒")
            else:
                self.logger.error(f"{self.name} 失败，耗时: {self.elapsed:.4f}秒")
        else:
            if exc_type is None:
                print(f"{self.name} 完成，耗时: {self.elapsed:.4f}秒")
            else:
                print(f"{self.name} 失败，耗时: {self.elapsed:.4f}秒")

    def get_elapsed(self) -> float:
        """获取经过的时间"""
        if self.elapsed is not None:
            return self.elapsed
        return time.time() - self.start_time
