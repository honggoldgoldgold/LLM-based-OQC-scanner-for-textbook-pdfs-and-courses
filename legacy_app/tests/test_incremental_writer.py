from OCRLLM.core.incremental_writer import IncrementalMDWriter


def test_incremental_writer_shortens_temp_path_for_long_output_names(tmp_path):
    filename = (
        "008_Modern Robotics, Chapter 2.4_ Configuration and Velocity Constraints_"
        "A14ArEZ47LE_\u677f\u4e66\u8bc6\u522b.md"
    )
    output_path = None
    for repeat in range(1, 80):
        candidate_dir = tmp_path / ("P8_" + ("x" * repeat))
        candidate = candidate_dir / filename
        normal_tmp = candidate.with_name(candidate.name + ".tmp")
        output_len = len(str(candidate.resolve(strict=False)))
        normal_tmp_len = len(str(normal_tmp.resolve(strict=False)))
        if output_len <= 240 < normal_tmp_len:
            output_path = candidate
            break
    assert output_path is not None
    output_path.parent.mkdir(parents=True)

    writer = IncrementalMDWriter(str(output_path), total_slots=2)
    temp_path = writer._temp_path()

    assert len(str(temp_path.resolve(strict=False))) <= 240
    assert temp_path.name != output_path.name + ".tmp"

    writer.write_slot(1, "second")
    writer.write_slot(0, "first")
    writer.finalize()

    assert output_path.read_text(encoding="utf-8") == "first\n\nsecond"
    assert not temp_path.exists()
