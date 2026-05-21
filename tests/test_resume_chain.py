import os
import tempfile
import time
import unittest

from OCRLLM.core.checkpoint import Checkpoint, CheckpointManager
from OCRLLM.processors.pdf import PDFProcessor
from OCRLLM.processors.video import VideoProcessor
from OCRLLM.processors.video_pipeline import BoardRecognizePhase, VideoPhase, VideoProcessContext


class ResumeContractTests(unittest.TestCase):
    def test_pdf_resume_options_restore_original_contract(self):
        checkpoint = Checkpoint(
            task_type="pdf",
            source_path="book.pdf",
            output_path="book_识别.md",
            total_items=3,
            extra={
                "page_range": [11, 20],
                "page_offset": 10,
                "batch_size": 10,
                "prompt_template": "custom-prompt",
            },
        )

        self.assertEqual(
            PDFProcessor.resume_options_from_checkpoint(checkpoint),
            {
                "pdf_path": "book.pdf",
                "need_formula": True,
                "output_path": "book_识别.md",
                "page_range": (11, 20),
                "prompt_template": "custom-prompt",
                "resume": True,
            },
        )

    def test_video_resume_options_restore_original_contract(self):
        checkpoint = Checkpoint(
            task_type="video",
            source_path="lecture.mp4",
            output_path="out/lecture",
            total_items=5,
            extra={
                "stem": "lecture",
                "phases": [1, 2, 3, 4],
                "skip_audio": True,
                "prompt_template": "board-prompt",
            },
        )

        self.assertEqual(
            VideoProcessor.resume_options_from_checkpoint(checkpoint),
            {
                "video_path": "lecture.mp4",
                "output_dir": "out/lecture",
                "phases": [1, 2, 3, 4],
                "skip_audio": True,
                "prompt_template": "board-prompt",
                "resume": True,
            },
        )

    def test_list_incomplete_returns_latest_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            src1 = os.path.join(tmp, "a.pdf")
            src2 = os.path.join(tmp, "b.mp4")
            open(src1, "w", encoding="utf-8").close()
            open(src2, "w", encoding="utf-8").close()

            mgr = CheckpointManager(tmp)
            cp1 = Checkpoint("pdf", src1, os.path.join(tmp, "a.md"), 3)
            cp2 = Checkpoint("video", src2, os.path.join(tmp, "b"), 5)
            cp1.updated_at = time.time() - 10
            cp2.updated_at = time.time()
            mgr.save(cp1)
            mgr.save(cp2)

            listed = mgr.list_incomplete()
            self.assertEqual([cp.task_type for cp in listed], ["video", "pdf"])

    def test_select_incomplete_preserves_preferred_checkpoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            src1 = os.path.join(tmp, "a.pdf")
            src2 = os.path.join(tmp, "b.mp4")
            open(src1, "w", encoding="utf-8").close()
            open(src2, "w", encoding="utf-8").close()

            mgr = CheckpointManager(tmp)
            pdf_cp = Checkpoint("pdf", src1, os.path.join(tmp, "a.md"), 3)
            video_cp = Checkpoint("video", src2, os.path.join(tmp, "b"), 5)
            pdf_cp.updated_at = time.time()
            video_cp.updated_at = time.time() - 10
            mgr.save(pdf_cp)
            mgr.save(video_cp)

            selected = mgr.select_incomplete(preferred_key=video_cp.resume_key)

            self.assertIsNotNone(selected)
            self.assertEqual(selected.resume_key, video_cp.resume_key)


