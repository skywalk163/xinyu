# -*- coding: utf-8 -*-
"""多轨制执行系统

支持多种执行轨道：
1. 数学轨（Math Track）- 使用 $() 包裹，支持数学表达式
2. Python轨（Python Track）- 使用 {{}} 包裹，直接执行Python代码
3. SQL轨（SQL Track）- 使用 SQL"" 包裹，执行SQL查询
4. Shell轨（Shell Track）- 使用 >() 包裹，执行Shell命令
"""

from enum import Enum
from typing import Any, Optional, Dict, List
import re
import math
import subprocess


class TrackType(Enum):
    """轨道类型枚举"""
    MATH = "math"      # 数学轨
    PYTHON = "python"  # Python轨
    SQL = "sql"        # SQL轨
    SHELL = "shell"    # Shell轨


class TrackResult:
    """轨道执行结果"""
    
    def __init__(
        self,
        success: bool,
        value: Any = None,
        error: Optional[str] = None,
        track_type: Optional[TrackType] = None
    ):
        self.success = success
        self.value = value
        self.error = error
        self.track_type = track_type
    
    def __repr__(self):
        if self.success:
            return f"TrackResult(success=True, value={self.value}, track={self.track_type.value})"
        else:
            return f"TrackResult(success=False, error={self.error})"


class MathTrack:
    """数学轨道
    
    支持数学表达式计算，使用 $() 包裹
    示例：$(π * r²)
    """
    
    # 数学常量
    CONSTANTS = {
        'π': math.pi,
        'pi': math.pi,
        'e': math.e,
        '∞': float('inf'),
        'inf': float('inf'),
    }
    
    # 数学函数
    FUNCTIONS = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'sqrt': math.sqrt,
        'log': math.log,
        'log10': math.log10,
        'exp': math.exp,
        'abs': abs,
        'floor': math.floor,
        'ceil': math.ceil,
        'pow': pow,
        'max': max,
        'min': min,
    }
    
    def execute(self, expression: str, context: Dict[str, Any] = None) -> TrackResult:
        """执行数学表达式
        
        Args:
            expression: 数学表达式（不含 $()）
            context: 上下文变量
            
        Returns:
            TrackResult: 执行结果
        """
        try:
            # 替换常量
            for const, value in self.CONSTANTS.items():
                expression = expression.replace(const, str(value))
            
            # 替换上标数字（² → **2）
            superscripts = {'⁰': '**0', '¹': '**1', '²': '**2', '³': '**3', '⁴': '**4', '⁵': '**5'}
            for sup, replacement in superscripts.items():
                expression = expression.replace(sup, replacement)
            
            # 替换下标数字（₀ → _0）
            subscripts = {'₀': '_0', '₁': '_1', '₂': '_2', '₃': '_3', '₄': '_4', '₅': '_5'}
            for sub, replacement in subscripts.items():
                expression = expression.replace(sub, replacement)
            
            # 合并上下文
            eval_context = {**self.FUNCTIONS, **self.CONSTANTS}
            if context:
                eval_context.update(context)
            
            # 计算表达式
            result = eval(expression, {"__builtins__": {}}, eval_context)
            
            return TrackResult(success=True, value=result, track_type=TrackType.MATH)
        
        except Exception as e:
            return TrackResult(success=False, error=str(e), track_type=TrackType.MATH)


class PythonTrack:
    """Python轨道
    
    直接执行Python代码，使用 {{}} 包裹
    示例：{{import pandas as pd; df = pd.DataFrame([1,2,3])}}
    """
    
    def __init__(self):
        self.globals = {}
        self.locals = {}
    
    def execute(self, code: str, context: Dict[str, Any] = None) -> TrackResult:
        """执行Python代码
        
        Args:
            code: Python代码（不含 {{}}）
            context: 上下文变量
            
        Returns:
            TrackResult: 执行结果
        """
        try:
            # 合并上下文
            if context:
                self.locals.update(context)
            
            # 执行代码
            exec(code, self.globals, self.locals)
            
            # 返回最后一个表达式的值
            # 如果代码以 return 开头，则返回其值
            if 'return' in code:
                result = eval(code.replace('return', ''), self.globals, self.locals)
                return TrackResult(success=True, value=result, track_type=TrackType.PYTHON)
            
            return TrackResult(success=True, value=None, track_type=TrackType.PYTHON)
        
        except Exception as e:
            return TrackResult(success=False, error=str(e), track_type=TrackType.PYTHON)


class SQLTrack:
    """SQL轨道
    
    执行SQL查询，使用 SQL"" 包裹
    示例：SQL"SELECT * FROM users WHERE age > 18"
    """
    
    def __init__(self, connection=None):
        self.connection = connection
    
    def execute(self, query: str, context: Dict[str, Any] = None) -> TrackResult:
        """执行SQL查询
        
        Args:
            query: SQL查询（不含 SQL""）
            context: 上下文变量（可用于参数化查询）
            
        Returns:
            TrackResult: 执行结果
        """
        try:
            if not self.connection:
                return TrackResult(
                    success=False,
                    error="SQL connection not configured",
                    track_type=TrackType.SQL
                )
            
            # 执行查询
            cursor = self.connection.cursor()
            
            # 参数化查询
            if context and 'params' in context:
                cursor.execute(query, context['params'])
            else:
                cursor.execute(query)
            
            # 获取结果
            results = cursor.fetchall()
            
            return TrackResult(success=True, value=results, track_type=TrackType.SQL)
        
        except Exception as e:
            return TrackResult(success=False, error=str(e), track_type=TrackType.SQL)


