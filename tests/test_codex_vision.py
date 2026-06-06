import os
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from OCRLLM.config import AppConfig, CodexVisionConfig
from OCRLLM.core.codex_vision import (
    CODEX_VISION_BATCH_SIZE,
    CODEX_VISION_MAX_PARALLEL,
    CodexCLIUnavailableError,
    CodexVisionRunner,
    apply_codex_vision_runtime_limits,
    inspect_codex_cli,
)
from OCRLLM.core.llm_client import LLMClient


class CodexVisionRunnerTests(unittest.TestCase):
    def test_default_codex_vision_model_is_image_capable_mini(self):
        cfg = CodexVisionConfig()

        self.assertEqual(cfg.model, "gpt-5.4-mini")
        self.assertEqual(cfg.reasoning_effort, "medium")

    def test_runner_uses_read_only_ask_style_exec_without_tools(self):
        cfg = AppConfig(
            codex_vision=CodexVisionConfig(
                enabled=True,
                command="codex",
                model="gpt-5.4-mini",
                reasoning_effort="medium",
            )
        )
        calls = []

        def fake_run(cmd, **kwargs):
            calls.append(cmd)
            output_path = cmd[cmd.index("--output-last-message") + 1]
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("OCR TEXT")
            return SimpleNamespace(returncode=0, stdout="", stderr="")

        with tempfile.NamedTemporaryFile(suffix=".png") as img, \
                patch("OCRLLM.core.codex_vision.shutil.which", return_value="/usr/bin/codex"), \
                patch("OCRLLM.core.codex_vision.subprocess.run", side_effect=fake_run):
            result = CodexVisionRunner(cfg.codex_vision).recognize("read", [img.name])

        self.assertEqual(result, "OCR TEXT")
        cmd = calls[0]
        self.assertIn("exec", cmd)
        self.assertIn("--ephemeral", cmd)
        self.assertIn("--ignore-user-config", cmd)
        self.assertIn("--ignore-rules", cmd)
        self.assertIn("--skip-git-repo-check", cmd)
        self.assertIn("--sandbox", cmd)
        self.assertEqual(cmd[cmd.index("--sandbox") + 1], "read-only")
        self.assertIn("--ask-for-approval", cmd)
        self.assertEqual(cmd[cmd.index("--ask-for-approval") + 1], "never")
        self.assertIn("-m", cmd)
        self.assertEqual(cmd[cmd.index("-m") + 1], "gpt-5.4-mini")
        self.assertIn('model_reasoning_effort="medium"', cmd)
        self.assertEqual(cmd[-2], "--")
        self.assertIn("用户原始提示:\nread", cmd[-1])
        for disabled in ["shell_tool", "browser_use", "computer_use", "apps", "multi_agent", "image_generation"]:
            disable_positions = [i for i, part in enumerate(cmd) if part == "--disable"]
            self.assertTrue(any(cmd[i + 1] == disabled for i in disable_positions))

    def test_llm_client_can_use_codex_vision_without_api_key(self):
        cfg = AppConfig(codex_vision=CodexVisionConfig(enabled=True))
        with patch("OCRLLM.core.llm_client.CodexVisionRunner") as runner_cls:
            runner_cls.return_value.recognize.return_value = "TEXT"
            client = LLMClient(cfg)
            result = client.chat_with_images("read", ["a.png"], max_retries=1)

        self.assertEqual(result, "TEXT")
        runner_cls.return_value.recognize.assert_called_once_with("read", ["a.png"])

    def test_runtime_limits_force_two_parallel_batches_and_five_images(self):
        cfg = AppConfig().with_updates(
            codex_vision={"enabled": True},
            concurrency={"llm_parallel_requests": 99},
            processing={"batch_size": 20},
            video={"batch_size": 30},
        )

        limited = apply_codex_vision_runtime_limits(cfg)

        self.assertEqual(limited.concurrency.llm_parallel_requests, CODEX_VISION_MAX_PARALLEL)
        self.assertEqual(limited.processing.batch_size, CODEX_VISION_BATCH_SIZE)
        self.assertEqual(limited.video.batch_size, CODEX_VISION_BATCH_SIZE)

    def test_env_codex_mode_applies_runtime_limits_for_cli_entrypoints(self):
        with patch.dict(os.environ, {"OCRLLM_CODEX_VISION_ENABLED": "1"}, clear=True):
            cfg = AppConfig.from_env()

        self.assertTrue(cfg.codex_vision.enabled)
        self.assertEqual(cfg.models.vision_model, "gpt-5.4-mini")
        self.assertEqual(cfg.concurrency.llm_parallel_requests, CODEX_VISION_MAX_PARALLEL)
        self.assertEqual(cfg.processing.batch_size, CODEX_VISION_BATCH_SIZE)
        self.assertEqual(cfg.video.batch_size, CODEX_VISION_BATCH_SIZE)


class CodexInspectionTests(unittest.TestCase):
    def test_inspection_rejects_missing_image_or_disable_support(self):
        def fake_run(cmd, **_kwargs):
            if cmd[-1] == "--version":
                return SimpleNamespace(returncode=0, stdout="codex-cli 0.135.0", stderr="")
            if cmd == ["codex", "--help"]:
                return SimpleNamespace(returncode=0, stdout="Usage: codex\n  --ask-for-approval\n", stderr="")
            if cmd[:2] == ["codex", "exec"]:
                return SimpleNamespace(returncode=0, stdout="Usage: codex exec\n  --image\n  --sandbox\n", stderr="")
            return SimpleNamespace(returncode=0, stdout='{"models":[]}', stderr="")

        with patch("OCRLLM.core.codex_vision.shutil.which", return_value="/usr/bin/codex"), \
                patch("OCRLLM.core.codex_vision.subprocess.run", side_effect=fake_run):
            report = inspect_codex_cli(CodexVisionConfig(model="gpt-5.3-codex-spark"))

        self.assertFalse(report.ok)
        self.assertIn("--disable", report.message)

    def test_runner_rejects_more_than_five_images(self):
        cfg = CodexVisionConfig(enabled=True)
        runner = CodexVisionRunner(cfg)

        with self.assertRaises(CodexCLIUnavailableError):
            runner.recognize("read", [f"{i}.png" for i in range(CODEX_VISION_BATCH_SIZE + 1)])


if __name__ == "__main__":
    unittest.main()
