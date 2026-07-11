"""Build one complete-board prompt with a silent symbol audit."""

from __future__ import annotations


def build_board_symbol_audit_prompt(base_prompt: str) -> str:
    """Return a source-faithful prompt that inventories small signs silently."""

    if type(base_prompt) is not str or not base_prompt.strip():
        raise ValueError("base_prompt must be nonempty plain text")
    return (
        f"{base_prompt} Independently transcribe the entire images. Before returning, "
        "silently inventory every text-bearing region and every standalone visible sign "
        "or operator, including small +, -, =, relation, and arrow marks. Preserve exact "
        "case, identifiers, numbers, signs, and formula atoms. Treat hatch, fill, shading, "
        "and texture strokes as drawing rather than text. Return only complete Markdown."
        " Markdown structure may organize only text and labels literally visible in the "
        "source. Never create region captions, diagram descriptions, item numbering, "
        "shape names, or positional words such as left, right, top, middle, circle, or "
        "segment unless those exact words are visibly written. Do not append explanatory "
        "sections or prefix visible labels with invented words such as Diagram or Labels."
    )
