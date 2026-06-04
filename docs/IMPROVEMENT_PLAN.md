# 心语项目改进实施计划

**创建日期**：2026-06-04  
**Python版本要求**：3.12+（优先支持3.12，学有余力支持3.13和3.14）  
**目标**：系统性地改进心语项目，确保无遗漏

---

## 📋 总体目标

1. 修复所有核心功能问题（25个失败测试）
2. 优化性能并建立性能基准
3. 完善生态系统（包管理、标准库、IDE支持）
4. 增强类型系统
5. 完善文档和示例
6. 提升代码质量

---

## 🎯 阶段一：核心功能完善（优先级：最高）

### 任务1.1：修复语法解析器问题

**问题描述**：12个测试失败，涉及while循环、for循环、字典字面量、函数参数解析

**失败测试清单**：
- [ ] test_while_loop - while循环语法解析
- [ ] test_for_loop - for循环语法解析
- [ ] test_dict_literal - 字典字面量词法分析
- [ ] test_function_with_parameters - 函数参数语法

**实施步骤**：

#### 步骤1.1.1：分析失败测试
```bash
# 运行失败的测试，收集详细错误信息
pytest tests/test_parser.py::test_while_loop -v
pytest tests/test_parser.py::test_for_loop -v
pytest tests/test_parser.py::test_dict_literal -v
pytest tests/test_parser.py::test_function_with_parameters -v
```

#### 步骤1.1.2：修复while循环解析
**文件**：`src/parser/parser.py`  
**位置**：`parse_while_statement` 方法  
**问题**：Unexpected token: COLON  
**修复方案**：
1. 检查while循环的语法规则
2. 修复冒号处理逻辑
3. 添加测试验证

#### 步骤1.1.3：修复for循环解析
**文件**：`src/parser/parser.py`  
**位置**：`parse_for_statement` 方法  
**问题**：Unexpected token: IN  
**修复方案**：
1. 检查for循环的语法规则
2. 修复"遍历"关键字处理
3. 添加测试验证

#### 步骤1.1.4：修复字典字面量解析
**文件**：`src/lexer/lexer.py` 和 `src/parser/parser.py`  
**问题**：词法错误: Unexpected character: :  
**修复方案**：
1. 在词法分析器中添加冒号支持
2. 在语法分析器中添加字典解析逻辑
3. 添加测试验证

#### 步骤1.1.5：修复函数参数解析
**文件**：`src/parser/parser.py`  
**位置**：`parse_function_def` 方法  
**问题**：Expected '：' after function parameters  
**修复方案**：
1. 检查函数定义的语法规则
2. 修复参数列表解析
3. 添加测试验证

**验证标准**：
- [ ] 所有语法解析测试通过
- [ ] 无回归问题
- [ ] 错误提示清晰友好

---

### 任务1.2：修复语义分析器问题

**问题描述**：5个测试失败，涉及参数检查、返回语句验证、字典操作

**失败测试清单**：
- [ ] test_function_call_with_correct_args - 参数解析
- [ ] test_return_outside_function - 返回语句检查
- [ ] test_dict_operations - 字典操作语义
- [ ] test_wrong_argument_count - 参数数量检查

**实施步骤**：

#### 步骤1.2.1：完善参数验证
**文件**：`src/semantic/analyzer.py`  
**修复方案**：
1. 实现函数调用参数数量检查
2. 添加参数类型检查
3. 提供清晰的错误信息

#### 步骤1.2.2：完善返回语句检查
**文件**：`src/semantic/analyzer.py`  
**修复方案**：
1. 跟踪当前是否在函数内
2. 检查返回语句的上下文
3. 验证返回值类型

#### 步骤1.2.3：完善字典操作语义
**文件**：`src/semantic/analyzer.py`  
**修复方案**：
1. 添加字典类型推断
2. 检查字典访问操作
3. 验证键值类型

**验证标准**：
- [ ] 所有语义分析测试通过
- [ ] 类型推断正确
- [ ] 错误检测完整

---

### 任务1.3：修复集成测试问题

**问题描述**：3个测试失败，涉及fibonacci、内置函数、完整流程

**失败测试清单**：
- [ ] test_fibonacci - 函数调用参数问题
- [ ] test_builtin_function - 内置函数集成
- [ ] test_full_pipeline - 完整流程

**实施步骤**：