class VideoPhase4ResumeTests(unittest.TestCase):
    def _make_context(self, tmp: str) -> VideoProcessContext:
        return VideoProcessContext(
            video_path="lecture.mp4",
            output_dir=tmp,
            frames_dir=os.path.join(tmp, "提取帧"),
            debug_dir=tmp,
            info_path=os.path.join(tmp, "frame_info.json"),
            stem="lecture",
            selected_phases=[4],
            skip_audio=False,
        )

    def _write_frame_info(self, tmp: str, frame_ids: list[str]) -> list[dict]:
        frame_dir = os.path.join(tmp, "提取帧")
        os.makedirs(frame_dir, exist_ok=True)
        frame_results = []
        for index, frame_id in enumerate(frame_ids):
            path = os.path.join(frame_dir, f"{frame_id}.jpg")
            with open(path, "w", encoding="utf-8") as f:
                f.write("frame")
            frame_results.append({"path": path, "timestamp": index * 10.0, "frame_idx": index})
        with open(os.path.join(tmp, "frame_info.json"), "w", encoding="utf-8") as f:
            import json
            json.dump(frame_results, f, ensure_ascii=False)
        return frame_results

    def _write_board_md(self, tmp: str, sections: list[tuple[str, str]]):
        board_path = os.path.join(tmp, "lecture_板书识别.md")
        content = []
        for frame_id, time_str in sections:
            content.extend([
                f"<!-- meta:frame id={frame_id} time={time_str} -->",
                f"内容 {frame_id}",
                "",
            ])
        with open(board_path, "w", encoding="utf-8") as f:
            f.write("\n".join(content))
        return board_path

    def test_phase4_can_resume_when_board_matches_frame_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            frame_ids = ["board_001_010s", "board_002_020s"]
            self._write_frame_info(tmp, frame_ids)
            self._write_board_md(tmp, [("board_001_010s", "0:10"), ("board_002_020s", "0:20")])
            with open(os.path.join(tmp, "lecture_热词表.txt"), "w", encoding="utf-8") as f:
                f.write("梯度\n步长\n")

            processor = VideoProcessor.__new__(VideoProcessor)
            context = self._make_context(tmp)
            phase = BoardRecognizePhase()

            self.assertTrue(phase.can_resume(processor, context))
            self.assertEqual(context.hotwords, ["梯度", "步长"])

    def test_phase4_rejects_board_when_frame_headers_do_not_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._write_frame_info(tmp, ["board_001_010s", "board_002_020s"])
            self._write_board_md(tmp, [("board_001_010s", "0:10")])

            processor = VideoProcessor.__new__(VideoProcessor)
            context = self._make_context(tmp)

            self.assertFalse(BoardRecognizePhase().can_resume(processor, context))


class VideoInvalidationTests(unittest.TestCase):
    class _DummyTracker:
        def start_phase(self, *args, **kwargs):
            pass

        def finish_phase(self, *args, **kwargs):
            pass

    class _DummyCheckpointManager:
        def __init__(self):
            self.saved = []

        def save(self, checkpoint):
            self.saved.append(sorted(checkpoint.completed_indices))

        def save_incremental(self, checkpoint, index):
            checkpoint.mark_completed(index)
            self.saved.append(sorted(checkpoint.completed_indices))

    class _DummyProcessor:
        def __init__(self):
            self.tracker = VideoInvalidationTests._DummyTracker()
            self.checkpoint_mgr = VideoInvalidationTests._DummyCheckpointManager()
            self.cleared = []

        def _clear_invalidated_phase_artifacts(self, output_dir, stem, invalidated):
            self.cleared.append((output_dir, stem, tuple(sorted(invalidated))))

    class _DummyPhase(VideoPhase):
        phase_id = 3
        phase_key = "phase3"
        phase_name = "phase3"

        def can_resume(self, processor, context):
            return False

        def execute(self, processor, context):
            return True

    def test_invalidated_video_phases_are_persisted_before_rerun(self):
        processor = self._DummyProcessor()
        checkpoint = Checkpoint("video", "src.mp4", "out_dir", 5, completed_indices={1, 2, 3, 4, 5})
        context = VideoProcessContext(
            video_path="src.mp4",
            output_dir="out_dir",
            frames_dir="frames",
            debug_dir="debug",
            info_path="info.json",
            stem="demo",
            selected_phases=[3, 4, 5],
            skip_audio=False,
        )
        completed = set(checkpoint.completed_indices)

        self._DummyPhase().run(processor, context, checkpoint, completed)

        self.assertEqual(completed, {1, 2})
        self.assertEqual(checkpoint.completed_indices, {1, 2, 3})
        self.assertEqual(processor.checkpoint_mgr.saved[0], [1, 2])
        self.assertEqual(processor.checkpoint_mgr.saved[1], [1, 2, 3])
        self.assertEqual(processor.cleared, [("out_dir", "demo", (3, 4, 5))])


if __name__ == "__main__":
    unittest.main()