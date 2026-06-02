# 心语语言用户手册

## 简介

心语语言是一个支持中文编程的Python扩展系统，提供完整的中文内置函数和标准库模块接口。用户可以使用中文或英文进行编程，两种方式完全等价。

## 快速开始

### 1. 基本使用

```python
from src.builtin import BuiltinRegistry
from src.module import ModuleManager

# 创建内置函数注册表
registry = BuiltinRegistry()
registry.register_all_builtins()

# 使用中文调用内置函数
result = registry.call('绝对值', -5)  # 返回 5
result = registry.call('最大值', 1, 2, 3)  # 返回 3

# 导入标准库模块
manager = ModuleManager()
math = manager.import_module('数学')
result = math.平方根(16)  # 返回 4.0
```

### 2. 内置函数使用

#### 数学函数

```python
# 绝对值
registry.call('绝对值', -10)  # 10
registry.call('abs', -10)     # 10 (英文也可以)

# 最大值和最小值
registry.call('最大值', 3, 7, 2, 9)  # 9
registry.call('最小值', 3, 7, 2, 9)  # 2

# 求和
registry.call('求和', [1, 2, 3, 4, 5])  # 15

# 幂运算
registry.call('幂运算', 2, 10)  # 1024

# 四舍五入
registry.call('四舍五入', 3.14159, 2)  # 3.14
```

#### 类型转换

```python
# 转整数
registry.call('转整数', '42')  # 42
registry.call('转整数', 3.14)  # 3

# 转浮点
registry.call('转浮点', '3.14')  # 3.14

# 转字符串
registry.call('转字符串', 123)  # '123'

# 转列表
registry.call('转列表', 'hello')  # ['h', 'e', 'l', 'l', 'o']
```

#### 序列操作

```python
# 长度
registry.call('长度', [1, 2, 3, 4, 5])  # 5

# 排序
registry.call('排序', [3, 1, 4, 1, 5])  # [1, 1, 3, 4, 5]

# 反转
list(registry.call('反转', [1, 2, 3]))  # [3, 2, 1]

# 过滤
list(registry.call('过滤', lambda x: x > 2, [1, 2, 3, 4, 5]))  # [3, 4, 5]
```

### 3. 标准库模块使用

#### 数学模块

```python
math = manager.import_module('数学')

# 常量
print(math.圆周率)    # 3.141592653589793
print(math.自然常数)  # 2.718281828459045

# 函数
print(math.平方根(16))    # 4.0
print(math.正弦(1.57))    # ≈ 1.0
print(math.余弦(0))       # 1.0
print(math.向上取整(3.2)) # 4
print(math.向下取整(3.8)) # 3
```

#### 随机模块

```python
random = manager.import_module('随机')

random.设置种子(42)  # 设置随机种子
print(random.随机数())           # 0.0 到 1.0 之间的随机数
print(random.随机整数(1, 100))   # 1 到 100 之间的随机整数
print(random.随机选择([1,2,3,4,5]))  # 随机选择一个元素
print(random.随机采样([1,2,3,4,5], 2))  # 随机采样2个元素
```

#### 集合模块

```python
collections = manager.import_module('集合')

# 计数器
计数器 = collections.计数器
text = "心语语言是一门优雅的中文编程语言"
counter = 计数器(text)
print(counter.most_common(3))  # 最常见的3个字符

# 默认字典
默认字典 = collections.默认字典
dd = 默认字典(int)
dd['a'] += 1
print(dd)  # {'a': 1}
```

#### 正则模块

```python
re = manager.import_module('正则')

text = "我的电话是13812345678"
pattern = r'1[3-9]\d{9}'

# 查找所有匹配
print(re.查找所有(pattern, text))  # ['13812345678']

# 匹配
match = re.匹配(pattern, text)
if match:
    print(f"找到手机号: {match.group()}")
```

#### 迭代工具模块

```python
itertools = manager.import_module('迭代工具')

# 排列
print(list(itertools.排列([1,2,3], 2)))
# [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]

# 组合
print(list(itertools.组合([1,2,3], 2)))
# [(1, 2), (1, 3), (2, 3)]
```

#### 函数工具模块

```python
functools = manager.import_module('函数工具')

# 记忆化装饰器
@functools.记忆化(maxsize=None)
def 斐波那契(n):
    if n < 2:
        return n
    return 斐波那契(n-1) + 斐波那契(n-2)

print(斐波那契(40))  # 快速计算斐波那契数
```

### 4. 帮助系统

```python
from src.builtin.chinese_help import ChineseHelp

help_system = ChineseHelp()

# 查看函数帮助
help_system.help('绝对值')
help_system.help('最大值')

# 列出所有函数
help_system.list_all_functions()

# 列出所有模块
help_system.list_all_modules()
```

## 完整API参考

### 内置函数（69个）

#### 数学函数（8个）
- `绝对值(x)` / `abs(x)` - 绝对值
- `最大值(*args)` / `max(*args)` - 最大值
- `最小值(*args)` / `min(*args)` - 最小值
- `求和(iterable)` / `sum(iterable)` - 求和
- `幂运算(x, y)` / `pow(x, y)` - 幂运算
- `四舍五入(x, n)` / `round(x, n)` - 四舍五入
- `除法余数(a, b)` / `divmod(a, b)` - 除法余数
- `复数(real, imag)` / `complex(real, imag)` - 创建复数

