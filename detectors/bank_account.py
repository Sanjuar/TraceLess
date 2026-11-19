import re

from detectors.base import Candidate

PATTERN = re.compile(r"\b(?:bank\s+)?account(?:\s+(?:number|no\.?))?\s*[:#=-]?\s*(\d(?:[ -]?\d){8,17})\b", re.I)


def detect(text: str) -> list[Candidate]:
    out = []
    for m in PATTERN.finditer(text):
        start, end = m.span(1)
        value = m.group(1)
        if sum(ch.isdigit() for ch in value) < 9:
            continue
        out.append(Candidate("bank_account_like", start, end, value, "bank_account_context_regex_v1", "low", "Number follows account context; existence, ownership and account validity are not verified."))
    return out