class ShellTrack:
    """Shell轨道
    
    执行Shell命令，使用 >() 包裹
    示例：>(ls -la)
    """
    
    def execute(self, command: str, context: Dict[str, Any] = None) -> TrackResult:
        """执行Shell命令
        
        Args:
            command: Shell命令（不含 >()）
            context: 上下文变量
            
        Returns:
            TrackResult: 执行结果
        """
        try:
            # 执行命令
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return TrackResult(
                    success=True,
                    value=result.stdout.strip(),
                    track_type=TrackType.SHELL
                )
            else:
                return TrackResult(
                    success=False,
                    error=result.stderr.strip(),
                    track_type=TrackType.SHELL
                )
        
        except subprocess.TimeoutExpired:
            return TrackResult(
                success=False,
                error="Command timeout",
                track_type=TrackType.SHELL
            )
        except Exception as e:
            return TrackResult(success=False, error=str(e), track_type=TrackType.SHELL)


class MultiTrackSystem:
    """多轨制系统
    
    统一管理所有轨道的执行
    """
    
    def __init__(self, sql_connection=None):
        self.math_track = MathTrack()
        self.python_track = PythonTrack()
        self.sql_track = SQLTrack(sql_connection)
        self.shell_track = ShellTrack()
        
        # 轨道标记模式
        self.patterns = {
            TrackType.MATH: re.compile(r'\$\((.*?)\)'),
            TrackType.PYTHON: re.compile(r'\{\{(.*?)\}\}'),
            TrackType.SQL: re.compile(r'SQL"(.*?)"'),
            TrackType.SHELL: re.compile(r'>\((.*?)\)'),
        }
    
    def detect_track(self, code: str) -> Optional[TrackType]:
        """检测代码所属轨道
        
        Args:
            code: 代码字符串
            
        Returns:
            TrackType: 轨道类型，如果无法识别则返回None
        """
        for track_type, pattern in self.patterns.items():
            if pattern.search(code):
                return track_type
        return None
    
    def extract_expression(self, code: str, track_type: TrackType) -> str:
        """提取轨道内的表达式
        
        Args:
            code: 代码字符串
            track_type: 轨道类型
            
        Returns:
            str: 提取的表达式
        """
        pattern = self.patterns[track_type]
        match = pattern.search(code)
        if match:
            return match.group(1)
        return code
    
    def execute(self, code: str, context: Dict[str, Any] = None) -> TrackResult:
        """执行代码（自动检测轨道）
        
        Args:
            code: 代码字符串
            context: 上下文变量
            
        Returns:
            TrackResult: 执行结果
        """
        # 检测轨道类型
        track_type = self.detect_track(code)
        
        if not track_type:
            return TrackResult(
                success=False,
                error="Unable to detect track type"
            )
        
        # 提取表达式
        expression = self.extract_expression(code, track_type)
        
        # 根据轨道类型执行
        if track_type == TrackType.MATH:
            return self.math_track.execute(expression, context)
        elif track_type == TrackType.PYTHON:
            return self.python_track.execute(expression, context)
        elif track_type == TrackType.SQL:
            return self.sql_track.execute(expression, context)
        elif track_type == TrackType.SHELL:
            return self.shell_track.execute(expression, context)
        
        return TrackResult(success=False, error="Unknown track type")
    
    def execute_math(self, expression: str, context: Dict[str, Any] = None) -> TrackResult:
        """执行数学表达式"""
        return self.math_track.execute(expression, context)
    
    def execute_python(self, code: str, context: Dict[str, Any] = None) -> TrackResult:
        """执行Python代码"""
        return self.python_track.execute(code, context)
    
    def execute_sql(self, query: str, context: Dict[str, Any] = None) -> TrackResult:
        """执行SQL查询"""
        return self.sql_track.execute(query, context)
    
    def execute_shell(self, command: str, context: Dict[str, Any] = None) -> TrackResult:
        """执行Shell命令"""
        return self.shell_track.execute(command, context)


# 使用示例
if __name__ == '__main__':
    # 创建多轨制系统
    multi_track = MultiTrackSystem()
    
    # 数学轨示例
    print("=== 数学轨示例 ===")
    result = multi_track.execute("$(π * 5²)")
    print(f"π * 5² = {result.value}")
    
    result = multi_track.execute("$(sqrt(16) + sin(π/2))")
    print(f"sqrt(16) + sin(π/2) = {result.value}")
    
    # Python轨示例
    print("\n=== Python轨示例 ===")
    result = multi_track.execute("{{x = [1, 2, 3]; sum(x)}}")
    print(f"sum([1, 2, 3]) = {result.value}")
    
    # Shell轨示例
    print("\n=== Shell轨示例 ===")
    result = multi_track.execute(">(echo 'Hello from Shell')")
    print(f"Shell output: {result.value}")
    
    # 自动检测示例
    print("\n=== 自动检测示例 ===")
    codes = [
        "$(2 + 3)",
        "{{print('Hello')}}",
        ">(pwd)",
    ]
    
    for code in codes:
        track_type = multi_track.detect_track(code)
        print(f"{code} -> {track_type.value if track_type else 'Unknown'}")
