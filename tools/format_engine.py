# -*- coding: utf-8 -*-
"""心语代码格式化引擎

提供AST级别的代码格式化功能，包括：
- AST遍历和修改
- 格式化规则应用
- 源代码生成
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union, Callable
from pathlib import Path

from src.parser.ast_nodes import (
    ASTNode, NumberNode, StringNode, IdentifierNode,
    BinaryOpNode, UnaryOpNode, FunctionCallNode, AssignNode,
    FunctionDefNode, ReturnNode, IfNode, WhileNode,
    ForNode, ListNode, DictNode
)


@dataclass
class FormatResult:
    """格式化结果"""
    formatted_code: str
    issues: List[Dict[str, Any]] = field(default_factory=list)
    changed: bool = False


class ASTFormatter:
    """AST格式化器"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.indent_size = config.get('indent_size', 4)
        self.line_length = config.get('line_length', 100)
        self.quote_style = config.get('quote_style', 'double')
        self.current_indent = 0
        self.output_lines = []
        self.current_line = ''
        self.issues = []
    
    def format_ast(self, ast: ASTNode) -> FormatResult:
        """格式化AST节点"""
        self.output_lines = []
        self.current_line = ''
        self.current_indent = 0
        self.issues = []
        
        self._visit_node(ast)
        
        # 添加最后一行
        if self.current_line:
            self.output_lines.append(self.current_line)
        
        formatted_code = '\n'.join(self.output_lines)
        
        # 应用后处理规则
        formatted_code = self._post_process(formatted_code)
        
        return FormatResult(
            formatted_code=formatted_code,
            issues=self.issues,
            changed=True  # 暂时假设总是有变化
        )
    
    def _visit_node(self, node: ASTNode) -> None:
        """访问AST节点"""
        node_type = type(node).__name__
        visitor_method = getattr(self, f'_visit_{node_type}', None)
        
        if visitor_method:
            visitor_method(node)
        else:
            # 默认处理：使用节点的字符串表示
            self._add_to_line(str(node))
    
    def _visit_NumberNode(self, node: NumberNode) -> None:
        """访问数字节点"""
        self._add_to_line(str(node.value))
    
    def _visit_StringNode(self, node: StringNode) -> None:
        """访问字符串节点"""
        if self.quote_style == 'single':
            self._add_to_line(f"'{node.value}'")
        else:
            self._add_to_line(f'"{node.value}"')
    
    def _visit_IdentifierNode(self, node: IdentifierNode) -> None:
        """访问标识符节点"""
        self._add_to_line(node.name)
    
    def _visit_BinaryOpNode(self, node: BinaryOpNode) -> None:
        """访问二元操作节点"""
        self._visit_node(node.left)
        self._add_to_line(f' {node.operator} ')
        self._visit_node(node.right)
    
    def _visit_UnaryOpNode(self, node: UnaryOpNode) -> None:
        """访问一元操作节点"""
        self._add_to_line(node.operator)
        self._visit_node(node.operand)
    
    def _visit_FunctionCallNode(self, node: 'FunctionCallNode') -> None:
        """访问函数调用节点"""
        self._visit_node(node.function)
        self._add_to_line('(')
        
        for i, arg in enumerate(node.arguments):
            if i > 0:
                self._add_to_line(', ')
            self._visit_node(arg)
        
        self._add_to_line(')')
    
    def _visit_AssignNode(self, node: 'AssignNode') -> None:
        """访问赋值节点"""
        self._visit_node(node.target)
        self._add_to_line(' = ')
        self._visit_node(node.value)
    
    def _visit_FunctionDefNode(self, node: 'FunctionDefNode') -> None:
        """访问函数定义节点"""
        self._add_to_line(f'定义 {node.name}(')
        
        for i, param in enumerate(node.parameters):
            if i > 0:
                self._add_to_line(', ')
            self._add_to_line(param)
        
        self._add_to_line('):')
        self._new_line()
        self._increase_indent()
        
        for stmt in node.body:
            self._visit_node(stmt)
            self._new_line()
        
        self._decrease_indent()
    
    def _visit_ReturnNode(self, node: 'ReturnNode') -> None:
        """访问返回节点"""
        self._add_to_line('返回 ')
        if node.value:
            self._visit_node(node.value)
    
    def _visit_IfNode(self, node: 'IfNode') -> None:
        """访问条件节点"""
        self._add_to_line('如果 ')
        self._visit_node(node.condition)
        self._add_to_line(':')
        self._new_line()
        self._increase_indent()
        
        for stmt in node.then_branch:
            self._visit_node(stmt)
            self._new_line()
        
        self._decrease_indent()
        
        if node.else_branch:
            self._add_to_line('否则:')
            self._new_line()
            self._increase_indent()
            
            for stmt in node.else_branch:
                self._visit_node(stmt)
                self._new_line()
            
            self._decrease_indent()
    
    def _visit_WhileNode(self, node: 'WhileNode') -> None:
        """访问循环节点"""
        self._add_to_line('当 ')
        self._visit_node(node.condition)
        self._add_to_line(':')
        self._new_line()
        self._increase_indent()
        
        for stmt in node.body:
            self._visit_node(stmt)
            self._new_line()
        
        self._decrease_indent()
    
    def _visit_ForNode(self, node: 'ForNode') -> None:
        """访问for循环节点"""
        self._add_to_line(f'对于 {node.variable} 在 ')
        self._visit_node(node.iterable)
        self._add_to_line(':')
        self._new_line()
        self._increase_indent()
        
        for stmt in node.body:
            self._visit_node(stmt)
            self._new_line()
        
        self._decrease_indent()
    
    def _visit_ListNode(self, node: 'ListNode') -> None:
        """访问列表节点"""
        self._add_to_line('[')
        
        for i, element in enumerate(node.elements):
            if i > 0:
                self._add_to_line(', ')
            self._visit_node(element)
        
        self._add_to_line(']')
    
    def _visit_DictNode(self, node: 'DictNode') -> None:
        """访问字典节点"""
        self._add_to_line('{')
        
        for i, (key, value) in enumerate(node.items):
            if i > 0:
                self._add_to_line(', ')
            self._visit_node(key)
            self._add_to_line(': ')
            self._visit_node(value)
        
        self._add_to_line('}')
    
    def _add_to_line(self, text: str) -> None:
        """添加文本到当前行"""
        self.current_line += text
        
        # 检查行长度
        if len(self.current_line) > self.line_length:
            self.issues.append({
                'type': 'line_too_long',
                'line': len(self.output_lines) + 1,
                'column': len(self.current_line),
                'message': f'行长度超过{self.line_length}个字符',
                'severity': 'warning'
            })
    
    def _new_line(self) -> None:
        """开始新行"""
        if self.current_line:
            self.output_lines.append(self.current_line)
            self.current_line = ''
        
        # 添加缩进
        indent = ' ' * (self.current_indent * self.indent_size)
        self.current_line = indent
    
    def _increase_indent(self) -> None:
        """增加缩进级别"""
        self.current_indent += 1
    
    def _decrease_indent(self) -> None:
        """减少缩进级别"""
        if self.current_indent > 0:
            self.current_indent -= 1
    
    def _post_process(self, code: str) -> str:
        """后处理格式化后的代码"""
        lines = code.split('\n')
        processed_lines = []
        
        # 移除多余的空行
        empty_line_count = 0
        max_empty_lines = self.config.get('max_empty_lines', 2)
        
        for line in lines:
            if line.strip() == '':
                empty_line_count += 1
                if empty_line_count <= max_empty_lines:
                    processed_lines.append(line)
            else:
                empty_line_count = 0
                processed_lines.append(line)
        
        # 确保文件以换行符结束
        result = '\n'.join(processed_lines)
        if not result.endswith('\n'):
            result += '\n'
        
        return result


