import re

from detectors.base import Candidate

PATTERN = re.compile(r"\b(?:age\s*[:=]?\s*(\d{1,3})|aged\s+(\d{1,3})|(\d{1,3})\s+years?\s+old)\b", re.I)


def detect(text: str) -> list[Candidate]:
    out = []
    for m in PATTERN.finditer(text):
        value = next(group for group in m.groups() if group is not None)
        age = int(value)
        if not 0 <= age <= 120:
            continue
        out.append(Candidate("age", m.start(), m.end(), m.group(), "age_context_regex_v1", "medium", "Age phrase matched; this is an unverified text claim."))
    return out
