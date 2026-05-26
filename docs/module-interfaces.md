# 心语语言模块接口文档

## 1. Lexer模块（词法分析器）

### 1.1 模块概述

**路径**：`src/lexer/`  
**职责**：将源代码字符串转换为Token序列  
**主要文件**：
- `lexer.py`：词法分析器实现
- `tokens.py`：Token定义
- `keywords.py`：关键字映射

### 1.2 公共接口

#### Lexer类

```python
class Lexer:
    """词法分析器
    
    将源代码字符串转换为Token序列。
    """
    
    def __init__(self, source: str):
        """初始化词法分析器
        
        Args:
            source: 源代码字符串
        """
        ...
    
    def tokenize(self) -> List[Token]:
        """执行词法分析
        
        Returns:
            Token列表
            
        Raises:
            LexerError: 词法错误
        """
        ...
```

#### Token类

```python
@dataclass
class Token:
    """Token数据结构"""
    type: TokenType      # Token类型
    value: Any          # Token值
    line: int           # 所在行号
    column: int         # 所在列号
```

#### TokenType枚举

```python
class TokenType(Enum):
    """Token类型枚举"""
    # 字面量
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    
    # 关键字
    VAR = auto()        # 定
    FUNCTION = auto()   # 函
    IF = auto()         # 若
    TRUE = auto()       # 真值
    FALSE = auto()      # 假值
    
    # 操作符
    PLUS = auto()       # 加
    MINUS = auto()      # 减
    MULTIPLY = auto()   # 乘
    DIVIDE = auto()     # 除以
    
    # 其他...
```

### 1.3 使用示例

```python
from src.lexer.lexer import Lexer

source = '定 x = 5。'
lexer = Lexer(source)
tokens = lexer.tokenize()

for token in tokens:
    print(f"{token.type}: {token.value} (行{token.line}, 列{token.column})")
```

---

## 2. Parser模块（语法分析器）

### 2.1 模块概述

**路径**：`src/parser/`  
**职责**：将Token序列转换为抽象语法树（AST）  
**主要文件**：
- `parser.py`：语法分析器实现
- `ast_nodes.py`：AST节点定义

### 2.2 公共接口

#### Parser类

```python
class Parser:
    """语法分析器
    
    将Token序列转换为抽象语法树。
    """
    
    def __init__(self, tokens: List[Token]):
        """初始化语法分析器
        
        Args:
            tokens: Token列表
        """
        ...
    
    def parse(self) -> ProgramNode:
        """执行语法分析
        
        Returns:
            程序根节点（AST）
            
        Raises:
            ParseError: 语法错误
        """
        ...
```

#### AST节点类

```python
@dataclass
class ASTNode:
    """AST节点基类"""
    pass

@dataclass
class ProgramNode(ASTNode):
    """程序根节点"""
    statements: List[ASTNode]

@dataclass
class VarDefNode(ASTNode):
    """变量定义节点"""
    name: str
    value: ASTNode
    line: int

@dataclass
class FunctionDefNode(ASTNode):
    """函数定义节点"""
    name: str
    params: List[str]
    body: List[ASTNode]
    line: int

# 其他节点类型...
```

### 2.3 使用示例

```python
from src.lexer.lexer import Lexer
from src.parser.parser import Parser

source = '定 x = 5。'
lexer = Lexer(source)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

print(f"程序包含{len(ast.statements)}个语句")
```

---

## 3. Semantic模块（语义分析器）

### 3.1 模块概述

**路径**：`src/semantic/`  
**职责**：检查AST的语义正确性，构建符号表  
**主要文件**：
- `analyzer.py`：语义分析器实现
- `scope.py`：作用域管理
- `type_inference.py`：类型推断

### 3.2 公共接口

#### SemanticAnalyzer类

```python
class SemanticAnalyzer:
    """语义分析器
    
    检查AST的语义正确性，构建符号表。
    """
    
    def __init__(self):
        """初始化语义分析器"""
        ...
    
    def analyze(self, ast: ProgramNode) -> bool:
        """执行语义分析
        
        Args:
            ast: 抽象语法树
            
        Returns:
            是否通过分析
        """
        ...
    
    @property
    def errors(self) -> List[SemanticError]:
        """获取语义错误列表
        
        Returns:
            错误列表
        """
        ...
    
    @property
    def symbol_table(self) -> Dict:
        """获取符号表
        
        Returns:
            符号表字典
        """
        ...
```