#### 步骤1.3.1：修复fibonacci测试
**问题**：函数调用参数传递问题  
**修复方案**：
1. 检查函数调用的参数传递机制
2. 验证递归函数的正确性
3. 添加更多递归测试

#### 步骤1.3.2：修复内置函数集成
**问题**：内置函数调用问题  
**修复方案**：
1. 检查内置函数注册
2. 验证参数传递
3. 测试所有内置函数

#### 步骤1.3.3：修复完整流程测试
**问题**：编译到执行的完整流程  
**修复方案**：
1. 测试词法分析 → 语法分析 → 语义分析 → 代码生成 → 执行
2. 验证每个阶段的正确性
3. 添加端到端测试

**验证标准**：
- [ ] 所有集成测试通过
- [ ] 完整编译流程正确
- [ ] 执行结果正确

---

### 任务1.4：修复宏展开问题

**问题描述**：3个测试失败，涉及AST展开、循环宏

**失败测试清单**：
- [ ] test_expand_ast_repeat_node_with_macro
- [ ] test_expand_for_loop_method
- [ ] test_expand_repeat_loop_method

**实施步骤**：

#### 步骤1.4.1：修复AST展开
**文件**：`src/macro/macro_expander.py`  
**修复方案**：
1. 检查AST节点展开逻辑
2. 修复节点转换
3. 验证展开结果

#### 步骤1.4.2：修复循环宏展开
**文件**：`src/macro/builtin_macros.py`  
**修复方案**：
1. 检查for循环宏定义
2. 检查repeat循环宏定义
3. 验证宏展开结果

**验证标准**：
- [ ] 所有宏测试通过
- [ ] 宏展开正确
- [ ] 无性能问题

---

### 任务1.5：修复其他问题

**问题描述**：2个测试失败

**失败测试清单**：
- [ ] test_function_call - 函数调用解析
- [ ] test_execute_print - 安全运行时执行

**实施步骤**：

#### 步骤1.5.1：修复函数调用解析
**文件**：`src/parser/parser.py`  
**修复方案**：
1. 检查函数调用解析逻辑
2. 验证元数驱动解析
3. 添加更多测试

#### 步骤1.5.2：修复安全运行时
**文件**：`src/runtime/secure_runtime.py`  
**修复方案**：
1. 检查安全执行环境
2. 验证print函数执行
3. 测试安全限制

**验证标准**：
- [ ] 所有测试通过
- [ ] 无安全问题
- [ ] 执行正确

---

## 🎯 阶段二：性能优化（优先级：高）

### 任务2.1：建立性能测试框架

**实施步骤**：

#### 步骤2.1.1：创建性能测试目录
```bash
mkdir -p tests/test_performance
```

#### 步骤2.1.2：创建词法分析性能测试
**文件**：`tests/test_performance/test_lexer_performance.py`
```python
import pytest
import time
from src.lexer.lexer import Lexer

class TestLexerPerformance:
    """词法分析性能测试"""
    
    def test_large_file_lexing(self):
        """测试大文件词法分析性能"""
        # 生成10000行代码
        code = "\n".join([f'定义 x{i} = {i}。' for i in range(10000)])
        
        start = time.time()
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        elapsed = time.time() - start
        
        # 应该在1秒内完成
        assert elapsed < 1.0
        assert len(tokens) > 10000
```

#### 步骤2.1.3：创建语法分析性能测试
**文件**：`tests/test_performance/test_parser_performance.py`

#### 步骤2.1.4：创建代码生成性能测试
**文件**：`tests/test_performance/test_codegen_performance.py`

#### 步骤2.1.5：创建运行时性能测试
**文件**：`tests/test_performance/test_runtime_performance.py`

**验证标准**：
- [ ] 性能测试框架完整
- [ ] 基准数据收集
- [ ] 性能回归检测

---

### 任务2.2：优化编译流程

**实施步骤**：

