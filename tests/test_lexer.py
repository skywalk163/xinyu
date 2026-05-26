# tests/test_lexer.py
import pytest
from src.lexer.tokens import Token, TokenType

def test_token_creation():
    token = Token(TokenType.NUMBER, "123", 1, 0)
    assert token.type == TokenType.NUMBER
    assert token.value == "123"
    assert token.line == 1
    assert token.column == 0

def test_token_string_representation():
    token = Token(TokenType.STRING, "你好", 1, 0)
    assert str(token) == "Token(STRING, '你好', line=1, col=0)"

def test_token_equality():
    token1 = Token(TokenType.NUMBER, "123", 1, 0)
    token2 = Token(TokenType.NUMBER, "123", 1, 0)
    assert token1 == token2


# ===== 任务3：中文关键字定义测试 =====
from src.lexer.keywords import CORE_KEYWORDS, SYNTAX_MARKERS, OPERATORS

def test_core_keywords():
    """核心关键字只有5个"""
    assert CORE_KEYWORDS["定义"] == TokenType.VAR
    assert CORE_KEYWORDS["函数"] == TokenType.FUNCTION
    assert CORE_KEYWORDS["如果"] == TokenType.IF
    assert CORE_KEYWORDS["真值"] == TokenType.TRUE
    assert CORE_KEYWORDS["假值"] == TokenType.FALSE

def test_syntax_markers():
    """语法标记（非关键字）"""
    assert SYNTAX_MARKERS["那么"] == TokenType.THEN
    assert SYNTAX_MARKERS["否则"] == TokenType.ELSE
    assert SYNTAX_MARKERS["循环"] == TokenType.FOR
    assert SYNTAX_MARKERS["当满足"] == TokenType.WHILE

def test_operators():
    """操作符（函数，非关键字）"""
    assert OPERATORS["相加"] == TokenType.PLUS
    assert OPERATORS["相减"] == TokenType.MINUS
    assert OPERATORS["相乘"] == TokenType.MULTIPLY
    assert OPERATORS["相除"] == TokenType.DIVIDE


# ===== 任务4：词法分析器基础测试 =====
from src.lexer.lexer import Lexer

def test_lexer_number():
    """词法分析器：数字"""
    lexer = Lexer("123")
    tokens = lexer.tokenize()
    assert len(tokens) == 2  # NUMBER + EOF
    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].value == 123

def test_lexer_string():
    """词法分析器：字符串"""
    lexer = Lexer('"你好世界"')
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "你好世界"

def test_lexer_identifier():
    """词法分析器：标识符"""
    lexer = Lexer("用户数据")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == "用户数据"

def test_lexer_keyword():
    """词法分析器：关键字"""
    lexer = Lexer("如果")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.IF


# ===== 任务4：词法分析器增强测试 =====

def test_lexer_float():
    """词法分析器：浮点数"""
    lexer = Lexer("3.14")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].value == 3.14

def test_lexer_indent():
    """词法分析器：缩进处理"""
    source = """定义 x = 1。
  定义 y = 2。"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    # 查找 INDENT token
    indent_tokens = [t for t in tokens if t.type == TokenType.INDENT]
    assert len(indent_tokens) == 1
    assert indent_tokens[0].value == 2

def test_lexer_dedent():
    """词法分析器：DEDENT处理"""
    source = """定义 x = 1。
  定义 y = 2。
定义 z = 3。"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    # 查找 INDENT 和 DEDENT tokens
    indent_tokens = [t for t in tokens if t.type == TokenType.INDENT]
    dedent_tokens = [t for t in tokens if t.type == TokenType.DEDENT]

    assert len(indent_tokens) == 1
    assert len(dedent_tokens) == 1

def test_lexer_comment():
    """词法分析器：注释处理"""
    lexer = Lexer("定义 x = 1。 -- 这是注释\n定义 y = 2。")
    tokens = lexer.tokenize()

    # 注释应该被跳过，不应该出现在 tokens 中
    comment_tokens = [t for t in tokens if "注释" in str(t.value)]
    assert len(comment_tokens) == 0

    # 应该有两个 VAR 关键字
    var_tokens = [t for t in tokens if t.type == TokenType.VAR]
    assert len(var_tokens) == 2

def test_lexer_string_escape_newline():
    """词法分析器：字符串转义 - 换行符"""
    lexer = Lexer('"第一行\\n第二行"')
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "第一行\n第二行"

def test_lexer_string_escape_tab():
    """词法分析器：字符串转义 - 制表符"""
    lexer = Lexer('"列1\\t列2"')
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "列1\t列2"

