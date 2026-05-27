# -*- coding: utf-8 -*-
"""标准库测试

测试标准库模块的功能。
"""

import pytest
from stdlib import math as 数学
from stdlib import string as 字符串
from stdlib import list as 列表


class TestMathModule:
    """数学模块测试"""
    
    def test_绝对值(self):
        """测试绝对值"""
        assert 数学.绝对值(-5) == 5
        assert 数学.绝对值(5) == 5
        assert 数学.绝对值(0) == 0
    
    def test_最大值(self):
        """测试最大值"""
        assert 数学.最大值(1, 2, 3) == 3
        assert 数学.最大值(5, 2, 8, 1) == 8
    
    def test_最小值(self):
        """测试最小值"""
        assert 数学.最小值(1, 2, 3) == 1
        assert 数学.最小值(5, 2, 8, 1) == 1
    
    def test_平方根(self):
        """测试平方根"""
        assert 数学.平方根(16) == 4.0
        assert 数学.平方根(9) == 3.0
    
    def test_幂(self):
        """测试幂运算"""
        assert 数学.幂(2, 3) == 8.0
        assert 数学.幂(3, 2) == 9.0
    
    def test_对数(self):
        """测试对数"""
        assert 数学.对数(10, 10) == 1.0
        assert 数学.对数(数学.e) == 1.0
    
    def test_三角函数(self):
        """测试三角函数"""
        import math
        assert abs(数学.正弦(0) - 0.0) < 0.0001
        assert abs(数学.余弦(0) - 1.0) < 0.0001
        assert abs(数学.正切(0) - 0.0) < 0.0001
    
    def test_取整函数(self):
        """测试取整函数"""
        assert 数学.向下取整(3.7) == 3
        assert 数学.向上取整(3.2) == 4
        assert 数学.四舍五入(3.5) == 4
        assert 数学.四舍五入(3.14159, 2) == 3.14
    
    def test_常量(self):
        """测试常量"""
        import math
        assert 数学.π == math.pi
        assert 数学.e == math.e


class TestStringModule:
    """字符串模块测试"""
    
    def test_长度(self):
        """测试长度"""
        assert 字符串.长度("hello") == 5
        assert 字符串.长度("你好") == 2
    
    def test_大小写转换(self):
        """测试大小写转换"""
        assert 字符串.大写("hello") == "HELLO"
        assert 字符串.小写("HELLO") == "hello"
    
    def test_去空白(self):
        """测试去空白"""
        assert 字符串.去空白("  hello  ") == "hello"
    
    def test_分割(self):
        """测试分割"""
        assert 字符串.分割("a,b,c", ",") == ["a", "b", "c"]
    
    def test_连接(self):
        """测试连接"""
        assert 字符串.连接(["a", "b", "c"], ",") == "a,b,c"
    
    def test_替换(self):
        """测试替换"""
        assert 字符串.替换("hello world", "world", "心语") == "hello 心语"
    
    def test_查找(self):
        """测试查找"""
        assert 字符串.查找("hello", "ll") == 2
        assert 字符串.查找("hello", "x") == -1
    
    def test_计数(self):
        """测试计数"""
        assert 字符串.计数("hello", "l") == 2
    
    def test_开头结尾(self):
        """测试开头结尾"""
        assert 字符串.开头为("hello", "he") is True
        assert 字符串.结尾为("hello", "lo") is True
    
    def test_包含(self):
        """测试包含"""
        assert 字符串.包含("hello", "ell") is True
        assert 字符串.包含("hello", "xyz") is False
    
    def test_重复(self):
        """测试重复"""
        assert 字符串.重复("ab", 3) == "ababab"
    
    def test_格式化(self):
        """测试格式化"""
        assert 字符串.首字母大写("hello") == "Hello"
        assert 字符串.标题格式("hello world") == "Hello World"
    
    def test_类型检查(self):
        """测试类型检查"""
        assert 字符串.是否数字("123") is True
        assert 字符串.是否字母("abc") is True
        assert 字符串.是否空白("   ") is True


class TestListModule:
    """列表模块测试"""
    
    def test_长度(self):
        """测试长度"""
        assert 列表.长度([1, 2, 3]) == 3
    
    def test_添加(self):
        """测试添加"""
        assert 列表.添加([1, 2], 3) == [1, 2, 3]
    
    def test_扩展(self):
        """测试扩展"""
        assert 列表.扩展([1, 2], [3, 4]) == [1, 2, 3, 4]
    
    def test_插入(self):
        """测试插入"""
        assert 列表.插入([1, 2, 3], 1, 5) == [1, 5, 2, 3]
    
    def test_移除(self):
        """测试移除"""
        assert 列表.移除([1, 2, 3, 2], 2) == [1, 3, 2]
    
    def test_弹出(self):
        """测试弹出"""
        assert 列表.弹出([1, 2, 3]) == 3
    
    def test_排序(self):
        """测试排序"""
        assert 列表.排序([3, 1, 2]) == [1, 2, 3]
        assert 列表.排序([3, 1, 2], reverse=True) == [3, 2, 1]
    
    def test_反转(self):
        """测试反转"""
        assert 列表.反转([1, 2, 3]) == [3, 2, 1]
    
    def test_索引(self):
        """测试索引"""
        assert 列表.索引([1, 2, 3], 2) == 1
    
    def test_计数(self):
        """测试计数"""
        assert 列表.计数([1, 2, 2, 3], 2) == 2
    
    def test_包含(self):
        """测试包含"""
        assert 列表.包含([1, 2, 3], 2) is True
        assert 列表.包含([1, 2, 3], 5) is False
    
    def test_切片(self):
        """测试切片"""
        assert 列表.切片([1, 2, 3, 4, 5], 1, 4) == [2, 3, 4]
    
    def test_连接(self):
        """测试连接"""
        assert 列表.连接([1, 2, 3], ",") == "1,2,3"
    
    def test_统计函数(self):
        """测试统计函数"""
        assert 列表.求和([1, 2, 3]) == 6
        assert 列表.最大值([1, 2, 3]) == 3
        assert 列表.最小值([1, 2, 3]) == 1
    
    def test_去重(self):
        """测试去重"""
        assert 列表.去重([1, 2, 2, 3]) == [1, 2, 3]


class TestStdlibIntegration:
    """标准库集成测试"""
    
    def test_模块导入(self):
        """测试模块导入"""
        from stdlib import 数学, 字符串, 列表
        assert 数学 is not None
        assert 字符串 is not None
        assert 列表 is not None
    
    def test_跨模块使用(self):
        """测试跨模块使用"""
        # 使用数学模块计算
        result = 数学.平方根(16)
        # 使用字符串模块处理
        text = 字符串.大写("hello")
        # 使用列表模块处理
        lst = 列表.排序([3, 1, 2])

        assert result == 4.0
        assert text == "HELLO"
        assert lst == [1, 2, 3]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
