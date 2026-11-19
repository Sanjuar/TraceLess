import re

from detectors.base import Candidate

# Deliberately requires certificate context; there is no universal certificate ID format.
PATTERN = re.compile(r"\b(?:certificate|cert\.?)(?:\s+(?:number|no\.?|id))?\s*[:#=-]?\s*([A-Z0-9][A-Z0-9/-]{3,23})\b", re.I)


def detect(text: str) -> list[Candidate]:
    out = []
    for m in PATTERN.finditer(text):
        start, end = m.span(1)
        out.append(Candidate("certificate_id", start, end, m.group(1), "certificate_context_regex_v1", "low", "Identifier follows certificate context; formats vary and issuer/validity are not verified."))
    return out
