"""Audit OCRLLM social-long course output directories."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path


BOARD_SUFFIX = "_\u677f\u4e66\u8bc6\u522b.md"
AUDIO_SUFFIX = "_\u5f55\u97f3\u8bc6\u522b.md"
PART_DIR_RE = re.compile(r"^P(?P<index>\d+)_")
DIRTY_MARKERS = (
    "Reading additional input from stdin",
    "[WinError 10061]",
    "<!-- \u6279\u6b21",
    "Codex \u8bc6\u56fe\u5931\u8d25",
)


@dataclass
class PartAudit:
    index: int
    directory: str
    board_files: list[str] = field(default_factory=list)
    audio_files: list[str] = field(default_factory=list)
    dirty_files: list[str] = field(default_factory=list)

    @property
    def is_complete(self) -> bool:
        return len(self.board_files) == 1 and len(self.audio_files) == 1 and not self.dirty_files


@dataclass
class CourseAudit:
    root: str
    expected_parts: int | None
    part_dirs: int
    board_markdown: int
    audio_markdown: int
    downloaded_mp4: int
    filetrans_sidecars: int
    incomplete_parts: list[PartAudit]
    dirty_markdown: list[str]

    @property
    def ok(self) -> bool:
        if self.expected_parts is not None and self.part_dirs != self.expected_parts:
            return False
        if self.expected_parts is not None and self.board_markdown != self.expected_parts:
            return False
        if self.expected_parts is not None and self.audio_markdown != self.expected_parts:
            return False
        return not self.incomplete_parts and not self.dirty_markdown and self.filetrans_sidecars == 0


def iter_part_dirs(root: Path) -> list[Path]:
    dirs = [path for path in root.iterdir() if path.is_dir() and PART_DIR_RE.match(path.name)]
    return sorted(dirs, key=lambda path: int(PART_DIR_RE.match(path.name).group("index")))


def part_index(path: Path) -> int:
    match = PART_DIR_RE.match(path.name)
    if not match:
        raise ValueError(f"not a part directory: {path}")
    return int(match.group("index"))


def files_with_suffix(path: Path, suffix: str) -> list[Path]:
    return sorted(candidate for candidate in path.glob(f"*{suffix}") if candidate.is_file())


def contains_dirty_marker(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return True
    return any(marker in text for marker in DIRTY_MARKERS)


def audit_part(path: Path) -> PartAudit:
    board_files = files_with_suffix(path, BOARD_SUFFIX)
    audio_files = files_with_suffix(path, AUDIO_SUFFIX)
    dirty_files = [
        markdown
        for markdown in board_files + audio_files
        if markdown.stat().st_size <= 0 or contains_dirty_marker(markdown)
    ]
    return PartAudit(
        index=part_index(path),
        directory=str(path),
        board_files=[str(file_path) for file_path in board_files],
        audio_files=[str(file_path) for file_path in audio_files],
        dirty_files=[str(file_path) for file_path in dirty_files],
    )


def audit_course_output(root: Path, expected_parts: int | None = None) -> CourseAudit:
    root = root.resolve()
    parts = [audit_part(path) for path in iter_part_dirs(root)]
    all_markdown = list(root.rglob("*.md"))
    dirty_markdown = [str(path) for path in all_markdown if contains_dirty_marker(path)]
    downloads_dir = root / "_downloads"
    downloaded_mp4 = len(list(downloads_dir.glob("*.mp4"))) if downloads_dir.is_dir() else 0
    return CourseAudit(
        root=str(root),
        expected_parts=expected_parts,
        part_dirs=len(parts),
        board_markdown=sum(len(part.board_files) for part in parts),
        audio_markdown=sum(len(part.audio_files) for part in parts),
        downloaded_mp4=downloaded_mp4,
        filetrans_sidecars=len(list(root.rglob("*.filetrans_task.json"))),
        incomplete_parts=[part for part in parts if not part.is_complete],
        dirty_markdown=dirty_markdown,
    )


def format_text_report(audit: CourseAudit) -> str:
    lines = [
        f"Root: {audit.root}",
        f"ExpectedParts: {audit.expected_parts if audit.expected_parts is not None else 'unspecified'}",
        f"PartDirs: {audit.part_dirs}",
        f"BoardMarkdown: {audit.board_markdown}",
        f"AudioMarkdown: {audit.audio_markdown}",
        f"DownloadedMp4: {audit.downloaded_mp4}",
        f"FileTransSidecars: {audit.filetrans_sidecars}",
        f"DirtyMarkdown: {len(audit.dirty_markdown)}",
        f"IncompleteParts: {len(audit.incomplete_parts)}",
        f"OK: {audit.ok}",
    ]
    if audit.incomplete_parts:
        lines.append("")
        lines.append("Incomplete part details:")
        for part in audit.incomplete_parts[:20]:
            lines.append(
                f"- P{part.index}: board={len(part.board_files)} audio={len(part.audio_files)} dirty={len(part.dirty_files)}"
            )
    if audit.dirty_markdown:
        lines.append("")
        lines.append("Dirty markdown examples:")
        lines.extend(f"- {path}" for path in audit.dirty_markdown[:20])
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="social_long output root")
    parser.add_argument("--expected-parts", type=int, help="expected number of part directories and markdown pairs")
    parser.add_argument("--json", action="store_true", help="write JSON instead of text")
    return parser.parse_args(argv)


def write_stdout(text: str) -> None:
    try:
        print(text)
    except UnicodeEncodeError:
        sys.stdout.buffer.write((text + "\n").encode("utf-8"))


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    audit = audit_course_output(args.root, expected_parts=args.expected_parts)
    if args.json:
        write_stdout(json.dumps(asdict(audit), ensure_ascii=False, indent=2))
    else:
        write_stdout(format_text_report(audit))
    return 0 if audit.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
