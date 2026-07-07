from pathlib import Path

from tools.audit_social_long_course_output import (
    AUDIO_SUFFIX,
    BOARD_SUFFIX,
    audit_course_output,
)
from tools.combine_social_long_course_markdowns import combine_course_markdowns


def write_part(root: Path, index: int, title: str = "intro") -> Path:
    part_dir = root / f"P{index}_{title}"
    part_dir.mkdir(parents=True)
    stem = f"{index:03d}_{title}"
    (part_dir / f"{stem}{BOARD_SUFFIX}").write_text(f"# board {index}\n", encoding="utf-8")
    (part_dir / f"{stem}{AUDIO_SUFFIX}").write_text(f"# audio {index}\n", encoding="utf-8")
    return part_dir


def test_audit_social_long_course_output_accepts_complete_course(tmp_path):
    write_part(tmp_path, 1)
    write_part(tmp_path, 2)
    downloads = tmp_path / "_downloads"
    downloads.mkdir()
    (downloads / "001_a.mp4").write_bytes(b"video")
    (downloads / "002_b.mp4").write_bytes(b"video")

    audit = audit_course_output(tmp_path, expected_parts=2)

    assert audit.ok
    assert audit.part_dirs == 2
    assert audit.board_markdown == 2
    assert audit.audio_markdown == 2
    assert audit.downloaded_mp4 == 2
    assert audit.filetrans_sidecars == 0


def test_audit_social_long_course_output_rejects_dirty_markdown(tmp_path):
    part_dir = write_part(tmp_path, 1)
    board_path = next(part_dir.glob(f"*{BOARD_SUFFIX}"))
    board_path.write_text("<!-- \u6279\u6b21 1 \u5931\u8d25: Reading additional input from stdin -->", encoding="utf-8")

    audit = audit_course_output(tmp_path, expected_parts=1)

    assert not audit.ok
    assert len(audit.incomplete_parts) == 1
    assert audit.dirty_markdown == [str(board_path.resolve())]


def test_combine_social_long_course_markdowns_writes_readable_pieces(tmp_path):
    write_part(tmp_path, 1, "intro")
    write_part(tmp_path, 2, "chapter")
    write_part(tmp_path, 3, "review")

    written = combine_course_markdowns(
        tmp_path,
        videos_per_piece=2,
        course_title="Course",
        mode="paired",
    )

    assert [path.name for path in written] == ["P001-P002_study.md", "P003-P003_study.md"]
    first = written[0].read_text(encoding="utf-8")
    assert "# Course P001-P002" in first
    assert "## P001 intro" in first
    assert "### Board Recognition" in first
    assert "# board 1" in first
    assert "### Audio Recognition" in first
    assert "# audio 2" in first
