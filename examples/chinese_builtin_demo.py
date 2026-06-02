"""
心语语言使用示例

演示如何使用中文内置函数和标准库模块。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.builtin import BuiltinRegistry
from src.module import ModuleManager


def example_basic_functions():
    """基本内置函数示例"""
    print("\n" + "=" * 60)
    print("示例1: 基本内置函数")
    print("=" * 60)
    
    registry = BuiltinRegistry()
    registry.register_all_builtins()
    
    # 数学运算
    print("\n数学运算:")
    print(f"  绝对值(-10) = {registry.call('绝对值', -10)}")
    print(f"  最大值(3, 7, 2, 9) = {registry.call('最大值', 3, 7, 2, 9)}")
    print(f"  最小值(3, 7, 2, 9) = {registry.call('最小值', 3, 7, 2, 9)}")
    print(f"  幂运算(2, 8) = {registry.call('幂运算', 2, 8)}")
    print(f"  四舍五入(3.14159, 2) = {registry.call('四舍五入', 3.14159, 2)}")
    
    # 类型转换
    print("\n类型转换:")
    print(f"  转整数('42') = {registry.call('转整数', '42')}")
    print(f"  转浮点('3.14') = {registry.call('转浮点', '3.14')}")
    print(f"  转字符串(123) = {registry.call('转字符串', 123)}")
    print(f"  转列表('hello') = {registry.call('转列表', 'hello')}")
    
    # 序列操作
    print("\n序列操作:")
    numbers = [1, 2, 3, 4, 5]
    print(f"  数列: {numbers}")
    print(f"  长度 = {registry.call('长度', numbers)}")
    print(f"  求和 = {registry.call('求和', numbers)}")
    print(f"  排序([3,1,4,1,5]) = {list(registry.call('排序', [3,1,4,1,5]))}")
    print(f"  反转([1,2,3]) = {list(registry.call('反转', [1,2,3]))}")


def example_module_usage():
    """模块使用示例"""
    print("\n" + "=" * 60)
    print("示例2: 标准库模块使用")
    print("=" * 60)
    
    manager = ModuleManager()
    
    # 使用math模块
    print("\n数学模块:")
    math = manager.import_module('数学')
    print(f"  圆周率 = {math.圆周率}")
    print(f"  自然常数 = {math.自然常数}")
    print(f"  平方根(16) = {math.平方根(16)}")
    print(f"  正弦(1.57) ≈ {math.正弦(1.57):.2f}")
    print(f"  余弦(0) = {math.余弦(0)}")
    print(f"  向上取整(3.2) = {math.向上取整(3.2)}")
    print(f"  向下取整(3.8) = {math.向下取整(3.8)}")
    
    # 使用json模块
    print("\nJSON模块:")
    json = manager.import_module('JSON')
    data = {"姓名": "张三", "年龄": 25, "城市": "北京"}
    json_str = json.转字符串(data, ensure_ascii=False)
    print(f"  原始数据: {data}")
    print(f"  转字符串: {json_str}")
    parsed = json.加载字符串(json_str)
    print(f"  加载字符串: {parsed}")


def example_practical_application():
    """实际应用示例"""
    print("\n" + "=" * 60)
    print("示例3: 实际应用 - 学生成绩统计")
    print("=" * 60)
    
    registry = BuiltinRegistry()
    registry.register_all_builtins()
    
    # 学生成绩数据
    students = [
        {"姓名": "张三", "成绩": 85},
        {"姓名": "李四", "成绩": 92},
        {"姓名": "王五", "成绩": 78},
        {"姓名": "赵六", "成绩": 95},
        {"姓名": "钱七", "成绩": 88}
    ]
    
    # 提取成绩
    scores = [s["成绩"] for s in students]
    
    # 统计分析
    print("\n成绩统计:")
    print(f"  学生人数: {registry.call('长度', students)}")
    print(f"  最高分: {registry.call('最大值', *scores)}")
    print(f"  最低分: {registry.call('最小值', *scores)}")
    print(f"  平均分: {registry.call('求和', scores) / registry.call('长度', scores):.2f}")
    
    # 排序
    sorted_scores = list(registry.call('排序', scores, reverse=True))
    print(f"  成绩排名: {sorted_scores}")
    
    # 成绩等级判断
    print("\n成绩等级:")
    for student in students:
        score = student["成绩"]
        if score >= 90:
            grade = "优秀"
        elif score >= 80:
            grade = "良好"
        elif score >= 70:
            grade = "中等"
        elif score >= 60:
            grade = "及格"
        else:
            grade = "不及格"
        print(f"  {student['姓名']}: {score}分 - {grade}")


def example_data_processing():
    """数据处理示例"""
    print("\n" + "=" * 60)
    print("示例4: 数据处理 - 文本分析")
    print("=" * 60)
    
    registry = BuiltinRegistry()
    registry.register_all_builtins()
    
    # 文本数据
    text = "心语语言是一门优雅的中文编程语言"
    
    print("\n文本分析:")
    print(f"  原文: {text}")
    print(f"  字符数: {registry.call('长度', text)}")
    
    # 转换为字符列表
    chars = registry.call('转列表', text)
    print(f"  字符列表: {chars[:10]}...")  # 只显示前10个
    
    # 统计字符频率
    from collections import Counter
    char_freq = Counter(chars)
    print(f"  最常见字符: {char_freq.most_common(3)}")
    
    # 数值处理
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print("\n数值处理:")
    print(f"  数列: {numbers}")
    print(f"  总和: {registry.call('求和', numbers)}")
    print(f"  平均值: {registry.call('求和', numbers) / registry.call('长度', numbers)}")
    
    # 筛选偶数
    evens = [x for x in numbers if x % 2 == 0]
    print(f"  偶数: {evens}")
    print(f"  偶数和: {registry.call('求和', evens)}")


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("心语语言 - 中文编程示例")
    print("=" * 60)
    
    example_basic_functions()
    example_module_usage()
    example_practical_application()
    example_data_processing()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