#### Scope类

```python
class Scope:
    """作用域管理"""
    
    def define(self, name: str, symbol_type: str, **attrs) -> None:
        """定义符号
        
        Args:
            name: 符号名
            symbol_type: 符号类型
            **attrs: 其他属性
        """
        ...
    
    def resolve(self, name: str) -> Optional[Symbol]:
        """查找符号
        
        Args:
            name: 符号名
            
        Returns:
            符号对象，如果未找到则返回None
        """
        ...
```

### 3.3 使用示例

```python
from src.semantic.analyzer import SemanticAnalyzer

analyzer = SemanticAnalyzer()
if analyzer.analyze(ast):
    print("语义分析通过")
    print(f"符号表: {analyzer.symbol_table}")
else:
    for error in analyzer.errors:
        print(f"错误: {error.message}")
```

---

## 4. Codegen模块（代码生成器）

### 4.1 模块概述

**路径**：`src/codegen/`  
**职责**：将AST转换为目标代码（Python）  
**主要文件**：
- `python_codegen.py`：Python代码生成器实现

### 4.2 公共接口

#### PythonCodegen类

```python
class PythonCodegen:
    """Python代码生成器
    
    将AST转换为可执行的Python代码。
    """
    
    def generate(self, ast: ProgramNode) -> str:
        """生成Python代码
        
        Args:
            ast: 抽象语法树
            
        Returns:
            Python代码字符串
            
        Raises:
            CodegenError: 代码生成错误
        """
        ...
```

### 4.3 使用示例

```python
from src.codegen.python_codegen import PythonCodegen

codegen = PythonCodegen()
python_code = codegen.generate(ast)
print("生成的Python代码:")
print(python_code)
```

---

## 5. Macro模块（宏系统）

### 5.1 模块概述

**路径**：`src/macro/`  
**职责**：宏定义、展开和代码变换  
**主要文件**：
- `macro_system.py`：宏系统核心
- `macro_expander.py`：宏展开器
- `builtin_macros.py`：内置宏
- `idiom_macros.py`：成语宏

### 5.2 公共接口

#### MacroSystem类

```python
class MacroSystem:
    """宏系统核心"""
    
    def register(self, name: str, macro: Macro) -> None:
        """注册宏
        
        Args:
            name: 宏名称
            macro: 宏对象
        """
        ...
    
    def expand(self, name: str, args: Dict[str, Any]) -> str:
        """展开宏
        
        Args:
            name: 宏名称
            args: 宏参数
            
        Returns:
            展开后的代码
        """
        ...
```

#### Macro类

```python
@dataclass
class Macro:
    """宏定义"""
    name: str                      # 宏名称
    type: MacroType                # 宏类型
    params: List[str]              # 参数列表
    body: str                      # 宏体
    description: Optional[str]     # 描述
```

### 5.3 使用示例

```python
from src.macro.macro_system import MacroSystem

macro_system = MacroSystem()
macro_system.register("for_loop", for_loop_macro)
expanded_code = macro_system.expand("for_loop", {"var": "i", "list": "[1,2,3]"})
```

---

## 6. Runtime模块（运行时环境）

### 6.1 模块概述

**路径**：`src/runtime/`  
**职责**：执行生成的代码，提供安全执行环境  
**主要文件**：
- `secure_runtime.py`：安全运行时实现

### 6.2 公共接口

#### SecureRuntime类

```python
class SecureRuntime:
    """安全运行时环境
    
    使用RestrictedPython实现安全的代码执行。
    """
    
    def __init__(self, allowed_modules: Optional[Set[str]] = None):
        """初始化安全运行时
        
        Args:
            allowed_modules: 允许的模块集合
        """
        ...
    
    def execute(self, code: str, validate: bool = True) -> Tuple[bool, Optional[Any], Optional[str]]:
        """执行代码
        
        Args:
            code: Python代码字符串
            validate: 是否进行输入验证
            
        Returns:
            (是否成功, 结果, 错误信息)
        """
        ...
    
    def compile_restricted_code(self, code: str) -> Tuple[bool, Optional[Any], Optional[str]]:
        """编译受限代码（不执行）
        
        Args:
            code: Python代码字符串
            
        Returns:
            (是否成功, 字节码, 错误信息)
        """
        ...
```

