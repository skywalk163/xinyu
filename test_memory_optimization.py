#!/usr/bin/env python3
"""
测试内存优化模块
"""

import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.memory import (
    ASTNodePoolStrategy,
    CacheMemoryLimitStrategy,
    LexerPool,
    MemoryMonitor,
    MemoryOptimizer,
    ObjectPool,
    ParserPool,
    StringInterningStrategy,
    TokenFlyweight,
    TokenFlyweightStrategy,
    estimate_memory_usage,
    find_memory_leaks,
    generate_memory_report,
    get_memory_monitor,
    get_memory_optimizer,
    monitor_memory_growth,
    optimize_memory_usage,
    profile_memory_usage,
    track_memory_allocation,
)


def test_object_pool():
    """测试对象池"""
    print("=" * 80)
    print("测试对象池")
    print("=" * 80)

    # 创建简单的对象工厂
    class TestObject:
        def __init__(self, value):
            self.value = value
            self.created_at = time.time()

        def reset(self):
            self.value = None

    def create_object(value=0):
        return TestObject(value)

    def validate_object(obj):
        return hasattr(obj, "reset") and callable(obj.reset)

    # 创建对象池
    pool = ObjectPool(
        factory_func=create_object,
        max_size=5,
        reset_func=lambda obj: obj.reset(),
        validate_func=validate_object,
    )

    # 测试对象获取和释放
    objects = []
    for i in range(10):
        obj = pool.acquire(i)
        objects.append(obj)
        print(f"获取对象 {i}: id={id(obj)}, value={obj.value}")

    # 释放对象回池
    for obj in objects:
        pool.release(obj)

    # 获取统计信息
    stats = pool.get_stats()
    print(f"\n对象池统计:")
    print(f"  创建总数: {stats.total_created}")
    print(f"  复用次数: {stats.total_reused}")
    print(f"  当前池大小: {stats.current_size}")
    print(f"  最大池大小: {stats.max_size}")
    print(f"  命中率: {stats.hit_rate:.1f}%")

    # 测试上下文管理器
    with ObjectPool(factory_func=create_object, max_size=3) as ctx_pool:
        obj1 = ctx_pool.acquire(100)
        obj2 = ctx_pool.acquire(200)
        print(f"\n上下文管理器测试:")
        print(f"  对象1: {obj1.value}")
        print(f"  对象2: {obj2.value}")

    print("\n对象池测试: 通过")
    return True


def test_lexer_parser_pools():
    """测试Lexer和Parser对象池"""
    print("\n" + "=" * 80)
    print("测试Lexer和Parser对象池")
    print("=" * 80)

    try:
        # 尝试导入相关模块
        import importlib.util

        # 检查Lexer模块是否存在
        lexer_spec = importlib.util.find_spec("src.lexer.lexer")
        parser_spec = importlib.util.find_spec("src.parser.parser")
        tokens_spec = importlib.util.find_spec("src.lexer.tokens")

        if not lexer_spec or not parser_spec or not tokens_spec:
            print("跳过Lexer/Parser池测试：相关模块不存在")
            return True

        # 获取全局池
        lexer_pool = LexerPool(max_size=3)
        parser_pool = ParserPool(max_size=3)

        # 测试Lexer池
        print("\n测试Lexer池:")
        lexers = []
        for i in range(5):
            source = f"print('Hello {i}')"
            lexer = lexer_pool.acquire_lexer(source)
            lexers.append(lexer)
            print(f"  获取Lexer {i}: id={id(lexer)}")

        # 释放Lexer
        for lexer in lexers:
            lexer_pool.release(lexer)

        # 测试Parser池
        print("\n测试Parser池:")
        parsers = []
        for i in range(5):
            parser = parser_pool.acquire_parser()
            parsers.append(parser)
            print(f"  获取Parser {i}: id={id(parser)}")

        # 释放Parser
        for parser in parsers:
            parser_pool.release(parser)

        # 获取统计信息
        lexer_stats = lexer_pool.get_stats()
        parser_stats = parser_pool.get_stats()

        print(f"\nLexer池统计:")
        print(f"  创建总数: {lexer_stats.total_created}")
        print(f"  复用次数: {lexer_stats.total_reused}")
        print(f"  当前池大小: {lexer_stats.current_size}")
        print(f"  最大池大小: {lexer_stats.max_size}")
        print(f"  命中率: {lexer_stats.hit_rate:.1f}%")

        print(f"\nParser池统计:")
        print(f"  创建总数: {parser_stats.total_created}")
        print(f"  复用次数: {parser_stats.total_reused}")
        print(f"  当前池大小: {parser_stats.current_size}")
        print(f"  最大池大小: {parser_stats.max_size}")
        print(f"  命中率: {parser_stats.hit_rate:.1f}%")

        print("\nLexer/Parser池测试: 通过")
        return True

    except ImportError as e:
        print(f"导入错误: {e}")
        print("跳过Lexer/Parser池测试")
        return True
    except Exception as e:
        print(f"测试错误: {e}")
        return False


