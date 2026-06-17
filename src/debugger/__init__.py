"""
调试器模块
提供心语语言的调试功能
"""

from .interface import DebuggerBase, IDebugger
from .manager import DebuggerManager
from .pdb_debugger import PdbDebugger

__all__ = ["IDebugger", "DebuggerBase", "PdbDebugger", "DebuggerManager"]


class Debugger:
    """调试器工厂类"""

    @staticmethod
    def create_pdb_debugger(compiler=None):
        """创建PDB调试器"""
        return PdbDebugger(compiler)

    @staticmethod
    def create_debugger_manager(compiler=None):
        """创建调试器管理器"""
        return DebuggerManager(compiler)