#### 类型转换函数（12个）
- `转整数(x)` / `int(x)` - 转整数
- `转浮点(x)` / `float(x)` - 转浮点数
- `转字符串(x)` / `str(x)` - 转字符串
- `转布尔(x)` / `bool(x)` - 转布尔值
- `转列表(x)` / `list(x)` - 转列表
- `转字典(x)` / `dict(x)` - 转字典
- `转元组(x)` / `tuple(x)` - 转元组
- `转集合(x)` / `set(x)` - 转集合
- `转冻结集合(x)` / `frozenset(x)` - 转冻结集合
- `转字节(x)` / `bytes(x)` - 转字节
- `转字节数组(x)` / `bytearray(x)` - 转字节数组
- `转内存视图(x)` / `memoryview(x)` - 创建内存视图

#### 序列操作函数（15个）
- `长度(s)` / `len(s)` - 长度
- `范围(start, stop, step)` / `range(start, stop, step)` - 创建范围
- `枚举(iterable)` / `enumerate(iterable)` - 枚举
- `拉链(*iterables)` / `zip(*iterables)` - 配对
- `映射(func, iterable)` / `map(func, iterable)` - 映射
- `过滤(func, iterable)` / `filter(func, iterable)` - 过滤
- `排序(iterable)` / `sorted(iterable)` - 排序
- `反转(sequence)` / `reversed(sequence)` - 反转
- `迭代器(iterable)` / `iter(iterable)` - 创建迭代器
- `下一个(iterator)` / `next(iterator)` - 取下一个
- `全部为真(iterable)` / `all(iterable)` - 全部为真
- `任一为真(iterable)` / `any(iterable)` - 任一为真
- `切片(start, stop, step)` / `slice(start, stop, step)` - 切片

### 标准库模块（12个）

#### 数学模块
- `圆周率` - π常量
- `自然常数` - e常量
- `平方根(x)` - 平方根
- `正弦(x)` - 正弦函数
- `余弦(x)` - 余弦函数
- `正切(x)` - 正切函数
- `向上取整(x)` - 向上取整
- `向下取整(x)` - 向下取整

#### 随机模块
- `随机数()` - 生成0-1随机数
- `随机整数(a, b)` - 生成a-b随机整数
- `随机选择(seq)` - 随机选择元素
- `随机采样(seq, k)` - 随机采样k个元素
- `随机打乱(seq)` - 随机打乱序列
- `设置种子(n)` - 设置随机种子

#### 集合模块
- `计数器` - 计数器类
- `默认字典` - 默认字典类
- `有序字典` - 有序字典类
- `命名元组` - 命名元组函数
- `双端队列` - 双端队列类

#### 正则模块
- `匹配(pattern, string)` - 匹配
- `搜索(pattern, string)` - 搜索
- `查找所有(pattern, string)` - 查找所有
- `替换(pattern, repl, string)` - 替换
- `分割(pattern, string)` - 分割
- `编译(pattern)` - 编译正则表达式

#### 迭代工具模块
- `排列(iterable, r)` - 排列
- `组合(iterable, r)` - 组合
- `笛卡尔积(*iterables)` - 笛卡尔积
- `计数(start)` - 计数迭代器
- `循环(iterable)` - 循环迭代器
- `重复(elem, n)` - 重复迭代器

#### 函数工具模块
- `缓存(func)` - 缓存装饰器
- `记忆化(maxsize)` - LRU缓存装饰器
- `偏函数(func, *args)` - 偏函数
- `归约(func, iterable)` - 归约函数

## 实际应用示例

### 示例1: 学生成绩统计

```python
from src.builtin import BuiltinRegistry

registry = BuiltinRegistry()
registry.register_all_builtins()

students = [
    {"姓名": "张三", "成绩": 85},
    {"姓名": "李四", "成绩": 92},
    {"姓名": "王五", "成绩": 78},
    {"姓名": "赵六", "成绩": 95},
    {"姓名": "钱七", "成绩": 88}
]

scores = [s["成绩"] for s in students]

print(f"学生人数: {registry.call('长度', students)}")
print(f"最高分: {registry.call('最大值', *scores)}")
print(f"最低分: {registry.call('最小值', *scores)}")
print(f"平均分: {registry.call('求和', scores) / registry.call('长度', scores):.2f}")
```

### 示例2: 文本分析

```python
from src.module import ModuleManager

manager = ModuleManager()
collections = manager.import_module('集合')

text = "心语语言是一门优雅的中文编程语言"
计数器 = collections.计数器
counter = 计数器(text)

print(f"字符统计: {counter.most_common(5)}")
```

### 示例3: 数据验证

```python
from src.module import ModuleManager

manager = ModuleManager()
re = manager.import_module('正则')

emails = ["test@example.com", "invalid-email", "user@domain.org"]
email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

for email in emails:
    is_valid = bool(re.匹配(email_pattern, email))
    print(f"{email}: {'有效' if is_valid else '无效'}")
```

## 特性总结

1. **中英文双语支持** - 所有函数和模块都支持中文和英文调用
2. **别名系统** - 每个函数支持多个中文别名
3. **完整文档** - 提供详细的中文文档和帮助系统
4. **零开销** - 直接调用Python原生函数，无性能损失
5. **易于扩展** - 可轻松添加新的函数和模块封装

## 系统要求

- Python 3.10+
- 无需额外依赖

## 版本信息

- 版本: 1.0.0
- 发布日期: 2026-06-02
- 支持的内置函数: 69个
- 支持的标准库模块: 12个

---

**心语语言 - 让编程更优雅！**
