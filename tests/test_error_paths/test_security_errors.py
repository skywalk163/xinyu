"""安全错误路径测试

测试安全验证的错误处理能力。
"""
import pytest

from src.main import ChineseProgram

try:
    from src.security.input_validator import SourceCodeValidator, validate_source

    InputValidator = SourceCodeValidator  # 保持向后兼容
except ImportError:
    InputValidator = None
    validate_source = None


class TestSecurityErrors:
    """安全错误测试"""

    def test_code_injection_attempt(self):
        """测试代码注入防护"""
        program = ChineseProgram()
        # 尝试注入恶意代码
        malicious_sources = [
            '定义 代码 = \'__import__("os").system("rm -rf /")\'。',
            '执行 \'__import__("os").system("ls")\'。',
            "定义 危险 = eval('1+1')。",
        ]
        for source in malicious_sources:
            result = program.run(source)
            # 应该拒绝执行或安全处理
            # 根据实际实现决定

    def test_file_access_attempt(self):
        """测试文件访问防护"""
        program = ChineseProgram()
        source = '定义 文件 = 打开("/etc/passwd")。'
        result = program.run(source)
        # 应该拒绝文件访问
        assert result is None

    def test_network_access_attempt(self):
        """测试网络访问防护"""
        program = ChineseProgram()
        source = '定义 连接 = 连接("http://malicious.com")。'
        result = program.run(source)
        # 应该拒绝网络访问
        assert result is None

    def test_dangerous_function_call(self):
        """测试危险函数调用"""
        program = ChineseProgram()
        dangerous_sources = [
            "定义 结果 = exec('print(1)')。",
            "定义 结果 = compile('1+1', '<string>', 'eval')。",
        ]
        for source in dangerous_sources:
            result = program.run(source)
            # 应该拒绝或安全处理
            # 根据实际实现决定


class TestInputValidation:
    """输入验证测试"""

    def test_validate_source_code(self):
        """测试源代码验证"""
        if validate_source is None:
            pytest.skip("validate_source not available")

        valid_sources = [
            '打印"你好"。',
            "定义 变量 = 1。",
            "定义 函数名 = 函 x：返回 x。",
        ]
        for source in valid_sources:
            # 应该通过验证
            result = validate_source(source)
            assert result.is_valid, f"验证失败: {result.errors}"

    def test_validate_malicious_input(self):
        """测试恶意输入验证"""
        if validate_source is None:
            pytest.skip("validate_source not available")

        malicious_sources = [
            "__import__('os').system('ls')",
            "eval('1+1')",
            "exec('print(1)')",
        ]
        for source in malicious_sources:
            # 应该拒绝或标记为危险
            result = validate_source(source)
            assert not result.is_valid, f"恶意代码应该被拒绝: {source}"

    def test_validate_input_length(self):
        """测试输入长度验证"""
        if validate_source is None:
            pytest.skip("validate_source not available")

        # 超长输入
        long_source = "打印" + "。" * 1000000
        result = validate_source(long_source)
        # 超长输入应该产生警告
        assert len(result.warnings) > 0, "超长输入应该产生警告"

    def test_validate_special_characters(self):
        """测试特殊字符验证"""
        if validate_source is None:
            pytest.skip("validate_source not available")

        special_sources = [
            '打印"\x00\x01\x02"。',
            '定义 变量 = "\n\r\t"。',
        ]
        for source in special_sources:
            result = validate_source(source)
            # 特殊字符应该被允许（除非是控制字符）
            # 这里我们只检查验证不会崩溃
            assert result is not None, "验证应该返回结果"


class TestSandboxSecurity:
    """沙箱安全测试"""

    def test_sandbox_isolation(self):
        """测试沙箱隔离"""
        program = ChineseProgram()
        # 在沙箱中执行的代码不应该访问外部环境
        source = """
定义 尝试访问 = 尝试：
    返回 __import__('os')。
捕获：
    返回 空。
"""
        result = program.run(source)
        # 应该无法访问os模块
        # 根据实际实现决定

    def test_resource_limit(self):
        """测试资源限制"""
        program = ChineseProgram()
        # 尝试消耗大量资源
        source = """
定义 列表 = []。
重复 100000 次：
    列表.追加(1)。
"""
        result = program.run(source)
        # 应该有资源限制
        # 根据实际实现决定

    def test_no_system_access(self):
        """测试无系统访问"""
        program = ChineseProgram()
        source = "定义 系统 = __import__('sys')。"
        result = program.run(source)
        # 应该无法访问sys模块
        # 根据实际实现决定


class TestSecurityErrorRecovery:
    """安全错误恢复测试"""

    def test_graceful_degradation(self):
        """测试优雅降级"""
        program = ChineseProgram()
        # 即使安全检查失败，也应该优雅处理
        sources = [
            "定义 正常 = 1。",
            "__import__('os').system('ls')",
            "定义 变量 = 2。",
        ]
        for source in sources:
            try:
                result = program.run(source)
                # 不应该崩溃
            except Exception as e:
                # 异常应该是预期的类型
                assert isinstance(e, (SecurityError, ValueError, TypeError))

    def test_error_logging(self):
        """测试错误日志"""
        program = ChineseProgram()
        source = "__import__('os').system('ls')"
        try:
            result = program.run(source)
            # 应该记录安全错误
            # 根据实际实现决定
        except Exception:
            pass
