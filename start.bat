@echo off
chcp 65001 >nul 2>&1
setlocal

set "ROOT_DIR=%~dp0"
set "LEGACY_START=%ROOT_DIR%legacy_app\start.bat"

if not exist "%LEGACY_START%" (
    echo [错误] 未找到 legacy app 启动脚本:
    echo        %LEGACY_START%
    echo.
    echo 当前仓库已迁移为 library-first 结构；旧 GUI/CLI 应用应位于 legacy_app\。
    pause
    exit /b 1
)

call "%LEGACY_START%" %*
exit /b %ERRORLEVEL%
