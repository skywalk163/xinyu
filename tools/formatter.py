# -*- coding: utf-8 -*-
"""心语代码格式化工具

提供心语源代码的格式化功能：
- 代码格式化
- 格式检查
- 批量处理
- 配置支持
"""

import os
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Protocol, Union
import yaml

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.compiler import XinyuCompiler
from src.parser.ast_nodes import ASTNode

# 尝试相对导入，如果失败则尝试绝对导入
try:
    from .format_engine import FormatEngine, FormatResult
except ImportError:
    from format_engine import FormatEngine, FormatResult


class Severity(str, Enum):
    """问题严重程度"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class FormatIssue:
    """格式问题"""
    line: int
    column: int
    message: str
    severity: Severity
    fix_suggestion: Optional[str] = None
    
    def __str__(self) -> str:
        return f"{self.severity.value}:{self.line}:{self.column}: {self.message}"


@dataclass
class FormatterConfig:
    """格式化器配置"""
    line_length: int = 100
    indent_size: int = 4
    quote_style: str = "double"  # "single" 或 "double"
    trailing_comma: bool = True
    max_empty_lines: int = 2
    spaces_around_operators: bool = True
    spaces_after_comma: bool = True
    spaces_after_colon: bool = True
    custom_rules: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_yaml(cls, yaml_path: Union[str, Path]) -> 'FormatterConfig':
        """从YAML文件加载配置"""
        yaml_path = Path(yaml_path)
        if not yaml_path.exists():
            return cls()
        
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f) or {}
        
        # 创建配置实例
        config = cls()
        
        # 更新配置属性
        for key, value in config_data.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        return config
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'line_length': self.line_length,
            'indent_size': self.indent_size,
            'quote_style': self.quote_style,
            'trailing_comma': self.trailing_comma,
            'max_empty_lines': self.max_empty_lines,
            'spaces_around_operators': self.spaces_around_operators,
            'spaces_after_comma': self.spaces_after_comma,
            'spaces_after_colon': self.spaces_after_colon,
            'custom_rules': self.custom_rules
        }
    
    def to_yaml(self, yaml_path: Union[str, Path]) -> None:
        """保存配置到YAML文件"""
        config_dict = self.to_dict()
        
        yaml_path = Path(yaml_path)
        yaml_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_dict, f, default_flow_style=False, allow_unicode=True, indent=2)


class FormatContext:
    """格式化上下文"""
    def __init__(self, config: FormatterConfig, indent_level: int = 0):
        self.config = config
        self.indent_level = indent_level
        self.current_line = 1
        self.current_column = 1
        self.issues: List[FormatIssue] = []
    
    def indent(self) -> 'FormatContext':
        """增加缩进级别"""
        return FormatContext(self.config, self.indent_level + 1)
    
    def add_issue(self, issue: FormatIssue) -> None:
        """添加格式问题"""
        self.issues.append(issue)


class IFormatRule(Protocol):
    """格式化规则接口"""
    def apply(self, node: ASTNode, context: FormatContext) -> ASTNode:
        """应用格式化规则"""
        ...
    
    def get_description(self) -> str:
        """获取规则描述"""
        ...


class IFormatter(Protocol):
    """格式化器接口"""
    def format(self, source: str) -> str:
        """格式化源代码"""
        ...
    
    def check(self, source: str) -> List[FormatIssue]:
        """检查代码格式问题"""
        ...
    
    def format_file(self, filepath: Path) -> bool:
        """格式化文件并保存"""
        ...


class XinyuFormatter:
    """心语代码格式化器"""
    
    def __init__(self, config: Optional[FormatterConfig] = None):
        self.config = config or FormatterConfig()
        self.engine = FormatEngine(self.config.to_dict())
    
    def format_code(self, source: str) -> str:
        """格式化心语源代码"""
        result = self.engine.format(source)
        
        # 如果有错误，打印警告但继续
        errors = [issue for issue in result.issues if issue.get('severity') == 'error']
        if errors:
            print(f"格式化警告: 发现{len(errors)}个错误", file=sys.stderr)
            for error in errors:
                print(f"  第{error['line']}行第{error['column']}列: {error['message']}", file=sys.stderr)
        
        return result.formatted_code
    
    def check_format(self, source: str) -> List[FormatIssue]:
        """检查代码格式问题"""
        issues = self.engine.check(source)
        
        # 转换为FormatIssue对象
        format_issues = []
        for issue in issues:
            severity_map = {
                'error': Severity.ERROR,
                'warning': Severity.WARNING,
                'info': Severity.INFO
            }
            
            format_issues.append(FormatIssue(
                line=issue.get('line', 1),
                column=issue.get('column', 1),
                message=issue.get('message', '未知问题'),
                severity=severity_map.get(issue.get('severity', 'info'), Severity.INFO),
                fix_suggestion=issue.get('fix_suggestion')
            ))
        
        return format_issues
    
    def apply_format(self, filepath: Path) -> bool:
        """格式化文件并保存"""
        try:
            # 读取文件
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()
            
            # 格式化代码
            formatted = self.format_code(source)
            
            # 如果代码有变化，保存文件
            if formatted != source:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(formatted)
                return True
            return False
            
        except Exception as e:
            print(f"格式化文件失败 {filepath}: {e}", file=sys.stderr)
            return False


class IndentationRule:
    """缩进规则"""
    
    def apply(self, node: ASTNode, context: FormatContext) -> ASTNode:
        """应用缩进规则"""
        # 这里需要实现具体的缩进逻辑
        # 目前返回原始节点
        return node
    
    def get_description(self) -> str:
        return "确保正确的缩进级别"


class LineLengthRule:
    """行长度规则"""
    
    def apply(self, node: ASTNode, context: FormatContext) -> ASTNode:
        """应用行长度规则"""
        # 检查行长度
        # 这里需要实现具体的行长度检查逻辑
        return node
    
    def get_description(self) -> str:
        return "确保行长度不超过限制"


class QuoteStyleRule:
    """引号风格规则"""
    
    def apply(self, node: ASTNode, context: FormatContext) -> ASTNode:
        """应用引号风格规则"""
        # 统一引号风格
        # 这里需要实现具体的引号风格转换逻辑
        return node
    
    def get_description(self) -> str:
        return "统一字符串引号风格"


class SpacingRule:
    """空格规则"""
    
    def apply(self, node: ASTNode, context: FormatContext) -> ASTNode:
        """应用空格规则"""
        # 确保操作符周围的空格
        # 这里需要实现具体的空格处理逻辑
        return node
    
    def get_description(self) -> str:
        return "确保操作符和标点符号周围的空格"


class EmptyLineRule:
    """空行规则"""
    
    def apply(self, node: ASTNode, context: FormatContext) -> ASTNode:
        """应用空行规则"""
        # 限制连续空行数量
        # 这里需要实现具体的空行处理逻辑
        return node
    
    def get_description(self) -> str:
        return "限制连续空行数量"


class TrailingCommaRule:
    """尾随逗号规则"""
    
    def apply(self, node: ASTNode, context: FormatContext) -> ASTNode:
        """应用尾随逗号规则"""
        # 添加或移除尾随逗号
        # 这里需要实现具体的尾随逗号处理逻辑
        return node
    
    def get_description(self) -> str:
        return "在多行结构中添加尾随逗号"


def format_command():
    """格式化命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='心语代码格式化工具')
    parser.add_argument('files', nargs='+', help='要格式化的文件或目录')
    parser.add_argument('--check', action='store_true', help='只检查不修改')
    parser.add_argument('--config', help='配置文件路径')
    parser.add_argument('--in-place', '-i', action='store_true', help='直接修改文件')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    # 加载配置
    config = FormatterConfig()
    if args.config:
        config = FormatterConfig.from_yaml(args.config)
    
    # 创建格式化器
    formatter = XinyuFormatter(config)
    
    # 处理文件
    for file_pattern in args.files:
        path = Path(file_pattern)
        
        if path.is_dir():
            # 处理目录
            files = list(path.rglob('*.xinyu'))
        else:
            # 处理文件
            files = [path] if path.exists() else []
        
        for file_path in files:
            if args.check:
                # 只检查格式
                issues = formatter.check_format(file_path.read_text(encoding='utf-8'))
                if issues:
                    print(f"{file_path}:")
                    for issue in issues:
                        print(f"  {issue}")
            else:
                # 格式化文件
                if args.in_place:
                    changed = formatter.apply_format(file_path)
                    if changed:
                        print(f"格式化: {file_path}")
                    elif args.verbose:
                        print(f"无变化: {file_path}")
                else:
                    # 输出格式化后的代码
                    source = file_path.read_text(encoding='utf-8')
                    formatted = formatter.format_code(source)
                    print(formatted)


if __name__ == '__main__':
    format_command()