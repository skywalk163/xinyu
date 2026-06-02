"""
内置函数注册表

管理所有内置函数的注册、查询和调用。
"""

from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass
from .name_mapper import NameMapper
from ..validation.param_validator import ParamValidator
from ..exception.translator import ExceptionTranslator


@dataclass
class BuiltinFunction:
    """内置函数数据结构"""
    name: str                    # 英文名称
    chinese_name: str            # 中文名称
    func: Callable               # 函数对象
    arity: tuple                 # 元数信息 (min_args, max_args)
    doc: str                     # 中文文档
    aliases: List[str] = None    # 中文别名列表
    
    def __post_init__(self):
        if self.aliases is None:
            self.aliases = []


class BuiltinRegistry:
    """内置函数注册表"""
    
    def __init__(self):
        """初始化注册表"""
        self._functions: Dict[str, BuiltinFunction] = {}
        self._name_mapper = NameMapper()
        self._param_validator = ParamValidator()
        self._exception_translator = ExceptionTranslator()
        
        # 注册所有内置函数的名称映射
        self._name_mapper.register_builtin_mappings()
    
    def register(self, func_info: BuiltinFunction) -> None:
        """
        注册内置函数
        
        Args:
            func_info: 内置函数信息对象
        """
        self._functions[func_info.name] = func_info
    
    def get(self, name: str) -> Optional[BuiltinFunction]:
        """
        查询内置函数（支持中英文）
        
        Args:
            name: 函数名（中文或英文）
            
        Returns:
            内置函数信息对象，如果不存在返回None
        """
        # 先尝试英文名
        if name in self._functions:
            return self._functions[name]
        
        # 再尝试通过NameMapper查找
        if self._name_mapper:
            english_name = self._name_mapper.to_english(name)
            if english_name and english_name in self._functions:
                return self._functions[english_name]
        
        return None
    
    def call(self, name: str, *args, **kwargs) -> Any:
        """
        调用内置函数
        
        Args:
            name: 函数名（中文或英文）
            *args: 位置参数
            **kwargs: 关键字参数
            
        Returns:
            函数调用结果
        """
        func_info = self.get(name)
        if func_info is None:
            raise NameError(f"未找到内置函数: {name}")
        
        # 参数验证（如果启用）
        if self._param_validator:
            self._param_validator.validate(func_info, args, kwargs)
        
        # 调用函数
        try:
            return func_info.func(*args, **kwargs)
        except Exception as e:
            # 异常转换（如果启用）
            if self._exception_translator:
                raise self._exception_translator.translate(e)
            raise
    
    def register_all_builtins(self) -> None:
        """注册所有69个内置函数"""
        # 导入所有内置函数实现
        from .functions import (
            # 数学函数
            builtin_abs, builtin_max, builtin_min, builtin_sum,
            builtin_pow, builtin_round, builtin_divmod, builtin_complex,
            # 类型转换函数
            builtin_int, builtin_float, builtin_str, builtin_bool,
            builtin_list, builtin_dict, builtin_tuple, builtin_set,
            builtin_frozenset, builtin_bytes, builtin_bytearray, builtin_memoryview,
            # 序列操作函数
            builtin_len, builtin_range, builtin_enumerate, builtin_zip,
            builtin_map, builtin_filter, builtin_sorted, builtin_reversed,
            builtin_iter, builtin_next, builtin_all, builtin_any, builtin_slice,
            # 对象操作函数
            builtin_type, builtin_isinstance, builtin_issubclass,
            builtin_hasattr, builtin_getattr, builtin_setattr, builtin_delattr,
            # IO函数
            builtin_print, builtin_input, builtin_open, builtin_format,
            # 其他函数
            builtin_id, builtin_hash, builtin_repr, builtin_ascii,
            builtin_bin, builtin_oct, builtin_hex, builtin_chr, builtin_ord,
            builtin_callable, builtin_help, builtin_eval, builtin_exec,
            builtin_compile, builtin_globals, builtin_locals
        )
        
        # 注册数学函数
        self.register(BuiltinFunction('abs', '绝对值', builtin_abs, (1, 1), '返回数字的绝对值', ['求绝对值']))
        self.register(BuiltinFunction('max', '最大值', builtin_max, (1, None), '返回最大值', ['求最大']))
        self.register(BuiltinFunction('min', '最小值', builtin_min, (1, None), '返回最小值', ['求最小']))
        self.register(BuiltinFunction('sum', '求和', builtin_sum, (1, 2), '求和', ['合计']))
        self.register(BuiltinFunction('pow', '幂运算', builtin_pow, (2, 3), '幂运算', ['乘方']))
        self.register(BuiltinFunction('round', '四舍五入', builtin_round, (1, 2), '四舍五入', ['取整']))
        self.register(BuiltinFunction('divmod', '除法余数', builtin_divmod, (2, 2), '返回除法的商和余数', ['除余']))
        self.register(BuiltinFunction('complex', '复数', builtin_complex, (1, 2), '创建复数', ['创建复数']))
        
        # 注册类型转换函数
        self.register(BuiltinFunction('int', '转整数', builtin_int, (1, 2), '转换为整数', ['整数']))
        self.register(BuiltinFunction('float', '转浮点', builtin_float, (1, 1), '转换为浮点数', ['浮点数']))
        self.register(BuiltinFunction('str', '转字符串', builtin_str, (1, 1), '转换为字符串', ['字符串']))
        self.register(BuiltinFunction('bool', '转布尔', builtin_bool, (1, 1), '转换为布尔值', ['布尔值']))
        self.register(BuiltinFunction('list', '转列表', builtin_list, (1, 1), '转换为列表', ['列表']))
        self.register(BuiltinFunction('dict', '转字典', builtin_dict, (1, 1), '转换为字典', ['字典']))
        self.register(BuiltinFunction('tuple', '转元组', builtin_tuple, (1, 1), '转换为元组', ['元组']))
        self.register(BuiltinFunction('set', '转集合', builtin_set, (1, 1), '转换为集合', ['集合']))
        self.register(BuiltinFunction('frozenset', '转冻结集合', builtin_frozenset, (1, 1), '转换为冻结集合', ['冻结集合']))
        self.register(BuiltinFunction('bytes', '转字节', builtin_bytes, (1, 2), '转换为字节', ['字节']))
        self.register(BuiltinFunction('bytearray', '转字节数组', builtin_bytearray, (1, 2), '转换为字节数组', ['字节数组']))
        self.register(BuiltinFunction('memoryview', '转内存视图', builtin_memoryview, (1, 1), '创建内存视图', ['内存视图']))
        
        # 注册序列操作函数
        self.register(BuiltinFunction('len', '长度', builtin_len, (1, 1), '返回长度', ['求长度']))
        self.register(BuiltinFunction('range', '范围', builtin_range, (1, 3), '创建范围', ['创建范围']))
        self.register(BuiltinFunction('enumerate', '枚举', builtin_enumerate, (1, 2), '枚举', ['编号']))
        self.register(BuiltinFunction('zip', '拉链', builtin_zip, (0, None), '配对', ['配对']))
        self.register(BuiltinFunction('map', '映射', builtin_map, (2, None), '映射', ['遍历映射']))
        self.register(BuiltinFunction('filter', '过滤', builtin_filter, (2, 2), '过滤', ['筛选']))
        self.register(BuiltinFunction('sorted', '排序', builtin_sorted, (1, None), '排序', ['排序']))
        self.register(BuiltinFunction('reversed', '反转', builtin_reversed, (1, 1), '反转', ['逆序']))
        self.register(BuiltinFunction('iter', '迭代器', builtin_iter, (1, 2), '创建迭代器', ['创建迭代器']))
        self.register(BuiltinFunction('next', '下一个', builtin_next, (1, 2), '取下一个', ['取下一个']))
        self.register(BuiltinFunction('all', '全部为真', builtin_all, (1, 1), '检查是否全部为真', ['全真']))
        self.register(BuiltinFunction('any', '任一为真', builtin_any, (1, 1), '检查是否任一为真', ['存在真']))
        self.register(BuiltinFunction('slice', '切片', builtin_slice, (1, 3), '创建切片', ['截取']))
        
        # 注册对象操作函数
        self.register(BuiltinFunction('type', '类型', builtin_type, (1, 3), '获取类型', ['获取类型']))
        self.register(BuiltinFunction('isinstance', '是实例', builtin_isinstance, (2, 2), '实例检查', ['实例检查']))
        self.register(BuiltinFunction('issubclass', '是子类', builtin_issubclass, (2, 2), '子类检查', ['子类检查']))
        self.register(BuiltinFunction('hasattr', '有属性', builtin_hasattr, (2, 2), '属性存在检查', ['属性存在']))
        self.register(BuiltinFunction('getattr', '取属性', builtin_getattr, (2, 3), '获取属性', ['获取属性']))
        self.register(BuiltinFunction('setattr', '设属性', builtin_setattr, (3, 3), '设置属性', ['设置属性']))
        self.register(BuiltinFunction('delattr', '删属性', builtin_delattr, (2, 2), '删除属性', ['删除属性']))
        
        # 注册IO函数
        self.register(BuiltinFunction('print', '打印', builtin_print, (0, None), '打印输出', ['输出']))
        self.register(BuiltinFunction('input', '输入', builtin_input, (0, 1), '读取输入', ['读取输入']))
        self.register(BuiltinFunction('open', '打开', builtin_open, (1, None), '打开文件', ['打开文件']))
        self.register(BuiltinFunction('format', '格式化', builtin_format, (1, 2), '格式化', ['格式']))
        
        # 注册其他函数
        self.register(BuiltinFunction('id', '标识', builtin_id, (1, 1), '对象标识', ['对象标识']))
        self.register(BuiltinFunction('hash', '哈希', builtin_hash, (1, 1), '哈希值', ['哈希值']))
        self.register(BuiltinFunction('repr', '表示', builtin_repr, (1, 1), '字符串表示', ['字符串表示']))
        self.register(BuiltinFunction('ascii', 'ASCII表示', builtin_ascii, (1, 1), 'ASCII表示', ['ASCII']))
        self.register(BuiltinFunction('bin', '二进制', builtin_bin, (1, 1), '转二进制', ['转二进制']))
        self.register(BuiltinFunction('oct', '八进制', builtin_oct, (1, 1), '转八进制', ['转八进制']))
        self.register(BuiltinFunction('hex', '十六进制', builtin_hex, (1, 1), '转十六进制', ['转十六进制']))
        self.register(BuiltinFunction('chr', '转字符', builtin_chr, (1, 1), '转字符', ['字符']))
        self.register(BuiltinFunction('ord', '转编码', builtin_ord, (1, 1), '转编码', ['编码']))
        self.register(BuiltinFunction('callable', '可调用', builtin_callable, (1, 1), '是否可调用', ['是否可调用']))
        self.register(BuiltinFunction('help', '帮助', builtin_help, (0, 1), '查看帮助', ['查看帮助']))
        self.register(BuiltinFunction('eval', '求值', builtin_eval, (1, 3), '计算表达式', ['计算表达式']))
        self.register(BuiltinFunction('exec', '执行', builtin_exec, (1, 3), '执行代码', ['执行代码']))
        self.register(BuiltinFunction('compile', '编译', builtin_compile, (3, 6), '编译代码', ['编译代码']))
        self.register(BuiltinFunction('globals', '全局变量', builtin_globals, (0, 0), '全局变量', ['全局']))
        self.register(BuiltinFunction('locals', '局部变量', builtin_locals, (0, 0), '局部变量', ['局部']))
    
    def list_all_functions(self) -> List[str]:
        """列出所有已注册的内置函数"""
        return list(self._functions.keys())
