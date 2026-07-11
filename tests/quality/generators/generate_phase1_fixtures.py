"""Write or byte-check all generated Phase 1 quality images."""

from __future__ import annotations

import argparse
import hashlib
import tempfile
from pathlib import Path

from .generate_bilingual_slide import generate_bilingual_slide
from .generate_calibration_table import generate_calibration_table
from .generate_formula_board import generate_formula_board
from .generate_projected_slide_derivative import (
    generate_projected_slide_derivative,
)


GENERATED_FILENAMES = (
    "bilingual_printed_slide.png",
    "bilingual_printed_slide_projected.jpg",
    "formula_board.png",
    "calibration_table.png",
)


def generate_phase1_fixtures(output_directory: Path) -> tuple[Path, ...]:
    """Generate the four repo-owned images into one explicit directory."""
    output_directory.mkdir(parents=True, exist_ok=True)
    clean_slide = generate_bilingual_slide(
        output_directory / GENERATED_FILENAMES[0]
    )
    projected = generate_projected_slide_derivative(
        clean_slide,
        output_directory / GENERATED_FILENAMES[1],
    )
    formula = generate_formula_board(output_directory / GENERATED_FILENAMES[2])
    table = generate_calibration_table(output_directory / GENERATED_FILENAMES[3])
    return clean_slide, projected, formula, table


def check_phase1_fixtures(committed_directory: Path) -> None:
    """Regenerate elsewhere and require byte-identical committed artifacts."""
    with tempfile.TemporaryDirectory(prefix="ocrllm-phase1-fixtures-") as temporary:
        generated = generate_phase1_fixtures(Path(temporary))
        for generated_path in generated:
            committed_path = committed_directory / generated_path.name
            if not committed_path.is_file():
                raise RuntimeError(f"missing committed fixture: {committed_path.name}")
            if _sha256(generated_path) != _sha256(committed_path):
                raise RuntimeError(f"fixture bytes drifted: {committed_path.name}")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _default_image_directory() -> Path:
    return Path(__file__).resolve().parents[2] / "fixtures" / "phase1" / "images"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument(
        "--output-directory",
        type=Path,
        default=_default_image_directory(),
    )
    arguments = parser.parse_args()
    if arguments.write:
        for path in generate_phase1_fixtures(arguments.output_directory):
            print(f"{path.name} {_sha256(path)}")
    else:
        check_phase1_fixtures(arguments.output_directory)
        print("Phase 1 generated fixtures are byte-identical.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