#### 步骤2.2.1：添加编译缓存
**文件**：`src/cache/compile_cache.py`
```python
import hashlib
import pickle
from pathlib import Path

class CompileCache:
    """编译缓存管理器"""
    
    def __init__(self, cache_dir: str = ".xinyu_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_cache_key(self, source: str) -> str:
        """计算源码的缓存键"""
        return hashlib.md5(source.encode()).hexdigest()
    
    def get(self, source: str):
        """获取缓存的编译结果"""
        key = self.get_cache_key(source)
        cache_file = self.cache_dir / f"{key}.pkl"
        if cache_file.exists():
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        return None
    
    def set(self, source: str, result):
        """保存编译结果到缓存"""
        key = self.get_cache_key(source)
        cache_file = self.cache_dir / f"{key}.pkl"
        with open(cache_file, 'wb') as f:
            pickle.dump(result, f)
```

#### 步骤2.2.2：优化Token处理
**文件**：`src/lexer/optimized_lexer.py`  
**优化点**：
1. 使用生成器而非列表
2. 减少字符串拷贝
3. 优化关键字查找

#### 步骤2.2.3：优化AST构建
**文件**：`src/parser/parser.py`  
**优化点**：
1. 减少AST节点创建
2. 优化节点访问
3. 使用更高效的数据结构

**验证标准**：
- [ ] 编译速度提升30%+
- [ ] 内存占用减少
- [ ] 缓存命中率>80%

---

### 任务2.3：建立性能基准

**文件**：`docs/PERFORMANCE_BASELINE.md`

**基准指标**：
```markdown
# 性能基准

## 编译性能
- 词法分析：X 行/秒
- 语法分析：X 行/秒
- 代码生成：X 行/秒
- 完整编译：X 行/秒

## 执行性能
- 与Python对比：X%
- 函数调用开销：X ms
- 循环执行开销：X ms

## 内存占用
- 编译时内存：X MB
- 运行时内存：X MB
```

**验证标准**：
- [ ] 基准数据完整
- [ ] 定期回归测试
- [ ] 性能监控图表

---

## 🎯 阶段三：生态建设（优先级：高）

### 任务3.1：完善包管理器

**实施步骤**：

#### 步骤3.1.1：设计包规范
**文件**：`docs/PACKAGE_SPEC.md`
```markdown
# 心语包规范

## 包结构
my_package/
├── package.json       # 包配置
├── README.md          # 包说明
├── lib/               # 包源码
│   └── main.yan
└── tests/             # 包测试
    └── test_main.yan

## package.json 格式
{
  "name": "my-package",
  "version": "1.0.0",
  "description": "包描述",
  "main": "lib/main.yan",
  "dependencies": {
    "other-package": "^2.0.0"
  }
}
```

#### 步骤3.1.2：实现包管理器
**文件**：`tools/package_manager.py`
```python
class PackageManager:
    """心语包管理器"""
    
    def install(self, package_name: str, version: str = None):
        """安装包"""
        # 1. 从仓库获取包信息
        # 2. 下载包文件
        # 3. 解析依赖
        # 4. 安装依赖
        # 5. 验证安装
        pass
    
    def uninstall(self, package_name: str):
        """卸载包"""
        pass
    
    def update(self, package_name: str = None):
        """更新包"""
        pass
    
    def search(self, keyword: str):
        """搜索包"""
        pass
    
    def publish(self, package_path: str):
        """发布包"""
        pass
```

#### 步骤3.1.3：创建包仓库
**文件**：`tools/package_repository.py`
```python
class PackageRepository:
    """包仓库管理"""
    
    def __init__(self, repo_url: str = "https://packages.xinyu-lang.org"):
        self.repo_url = repo_url
    
    def get_package_info(self, name: str) -> dict:
        """获取包信息"""
        pass
    
    def download_package(self, name: str, version: str) -> str:
        """下载包"""
        pass
```

**验证标准**：
- [ ] 包安装/卸载正常
- [ ] 依赖解析正确
- [ ] 版本管理完善

---

### 任务3.2：开发标准库

**实施步骤**：

#### 步骤3.2.1：完善现有标准库
**文件**：`stdlib/io.yan`, `stdlib/math.yan`, `stdlib/net.yan`

#### 步骤3.2.2：开发新的标准库模块
```
stdlib/
├── io.yan           # IO操作（完善）
├── math.yan         # 数学运算（新建）
├── string.yan       # 字符串处理（新建）
├── collection.yan   # 集合操作（新建）
├── net.yan          # 网络编程（完善）
├── file.yan         # 文件操作（新建）
├── json.yan         # JSON处理（新建）
└── datetime.yan     # 日期时间（新建）
```