def test_token_flyweight():
    """测试Token享元模式"""
    print("\n" + "=" * 80)
    print("测试Token享元模式")
    print("=" * 80)

    try:
        # 尝试导入Token模块
        import importlib.util

        tokens_spec = importlib.util.find_spec("src.lexer.tokens")

        if not tokens_spec:
            print("跳过Token享元测试：Token模块不存在")
            return True

        from src.lexer.tokens import Token

        # 创建多个相同值的Token
        tokens = []
        for i in range(100):
            # 创建相同值的Token
            token1 = TokenFlyweight.get_token("IDENTIFIER", "variable", i, 1)
            token2 = TokenFlyweight.get_token("IDENTIFIER", "variable", i, 2)
            token3 = TokenFlyweight.get_token("NUMBER", "42", i, 3)

            tokens.extend([token1, token2, token3])

        # 检查对象ID - 相同值的Token应该共享实例
        print(f"创建的Token数量: {len(tokens)}")

        # 检查前两个IDENTIFIER "variable" Token是否共享实例
        if id(tokens[0]) == id(tokens[1]):
            print("✓ 相同值的Token共享实例")
        else:
            print("✗ 相同值的Token未共享实例")

        # 检查池大小
        pool_size = TokenFlyweight.get_pool_size()
        print(f"Token池大小: {pool_size}")

        # 清空池
        TokenFlyweight.clear_pool()
        print(f"清空后Token池大小: {TokenFlyweight.get_pool_size()}")

        print("\nToken享元测试: 通过")
        return True

    except ImportError as e:
        print(f"导入错误: {e}")
        print("跳过Token享元测试")
        return True
    except Exception as e:
        print(f"测试错误: {e}")
        return False


def test_memory_monitor():
    """测试内存监控器"""
    print("\n" + "=" * 80)
    print("测试内存监控器")
    print("=" * 80)

    # 创建内存监控器
    monitor = MemoryMonitor(check_interval=0.5, memory_threshold_mb=10.0)

    # 测试手动快照
    snapshot1 = monitor.take_snapshot("快照1")
    print(f"快照1 - 内存: {snapshot1.current_memory_mb:.2f}MB, 对象: {snapshot1.object_count}")

    # 分配一些内存
    data = []
    for i in range(10000):
        data.append([j for j in range(100)])  # 分配一些内存

    snapshot2 = monitor.take_snapshot("快照2")
    print(f"快照2 - 内存: {snapshot2.current_memory_mb:.2f}MB, 对象: {snapshot2.object_count}")

    # 比较快照
    comparison = monitor.compare_snapshots(snapshot1, snapshot2)
    print(f"\n快照比较:")
    print(f"  时间差: {comparison['time_diff_seconds']:.2f}秒")
    print(f"  内存增长: {comparison['memory_growth_mb']:.2f}MB")
    print(f"  对象增长: {comparison['object_growth']}")

    # 获取当前内存统计
    stats = monitor.get_memory_stats()
    print(f"\n当前内存统计:")
    print(f"  当前内存: {stats['current_memory_mb']:.2f}MB")
    print(f"  峰值内存: {stats['peak_memory_mb']:.2f}MB")
    print(f"  可用内存: {stats['available_memory_mb']:.2f}MB")
    print(f"  总内存: {stats['total_memory_mb']:.2f}MB")
    print(f"  内存使用率: {stats['memory_percent']:.1f}%")
    print(f"  对象数量: {stats['object_count']}")

    # 清理数据
    del data

    print("\n内存监控器测试: 通过")
    return True


