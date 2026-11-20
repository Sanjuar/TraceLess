"""Conservative detector for Aadhaar-shaped 12-digit values."""

import re

from detectors.base import Candidate

PATTERN = re.compile(r"(?<!\d)\d{4}(?:[ \t]?\d{4}){2}(?!\d)")
PHONE_PREFIX_CHARACTERS = frozenset("+0123456789 \t().-")


def _follows_international_prefix(text: str, start: int) -> bool:
    """Reject Aadhaar-shaped digits attached to a nearby international `+` prefix."""
    prefix = text[max(0, start - 24):start]
    plus_index = prefix.rfind("+")
    if plus_index < 0:
        return False

    phone_prefix = prefix[plus_index:]
    if any(char not in PHONE_PREFIX_CHARACTERS for char in phone_prefix):
        return False
    if sum(char.isdigit() for char in phone_prefix) > 6:
        return False

    absolute_plus = start - len(prefix) + plus_index
    return absolute_plus == 0 or not text[absolute_plus - 1].isalnum()


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
        if not _follows_international_prefix(text, match.start())
    ]
