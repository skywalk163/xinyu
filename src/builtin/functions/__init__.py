"""
内置函数实现模块

该模块包含所有Python内置函数的具体实现，按功能分类组织。
"""

# 数学函数
from .math_funcs import (
    builtin_abs, builtin_max, builtin_min, builtin_sum,
    builtin_pow, builtin_round, builtin_divmod, builtin_complex
)

# 类型转换函数
from .type_funcs import (
    builtin_int, builtin_float, builtin_str, builtin_bool,
    builtin_list, builtin_dict, builtin_tuple, builtin_set,
    builtin_frozenset, builtin_bytes, builtin_bytearray, builtin_memoryview
)

# 序列操作函数
from .sequence_funcs import (
    builtin_len, builtin_range, builtin_enumerate, builtin_zip,
    builtin_map, builtin_filter, builtin_sorted, builtin_reversed,
    builtin_iter, builtin_next, builtin_all, builtin_any, builtin_slice
)

# 对象操作函数
from .object_funcs import (
    builtin_type, builtin_isinstance, builtin_issubclass,
    builtin_hasattr, builtin_getattr, builtin_setattr, builtin_delattr
)

# IO函数
from .io_funcs import (
    builtin_print, builtin_input, builtin_open, builtin_format
)

# 其他函数
from .other_funcs import (
    builtin_id, builtin_hash, builtin_repr, builtin_ascii,
    builtin_bin, builtin_oct, builtin_hex, builtin_chr, builtin_ord,
    builtin_callable, builtin_help, builtin_eval, builtin_exec,
    builtin_compile, builtin_globals, builtin_locals
)

__all__ = [
    # 数学函数
    'builtin_abs', 'builtin_max', 'builtin_min', 'builtin_sum',
    'builtin_pow', 'builtin_round', 'builtin_divmod', 'builtin_complex',
    # 类型转换函数
    'builtin_int', 'builtin_float', 'builtin_str', 'builtin_bool',
    'builtin_list', 'builtin_dict', 'builtin_tuple', 'builtin_set',
    'builtin_frozenset', 'builtin_bytes', 'builtin_bytearray', 'builtin_memoryview',
    # 序列操作函数
    'builtin_len', 'builtin_range', 'builtin_enumerate', 'builtin_zip',
    'builtin_map', 'builtin_filter', 'builtin_sorted', 'builtin_reversed',
    'builtin_iter', 'builtin_next', 'builtin_all', 'builtin_any', 'builtin_slice',
    # 对象操作函数
    'builtin_type', 'builtin_isinstance', 'builtin_issubclass',
    'builtin_hasattr', 'builtin_getattr', 'builtin_setattr', 'builtin_delattr',
    # IO函数
    'builtin_print', 'builtin_input', 'builtin_open', 'builtin_format',
    # 其他函数
    'builtin_id', 'builtin_hash', 'builtin_repr', 'builtin_ascii',
    'builtin_bin', 'builtin_oct', 'builtin_hex', 'builtin_chr', 'builtin_ord',
    'builtin_callable', 'builtin_help', 'builtin_eval', 'builtin_exec',
    'builtin_compile', 'builtin_globals', 'builtin_locals'
]
