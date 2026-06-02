"""
基础模块封装类

提供模块中文接口封装的基础功能。
"""

from typing import Any, Dict


class ChineseModuleWrapper:
    """中文模块封装基类"""
    
    def __init__(self, module: Any, name_map: Dict[str, str]):
        """
        初始化模块封装
        
        Args:
            module: 原始Python模块
            name_map: 中文名到英文名的映射字典
        """
        self._module = module
        self._name_map = name_map
    
    def __getattr__(self, name: str) -> Any:
        """获取模块属性（支持中文）"""
        # 如果是中文名，转换为英文名
        if name in self._name_map:
            english_name = self._name_map[name]
            return getattr(self._module, english_name)
        
        # 否则直接访问
        return getattr(self._module, name)
