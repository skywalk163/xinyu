"""
subprocess模块中文封装（子进程）
"""

import subprocess
from .base_wrapper import ChineseModuleWrapper


class SubprocessWrapper(ChineseModuleWrapper):
    """subprocess模块中文封装"""
    
    NAME_MAP = {
        '运行': 'run',
        '调用': 'call',
        '检查调用': 'check_call',
        '检查输出': 'check_output',
        'Popen': 'Popen',
        '管道': 'PIPE',
        '标准输出': 'STDOUT',
        '创建进程': 'CREATE_NEW_PROCESS_GROUP',
    }
    
    def __init__(self):
        super().__init__(module=subprocess, name_map=self.NAME_MAP)
