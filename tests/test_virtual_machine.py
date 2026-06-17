#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""虚拟机测试"""

import pytest

from src.vm.virtual_machine import Instruction, OpCode, VirtualMachine


class TestVirtualMachine:
    """虚拟机测试类"""

    def test_vm_initialization(self):
        """测试虚拟机初始化"""
        vm = VirtualMachine()
        assert vm.stack == []
        assert vm.globals == {}
        assert vm.locals_stack == [{}]
        assert vm.call_stack == []
        assert vm.pc == 0
        assert vm.instructions == []
        assert vm.debug is False
        assert vm.running is False

    def test_vm_initialization_with_debug(self):
        """测试带调试模式的虚拟机初始化"""
        vm = VirtualMachine(debug=True)
        assert vm.debug is True

    def test_load_instructions(self):
        """测试加载指令"""
        vm = VirtualMachine()
        instructions = [
            Instruction(OpCode.PUSH, 42),
            Instruction(OpCode.PUSH, 10),
            Instruction(OpCode.ADD),
            Instruction(OpCode.HALT),
        ]

        vm.load(instructions)
        assert vm.instructions == instructions
        assert vm.pc == 0
        assert vm.stack == []

    def test_execute_push(self):
        """测试PUSH指令"""
        vm = VirtualMachine()
        vm.load([Instruction(OpCode.PUSH, 42)])
        vm.run()

        assert vm.stack == [42]
        assert vm.pc == 1

    def test_execute_pop(self):
        """测试POP指令"""
        vm = VirtualMachine()
        vm.load(
            [
                Instruction(OpCode.PUSH, 42),
                Instruction(OpCode.PUSH, 10),
                Instruction(OpCode.POP),
                Instruction(OpCode.HALT),
            ]
        )
        vm.run()

        assert vm.stack == [42]  # 10被弹出
        assert vm.pc == 4

    def test_execute_dup(self):
        """测试DUP指令"""
        vm = VirtualMachine()
        vm.load([Instruction(OpCode.PUSH, 42), Instruction(OpCode.DUP), Instruction(OpCode.HALT)])
        vm.run()

        assert vm.stack == [42, 42]  # 复制栈顶
        assert vm.pc == 3

    def test_execute_add(self):
        """测试ADD指令"""
        vm = VirtualMachine()
        vm.load(
            [
                Instruction(OpCode.PUSH, 20),
                Instruction(OpCode.PUSH, 22),
                Instruction(OpCode.ADD),
                Instruction(OpCode.HALT),
            ]
        )
        vm.run()

        assert vm.stack == [42]  # 20 + 22 = 42
        assert vm.pc == 4

    def test_execute_sub(self):
        """测试SUB指令"""
        vm = VirtualMachine()
        vm.load(
            [
                Instruction(OpCode.PUSH, 50),
                Instruction(OpCode.PUSH, 8),
                Instruction(OpCode.SUB),
                Instruction(OpCode.HALT),
            ]
        )
        vm.run()

        assert vm.stack == [42]  # 50 - 8 = 42
        assert vm.pc == 4

    def test_execute_mul(self):
        """测试MUL指令"""
        vm = VirtualMachine()
        vm.load(
            [
                Instruction(OpCode.PUSH, 6),
                Instruction(OpCode.PUSH, 7),
                Instruction(OpCode.MUL),
                Instruction(OpCode.HALT),
            ]
        )
        vm.run()

        assert vm.stack == [42]  # 6 * 7 = 42
        assert vm.pc == 4

    def test_execute_div(self):
        """测试DIV指令"""
        vm = VirtualMachine()
        vm.load(
            [
                Instruction(OpCode.PUSH, 84),
                Instruction(OpCode.PUSH, 2),
                Instruction(OpCode.DIV),
                Instruction(OpCode.HALT),
            ]
        )
        vm.run()

        assert vm.stack == [42]  # 84 / 2 = 42
        assert vm.pc == 4

    def test_execute_mod(self):
        """测试MOD指令"""
        vm = VirtualMachine()
        vm.load(
            [
                Instruction(OpCode.PUSH, 47),
                Instruction(OpCode.PUSH, 5),
                Instruction(OpCode.MOD),
                Instruction(OpCode.HALT),
            ]
        )
        vm.run()

        assert vm.stack == [2]  # 47 % 5 = 2
        assert vm.pc == 4

    def test_execute_neg(self):
        """测试NEG指令"""
        vm = VirtualMachine()
        vm.load([Instruction(OpCode.PUSH, 42), Instruction(OpCode.NEG), Instruction(OpCode.HALT)])
        vm.run()

        assert vm.stack == [-42]  # 取负
        assert vm.pc == 3

    def test_execute_eq(self):
        """测试EQ指令"""
        vm = VirtualMachine()
        vm.load(
            [
                Instruction(OpCode.PUSH, 42),
                Instruction(OpCode.PUSH, 42),
                Instruction(OpCode.EQ),
                Instruction(OpCode.HALT),
            ]
        )
        vm.run()

        assert vm.stack == [True]  # 42 == 42
        assert vm.pc == 4

    def test_execute_ne(self):
        """测试NE指令"""
        vm = VirtualMachine()
        vm.load(
            [
                Instruction(OpCode.PUSH, 42),
                Instruction(OpCode.PUSH, 10),
                Instruction(OpCode.NE),
                Instruction(OpCode.HALT),
            ]
        )
        vm.run()

        assert vm.stack == [True]  # 42 != 10
        assert vm.pc == 4

    def test_execute_lt(self):
        """测试LT指令"""
        vm = VirtualMachine()
        vm.load(
            [
                Instruction(OpCode.PUSH, 10),
                Instruction(OpCode.PUSH, 42),
                Instruction(OpCode.LT),
                Instruction(OpCode.HALT),
            ]
        )
        vm.run()

        assert vm.stack == [True]  # 10 < 42
        assert vm.pc == 4

    def test_execute_le(self):
        """测试LE指令"""
        vm = VirtualMachine()
        vm.load(
            [
                Instruction(OpCode.PUSH, 42),
                Instruction(OpCode.PUSH, 42),
                Instruction(OpCode.LE),
                Instruction(OpCode.HALT),
            ]
        )
        vm.run()

        assert vm.stack == [True]  # 42 <= 42
        assert vm.pc == 4

    def test_execute_gt(self):
        """测试GT指令"""
        vm = VirtualMachine()
        vm.load(
            [
                Instruction(OpCode.PUSH, 42),
                Instruction(OpCode.PUSH, 10),
                Instruction(OpCode.GT),
                Instruction(OpCode.HALT),
            ]
        )
        vm.run()

        assert vm.stack == [True]  # 42 > 10
        assert vm.pc == 4

    def test_execute_ge(self):
        """测试GE指令"""
        vm = VirtualMachine()
        vm.load(
            [
                Instruction(OpCode.PUSH, 42),
                Instruction(OpCode.PUSH, 42),
                Instruction(OpCode.GE),
                Instruction(OpCode.HALT),
            ]
        )
        vm.run()

        assert vm.stack == [True]  # 42 >= 42
        assert vm.pc == 4

    def test_execute_and(self):
        """测试AND指令"""
        vm = VirtualMachine()
        vm.load(
            [
                Instruction(OpCode.PUSH, True),
                Instruction(OpCode.PUSH, True),
                Instruction(OpCode.AND),
                Instruction(OpCode.HALT),
            ]
        )
        vm.run()

        assert vm.stack == [True]  # True AND True
        assert vm.pc == 4

    def test_execute_or(self):
        """测试OR指令"""
        vm = VirtualMachine()
        vm.load(
            [
                Instruction(OpCode.PUSH, True),
                Instruction(OpCode.PUSH, False),
                Instruction(OpCode.OR),
                Instruction(OpCode.HALT),
            ]
        )
        vm.run()

        assert vm.stack == [True]  # True OR False
        assert vm.pc == 4

    def test_execute_not(self):
        """测试NOT指令"""
        vm = VirtualMachine()
        vm.load(
            [Instruction(OpCode.PUSH, False), Instruction(OpCode.NOT), Instruction(OpCode.HALT)]
        )
        vm.run()

        assert vm.stack == [True]  # NOT False
        assert vm.pc == 3

    def test_execute_load_store(self):
        """测试LOAD和STORE指令"""
        vm = VirtualMachine()
        vm.load(
            [
                Instruction(OpCode.PUSH, 42),
                Instruction(OpCode.STORE, "x"),
                Instruction(OpCode.LOAD, "x"),
                Instruction(OpCode.HALT),
            ]
        )
        vm.run()

        assert vm.stack == [42]  # 存储后加载
        assert vm.globals == {"x": 42}
        assert vm.pc == 4

    def test_execute_jump(self):
        """测试JUMP指令"""
        vm = VirtualMachine()
        vm.load(
            [
                Instruction(OpCode.PUSH, 1),
                Instruction(OpCode.JUMP, 4),  # 跳转到HALT
                Instruction(OpCode.PUSH, 2),  # 应该跳过
                Instruction(OpCode.PUSH, 3),  # 应该跳过
                Instruction(OpCode.HALT),
            ]
        )
        vm.run()

        assert vm.stack == [1]  # 只执行了PUSH 1
        assert vm.pc == 5

    def test_execute_jump_if_true(self):
        """测试JUMP_IF_TRUE指令"""
        vm = VirtualMachine()
        vm.load(
            [
                Instruction(OpCode.PUSH, True),
                Instruction(OpCode.JUMP_IF_TRUE, 4),  # 条件为真，跳转
                Instruction(OpCode.PUSH, 2),  # 应该跳过
                Instruction(OpCode.PUSH, 3),  # 应该跳过
                Instruction(OpCode.PUSH, 42),
                Instruction(OpCode.HALT),
            ]
        )
        vm.run()

        assert vm.stack == [True, 42]  # 跳过了2和3
        assert vm.pc == 6

    def test_execute_jump_if_false(self):
        """测试JUMP_IF_FALSE指令"""
        vm = VirtualMachine()
        vm.load(
            [
                Instruction(OpCode.PUSH, False),
                Instruction(OpCode.JUMP_IF_FALSE, 4),  # 条件为假，跳转
                Instruction(OpCode.PUSH, 2),  # 应该跳过
                Instruction(OpCode.PUSH, 3),  # 应该跳过
                Instruction(OpCode.PUSH, 42),
                Instruction(OpCode.HALT),
            ]
        )
        vm.run()

        assert vm.stack == [False, 42]  # 跳过了2和3
        assert vm.pc == 6

    def test_execute_call_return(self):
        """测试CALL和RETURN指令"""
        vm = VirtualMachine()
        vm.load(
            [
                Instruction(OpCode.PUSH, 10),  # 参数
                Instruction(OpCode.CALL, 4),  # 调用函数
                Instruction(OpCode.HALT),  # 主程序结束
                # 函数开始
                Instruction(OpCode.PUSH, 2),  # 函数体
                Instruction(OpCode.MUL),  # 10 * 2 = 20
                Instruction(OpCode.RETURN),  # 返回
            ]
        )
        vm.run()

        assert vm.stack == [20]  # 函数返回值
        assert vm.pc == 3  # 停在HALT指令

    def test_execute_print(self):
        """测试PRINT指令"""
        vm = VirtualMachine()
        vm.load(
            [
                Instruction(OpCode.PUSH, "Hello, World!"),
                Instruction(OpCode.PRINT),
                Instruction(OpCode.HALT),
            ]
        )
        vm.run()

        assert vm.stack == []  # 打印后栈为空
        assert vm.pc == 3

    def test_complex_expression(self):
        """测试复杂表达式"""
        vm = VirtualMachine()
        # 计算 (10 + 2) * 3 - 4
        vm.load(
            [
                Instruction(OpCode.PUSH, 10),
                Instruction(OpCode.PUSH, 2),
                Instruction(OpCode.ADD),  # 10 + 2 = 12
                Instruction(OpCode.PUSH, 3),
                Instruction(OpCode.MUL),  # 12 * 3 = 36
                Instruction(OpCode.PUSH, 4),
                Instruction(OpCode.SUB),  # 36 - 4 = 32
                Instruction(OpCode.HALT),
            ]
        )
        vm.run()

        assert vm.stack == [32]
        assert vm.pc == 8

    def test_variable_scope(self):
        """测试变量作用域"""
        vm = VirtualMachine()
        vm.load(
            [
                Instruction(OpCode.PUSH, 10),
                Instruction(OpCode.STORE, "x"),  # 全局变量 x = 10
                Instruction(OpCode.PUSH, 20),
                Instruction(OpCode.STORE, "y"),  # 全局变量 y = 20
                Instruction(OpCode.LOAD, "x"),
                Instruction(OpCode.LOAD, "y"),
                Instruction(OpCode.ADD),  # x + y = 30
                Instruction(OpCode.HALT),
            ]
        )
        vm.run()

        assert vm.stack == [30]
        assert vm.globals == {"x": 10, "y": 20}
        assert vm.pc == 8

    def test_conditional_execution(self):
        """测试条件执行"""
        vm = VirtualMachine()
        # if (5 > 3) then push 42 else push 0
        vm.load(
            [
                Instruction(OpCode.PUSH, 5),
                Instruction(OpCode.PUSH, 3),
                Instruction(OpCode.GT),  # 5 > 3 = True
                Instruction(OpCode.JUMP_IF_FALSE, 6),  # 如果为假跳转到else分支
                Instruction(OpCode.PUSH, 42),  # then分支
                Instruction(OpCode.JUMP, 7),  # 跳过else分支
                Instruction(OpCode.PUSH, 0),  # else分支
                Instruction(OpCode.HALT),
            ]
        )
        vm.run()

        assert vm.stack == [True, 42]  # 条件为真，执行then分支
        assert vm.pc == 8

    def test_function_with_parameters(self):
        """测试带参数的函数"""
        vm = VirtualMachine()
        # 函数: f(x, y) = x * y + 10
        vm.load(
            [
                # 主程序
                Instruction(OpCode.PUSH, 5),  # 第一个参数
                Instruction(OpCode.PUSH, 6),  # 第二个参数
                Instruction(OpCode.CALL, 5),  # 调用函数
                Instruction(OpCode.HALT),
                # 函数体
                Instruction(OpCode.MUL),  # x * y
                Instruction(OpCode.PUSH, 10),
                Instruction(OpCode.ADD),  # (x * y) + 10
                Instruction(OpCode.RETURN),
            ]
        )
        vm.run()

        # 5 * 6 + 10 = 40
        assert vm.stack == [40]
        assert vm.pc == 4

    def test_nested_function_calls(self):
        """测试嵌套函数调用"""
        vm = VirtualMachine()
        # 计算 add(mul(3, 4), 5)
        vm.load(
            [
                # 主程序
                Instruction(OpCode.PUSH, 3),
                Instruction(OpCode.PUSH, 4),
                Instruction(OpCode.CALL, 5),  # 调用mul函数
                Instruction(OpCode.PUSH, 5),
                Instruction(OpCode.CALL, 9),  # 调用add函数
                Instruction(OpCode.HALT),
                # mul函数
                Instruction(OpCode.MUL),  # 3 * 4 = 12
                Instruction(OpCode.RETURN),
                # add函数
                Instruction(OpCode.ADD),  # 12 + 5 = 17
                Instruction(OpCode.RETURN),
            ]
        )
        vm.run()

        assert vm.stack == [17]  # 3 * 4 + 5 = 17
        assert vm.pc == 6

    def test_error_handling_empty_stack(self):
        """测试空栈错误处理"""
        vm = VirtualMachine()
        vm.load([Instruction(OpCode.ADD), Instruction(OpCode.HALT)])  # 空栈执行ADD

        # 应该抛出IndexError
        with pytest.raises(IndexError):
            vm.run()

    def test_error_handling_division_by_zero(self):
        """测试除以零错误处理"""
        vm = VirtualMachine()
        vm.load(
            [
                Instruction(OpCode.PUSH, 10),
                Instruction(OpCode.PUSH, 0),
                Instruction(OpCode.DIV),  # 10 / 0
                Instruction(OpCode.HALT),
            ]
        )

        # 应该抛出ZeroDivisionError
        with pytest.raises(ZeroDivisionError):
            vm.run()

    def test_debug_mode(self):
        """测试调试模式"""
        vm = VirtualMachine(debug=True)
        vm.load([Instruction(OpCode.PUSH, 42), Instruction(OpCode.HALT)])

        # 运行应该不会出错
        vm.run()
        assert vm.stack == [42]
        assert vm.pc == 2

    def test_halt_instruction(self):
        """测试HALT指令"""
        vm = VirtualMachine()
        vm.load(
            [
                Instruction(OpCode.PUSH, 1),
                Instruction(OpCode.HALT),
                Instruction(OpCode.PUSH, 2),  # 不应该执行
                Instruction(OpCode.PUSH, 3),  # 不应该执行
            ]
        )
        vm.run()

        assert vm.stack == [1]  # 只执行了PUSH 1
        assert vm.pc == 2  # 停在HALT指令

    def test_instruction_string_representation(self):
        """测试指令的字符串表示"""
        instr1 = Instruction(OpCode.PUSH, 42)
        instr2 = Instruction(OpCode.ADD)

        assert str(instr1) == "PUSH 42"
        assert str(instr2) == "ADD"
