# -*- coding: utf-8 -*-
"""安全运行时环境测试

测试SecureRuntime和InputValidator的功能。
"""

import pytest

from src.runtime.secure_runtime import (
    InputValidator,
    SecureRuntime,
    SecurityError,
    create_safe_runtime,
    execute_safely,
)
from src.security.input_validator import (
    InputSanitizer,
    SourceCodeValidator,
    sanitize_source,
    validate_source,
)


class TestInputValidator:
    """输入验证器测试"""

    def test_validate_source_valid(self):
        """测试有效源代码验证"""
        source = 'print("你好")'
        is_valid, error = InputValidator.validate_source(source)
        assert is_valid is True
        assert error is None

    def test_validate_source_too_long(self):
        """测试源代码过长"""
        source = "x" * (InputValidator.MAX_SOURCE_LENGTH + 1)
        is_valid, error = InputValidator.validate_source(source)
        assert is_valid is False
        assert "过长" in error

    def test_validate_source_dangerous_import(self):
        """测试危险导入"""
        source = '__import__("os")'
        is_valid, error = InputValidator.validate_source(source)
        assert is_valid is False
        assert "__import__" in error

    def test_validate_source_dangerous_eval(self):
        """测试危险eval"""
        source = 'eval("1+1")'
        is_valid, error = InputValidator.validate_source(source)
        assert is_valid is False
        assert "eval" in error

    def test_validate_source_dangerous_exec(self):
        """测试危险exec"""
        source = 'exec("print(1)")'
        is_valid, error = InputValidator.validate_source(source)
        assert is_valid is False
        assert "exec" in error

    def test_validate_source_dangerous_os(self):
        """测试危险os模块"""
        source = 'os.system("ls")'
        is_valid, error = InputValidator.validate_source(source)
        assert is_valid is False
        assert "os" in error

    def test_validate_encoding_valid(self):
        """测试有效编码"""
        source = 'print("你好")'
        is_valid, error = InputValidator.validate_encoding(source)
        assert is_valid is True
        assert error is None


class TestSecureRuntime:
    """安全运行时测试"""

    def test_execute_simple_code(self):
        """测试执行简单代码"""
        runtime = SecureRuntime()
        code = "result = 1 + 1"
        success, result, error = runtime.execute(code)
        assert success is True
        assert error is None

    def test_execute_print(self):
        """测试打印功能"""
        runtime = SecureRuntime()
        code = 'print("你好，心语")'
        success, result, error = runtime.execute(code)
        assert success is True
        assert error is None

    def test_execute_math_operations(self):
        """测试数学运算"""
        runtime = SecureRuntime()
        code = "result = 2 * 3 + 4"
        success, result, error = runtime.execute(code)
        assert success is True
        assert error is None

    def test_execute_with_math_module(self):
        """测试使用math模块"""
        runtime = SecureRuntime()
        code = "result = math.sqrt(16)"
        success, result, error = runtime.execute(code)
        assert success is True
        assert error is None

    def test_execute_with_json_module(self):
        """测试使用json模块"""
        runtime = SecureRuntime()
        code = 'result = json.dumps({"key": "value"})'
        success, result, error = runtime.execute(code)
        assert success is True
        assert error is None

    def test_execute_dangerous_code_blocked(self):
        """测试危险代码被阻止"""
        runtime = SecureRuntime()
        code = '__import__("os").system("ls")'
        success, result, error = runtime.execute(code)
        assert success is False
        assert "__import__" in error

    def test_execute_eval_blocked(self):
        """测试eval被阻止"""
        runtime = SecureRuntime()
        code = 'eval("1+1")'
        success, result, error = runtime.execute(code)
        assert success is False
        assert "eval" in error

    def test_execute_with_validation(self):
        """测试带验证的执行"""
        runtime = SecureRuntime()
        code = "result = 1 + 1"
        success, result, error = runtime.execute(code, validate=True)
        assert success is True
        assert error is None

    def test_execute_without_validation(self):
        """测试不带验证的执行"""
        runtime = SecureRuntime()
        code = "result = 1 + 1"
        success, result, error = runtime.execute(code, validate=False)
        assert success is True
        assert error is None

    def test_compile_restricted_code(self):
        """测试编译受限代码"""
        runtime = SecureRuntime()
        code = "result = 1 + 1"
        success, byte_code, error = runtime.compile_restricted_code(code)
        assert success is True
        assert byte_code is not None
        assert error is None

    def test_compile_invalid_code(self):
        """测试编译无效代码"""
        runtime = SecureRuntime()
        code = "result = 1 + "  # 语法错误
        success, byte_code, error = runtime.compile_restricted_code(code)
        assert success is False
        assert error is not None