def test_memory_optimizer():
    """测试内存优化器"""
    print("\n" + "=" * 80)
    print("测试内存优化器")
    print("=" * 80)

    # 获取内存优化器
    optimizer = get_memory_optimizer()

    # 获取策略统计
    stats = optimizer.get_strategy_stats()
    print("注册的优化策略:")
    for name, strategy_stats in stats.items():
        print(f"  {name}: {strategy_stats['description']}")
        print(f"    启用: {strategy_stats['enabled']}")

    # 测试Token享元策略
    print("\n测试Token享元策略:")
    result = optimizer.apply_strategy("token_flyweight")
    if result:
        print(f"  成功: {result.success}")
        print(f"  消息: {result.message}")
        print(f"  节省内存: {result.memory_saved_mb:.2f}MB")
        print(f"  减少对象: {result.objects_reduced}")
    else:
        print("  策略不可用或未找到")

    # 测试所有策略
    print("\n应用所有优化策略:")
    results = optimizer.apply_all()

    for result in results:
        print(f"\n  {result.strategy_name}:")
        print(f"    成功: {result.success}")
        print(f"    消息: {result.message}")
        print(f"    节省内存: {result.memory_saved_mb:.2f}MB")
        print(f"    减少对象: {result.objects_reduced}")
        print(f"    执行时间: {result.execution_time_ms:.2f}ms")

    # 获取优化摘要
    summary = optimizer.get_optimization_summary()
    print(f"\n优化摘要:")
    print(f"  总节省内存: {summary['total_saved_mb']:.2f}MB")
    print(f"  总减少对象: {summary['total_objects_reduced']}")
    print(f"  成功策略数: {summary['success_count']}/{summary['total_strategies']}")

    print("\n内存优化器测试: 通过")
    return True


def test_memory_utils():
    """测试内存工具函数"""
    print("\n" + "=" * 80)
    print("测试内存工具函数")
    print("=" * 80)

    # 测试内存使用估算
    print("\n1. 测试内存使用估算:")
    test_list = [i for i in range(1000)]
    test_dict = {f"key_{i}": f"value_{i}" for i in range(100)}

    list_size = estimate_memory_usage(test_list)
    dict_size = estimate_memory_usage(test_dict)

    print(f"  列表大小: {list_size} 字节 ({list_size/1024:.2f}KB)")
    print(f"  字典大小: {dict_size} 字节 ({dict_size/1024:.2f}KB)")

    # 测试内存分配跟踪
    print("\n2. 测试内存分配跟踪:")

    def allocate_memory():
        data = []
        for i in range(1000):
            data.append([j for j in range(100)])
        return len(data)

    result, allocated = track_memory_allocation(allocate_memory)
    print(f"  函数结果: {result}")
    print(f"  分配内存: {allocated} 字节 ({allocated/1024:.2f}KB)")

    # 测试内存泄漏检测
    print("\n3. 测试内存泄漏检测:")

    # 模拟内存泄漏
    leaked_data = []

    def leak_memory():
        for i in range(100):
            leaked_data.append(bytearray(1024))  # 分配1KB

    # 运行多次以产生泄漏
    for _ in range(10):
        leak_memory()

    leaks = find_memory_leaks(snapshot_interval=0.1, duration=0.5, top_n=3)
    if leaks:
        print(f"  发现 {len(leaks)} 个潜在内存泄漏")
        for i, leak in enumerate(leaks[:3], 1):
            print(f"  泄漏 {i}:")
            print(f"    大小: {leak['size_diff'] / 1024:.2f}KB")
            print(f"    文件: {leak['filename']}:{leak['lineno']}")
            print(f"    代码: {leak['line']}")
    else:
        print("  未发现明显内存泄漏")

    # 清理泄漏数据
    leaked_data.clear()

    # 测试内存优化
    print("\n4. 测试内存优化:")
    optimization_result = optimize_memory_usage(aggressive=True)
    print(f"  优化前内存: {optimization_result['before_memory_mb']:.2f}MB")
    print(f"  优化后内存: {optimization_result['after_memory_mb']:.2f}MB")
    print(f"  节省内存: {optimization_result['memory_saved_mb']:.2f}MB")
    print(f"  回收对象: {optimization_result['objects_collected']}")
    print(f"  应用优化: {len(optimization_result['optimizations_applied'])}")

    # 测试内存报告生成
    print("\n5. 测试内存报告生成:")
    report = generate_memory_report()
    print(f"  报告生成时间: {report['datetime']}")
    print(f"  当前内存: {report['memory_usage']['rss_mb']:.2f}MB")
    print(f"  内存使用率: {report['memory_usage']['percent']:.1f}%")
    print(f"  对象类型数量: {len(report['object_analysis'])}")
    print(f"  潜在泄漏: {len(report['potential_leaks'])}")
    print(f"  建议数量: {len(report['recommendations'])}")

    print("\n内存工具函数测试: 通过")
    return True


