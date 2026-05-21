@echo off
chcp 65001 >nul 2>&1
setlocal

set "ENV_NAME=OCRLLM"
set "SCRIPT_DIR=%~dp0"

echo.
echo ============================================================
echo   OCRLLM 启动
echo ============================================================
echo.

where conda >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 conda，请先安装 Anaconda 或 Miniconda。
    pause
    exit /b 1
)

call conda activate %ENV_NAME%
if errorlevel 1 (
    echo [错误] 无法激活环境 %ENV_NAME%。
    echo        请先运行 setup_env.bat，或执行 conda init cmd.exe。
    pause
    exit /b 1
)

cd /d "%SCRIPT_DIR%"
python main.py
if errorlevel 1 (
    echo.
    echo [错误] OCRLLM 启动失败。
    pause
    exit /b 1
)

endlocal