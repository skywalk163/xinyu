# 心语 Playground 启动脚本 (PowerShell)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "心语 Playground 启动器" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否在虚拟环境中
if ($env:VIRTUAL_ENV) {
    Write-Host "[信息] 检测到虚拟环境: $env:VIRTUAL_ENV" -ForegroundColor Green
} else {
    Write-Host "[信息] 使用全局Python环境" -ForegroundColor Yellow
}

# 检查Flask是否安装
Write-Host "正在检查依赖..." -ForegroundColor Cyan
try {
    python -c "import flask" 2>$null
    Write-Host "[成功] Flask已安装" -ForegroundColor Green
} catch {
    Write-Host "[警告] Flask未安装，正在安装依赖..." -ForegroundColor Yellow
    pip install flask flask-cors
    Write-Host ""
}

# 启动服务器
Write-Host "启动Playground服务器..." -ForegroundColor Cyan
Write-Host ""
Write-Host "访问地址: " -NoNewline
Write-Host "http://localhost:5000" -ForegroundColor Green
Write-Host "按 " -NoNewline
Write-Host "Ctrl+C" -ForegroundColor Yellow -NoNewline
Write-Host " 停止服务器"
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# 运行服务器
python server.py
