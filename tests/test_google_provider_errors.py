import unittest

from OCRLLM.core.providers.google_provider import (
    ClassifiedGoogleError,
    GoogleErrorKind,
    GoogleProviderClient,
    GoogleProviderFailure,
    classify_google_error,
    google_retry_delay_seconds,
)
from OCRLLM.config import AppConfig


class GoogleProviderErrorTests(unittest.TestCase):
    def test_quota_exhaustion_switches_model_without_retrying_same_model(self):
        classified = classify_google_error(RuntimeError(
            "RESOURCE_EXHAUSTED: You exceeded your current quota, "
            "please check your plan and billing details."
        ))

        self.assertEqual(classified.kind, GoogleErrorKind.QUOTA_EXHAUSTED)
        self.assertTrue(classified.should_switch_model)
        self.assertFalse(classified.should_retry_same_model)

    def test_rate_limit_retries_same_model_before_user_visible_failure(self):
        classified = classify_google_error(RuntimeError(
            "429 Too Many Requests: rate limit exceeded for current project"
        ))

        self.assertEqual(classified.kind, GoogleErrorKind.RATE_LIMIT)
        self.assertFalse(classified.should_switch_model)
        self.assertTrue(classified.should_retry_same_model)

    def test_404_model_error_switches_to_next_candidate(self):
        classified = classify_google_error(RuntimeError(
            '{"error":{"code":404,"status":"NOT_FOUND","message":"models/gemini-old is not found"}}'
        ))

        self.assertEqual(classified.kind, GoogleErrorKind.INVALID_MODEL)
        self.assertTrue(classified.should_switch_model)
        self.assertFalse(classified.should_retry_same_model)

    def test_network_error_retries_same_model(self):
        classified = classify_google_error(TimeoutError("timed out while connecting"))

        self.assertEqual(classified.kind, GoogleErrorKind.NETWORK)
        self.assertFalse(classified.should_switch_model)
        self.assertTrue(classified.should_retry_same_model)

    def test_rate_limit_waits_across_minute_window(self):
        classified = classify_google_error(RuntimeError(
            "429 Too Many Requests: rate limit exceeded for current project"
        ))

        self.assertGreaterEqual(google_retry_delay_seconds(classified, attempt=1), 60.0)

    def test_retry_delay_honors_google_retry_info(self):
        classified = classify_google_error(RuntimeError(
            '{"error":{"code":429,"status":"RESOURCE_EXHAUSTED",'
            '"message":"Rate limit exceeded",'
            '"details":[{"@type":"type.googleapis.com/google.rpc.RetryInfo",'
            '"retryDelay":"73s"}]}}'
        ))

        self.assertEqual(google_retry_delay_seconds(classified, attempt=1), 73.0)

    def test_provider_reuses_successful_model_after_switchable_failures(self):
        cfg = AppConfig().with_updates(google_api={"enabled": True, "api_key": "AIza-test"})
        client = GoogleProviderClient(cfg=cfg)
        calls: list[str] = []

        def fake_retry(model: str, _invoke, _max_retries: int) -> str:
            calls.append(model)
            if model == "broken-image-model":
                raise GoogleProviderFailure(ClassifiedGoogleError(
                    GoogleErrorKind.INVALID_MODEL,
                    should_switch_model=True,
                    should_retry_same_model=False,
                    message="404 model not found",
                ))
            return f"ok:{model}"

        client._retry_same_model = fake_retry

        first = client._call_with_model_switch(
            "broken-image-model",
            ["broken-image-model", "gemini-flash-latest"],
            "vision",
            lambda _model: "",
            max_retries=1,
        )
        second = client._call_with_model_switch(
            "broken-image-model",
            ["broken-image-model", "gemini-flash-latest"],
            "vision",
            lambda _model: "",
            max_retries=1,
        )

        self.assertEqual(first, "ok:gemini-flash-latest")
        self.assertEqual(second, "ok:gemini-flash-latest")
        self.assertEqual(calls, ["broken-image-model", "gemini-flash-latest", "gemini-flash-latest"])


if __name__ == "__main__":
    unittest.main()
