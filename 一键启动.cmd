@echo off
chcp 65001 >nul
title 一键启动 - Private Blog

echo ============================================
echo   Private Blog 一键启动
echo ============================================
echo.

cd /d "%~dp0"

:: =========== 检查 Python ===========
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] 未找到 Python，请先安装 Python 3.9+
    pause
    exit /b 1
)

:: =========== 检查 Node.js ===========
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] 未找到 Node.js，请先安装 Node.js 18+
    pause
    exit /b 1
)

:: =========== 检查 .env 文件 ===========
if not exist "backend\.env" (
    echo [INFO] .env 文件不存在，正在从 .env.example 创建...
    copy "backend\.env.example" "backend\.env" >nul
    if %errorlevel% neq 0 (
        echo [ERROR] 无法创建 .env 文件，请手动复制 backend\.env.example 为 backend\.env
        pause
        exit /b 1
    )
    echo [INFO] .env 文件已创建，请根据需要修改 backend\.env 中的配置
)

:: =========== 检查/安装后端依赖 ===========
echo [INFO] 检查后端 Python 依赖...
cd /d "%~dp0backend"
python -c "import fastapi, uvicorn, PIL, pydantic_settings" >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] 后端依赖已就绪
) else (
    echo [INFO] 正在安装后端依赖，请稍候...
    python -m pip install -r requirements.txt -q 2>nul
    if %errorlevel% neq 0 (
        echo [WARN] 后端依赖安装失败，如果依赖已安装请忽略此警告
        echo [WARN] 如启动失败，请手动执行: cd backend ^&^& python -m pip install -r requirements.txt
    ) else (
        echo [INFO] 后端依赖安装完成
    )
)

:: =========== 检查/安装前端依赖 ===========
cd /d "%~dp0frontend"
if not exist "node_modules\" (
    echo [INFO] 正在安装前端依赖，请稍候...
    call npm install
    if %errorlevel% neq 0 (
        echo [WARN] 前端依赖安装失败，如果依赖已安装请忽略此警告
        echo [WARN] 如启动失败，请手动执行: cd frontend ^&^& npm install
    ) else (
        echo [INFO] 前端依赖安装完成
    )
) else (
    echo [INFO] 前端依赖已就绪
)

:: =========== 启动后端 ===========
cd /d "%~dp0backend"
echo [INFO] 正在启动后端服务 (端口 8000)...
start "Private Blog - Backend" cmd /k "cd /d %~dp0backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

:: =========== 等待后端启动 ===========
echo [INFO] 等待后端服务启动...
timeout /t 3 /nobreak >nul

:: =========== 启动前端 ===========
cd /d "%~dp0frontend"
echo [INFO] 正在启动前端服务 (端口 5173)...
start "Private Blog - Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

:: =========== 打开浏览器 ===========
echo [INFO] 等待前端服务就绪后打开浏览器...
timeout /t 5 /nobreak >nul
start http://localhost:5173

echo.
echo ============================================
echo   启动完成！
echo   后端: http://localhost:8000
echo   前端: http://localhost:5173
echo   API文档: http://localhost:8000/docs
echo ============================================
echo.
echo 按任意键关闭此窗口（这将同时关闭前后端服务）...

:: 等待用户按键后清理进程
pause >nul
taskkill /fi "WINDOWTITLE eq Private Blog - Backend*" /f >nul 2>&1
taskkill /fi "WINDOWTITLE eq Private Blog - Frontend*" /f >nul 2>&1
pause >nul