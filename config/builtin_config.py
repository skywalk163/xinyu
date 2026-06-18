"""
心语语言内置函数和模块配置

该配置文件定义内置函数和标准库模块的配置信息。
"""

# 内置函数配置
BUILTIN_CONFIG = {
    # 是否启用参数验证
    "enable_param_validation": True,
    # 是否启用异常转换
    "enable_exception_translation": True,
    # 是否启用中文文档
    "enable_chinese_docs": True,
    # 是否启用性能缓存
    "enable_cache": True,
    # 危险函数权限控制
    "dangerous_functions": {
        "eval": {
            "enabled": False,  # 默认禁用
            "require_permission": True,
            "description": "动态代码执行，存在安全风险",
        },
        "exec": {
            "enabled": False,  # 默认禁用
            "require_permission": True,
            "description": "动态代码执行，存在安全风险",
        },
        "compile": {
            "enabled": False,  # 默认禁用
            "require_permission": True,
            "description": "代码编译，存在安全风险",
        },
    },
}

# 标准库模块配置
STDLIB_CONFIG = {
    # 优先实现的模块列表（20个）
    "priority_modules": [
        "math",  # 数学函数
        "os",  # 操作系统接口
        "sys",  # 系统相关
        "json",  # JSON处理
        "datetime",  # 日期时间
        "re",  # 正则表达式
        "collections",  # 高级数据结构
        "itertools",  # 迭代器
        "functools",  # 高阶函数
        "random",  # 随机数
        "pathlib",  # 路径操作
        "typing",  # 类型提示
        "io",  # 输入输出流
        "string",  # 字符串操作
        "textwrap",  # 文本格式化
        "copy",  # 对象复制
        "pprint",  # 格式化打印
        "time",  # 时间访问
        "logging",  # 日志记录
        "argparse",  # 命令行参数解析
    ],
    # 模块懒加载配置
    "lazy_loading": True,
    # 模块缓存配置
    "module_cache": {"enabled": True, "max_size": 100},  # 最多缓存100个模块
}

# 中文命名映射配置
NAME_MAPPING_CONFIG = {
    # 是否允许英文调用
    "allow_english_names": True,
    # 是否允许中文调用
    "allow_chinese_names": True,
    # 是否支持别名
    "support_aliases": True,
    # 默认语言
    "default_language": "chinese",
}

# 错误信息配置
ERROR_MESSAGE_CONFIG = {
    # 错误信息语言
    "language": "chinese",
    # 是否显示原始异常
    "show_original_exception": False,
    # 是否显示堆栈跟踪
    "show_traceback": True,
}
