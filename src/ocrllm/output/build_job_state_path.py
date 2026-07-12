"""Build the fixed sibling state path for one final Markdown output."""

from pathlib import Path


def build_job_state_path(output_path: Path) -> Path:
    """Append the version-one state suffix to the final Markdown stem."""
    return output_path.with_name(f"{output_path.stem}.ocrllm-state.json")
