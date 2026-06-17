# 虚拟环境启动指南

## ⚠️ 重要提示

检测到您正在使用虚拟环境（.venv），需要先激活虚拟环境再安装依赖！

## 🚀 正确的启动步骤

### 步骤1：激活虚拟环境

**PowerShell**：
```powershell
cd G:\dumategithub\chineseprogram
.\.venv\Scripts\Activate.ps1
```

**CMD**：
```cmd
cd G:\dumategithub\chineseprogram
.venv\Scripts\activate.bat
```

### 步骤2：安装依赖

激活虚拟环境后，安装Flask：

```bash
pip install flask flask-cors
```

### 步骤3：启动Playground

```bash
cd playground
python server.py
```

## 🎯 一键启动（推荐）

### PowerShell用户

在项目根目录运行：

```powershell
.\.venv\Scripts\Activate.ps1
cd playground
python server.py
```

或者使用我们提供的PowerShell脚本：

```powershell
.\.venv\Scripts\Activate.ps1
cd playground
.\start.ps1
```

### CMD用户

在项目根目录运行：

```cmd
.venv\Scripts\activate.bat
cd playground
python server.py
```

## 📝 完整示例

```powershell
# 1. 进入项目目录
cd G:\dumategithub\chineseprogram

# 2. 激活虚拟环境
.\.venv\Scripts\Activate.ps1

# 3. 安装依赖（首次运行）
pip install flask flask-cors

# 4. 进入playground目录
cd playground

# 5. 启动服务器
python server.py

# 6. 访问 http://localhost:5000
```

## 🔧 常见问题

### 问题1：权限错误

如果PowerShell提示权限错误，运行：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 问题2：虚拟环境未激活

确保命令行前面有 `(.venv)` 标识：

```
(.venv) PS G:\dumategithub\chineseprogram\playground>
```

### 问题3：依赖安装到全局环境

**错误做法**：
```bash
# 未激活虚拟环境
pip install flask  # 这会安装到全局环境
```

**正确做法**：
```bash
# 先激活虚拟环境
.\.venv\Scripts\Activate.ps1
pip install flask  # 这会安装到虚拟环境
```

## 🎉 快速启动命令

复制以下命令直接运行：

```powershell
cd G:\dumategithub\chineseprogram; .\.venv\Scripts\Activate.ps1; pip install flask flask-cors; cd playground; python server.py
```

---

**记住：先激活虚拟环境，再安装依赖！** 🎯
