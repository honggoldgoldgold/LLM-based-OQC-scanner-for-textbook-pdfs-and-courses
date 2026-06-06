@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

REM ============================================================
REM OCRLLM One-Click Environment Setup
REM Auto-detect network and switch pip source
REM ============================================================

set "ENV_NAME=OCRLLM"
set "PYTHON_VER=3.10"
set "SCRIPT_DIR=%~dp0"

:: pip 源列表
set "SRC_OFFICIAL=https://pypi.org/simple"
set "SRC_TSINGHUA=https://pypi.tuna.tsinghua.edu.cn/simple"
set "SRC_ALIYUN=https://mirrors.aliyun.com/pypi/simple/"

echo.
echo ============================================================
echo   OCRLLM 一键环境配置
echo ============================================================
echo.

:: ------ 第 1 步: 检测 conda ------
echo [1/5] 检测 conda ...
where conda >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 conda，请先安装 Anaconda 或 Miniconda。
    echo        下载地址: https://docs.conda.io/en/latest/miniconda.html
    goto :fail
)
for /f "tokens=*" %%i in ('conda --version 2^>nul') do echo        %%i
echo        [OK]
echo.

:: ------ 第 2 步: 创建或更新 conda 环境 ------
echo [2/5] 配置 conda 环境 "%ENV_NAME%" (Python %PYTHON_VER%) ...
conda info --envs 2>nul | findstr /C:"%ENV_NAME%" >nul 2>&1
if %errorlevel% equ 0 (
    echo        环境已存在，跳过创建。
) else (
    echo        创建新环境 ...
    conda create -n %ENV_NAME% python=%PYTHON_VER% pip -y -q
    if !errorlevel! neq 0 (
        echo [错误] conda 环境创建失败。
        goto :fail
    )
)
echo        [OK]
echo.

:: ------ 第 3 步: 激活环境 ------
echo [3/5] 激活环境 ...
call conda activate %ENV_NAME%
if %errorlevel% neq 0 (
    echo [错误] 无法激活环境，请尝试以管理员权限运行，或执行 conda init cmd.exe。
    goto :fail
)
echo        Python: 
python --version
echo        [OK]
echo.

:: ------ 第 4 步: 选择最快的 pip 源 ------
echo [4/5] Detecting best pip source ...
set "BEST_SOURCE="
set "SRC_FLAG=none"

:: 优先测试清华源
echo        Testing Tsinghua mirror ...
pip install --dry-run --index-url %SRC_TSINGHUA% --trusted-host pypi.tuna.tsinghua.edu.cn pip >nul 2>&1
if !errorlevel! equ 0 (
    set "BEST_SOURCE=%SRC_TSINGHUA%"
    set "SRC_FLAG=tsinghua"
    echo        Tsinghua mirror OK.
)

:: 清华不可用则测试阿里云源
if "!SRC_FLAG!"=="none" (
    echo        Testing Aliyun mirror ...
    pip install --dry-run --index-url %SRC_ALIYUN% --trusted-host mirrors.aliyun.com pip >nul 2>&1
    if !errorlevel! equ 0 (
        set "BEST_SOURCE=%SRC_ALIYUN%"
        set "SRC_FLAG=aliyun"
        echo        Aliyun mirror OK.
    )
)

:: 最后测试官方源
if "!SRC_FLAG!"=="none" (
    echo        Testing official PyPI ...
    pip install --dry-run --index-url %SRC_OFFICIAL% pip >nul 2>&1
    if !errorlevel! equ 0 (
        set "BEST_SOURCE=%SRC_OFFICIAL%"
        set "SRC_FLAG=official"
        echo        Official PyPI OK.
    )
)

if "!SRC_FLAG!"=="none" (
    echo [ERROR] No pip source available. Check network.
    goto :fail
)

echo        Using: !BEST_SOURCE!
echo.

:: ------ 第 5 步: 安装依赖 ------
echo [5/5] 安装 Python 依赖 ...
set "REQ_FILE=%SCRIPT_DIR%requirements.txt"

if not exist "!REQ_FILE!" (
    echo [错误] 未找到 requirements.txt: !REQ_FILE!
    goto :fail
)

pip install -r "!REQ_FILE!" --index-url "!BEST_SOURCE!" -q
if !errorlevel! neq 0 (
    echo.
    echo        首选源安装失败，尝试回退到官方源 ...
    pip install -r "!REQ_FILE!" --index-url %SRC_OFFICIAL% -q
    if !errorlevel! neq 0 (
        echo [错误] 依赖安装失败。请检查网络或手动安装。
        goto :fail
    )
)
echo        [OK]
echo.

:: ------ 验证 ------
echo ============================================================
echo   验证安装 ...
echo ============================================================
echo.

python -c "import openai; print(f'  openai        {openai.__version__}')"
python -c "import fitz; print(f'  PyMuPDF       {fitz.__version__}')"
python -c "import rapidocr_onnxruntime; print(f'  RapidOCR      OK')"
python -c "import cv2; print(f'  OpenCV        {cv2.__version__}')"
python -c "import numpy; print(f'  NumPy         {numpy.__version__}')"
python -c "import PyQt5; print(f'  PyQt5         OK')"
python -c "import dashscope; v=getattr(dashscope,'__version__','?'); print(f'  DashScope     {v}')"
python -c "import imageio_ffmpeg; print(f'  ffmpeg        OK')"

echo.
echo ============================================================
echo   环境配置完成!
echo.
echo   使用方式:
echo     conda activate %ENV_NAME%
echo     python -m OCRLLM.main          (命令行)
echo     python -m OCRLLM.main --gui    (图形界面)
echo ============================================================
goto :end

:fail
echo.
echo ============================================================
echo   [失败] 环境配置未完成，请查看上方错误信息。
echo ============================================================

:end
echo.
pause
