"""Count source-equivalent representations of one standalone sign."""

from __future__ import annotations

import re

from .parse_standalone_sign_ledger import SUPPORTED_STANDALONE_SIGNS


_RELATION_REPRESENTATION = {
    "<=": re.compile(r"(?<![<>=])(?:<=|≤)(?![=])|\\(?:le|leq|leqslant)\b"),
    "≤": re.compile(r"(?<![<>=])(?:<=|≤)(?![=])|\\(?:le|leq|leqslant)\b"),
    ">=": re.compile(r"(?<![<>=])(?:>=|≥)(?![=])|\\(?:ge|geq|geqslant)\b"),
    "≥": re.compile(r"(?<![<>=])(?:>=|≥)(?![=])|\\(?:ge|geq|geqslant)\b"),
}
_TOKEN_WRAPPERS = "`*_~$()[]{}.,;:!?"


def count_standalone_sign_representations(markdown: str, sign: str) -> int:
    """Return a conservative count of exact or source-equivalent sign forms."""

    if type(markdown) is not str:
        raise ValueError("markdown must be plain text")
    if type(sign) is not str or sign not in SUPPORTED_STANDALONE_SIGNS:
        raise ValueError("sign must be one supported standalone sign")

    relation_pattern = _RELATION_REPRESENTATION.get(sign)
    if relation_pattern is not None:
        return sum(1 for _ in relation_pattern.finditer(markdown))
    return sum(
        _unwrap_markdown_token(token) == sign
        for token in markdown.split()
    )


def _unwrap_markdown_token(token: str) -> str:
    return token.strip(_TOKEN_WRAPPERS)
