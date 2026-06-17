# Playground 示例加载问题排查

**问题描述**：点击示例代码后，编辑器显示"0 字符"，示例没有加载到编辑器中。

---

## 🔍 问题排查

### 1. 检查文件配置

已验证：
- ✅ examples对象定义正确（包含13个示例）
- ✅ loadExample函数定义正确
- ✅ onclick绑定正确（13个按钮都绑定了）

### 2. 可能的原因

1. **浏览器缓存**：浏览器缓存了旧版本的HTML文件
2. **JavaScript错误**：可能有其他JavaScript代码阻止了执行
3. **文件编码**：文件编码问题导致JavaScript无法正确解析

---

## ✅ 解决方案

### 方案1：清除浏览器缓存（推荐）

1. **Chrome/Edge**：
   - 按 `Ctrl + Shift + Delete`
   - 选择"缓存的图片和文件"
   - 点击"清除数据"
   - 刷新页面（`F5`）

2. **Firefox**：
   - 按 `Ctrl + Shift + Delete`
   - 选择"缓存"
   - 点击"立即清除"
   - 刷新页面

3. **强制刷新**：
   - 按 `Ctrl + F5`（强制刷新，忽略缓存）
   - 或 `Ctrl + Shift + R`

### 方案2：使用测试页面验证

访问测试页面验证功能是否正常：

```
http://localhost:5000/test_load.html
```

如果测试页面正常工作，说明是主页面的问题。

### 方案3：检查浏览器控制台

1. 打开浏览器开发者工具（`F12`）
2. 切换到"Console"标签
3. 点击示例按钮
4. 查看是否有错误信息

**预期输出**：
```
Loading example: hello
Examples object: {hello: "...", variables: "...", ...}
Example content: # 你好，世界...
Editor value set, length: 50
```

**如果有错误**：
- 红色错误信息表示JavaScript执行失败
- 根据错误信息修复问题

### 方案4：检查网络请求

1. 打开开发者工具（`F12`）
2. 切换到"Network"标签
3. 刷新页面
4. 检查`index.html`是否正确加载（状态码200）

---

## 🧪 测试步骤

### 步骤1：启动服务器

```powershell
cd playground
python server.py
```

### 步骤2：访问测试页面

```
http://localhost:5000/test_load.html
```

点击按钮，查看：
- 编辑器是否显示代码
- 字符数是否正确
- 调试信息是否正常

### 步骤3：访问主页面

```
http://localhost:5000
```

强制刷新（`Ctrl + F5`），然后：
1. 打开开发者工具（`F12`）
2. 切换到Console标签
3. 点击任意示例按钮
4. 查看控制台输出

---

## 📝 调试信息

### 正常情况下的控制台输出

```javascript
Loading example: hello
Examples object: {hello: "# 你好，世界...", variables: "# 变量定义示例...", ...}
Example content: # 你好，世界
定义 问候 = "你好，心语！"。
打印 问候。

定义 名字 = "世界"。
打印 "你好，" 名字。
Editor value set, length: 67
```

### 异常情况

**情况1：examples对象未定义**
```
Uncaught ReferenceError: examples is not defined
```
**原因**：JavaScript文件加载失败或语法错误
**解决**：检查HTML文件是否完整

**情况2：示例未找到**
```
Example not found: hello
```
**原因**：examples对象中没有该示例
**解决**：检查examples对象定义

**情况3：编辑器未找到**
```
Uncaught TypeError: Cannot set property 'value' of null
```
**原因**：editor元素未找到
**解决**：检查HTML结构

---

## 🔧 已添加的调试功能

在`index.html`中已添加调试代码：

```javascript
function loadExample(name) {
    console.log('Loading example:', name);
    console.log('Examples object:', examples);
    console.log('Example content:', examples[name]);

    if (!examples[name]) {
        console.error('Example not found:', name);
        output.innerHTML = '<div class="output-error">❌ 示例未找到: ' + name + '</div>';
        return;
    }

    editor.value = examples[name];
    charCount.textContent = `${editor.value.length} 字符`;
    output.innerHTML = '<div class="output-info">▶ 已加载示例，点击「运行代码」执行</div>';

    console.log('Editor value set, length:', editor.value.length);
}
```

---

## 🎯 快速解决方案

### 最可能的原因：浏览器缓存

**解决步骤**：

1. 停止服务器（`Ctrl + C`）
2. 清除浏览器缓存（`Ctrl + Shift + Delete`）
3. 重启服务器
4. 强制刷新页面（`Ctrl + F5`）
5. 点击示例按钮测试

### 验证是否解决

点击示例按钮后：
- ✅ 编辑器显示代码
- ✅ 字符数显示正确（不是0）
- ✅ 输出面板显示"已加载示例"

---

## 📞 如果问题仍然存在

请提供以下信息：

1. **浏览器类型和版本**
   - 例如：Chrome 120.0.6099.109

2. **控制台错误信息**
   - 打开F12，复制Console中的错误

3. **测试页面结果**
   - 访问`/test_load.html`的结果

4. **网络请求状态**
   - F12 → Network → index.html的状态码

---

## ✅ 预期结果

正常情况下：

1. 点击示例按钮
2. 编辑器显示对应代码
3. 字符数显示正确
4. 输出面板显示"已加载示例"
5. 点击"运行代码"可以执行

**如果按照上述步骤操作后问题解决，就可以正常使用Playground了！** 🎉
