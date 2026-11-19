import re

from detectors.base import Candidate

PATTERN = re.compile(r"\b(?:my\s+name\s+is|name\s*[:=]|regards[, ]+|sincerely[, ]+)\s*([A-Z][\w'’-]*(?:\s+[A-Z][\w'’-]*){0,2})", re.I)


def detect(text: str) -> list[Candidate]:
    out = []
    for m in PATTERN.finditer(text):
        value = m.group(1).strip(" ,.;:")
        start = m.start(1)
        end = start + len(value)
        out.append(Candidate("name", start, end, value, "name_context_regex_v1", "low", "Contextual name candidate only; it may be a place, organization or other text and is not identity proof."))
    return out
