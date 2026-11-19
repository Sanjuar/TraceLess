from dataclasses import dataclass
from typing import Literal

Confidence = Literal["high", "medium", "low"]


@dataclass(frozen=True)
class Candidate:
    kind: str
    start: int
    end: int
    value: str
    detector: str
    confidence: Confidence
    notes: str
    country_code: int | None = None
    country_region: str | None = None
    phone_national_digits: str | None = None
