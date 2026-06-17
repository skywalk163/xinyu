#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""简单的心语代码格式化工具

基于正则表达式的格式化，不依赖完整的AST解析。
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import yaml


class SimpleXinyuFormatter:
    """简单的心语代码格式化器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self.default_config()
        self.indent_size = self.config.get('indent_size', 4)
        self.line_length = self.config.get('line_length', 100)
        self.quote_style = self.config.get('quote_style', 'double')
    
    @staticmethod
    def default_config() -> Dict[str, Any]:
        """默认配置"""
        return {
            'line_length': 100,
            'indent_size': 4,
            'quote_style': 'double',
            'trailing_comma': True,
            'max_empty_lines': 2,
            'spaces_around_operators': True,
            'spaces_after_comma': True,
            'spaces_after_colon': True,
        }
    
    def format_code(self, source: str) -> str:
        """格式化心语源代码"""
        lines = source.split('\n')
        formatted_lines = []
        indent_level = 0
        in_multiline_string = False
        multiline_string_indent = 0
        
        for line in lines:
            stripped = line.strip()
            
            # 跳过空行
            if not stripped:
                # 限制连续空行数量
                if (not formatted_lines or 
                    formatted_lines[-1].strip() != '' or 
                    self.count_trailing_empty_lines(formatted_lines) < self.config.get('max_empty_lines', 2)):
                    formatted_lines.append('')
                continue
            
            # 处理多行字符串
            if in_multiline_string:
                if stripped.endswith('"""') or stripped.endswith("'''"):
                    in_multiline_string = False
                formatted_lines.append(' ' * multiline_string_indent + stripped)
                continue
            elif stripped.startswith('"""') or stripped.startswith("'''"):
                in_multiline_string = True
                multiline_string_indent = indent_level * self.indent_size
                formatted_lines.append(' ' * multiline_string_indent + stripped)
                continue
            
            # 计算缩进
            current_indent = indent_level * self.indent_size
            
            # 处理行尾注释
            if '#' in stripped:
                code_part, comment_part = stripped.split('#', 1)
                stripped = code_part.rstrip() + ' #' + comment_part
            
            # 应用基本格式化规则
            formatted_line = self._format_line(stripped, current_indent)
            
            # 调整缩进级别
            indent_level = self._adjust_indent_level(indent_level, stripped)
            
            formatted_lines.append(formatted_line)
        
        # 确保文件以换行符结束
        result = '\n'.join(formatted_lines)
        if not result.endswith('\n'):
            result += '\n'
        
        return result
    
    def _format_line(self, line: str, indent: int) -> str:
        """格式化单行代码"""
        # 添加缩进
        formatted = ' ' * indent + line
        
        # 在操作符周围添加空格
        if self.config.get('spaces_around_operators', True):
            formatted = self._add_spaces_around_operators(formatted)
        
        # 在逗号后添加空格
        if self.config.get('spaces_after_comma', True):
            formatted = self._add_spaces_after_commas(formatted)
        
        # 在冒号后添加空格
        if self.config.get('spaces_after_colon', True):
            formatted = self._add_spaces_after_colons(formatted)
        
        # 统一引号风格
        if self.quote_style == 'single':
            formatted = self._convert_to_single_quotes(formatted)
        elif self.quote_style == 'double':
            formatted = self._convert_to_double_quotes(formatted)
        
        return formatted
    
    def _add_spaces_around_operators(self, line: str) -> str:
        """在操作符周围添加空格"""
        operators = ['=', '==', '!=', '<', '>', '<=', '>=', '+', '-', '*', '/', '%', '+=', '-=', '*=', '/=']
        
        for op in operators:
            pattern = rf'(\S)({re.escape(op)})(\S)'
            replacement = rf'\1 {op} \3'
            line = re.sub(pattern, replacement, line)
        
        return line
    
    def _add_spaces_after_commas(self, line: str) -> str:
        """在逗号后添加空格"""
        # 匹配逗号后没有空格的情况，但排除字符串内的逗号
        pattern = r',(\S)'
        replacement = r', \1'
        line = re.sub(pattern, replacement, line)
        return line
    
    def _add_spaces_after_colons(self, line: str) -> str:
        """在冒号后添加空格"""
        # 匹配冒号后没有空格的情况，但排除切片语法和字典中的冒号
        pattern = r':(\S)(?![:\d])'  # 排除 ::
        replacement = r': \1'
        line = re.sub(pattern, replacement, line)
        return line
    
    def _convert_to_single_quotes(self, line: str) -> str:
        """将双引号转换为单引号"""
        # 简单的转换，不处理转义字符
        line = line.replace('"', "'")
        return line
    
    def _convert_to_double_quotes(self, line: str) -> str:
        """将单引号转换为双引号"""
        # 简单的转换，不处理转义字符
        line = line.replace("'", '"')
        return line
    
    def _adjust_indent_level(self, current_level: int, line: str) -> int:
        """根据当前行调整缩进级别"""
        stripped = line.strip()
        
        # 增加缩进的情况
        if (stripped.startswith('定义') or 
            stripped.startswith('如果') or 
            stripped.startswith('否则') or
            stripped.startswith('对于') or
            stripped.startswith('当') or
            stripped.startswith('重复') or
            stripped.endswith(':')):
            return current_level + 1
        
        # 减少缩进的情况
        if (stripped.startswith('返回') or
            stripped.startswith('结束') or
            stripped == '否则:'):
            return max(0, current_level - 1)
        
        return current_level
    
    def count_trailing_empty_lines(self, lines: List[str]) -> int:
        """计算末尾连续空行数量"""
        count = 0
        for line in reversed(lines):
            if line.strip() == '':
                count += 1
            else:
                break
        return count
    
    def check_format(self, source: str) -> List[Dict[str, Any]]:
        """检查代码格式问题"""
        issues = []
        lines = source.split('\n')
        
        for i, line in enumerate(lines, 1):
            # 检查行长度
            if len(line) > self.line_length:
                issues.append({
                    'line': i,
                    'column': self.line_length + 1,
                    'message': f'行长度超过{self.line_length}个字符',
                    'severity': 'warning'
                })
            
            # 检查尾随空格
            if line.rstrip() != line:
                issues.append({
                    'line': i,
                    'column': len(line.rstrip()) + 1,
                    'message': '行尾有空格',
                    'severity': 'info'
                })
            
            # 检查制表符
            if '\t' in line:
                issues.append({
                    'line': i,
                    'column': line.find('\t') + 1,
                    'message': '使用制表符而不是空格',
                    'severity': 'warning'
                })
        
        return issues
    
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


def main():
    """命令行入口点"""
    import argparse
    
    parser = argparse.ArgumentParser(description='简单心语代码格式化工具')
    parser.add_argument('files', nargs='+', help='要格式化的文件或目录')
    parser.add_argument('--check', action='store_true', help='只检查不修改')
    parser.add_argument('--config', help='配置文件路径')
    parser.add_argument('--in-place', '-i', action='store_true', help='直接修改文件')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    # 加载配置
    config = SimpleXinyuFormatter.default_config()
    if args.config and Path(args.config).exists():
        try:
            with open(args.config, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f) or {}
                config.update(user_config)
        except Exception as e:
            print(f"警告: 加载配置文件失败: {e}", file=sys.stderr)
    
    # 创建格式化器
    formatter = SimpleXinyuFormatter(config)
    
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
                with open(file_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                
                issues = formatter.check_format(source)
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
                    with open(file_path, 'r', encoding='utf-8') as f:
                        source = f.read()
                    
                    formatted = formatter.format_code(source)
                    print(formatted)


if __name__ == '__main__':
    main()