"""
内置函数实现模块

该模块包含所有Python内置函数的具体实现，按功能分类组织。
"""

# IO函数
from .io_funcs import builtin_format, builtin_input, builtin_open, builtin_print

# 数学函数
from .math_funcs import (
    builtin_abs,
    builtin_complex,
    builtin_divmod,
    builtin_max,
    builtin_min,
    builtin_pow,
    builtin_round,
    builtin_sum,
)

# 对象操作函数
from .object_funcs import (
    builtin_delattr,
    builtin_getattr,
    builtin_hasattr,
    builtin_isinstance,
    builtin_issubclass,
    builtin_setattr,
    builtin_type,
)

# 其他函数
from .other_funcs import (
    builtin_ascii,
    builtin_bin,
    builtin_callable,
    builtin_chr,
    builtin_compile,
    builtin_eval,
    builtin_exec,
    builtin_globals,
    builtin_hash,
    builtin_help,
    builtin_hex,
    builtin_id,
    builtin_locals,
    builtin_oct,
    builtin_ord,
    builtin_repr,
)

# 序列操作函数
from .sequence_funcs import (
    builtin_all,
    builtin_any,
    builtin_enumerate,
    builtin_filter,
    builtin_iter,
    builtin_len,
    builtin_map,
    builtin_next,
    builtin_range,
    builtin_reversed,
    builtin_slice,
    builtin_sorted,
    builtin_zip,
)

# 类型转换函数
from .type_funcs import (
    builtin_bool,
    builtin_bytearray,
    builtin_bytes,
    builtin_dict,
    builtin_float,
    builtin_frozenset,
    builtin_int,
    builtin_list,
    builtin_memoryview,
    builtin_set,
    builtin_str,
    builtin_tuple,
)

__all__ = [
    # 数学函数
    "builtin_abs",
    "builtin_max",
    "builtin_min",
    "builtin_sum",
    "builtin_pow",
    "builtin_round",
    "builtin_divmod",
    "builtin_complex",
    # 类型转换函数
    "builtin_int",
    "builtin_float",
    "builtin_str",
    "builtin_bool",
    "builtin_list",
    "builtin_dict",
    "builtin_tuple",
    "builtin_set",
    "builtin_frozenset",
    "builtin_bytes",
    "builtin_bytearray",
    "builtin_memoryview",
    # 序列操作函数
    "builtin_len",
    "builtin_range",
    "builtin_enumerate",
    "builtin_zip",
    "builtin_map",
    "builtin_filter",
    "builtin_sorted",
    "builtin_reversed",
    "builtin_iter",
    "builtin_next",
    "builtin_all",
    "builtin_any",
    "builtin_slice",
    # 对象操作函数
    "builtin_type",
    "builtin_isinstance",
    "builtin_issubclass",
    "builtin_hasattr",
    "builtin_getattr",
    "builtin_setattr",
    "builtin_delattr",
    # IO函数
    "builtin_print",
    "builtin_input",
    "builtin_open",
    "builtin_format",
    # 其他函数
    "builtin_id",
    "builtin_hash",
    "builtin_repr",
    "builtin_ascii",
    "builtin_bin",
    "builtin_oct",
    "builtin_hex",
    "builtin_chr",
    "builtin_ord",
    "builtin_callable",
    "builtin_help",
    "builtin_eval",
    "builtin_exec",
    "builtin_compile",
    "builtin_globals",
    "builtin_locals",
]
