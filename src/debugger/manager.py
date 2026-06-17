"""
调试器管理器
管理调试器实例和调试会话
"""

import sys
import traceback
from typing import Dict, Any, Optional, List
from .interface import IDebugger
from .pdb_debugger import PdbDebugger


class DebuggerManager:
    """调试器管理器"""
    
    def __init__(self, compiler=None):
        self.compiler = compiler
        self.debugger: Optional[IDebugger] = None
        self.is_debugging = False
        self.breakpoints: Dict[str, List[int]] = {}
        self.debug_history: List[Dict[str, Any]] = []
        
    def start_debug_session(self) -> bool:
        """开始调试会话"""
        if self.is_debugging:
            print("调试会话已在运行中")
            return False
            
        try:
            # 创建调试器实例
            self.debugger = PdbDebugger(self.compiler)
            self.is_debugging = True
            self.debug_history.clear()
            
            print("调试会话已开始")
            print("可用命令:")
            print("  break <文件>:<行号> [条件] - 设置断点")
            print("  clear <断点ID> - 清除断点")
            print("  list - 列出所有断点")
            print("  step - 单步执行（步入）")
            print("  next - 单步执行（步过）")
            print("  continue - 继续执行")
            print("  vars [local|global] - 查看变量")
            print("  set <变量名> <值> - 设置变量")
            print("  stack - 查看调用栈")
            print("  eval <表达式> - 计算表达式")
            print("  quit - 退出调试")
            
            return True
            
        except Exception as e:
            print(f"启动调试会话失败: {e}")
            return False
            
    def stop_debug_session(self) -> bool:
        """停止调试会话"""
        if not self.is_debugging:
            print("没有活动的调试会话")
            return False
            
        self.is_debugging = False
        self.debugger = None
        print("调试会话已结束")
        return True
        
    def execute_with_debug(self, code: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """使用调试器执行代码"""
        if not self.is_debugging or not self.debugger:
            print("错误: 没有活动的调试会话")
            return None
            
        try:
            # 记录调试历史
            debug_entry = {
                "code": code,
                "context": context,
                "timestamp": self._get_timestamp()
            }
            self.debug_history.append(debug_entry)
            
            # 使用调试器执行
            result = self.debugger.debug_execute(code, context)
            
            # 更新调试历史
            debug_entry["result"] = result
            debug_entry["completed"] = True
            
            return result
            
        except Exception as e:
            print(f"调试执行失败: {e}")
            traceback.print_exc()
            return None
            
    def handle_command(self, command: str) -> bool:
        """处理调试命令"""
        if not self.is_debugging or not self.debugger:
            print("错误: 没有活动的调试会话")
            return False
            
        parts = command.strip().split()
        if not parts:
            return True
            
        cmd = parts[0].lower()
        args = parts[1:]
        
        try:
            if cmd in ["break", "b"]:
                return self._handle_breakpoint(args)
            elif cmd in ["clear", "c"]:
                return self._handle_clear(args)
            elif cmd in ["list", "l"]:
                return self._handle_list()
            elif cmd in ["step", "s"]:
                return self._handle_step()
            elif cmd in ["next", "n"]:
                return self._handle_next()
            elif cmd in ["continue", "cont"]:
                return self._handle_continue()
            elif cmd in ["vars", "v"]:
                return self._handle_vars(args)
            elif cmd in ["set"]:
                return self._handle_set(args)
            elif cmd in ["stack", "st"]:
                return self._handle_stack()
            elif cmd in ["eval", "e"]:
                return self._handle_eval(args)
            elif cmd in ["quit", "q", "exit"]:
                return self._handle_quit()
            elif cmd in ["help", "h", "?"]:
                return self._handle_help()
            else:
                print(f"未知命令: {cmd}")
                print("输入 'help' 查看可用命令")
                return False
                
        except Exception as e:
            print(f"执行命令失败: {e}")
            return False
            
    def _handle_breakpoint(self, args: List[str]) -> bool:
        """处理设置断点命令"""
        if len(args) < 1:
            print("用法: break <文件>:<行号> [条件]")
            return False
            
        location = args[0]
        condition = args[1] if len(args) > 1 else None
        
        # 解析位置
        if ":" in location:
            filename, line_str = location.split(":", 1)
            try:
                line = int(line_str)
            except ValueError:
                print(f"无效的行号: {line_str}")
                return False
        else:
            print("位置格式应为 <文件>:<行号>")
            return False
            
        # 设置断点
        if self.debugger:
            return self.debugger.set_breakpoint(filename, line, condition)
        return False
        
    def _handle_clear(self, args: List[str]) -> bool:
        """处理清除断点命令"""
        if len(args) < 1:
            print("用法: clear <断点ID>")
            return False
            
        try:
            bp_id = int(args[0])
        except ValueError:
            print(f"无效的断点ID: {args[0]}")
            return False
            
        if self.debugger:
            return self.debugger.clear_breakpoint(bp_id)
        return False
        
    def _handle_list(self) -> bool:
        """处理列出断点命令"""
        if self.debugger:
            breakpoints = self.debugger.list_breakpoints()
            if not breakpoints:
                print("没有设置断点")
            else:
                print("断点列表:")
                for bp in breakpoints:
                    condition = f" (条件: {bp['condition']})" if bp.get('condition') else ""
                    print(f"  {bp['id']}: {bp['filename']}:{bp['line']}{condition}")
            return True
        return False
        
    def _handle_step(self) -> bool:
        """处理单步执行（步入）命令"""
        if self.debugger:
            result = self.debugger.step_into()
            self._print_debug_result(result)
            return True
        return False
        
    def _handle_next(self) -> bool:
        """处理单步执行（步过）命令"""
        if self.debugger:
            result = self.debugger.step_over()
            self._print_debug_result(result)
            return True
        return False
        
    def _handle_continue(self) -> bool:
        """处理继续执行命令"""
        if self.debugger:
            result = self.debugger.continue_execution()
            self._print_debug_result(result)
            return True
        return False
        
    def _handle_vars(self, args: List[str]) -> bool:
        """处理查看变量命令"""
        scope = "local"
        if args:
            scope = args[0].lower()
            if scope not in ["local", "global"]:
                print("作用域应为 'local' 或 'global'")
                return False
                
        if self.debugger:
            variables = self.debugger.get_variables(scope)
            if not variables:
                print(f"没有 {scope} 变量")
            else:
                print(f"{scope} 变量:")
                for name, value in variables.items():
                    print(f"  {name} = {value}")
            return True
        return False
        
    def _handle_set(self, args: List[str]) -> bool:
        """处理设置变量命令"""
        if len(args) < 2:
            print("用法: set <变量名> <值>")
            return False
            
        var_name = args[0]
        var_value = " ".join(args[1:])
        
        # 尝试解析值
        try:
            # 尝试作为Python表达式计算
            import ast
            parsed_value = ast.literal_eval(var_value)
        except:
            # 如果失败，作为字符串处理
            parsed_value = var_value
            
        if self.debugger:
            success = self.debugger.set_variable(var_name, parsed_value)
            if success:
                print(f"变量 {var_name} 已设置为: {parsed_value}")
            return success
        return False
        
    def _handle_stack(self) -> bool:
        """处理查看调用栈命令"""
        if self.debugger:
            stack = self.debugger.get_call_stack()
            if not stack:
                print("调用栈为空")
            else:
                print("调用栈:")
                for i, frame in enumerate(stack):
                    print(f"  #{i}: {frame['function']} at {frame['filename']}:{frame['line']}")
            return True
        return False
        
    def _handle_eval(self, args: List[str]) -> bool:
        """处理计算表达式命令"""
        if len(args) < 1:
            print("用法: eval <表达式>")
            return False
            
        expression = " ".join(args)
        if self.debugger:
            result = self.debugger.evaluate(expression)
            print(f"{expression} = {result}")
            return True
        return False
        
    def _handle_quit(self) -> bool:
        """处理退出命令"""
        print("退出调试会话")
        return self.stop_debug_session()
        
    def _handle_help(self) -> bool:
        """处理帮助命令"""
        help_text = """
调试命令:
  break/b <文件>:<行号> [条件] - 设置断点
  clear/c <断点ID>           - 清除断点
  list/l                     - 列出所有断点
  step/s                     - 单步执行（步入）
  next/n                     - 单步执行（步过）
  continue/cont              - 继续执行
  vars/v [local|global]      - 查看变量
  set <变量名> <值>          - 设置变量
  stack/st                   - 查看调用栈
  eval/e <表达式>            - 计算表达式
  quit/q                     - 退出调试
  help/h/?                   - 显示此帮助
        """
        print(help_text.strip())
        return True
        
    def _print_debug_result(self, result: Dict[str, Any]) -> None:
        """打印调试结果"""
        if "error" in result:
            print(f"错误: {result['error']}")
        elif "frame" in result:
            frame = result["frame"]
            print(f"当前位置: {frame.get('function', '未知')} at {frame.get('filename', '未知')}:{frame.get('line', '未知')}")
            if "code" in frame:
                print(f"代码: {frame['code']}")
        elif "status" in result:
            print(f"状态: {result['status']}")
            
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def get_debug_history(self) -> List[Dict[str, Any]]:
        """获取调试历史"""
        return self.debug_history.copy()