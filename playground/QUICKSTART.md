# 心语 Playground 快速启动指南

## ⚠️ 重要提示

**如果您使用虚拟环境（.venv），请先激活虚拟环境！**

检测到您的项目有虚拟环境，请按照以下步骤操作。

## 🚀 快速启动步骤

### 方法1：使用自动启动脚本（推荐）

**PowerShell用户**：
```powershell
cd playground
.\start_auto.ps1
```

**CMD用户**：
```cmd
cd playground
start_auto.bat
```

这些脚本会自动：
- 检测并激活虚拟环境
- 检查并安装依赖
- 启动服务器

### 方法2：手动激活虚拟环境

**步骤1：激活虚拟环境**

PowerShell：
```powershell
cd G:\dumategithub\chineseprogram
.\.venv\Scripts\Activate.ps1
```

CMD：
```cmd
cd G:\dumategithub\chineseprogram
.venv\Scripts\activate.bat
```

**步骤2：安装依赖**

```bash
pip install flask flask-cors
```

**步骤3：启动Playground**

```bash
cd playground
python server.py
```

### 第三步：访问Playground

打开浏览器，访问：

```
http://localhost:5000
```

### 第四步：开始使用

1. 在左侧编辑器中输入心语代码
2. 点击右上角的「运行代码」按钮（或按 Ctrl+Enter）
3. 在中间的输出面板查看结果
4. 点击右侧的示例代码快速学习

## 📝 示例代码

### Hello World

```yan
定义 问候 = "你好，心语！"。
打印 问候。
```

### 函数定义

```yan
定义 平方 = 函 x：
  返回 x 相乘 x。
。

打印 平方 5。
```

### 循环遍历

```yan
遍历 i 于 范围 1 6：
  打印 i。
。
```

## ⚠️ 常见问题

### 问题1：ModuleNotFoundError: No module named 'flask'

**解决方案**：
```bash
pip install flask flask-cors
```

或者：
```bash
pip install -r requirements.txt
```

### 问题2：ImportError: cannot import name 'PythonCodeGenerator'

**解决方案**：
这个问题已经修复，请确保使用最新版本的 `server.py`。

### 问题3：端口被占用

如果5000端口被占用，可以修改 `server.py` 最后一行：

```python
app.run(host='0.0.0.0', port=5001, debug=True)  # 改为5001或其他端口
```

### 问题4：浏览器无法访问

**解决方案**：
1. 确认服务器已启动（终端显示 "Running on http://0.0.0.0:5000"）
2. 检查防火墙设置
3. 尝试访问 http://127.0.0.1:5000

## 🎯 快捷键

- `Ctrl + Enter` - 运行代码
- `Esc` - 关闭语法文档

## 🎨 界面说明

```
┌─────────────────────────────────────────────────────────┐
│  心语 Playground                    [语法文档] [运行]   │
├──────────────────┬──────────────────┬──────────────────┤
│                  │                  │                  │
│    编辑器        │      输出        │    示例代码      │
│                  │                  │                  │
│  (输入代码)      │   (显示结果)     │  (点击加载)      │
│                  │                  │                  │
└──────────────────┴──────────────────┴──────────────────┘
```

## 📚 更多信息

- [完整文档](README.md)
- [心语语言规范](../docs/LANGUAGE_SPEC_V3.md)
- [为什么选择心语](../docs/WHY_XINYU.md)

---

**祝你使用愉快！** 🎉