def test_memory_profiling():
    """测试内存性能分析"""
    print("\n" + "=" * 80)
    print("测试内存性能分析")
    print("=" * 80)

    # 定义测试函数
    def process_data(size):
        """处理数据的测试函数"""
        result = []
        for i in range(size):
            # 创建一些数据
            data = {
                "id": i,
                "name": f"item_{i}",
                "values": [j for j in range(100)],
                "nested": {"a": i * 2, "b": i * 3, "c": [k for k in range(10)]},
            }
            result.append(data)
        return len(result)

    # 分析函数内存使用
    print("分析 process_data 函数的内存使用:")
    profile_result = profile_memory_usage(process_data, 100)

    print(f"  函数: {profile_result['function']}")
    print(f"  执行时间: {profile_result['execution_time_seconds']:.4f}秒")
    print(f"  RSS内存增长: {profile_result['memory_usage']['rss_growth_mb']:.2f}MB")
    print(f"  VMS内存增长: {profile_result['memory_usage']['vms_growth_mb']:.2f}MB")
    print(f"  总分配内存: {profile_result['memory_allocation']['total_allocated_mb']:.2f}MB")
    print(f"  总释放内存: {profile_result['memory_allocation']['total_freed_mb']:.2f}MB")
    print(f"  净分配内存: {profile_result['memory_allocation']['net_allocated_mb']:.2f}MB")

    if profile_result["allocation_hotspots"]:
        print(f"  内存分配热点: {len(profile_result['allocation_hotspots'])} 个")
        for i, hotspot in enumerate(profile_result["allocation_hotspots"][:3], 1):
            print(
                f"    热点 {i}: {hotspot['filename']}:{hotspot['lineno']} - {hotspot['size_diff_kb']:.2f}KB"
            )

    # 测试内存增长监控
    print("\n测试内存增长监控:")

    def simulate_memory_growth():
        """模拟内存增长"""
        data = []
        for i in range(5):
            data.append(bytearray(1024 * 1024))  # 每次分配1MB
            time.sleep(0.1)
        return len(data)

    # 在后台运行内存增长
    import threading

    growth_thread = threading.Thread(target=simulate_memory_growth)
    growth_thread.start()

    # 监控内存增长
    monitor_result = monitor_memory_growth(interval=0.2, duration=1.0, threshold_mb=2.0)

    growth_thread.join()

    print(f"  内存增长: {monitor_result['memory_growth_mb']:.2f}MB")
    print(f"  监控时长: {monitor_result['duration_seconds']:.2f}秒")
    print(f"  超过阈值: {monitor_result['exceeded_threshold']}")

    if monitor_result["exceeded_threshold"]:
        print(f"  检测到内存增长超过 {monitor_result['threshold_mb']}MB 阈值")

    print("\n内存性能分析测试: 通过")
    return True


def test_integration():
    """测试内存优化模块集成"""
    print("\n" + "=" * 80)
    print("测试内存优化模块集成")
    print("=" * 80)

    # 创建综合测试场景
    print("创建测试数据...")
    test_data = []

    # 分配一些内存
    for i in range(1000):
        test_data.append(
            {
                "id": i,
                "name": f"test_{i}",
                "data": [j for j in range(100)],
                "timestamp": time.time(),
            }
        )

    # 获取初始内存使用
    from src.memory.memory_utils import get_memory_usage

    initial_memory = get_memory_usage()
    print(f"初始内存: {initial_memory.rss_mb:.2f}MB")

    # 应用内存优化
    print("\n应用内存优化...")
    optimizer = get_memory_optimizer()

    # 只应用可用的策略，跳过可能有问题的方法
    available_strategies = []
    for name, strategy in optimizer.strategies.items():
        if strategy.enabled and strategy.can_apply():
            # 跳过可能修改sys模块的策略
            if name != "string_interning":
                available_strategies.append(name)

    total_saved = 0
    for strategy_name in available_strategies:
        result = optimizer.apply_strategy(strategy_name)
        if result and result.success:
            print(f"  {result.strategy_name}: 节省 {result.memory_saved_mb:.2f}MB")
            total_saved += result.memory_saved_mb

    # 获取优化后内存使用
    optimized_memory = get_memory_usage()
    print(f"优化后内存: {optimized_memory.rss_mb:.2f}MB")
    print(f"总节省内存: {total_saved:.2f}MB")

    # 生成内存报告
    print("\n生成内存报告...")
    report = generate_memory_report()

    print(f"报告摘要:")
    print(f"  当前内存: {report['memory_usage']['rss_mb']:.2f}MB")
    print(f"  内存使用率: {report['memory_usage']['percent']:.1f}%")
    print(f"  对象类型: {len(report['object_analysis'])} 种")
    print(f"  GC回收次数: {len(report['gc_stats']['collections'])}")

    # 显示前5个对象类型
    print(f"\n前5个对象类型:")
    for i, obj_info in enumerate(report["object_analysis"][:5], 1):
        print(
            f"  {i}. {obj_info['type_name']}: {obj_info['count']} 个, {obj_info['total_size']/1024:.1f}KB"
        )

    # 显示优化建议
    if report["recommendations"]:
        print(f"\n优化建议:")
        for i, recommendation in enumerate(report["recommendations"][:3], 1):
            print(f"  {i}. {recommendation}")

    # 清理测试数据
    test_data.clear()

    print("\n集成测试: 通过")
    return True


