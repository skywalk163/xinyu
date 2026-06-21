"""
模块管理器

处理模块导入和生命周期管理。
"""

import importlib
from typing import Any, Dict

from .wrappers import (
    ArgparseWrapper,
    AsyncioWrapper,
    Base64Wrapper,
    BisectWrapper,
    CollectionsWrapper,
    ConfigparserWrapper,
    CopyWrapper,
    CsvWrapper,
    DatetimeWrapper,
    DbmWrapper,
    DecimalWrapper,
    DoctestWrapper,
    FnmatchWrapper,
    FunctoolsWrapper,
    GettextWrapper,
    GlobWrapper,
    GzipWrapper,
    HashlibWrapper,
    HeapqWrapper,
    HttpWrapper,
    InspectWrapper,
    ItertoolsWrapper,
    JsonWrapper,
    LinecacheWrapper,
    LocaleWrapper,
    LoggingWrapper,
    MathWrapper,
    OsWrapper,
    PathlibWrapper,
    PickleWrapper,
    PprintWrapper,
    QueueWrapper,
    RandomWrapper,
    ReWrapper,
    SecretsWrapper,
    ShutilWrapper,
    SocketWrapper,
    Sqlite3Wrapper,
    SslWrapper,
    StatisticsWrapper,
    StringWrapper,
    StructWrapper,
    SubprocessWrapper,
    SysWrapper,
    TarfileWrapper,
    TempfileWrapper,
    TextwrapWrapper,
    ThreadingWrapper,
    TimeWrapper,
    TkinterWrapper,
    TracebackWrapper,
    TypingWrapper,
    UnittestWrapper,
    UrllibWrapper,
    XmlEtreeWrapper,
    ZipfileWrapper,
    ZlibWrapper,
)


class ModuleManager:
    """模块管理器"""

    def __init__(self):
        """初始化模块管理器"""
        self._modules: Dict[str, Any] = {}
        self._cache: Dict[str, Any] = {}

        # 中文模块名映射
        self._chinese_module_map = {
            "数学": "math",
            "系统": "os",
            "系统信息": "sys",
            "JSON": "json",
            "日期时间": "datetime",
            "正则": "re",
            "集合": "collections",
            "迭代工具": "itertools",
            "函数工具": "functools",
            "随机": "random",
            "路径": "pathlib",
            "时间": "time",
            "字符串": "string",
            "文本包裹": "textwrap",
            "复制": "copy",
            "美化打印": "pprint",
            "序列化": "pickle",
            "CSV": "csv",
            "哈希": "hashlib",
            "文件操作": "shutil",
            "文件匹配": "glob",
            "参数解析": "argparse",
            "日志": "logging",
            "线程": "threading",
            "队列": "queue",
            "小数": "decimal",
            "统计": "statistics",
            "套接字": "socket",
            "SSL": "ssl",
            "HTTP": "http",
            "URL": "urllib",
            "压缩": "zlib",
            "GZIP": "gzip",
            "ZIP": "zipfile",
            "TAR": "tarfile",
            "数据库": "sqlite3",
            "DBM": "dbm",
            "单元测试": "unittest",
            "文档测试": "doctest",
            "异步": "asyncio",
            "图形界面": "tkinter",
            "Base64": "base64",
            "配置": "configparser",
            "子进程": "subprocess",
            "安全随机": "secrets",
            "类型提示": "typing",
            "检查": "inspect",
            "堆栈跟踪": "traceback",
            "国际化": "gettext",
            "本地化": "locale",
            "XML树": "xml.etree.ElementTree",
            "二进制结构": "struct",
            "临时文件": "tempfile",
            "文件名匹配": "fnmatch",
            "行缓存": "linecache",
            "二分查找": "bisect",
            "堆队列": "heapq",
        }

        # 模块封装器映射
        self._wrapper_map = {
            "math": MathWrapper,
            "os": OsWrapper,
            "sys": SysWrapper,
            "json": JsonWrapper,
            "datetime": DatetimeWrapper,
            "re": ReWrapper,
            "collections": CollectionsWrapper,
            "itertools": ItertoolsWrapper,
            "functools": FunctoolsWrapper,
            "random": RandomWrapper,
            "pathlib": PathlibWrapper,
            "time": TimeWrapper,
            "string": StringWrapper,
            "textwrap": TextwrapWrapper,
            "copy": CopyWrapper,
            "pprint": PprintWrapper,
            "pickle": PickleWrapper,
            "csv": CsvWrapper,
            "hashlib": HashlibWrapper,
            "shutil": ShutilWrapper,
            "glob": GlobWrapper,
            "argparse": ArgparseWrapper,
            "logging": LoggingWrapper,
            "threading": ThreadingWrapper,
            "queue": QueueWrapper,
            "decimal": DecimalWrapper,
            "statistics": StatisticsWrapper,
            "socket": SocketWrapper,
            "ssl": SslWrapper,
            "http": HttpWrapper,
            "urllib": UrllibWrapper,
            "zlib": ZlibWrapper,
            "gzip": GzipWrapper,
            "zipfile": ZipfileWrapper,
            "tarfile": TarfileWrapper,
            "sqlite3": Sqlite3Wrapper,
            "dbm": DbmWrapper,
            "unittest": UnittestWrapper,
            "doctest": DoctestWrapper,
            "asyncio": AsyncioWrapper,
            "tkinter": TkinterWrapper,
            "base64": Base64Wrapper,
            "configparser": ConfigparserWrapper,
            "subprocess": SubprocessWrapper,
            "secrets": SecretsWrapper,
            "typing": TypingWrapper,
            "inspect": InspectWrapper,
            "traceback": TracebackWrapper,
            "gettext": GettextWrapper,
            "locale": LocaleWrapper,
            "xml.etree.ElementTree": XmlEtreeWrapper,
            "struct": StructWrapper,
            "tempfile": TempfileWrapper,
            "fnmatch": FnmatchWrapper,
            "linecache": LinecacheWrapper,
            "bisect": BisectWrapper,
            "heapq": HeapqWrapper,
        }

    def import_module(self, name: str, use_chinese_wrapper: bool = True) -> Any:
        """
        导入模块

        Args:
            name: 模块名（中文或英文）
            use_chinese_wrapper: 是否使用中文封装

        Returns:
            模块对象（可能是中文封装）
        """
        # 检查缓存
        if name in self._cache:
            return self._cache[name]

        # 转换中文模块名
        english_name = self._chinese_module_map.get(name, name)

        # 导入Python模块
        try:
            module = importlib.import_module(english_name)
        except ImportError as e:
            raise ImportError(f"无法导入模块: {name} ({english_name})") from e

        # 如果需要中文封装
        if use_chinese_wrapper and english_name in self._wrapper_map:
            wrapper_class = self._wrapper_map[english_name]
            wrapped_module = wrapper_class()
            self._cache[name] = wrapped_module
            self._modules[name] = wrapped_module
            return wrapped_module

        # 否则返回原始模块
        self._cache[name] = module
        self._modules[name] = module
        return module

    def get_attribute(self, module_name: str, attr_name: str) -> Any:
        """
        获取模块属性

        Args:
            module_name: 模块名
            attr_name: 属性名（中文或英文）

        Returns:
            属性值
        """
        module = self.import_module(module_name)
        return getattr(module, attr_name)

    def clear_cache(self) -> None:
        """清空模块缓存"""
        self._cache.clear()

    def list_imported_modules(self) -> list:
        """列出已导入的模块"""
        return list(self._modules.keys())
