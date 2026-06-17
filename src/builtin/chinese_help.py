"""
中文帮助系统

提供内置函数和模块的中文帮助文档查看功能。
"""

from .builtin_docs import get_doc
from .name_mapper import NameMapper


class ChineseHelp:
    """中文帮助系统"""

    def __init__(self, name_mapper: NameMapper = None):
        """
        初始化帮助系统

        Args:
            name_mapper: 名称映射器
        """
        self.name_mapper = name_mapper or NameMapper()
        self.name_mapper.register_builtin_mappings()

    def help(self, obj=None) -> None:
        """
        显示帮助信息

        Args:
            obj: 要查看帮助的对象（函数名、模块名等）
        """
        if obj is None:
            self._show_general_help()
            return

        # 如果是字符串，尝试查找函数或模块文档
        if isinstance(obj, str):
            # 先尝试作为函数名查找
            doc = get_doc(obj)
            if doc and not doc.startswith("暂无"):
                print(doc)
                return

            # 尝试转换中文名
            english_name = self.name_mapper.to_english(obj)
            if english_name:
                doc = get_doc(english_name)
                if doc and not doc.startswith("暂无"):
                    print(doc)
                    return

            # 未找到文档
            print(f"未找到 '{obj}' 的帮助文档")
            return

        # 如果是对象，显示其类型和属性
        print(f"类型: {type(obj).__name__}")
        print(f"值: {obj}")
        if hasattr(obj, "__doc__") and obj.__doc__:
            print(f"\n文档:\n{obj.__doc__}")

    def _show_general_help(self) -> None:
        """显示通用帮助信息"""
        print(
            """
心语语言帮助系统
================

欢迎使用心语语言！这是一个支持中文编程的语言系统。

内置函数分类:
-------------
1. 数学函数: 绝对值, 最大值, 最小值, 求和, 幂运算, 四舍五入, 除法余数, 复数
2. 类型转换: 转整数, 转浮点, 转字符串, 转布尔, 转列表, 转字典, 转元组, 转集合
3. 序列操作: 长度, 范围, 枚举, 拉链, 映射, 过滤, 排序, 反转
4. 对象操作: 类型, 是实例, 是子类, 有属性, 取属性, 设属性, 删属性
5. 输入输出: 打印, 输入, 打开, 格式化
6. 其他函数: 标识, 哈希, 表示, 二进制, 八进制, 十六进制, 转字符, 转编码

标准库模块:
-----------
- 数学: 数学函数库
- 系统: 操作系统接口
- 系统信息: 系统相关功能
- JSON: JSON数据处理
- 日期时间: 日期时间处理
- 正则: 正则表达式
- 集合: 高级数据结构
- 迭代工具: 迭代器工具
- 函数工具: 高阶函数工具
- 随机: 随机数生成
- 路径: 路径操作
- 时间: 时间访问

使用方法:
---------
查看函数帮助: 帮助('函数名')
查看模块帮助: 帮助('模块名')
列出所有函数: 列出所有函数()

示例:
    帮助('绝对值')
    帮助('最大值')
    帮助('排序')
"""
        )

    def list_all_functions(self) -> None:
        """列出所有内置函数"""
        print("\n所有内置函数列表:")
        print("=" * 60)

        # 数学函数
        print("\n数学函数:")
        print("  绝对值, 最大值, 最小值, 求和, 幂运算, 四舍五入, 除法余数, 复数")

        # 类型转换函数
        print("\n类型转换函数:")
        print("  转整数, 转浮点, 转字符串, 转布尔, 转列表, 转字典, 转元组, 转集合")
        print("  转冻结集合, 转字节, 转字节数组, 转内存视图")

        # 序列操作函数
        print("\n序列操作函数:")
        print("  长度, 范围, 枚举, 拉链, 映射, 过滤, 排序, 反转")
        print("  迭代器, 下一个, 全部为真, 任一为真, 切片")

        # 对象操作函数
        print("\n对象操作函数:")
        print("  类型, 是实例, 是子类, 有属性, 取属性, 设属性, 删属性")

        # IO函数
        print("\n输入输出函数:")
        print("  打印, 输入, 打开, 格式化")

        # 其他函数
        print("\n其他函数:")
        print("  标识, 哈希, 表示, ASCII表示, 二进制, 八进制, 十六进制")
        print("  转字符, 转编码, 可调用, 帮助, 求值, 执行, 编译")
        print("  全局变量, 局部变量")

        print("\n" + "=" * 60)
        print("总计: 69个内置函数")

    def list_all_modules(self) -> None:
        """列出所有可用模块"""
        print("\n所有可用模块列表:")
        print("=" * 60)

        modules = [
            ("数学", "数学函数库", "平方根, 正弦, 余弦, 圆周率, 自然常数等"),
            ("系统", "操作系统接口", "获取当前目录, 列出目录, 创建目录等"),
            ("系统信息", "系统相关功能", "版本, 平台, 命令行参数等"),
            ("JSON", "JSON数据处理", "转字符串, 加载字符串等"),
            ("日期时间", "日期时间处理", "当前时间, 今天等"),
            ("正则", "正则表达式", "匹配, 搜索, 查找所有, 替换等"),
            ("集合", "高级数据结构", "计数器, 默认字典, 有序字典, 命名元组等"),
            ("迭代工具", "迭代器工具", "计数, 循环, 重复, 排列, 组合等"),
            ("函数工具", "高阶函数工具", "缓存, 记忆化, 偏函数, 归约等"),
            ("随机", "随机数生成", "随机数, 随机整数, 随机选择, 随机打乱等"),
            ("路径", "路径操作", "路径, 当前目录, 主目录等"),
            ("时间", "时间访问", "当前时间, 格式化时间, 睡眠等"),
        ]

        for i, (name, desc, funcs) in enumerate(modules, 1):
            print(f"\n{i}. {name} - {desc}")
            print(f"   主要功能: {funcs}")

        print("\n" + "=" * 60)
        print(f"总计: {len(modules)}个标准库模块")


# 创建全局帮助实例
_help_instance = None


def get_help_instance() -> ChineseHelp:
    """获取全局帮助实例"""
    global _help_instance
    if _help_instance is None:
        _help_instance = ChineseHelp()
    return _help_instance


def chinese_help(obj=None) -> None:
    """
    中文帮助函数

    Args:
        obj: 要查看帮助的对象
    """
    help_instance = get_help_instance()
    help_instance.help(obj)
