"""
tkinter模块中文封装（图形用户界面）
"""

import tkinter
from .base_wrapper import ChineseModuleWrapper


class TkinterWrapper(ChineseModuleWrapper):
    """tkinter模块中文封装"""
    
    NAME_MAP = {
        '主窗口': 'Tk',
        '框架': 'Frame',
        '标签': 'Label',
        '按钮': 'Button',
        '输入框': 'Entry',
        '文本框': 'Text',
        '画布': 'Canvas',
        '列表框': 'Listbox',
        '菜单': 'Menu',
        '消息框': 'messagebox',
        '文件对话框': 'filedialog',
        '颜色选择器': 'colorchooser',
        '变量': 'StringVar',
        '整型变量': 'IntVar',
        '布尔变量': 'BooleanVar',
    }
    
    def __init__(self):
        super().__init__(module=tkinter, name_map=self.NAME_MAP)
