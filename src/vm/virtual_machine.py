# -*- coding: utf-8 -*-
"""心语语言虚拟机

实现基于栈的虚拟机，支持字节码执行。
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List


class OpCode(Enum):
    """操作码枚举"""

    # 栈操作
    PUSH = auto()  # 压栈
    POP = auto()  # 出栈
    DUP = auto()  # 复制栈顶

    # 算术运算
    ADD = auto()  # 加法
    SUB = auto()  # 减法
    MUL = auto()  # 乘法
    DIV = auto()  # 除法
    MOD = auto()  # 取模
    NEG = auto()  # 取负

    # 比较运算
    EQ = auto()  # 等于
    NE = auto()  # 不等于
    LT = auto()  # 小于
    LE = auto()  # 小于等于
    GT = auto()  # 大于
    GE = auto()  # 大于等于

    # 逻辑运算
    AND = auto()  # 逻辑与
    OR = auto()  # 逻辑或
    NOT = auto()  # 逻辑非

    # 变量操作
    LOAD = auto()  # 加载变量
    STORE = auto()  # 存储变量

    # 控制流
    JUMP = auto()  # 无条件跳转
    JUMP_IF_TRUE = auto()  # 为真跳转
    JUMP_IF_FALSE = auto()  # 为假跳转
    CALL = auto()  # 函数调用
    RETURN = auto()  # 返回

    # 内置函数
    PRINT = auto()  # 打印

    # 其他
    HALT = auto()  # 停止


@dataclass
class Instruction:
    """指令"""

    opcode: OpCode  # 操作码
    operand: Any = None  # 操作数

    def __str__(self):
        if self.operand is not None:
            return f"{self.opcode.name} {self.operand}"
        return self.opcode.name


class VirtualMachine:
    """心语语言虚拟机

    基于栈的虚拟机，执行字节码指令。
    """

    def __init__(self, debug: bool = False):
        """初始化虚拟机

        Args:
            debug: 是否启用调试模式
        """
        self.stack: List[Any] = []  # 操作数栈
        self.globals: Dict[str, Any] = {}  # 全局变量
        self.locals_stack: List[Dict] = [{}]  # 局部变量栈
        self.call_stack: List[int] = []  # 调用栈（保存返回地址）
        self.pc = 0  # 程序计数器
        self.instructions: List[Instruction] = []  # 指令序列
        self.debug = debug  # 调试模式
        self.running = False  # 运行状态

    def load(self, instructions: List[Instruction]):
        """加载指令序列

        Args:
            instructions: 指令列表
        """
        self.instructions = instructions
        self.pc = 0
        self.stack = []

    def run(self):
        """运行虚拟机"""
        self.running = True

        while self.running and self.pc < len(self.instructions):
            instruction = self.instructions[self.pc]

            if self.debug:
                print(f"PC={self.pc}: {instruction}, Stack={self.stack}")

            self._execute(instruction)
            self.pc += 1

    def _execute(self, instruction: Instruction):
        """执行单条指令

        Args:
            instruction: 要执行的指令
        """
        opcode = instruction.opcode
        operand = instruction.operand

        # 栈操作
        if opcode == OpCode.PUSH:
            self.stack.append(operand)

        elif opcode == OpCode.POP:
            self.stack.pop()

        elif opcode == OpCode.DUP:
            self.stack.append(self.stack[-1])

        # 算术运算
        elif opcode == OpCode.ADD:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a + b)

        elif opcode == OpCode.SUB:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a - b)

        elif opcode == OpCode.MUL:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a * b)

        elif opcode == OpCode.DIV:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a / b)

        elif opcode == OpCode.MOD:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a % b)

        elif opcode == OpCode.NEG:
            a = self.stack.pop()
            self.stack.append(-a)

        # 比较运算
        elif opcode == OpCode.EQ:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a == b)

        elif opcode == OpCode.NE:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a != b)

        elif opcode == OpCode.LT:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a < b)

        elif opcode == OpCode.LE:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a <= b)

        elif opcode == OpCode.GT:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a > b)

        elif opcode == OpCode.GE:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a >= b)

        # 逻辑运算
        elif opcode == OpCode.AND:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a and b)

        elif opcode == OpCode.OR:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a or b)

        elif opcode == OpCode.NOT:
            a = self.stack.pop()
            self.stack.append(not a)

        # 变量操作
        elif opcode == OpCode.LOAD:
            name = operand
            # 先查找局部变量，再查找全局变量
            for scope in reversed(self.locals_stack):
                if name in scope:
                    self.stack.append(scope[name])
                    return
            if name in self.globals:
                self.stack.append(self.globals[name])
            else:
                raise RuntimeError(f"未定义的变量: {name}")

        elif opcode == OpCode.STORE:
            name = operand
            value = self.stack.pop()
            # 存储到当前作用域
            self.locals_stack[-1][name] = value

        # 控制流
        elif opcode == OpCode.JUMP:
            self.pc = operand - 1  # -1 因为外层会+1

        elif opcode == OpCode.JUMP_IF_TRUE:
            condition = self.stack.pop()
            if condition:
                self.pc = operand - 1

        elif opcode == OpCode.JUMP_IF_FALSE:
            condition = self.stack.pop()
            if not condition:
                self.pc = operand - 1

        elif opcode == OpCode.CALL:
            # 保存返回地址
            self.call_stack.append(self.pc)
            # 跳转到函数入口
            self.pc = operand - 1
            # 创建新的局部作用域
            self.locals_stack.append({})

        elif opcode == OpCode.RETURN:
            # 恢复调用前的状态
            if self.call_stack:
                self.pc = self.call_stack.pop()
            # 弹出局部作用域
            if len(self.locals_stack) > 1:
                self.locals_stack.pop()

        # 内置函数
        elif opcode == OpCode.PRINT:
            value = self.stack.pop()
            print(value)

        # 其他
        elif opcode == OpCode.HALT:
            self.running = False

    def get_result(self) -> Any:
        """获取执行结果

        Returns:
            栈顶元素（如果有）
        """
        if self.stack:
            return self.stack[-1]
        return None


# 示例：编译简单表达式到字节码
def compile_expression(expr: str) -> List[Instruction]:
    """编译简单表达式到字节码

    Args:
        expr: 表达式字符串

    Returns:
        指令列表
    """
    # 这是一个简化的编译器示例
    # 实际实现需要完整的解析和代码生成

    instructions = []
    _ = .split()  # 未使用变量

    for token in tokens:
        if token.isdigit():
            instructions.append(Instruction(OpCode.PUSH, int(token)))
        elif token == "+":
            instructions.append(Instruction(OpCode.ADD))
        elif token == "-":
            instructions.append(Instruction(OpCode.SUB))
        elif token == "*":
            instructions.append(Instruction(OpCode.MUL))
        elif token == "/":
            instructions.append(Instruction(OpCode.DIV))

    instructions.append(Instruction(OpCode.HALT))
    return instructions


# 测试虚拟机
def test_vm():
    """测试虚拟机"""
    # 创建虚拟机
    vm = VirtualMachine(debug=True)

    # 编译并执行: 3 + 5 * 2
    instructions = [
        Instruction(OpCode.PUSH, 3),
        Instruction(OpCode.PUSH, 5),
        Instruction(OpCode.PUSH, 2),
        Instruction(OpCode.MUL),
        Instruction(OpCode.ADD),
        Instruction(OpCode.PRINT),
        Instruction(OpCode.HALT),
    ]

    print("执行: 3 + 5 * 2")
    vm.load(instructions)
    vm.run()
    print(f"结果: {vm.get_result()}")


if __name__ == "__main__":
    test_vm()