class FormatRule:
    """格式化规则基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def apply(self, ast: ASTNode, formatter: ASTFormatter) -> ASTNode:
        """应用格式化规则"""
        return ast
    
    def get_description(self) -> str:
        """获取规则描述"""
        return self.__class__.__name__


class IndentationRule(FormatRule):
    """缩进规则"""
    
    def apply(self, ast: ASTNode, formatter: ASTFormatter) -> ASTNode:
        """确保正确的缩进"""
        # 缩进规则已经在ASTFormatter中实现
        return ast
    
    def get_description(self) -> str:
        return "确保正确的缩进级别"


class LineLengthRule(FormatRule):
    """行长度规则"""
    
    def apply(self, ast: ASTNode, formatter: ASTFormatter) -> ASTNode:
        """检查行长度"""
        # 行长度检查已经在ASTFormatter._add_to_line中实现
        return ast
    
    def get_description(self) -> str:
        return f"确保行长度不超过{self.config.get('line_length', 100)}个字符"


class QuoteStyleRule(FormatRule):
    """引号风格规则"""
    
    def apply(self, ast: ASTNode, formatter: ASTFormatter) -> ASTNode:
        """统一引号风格"""
        # 引号风格已经在ASTFormatter._visit_StringNode中实现
        return ast
    
    def get_description(self) -> str:
        quote_style = self.config.get('quote_style', 'double')
        return f"统一字符串使用{quote_style}引号"


class SpacingRule(FormatRule):
    """空格规则"""
    
    def apply(self, ast: ASTNode, formatter: ASTFormatter) -> ASTNode:
        """确保操作符和标点符号周围的空格"""
        # 空格规则已经在各个visit方法中实现
        return ast
    
    def get_description(self) -> str:
        return "确保操作符和标点符号周围的空格"


class FormatEngine:
    """格式化引擎"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.rules = self._load_rules()
        self.formatter = ASTFormatter(config)
    
    def _load_rules(self) -> List[FormatRule]:
        """加载格式化规则"""
        rules = [
            IndentationRule(self.config),
            LineLengthRule(self.config),
            QuoteStyleRule(self.config),
            SpacingRule(self.config),
        ]
        
        # 添加自定义规则
        custom_rules = self.config.get('custom_rules', {})
        if custom_rules.get('trailing_comma', False):
            from .formatter import TrailingCommaRule
            rules.append(TrailingCommaRule())
        
        return rules
    
    def format(self, source: str) -> FormatResult:
        """格式化源代码"""
        try:
            # 解析源代码为AST
            from src.core.compiler import XinyuCompiler
            compiler = XinyuCompiler()
            ast = compiler.parse(source)
            
            # 应用格式化规则
            formatted_ast = ast
            for rule in self.rules:
                formatted_ast = rule.apply(formatted_ast, self.formatter)
            
            # 生成格式化后的代码
            result = self.formatter.format_ast(formatted_ast)
            
            return result
            
        except Exception as e:
            # 如果解析失败，返回错误
            return FormatResult(
                formatted_code=source,
                issues=[{
                    'type': 'parse_error',
                    'line': 1,
                    'column': 1,
                    'message': f'解析错误: {e}',
                    'severity': 'error'
                }],
                changed=False
            )
    
    def check(self, source: str) -> List[Dict[str, Any]]:
        """检查代码格式问题"""
        result = self.format(source)
        return result.issues