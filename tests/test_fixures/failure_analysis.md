# 失败测试根本原因分析报告

## 1. test_fibonacci (tests/test_integration.py::TestComplexPrograms)

**错误信息**: `assert '55' in '运行时错误: maximum recursion depth exceeded\n'`

**根本原因**:
- 斐波那契函数的递归实现导致递归深度超过Python默认限制
- 代码：`返回 斐波那契 n 相减 1 相加 斐波那契 n 相减 2`
- 问题：递归调用没有尾递归优化，且Python默认递归深度限制为1000

**修复策略**:
- 方案1：增加Python递归深度限制（临时方案）
- 方案2：修改测试用例，使用更小的输入值（如fib(5)）
- 方案3：实现尾递归优化或迭代版本（长期方案）

**推荐**: 方案2 - 修改测试用例使用fib(5)或fib(7)

---

## 2. test_builtin_function (tests/test_integration_enhanced.py::TestSemanticAnalyzerWithInference)

**错误信息**: `assert False`

**根本原因**: 需要查看测试代码进一步分析

**修复策略**: 待分析

---

## 3. test_full_pipeline (tests/test_integration_enhanced.py::TestIntegration)

**错误信息**: `assert False`

**根本原因**: 需要查看测试代码进一步分析

**修复策略**: 待分析

---

## 4. test_expand_ast_for_node_with_macro (tests/test_macro_expander_detailed.py::TestMacroExpanderDetailed)

**错误信息**: `assert isinstance(ForNode(...), list)` - 期望返回list，实际返回ForNode

**根本原因**:
- `_expand_for_loop`方法（第148-160行）调用`_expand_macro_call`
- `_expand_macro_call`返回`FunctionCallNode`（第159行创建的macro_call）
- 但测试期望返回展开后的语句列表

**代码位置**: `src/macro/macro_expander.py:148-160`

**问题代码**:
```python
def _expand_for_loop(self, node: ForNode) -> ASTNode:
    macro_call = FunctionCallNode(name="遍历", args=[...])
    return self._expand_macro_call(macro_call)  # 返回FunctionCallNode
```

**修复策略**:
- `_expand_for_loop`应该返回展开后的结果，而不是macro_call
- 需要确保`_expand_macro_call`正确展开并返回列表

**推荐修复**:
```python
def _expand_for_loop(self, node: ForNode) -> ASTNode:
    macro_call = FunctionCallNode(name="遍历", args=[...])
    expanded = self._expand_macro_call(macro_call)
    # 如果展开结果是列表，直接返回
    if isinstance(expanded, list):
        return expanded
    # 否则包装成列表
    return [expanded] if expanded else []
```

---

## 5. test_expand_for_loop_method (tests/test_macro_expander_detailed.py::TestMacroExpanderDetailed)

**错误信息**: `assert isinstance(FunctionCallNode(...), list)` - 期望返回list，实际返回FunctionCallNode

**根本原因**: 与问题4相同，`_expand_for_loop`返回类型错误

**修复策略**: 与问题4相同

---

## 6. test_execute_print (tests/test_secure_runtime.py::TestSecureRuntime)

**错误信息**: `assert False is True`

**根本原因**: 需要查看测试代码进一步分析

**修复策略**: 待分析

---

## 7. test_execute_with_math_module (tests/test_secure_runtime.py::TestSecureRuntime)

**错误信息**: `assert False is True`

**根本原因**: 需要查看测试代码进一步分析

**修复策略**: 待分析

---

## 8. test_execute_with_json_module (tests/test_secure_runtime.py::TestSecureRuntime)

**错误信息**: `assert False is True`

**根本原因**: 需要查看测试代码进一步分析

**修复策略**: 待分析

---

## 9. test_function_call (tests/test_semantic.py::TestSemanticAnalyzer)

**错误信息**: `False is not true`

**根本原因**: 需要查看测试代码进一步分析

**修复策略**: 待分析

---

## 修复优先级排序

### P0 - 高优先级（影响核心功能）

1. **问题4和5**: 宏展开返回类型错误 - 影响宏系统核心功能
2. **问题1**: 斐波那契递归深度问题 - 影响递归函数支持

### P1 - 中优先级（影响部分功能）

3. **问题6, 7, 8**: 安全运行时测试失败
4. **问题9**: 语义分析器测试失败

### P2 - 低优先级（需要进一步分析）

5. **问题2, 3**: 集成测试失败 - 需要查看具体代码

---

## 下一步行动

1. 立即修复问题4和5（宏展开返回类型）
2. 修复问题1（斐波那契测试用例）
3. 分析并修复问题6-9
4. 分析并修复问题2-3
