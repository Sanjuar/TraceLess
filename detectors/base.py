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
