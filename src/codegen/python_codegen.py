# -*- coding: utf-8 -*-
"""Python代码生成器

将AST节点转换为可执行的Python代码。
"""
from typing import Dict, Type
from src.parser.ast_nodes import (
    ASTNode,
    # 基础节点
    NumberNode, StringNode, IdentifierNode,
    # 表达式节点
    BinaryOpNode, UnaryOpNode, ListNode, DictNode,
    MemberAccessNode, IndexNode,
    # 语句节点
    AssignNode, VarDefNode, IfNode, ForNode, WhileNode,
    RepeatNode, FunctionDefNode, FunctionCallNode, ReturnNode,
    # 特殊节点
    ProgramNode, BlockNode
)


class CodegenError(Exception):
    """代码生成错误"""
    pass


class PythonCodegen:
    """Python代码生成器
    
    将AST节点转换为Python代码字符串。
    使用访问者模式遍历AST。
    """
    
    # 内置函数映射：中文函数名 -> Python函数名
    BUILTIN_FUNCTIONS: Dict[str, str] = {
        "印": "print",
        "读取": "input",
    }
    
    # 二元操作符映射：中文操作符 -> Python操作符
    BINARY_OPERATORS: Dict[str, str] = {
        "加": "+",
        "减": "-",
        "乘": "*",
        "除以": "/",
        "整除": "//",
        "取余": "%",
        "大于": ">",
        "小于": "<",
        "等于": "==",
        "不等于": "!=",
        "大于等于": ">=",
        "小于等于": "<=",
        "且": "and",
        "或": "or",
    }
    
    # 一元操作符映射：中文操作符 -> Python操作符
    UNARY_OPERATORS: Dict[str, str] = {
        "负": "-",
        "非": "not",
    }
    
    def __init__(self):
        """初始化代码生成器"""
        self.indent_level = 0
        self.indent_str = "    "  # 4个空格
    
    def generate(self, node: ASTNode) -> str:
        """生成Python代码
        
        Args:
            node: AST节点
            
        Returns:
            生成的Python代码字符串
            
        Raises:
            CodegenError: 遇到未知节点类型
        """
        # 根据节点类型分派到对应的生成方法
        method_name = f"_generate_{node.__class__.__name__.replace('Node', '').lower()}"
        method = getattr(self, method_name, None)
        
        if method is None:
            raise CodegenError(f"未知节点类型: {node.__class__.__name__}")
        
        return method(node)
    
    # ============ 辅助方法 ============
    
    def _indent(self) -> str:
        """获取当前缩进字符串
        
        Returns:
            当前缩进级别的缩进字符串
        """
        return self.indent_str * self.indent_level
    
    def _increase_indent(self):
        """增加缩进级别"""
        self.indent_level += 1
    
    def _decrease_indent(self):
        """减少缩进级别"""
        self.indent_level = max(0, self.indent_level - 1)
    
    # ============ 基础表达式生成方法 ============
    
    def _generate_number(self, node: NumberNode) -> str:
        """生成数字表达式
        
        Args:
            node: 数字节点
            
        Returns:
            数字字符串
        """
        return str(node.value)
    
    def _generate_string(self, node: StringNode) -> str:
        """生成字符串表达式
        
        Args:
            node: 字符串节点
            
        Returns:
            用单引号包裹的字符串
        """
        # 使用单引号包裹字符串
        return f"'{node.value}'"
    
    def _generate_identifier(self, node: IdentifierNode) -> str:
        """生成标识符表达式
        
        Args:
            node: 标识符节点
            
        Returns:
            标识符名称
        """
        return node.name
    
    # ============ 复合表达式生成方法 ============
    
    def _generate_binaryop(self, node: BinaryOpNode) -> str:
        """生成二元操作表达式
        
        Args:
            node: 二元操作节点
            
        Returns:
            二元操作表达式字符串
        """
        left = self.generate(node.left)
        right = self.generate(node.right)
        
        # 映射操作符
        operator = self.BINARY_OPERATORS.get(node.operator, node.operator)
        
        return f"{left} {operator} {right}"
    
    def _generate_unaryop(self, node: UnaryOpNode) -> str:
        """生成一元操作表达式
        
        Args:
            node: 一元操作节点
            
        Returns:
            一元操作表达式字符串
        """
        operand = self.generate(node.operand)
        
        # 映射操作符
        operator = self.UNARY_OPERATORS.get(node.operator, node.operator)
        
        # not 是关键字，需要空格
        if operator == "not":
            return f"{operator} {operand}"
        else:
            return f"{operator}{operand}"
    
    def _generate_list(self, node: ListNode) -> str:
        """生成列表表达式
        
        Args:
            node: 列表节点
            
        Returns:
            列表表达式字符串
        """
        elements = [self.generate(elem) for elem in node.elements]
        return f"[{', '.join(elements)}]"
    
    def _generate_dict(self, node: DictNode) -> str:
        """生成字典表达式
        
        Args:
            node: 字典节点
            
        Returns:
            字典表达式字符串
        """
        pairs = []
        for key, value in node.pairs:
            key_str = self.generate(key)
            value_str = self.generate(value)
            pairs.append(f"{key_str}: {value_str}")
        
        return f"{{{', '.join(pairs)}}}"
    
    def _generate_memberaccess(self, node: MemberAccessNode) -> str:
        """生成成员访问表达式
        
        Args:
            node: 成员访问节点
            
        Returns:
            成员访问表达式字符串
        """
        obj = self.generate(node.obj)
        return f"{obj}.{node.member}"
    
    def _generate_index(self, node: IndexNode) -> str:
        """生成索引表达式
        
        Args:
            node: 索引节点
            
        Returns:
            索引表达式字符串
        """
        obj = self.generate(node.obj)
        index = self.generate(node.index)
        return f"{obj}[{index}]"
    
    def _generate_functioncall(self, node: FunctionCallNode) -> str:
        """生成函数调用表达式
        
        Args:
            node: 函数调用节点
            
        Returns:
            函数调用表达式字符串
        """
        # 映射内置函数名
        func_name = self.BUILTIN_FUNCTIONS.get(node.name, node.name)
        
        # 生成参数列表
        args = [self.generate(arg) for arg in node.args]
        
        return f"{func_name}({', '.join(args)})"
    
    # ============ 语句生成方法 ============
    
    def _generate_vardef(self, node: VarDefNode) -> str:
        """生成变量定义语句
        
        Args:
            node: 变量定义节点
            
        Returns:
            变量定义语句字符串
        """
        if node.value is not None:
            value = self.generate(node.value)
            return f"{node.name} = {value}"
        else:
            return f"{node.name} = None"
    
    def _generate_assign(self, node: AssignNode) -> str:
        """生成赋值语句
        
        Args:
            node: 赋值节点
            
        Returns:
            赋值语句字符串
        """
        target = self.generate(node.target)
        value = self.generate(node.value)
        return f"{target} = {value}"
    
    def _generate_functiondef(self, node: FunctionDefNode) -> str:
        """生成函数定义语句
        
        Args:
            node: 函数定义节点
            
        Returns:
            函数定义语句字符串
        """
        # 生成函数签名
        params = ", ".join(node.params)
        lines = [f"def {node.name}({params}):"]
        
        # 增加缩进
        self._increase_indent()
        
        # 生成函数体
        if node.body:
            for stmt in node.body:
                lines.append(f"{self._indent()}{self.generate(stmt)}")
        else:
            # 空函数体
            lines.append(f"{self._indent()}pass")
        
        # 减少缩进
        self._decrease_indent()
        
        return "\n".join(lines)
    
    def _generate_if(self, node: IfNode) -> str:
        """生成条件语句
        
        Args:
            node: 条件节点
            
        Returns:
            条件语句字符串
        """
        condition = self.generate(node.condition)
        lines = [f"if {condition}:"]
        
        # 增加缩进
        self._increase_indent()
        
        # 生成then分支
        if node.then_branch:
            for stmt in node.then_branch:
                lines.append(f"{self._indent()}{self.generate(stmt)}")
        else:
            lines.append(f"{self._indent()}pass")
        
        # 减少缩进
        self._decrease_indent()
        
        # 生成else分支
        if node.else_branch:
            lines.append("else:")
            self._increase_indent()
            
            for stmt in node.else_branch:
                lines.append(f"{self._indent()}{self.generate(stmt)}")
            
            self._decrease_indent()
        
        return "\n".join(lines)
    
    def _generate_for(self, node: ForNode) -> str:
        """生成遍历循环语句
        
        Args:
            node: 遍历循环节点
            
        Returns:
            遍历循环语句字符串
        """
        iterable = self.generate(node.iterable)
        lines = [f"for {node.var} in {iterable}:"]
        
        # 增加缩进
        self._increase_indent()
        
        # 生成循环体
        if node.body:
            for stmt in node.body:
                lines.append(f"{self._indent()}{self.generate(stmt)}")
        else:
            lines.append(f"{self._indent()}pass")
        
        # 减少缩进
        self._decrease_indent()
        
        return "\n".join(lines)
    
    def _generate_while(self, node: WhileNode) -> str:
        """生成当循环语句
        
        Args:
            node: 当循环节点
            
        Returns:
            当循环语句字符串
        """
        condition = self.generate(node.condition)
        lines = [f"while {condition}:"]
        
        # 增加缩进
        self._increase_indent()
        
        # 生成循环体
        if node.body:
            for stmt in node.body:
                lines.append(f"{self._indent()}{self.generate(stmt)}")
        else:
            lines.append(f"{self._indent()}pass")
        
        # 减少缩进
        self._decrease_indent()
        
        return "\n".join(lines)
    
    def _generate_repeat(self, node: RepeatNode) -> str:
        """生成重复语句
        
        Args:
            node: 重复节点
            
        Returns:
            重复语句字符串（转换为for循环）
        """
        count = self.generate(node.count)
        lines = [f"for _ in range({count}):"]
        
        # 增加缩进
        self._increase_indent()
        
        # 生成循环体
        if node.body:
            for stmt in node.body:
                lines.append(f"{self._indent()}{self.generate(stmt)}")
        else:
            lines.append(f"{self._indent()}pass")
        
        # 减少缩进
        self._decrease_indent()
        
        return "\n".join(lines)
    
    def _generate_return(self, node: ReturnNode) -> str:
        """生成返回语句
        
        Args:
            node: 返回节点
            
        Returns:
            返回语句字符串
        """
        if node.value is not None:
            value = self.generate(node.value)
            return f"return {value}"
        else:
            return "return"
    
    # ============ 特殊节点生成方法 ============
    
    def _generate_program(self, node: ProgramNode) -> str:
        """生成程序
        
        Args:
            node: 程序节点
            
        Returns:
            程序代码字符串
        """
        if not node.statements:
            return ""
        
        lines = []
        for stmt in node.statements:
            lines.append(self.generate(stmt))
        
        return "\n".join(lines)
    
    def _generate_block(self, node: BlockNode) -> str:
        """生成代码块
        
        Args:
            node: 代码块节点
            
        Returns:
            代码块字符串
        """
        if not node.statements:
            return ""
        
        lines = []
        for stmt in node.statements:
            lines.append(f"{self._indent()}{self.generate(stmt)}")
        
        return "\n".join(lines)