class TestSourceCodeValidator:
    """源代码验证器测试"""

    def test_validate_valid_code(self):
        """测试验证有效代码"""
        source = "定 x = 5。"
        result = validate_source(source)
        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validate_empty_code(self):
        """测试验证空代码"""
        source = ""
        result = validate_source(source)
        assert result.is_valid is False
        assert "空" in result.errors[0]

    def test_validate_too_long_code(self):
        """测试验证过长代码"""
        source = "x" * (SourceCodeValidator.MAX_SOURCE_LENGTH + 1)
        result = validate_source(source)
        assert result.is_valid is False
        assert "过长" in result.errors[0]

    def test_validate_dangerous_import(self):
        """测试验证危险导入"""
        source = "导入 os"
        result = validate_source(source)
        assert result.is_valid is False
        assert any("os" in err for err in result.errors)

    def test_validate_bracket_mismatch(self):
        """测试验证括号不匹配"""
        source = "定 x = [1, 2, 3"
        result = validate_source(source, strict=True)
        assert len(result.warnings) > 0  # 应该有警告


class TestInputSanitizer:
    """输入清理器测试"""

    def test_sanitize_bom(self):
        """测试清理BOM标记"""
        source = '\ufeffprint("你好")'
        sanitized = sanitize_source(source)
        assert not sanitized.startswith("\ufeff")

    def test_sanitize_newlines(self):
        """测试规范化换行符"""
        source = "line1\r\nline2\rline3"
        sanitized = sanitize_source(source)
        assert "\r" not in sanitized

    def test_sanitize_trailing_whitespace(self):
        """测试移除尾部空白"""
        source = "line1   \nline2\t\t"
        sanitized = sanitize_source(source)
        lines = sanitized.split("\n")
        for line in lines:
            assert line == line.rstrip()

    def test_sanitize_multiple_blank_lines(self):
        """测试移除多余空行"""
        source = "line1\n\n\n\n\nline2"
        sanitized = sanitize_source(source)
        assert "\n\n\n" not in sanitized


class TestConvenienceFunctions:
    """便捷函数测试"""

    def test_execute_safely(self):
        """测试安全执行函数"""
        code = "result = 1 + 1"
        success, result, error = execute_safely(code)
        assert success is True
        assert error is None

    def test_create_safe_runtime(self):
        """测试创建安全运行时"""
        runtime = create_safe_runtime()
        assert isinstance(runtime, SecureRuntime)

    def test_create_safe_runtime_with_modules(self):
        """测试创建带自定义模块的安全运行时"""
        allowed_modules = {"math", "json"}
        runtime = create_safe_runtime(allowed_modules)
        assert runtime.allowed_modules == allowed_modules


class TestSecurityIntegration:
    """安全集成测试"""

    def test_full_security_workflow(self):
        """测试完整安全工作流"""
        # 1. 清理输入
        source = "  定 x = 5。  \n"
        sanitized = sanitize_source(source)

        # 2. 验证输入
        result = validate_source(sanitized)
        assert result.is_valid is True

        # 3. 执行代码（模拟）
        # 注意：这里需要先将心语代码编译为Python代码
        # 我们直接测试Python代码的执行
        python_code = "x = 5"
        success, _, error = execute_safely(python_code)
        assert success is True

    def test_security_with_chinese_operators(self):
        """测试中文操作符的安全性"""
        # 模拟包含中文操作符的代码
        python_code = "result = 1 + 2"  # 对应 "1加2"
        success, result, error = execute_safely(python_code)
        assert success is True

    def test_security_with_builtin_functions(self):
        """测试内置函数的安全性"""
        python_code = "result = len([1, 2, 3])"
        success, result, error = execute_safely(python_code)
        assert success is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
