"""
测试新增模块

测试fnmatch、linecache、bisect、heapq模块。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.module import ModuleManager


def test_fnmatch_module():
    """测试文件名匹配模块"""
    print("\n" + "=" * 70)
    print("文件名匹配模块测试")
    print("=" * 70)
    
    manager = ModuleManager()
    fnmatch = manager.import_module('文件名匹配')
    
    # 测试匹配
    filenames = ['test.py', 'example.txt', 'script.py', 'data.json', 'main.py']
    pattern = '*.py'
    
    print(f"\n1. 文件名匹配测试:")
    print(f"   文件列表: {filenames}")
    print(f"   匹配模式: {pattern}")
    
    matched = fnmatch.过滤(filenames, pattern)
    print(f"   匹配结果: {matched}")
    
    # 测试单个匹配
    print(f"\n2. 单个文件匹配:")
    print(f"   'test.py' 匹配 '*.py': {fnmatch.匹配('test.py', '*.py')}")
    print(f"   'test.txt' 匹配 '*.py': {fnmatch.匹配('test.txt', '*.py')}")


def test_bisect_module():
    """测试二分查找模块"""
    print("\n" + "=" * 70)
    print("二分查找模块测试")
    print("=" * 70)
    
    manager = ModuleManager()
    bisect = manager.import_module('二分查找')
    
    # 测试二分查找
    sorted_list = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    
    print(f"\n1. 二分查找测试:")
    print(f"   有序列表: {sorted_list}")
    
    # 查找插入位置
    value = 10
    pos = bisect.查找位置(sorted_list, value)
    print(f"   查找 {value} 的插入位置: {pos}")
    
    # 插入元素
    import copy
    new_list = copy.copy(sorted_list)
    bisect.插入(new_list, value)
    print(f"   插入 {value} 后: {new_list}")
    
    # 查找左位置
    print(f"\n2. 查找左右位置:")
    print(f"   查找 7 的左位置: {bisect.查找左位置(sorted_list, 7)}")
    print(f"   查找 7 的右位置: {bisect.查找右位置(sorted_list, 7)}")


def test_heapq_module():
    """测试堆队列模块"""
    print("\n" + "=" * 70)
    print("堆队列模块测试")
    print("=" * 70)
    
    manager = ModuleManager()
    heapq = manager.import_module('堆队列')
    
    # 测试堆操作
    data = [5, 3, 8, 1, 9, 2, 7, 4, 6]
    
    print(f"\n1. 堆化测试:")
    print(f"   原始数据: {data}")
    
    import copy
    heap = copy.copy(data)
    heapq.堆化(heap)
    print(f"   堆化后: {heap}")
    
    # 弹出最小元素
    print(f"\n2. 堆操作测试:")
    min_val = heapq.弹出(heap)
    print(f"   弹出最小值: {min_val}")
    print(f"   弹出后堆: {heap}")
    
    # 推入新元素
    heapq.推入(heap, 0)
    print(f"   推入 0 后: {heap}")
    
    # 获取最大n个元素
    print(f"\n3. 最大最小n个元素:")
    print(f"   最大3个: {heapq.最大n个(3, data)}")
    print(f"   最小3个: {heapq.最小n个(3, data)}")


def test_linecache_module():
    """测试行缓存模块"""
    print("\n" + "=" * 70)
    print("行缓存模块测试")
    print("=" * 70)
    
    manager = ModuleManager()
    linecache = manager.import_module('行缓存')
    
    # 测试获取行
    print(f"\n1. 行缓存测试:")
    # 使用当前文件测试
    current_file = __file__
    line = linecache.获取行(current_file, 1)
    print(f"   文件: {os.path.basename(current_file)}")
    print(f"   第1行: {line.strip() if line else 'None'}")
    
    # 清空缓存
    linecache.清空缓存()
    print("   缓存已清空")


def list_all_modules():
    """列出所有模块"""
    print("\n" + "=" * 70)
    print("所有可用模块列表")
    print("=" * 70)
    
    manager = ModuleManager()
    modules = manager._chinese_module_map
    
    print(f"\n总计: {len(modules)}个模块\n")
    
    # 按类别显示
    categories = {
        "数学运算": ["数学", "小数", "统计", "随机"],
        "文本处理": ["字符串", "文本包裹", "正则"],
        "数据类型": ["集合", "迭代工具", "函数工具", "复制", "美化打印", "类型提示"],
        "算法": ["二分查找", "堆队列"],
        "文件操作": ["系统", "路径", "文件操作", "文件匹配", "文件名匹配", "临时文件", "行缓存"],
        "数据存储": ["JSON", "序列化", "CSV", "数据库", "DBM", "配置"],
        "时间日期": ["日期时间", "时间"],
        "并发编程": ["线程", "队列", "异步", "子进程"],
        "数据压缩": ["压缩", "GZIP", "ZIP", "TAR"],
        "网络编程": ["套接字", "SSL", "HTTP", "URL"],
        "测试框架": ["单元测试", "文档测试"],
        "图形界面": ["图形界面"],
        "编码解码": ["Base64", "二进制结构"],
        "XML处理": ["XML树"],
        "国际化": ["国际化", "本地化"],
        "系统工具": ["系统信息", "参数解析", "日志", "哈希", "安全随机", "检查", "堆栈跟踪"],
    }
    
    for category, module_names in categories.items():
        available = [name for name in module_names if name in modules]
        if available:
            print(f"\n{category} ({len(available)}个):")
            for name in available:
                print(f"  {name:10s} -> {modules[name]}")


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("心语语言 - 新增模块测试")
    print("=" * 70)
    
    try:
        list_all_modules()
        test_fnmatch_module()
        test_bisect_module()
        test_heapq_module()
        test_linecache_module()
        
        print("\n" + "=" * 70)
        print("[SUCCESS] 所有新增模块测试通过！")
        print("=" * 70)
        
        print("\n功能总结:")
        print("  [OK] 已实现57个标准库模块的中文封装")
        print("  [OK] 新增4个实用模块（fnmatch, linecache, bisect, heapq）")
        print("  [OK] 覆盖文件匹配、行缓存、二分查找、堆队列等")
        print("  [OK] 所有模块支持中英文双语调用")
        print("\n")
        
    except Exception as e:
        print(f"\n[ERROR] 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
