import unittest

from OCRLLM.core.providers.google_provider import (
    GoogleErrorKind,
    classify_google_error,
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


if __name__ == "__main__":
    unittest.main()
