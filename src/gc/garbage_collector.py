# -*- coding: utf-8 -*-
"""简单垃圾回收器

实现基于引用计数和标记-清除的垃圾回收。
"""

import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Set


@dataclass
class GCObject:
    """垃圾回收对象"""

    id: int  # 对象ID
    value: Any  # 对象值
    ref_count: int = 0  # 引用计数
    marked: bool = False  # 标记位（用于标记-清除）
    size: int = 0  # 对象大小（字节）


class SimpleGarbageCollector:
    """简单垃圾回收器

    实现两种GC算法：
    1. 引用计数（实时回收）
    2. 标记-清除（周期回收）
    """

    def __init__(self, threshold: int = 1000):
        """初始化垃圾回收器

        Args:
            threshold: GC触发阈值（对象数量）
        """
        self.objects: Dict[int, GCObject] = {}  # 对象池
        self.roots: Set[int] = set()  # 根集合
        self.next_id = 0  # 下一个对象ID
        self.threshold = threshold  # GC阈值
        self.gc_count = 0  # GC次数
        self.total_collected = 0  # 总回收对象数

        # 统计信息
        self.stats = {
            "ref_count_gc": 0,  # 引用计数GC次数
            "mark_sweep_gc": 0,  # 标记-清除GC次数
            "objects_created": 0,  # 创建对象数
            "objects_freed": 0,  # 释放对象数
        }

    def allocate(self, value: Any) -> int:
        """分配新对象

        Args:
            value: 对象值

        Returns:
            对象ID
        """
        # 检查是否需要GC
        if len(self.objects) >= self.threshold:
            self.collect()

        # 创建新对象
        obj_id = self.next_id
        self.next_id += 1

        # 计算对象大小
        size = self._estimate_size(value)

        # 创建GC对象
        gc_obj = GCObject(id=obj_id, value=value, ref_count=1, size=size)

        self.objects[obj_id] = gc_obj
        self.stats["objects_created"] += 1

        return obj_id

    def add_reference(self, obj_id: int):
        """添加引用

        Args:
            obj_id: 对象ID
        """
        if obj_id in self.objects:
            self.objects[obj_id].ref_count += 1

    def remove_reference(self, obj_id: int):
        """移除引用

        Args:
            obj_id: 对象ID
        """
        if obj_id in self.objects:
            self.objects[obj_id].ref_count -= 1

            # 引用计数为0，立即回收
            if self.objects[obj_id].ref_count <= 0:
                self._free_object(obj_id)
                self.stats["ref_count_gc"] += 1

    def add_root(self, obj_id: int):
        """添加根引用

        Args:
            obj_id: 对象ID
        """
        self.roots.add(obj_id)
        self.add_reference(obj_id)

    def remove_root(self, obj_id: int):
        """移除根引用

        Args:
            obj_id: 对象ID
        """
        self.roots.discard(obj_id)
        self.remove_reference(obj_id)

    def collect(self):
        """执行垃圾回收（标记-清除算法）"""
        start_time = time.time()

        # 标记阶段
        self._mark()

        # 清除阶段
        collected = self._sweep()

        self.gc_count += 1
        self.total_collected += collected
        self.stats["mark_sweep_gc"] += 1

        elapsed = time.time() - start_time
        print(f"GC: 回收了{collected}个对象，耗时{elapsed:.4f}秒")

    def _mark(self):
        """标记阶段：从根集合开始标记可达对象"""
        # 清除所有标记
        for obj in self.objects.values():
            obj.marked = False

        # 从根集合开始标记
        for root_id in self.roots:
            if root_id in self.objects:
                self._mark_object(root_id)

    def _mark_object(self, obj_id: int):
        """标记对象及其引用的对象

        Args:
            obj_id: 对象ID
        """
        if obj_id not in self.objects:
            return

        obj = self.objects[obj_id]

        # 已标记，跳过
        if obj.marked:
            return

        # 标记对象
        obj.marked = True

        # 递归标记引用的对象
        value = obj.value
        if isinstance(value, (list, tuple, set)):
            for item in value:
                if isinstance(item, int) and item in self.objects:
                    self._mark_object(item)
        elif isinstance(value, dict):
            for v in value.values():
                if isinstance(v, int) and v in self.objects:
                    self._mark_object(v)

    def _sweep(self) -> int:
        """清除阶段：回收未标记的对象

        Returns:
            回收的对象数量
        """
        to_free = []

        for obj_id, obj in self.objects.items():
            if not obj.marked:
                to_free.append(obj_id)

        for obj_id in to_free:
            self._free_object(obj_id)

        return len(to_free)

    def _free_object(self, obj_id: int):
        """释放对象

        Args:
            obj_id: 对象ID
        """
        if obj_id in self.objects:
            del self.objects[obj_id]
            self.stats["objects_freed"] += 1

    def _estimate_size(self, value: Any) -> int:
        """估算对象大小

        Args:
            value: 对象值

        Returns:
            估算大小（字节）
        """
        if isinstance(value, (int, float)):
            return 28  # Python int/float大约28字节
        elif isinstance(value, str):
            return len(value) * 2 + 50  # 字符串
        elif isinstance(value, (list, tuple)):
            return len(value) * 8 + 56  # 列表/元组
        elif isinstance(value, dict):
            return len(value) * 16 + 72  # 字典
        else:
            return 64  # 默认大小

    def get_stats(self) -> Dict[str, Any]:
        """获取GC统计信息

        Returns:
            统计信息字典
        """
        total_size = sum(obj.size for obj in self.objects.values())

        return {
            "objects_count": len(self.objects),
            "total_size": total_size,
            "gc_count": self.gc_count,
            "total_collected": self.total_collected,
            **self.stats,
        }

    def get_object(self, obj_id: int) -> Optional[Any]:
        """获取对象值

        Args:
            obj_id: 对象ID

        Returns:
            对象值，如果不存在则返回None
        """
        if obj_id in self.objects:
            return self.objects[obj_id].value
        return None


# 测试垃圾回收器
def test_gc():
    """测试垃圾回收器"""
    print("=== 测试垃圾回收器 ===")

    # 创建GC
    gc = SimpleGarbageCollector(threshold=10)

    # 分配对象
    obj1 = gc.allocate(42)
    obj2 = gc.allocate("hello")
    obj3 = gc.allocate([1, 2, 3])

    print(f"创建了3个对象: {obj1}, {obj2}, {obj3}")

    # 添加根引用
    gc.add_root(obj1)
    gc.add_root(obj2)

    print("添加了2个根引用")

    # 查看统计
    stats = gc.get_stats()
    print(f"统计: {stats}")

    # 移除根引用
    gc.remove_root(obj2)
    print("移除了obj2的根引用")

    # 手动触发GC
    gc.collect()

    # 查看最终统计
    stats = gc.get_stats()
    print(f"最终统计: {stats}")


if __name__ == "__main__":
    test_gc()