def test_lexer_string_escape_quote():
    """词法分析器：字符串转义 - 引号"""
    lexer = Lexer('"他说\\"你好\\""')
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == '他说"你好"'

def test_lexer_string_escape_backslash():
    """词法分析器：字符串转义 - 反斜杠"""
    lexer = Lexer('"路径：C:\\\\Users"')
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "路径：C:\\Users"

def test_lexer_string_escape_multiple():
    """词法分析器：字符串转义 - 多个转义字符"""
    lexer = Lexer('"行1\\n行2\\t缩进\\\\反斜杠\\"引号\\""')
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == '行1\n行2\t缩进\\反斜杠"引号"'

def test_lexer_unterminated_string():
    """词法分析器：未闭合字符串错误"""
    from src.lexer.lexer import LexerError

    lexer = Lexer('"未闭合的字符串')
    with pytest.raises(LexerError) as exc_info:
        lexer.tokenize()

    assert "Unterminated string" in str(exc_info.value)

def test_lexer_invalid_number_multiple_dots():
    """词法分析器：非法数字（多个小数点）"""
    from src.lexer.lexer import LexerError

    lexer = Lexer("1.2.3")
    with pytest.raises(LexerError) as exc_info:
        lexer.tokenize()

    assert "multiple decimal points" in str(exc_info.value)

def test_lexer_unexpected_character():
    """词法分析器：非法字符"""
    from src.lexer.lexer import LexerError

    lexer = Lexer("定义 x = @")
    with pytest.raises(LexerError) as exc_info:
        lexer.tokenize()

    assert "Unexpected character" in str(exc_info.value)

def test_lexer_multiple_indent_levels():
    """词法分析器：多层缩进"""
    source = """定义 a = 1。
  定义 b = 2。
    定义 c = 3。
  定义 d = 4。
定义 e = 5。"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    indent_tokens = [t for t in tokens if t.type == TokenType.INDENT]
    dedent_tokens = [t for t in tokens if t.type == TokenType.DEDENT]

    # 应该有 2 个 INDENT（2空格和4空格）
    assert len(indent_tokens) == 2
    # 应该有 2 个 DEDENT（从4回到2，从2回到0）
    assert len(dedent_tokens) == 2

def test_lexer_empty_source():
    """词法分析器：空源代码"""
    lexer = Lexer("")
    tokens = lexer.tokenize()

    assert len(tokens) == 1
    assert tokens[0].type == TokenType.EOF

def test_lexer_only_comments():
    """词法分析器：只有注释"""
    lexer = Lexer("-- 这是注释\n-- 另一行注释")
    tokens = lexer.tokenize()

    # 应该只有 NEWLINE 和 EOF（注释被跳过）
    non_eof_tokens = [t for t in tokens if t.type != TokenType.EOF]
    assert all(t.type == TokenType.NEWLINE for t in non_eof_tokens)
    assert tokens[-1].type == TokenType.EOF

def test_lexer_chinese_operators():
    """词法分析器：中文操作符"""
    lexer = Lexer("相加 相减 相乘 相除")
    tokens = lexer.tokenize()

    operator_types = [TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE]
    for i, expected_type in enumerate(operator_types):
        assert tokens[i].type == expected_type

def test_lexer_symbols():
    """词法分析器：符号"""
    lexer = Lexer("，。：（）【】")
    tokens = lexer.tokenize()

    expected_types = [
        TokenType.COMMA,
        TokenType.PERIOD,
        TokenType.COLON,
        TokenType.LPAREN,
        TokenType.RPAREN,
        TokenType.LBRACKET,
        TokenType.RBRACKET,
    ]

    for i, expected_type in enumerate(expected_types):
        assert tokens[i].type == expected_type


# ===== 任务5：词法分析器高级特性测试 =====

def test_lexer_math_expression():
    """词法分析器：数学表达式 $()"""
    lexer = Lexer('$(π * r²)')
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.DOLLAR
    assert tokens[1].type == TokenType.LPAREN

def test_lexer_python_block():
    """词法分析器：Python代码块 {{}}"""
    lexer = Lexer('{{import pandas}}')
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.LBRACE

def test_lexer_indentation():
    """词法分析器：缩进处理（任务4已实现，此测试验证）"""
    source = """若条件：
  动作。
否则：
  其他动作。"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    assert TokenType.INDENT in [t.type for t in tokens]
    assert TokenType.DEDENT in [t.type for t in tokens]

def test_lexer_mixed_chinese_english():
    """词法分析器：混合中英文标识符"""
    lexer = Lexer('用户name = "张三"')
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == "用户name"
