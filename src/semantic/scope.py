# -*- coding: utf-8 -*-
"""作用域管理

管理变量和函数的作用域，支持嵌套作用域和符号查找。
"""

from typing import Any, Dict, Optional


class Scope:
    """作用域类
    
    管理符号表，支持嵌套作用域。
    
    属性：
        parent: 父作用域
        symbols: 符号表 {name: {type, value_type, ...}}
    """
    
    def __init__(self, parent: Optional['Scope'] = None):
        """初始化作用域
        
        Args:
            parent: 父作用域（可选）
        """
        self.parent = parent
        self.symbols: Dict[str, Dict[str, Any]] = {}
    
    def define(self, name: str, symbol_type: str, **attrs) -> None:
        """定义符号
        
        Args:
            name: 符号名称
            symbol_type: 符号类型（variable, function, parameter等）
            **attrs: 其他属性（value_type, params等）
        """
        self.symbols[name] = {
            "type": symbol_type,
            **attrs
        }
    
    def lookup(self, name: str) -> Optional[Dict[str, Any]]:
        """查找符号
        
        从当前作用域开始查找，如果未找到则向上查找父作用域。
        
        Args:
            name: 符号名称
            
        Returns:
            符号信息字典，如果未找到返回 None
        """
        if name in self.symbols:
            return self.symbols[name]
        
        if self.parent:
            return self.parent.lookup(name)
        
        return None
    
    def lookup_local(self, name: str) -> Optional[Dict[str, Any]]:
        """仅在当前作用域查找符号
        
        Args:
            name: 符号名称
            
        Returns:
            符号信息字典，如果未找到返回 None
        """
        return self.symbols.get(name)
    
    def assign(self, name: str, value_type: str) -> bool:
        """更新符号类型
        
        从当前作用域开始查找，如果未找到则向上查找父作用域。
        
        Args:
            name: 符号名称
            value_type: 新的类型
            
        Returns:
            是否更新成功
        """
        if name in self.symbols:
            self.symbols[name]["value_type"] = value_type
            return True
        
        if self.parent:
            return self.parent.assign(name, value_type)
        
        return False
    
    def __repr__(self) -> str:
        """返回作用域的字符串表示"""
        symbols_str = ", ".join(f"{k}: {v}" for k, v in self.symbols.items())
        return f"Scope({symbols_str})"
