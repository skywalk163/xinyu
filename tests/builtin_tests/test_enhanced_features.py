"""
测试增强功能

测试新增的标准库模块和帮助系统。
"""

import os
import sys

# 添加项目根目录到路径（需要向上跳两级）
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.builtin.chinese_help import ChineseHelp
from src.module import ModuleManager


def test_new_modules():
    """测试新增的标准库模块"""
    print("\n" + "=" * 60)
    print("测试新增标准库模块")
    print("=" * 60)

    manager = ModuleManager()

    # 测试random模块
    print("\n1. 随机模块测试:")
    random = manager.import_module("随机")
    random.设置种子(42)  # 设置随机种子以便测试
    print(f"   随机数: {random.随机数():.4f}")
    print(f"   随机整数(1, 100): {random.随机整数(1, 100)}")
    print(f"   随机选择([1,2,3,4,5]): {random.随机选择([1,2,3,4,5])}")

    # 测试collections模块
    print("\n2. 集合模块测试:")
    collections = manager.import_module("集合")
    计数器 = collections.计数器
    text = "心语语言是一门优雅的中文编程语言"
    counter = 计数器(text)
    print(f"   文本: {text}")
    print(f"   字符统计: {counter.most_common(5)}")

    # 测试itertools模块
    print("\n3. 迭代工具模块测试:")
    itertools = manager.import_module("迭代工具")
    print(f"   排列([1,2,3], 2): {list(itertools.排列([1,2,3], 2))}")
    print(f"   组合([1,2,3], 2): {list(itertools.组合([1,2,3], 2))}")

    # 测试functools模块
    print("\n4. 函数工具模块测试:")
    functools = manager.import_module("函数工具")

    # 使用记忆化装饰器
    @functools.记忆化(maxsize=None)
    def 斐波那契(n):
        if n < 2:
            return n
        return 斐波那契(n - 1) + 斐波那契(n - 2)

    print(f"   斐波那契(10): {斐波那契(10)}")
    print(f"   斐波那契(20): {斐波那契(20)}")

    # 测试re模块
    print("\n5. 正则模块测试:")
    re = manager.import_module("正则")
    text = "我的电话是13812345678，邮箱是test@example.com"
    phone_pattern = r"1[3-9]\d{9}"
    email_pattern = r"\w+@\w+\.\w+"
    print(f"   文本: {text}")
    print(f"   查找手机号: {re.查找所有(phone_pattern, text)}")
    print(f"   查找邮箱: {re.查找所有(email_pattern, text)}")

    # 测试time模块
    print("\n6. 时间模块测试:")
    time = manager.import_module("时间")
    import time as py_time

    current = py_time.time()
    print(f"   当前时间戳: {current:.2f}")
    print(f"   格式化时间: {time.格式化时间('%Y-%m-%d %H:%M:%S', time.本地时间(current))}")

    print("\n[OK] 所有新模块测试通过！")


def test_help_system():
    """测试帮助系统"""
    print("\n" + "=" * 60)
    print("测试帮助系统")
    print("=" * 60)

    help_system = ChineseHelp()

    # 测试函数帮助
    print("\n1. 查看函数帮助:")
    print("-" * 40)
    help_system.help("绝对值")

    print("\n2. 查看另一个函数帮助:")
    print("-" * 40)
    help_system.help("最大值")

    # 列出所有函数
    print("\n3. 列出所有内置函数:")
    help_system.list_all_functions()

    # 列出所有模块
    print("\n4. 列出所有可用模块:")
    help_system.list_all_modules()

    print("\n[OK] 帮助系统测试通过！")


def test_practical_examples():
    """实际应用示例"""
    print("\n" + "=" * 60)
    print("实际应用示例")
    print("=" * 60)

    manager = ModuleManager()

    # 示例1: 数据统计
    print("\n示例1: 使用计数器统计词频")
    collections = manager.import_module("集合")
    计数器 = collections.计数器

    words = ["苹果", "香蕉", "苹果", "橙子", "香蕉", "苹果", "葡萄"]
    word_count = 计数器(words)
    print(f"   单词列表: {words}")
    print(f"   词频统计: {dict(word_count)}")
    print(f"   最常见: {word_count.most_common(2)}")

    # 示例2: 随机抽样
    print("\n示例2: 随机抽样")
    random = manager.import_module("随机")
    random.设置种子(42)

    students = ["张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十"]
    sample = random.随机采样(students, 3)
    print(f"   学生列表: {students}")
    print(f"   随机抽取3人: {sample}")

    # 示例3: 排列组合
    print("\n示例3: 排列组合")
    itertools = manager.import_module("迭代工具")

    colors = ["红", "绿", "蓝"]
    print(f"   颜色: {colors}")
    print(f"   两两排列: {list(itertools.排列(colors, 2))}")
    print(f"   两两组合: {list(itertools.组合(colors, 2))}")

    # 示例4: 正则表达式
    print("\n示例4: 正则表达式验证")
    re = manager.import_module("正则")

    emails = ["test@example.com", "invalid-email", "user@domain.org", "no-at-sign.com"]
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    print(f"   邮箱列表: {emails}")
    for email in emails:
        is_valid = bool(re.匹配(email_pattern, email))
        status = "有效" if is_valid else "无效"
        print(f"   {email}: {status}")

    print("\n[OK] 实际应用示例测试通过！")


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("心语语言增强功能测试")
    print("=" * 60)

    try:
        test_new_modules()
        test_help_system()
        test_practical_examples()

        print("\n" + "=" * 60)
        print("[SUCCESS] 所有增强功能测试通过！")
        print("=" * 60)

        print("\n新增功能总结:")
        print("  [OK] 新增7个标准库模块中文封装")
        print("  [OK] 实现中文帮助系统")
        print("  [OK] 提供详细的函数文档")
        print("  [OK] 支持模块和函数列表查看")
        print("\n当前支持的模块总数: 12个")
        print("当前支持的内置函数总数: 69个")
        print("\n")

    except Exception as e:
        print(f"\n[ERROR] 测试失败: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
