"""Combine OCRLLM social-long per-video markdowns into study pieces."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


BOARD_SUFFIX = "_\u677f\u4e66\u8bc6\u522b.md"
AUDIO_SUFFIX = "_\u5f55\u97f3\u8bc6\u522b.md"
PART_DIR_RE = re.compile(r"^P(?P<index>\d+)_(?P<title>.*)$")


@dataclass(frozen=True)
class PartMarkdown:
    index: int
    title: str
    directory: Path
    board_path: Path
    audio_path: Path


def part_sort_key(path: Path) -> int:
    match = PART_DIR_RE.match(path.name)
    if not match:
        raise ValueError(f"not a social-long part directory: {path}")
    return int(match.group("index"))


def part_title(path: Path) -> str:
    match = PART_DIR_RE.match(path.name)
    if not match:
        raise ValueError(f"not a social-long part directory: {path}")
    return match.group("title").replace("_", " ").strip() or path.name


def find_single(path: Path, suffix: str) -> Path:
    matches = sorted(candidate for candidate in path.glob(f"*{suffix}") if candidate.is_file())
    if len(matches) != 1:
        raise RuntimeError(f"{path} expected exactly one *{suffix}, found {len(matches)}")
    return matches[0]


def load_parts(root: Path) -> list[PartMarkdown]:
    part_dirs = sorted(
        [path for path in root.iterdir() if path.is_dir() and PART_DIR_RE.match(path.name)],
        key=part_sort_key,
    )
    if not part_dirs:
        raise RuntimeError(f"no P*_ part directories found under {root}")
    return [
        PartMarkdown(
            index=part_sort_key(path),
            title=part_title(path),
            directory=path,
            board_path=find_single(path, BOARD_SUFFIX),
            audio_path=find_single(path, AUDIO_SUFFIX),
        )
        for path in part_dirs
    ]


def chunks(items: list[PartMarkdown], size: int) -> list[list[PartMarkdown]]:
    if size < 1:
        raise ValueError("videos per piece must be at least 1")
    return [items[index:index + size] for index in range(0, len(items), size)]


def read_markdown(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace").strip()


def piece_name(parts: list[PartMarkdown], suffix: str) -> str:
    return f"P{parts[0].index:03d}-P{parts[-1].index:03d}_{suffix}.md"


def write_paired_piece(parts: list[PartMarkdown], output_dir: Path, course_title: str) -> Path:
    output_path = output_dir / piece_name(parts, "study")
    lines = [
        f"# {course_title} P{parts[0].index:03d}-P{parts[-1].index:03d}",
        "",
    ]
    for part in parts:
        lines.extend([
            f"## P{part.index:03d} {part.title}",
            "",
            f"Source directory: `{part.directory.as_posix()}`",
            "",
            "### Board Recognition",
            "",
            read_markdown(part.board_path),
            "",
            "### Audio Recognition",
            "",
            read_markdown(part.audio_path),
            "",
        ])
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return output_path


def write_separate_piece(parts: list[PartMarkdown], output_dir: Path, course_title: str, kind: str) -> Path:
    source_attr = "board_path" if kind == "board" else "audio_path"
    output_path = output_dir / piece_name(parts, kind)
    lines = [
        f"# {course_title} P{parts[0].index:03d}-P{parts[-1].index:03d} {kind.title()}",
        "",
    ]
    for part in parts:
        source_path = getattr(part, source_attr)
        lines.extend([
            f"## P{part.index:03d} {part.title}",
            "",
            f"Source file: `{source_path.as_posix()}`",
            "",
            read_markdown(source_path),
            "",
        ])
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return output_path


def combine_course_markdowns(
    root: Path,
    *,
    output_dir: Path | None = None,
    videos_per_piece: int = 10,
    course_title: str | None = None,
    mode: str = "paired",
) -> list[Path]:
    root = root.resolve()
    output_dir = (output_dir or (root / "combined_markdown")).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    title = course_title or root.name
    written: list[Path] = []
    for piece_parts in chunks(load_parts(root), videos_per_piece):
        if mode == "paired":
            written.append(write_paired_piece(piece_parts, output_dir, title))
        elif mode == "separate":
            written.append(write_separate_piece(piece_parts, output_dir, title, "board"))
            written.append(write_separate_piece(piece_parts, output_dir, title, "audio"))
        else:
            raise ValueError(f"unknown mode: {mode}")
    return written


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="social_long output root")
    parser.add_argument("--output-dir", type=Path, help="combined markdown output directory")
    parser.add_argument("--videos-per-piece", type=int, default=10)
    parser.add_argument("--course-title", default="")
    parser.add_argument("--mode", choices=("paired", "separate"), default="paired")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    written = combine_course_markdowns(
        args.root,
        output_dir=args.output_dir,
        videos_per_piece=args.videos_per_piece,
        course_title=args.course_title or None,
        mode=args.mode,
    )
    for path in written:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