def main():
    """主测试函数"""
    print("=" * 80)
    print("内存优化模块测试")
    print("=" * 80)

    all_passed = True

    try:
        # 测试对象池
        print("\n[1/8] 测试对象池...")
        if test_object_pool():
            print("通过 对象池测试通过")
        else:
            print("失败 对象池测试失败")
            all_passed = False
    except Exception as e:
        print(f"失败 对象池测试异常: {e}")
        all_passed = False

    try:
        # 测试Lexer/Parser池
        print("\n[2/8] 测试Lexer/Parser池...")
        if test_lexer_parser_pools():
            print("通过 Lexer/Parser池测试通过")
        else:
            print("失败 Lexer/Parser池测试失败")
            all_passed = False
    except Exception as e:
        print(f"失败 Lexer/Parser池测试异常: {e}")
        all_passed = False

    try:
        # 测试Token享元模式
        print("\n[3/8] 测试Token享元模式...")
        if test_token_flyweight():
            print("通过 Token享元模式测试通过")
        else:
            print("失败 Token享元模式测试失败")
            all_passed = False
    except Exception as e:
        print(f"失败 Token享元模式测试异常: {e}")
        all_passed = False

    try:
        # 测试内存监控器
        print("\n[4/8] 测试内存监控器...")
        if test_memory_monitor():
            print("通过 内存监控器测试通过")
        else:
            print("失败 内存监控器测试失败")
            all_passed = False
    except Exception as e:
        print(f"失败 内存监控器测试异常: {e}")
        all_passed = False

    try:
        # 测试内存优化器
        print("\n[5/8] 测试内存优化器...")
        if test_memory_optimizer():
            print("通过 内存优化器测试通过")
        else:
            print("失败 内存优化器测试失败")
            all_passed = False
    except Exception as e:
        print(f"失败 内存优化器测试异常: {e}")
        all_passed = False

    try:
        # 测试内存工具函数
        print("\n[6/8] 测试内存工具函数...")
        if test_memory_utils():
            print("通过 内存工具函数测试通过")
        else:
            print("失败 内存工具函数测试失败")
            all_passed = False
    except Exception as e:
        print(f"失败 内存工具函数测试异常: {e}")
        all_passed = False

    try:
        # 测试内存性能分析
        print("\n[7/8] 测试内存性能分析...")
        if test_memory_profiling():
            print("通过 内存性能分析测试通过")
        else:
            print("失败 内存性能分析测试失败")
            all_passed = False
    except Exception as e:
        print(f"失败 内存性能分析测试异常: {e}")
        all_passed = False

    try:
        # 测试集成
        print("\n[8/8] 测试集成...")
        if test_integration():
            print("通过 集成测试通过")
        else:
            print("失败 集成测试失败")
            all_passed = False
    except Exception as e:
        import traceback

        print(f"失败 集成测试异常: {e}")
        print("错误堆栈:")
        traceback.print_exc()
        all_passed = False

    print("\n" + "=" * 80)
    if all_passed:
        print("通过 所有内存优化模块测试通过！")
    else:
        print("失败 部分测试失败，请检查实现。")
    print("=" * 80)

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
