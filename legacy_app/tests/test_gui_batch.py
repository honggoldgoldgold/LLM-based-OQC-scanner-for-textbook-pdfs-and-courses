import os
import tempfile
import unittest

from OCRLLM.config import AppConfig
from OCRLLM.core.task_runner import ProgressReporter
from OCRLLM.gui.batch_tasks import (
    BatchFileTask,
    _resolve_batch_workers,
    _shared_batch_cfg,
    run_batch_tasks,
)
from OCRLLM.gui.widgets import join_paths_text, split_paths_text
from OCRLLM.processors.routing import route_input_paths


class PathTextTests(unittest.TestCase):
    def test_split_paths_text_filters_empty_entries(self):
        self.assertEqual(split_paths_text("a;b;; c "), ["a", "b", "c"])

    def test_join_paths_text_deduplicates_and_preserves_order(self):
        self.assertEqual(join_paths_text(["a", "b", "a", " c "]), "a;b;c")


class RoutingTests(unittest.TestCase):
    def test_same_type_multi_file_route_is_allowed_when_requested(self):
        with tempfile.TemporaryDirectory() as tmp:
            pdf1 = os.path.join(tmp, "a.pdf")
            pdf2 = os.path.join(tmp, "b.pdf")
            for path in [pdf1, pdf2]:
                open(path, "w", encoding="utf-8").close()

            routed = route_input_paths([pdf1, pdf2], allow_multiple_same_type=True)
            self.assertEqual(routed.spec.key, "pdf")
            self.assertEqual(list(routed.paths), [pdf1, pdf2])


class BatchRunnerTests(unittest.TestCase):
    def test_pdf_batch_workers_are_capped_for_default_config(self):
        cfg = AppConfig()

        workers = _resolve_batch_workers("pdf", cfg, 7)

        self.assertEqual(workers, 2)

    def test_pdf_batch_shares_auto_render_worker_budget(self):
        cfg = AppConfig()

        shared = _shared_batch_cfg(cfg, "pdf", 2)

        self.assertEqual(shared.concurrency.pdf_render_workers, 4)
        self.assertEqual(shared.concurrency.llm_parallel_requests, 7)

    def test_run_batch_tasks_reports_successes(self):
        messages = []
        reporter = ProgressReporter(on_progress=lambda current, total, message: messages.append((current, total, message)))
        cfg = AppConfig()
        tasks = [
            BatchFileTask(source_path="a.pdf", display_name="a.pdf", run=lambda task_cfg, child: "out-a.md"),
            BatchFileTask(source_path="b.pdf", display_name="b.pdf", run=lambda task_cfg, child: "out-b.md"),
        ]

        summary = run_batch_tasks(task_kind="pdf", task_label="PDF", cfg=cfg, reporter=reporter, tasks=tasks)

        self.assertIn("成功 2, 失败 0", summary)
        self.assertEqual(messages[0][0], 0)
        self.assertEqual(messages[-1][0], 2)

    def test_run_batch_tasks_raises_when_all_failed(self):
        reporter = ProgressReporter()
        cfg = AppConfig()
        tasks = [
            BatchFileTask(
                source_path="broken.pdf",
                display_name="broken.pdf",
                run=lambda task_cfg, child: (_ for _ in ()).throw(RuntimeError("boom")),
            )
        ]

        with self.assertRaises(RuntimeError) as ctx:
            run_batch_tasks(task_kind="pdf", task_label="PDF", cfg=cfg, reporter=reporter, tasks=tasks)

        self.assertIn("失败 1", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()