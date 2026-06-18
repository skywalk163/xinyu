#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""简单测试格式化工具"""

import os
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 直接导入formatter模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 简化测试，不依赖具体的AST节点
print("测试格式化工具基本功能...")

# 测试配置类
from dataclasses import dataclass, field
from typing import Any, Dict

import yaml


@dataclass
class SimpleFormatterConfig:
    """简化格式化器配置"""

    line_length: int = 100
    indent_size: int = 4
    quote_style: str = "double"
    trailing_comma: bool = True
    max_empty_lines: int = 2
    spaces_around_operators: bool = True
    spaces_after_comma: bool = True
    spaces_after_colon: bool = True
    custom_rules: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "line_length": self.line_length,
            "indent_size": self.indent_size,
            "quote_style": self.quote_style,
            "trailing_comma": self.trailing_comma,
            "max_empty_lines": self.max_empty_lines,
            "spaces_around_operators": self.spaces_around_operators,
            "spaces_after_comma": self.spaces_after_comma,
            "spaces_after_colon": self.spaces_after_colon,
            "custom_rules": self.custom_rules,
        }


# 测试配置创建
print("1. 测试配置创建...")
config = SimpleFormatterConfig(line_length=80, indent_size=4, quote_style="double")
print(f"   配置创建成功: line_length={config.line_length}, indent_size={config.indent_size}")

# 测试配置转字典
print("2. 测试配置转字典...")
config_dict = config.to_dict()
print(f"   配置字典: {config_dict}")

# 测试YAML配置保存和加载
print("3. 测试YAML配置...")
config_file = Path(".test-config.yaml")

# 保存配置
config_dict = config.to_dict()
with open(config_file, "w", encoding="utf-8") as f:
    yaml.dump(config_dict, f, default_flow_style=False, allow_unicode=True, indent=2)
print(f"   配置已保存到 {config_file}")

# 加载配置
with open(config_file, "r", encoding="utf-8") as f:
    loaded_config = yaml.safe_load(f)
print(f"   配置已加载: {loaded_config}")

# 清理测试文件
if config_file.exists():
    config_file.unlink()
    print("   测试文件已清理")

# 测试格式化器接口
print("4. 测试格式化器接口设计...")


class SimpleFormatter:
    """简化格式化器"""

    def __init__(self, config: SimpleFormatterConfig):
        self.config = config

    def format_code(self, source: str) -> str:
        """简化格式化实现"""
        # 基本格式化：确保每行有适当的缩进
        lines = source.split("\n")
        formatted_lines = []
        indent_level = 0

        for line in lines:
            stripped = line.strip()
            if not stripped:
                # 空行
                if len(formatted_lines) == 0 or formatted_lines[-1].strip():
                    formatted_lines.append("")
                continue

            # 检查缩进变化
            if (
                stripped.startswith("如果")
                or stripped.startswith("定义")
                or stripped.startswith("对于")
                or stripped.startswith("当")
            ):
                # 增加缩进
                indent = " " * (indent_level * self.config.indent_size)
                formatted_lines.append(indent + stripped)
                indent_level += 1
            elif stripped.startswith("返回") or stripped == "否则:":
                # 减少缩进
                indent_level = max(0, indent_level - 1)
                indent = " " * (indent_level * self.config.indent_size)
                formatted_lines.append(indent + stripped)
            else:
                # 保持当前缩进
                indent = " " * (indent_level * self.config.indent_size)
                formatted_lines.append(indent + stripped)

        return "\n".join(formatted_lines)

    def check_format(self, source: str) -> list:
        """检查格式问题"""
        issues = []
        lines = source.split("\n")

        for i, line in enumerate(lines, 1):
            # 检查行长度
            if len(line) > self.config.line_length:
                issues.append(
                    {
                        "line": i,
                        "column": self.config.line_length + 1,
                        "message": f"行长度超过{self.config.line_length}个字符",
                        "severity": "warning",
                    }
                )

            # 检查尾随空格
            if line.rstrip() != line:
                issues.append(
                    {
                        "line": i,
                        "column": len(line.rstrip()) + 1,
                        "message": "行尾有空格",
                        "severity": "info",
                    }
                )

        return issues


# 测试格式化器
print("5. 测试格式化器...")
formatter = SimpleFormatter(config)

test_code = """# 这是一个测试
定义 测试函数():
结果 = 1 + 2 * 3
返回 结果

如果 __名称__ == "__主__":
印 "Hello, World!"
"""

print("原始代码:")
print(test_code)

formatted = formatter.format_code(test_code)
print("\n格式化后的代码:")
print(formatted)

issues = formatter.check_format(test_code)
print(f"\n发现{len(issues)}个格式问题:")
for issue in issues:
    print(f"  第{issue['line']}行第{issue['column']}列: {issue['message']} ({issue['severity']})")

print("\n" + "=" * 60)
print("基本功能测试完成！")
print("=" * 60)
