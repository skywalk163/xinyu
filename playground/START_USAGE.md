# Playground 启动脚本使用说明

**文件**：`playground/start.py`
**功能**：支持自定义端口配置

---

## 🚀 基本用法

### 默认端口（5000）

```bash
python start.py
```

访问：http://localhost:5000

### 自定义端口

**方法1：位置参数**
```bash
python start.py 8080
```

**方法2：命名参数**
```bash
python start.py --port 8080
```

**方法3：短参数**
```bash
python start.py -p 8080
```

访问：http://localhost:8080

---

## 📝 完整参数说明

### 位置参数

```
port_positional    端口号（可选）
```

### 命名参数

```
-p PORT, --port PORT     端口号（默认：5000）
--host HOST              主机地址（默认：0.0.0.0）
--no-debug               禁用调试模式
-h, --help               显示帮助信息
```

---

## 💡 使用示例

### 示例1：使用默认配置

```bash
python start.py
```

输出：
```
============================================================
心语 Playground - 中文编程语言在线体验
============================================================

访问地址: http://localhost:5000

功能:
  ✅ 在线编写和执行心语代码
  ✅ 查看语法文档
  ✅ 加载示例代码
  ✅ 实时输出结果

快捷键:
  Ctrl+Enter - 运行代码
  Esc - 关闭文档

按 Ctrl+C 停止服务器
============================================================
```

### 示例2：使用端口8080

```bash
python start.py 8080
```

或

```bash
python start.py --port 8080
```

访问：http://localhost:8080

### 示例3：指定主机和端口

```bash
python start.py --host 127.0.0.1 --port 3000
```

访问：http://127.0.0.1:3000

### 示例4：生产模式（禁用调试）

```bash
python start.py --port 8000 --no-debug
```

---

## 🎯 常见场景

### 场景1：端口被占用

如果5000端口被占用，可以使用其他端口：

```bash
python start.py 8080
```

### 场景2：本地开发

只允许本地访问：

```bash
python start.py --host 127.0.0.1 --port 5000
```

### 场景3：局域网访问

允许局域网内其他设备访问：

```bash
python start.py --host 0.0.0.0 --port 5000
```

其他设备可以通过你的IP地址访问：
```
http://你的IP:5000
```

### 场景4：生产部署

禁用调试模式：

```bash
python start.py --port 80 --no-debug
```

---

## 🔧 参数优先级

当同时使用位置参数和命名参数时，**位置参数优先级更高**：

```bash
python start.py 8080 --port 3000
```

实际使用端口：**8080**（位置参数优先）

---

## 📊 端口选择建议

### 开发环境

- **5000** - 默认端口，适合开发
- **3000** - 常用的前端开发端口
- **8080** - 常用的后端开发端口

### 生产环境

- **80** - HTTP默认端口
- **443** - HTTPS默认端口（需要SSL证书）
- **8000** - 常用的生产端口

### 避免使用的端口

- **22** - SSH
- **80** - HTTP（需要root权限）
- **443** - HTTPS（需要root权限）
- **3306** - MySQL
- **5432** - PostgreSQL
- **6379** - Redis
- **27017** - MongoDB

---

## 🐛 故障排除

### 问题1：端口被占用

**错误信息**：
```
OSError: [Errno 98] Address already in use
```

**解决方案**：
1. 使用其他端口：`python start.py 8080`
2. 或找到并关闭占用端口的进程

### 问题2：权限不足

**错误信息**：
```
PermissionError: [Errno 13] Permission denied
```

**解决方案**：
1. 使用大于1024的端口（不需要root权限）
2. 或使用sudo（Linux/Mac）：`sudo python start.py 80`

### 问题3：防火墙阻止

**症状**：局域网内其他设备无法访问

**解决方案**：
1. 检查防火墙设置
2. 允许对应端口的入站连接
3. Windows：控制面板 → 防火墙 → 高级设置
4. Linux：`sudo ufw allow 5000`

---

## 📝 配置文件方式（可选）

如果不想每次都输入参数，可以创建配置文件：

### 创建 `playground_config.py`

```python
# Playground 配置
PORT = 8080
HOST = '0.0.0.0'
DEBUG = True
```

### 修改 `start.py`

在文件开头添加：

```python
try:
    from playground_config import PORT, HOST, DEBUG
    default_port = PORT
    default_host = HOST
    default_debug = DEBUG
except ImportError:
    default_port = 5000
    default_host = '0.0.0.0'
    default_debug = True
```

---

## 🎉 总结

### 新增功能

- ✅ 支持自定义端口
- ✅ 支持自定义主机地址
- ✅ 支持禁用调试模式
- ✅ 灵活的参数配置方式

### 使用方式

```bash
# 最简单
python start.py

# 自定义端口
python start.py 8080

# 完整配置
python start.py --host 127.0.0.1 --port 3000 --no-debug

# 查看帮助
python start.py --help
```

**现在可以根据需要灵活配置Playground了！** 🎯