### 6.3 使用示例

```python
from src.runtime.secure_runtime import SecureRuntime

runtime = SecureRuntime()
code = 'result = 1 + 1'
success, result, error = runtime.execute(code)

if success:
    print(f"执行成功: {result}")
else:
    print(f"执行失败: {error}")
```

---

## 7. Security模块（安全模块）

### 7.1 模块概述

**路径**：`src/security/`  
**职责**：输入验证和清理  
**主要文件**：
- `input_validator.py`：输入验证器

### 7.2 公共接口

#### SourceCodeValidator类

```python
class SourceCodeValidator:
    """源代码验证器"""
    
    @classmethod
    def validate(cls, source: str, strict: bool = True) -> ValidationResult:
        """验证源代码
        
        Args:
            source: 源代码字符串
            strict: 是否启用严格模式
            
        Returns:
            验证结果对象
        """
        ...
```

#### InputSanitizer类

```python
class InputSanitizer:
    """输入清理器"""
    
    @classmethod
    def sanitize(cls, source: str) -> str:
        """清理源代码
        
        Args:
            source: 原始源代码
            
        Returns:
            清理后的源代码
        """
        ...
```

### 7.3 使用示例

```python
from src.security.input_validator import validate_source, sanitize_source

# 清理输入
source = '  定 x = 5。  \n'
sanitized = sanitize_source(source)

# 验证输入
result = validate_source(sanitized)

if result.is_valid:
    print("验证通过")
else:
    print(f"验证失败: {result.errors}")
```

---

## 8. ErrorHandling模块（错误处理）

### 8.1 模块概述

**路径**：`src/error_handling.py`  
**职责**：统一错误处理和报告  

### 8.2 公共接口

#### 错误类层次

```python
class XinyuError(Exception):
    """心语语言基础异常"""
    pass

class LexerError(XinyuError):
    """词法错误"""
    pass

class ParseError(XinyuError):
    """语法错误"""
    pass

class SemanticError(XinyuError):
    """语义错误"""
    pass

class CodegenError(XinyuError):
    """代码生成错误"""
    pass

class RuntimeError(XinyuError):
    """运行时错误"""
    pass
```

---

## 9. Main模块（主程序）

### 9.1 模块概述

**路径**：`src/main.py`  
**职责**：编译流程编排，提供REPL和命令行接口  

### 9.2 公共接口

#### ChineseProgram类

```python
class ChineseProgram:
    """心语语言主类
    
    提供完整的编译和执行功能。
    """
    
    def run(self, source: str) -> Optional[Any]:
        """编译并执行心语代码
        
        Args:
            source: 心语源代码
            
        Returns:
            执行结果（如果有），或None（如果出错）
        """
        ...
    
    def compile(self, source: str) -> str:
        """编译心语代码为Python代码
        
        Args:
            source: 心语源代码
            
        Returns:
            生成的Python代码字符串
        """
        ...
```

### 9.3 使用示例

```python
from src.main import ChineseProgram

program = ChineseProgram()

# 执行代码
result = program.run('定 x = 5。印x。')

# 编译代码
python_code = program.compile('定 x = 5。')
```

---

## 10. 模块交互示例

### 10.1 完整编译流程

```python
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.codegen.python_codegen import PythonCodegen
from src.runtime.secure_runtime import SecureRuntime

# 1. 词法分析
source = '定 x = 5。印x。'
lexer = Lexer(source)
tokens = lexer.tokenize()

# 2. 语法分析
parser = Parser(tokens)
ast = parser.parse()

# 3. 语义分析
analyzer = SemanticAnalyzer()
if not analyzer.analyze(ast):
    for error in analyzer.errors:
        print(f"错误: {error.message}")
    exit(1)

# 4. 代码生成
codegen = PythonCodegen()
python_code = codegen.generate(ast)

# 5. 执行
runtime = SecureRuntime()
success, result, error = runtime.execute(python_code)

if success:
    print(f"执行成功: {result}")
else:
    print(f"执行失败: {error}")
```

### 10.2 使用便捷接口

```python
from src.main import ChineseProgram

program = ChineseProgram()
result = program.run('定 x = 5。印x。')
```
