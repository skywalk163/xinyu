from src.lexer.lexer import Lexer
from src.parser.parser import Parser

source = "平方根 16 相加 平方根 25。"
lexer = Lexer(source)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

print("Source:", source)
print("AST:", ast)
print("Statement:", ast.statements[0])
print("Type:", type(ast.statements[0]).__name__)

if hasattr(ast.statements[0], "left"):
    print("Left:", ast.statements[0].left)
    print("Left type:", type(ast.statements[0].left).__name__)
if hasattr(ast.statements[0], "operator"):
    print("Operator:", ast.statements[0].operator)
if hasattr(ast.statements[0], "right"):
    print("Right:", ast.statements[0].right)
    print("Right type:", type(ast.statements[0].right).__name__)
if hasattr(ast.statements[0], "args"):
    print("Args:", ast.statements[0].args)
