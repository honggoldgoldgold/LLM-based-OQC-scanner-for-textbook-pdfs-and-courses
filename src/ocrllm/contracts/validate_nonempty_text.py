"""Validate nonempty protocol text without echoing caller data."""


def validate_nonempty_text(value: object, *, field_name: str) -> str:
    """Return stripped-safe original text or raise a redacted error."""

    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be nonempty text")
    return value
