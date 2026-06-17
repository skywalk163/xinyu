"""
调试器接口定义
定义调试器的标准接口
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Protocol


class IDebugger(Protocol):
    """调试器接口协议"""

    def set_breakpoint(self, filename: str, line: int, condition: Optional[str] = None) -> bool:
        """设置断点

        Args:
            filename: 文件名
            line: 行号
            condition: 可选的条件表达式

        Returns:
            是否成功设置断点
        """
        ...

    def clear_breakpoint(self, breakpoint_id: int) -> bool:
        """清除断点

        Args:
            breakpoint_id: 断点ID

        Returns:
            是否成功清除断点
        """
        ...

    def list_breakpoints(self) -> List[Dict[str, Any]]:
        """列出所有断点

        Returns:
            断点列表，每个断点是一个字典
        """
        ...

    def step_over(self) -> Dict[str, Any]:
        """单步执行（步过）

        Returns:
            执行结果信息
        """
        ...

    def step_into(self) -> Dict[str, Any]:
        """单步执行（步入）

        Returns:
            执行结果信息
        """
        ...

    def step_out(self) -> Dict[str, Any]:
        """单步执行（步出）

        Returns:
            执行结果信息
        """
        ...

    def continue_execution(self) -> Dict[str, Any]:
        """继续执行

        Returns:
            执行结果信息
        """
        ...

    def pause_execution(self) -> None:
        """暂停执行"""
        ...

    def get_variables(self, scope: str = "local") -> Dict[str, Any]:
        """获取变量

        Args:
            scope: 作用域（local/global）

        Returns:
            变量字典
        """
        ...

    def set_variable(self, name: str, value: Any) -> bool:
        """设置变量值

        Args:
            name: 变量名
            value: 变量值

        Returns:
            是否成功设置
        """
        ...

    def get_call_stack(self) -> List[Dict[str, Any]]:
        """获取调用栈

        Returns:
            调用栈信息列表
        """
        ...

    def evaluate(self, expression: str) -> Any:
        """计算表达式

        Args:
            expression: 表达式字符串

        Returns:
            表达式计算结果
        """
        ...


class DebuggerBase(ABC):
    """调试器基类"""

    def __init__(self):
        self.breakpoints: Dict[int, Dict[str, Any]] = {}
        self.next_breakpoint_id = 1
        self.is_running = False
        self.is_paused = False
        self.current_frame = None

    @abstractmethod
    def set_breakpoint(self, filename: str, line: int, condition: Optional[str] = None) -> bool:
        """设置断点"""
        pass

    @abstractmethod
    def clear_breakpoint(self, breakpoint_id: int) -> bool:
        """清除断点"""
        pass

    def list_breakpoints(self) -> List[Dict[str, Any]]:
        """列出所有断点"""
        return list(self.breakpoints.values())

    @abstractmethod
    def step_over(self) -> Dict[str, Any]:
        """单步执行（步过）"""
        pass

    @abstractmethod
    def step_into(self) -> Dict[str, Any]:
        """单步执行（步入）"""
        pass

    @abstractmethod
    def step_out(self) -> Dict[str, Any]:
        """单步执行（步出）"""
        pass

    @abstractmethod
    def continue_execution(self) -> Dict[str, Any]:
        """继续执行"""
        pass

    def pause_execution(self) -> None:
        """暂停执行"""
        self.is_paused = True

    @abstractmethod
    def get_variables(self, scope: str = "local") -> Dict[str, Any]:
        """获取变量"""
        pass

    @abstractmethod
    def set_variable(self, name: str, value: Any) -> bool:
        """设置变量值"""
        pass

    @abstractmethod
    def get_call_stack(self) -> List[Dict[str, Any]]:
        """获取调用栈"""
        pass

    @abstractmethod
    def evaluate(self, expression: str) -> Any:
        """计算表达式"""
        pass

    def _generate_breakpoint_id(self) -> int:
        """生成断点ID"""
        bid = self.next_breakpoint_id
        self.next_breakpoint_id += 1
        return bid

    def _format_breakpoint_info(
        self, breakpoint_id: int, filename: str, line: int, condition: Optional[str] = None
    ) -> Dict[str, Any]:
        """格式化断点信息"""
        return {
            "id": breakpoint_id,
            "filename": filename,
            "line": line,
            "condition": condition,
            "enabled": True,
        }
