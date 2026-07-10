"""Fresh-process guard for the dependency-free public import."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_plain_import_does_not_load_optional_image_or_provider_packages():
    source_root = Path(__file__).resolve().parents[1] / "src"
    probe = (
        "import sys; "
        "sys.path.insert(0, sys.argv[1]); "
        "import ocrllm; "
        "loaded={name.split('.')[0] for name in sys.modules}; "
        "forbidden={'PIL','pypdfium2','openai'}; "
        "assert not loaded & forbidden, loaded & forbidden"
    )

    completed = subprocess.run(
        [sys.executable, "-I", "-c", probe, str(source_root)],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert completed.returncode == 0, completed.stderr
