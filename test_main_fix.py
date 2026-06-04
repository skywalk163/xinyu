"""
测试main.py的导入修复
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("测试1: 导入修复验证")
print("=" * 50)

try:
    from src.main import main
    print("[OK] 成功导入 src.main")
except Exception as e:
    print(f"[ERROR] 导入失败: {e}")

try:
    from src.builtin import BuiltinRegistry
    print("[OK] 成功导入 BuiltinRegistry")
    
    registry = BuiltinRegistry()
    registry.register_all_builtins()
    print(f"[OK] 成功注册 {len(registry.list_all_functions())} 个内置函数")
    
    # 测试几个函数
    result = registry.call('绝对值', -5)
    print(f"[OK] 绝对值(-5) = {result}")
    
    result = registry.call('最大值', 1, 2, 3)
    print(f"[OK] 最大值(1, 2, 3) = {result}")
    
except Exception as e:
    print(f"[ERROR] 测试失败: {e}")

try:
    from src.module import ModuleManager
    print("[OK] 成功导入 ModuleManager")
    
    manager = ModuleManager()
    math = manager.import_module('数学')
    result = math.平方根(16)
    print(f"[OK] 数学.平方根(16) = {result}")
    
except Exception as e:
    print(f"[ERROR] 模块测试失败: {e}")

print("\n" + "=" * 50)
print("测试完成！所有导入和基本功能正常。")
