@echo off
chcp 65001 >nul 2>&1
setlocal

set "ENV_NAME=OCRLLM"
set "SCRIPT_DIR=%~dp0"
set "PACKAGE_DIR=%SCRIPT_DIR%OCRLLM"
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"

echo.
echo ============================================================
echo   OCRLLM 启动
echo ============================================================
echo.

set "CONDA_BAT="
for /f "delims=" %%I in ('where conda.bat 2^>nul') do (
    if not defined CONDA_BAT set "CONDA_BAT=%%I"
)

if not defined CONDA_BAT (
    where conda >nul 2>&1
    if errorlevel 1 (
        echo [错误] 未找到 conda，请先安装 Anaconda 或 Miniconda。
        pause
        exit /b 1
    )
)

if defined CONDA_BAT (
    call "%CONDA_BAT%" activate %ENV_NAME%
) else (
    call conda activate %ENV_NAME%
)
if errorlevel 1 (
    echo [错误] 无法激活环境 %ENV_NAME%。
    echo        请先运行 setup_env.bat，或执行 conda init cmd.exe。
    pause
    exit /b 1
)

cd /d "%SCRIPT_DIR%"
if not exist "%PACKAGE_DIR%\main.py" (
    echo [错误] 未找到旧应用入口:
    echo        %PACKAGE_DIR%\main.py
    echo.
    echo 当前仓库结构应为:
    echo        legacy_app\OCRLLM\main.py
    pause
    exit /b 1
)

python -m OCRLLM.main %*
if errorlevel 1 (
    echo.
    echo [错误] OCRLLM 启动失败。
    pause
    exit /b 1
)

endlocal
