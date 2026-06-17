# -*- coding: utf-8 -*-
"""虚拟机模块

提供字节码虚拟机实现。
"""

from src.vm.virtual_machine import Instruction, OpCode, VirtualMachine, compile_expression

__all__ = [
    "OpCode",
    "Instruction",
    "VirtualMachine",
    "compile_expression",
]
