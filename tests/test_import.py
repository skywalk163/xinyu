# -*- coding: utf-8 -*-
"""模块导入测试

测试心语语言的模块导入功能。
"""
import io
import sys
from contextlib import redirect_stdout

import pytest


def test_main_module_exists():
    """测试主入口模块存在"""
    try:
        from src.main import ChineseProgram

        assert ChineseProgram is not None
    except ImportError:
        pytest.fail("主入口模块 src.main 不存在")


class TestBasicImport:
    """基本导入测试"""

    def test_import_module(self):
        """测试导入整个模块"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
导入 math。
定义 x = math.sqrt(16)。
打印 x。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)

        output = captured_output.getvalue()
        assert "4.0" in output

    def test_import_with_alias(self):
        """测试导入模块并起别名"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
导入 math 为 m。
定义 x = m.sqrt(25)。
打印 x。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)

        output = captured_output.getvalue()
        assert "5.0" in output


class TestFromImport:
    """from...import测试"""

    def test_from_import_single(self):
        """测试从模块导入单个函数"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
从 math 导入 sqrt。
定义 x = sqrt(36)。
打印 x。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)

        output = captured_output.getvalue()
        assert "6.0" in output

    def test_from_import_multiple(self):
        """测试从模块导入多个函数"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
从 math 导入 sqrt, sin, cos。
定义 x = sqrt(49)。
打印 x。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)

        output = captured_output.getvalue()
        assert "7.0" in output

    def test_from_import_with_alias(self):
        """测试从模块导入并起别名"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
从 math 导入 sqrt 为 square_root。
定义 x = square_root(64)。
打印 x。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)

        output = captured_output.getvalue()
        assert "8.0" in output


class TestImportUsage:
    """导入使用测试"""

    def test_import_and_use_constant(self):
        """测试导入并使用常量"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
导入 math。
定义 x = math.pi。
打印 x。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)

        output = captured_output.getvalue()
        assert "3.14" in output

    def test_import_multiple_modules(self):
        """测试导入多个模块"""
        from src.main import ChineseProgram

        program = ChineseProgram()
        source = """
导入 math。
导入 random。
定义 x = math.sqrt(100)。
打印 x。
"""

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = program.run(source)

        output = captured_output.getvalue()
        assert "10.0" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