#### 步骤3.2.3：编写标准库文档
**文件**：`docs/STDLIB_REFERENCE.md`

**验证标准**：
- [ ] 标准库功能完整
- [ ] 测试覆盖率高
- [ ] 文档完善

---

### 任务3.3：增强IDE支持

**实施步骤**：

#### 步骤3.3.1：增强VSCode扩展
**文件**：`tools/vscode-extension/`

**功能清单**：
- [x] 语法高亮
- [x] 代码片段
- [ ] 智能提示（IntelliSense）
- [ ] 错误检查（Diagnostics）
- [ ] 代码格式化（Formatting）
- [ ] 调试支持（Debug）
- [ ] 定义跳转（Go to Definition）
- [ ] 查找引用（Find References）

#### 步骤3.3.2：实现语言服务器
**文件**：`tools/vscode-extension/src/language-server.ts`
```typescript
class XinyuLanguageServer {
    // 提供智能提示
    provideCompletionItems(document, position): CompletionItem[]
    
    // 提供错误诊断
    provideDiagnostics(document): Diagnostic[]
    
    // 提供格式化
    provideDocumentFormattingEdits(document): TextEdit[]
    
    // 提供定义跳转
    provideDefinition(document, position): Location
}
```

#### 步骤3.3.3：实现调试适配器
**文件**：`tools/vscode-extension/src/debug-adapter.ts`

**验证标准**：
- [ ] 智能提示正常
- [ ] 错误检查准确
- [ ] 调试功能完整

---

## 🎯 阶段四：类型系统增强（优先级：中）

### 任务4.1：完善类型推断

**实施步骤**：

#### 步骤4.1.1：实现表达式类型推断
**文件**：`src/semantic/type_inference.py`
```python
class TypeInference:
    """类型推断系统"""
    
    def infer_expression(self, expr: ASTNode) -> Type:
        """推断表达式类型"""
        if isinstance(expr, NumberNode):
            return IntType if isinstance(expr.value, int) else FloatType
        elif isinstance(expr, StringNode):
            return StringType
        elif isinstance(expr, BinaryOpNode):
            return self.infer_binary_op(expr)
        # ... 其他情况
```

#### 步骤4.1.2：实现函数返回类型推断
**文件**：`src/semantic/type_inference.py`
```python
def infer_function_return(self, func: FunctionDefNode) -> Type:
    """推断函数返回类型"""
    # 分析函数体中的返回语句
    # 推断返回值类型
    # 返回统一类型或Union类型
```

#### 步骤4.1.3：完成TODO项
**位置**：
- `src/semantic/analyzer.py:447` - 成员类型推断
- `src/semantic/type_inference.py:179` - 函数返回类型推断

**验证标准**：
- [ ] 类型推断准确率>90%
- [ ] 支持常见类型
- [ ] 错误提示清晰

---

### 任务4.2：添加类型注解支持

**实施步骤**：

#### 步骤4.2.1：设计类型注解语法
```yan
# 类型注解语法
定义 x: 整数 = 10。
定义 y: 浮点数 = 3.14。
定义 名称: 字符串 = "心语"。

定义 平方 = 函 x: 整数 -> 整数：
  返回 x 相乘 x。
。
```

#### 步骤4.2.2：实现类型注解解析
**文件**：`src/parser/parser.py`
```python
def parse_type_annotation(self) -> Type:
    """解析类型注解"""
    # 解析类型名称
    # 处理泛型类型
    # 处理联合类型
```

#### 步骤4.2.3：生成带类型的Python代码
**文件**：`src/codegen/python_codegen.py`
```python
def generate_with_types(self, ast: ASTNode) -> str:
    """生成带类型注解的Python代码"""
    # 在生成代码时添加类型注解
    # 例如：x: int = 10
```

**验证标准**：
- [ ] 类型注解语法清晰
- [ ] 解析正确
- [ ] 生成代码正确

---

### 任务4.3：增强编译时检查

**实施步骤**：

#### 步骤4.3.1：实现类型检查
**文件**：`src/semantic/type_checker.py`
```python
class TypeChecker:
    """类型检查器"""
    
    def check_assignment(self, lhs_type: Type, rhs_type: Type) -> bool:
        """检查赋值类型兼容"""
        pass
    
    def check_function_call(self, func_type: Type, arg_types: List[Type]) -> bool:
        """检查函数调用类型"""
        pass
    
    def check_binary_op(self, op: str, left_type: Type, right_type: Type) -> Type:
        """检查二元操作类型"""
        pass
```

