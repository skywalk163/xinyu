"""
shutil模块中文封装（高级文件操作）
"""

import shutil

from .base_wrapper import ChineseModuleWrapper


class ShutilWrapper(ChineseModuleWrapper):
    """shutil模块中文封装"""

    NAME_MAP = {
        "复制文件": "copyfile",
        "复制": "copy",
        "复制2": "copy2",
        "复制目录": "copytree",
        "移动": "move",
        "删除目录": "rmtree",
        "磁盘使用": "disk_usage",
        "获取终端大小": "get_terminal_size",
        "压缩": "make_archive",
        "解压": "unpack_archive",
        "哪个": "which",
    }

    def __init__(self):
        super().__init__(module=shutil, name_map=self.NAME_MAP)
