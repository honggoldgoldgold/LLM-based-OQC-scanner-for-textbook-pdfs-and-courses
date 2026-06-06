#!/bin/bash
# OCRLLM 启动脚本 (Linux / Ubuntu)
# 使用方法: 双击桌面快捷方式，或直接运行 bash start_ocrllm.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"

# ── 加载 .env 文件（可选）────────────────────────────────────────────────────
# 在 OCRLLM/ 目录下创建 .env 并写入 DASHSCOPE_API_KEY=sk-xxx 即可自动生效
ENV_FILE="$SCRIPT_DIR/.env"
if [ -f "$ENV_FILE" ]; then
    set -o allexport
    # shellcheck disable=SC1090
    source "$ENV_FILE"
    set +o allexport
fi

# ── 检查虚拟环境 ────────────────────────────────────────────────────────────
if [ ! -f "$VENV_PYTHON" ]; then
    zenity --error --text="未找到虚拟环境。\n请先运行:\n  uv venv .venv && uv pip install -r requirements.txt" 2>/dev/null \
        || xmessage -center "未找到虚拟环境。请先运行:\n  uv venv .venv && uv pip install -r requirements.txt" 2>/dev/null \
        || echo "错误: .venv 不存在，请先安装依赖" >&2
    exit 1
fi

# ── 确保 ~/.local/bin (ffmpeg 符号链接) 在 PATH 中 ────────────────────────────
export PATH="$HOME/.local/bin:$PATH"

# ── 切换到工作目录 ───────────────────────────────────────────────────────────
cd "$WORKSPACE_ROOT"

# ── 启动 GUI ─────────────────────────────────────────────────────────────────
exec "$VENV_PYTHON" -m OCRLLM.main "$@"
