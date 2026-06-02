"""
中文命名映射器

提供中英文函数名的双向映射功能。
"""

from typing import Dict, List, Optional, Set


class NameMapper:
    """中文命名映射器"""
    
    def __init__(self):
        """初始化映射器"""
        # 英文名 -> 中文名列表
        self._english_to_chinese: Dict[str, List[str]] = {}
        # 中文名 -> 英文名
        self._chinese_to_english: Dict[str, str] = {}
        # 所有中文别名集合
        self._all_chinese_names: Set[str] = set()
    
    def register(self, english_name: str, chinese_name: str, 
                 aliases: Optional[List[str]] = None) -> None:
        """
        注册映射关系
        
        Args:
            english_name: 英文函数名
            chinese_name: 中文主名称
            aliases: 中文别名列表（可选）
        """
        # 构建中文名称列表
        chinese_names = [chinese_name]
        if aliases:
            chinese_names.extend(aliases)
        
        # 注册英文名到中文名的映射
        self._english_to_chinese[english_name] = chinese_names
        
        # 注册每个中文名到英文名的映射
        for cn_name in chinese_names:
            self._chinese_to_english[cn_name] = english_name
            self._all_chinese_names.add(cn_name)
    
    def to_chinese(self, english_name: str) -> Optional[str]:
        """
        英文名转中文名
        
        Args:
            english_name: 英文函数名
            
        Returns:
            中文主名称，如果不存在返回None
        """
        if english_name in self._english_to_chinese:
            return self._english_to_chinese[english_name][0]
        return None
    
    def to_english(self, chinese_name: str) -> Optional[str]:
        """
        中文名转英文名
        
        Args:
            chinese_name: 中文函数名
            
        Returns:
            英文名称，如果不存在返回None
        """
        return self._chinese_to_english.get(chinese_name)
    
    def get_aliases(self, english_name: str) -> List[str]:
        """
        获取所有中文别名
        
        Args:
            english_name: 英文函数名
            
        Returns:
            中文别名列表（包含主名称）
        """
        return self._english_to_chinese.get(english_name, [])
    
    def is_chinese_name(self, name: str) -> bool:
        """
        判断是否为中文名
        
        Args:
            name: 函数名
            
        Returns:
            如果是中文名返回True，否则返回False
        """
        return name in self._all_chinese_names
    
    def register_builtin_mappings(self) -> None:
        """注册所有内置函数的中英文映射"""
        # 数学函数
        self.register('abs', '绝对值', ['求绝对值'])
        self.register('max', '最大值', ['求最大'])
        self.register('min', '最小值', ['求最小'])
        self.register('sum', '求和', ['合计'])
        self.register('pow', '幂运算', ['乘方'])
        self.register('round', '四舍五入', ['取整'])
        self.register('divmod', '除法余数', ['除余'])
        self.register('complex', '复数', ['创建复数'])
        
        # 类型转换函数
        self.register('int', '转整数', ['整数'])
        self.register('float', '转浮点', ['浮点数'])
        self.register('str', '转字符串', ['字符串'])
        self.register('bool', '转布尔', ['布尔值'])
        self.register('list', '转列表', ['列表'])
        self.register('dict', '转字典', ['字典'])
        self.register('tuple', '转元组', ['元组'])
        self.register('set', '转集合', ['集合'])
        self.register('frozenset', '转冻结集合', ['冻结集合'])
        self.register('bytes', '转字节', ['字节'])
        self.register('bytearray', '转字节数组', ['字节数组'])
        self.register('memoryview', '转内存视图', ['内存视图'])
        
        # 序列操作函数
        self.register('len', '长度', ['求长度'])
        self.register('range', '范围', ['创建范围'])
        self.register('enumerate', '枚举', ['编号'])
        self.register('zip', '拉链', ['配对'])
        self.register('map', '映射', ['遍历映射'])
        self.register('filter', '过滤', ['筛选'])
        self.register('sorted', '排序', ['排序'])
        self.register('reversed', '反转', ['逆序'])
        self.register('iter', '迭代器', ['创建迭代器'])
        self.register('next', '下一个', ['取下一个'])
        self.register('all', '全部为真', ['全真'])
        self.register('any', '任一为真', ['存在真'])
        self.register('slice', '切片', ['截取'])
        
        # 对象操作函数
        self.register('type', '类型', ['获取类型'])
        self.register('isinstance', '是实例', ['实例检查'])
        self.register('issubclass', '是子类', ['子类检查'])
        self.register('hasattr', '有属性', ['属性存在'])
        self.register('getattr', '取属性', ['获取属性'])
        self.register('setattr', '设属性', ['设置属性'])
        self.register('delattr', '删属性', ['删除属性'])
        
        # IO函数
        self.register('print', '打印', ['输出'])
        self.register('input', '输入', ['读取输入'])
        self.register('open', '打开', ['打开文件'])
        self.register('format', '格式化', ['格式'])
        
        # 其他函数
        self.register('id', '标识', ['对象标识'])
        self.register('hash', '哈希', ['哈希值'])
        self.register('repr', '表示', ['字符串表示'])
        self.register('ascii', 'ASCII表示', ['ASCII'])
        self.register('bin', '二进制', ['转二进制'])
        self.register('oct', '八进制', ['转八进制'])
        self.register('hex', '十六进制', ['转十六进制'])
        self.register('chr', '转字符', ['字符'])
        self.register('ord', '转编码', ['编码'])
        self.register('callable', '可调用', ['是否可调用'])
        self.register('help', '帮助', ['查看帮助'])
        self.register('eval', '求值', ['计算表达式'])
        self.register('exec', '执行', ['执行代码'])
        self.register('compile', '编译', ['编译代码'])
        self.register('globals', '全局变量', ['全局'])
        self.register('locals', '局部变量', ['局部'])
