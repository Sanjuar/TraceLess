import re

from detectors.base import Candidate

PATTERN = re.compile(r"(?<![A-Z0-9])[A-Z]{5}\d{4}[A-Z](?![A-Z0-9])", re.I)


def detect(text: str) -> list[Candidate]:
    return [Candidate("pan_like", m.start(), m.end(), m.group(), "pan_format_regex_v1", "high", "Matches the Indian PAN format only; no government validation was performed.") for m in PATTERN.finditer(text)]