#### 步骤4.3.2：实现未定义变量检查
#### 步骤4.3.3：实现参数数量检查

**验证标准**：
- [ ] 编译时捕获常见错误
- [ ] 错误信息准确
- [ ] 无误报

---

## 🎯 阶段五：文档完善（优先级：中）

### 任务5.1：生成API参考文档

**实施步骤**：

#### 步骤5.1.1：创建API文档目录
```bash
mkdir -p docs/api
```

#### 步骤5.1.2：生成内置函数文档
**文件**：`docs/api/builtin_functions.md`
```markdown
# 内置函数参考

## 数学函数

### abs(x)
返回数字的绝对值。

**参数**：
- x: 数字

**返回值**：数字

**示例**：
```yan
绝对值 -5  # 5
```

### max(*args)
返回最大值。

...
```

#### 步骤5.1.3：生成标准库文档
**文件**：`docs/api/stdlib_modules.md`

#### 步骤5.1.4：生成语言参考
**文件**：`docs/api/language_reference.md`

**验证标准**：
- [ ] API文档完整
- [ ] 示例代码正确
- [ ] 格式统一

---

### 任务5.2：编写系统教程

**实施步骤**：

#### 步骤5.2.1：创建教程目录
```bash
mkdir -p docs/tutorials
```

#### 步骤5.2.2：编写入门教程
**文件**：`docs/tutorials/01_getting_started.md`
```markdown
# 心语入门指南

## 1. 安装心语

## 2. 第一个程序

## 3. 基础语法

## 4. 下一步
```

#### 步骤5.2.3：编写进阶教程
```
docs/tutorials/
├── 01_getting_started.md    # 入门
├── 02_basic_syntax.md       # 基础语法
├── 03_variables.md          # 变量
├── 04_functions.md          # 函数
├── 05_control_flow.md       # 控制流
├── 06_data_structures.md    # 数据结构
├── 07_modules.md            # 模块
├── 08_error_handling.md     # 错误处理
└── 09_advanced.md           # 高级特性
```

**验证标准**：
- [ ] 教程循序渐进
- [ ] 示例可运行
- [ ] 覆盖所有主题

---

### 任务5.3：规范化示例代码

**实施步骤**：

#### 步骤5.3.1：统一示例风格
**规范**：
- 使用规范关键字（打印而非印）
- 添加详细注释
- 提供预期输出
- 遵循代码风格指南

#### 步骤5.3.2：更新现有示例
**文件**：`examples/*.心语`

#### 步骤5.3.3：添加示例测试
**文件**：`tests/test_examples.py`
```python
def test_all_examples():
    """测试所有示例代码能正常运行"""
    for example_file in Path("examples").glob("*.心语"):
        code = example_file.read_text(encoding='utf-8')
        # 编译并执行
        result = execute(code)
        assert result.success
```

**验证标准**：
- [ ] 所有示例风格统一
- [ ] 所有示例可运行
- [ ] 注释清晰完整

---

## 🎯 阶段六：代码质量提升（优先级：中）

### 任务6.1：完善代码注释

**实施步骤**：

#### 步骤6.1.1：为核心模块添加详细注释
**目标文件**：
- `src/parser/parser.py`
- `src/semantic/analyzer.py`
- `src/codegen/python_codegen.py`

#### 步骤6.1.2：添加docstring
**规范**：
```python
def parse_expression(self) -> ASTNode:
    """解析表达式
    
    使用元数驱动解析技术，根据动词的元数自动收集参数。
    
    算法：
    1. 解析第一个表达式
    2. 如果遇到动词，根据元数收集参数
    3. 递归解析参数表达式
    
    Returns:
        ASTNode: 表达式的AST节点
        
    Raises:
        ParseError: 解析错误时抛出
        
    Example:
        >>> parser.parse_expression("3 相加 5")
        BinaryOpNode(op='相加', left=3, right=5)
    """
```

**验证标准**：
- [ ] 所有公共方法有docstring
- [ ] 复杂逻辑有注释
- [ ] 注释准确有用

---

### 任务6.2：消除重复代码

**实施步骤**：

