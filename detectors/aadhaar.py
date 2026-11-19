"""Conservative detector for Aadhaar-shaped 12-digit values."""

import re

from detectors.base import Candidate

PATTERN = re.compile(r"(?<!\d)\d{4}(?:[ \t]?\d{4}){2}(?!\d)")


def detect(text: str) -> list[Candidate]:
    return [
        Candidate(
            kind="aadhaar_like",
            start=match.start(),
            end=match.end(),
            value=match.group(),
            detector="aadhaar_format_regex_v1",
            confidence="medium",
            notes="Matches a 12-digit Aadhaar-like format only; no UIDAI or government validation was performed.",
        )
        for match in PATTERN.finditer(text)
    ]
