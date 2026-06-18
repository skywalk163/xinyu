"""
PDB调试器实现
基于Python标准库pdb的调试器
"""

import pdb
import sys
import traceback
from typing import Any, Dict, List, Optional

from .interface import DebuggerBase


class PdbDebugger(DebuggerBase):
    """基于pdb的调试器实现"""

    def __init__(self, compiler=None):
        super().__init__()
        self.compiler = compiler
        self.pdb = pdb.Pdb()
        self.pdb.use_rawinput = False  # 禁用交互式输入
        self.current_frame = None
        self.breakpoint_map: Dict[int, pdb.Breakpoint] = {}
        self.execution_context: Dict[str, Any] = {}

    def set_breakpoint(self, filename: str, line: int, condition: Optional[str] = None) -> bool:
        """设置断点"""
        try:
            # 创建pdb断点
            bp = self.pdb.set_break(filename, line, condition, 1, temporary=False)

            # 生成断点ID
            bp_id = self._generate_breakpoint_id()

            # 保存断点信息
            self.breakpoints[bp_id] = self._format_breakpoint_info(bp_id, filename, line, condition)
            self.breakpoint_map[bp_id] = bp

            print(
                f"断点 {bp_id} 已设置在 {filename}:{line}" + (f" (条件: {condition})" if condition else "")
            )
            return True

        except Exception as e:
            print(f"设置断点失败: {e}")
            return False

    def clear_breakpoint(self, breakpoint_id: int) -> bool:
        """清除断点"""
        if breakpoint_id not in self.breakpoints:
            print(f"断点 {breakpoint_id} 不存在")
            return False

        try:
            # 获取pdb断点
            bp = self.breakpoint_map.get(breakpoint_id)
            if bp:
                # 清除pdb断点
                self.pdb.clear_bpbynumber(bp.number)

            # 从映射中移除
            del self.breakpoints[breakpoint_id]
            if breakpoint_id in self.breakpoint_map:
                del self.breakpoint_map[breakpoint_id]

            print(f"断点 {breakpoint_id} 已清除")
            return True

        except Exception as e:
            print(f"清除断点失败: {e}")
            return False

    def step_over(self) -> Dict[str, Any]:
        """单步执行（步过）"""
        try:
            if not self.current_frame:
                return {"error": "没有活动的执行帧"}

            # 使用pdb的next命令
            self.pdb.set_step()
    _ = e_with_debug("next")  # 未使用变量

            return {
                "status": "step_over_completed",
                "frame": self._get_frame_info(),
                "result": result,
            }

        except Exception as e:
            return {"error": f"步过执行失败: {e}"}

    def step_into(self) -> Dict[str, Any]:
        """单步执行（步入）"""
        try:
            if not self.current_frame:
                return {"error": "没有活动的执行帧"}

            # 使用pdb的step命令
            self.pdb.set_step()
    _ = e_with_debug("step")  # 未使用变量

            return {
                "status": "step_into_completed",
                "frame": self._get_frame_info(),
                "result": result,
            }

        except Exception as e:
            return {"error": f"步入执行失败: {e}"}

    def step_out(self) -> Dict[str, Any]:
        """单步执行（步出）"""
        try:
            if not self.current_frame:
                return {"error": "没有活动的执行帧"}

            # 使用pdb的return命令
            self.pdb.set_return()
    _ = e_with_debug("return")  # 未使用变量

            return {
                "status": "step_out_completed",
                "frame": self._get_frame_info(),
                "result": result,
            }

        except Exception as e:
            return {"error": f"步出执行失败: {e}"}

    def continue_execution(self) -> Dict[str, Any]:
        """继续执行"""
        try:
            if not self.current_frame:
                return {"error": "没有活动的执行帧"}

            # 使用pdb的continue命令
    _ = e_with_debug("continue")  # 未使用变量

            return {"status": "execution_completed", "result": result}

        except Exception as e:
            return {"error": f"继续执行失败: {e}"}

    def get_variables(self, scope: str = "local") -> Dict[str, Any]:
        """获取变量"""
        try:
            if not self.current_frame:
                return {}

            frame = self.current_frame

            if scope == "local":
                # 获取局部变量
                variables = frame.f_locals.copy()
            elif scope == "global":
                # 获取全局变量
                variables = frame.f_globals.copy()
            else:
                # 默认获取所有变量
                variables = {}
                variables.update(frame.f_globals)
                variables.update(frame.f_locals)

            # 过滤掉内部变量
            filtered_vars = {}
            for name, value in variables.items():
                if not name.startswith("__") or not name.endswith("__"):
                    # 简化显示
                    try:
                        filtered_vars[name] = str(value)[:100]  # 限制长度
                    except Exception:
                        filtered_vars[name] = "<无法显示>"

            return filtered_vars

        except Exception as e:
            print(f"获取变量失败: {e}")
            return {}

    def set_variable(self, name: str, value: Any) -> bool:
        """设置变量值"""
        try:
            if not self.current_frame:
                return False

            frame = self.current_frame

            # 尝试在局部作用域设置
            if name in frame.f_locals:
                frame.f_locals[name] = value
            # 尝试在全局作用域设置
            elif name in frame.f_globals:
                frame.f_globals[name] = value
            else:
                # 在局部作用域创建新变量
                frame.f_locals[name] = value

            print(f"变量 {name} 已设置为: {value}")
            return True

        except Exception as e:
            print(f"设置变量失败: {e}")
            return False

    def get_call_stack(self) -> List[Dict[str, Any]]:
        """获取调用栈"""
        try:
            if not self.current_frame:
                return []

            stack = []
            frame = self.current_frame

            # 遍历调用栈
            while frame:
                stack_info = {
                    "filename": frame.f_code.co_filename,
                    "function": frame.f_code.co_name,
                    "line": frame.f_lineno,
                    "locals": list(frame.f_locals.keys()),
                    "globals": list(frame.f_globals.keys()),
                }
                stack.append(stack_info)
                frame = frame.f_back

            return stack

        except Exception as e:
            print(f"获取调用栈失败: {e}")
            return []

    def evaluate(self, expression: str) -> Any:
        """计算表达式"""
        try:
            if not self.current_frame:
                return "错误: 没有活动的执行帧"

            frame = self.current_frame

            # 在帧的上下文中计算表达式
    _ = ion, frame.f_globals, frame.f_locals)  # 未使用变量
            return result

        except Exception as e:
            return f"计算表达式失败: {e}"

    def debug_execute(self, code: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """调试执行代码"""
        try:
            # 准备执行上下文
            exec_context = self.execution_context.copy()
            if context:
                exec_context.update(context)

            # 设置当前帧
            self.current_frame = sys._getframe()

            # 编译代码
            compiled_code = compile(code, "<debug>", "exec")

            # 使用pdb运行
            self.pdb.run(compiled_code, exec_context)

            # 获取结果
    _ = .get("__result__", None)  # 未使用变量

            return result

        except Exception as e:
            print(f"调试执行失败: {e}")
            traceback.print_exc()
            return None
        finally:
            self.current_frame = None

    def _execute_with_debug(self, command: str) -> Any:
        """使用pdb执行命令"""
        try:
            # 保存当前标准输入输出
            old_stdin = sys.stdin
            old_stdout = sys.stdout

            # 重定向到字符串
            import io

            sys.stdin = io.StringIO(command + "\n")
            sys.stdout = io.StringIO()

            # 执行命令
            self.pdb.cmdloop()

            # 恢复标准输入输出
            sys.stdin = old_stdin
            sys.stdout = old_stdout

            # 获取输出
            output = sys.stdout.getvalue()
            return output

        except Exception as e:
            print(f"执行命令失败: {e}")
            return None

    def _get_frame_info(self) -> Dict[str, Any]:
        """获取当前帧信息"""
        if not self.current_frame:
            return {}

        frame = self.current_frame
        return {
            "filename": frame.f_code.co_filename,
            "function": frame.f_code.co_name,
            "line": frame.f_lineno,
            "code": self._get_current_line(frame),
        }

    def _get_current_line(self, frame) -> str:
        """获取当前行代码"""
        try:
            import linecache

            filename = frame.f_code.co_filename
            line_no = frame.f_lineno
            line = linecache.getline(filename, line_no)
            return line.strip()
        except Exception:
            return "<无法获取代码行>"
