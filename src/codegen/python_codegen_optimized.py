# -*- coding: utf-8 -*-
"""优化版Python代码生成器

优化点：
1. 字符串构建优化：使用列表和join()代替字符串拼接
2. 方法查找缓存：缓存getattr()结果
3. 局部变量缓存：缓存常用字典引用
"""

import functools
from typing import Dict

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


class CodegenError(Exception):
    """代码生成错误"""


class OptimizedPythonCodegen:
    """优化版Python代码生成器

    将AST节点转换为Python代码字符串。
    使用访问者模式遍历AST。

    优化特性：
    1. 字符串构建优化：使用列表和join()代替字符串拼接
    2. 方法查找缓存：缓存getattr()结果，避免重复反射调用
    3. 局部变量缓存：缓存常用字典引用到局部变量
    4. 减少临时对象创建
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

    def __init__(self):
        """初始化优化版代码生成器"""
        self.indent_level = 0
        self.indent_str = "    "  # 4个空格
        self._method_cache = {}  # 方法缓存
        self._parts = []  # 字符串构建缓冲区

    def _reset_parts(self):
        """重置字符串构建缓冲区"""
        self._parts.clear()

    def _add_part(self, part: str):
        """添加字符串片段到缓冲区"""
        self._parts.append(part)

    def _build_string(self) -> str:
        """构建最终字符串"""
        return "".join(self._parts)

    def generate(self, node: ASTNode) -> str:
        """生成Python代码

        Args:
            node: AST节点

        Returns:
            生成的Python代码字符串

        Raises:
            CodegenError: 遇到未知节点类型
        """
        # 从缓存获取方法
        node_type = node.__class__.__name__
        method = self._method_cache.get(node_type)

        if method is None:
            # 缓存未命中，查找并缓存
            method_name = f"_generate_{node_type.replace('Node', '').lower()}"
            method = getattr(self, method_name, None)
            if method is None:
                raise CodegenError(f"未知节点类型: {node_type}")
            self._method_cache[node_type] = method

        # 重置字符串缓冲区
        self._reset_parts()
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

    # ============ 基础表达式生成方法（优化版） ============

    def _generate_number(self, node: NumberNode) -> str:
        """生成数字表达式（优化版）

        Args:
            node: 数字节点

        Returns:
            数字字符串
        """
        # 直接返回，不使用缓冲区
        return str(node.value)

    def _generate_string(self, node: StringNode) -> str:
        """生成字符串表达式（优化版）

        Args:
            node: 字符串节点

        Returns:
            正确转义的字符串字面量
        """
        # 使用 repr() 自动处理转义（包括引号、换行符等）
        return repr(node.value)

    def _generate_identifier(self, node: IdentifierNode) -> str:
        """生成标识符表达式（优化版）

        Args:
            node: 标识符节点

        Returns:
            标识符名称
        """
        # 直接返回，不使用缓冲区
        return node.name

    # ============ 复合表达式生成方法（优化版） ============

    def _generate_binaryop(self, node: BinaryOpNode) -> str:
        """生成二元操作表达式（优化版）

        Args:
            node: 二元操作节点

        Returns:
            二元操作表达式字符串

        Raises:
            CodegenError: 遇到未知的二元操作符
        """
        # 使用局部变量缓存字典引用
        BINARY_OPERATORS = self.BINARY_OPERATORS

        # 生成左右表达式
        left = self.generate(node.left)
        right = self.generate(node.right)

        # 映射操作符（支持中文和英文）
        operator = BINARY_OPERATORS.get(node.operator)
        if operator is None:
            # 如果不是中文操作符，可能是英文操作符（语法分析器已转换）
            # 直接使用英文操作符
            if node.operator in [
                "+",
                "-",
                "*",
                "/",
                "%",
                "//",
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
                raise CodegenError(f"未知的二元操作符: {node.operator}")

        # 使用列表构建字符串（优化）
        parts = ["(", left, " ", operator, " ", right, ")"]
        return "".join(parts)

    def _generate_unaryop(self, node: UnaryOpNode) -> str:
        """生成一元操作表达式（优化版）

        Args:
            node: 一元操作节点

        Returns:
            一元操作表达式字符串

        Raises:
            CodegenError: 遇到未知的一元操作符
        """
        # 使用局部变量缓存字典引用
        UNARY_OPERATORS = self.UNARY_OPERATORS

        operand = self.generate(node.operand)

        # 映射操作符（支持中文和英文）
        operator = UNARY_OPERATORS.get(node.operator)
        if operator is None:
            # 如果不是中文操作符，可能是英文操作符（语法分析器已转换）
            # 直接使用英文操作符
            if node.operator in ["-", "not"]:
                operator = node.operator
            else:
                raise CodegenError(f"未知的一元操作符: {node.operator}")

        # not 是关键字，需要空格
        if operator == "not":
            return f"{operator} {operand}"
        else:
            return f"{operator}{operand}"

    def _generate_functioncall(self, node: FunctionCallNode) -> str:
        """生成函数调用表达式（优化版）

        Args:
            node: 函数调用节点

        Returns:
            函数调用表达式字符串
        """
        # 使用局部变量缓存字典引用
        BUILTIN_FUNCTIONS = self.BUILTIN_FUNCTIONS

        # 生成函数名
        if isinstance(node.name, str):
            func_name = node.name
            # 检查是否为内置函数
            if func_name in BUILTIN_FUNCTIONS:
                func_name = BUILTIN_FUNCTIONS[func_name]
        else:
            func_name = self.generate(node.name)

        # 生成参数列表
        if node.args:
            # 使用列表构建参数字符串（优化）
            arg_parts = []
            for arg in node.args:
                arg_parts.append(self.generate(arg))
            args_str = ", ".join(arg_parts)
            return f"{func_name}({args_str})"
        else:
            return f"{func_name}()"

    def _generate_memberaccess(self, node: MemberAccessNode) -> str:
        """生成成员访问表达式（优化版）

        Args:
            node: 成员访问节点

        Returns:
            成员访问表达式字符串
        """
        obj = self.generate(node.obj)
        return f"{obj}.{node.member}"

    def _generate_index(self, node: IndexNode) -> str:
        """生成索引表达式（优化版）

        Args:
            node: 索引节点

        Returns:
            索引表达式字符串
        """
        obj = self.generate(node.obj)
        index = self.generate(node.index)
        return f"{obj}[{index}]"

    # ============ 语句生成方法（优化版） ============

    def _generate_vardef(self, node: VarDefNode) -> str:
        """生成变量定义语句（优化版）

        Args:
            node: 变量定义节点

        Returns:
            变量定义语句字符串
        """
        if node.value is not None:
            value = self.generate(node.value)
            return f"{node.name} = {value}"
        else:
            return node.name

    def _generate_assign(self, node: AssignNode) -> str:
        """生成赋值语句（优化版）

        Args:
            node: 赋值节点

        Returns:
            赋值语句字符串
        """
        target = self.generate(node.target)
        value = self.generate(node.value)
        return f"{target} = {value}"

    def _generate_if(self, node: IfNode) -> str:
        """生成条件语句（优化版）

        Args:
            node: 条件节点

        Returns:
            条件语句字符串
        """
        # 使用列表构建字符串（优化）
        parts = []

        # 生成条件
        condition = self.generate(node.condition)
        parts.append(f"if {condition}:")

        # 增加缩进
        self._increase_indent()

        # 生成then分支
        if node.then_branch:
            for stmt in node.then_branch:
                parts.append(f"{self._indent()}{self.generate(stmt)}")
        else:
            parts.append(f"{self._indent()}pass")

        # 减少缩进
        self._decrease_indent()

        # 生成else分支
        if node.else_branch:
            parts.append(f"{self._indent()}else:")
            self._increase_indent()

            for stmt in node.else_branch:
                parts.append(f"{self._indent()}{self.generate(stmt)}")

            self._decrease_indent()

        return "\n".join(parts)

    def _generate_while(self, node: WhileNode) -> str:
        """生成while循环语句（优化版）

        Args:
            node: while循环节点

        Returns:
            while循环语句字符串
        """
        # 使用列表构建字符串（优化）
        parts = []

        # 生成条件
        condition = self.generate(node.condition)
        parts.append(f"while {condition}:")

        # 增加缩进
        self._increase_indent()

        # 生成循环体
        if node.body:
            for stmt in node.body:
                parts.append(f"{self._indent()}{self.generate(stmt)}")
        else:
            parts.append(f"{self._indent()}pass")

        # 减少缩进
        self._decrease_indent()

        return "\n".join(parts)

    def _generate_for(self, node: ForNode) -> str:
        """生成for循环语句（优化版）

        Args:
            node: for循环节点

        Returns:
            for循环语句字符串
        """
        # 使用列表构建字符串（优化）
        parts = []

        # 生成迭代变量和可迭代对象
        target = self.generate(node.target)
        iterable = self.generate(node.iterable)
        parts.append(f"for {target} in {iterable}:")

        # 增加缩进
        self._increase_indent()

        # 生成循环体
        if node.body:
            for stmt in node.body:
                parts.append(f"{self._indent()}{self.generate(stmt)}")
        else:
            parts.append(f"{self._indent()}pass")

        # 减少缩进
        self._decrease_indent()

        return "\n".join(parts)

    def _generate_return(self, node: ReturnNode) -> str:
        """生成return语句（优化版）

        Args:
            node: return节点

        Returns:
            return语句字符串
        """
        if node.value is not None:
            value = self.generate(node.value)
            return f"return {value}"
        else:
            return "return"

    # ============ 特殊节点生成方法（优化版） ============

    def _generate_program(self, node: ProgramNode) -> str:
        """生成程序（优化版）

        Args:
            node: 程序节点

        Returns:
            程序代码字符串
        """
        if not node.statements:
            return ""

        # 使用列表构建字符串（优化）
        lines = []
        for stmt in node.statements:
            code = self._generate_statement(stmt)
            if code:
                lines.append(code)

        return "\n".join(lines)

    def _generate_statement(self, stmt: ASTNode) -> str:
        """生成语句代码（优化版）

        Args:
            stmt: 语句节点

        Returns:
            语句代码字符串
        """
        # 特殊处理：单独的标识符语句可能是函数调用
        if isinstance(stmt, IdentifierNode):
            # 生成函数调用（无参数）
            return f"{stmt.name}()"

        return self.generate(stmt)

    def _generate_block(self, node: BlockNode) -> str:
        """生成代码块（优化版）

        Args:
            node: 代码块节点

        Returns:
            代码块字符串
        """
        if not node.statements:
            return ""

        # 使用列表构建字符串（优化）
        lines = []
        for stmt in node.statements:
            lines.append(f"{self._indent()}{self.generate(stmt)}")

        return "\n".join(lines)

    def _generate_try(self, node: TryNode) -> str:
        """生成try-except-finally语句（优化版）

        Args:
            node: try节点

        Returns:
            try-except-finally语句字符串
        """
        # 使用列表构建字符串（优化）
        lines = ["try:"]

        # 增加缩进
        self._increase_indent()

        # 生成try块
        if node.try_body:
            for stmt in node.try_body:
                lines.append(f"{self._indent()}{self.generate(stmt)}")
        else:
            lines.append(f"{self._indent()}pass")

        # 减少缩进
        self._decrease_indent()

        # 生成except子句
        for except_clause in node.except_clauses:
            lines.append(self._generate_except(except_clause))

        # 生成finally块
        if node.finally_body:
            lines.append(f"{self._indent()}finally:")
            self._increase_indent()

            for stmt in node.finally_body:
                lines.append(f"{self._indent()}{self.generate(stmt)}")

            self._decrease_indent()

        return "\n".join(lines)

    def _generate_except(self, node: ExceptNode) -> str:
        """生成except子句（优化版）

        Args:
            node: except节点

        Returns:
            except子句字符串
        """
        # 构建except语句
        if node.exception_type:
            exception_type = self.generate(node.exception_type)
            if node.exception_var:
                except_line = f"except {exception_type} as {node.exception_var}:"
            else:
                except_line = f"except {exception_type}:"
        else:
            except_line = "except:"

        # 使用列表构建字符串（优化）
        lines = [f"{self._indent()}{except_line}"]

        # 增加缩进
        self._increase_indent()

        # 生成except块
        if node.body:
            for stmt in node.body:
                lines.append(f"{self._indent()}{self.generate(stmt)}")
        else:
            lines.append(f"{self._indent()}pass")

        # 减少缩进
        self._decrease_indent()

        return "\n".join(lines)

    def _generate_raise(self, node: RaiseNode) -> str:
        """生成raise语句（优化版）

        Args:
            node: raise节点

        Returns:
            raise语句字符串
        """
        if node.exception:
            exception = self.generate(node.exception)
            return f"raise {exception}"
        else:
            return "raise"

    def _generate_import(self, node: ImportNode) -> str:
        """生成import语句（优化版）

        Args:
            node: import节点

        Returns:
            import语句字符串
        """
        if node.alias:
            return f"import {node.module} as {node.alias}"
        else:
            return f"import {node.module}"

    def _generate_fromimport(self, node: FromImportNode) -> str:
        """生成from...import语句（优化版）

        Args:
            node: from...import节点

        Returns:
            from...import语句字符串
        """
        # 构建导入列表（优化）
        import_list = []
        for name in node.names:
            if name in node.aliases:
                import_list.append(f"{name} as {node.aliases[name]}")
            else:
                import_list.append(name)

        imports_str = ", ".join(import_list)
        return f"from {node.module} import {imports_str}"

    # ============ OOP节点生成方法（优化版） ============

    def _generate_class(self, node: ClassNode) -> str:
        """生成类定义（优化版）

        Args:
            node: 类节点

        Returns:
            类定义字符串
        """
        # 使用列表构建字符串（优化）
        parts = ["class ", node.name]

        # 添加继承
        if node.extends:
            parts.append(f"({node.extends})")

        # 添加接口实现
        elif node.implements:
            interfaces = ", ".join(node.implements)
            parts.append(f"({interfaces})")

        parts.append(":")

        # 增加缩进
        self._increase_indent()

        # 生成类成员
        if node.members:
            for member in node.members:
                member_code = self.generate(member)
                if member_code:
                    parts.append(f"\n{self._indent()}{member_code}")
        else:
            parts.append(f"\n{self._indent()}pass")

        # 减少缩进
        self._decrease_indent()

        return "".join(parts)

    def _generate_interface(self, node: InterfaceNode) -> str:
        """生成接口定义（优化版）

        Args:
            node: 接口节点

        Returns:
            接口定义字符串
        """
        # 使用列表构建字符串（优化）
        parts = [f"class {node.name}(abc.ABC):"]

        # 增加缩进
        self._increase_indent()

        # 生成接口方法
        if node.methods:
            for method in node.methods:
                method_code = self._generate_method(method)
                if method_code:
                    parts.append(f"\n{self._indent()}{method_code}")
        else:
            parts.append(f"\n{self._indent()}pass")

        # 减少缩进
        self._decrease_indent()

        return "".join(parts)

    def _generate_method(self, node: MethodNode) -> str:
        """生成方法定义（优化版）

        Args:
            node: 方法节点

        Returns:
            方法定义字符串
        """
        # 使用列表构建字符串（优化）
        parts = []

        # 添加装饰器
        if node.is_static:
            parts.append("@staticmethod\n")
        elif node.is_constructor:
            # 构造函数使用__init__
            method_name = "__init__"
        else:
            method_name = node.name

        # 构建方法定义
        if node.is_constructor:
            # 构造函数
            params = ["sel"] + node.params
            param_str = ", ".join(params)
            parts.append(f"def {method_name}({param_str}):")
        else:
            # 普通方法
            params = ["sel"] + node.params if not node.is_static else node.params
            param_str = ", ".join(params)
            parts.append(f"def {method_name}({param_str}):")

        # 增加缩进
        self._increase_indent()

        # 生成方法体
        if node.body:
            for stmt in node.body:
                stmt_code = self.generate(stmt)
                if stmt_code:
                    parts.append(f"\n{self._indent()}{stmt_code}")
        else:
            parts.append(f"\n{self._indent()}pass")

        # 减少缩进
        self._decrease_indent()

        return "".join(parts)

    def _generate_property(self, node: PropertyNode) -> str:
        """生成属性定义（优化版）

        Args:
            node: 属性节点

        Returns:
            属性定义字符串
        """
        if node.is_static:
            # 静态属性
            if node.value is not None:
                value = self.generate(node.value)
                return f"{node.name} = {value}"
            else:
                return node.name
        else:
            # 实例属性
            if node.value is not None:
                value = self.generate(node.value)
                return f"self.{node.name} = {value}"
            else:
                return f"self.{node.name} = None"

    def _generate_new(self, node: NewNode) -> str:
        """生成对象创建表达式（优化版）

        Args:
            node: 新建对象节点

        Returns:
            对象创建表达式字符串
        """
        if node.args:
            # 生成参数列表（优化）
            arg_parts = []
            for arg in node.args:
                arg_parts.append(self.generate(arg))
            args_str = ", ".join(arg_parts)
            return f"{node.class_name}({args_str})"
        else:
            return f"{node.class_name}()"

    def _generate_this(self, node: ThisNode) -> str:
        """生成this表达式（优化版）

        Args:
            node: this节点

        Returns:
            this表达式字符串
        """
        return "sel"

    def _generate_super(self, node: SuperNode) -> str:
        """生成super表达式（优化版）

        Args:
            node: super节点

        Returns:
            super表达式字符串
        """
        return "super()"

    def _generate_export(self, node: ExportNode) -> str:
        """生成导出语句（优化版）

        Args:
            node: 导出节点

        Returns:
            导出语句字符串
        """
        # 构建导出列表（优化）
        export_list = []
        for name in node.names:
            if name in node.aliases:
                export_list.append(f"'{name}' as '{node.aliases[name]}'")
            else:
                export_list.append(f"'{name}'")

        exports_str = ", ".join(export_list)
        return f"__all__ = [{exports_str}]"

    # ============ 其他节点生成方法 ============

    def _generate_list(self, node: ListNode) -> str:
        """生成列表表达式（优化版）

        Args:
            node: 列表节点

        Returns:
            列表表达式字符串
        """
        if node.elements:
            # 生成元素列表（优化）
            elem_parts = []
            for elem in node.elements:
                elem_parts.append(self.generate(elem))
            elems_str = ", ".join(elem_parts)
            return f"[{elems_str}]"
        else:
            return "[]"

    def _generate_dict(self, node: DictNode) -> str:
        """生成字典表达式（优化版）

        Args:
            node: 字典节点

        Returns:
            字典表达式字符串
        """
        if node.items:
            # 生成键值对列表（优化）
            item_parts = []
            for key, value in node.items.items():
                key_str = self.generate(key)
                value_str = self.generate(value)
                item_parts.append(f"{key_str}: {value_str}")
            items_str = ", ".join(item_parts)
            return f"{{{items_str}}}"
        else:
            return "{}"

    def _generate_repeat(self, node: RepeatNode) -> str:
        """生成repeat循环语句（优化版）

        Args:
            node: repeat循环节点

        Returns:
            repeat循环语句字符串
        """
        # repeat循环转换为for循环
        count = self.generate(node.count)
        return f"for _ in range({count}):"

    # ============ 性能优化辅助方法 ============

    @functools.lru_cache(maxsize=128)
    def _get_method_name(self, node_type: str) -> str:
        """获取方法名（带缓存）

        Args:
            node_type: 节点类型名

        Returns:
            方法名
        """
        return f"_generate_{node_type.replace('Node', '').lower()}"

    def _optimized_generate(self, node: ASTNode) -> str:
        """优化版的generate方法（实验性）

        使用更高效的方法分发和字符串构建

        Args:
            node: AST节点

        Returns:
            生成的Python代码字符串
        """
        # 使用类型映射代替getattr
        method = self._method_cache.get(type(node))
        if method is None:
            # 根据类型直接分派
            if isinstance(node, NumberNode):
                method = self._generate_number
            elif isinstance(node, StringNode):
                method = self._generate_string
            elif isinstance(node, IdentifierNode):
                method = self._generate_identifier
            elif isinstance(node, BinaryOpNode):
                method = self._generate_binaryop
            elif isinstance(node, UnaryOpNode):
                method = self._generate_unaryop
            elif isinstance(node, FunctionCallNode):
                method = self._generate_functioncall
            elif isinstance(node, VarDefNode):
                method = self._generate_vardef
            elif isinstance(node, AssignNode):
                method = self._generate_assign
            elif isinstance(node, IfNode):
                method = self._generate_if
            elif isinstance(node, WhileNode):
                method = self._generate_while
            elif isinstance(node, ForNode):
                method = self._generate_for
            elif isinstance(node, ReturnNode):
                method = self._generate_return
            elif isinstance(node, ClassNode):
                method = self._generate_class
            elif isinstance(node, MethodNode):
                method = self._generate_method
            elif isinstance(node, PropertyNode):
                method = self._generate_property
            elif isinstance(node, NewNode):
                method = self._generate_new
            elif isinstance(node, ThisNode):
                method = self._generate_this
            elif isinstance(node, SuperNode):
                method = self._generate_super
            elif isinstance(node, InterfaceNode):
                method = self._generate_interface
            elif isinstance(node, ExportNode):
                method = self._generate_export
            elif isinstance(node, ImportNode):
                method = self._generate_import
            elif isinstance(node, FromImportNode):
                method = self._generate_fromimport
            elif isinstance(node, MemberAccessNode):
                method = self._generate_memberaccess
            elif isinstance(node, IndexNode):
                method = self._generate_index
            elif isinstance(node, ListNode):
                method = self._generate_list
            elif isinstance(node, DictNode):
                method = self._generate_dict
            elif isinstance(node, RepeatNode):
                method = self._generate_repeat
            elif isinstance(node, TryNode):
                method = self._generate_try
            elif isinstance(node, ExceptNode):
                method = self._generate_except
            elif isinstance(node, RaiseNode):
                method = self._generate_raise
            elif isinstance(node, BlockNode):
                method = self._generate_block
            elif isinstance(node, ProgramNode):
                method = self._generate_program
            else:
                raise CodegenError(f"未知节点类型: {type(node).__name__}")

            # 缓存方法
            self._method_cache[type(node)] = method

        # 调用方法
        return method(node)
