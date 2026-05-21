import unittest

from OCRLLM.core.progress_tracker import ProgressTracker


class ProgressTrackerTests(unittest.TestCase):
    def test_weighted_progress_uses_phase_fraction(self):
        tracker = ProgressTracker()
        tracker.start_task("pdf", total_items=100, phase_weights={"render": 0.2, "llm": 0.8})
        tracker.start_phase("render", "渲染", 10)
        tracker.update_phase("render", 5, "渲染中", total=10)

        snap = tracker.get_snapshot()

        self.assertAlmostEqual(snap["overall_percent"], 10.0)

    def test_weighted_progress_accumulates_finished_and_active_phases(self):
        tracker = ProgressTracker()
        tracker.start_task("video", phase_weights={"phase1": 0.25, "phase2": 0.75})
        tracker.start_phase("phase1", "音频提取", 1)
        tracker.finish_phase("phase1")
        tracker.start_phase("phase2", "抽帧", 8)
        tracker.update_phase("phase2", 4, "处理中", total=8)

        snap = tracker.get_snapshot()

        self.assertAlmostEqual(snap["overall_percent"], 62.5)

    def test_unweighted_progress_falls_back_to_completed_items(self):
        tracker = ProgressTracker()
        tracker.start_task("audio", total_items=5)
        tracker.increment_completed(2)

        snap = tracker.get_snapshot()

        self.assertAlmostEqual(snap["overall_percent"], 40.0)


if __name__ == "__main__":
    unittest.main()