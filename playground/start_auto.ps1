# 心语 Playground 自动启动脚本 (PowerShell)
# 自动检测并激活虚拟环境

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "心语 Playground 自动启动器" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# 检查并激活虚拟环境
$venvPath = Join-Path $PSScriptRoot "..\.venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    Write-Host "[信息] 检测到虚拟环境，正在激活..." -ForegroundColor Green
    & $venvPath
    Write-Host "[成功] 虚拟环境已激活" -ForegroundColor Green
} else {
    Write-Host "[信息] 未检测到虚拟环境，使用全局Python" -ForegroundColor Yellow
}

# 检查Flask
Write-Host ""
Write-Host "正在检查Flask..." -ForegroundColor Cyan
try {
    & python -c "import flask" 2>$null
    Write-Host "[成功] Flask已安装" -ForegroundColor Green
} catch {
    Write-Host "[警告] Flask未安装，正在安装..." -ForegroundColor Yellow
    & pip install flask flask-cors
    Write-Host "[成功] 依赖安装完成" -ForegroundColor Green
}

# 启动服务器
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "启动Playground服务器..." -ForegroundColor Yellow
Write-Host ""
Write-Host "访问地址: " -NoNewline
Write-Host "http://localhost:5000" -ForegroundColor Green
Write-Host "按 " -NoNewline
Write-Host "Ctrl+C" -ForegroundColor Yellow -NoNewline
Write-Host " 停止服务器"
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# 运行服务器
& python server.py