#### 步骤6.2.1：识别重复代码
```bash
# 使用工具检测重复代码
pip install pylint
pylint --disable=all --enable=duplicate-code src/
```

#### 步骤6.2.2：重构重复代码
**策略**：
- 提取公共函数
- 使用装饰器
- 创建工具类

**验证标准**：
- [ ] 无明显重复代码
- [ ] 代码复用率高
- [ ] 可维护性好

---

### 任务6.3：提高测试覆盖率

**实施步骤**：

#### 步骤6.3.1：分析当前覆盖率
```bash
pytest --cov=src --cov-report=html tests/
```

#### 步骤6.3.2：为未覆盖代码添加测试
**目标**：覆盖率从66%提升到80%+

#### 步骤6.3.3：添加边界条件测试
#### 步骤6.3.4：添加错误路径测试

**验证标准**：
- [ ] 覆盖率≥80%
- [ ] 关键路径100%覆盖
- [ ] 边界条件测试完整

---

## 📊 进度跟踪

### 阶段一：核心功能完善
- [ ] 任务1.1：修复语法解析器（0/5）
- [ ] 任务1.2：修复语义分析器（0/3）
- [ ] 任务1.3：修复集成测试（0/3）
- [ ] 任务1.4：修复宏展开（0/2）
- [ ] 任务1.5：修复其他问题（0/2）

### 阶段二：性能优化
- [ ] 任务2.1：建立性能测试框架（0/5）
- [ ] 任务2.2：优化编译流程（0/3）
- [ ] 任务2.3：建立性能基准（0/1）

### 阶段三：生态建设
- [ ] 任务3.1：完善包管理器（0/3）
- [ ] 任务3.2：开发标准库（0/3）
- [ ] 任务3.3：增强IDE支持（0/3）

### 阶段四：类型系统增强
- [ ] 任务4.1：完善类型推断（0/3）
- [ ] 任务4.2：添加类型注解支持（0/3）
- [ ] 任务4.3：增强编译时检查（0/3）

### 阶段五：文档完善
- [ ] 任务5.1：生成API参考文档（0/4）
- [ ] 任务5.2：编写系统教程（0/3）
- [ ] 任务5.3：规范化示例代码（0/3）

### 阶段六：代码质量提升
- [ ] 任务6.1：完善代码注释（0/2）
- [ ] 任务6.2：消除重复代码（0/2）
- [ ] 任务6.3：提高测试覆盖率（0/4）

---

## 🎯 验证清单

### 每个任务完成后验证
- [ ] 所有相关测试通过
- [ ] 无回归问题
- [ ] 代码风格符合规范
- [ ] 文档已更新
- [ ] 提交信息清晰

### 每个阶段完成后验证
- [ ] 所有任务完成
- [ ] 测试覆盖率达标
- [ ] 性能基准达标
- [ ] 文档完整
- [ ] 无已知bug

### 项目整体验证
- [ ] 所有测试通过（724个）
- [ ] 测试覆盖率≥80%
- [ ] 文档完整
- [ ] 示例可运行
- [ ] 性能达标

---

## 📝 执行原则

1. **严格按顺序执行**：不跳过任何步骤
2. **每步验证**：完成一步立即验证
3. **记录问题**：遇到问题记录到ISSUES.md
4. **及时提交**：完成一个任务提交一次
5. **保持质量**：不为了速度牺牲质量

---

## 🔄 更新记录

| 日期 | 阶段 | 任务 | 状态 | 备注 |
|------|------|------|------|------|
| 2026-06-04 | - | 创建改进计划 | ✅ 完成 | 初始版本 |
| 2026-06-04 | 1.1 | 修复字典字面量解析 | ✅ 完成 | 添加英文冒号支持，实现_parse_dict方法 |
| 2026-06-04 | 1.1 | 修复while循环解析 | ✅ 完成 | 添加"当"和"时"关键字支持 |
| 2026-06-04 | 1.1 | 修复for循环解析 | ✅ 完成 | 修正"遍历"关键字映射为FOR |
| 2026-06-04 | 1 | 核心功能修复进度 | 🔄 进行中 | 从25个失败减少到12个失败 |

---

**当前进度**：
- ✅ 字典字面量解析已修复
- ✅ while循环解析已修复
- ✅ for循环解析已修复
- 🔄 剩余12个失败测试待修复

**下一步行动**：继续修复剩余的12个失败测试
