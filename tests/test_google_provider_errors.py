import unittest

from OCRLLM.core.providers.google_provider import (
    GoogleErrorKind,
    classify_google_error,
    google_retry_delay_seconds,
)


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


if __name__ == "__main__":
    unittest.main()
