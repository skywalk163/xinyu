#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Python字节码编译器

将AST节点直接编译为Python字节码，跳过Python源代码生成步骤。
使用Python的ast模块和compile()函数直接生成字节码。
"""

import ast
import dis
import types
from typing import Any, Dict, Optional

from src.parser.ast_nodes import (
    AssignNode,
    ASTNode,
    BinaryOpNode,
    BlockNode,
    ClassNode,
    DictNode,
    ExceptNode,
    ExportNode,
    ForNode,
    FromImportNode,
    FunctionCallNode,
    FunctionDefNode,
    IdentifierNode,
    IfNode,
    ImportNode,
    IndexNode,
    InterfaceNode,
    ListNode,
    MemberAccessNode,
    MethodNode,
    NewNode,
    NumberNode,
    ProgramNode,
    PropertyNode,
    RaiseNode,
    RepeatNode,
    ReturnNode,
    StringNode,
    SuperNode,
    ThisNode,
    TryNode,
    UnaryOpNode,
    VarDefNode,
    WhileNode,
)


class BytecodeCompileError(Exception):
    """字节码编译错误"""


class BytecodeCompiler:
    """Python字节码编译器

    将AST节点直接编译为Python字节码，跳过Python源代码生成步骤。
    使用Python的ast模块构建抽象语法树，然后使用compile()生成字节码。

    优势：
    1. 跳过字符串生成步骤，减少内存分配
    2. 直接生成字节码，执行速度更快
    3. 支持更复杂的优化
    4. 更好的错误位置信息
    """

    # 内置函数映射：中文函数名 -> Python函数名
    BUILTIN_FUNCTIONS: Dict[str, str] = {
        "打印": "print",
        "输入": "input",
        "输出": "print",
        "写入": "print",
        "读取": "input",
        "请读取": "input",  # 别名
        "长度": "len",
        "范围": "range",
        "类型": "type",
        "整数": "int",
        "浮点": "float",
        "字符串": "str",
        "列表": "list",
        "字典": "dict",
        "绝对值": "abs",
        "最大值": "max",
        "最小值": "min",
        "求和": "sum",
        "排序": "sorted",
        "反转": "reversed",
        # 高阶函数
        "皆": "map",
        "只": "filter",
        # 旧语法兼容
        "印": "print",
        "读": "input",
    }

    # 二元操作符映射：中文操作符 -> Python操作符
    BINARY_OPERATORS: Dict[str, str] = {
        # 新语法（双字）
        "相加": "+",
        "相减": "-",
        "相乘": "*",
        "相除": "/",
        "相除以": "/",  # 别名
        "取余": "%",
        "等于": "==",
        "不等": "!=",
        "大于": ">",
        "大于于": ">",  # 别名
        "小于": "<",
        "小于于": "<",  # 别名
        "大等": ">=",
        "大于等于": ">=",  # 别名
        "小等": "<=",
        "小于等于": "<=",  # 别名
        "并且": "and",
        "或者": "or",
        # 旧语法（单字，兼容）
        "加": "+",
        "减": "-",
        "乘": "*",
        "除": "/",
        "等": "==",
        "大": ">",
        "小": "<",
        "且": "and",
        "或": "or",
    }

    # 一元操作符映射：中文操作符 -> Python操作符
    UNARY_OPERATORS: Dict[str, str] = {
        # 新语法
        "非也": "not",
        "非也也": "not",  # 别名
        # 旧语法（兼容）
        "负": "-",
        "非": "not",
    }

    def __init__(self, optimize: int = 0):
        """初始化字节码编译器

        Args:
            optimize: 优化级别（0=无优化，1=基本优化，2=完全优化）
        """
        self.optimize = optimize
        self._current_module = None
        self._current_function = None
        self._current_class = None
        self._indent_level = 0
        self._indent_str = "    "  # 4个空格

    def compile(self, node: ASTNode, filename: str = "<xinyu>") -> types.CodeType:
        """编译AST节点为Python字节码

        Args:
            node: AST节点
            filename: 源文件名（用于错误信息）

        Returns:
            Python字节码对象

        Raises:
            BytecodeCompileError: 编译错误
        """
        try:
            # 将心语AST转换为Python AST
            py_ast = self._convert_to_python_ast(node)

            # 设置源文件位置信息
            if hasattr(py_ast, "lineno"):
                py_ast.lineno = 1
                py_ast.col_offset = 0

            # 编译为字节码
            code_obj = compile(
                py_ast, filename=filename, mode="exec", optimize=self.optimize, dont_inherit=True
            )

            return code_obj

        except Exception as e:
            raise BytecodeCompileError(f"字节码编译失败: {e}")

    def compile_and_execute(
        self,
        node: ASTNode,
        globals_dict: Optional[Dict] = None,
        locals_dict: Optional[Dict] = None,
        filename: str = "<xinyu>",
    ) -> Any:
        """编译并执行AST节点

        Args:
            node: AST节点
            globals_dict: 全局变量字典
            locals_dict: 局部变量字典
            filename: 源文件名

        Returns:
            执行结果
        """
        # 编译为字节码
        code_obj = self.compile(node, filename)

        # 准备执行环境
        if globals_dict is None:
            globals_dict = {}

        # 添加内置函数
        self._add_builtins(globals_dict)

        # 执行字节码
        exec(code_obj, globals_dict, locals_dict)

        # 返回结果（如果有）
        if "__result__" in globals_dict:
            return globals_dict["__result__"]
        return None

    def _add_builtins(self, globals_dict: Dict):
        """添加内置函数到全局变量字典"""
        for chinese_name, python_name in self.BUILTIN_FUNCTIONS.items():
            if python_name in __builtins__:
                globals_dict[chinese_name] = __builtins__[python_name]

    def _convert_to_python_ast(self, node: ASTNode) -> ast.AST:
        """将心语AST节点转换为Python AST节点

        Args:
            node: 心语AST节点

        Returns:
            Python AST节点
        """
        node_type = node.__class__.__name__
        method_name = f"_convert_{node_type.replace('Node', '').lower()}"
        method = getattr(self, method_name, None)

        if method is None:
            raise BytecodeCompileError(f"不支持的节点类型: {node_type}")

        return method(node)

    # ============ 基础表达式转换方法 ============

    def _convert_number(self, node: NumberNode) -> ast.Constant:
        """转换数字节点为Python AST常量节点"""
        return ast.Constant(value=node.value, lineno=node.line, col_offset=node.column)

    def _convert_string(self, node: StringNode) -> ast.Constant:
        """转换字符串节点为Python AST常量节点"""
        return ast.Constant(value=node.value, lineno=node.line, col_offset=node.column)

    def _convert_identifier(self, node: IdentifierNode) -> ast.Name:
        """转换标识符节点为Python AST名称节点"""
        return ast.Name(id=node.name, ctx=ast.Load(), lineno=node.line, col_offset=node.column)

    # ============ 复合表达式转换方法 ============

    def _convert_binaryop(self, node: BinaryOpNode) -> ast.BinOp:
        """转换二元操作节点为Python AST二元操作节点"""
        # 转换左右操作数
        left = self._convert_to_python_ast(node.left)
        right = self._convert_to_python_ast(node.right)

        # 映射操作符
        operator = self.BINARY_OPERATORS.get(node.operator)
        if operator is None:
            # 如果不是中文操作符，可能是英文操作符
            if node.operator in [
                "+",
                "-",
                "*",
                "/",
                "%",
                "//",
                "**",
                "==",
                "!=",
                "<",
                ">",
                "<=",
                ">=",
                "and",
                "or",
            ]:
                operator = node.operator
            else:
                raise BytecodeCompileError(f"不支持的二元操作符: {node.operator}")

        # 创建二元操作节点
        op_map = {
            "+": ast.Add(),
            "-": ast.Sub(),
            "*": ast.Mult(),
            "/": ast.Div(),
            "//": ast.FloorDiv(),
            "%": ast.Mod(),
            "**": ast.Pow(),
            "==": ast.Eq(),
            "!=": ast.NotEq(),
            "<": ast.Lt(),
            ">": ast.Gt(),
            "<=": ast.LtE(),
            ">=": ast.GtE(),
            "and": ast.And(),
            "or": ast.Or(),
        }

        if operator not in op_map:
            raise BytecodeCompileError(f"不支持的二元操作符: {operator}")

        return ast.BinOp(
            left=left, op=op_map[operator], right=right, lineno=node.line, col_offset=node.column
        )

    def _convert_unaryop(self, node: UnaryOpNode) -> ast.UnaryOp:
        """转换一元操作节点为Python AST一元操作节点"""
        # 转换操作数
        operand = self._convert_to_python_ast(node.operand)

        # 映射操作符
        operator = self.UNARY_OPERATORS.get(node.operator)
        if operator is None:
            # 如果不是中文操作符，可能是英文操作符
            if node.operator in ["-", "+", "not"]:
                operator = node.operator
            else:
                raise BytecodeCompileError(f"不支持的一元操作符: {node.operator}")

        # 创建一元操作节点
        op_map = {
            "-": ast.USub(),
            "+": ast.UAdd(),
            "not": ast.Not(),
        }

        if operator not in op_map:
            raise BytecodeCompileError(f"不支持的一元操作符: {operator}")

        return ast.UnaryOp(
            op=op_map[operator], operand=operand, lineno=node.line, col_offset=node.column
        )

    def _convert_functioncall(self, node: FunctionCallNode) -> ast.Call:
        """转换函数调用节点为Python AST调用节点"""
        # 转换函数名
        if isinstance(node.name, str):
            func_name = node.name
            # 检查是否为内置函数
            if func_name in self.BUILTIN_FUNCTIONS:
                func_name = self.BUILTIN_FUNCTIONS[func_name]
            func = ast.Name(id=func_name, ctx=ast.Load(), lineno=node.line, col_offset=node.column)
        else:
            func = self._convert_to_python_ast(node.name)

        # 转换参数
        args = []
        for arg in node.args:
            args.append(self._convert_to_python_ast(arg))

        # 创建调用节点
        return ast.Call(func=func, args=args, keywords=[], lineno=node.line, col_offset=node.column)

    def _convert_memberaccess(self, node: MemberAccessNode) -> ast.Attribute:
        """转换成员访问节点为Python AST属性节点"""
        obj = self._convert_to_python_ast(node.obj)
        return ast.Attribute(
            value=obj, attr=node.member, ctx=ast.Load(), lineno=node.line, col_offset=node.column
        )

    def _convert_index(self, node: IndexNode) -> ast.Subscript:
        """转换索引节点为Python AST下标节点"""
        obj = self._convert_to_python_ast(node.obj)
        index = self._convert_to_python_ast(node.index)
        return ast.Subscript(
            value=obj,
            slice=ast.Index(value=index),
            ctx=ast.Load(),
            lineno=node.line,
            col_offset=node.column,
        )

    # ============ 语句转换方法 ============

    def _convert_vardef(self, node: VarDefNode) -> ast.Assign:
        """转换变量定义节点为Python AST赋值节点"""
        if node.value is not None:
            value = self._convert_to_python_ast(node.value)
        else:
            value = ast.Constant(value=None, lineno=node.line, col_offset=node.column)

        target = ast.Name(id=node.name, ctx=ast.Store(), lineno=node.line, col_offset=node.column)
        return ast.Assign(targets=[target], value=value, lineno=node.line, col_offset=node.column)

    def _convert_assign(self, node: AssignNode) -> ast.Assign:
        """转换赋值节点为Python AST赋值节点"""
        target = self._convert_to_python_ast(node.target)
        value = self._convert_to_python_ast(node.value)

        # 确保目标是存储上下文
        if isinstance(target, ast.Name):
            target.ctx = ast.Store()
        elif isinstance(target, ast.Attribute):
            target.ctx = ast.Store()
        elif isinstance(target, ast.Subscript):
            target.ctx = ast.Store()

        return ast.Assign(targets=[target], value=value, lineno=node.line, col_offset=node.column)

    def _convert_if(self, node: IfNode) -> ast.If:
        """转换条件节点为Python AST条件节点"""
        # 转换条件
        test = self._convert_to_python_ast(node.condition)

        # 转换then分支
        then_body = []
        if node.then_branch:
            for stmt in node.then_branch:
                then_body.append(self._convert_to_python_ast(stmt))
        else:
            then_body.append(ast.Pass(lineno=node.line, col_offset=node.column))

        # 转换else分支
        else_body = []
        if node.else_branch:
            for stmt in node.else_branch:
                else_body.append(self._convert_to_python_ast(stmt))

        return ast.If(
            test=test, body=then_body, orelse=else_body, lineno=node.line, col_offset=node.column
        )

    def _convert_while(self, node: WhileNode) -> ast.While:
        """转换while循环节点为Python AST while循环节点"""
        # 转换条件
        test = self._convert_to_python_ast(node.condition)

        # 转换循环体
        body = []
        if node.body:
            for stmt in node.body:
                body.append(self._convert_to_python_ast(stmt))
        else:
            body.append(ast.Pass(lineno=node.line, col_offset=node.column))

        return ast.While(test=test, body=body, orelse=[], lineno=node.line, col_offset=node.column)

    def _convert_for(self, node: ForNode) -> ast.For:
        """转换for循环节点为Python AST for循环节点"""
        # 转换目标
        target = self._convert_to_python_ast(node.target)
        if isinstance(target, ast.Name):
            target.ctx = ast.Store()

        # 转换可迭代对象
        iter_obj = self._convert_to_python_ast(node.iterable)

        # 转换循环体
        body = []
        if node.body:
            for stmt in node.body:
                body.append(self._convert_to_python_ast(stmt))
        else:
            body.append(ast.Pass(lineno=node.line, col_offset=node.column))

        return ast.For(
            target=target,
            iter=iter_obj,
            body=body,
            orelse=[],
            lineno=node.line,
            col_offset=node.column,
        )

    def _convert_return(self, node: ReturnNode) -> ast.Return:
        """转换return节点为Python AST return节点"""
        if node.value is not None:
            value = self._convert_to_python_ast(node.value)
        else:
            value = None

        return ast.Return(value=value, lineno=node.line, col_offset=node.column)

    # ============ 特殊节点转换方法 ============

    def _convert_program(self, node: ProgramNode) -> ast.Module:
        """转换程序节点为Python AST模块节点"""
        body = []
        for stmt in node.statements:
            body.append(self._convert_to_python_ast(stmt))

        return ast.Module(body=body, type_ignores=[])

    def _convert_block(self, node: BlockNode) -> list:
        """转换代码块节点为Python AST语句列表"""
        body = []
        for stmt in node.statements:
            body.append(self._convert_to_python_ast(stmt))
        return body

    def _convert_try(self, node: TryNode) -> ast.Try:
        """转换try节点为Python AST try节点"""
        # 转换try块
        body = []
        if node.try_body:
            for stmt in node.try_body:
                body.append(self._convert_to_python_ast(stmt))
        else:
            body.append(ast.Pass(lineno=node.line, col_offset=node.column))

        # 转换except子句
        handlers = []
        for except_clause in node.except_clauses:
            handlers.append(self._convert_except(except_clause))

        # 转换finally块
        finalbody = []
        if node.finally_body:
            for stmt in node.finally_body:
                finalbody.append(self._convert_to_python_ast(stmt))

        return ast.Try(
            body=body,
            handlers=handlers,
            orelse=[],
            finalbody=finalbody,
            lineno=node.line,
            col_offset=node.column,
        )

    def _convert_except(self, node: ExceptNode) -> ast.ExceptHandler:
        """转换except节点为Python AST except处理器节点"""
        # 转换异常类型
        if node.exception_type:
            type_node = self._convert_to_python_ast(node.exception_type)
        else:
            type_node = None

        # 转换异常变量名
        if node.exception_var:
            name = node.exception_var
        else:
            name = None

        # 转换except块
        body = []
        if node.body:
            for stmt in node.body:
                body.append(self._convert_to_python_ast(stmt))
        else:
            body.append(ast.Pass(lineno=node.line, col_offset=node.column))

        return ast.ExceptHandler(
            type=type_node, name=name, body=body, lineno=node.line, col_offset=node.column
        )

    def _convert_raise(self, node: RaiseNode) -> ast.Raise:
        """转换raise节点为Python AST raise节点"""
        if node.exception:
            exc = self._convert_to_python_ast(node.exception)
        else:
            exc = None

        return ast.Raise(exc=exc, cause=None, lineno=node.line, col_offset=node.column)

    def _convert_import(self, node: ImportNode) -> ast.Import:
        """转换import节点为Python AST import节点"""
        if node.alias:
            alias = ast.alias(name=node.module, asname=node.alias)
        else:
            alias = ast.alias(name=node.module, asname=None)

        return ast.Import(names=[alias], lineno=node.line, col_offset=node.column)

    def _convert_fromimport(self, node: FromImportNode) -> ast.ImportFrom:
        """转换from...import节点为Python AST import from节点"""
        # 构建导入列表
        names = []
        for name in node.names:
            if name in node.aliases:
                alias = ast.alias(name=name, asname=node.aliases[name])
            else:
                alias = ast.alias(name=name, asname=None)
            names.append(alias)

        return ast.ImportFrom(
            module=node.module, names=names, level=0, lineno=node.line, col_offset=node.column
        )

    # ============ OOP节点转换方法 ============

    def _convert_class(self, node: ClassNode) -> ast.ClassDef:
        """转换类节点为Python AST类定义节点"""
        # 构建基类列表
        bases = []
        if node.extends:
            bases.append(
                ast.Name(id=node.extends, ctx=ast.Load(), lineno=node.line, col_offset=node.column)
            )
        elif node.implements:
            for interface in node.implements:
                bases.append(
                    ast.Name(id=interface, ctx=ast.Load(), lineno=node.line, col_offset=node.column)
                )

        # 转换类成员
        body = []
        if node.members:
            for member in node.members:
                body.append(self._convert_to_python_ast(member))
        else:
            body.append(ast.Pass(lineno=node.line, col_offset=node.column))

        return ast.ClassDef(
            name=node.name,
            bases=bases,
            keywords=[],
            body=body,
            decorator_list=[],
            lineno=node.line,
            col_offset=node.column,
        )

    def _convert_interface(self, node: InterfaceNode) -> ast.ClassDef:
        """转换接口节点为Python AST类定义节点"""
        # 接口转换为抽象类
        body = []
        if node.methods:
            for method in node.methods:
                body.append(self._convert_to_python_ast(method))
        else:
            body.append(ast.Pass(lineno=node.line, col_offset=node.column))

        # 添加abc.ABC基类
        bases = [
            ast.Attribute(value=ast.Name(id="abc", ctx=ast.Load()), attr="ABC", ctx=ast.Load())
        ]

        return ast.ClassDef(
            name=node.name,
            bases=bases,
            keywords=[],
            body=body,
            decorator_list=[],
            lineno=node.line,
            col_offset=node.column,
        )

    def _convert_method(self, node: MethodNode) -> ast.FunctionDef:
        """转换方法节点为Python AST函数定义节点"""
        # 构建参数列表
        args = []

        # 添加self参数（如果不是静态方法）
        if not node.is_static:
            args.append(ast.arg(arg="sel", annotation=None))

        # 添加其他参数
        for param in node.params:
            args.append(ast.arg(arg=param, annotation=None))

        # 构建函数体
        body = []
        if node.body:
            for stmt in node.body:
                body.append(self._convert_to_python_ast(stmt))
        else:
            body.append(ast.Pass(lineno=node.line, col_offset=node.column))

        # 构建函数定义
        func_def = ast.FunctionDef(
            name=node.name if not node.is_constructor else "__init__",
            args=ast.arguments(
                posonlyargs=[],
                args=args,
                vararg=None,
                kwonlyargs=[],
                kw_defaults=[],
                kwarg=None,
                defaults=[],
            ),
            body=body,
            decorator_list=[],
            returns=None,
            lineno=node.line,
            col_offset=node.column,
        )

        # 如果是静态方法，添加装饰器
        if node.is_static:
            func_def.decorator_list.append(ast.Name(id="staticmethod", ctx=ast.Load()))

        return func_def

    def _convert_property(self, node: PropertyNode) -> ast.Assign:
        """转换属性节点为Python AST赋值节点"""
        if node.is_static:
            # 静态属性
            target = ast.Name(
                id=node.name, ctx=ast.Store(), lineno=node.line, col_offset=node.column
            )
        else:
            # 实例属性（在__init__中设置）
            # 这里需要特殊处理，因为属性定义通常在__init__方法中
            # 暂时返回一个赋值语句
            target = ast.Attribute(
                value=ast.Name(id="sel", ctx=ast.Load()),
                attr=node.name,
                ctx=ast.Store(),
                lineno=node.line,
                col_offset=node.column,
            )

        if node.value is not None:
            value = self._convert_to_python_ast(node.value)
        else:
            value = ast.Constant(value=None, lineno=node.line, col_offset=node.column)

        return ast.Assign(targets=[target], value=value, lineno=node.line, col_offset=node.column)

    def _convert_new(self, node: NewNode) -> ast.Call:
        """转换新建对象节点为Python AST调用节点"""
        # 转换类名
        class_name = ast.Name(
            id=node.class_name, ctx=ast.Load(), lineno=node.line, col_offset=node.column
        )

        # 转换参数
        args = []
        for arg in node.args:
            args.append(self._convert_to_python_ast(arg))

        return ast.Call(
            func=class_name, args=args, keywords=[], lineno=node.line, col_offset=node.column
        )

    def _convert_this(self, node: ThisNode) -> ast.Name:
        """转换this节点为Python AST名称节点"""
        return ast.Name(id="sel", ctx=ast.Load(), lineno=node.line, col_offset=node.column)

    def _convert_super(self, node: SuperNode) -> ast.Call:
        """转换super节点为Python AST调用节点"""
        return ast.Call(
            func=ast.Name(id="super", ctx=ast.Load()),
            args=[],
            keywords=[],
            lineno=node.line,
            col_offset=node.column,
        )

    def _convert_export(self, node: ExportNode) -> ast.Assign:
        """转换导出节点为Python AST赋值节点"""
        # 构建__all__列表
        elements = []
        for name in node.names:
            if name in node.aliases:
                # 处理别名
                elements.append(ast.Constant(value=f"{name} as {node.aliases[name]}"))
            else:
                elements.append(ast.Constant(value=name))

        list_node = ast.List(elts=elements, ctx=ast.Load())

        return ast.Assign(
            targets=[ast.Name(id="__all__", ctx=ast.Store())],
            value=list_node,
            lineno=node.line,
            col_offset=node.column,
        )

    # ============ 其他节点转换方法 ============

    def _convert_list(self, node: ListNode) -> ast.List:
        """转换列表节点为Python AST列表节点"""
        elements = []
        for elem in node.elements:
            elements.append(self._convert_to_python_ast(elem))

        return ast.List(elts=elements, ctx=ast.Load(), lineno=node.line, col_offset=node.column)

    def _convert_dict(self, node: DictNode) -> ast.Dict:
        """转换字典节点为Python AST字典节点"""
        keys = []
        values = []

        for key, value in node.items.items():
            keys.append(self._convert_to_python_ast(key))
            values.append(self._convert_to_python_ast(value))

        return ast.Dict(keys=keys, values=values, lineno=node.line, col_offset=node.column)

    def _convert_repeat(self, node: RepeatNode) -> ast.For:
        """转换repeat循环节点为Python AST for循环节点"""
        # repeat循环转换为for循环
        count = self._convert_to_python_ast(node.count)

        # 创建range调用
        range_call = ast.Call(
            func=ast.Name(id="range", ctx=ast.Load()),
            args=[count],
            keywords=[],
            lineno=node.line,
            col_offset=node.column,
        )

        # 创建for循环
        target = ast.Name(id="_", ctx=ast.Store(), lineno=node.line, col_offset=node.column)

        # 转换循环体
        body = []
        if node.body:
            for stmt in node.body:
                body.append(self._convert_to_python_ast(stmt))
        else:
            body.append(ast.Pass(lineno=node.line, col_offset=node.column))

        return ast.For(
            target=target,
            iter=range_call,
            body=body,
            orelse=[],
            lineno=node.line,
            col_offset=node.column,
        )

    def _convert_functiondef(self, node: FunctionDefNode) -> ast.FunctionDef:
        """转换函数定义节点为Python AST函数定义节点"""
        # 构建参数列表
        args = []
        for param in node.params:
            args.append(
                ast.arg(arg=param, annotation=None, lineno=node.line, col_offset=node.column)
            )

        # 构建函数体
        body = []
        if node.body:
            for stmt in node.body:
                body.append(self._convert_to_python_ast(stmt))
        else:
            body.append(ast.Pass(lineno=node.line, col_offset=node.column))

        return ast.FunctionDef(
            name=node.name,
            args=ast.arguments(
                posonlyargs=[],
                args=args,
                vararg=None,
                kwonlyargs=[],
                kw_defaults=[],
                kwarg=None,
                defaults=[],
            ),
            body=body,
            decorator_list=[],
            returns=None,
            lineno=node.line,
            col_offset=node.column,
        )


# 测试函数
def test_bytecode_compiler():
    """测试字节码编译器"""
    from src.parser.ast_nodes import (
        AssignNode,
        BinaryOpNode,
        FunctionCallNode,
        FunctionDefNode,
        IdentifierNode,
        IfNode,
        NumberNode,
        ProgramNode,
        ReturnNode,
        StringNode,
        VarDefNode,
        WhileNode,
    )

    # 创建测试AST
    print("测试字节码编译器:")
    print("=" * 70)

    ast = ProgramNode(
        line=1,
        column=1,
        statements=[
            # 变量定义
            VarDefNode(
                line=1,
                column=1,
                name="x",
                value=BinaryOpNode(
                    line=1,
                    column=1,
                    left=NumberNode(line=1, column=1, value=10),
                    operator="+",
                    right=BinaryOpNode(
                        line=1,
                        column=1,
                        left=NumberNode(line=1, column=1, value=5),
                        operator="*",
                        right=NumberNode(line=1, column=1, value=2),
                    ),
                ),
            ),
            # 函数定义
            FunctionDefNode(
                line=2,
                column=1,
                name="add",
                params=["a", "b"],
                body=[
                    ReturnNode(
                        line=3,
                        column=5,
                        value=BinaryOpNode(
                            line=3,
                            column=5,
                            left=IdentifierNode(line=3, column=5, name="a"),
                            operator="+",
                            right=IdentifierNode(line=3, column=5, name="b"),
                        ),
                    )
                ],
            ),
            # 函数调用
            VarDefNode(
                line=4,
                column=1,
                name="result",
                value=FunctionCallNode(
                    line=4,
                    column=1,
                    name=IdentifierNode(line=4, column=1, name="add"),
                    args=[
                        IdentifierNode(line=4, column=1, name="x"),
                        NumberNode(line=4, column=1, value=5),
                    ],
                ),
            ),
            # 条件语句
            IfNode(
                line=5,
                column=1,
                condition=BinaryOpNode(
                    line=5,
                    column=1,
                    left=IdentifierNode(line=5, column=1, name="result"),
                    operator=">",
                    right=NumberNode(line=5, column=1, value=20),
                ),
                then_branch=[
                    FunctionCallNode(
                        line=6,
                        column=5,
                        name=IdentifierNode(line=6, column=5, name="print"),
                        args=[StringNode(line=6, column=5, value="结果大于20")],
                    )
                ],
                else_branch=[
                    FunctionCallNode(
                        line=7,
                        column=5,
                        name=IdentifierNode(line=7, column=5, name="print"),
                        args=[StringNode(line=7, column=5, value="结果小于等于20")],
                    )
                ],
            ),
            # 循环
            VarDefNode(line=8, column=1, name="sum", value=NumberNode(line=8, column=1, value=0)),
            VarDefNode(line=9, column=1, name="i", value=NumberNode(line=9, column=1, value=0)),
            WhileNode(
                line=10,
                column=1,
                condition=BinaryOpNode(
                    line=10,
                    column=1,
                    left=IdentifierNode(line=10, column=1, name="i"),
                    operator="<",
                    right=NumberNode(line=10, column=1, value=10),
                ),
                body=[
                    AssignNode(
                        line=11,
                        column=5,
                        target=IdentifierNode(line=11, column=5, name="sum"),
                        value=BinaryOpNode(
                            line=11,
                            column=5,
                            left=IdentifierNode(line=11, column=5, name="sum"),
                            operator="+",
                            right=IdentifierNode(line=11, column=5, name="i"),
                        ),
                    ),
                    AssignNode(
                        line=12,
                        column=5,
                        target=IdentifierNode(line=12, column=5, name="i"),
                        value=BinaryOpNode(
                            line=12,
                            column=5,
                            left=IdentifierNode(line=12, column=5, name="i"),
                            operator="+",
                            right=NumberNode(line=12, column=5, value=1),
                        ),
                    ),
                ],
            ),
            # 打印结果
            FunctionCallNode(
                line=13,
                column=1,
                name=IdentifierNode(line=13, column=1, name="print"),
                args=[
                    BinaryOpNode(
                        line=13,
                        column=1,
                        left=StringNode(line=13, column=1, value="总和: "),
                        operator="+",
                        right=IdentifierNode(line=13, column=1, name="sum"),
                    )
                ],
            ),
        ],
    )

    # 测试字节码编译器
    print("1. 测试字节码编译器:")
    print("-" * 50)

    compiler = BytecodeCompiler(optimize=1)

    try:
        # 编译为字节码
        code_obj = compiler.compile(ast)

        print("编译成功!")
        print(f"字节码对象: {code_obj}")
        print(f"字节码文件名: {code_obj.co_filename}")
        print(f"字节码参数数量: {code_obj.co_argcount}")
        print(f"字节码局部变量数量: {code_obj.co_nlocals}")
        print(f"字节码栈大小: {code_obj.co_stacksize}")
        print(f"字节码标志: {code_obj.co_flags}")

        # 反汇编字节码
        print("\n反汇编字节码:")
        print("-" * 50)
        dis.dis(code_obj)

        # 执行字节码
        print("\n执行字节码:")
        print("-" * 50)
        result = compiler.compile_and_execute(ast)
        print(f"执行结果: {result}")

        # 测试性能
        print("\n2. 性能测试:")
        print("-" * 50)

        import time

        # 编译性能
        start_time = time.perf_counter()
        for _ in range(1000):
            code_obj = compiler.compile(ast)
        compile_time = time.perf_counter() - start_time

        # 执行性能
        start_time = time.perf_counter()
        for _ in range(1000):
            compiler.compile_and_execute(ast)
        execute_time = time.perf_counter() - start_time

        print(f"编译1000次时间: {compile_time:.6f} 秒")
        print(f"执行1000次时间: {execute_time:.6f} 秒")
        print(f"总时间: {compile_time + execute_time:.6f} 秒")
        print(f"平均每次: {(compile_time + execute_time) / 1000 * 1000:.2f} 毫秒")

        # 与原始代码生成器比较
        print("\n3. 与原始代码生成器比较:")
        print("-" * 50)

        from src.codegen.python_codegen import PythonCodegen
        from src.runtime.secure_executor import SecureExecutor

        # 原始代码生成器
        original_codegen = PythonCodegen()
        secure_executor = SecureExecutor()

        # 生成Python代码
        start_time = time.perf_counter()
        for _ in range(1000):
            python_code = original_codegen.generate(ast)
        generate_time = time.perf_counter() - start_time

        # 编译Python代码
        start_time = time.perf_counter()
        for _ in range(1000):
            code_obj = compile(python_code, "<xinyu>", "exec")
        python_compile_time = time.perf_counter() - start_time

        # 执行Python代码
        start_time = time.perf_counter()
        for _ in range(1000):
            secure_executor.execute(python_code)
        python_execute_time = time.perf_counter() - start_time

        print("原始代码生成器:")
        print(f"  生成代码时间: {generate_time:.6f} 秒")
        print(f"  编译Python代码时间: {python_compile_time:.6f} 秒")
        print(f"  执行Python代码时间: {python_execute_time:.6f} 秒")
        print(f"  总时间: {generate_time + python_compile_time + python_execute_time:.6f} 秒")

        print("\n字节码编译器:")
        print(f"  编译时间: {compile_time:.6f} 秒")
        print(f"  执行时间: {execute_time:.6f} 秒")
        print(f"  总时间: {compile_time + execute_time:.6f} 秒")

        total_original = generate_time + python_compile_time + python_execute_time
        total_bytecode = compile_time + execute_time
        speedup = total_original / total_bytecode if total_bytecode > 0 else 0

        print(f"\n性能提升: {speedup:.2f}x")

        if speedup > 1:
            print(f"字节码编译器比原始代码生成器快 {speedup:.2f} 倍")
        else:
            print(f"原始代码生成器比字节码编译器快 {1 / speedup:.2f} 倍")

    except Exception as e:
        print(f"编译失败: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_bytecode_compiler()
