from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Confidence = Literal["high", "medium", "low"]


class Finding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    type: str
    value_masked: str
    confidence: Confidence
    start_offset: int = Field(ge=0)
    end_offset: int = Field(ge=0)
    evidence_snippet: str
    detector: str
    source: Literal["pasted_text"] = "pasted_text"
    notes: str


class ScanSummary(BaseModel):
    total_findings: int


class ScanResponse(BaseModel):
    scan_id: str
    status: Literal["completed"] = "completed"
    findings: list[Finding]
    summary: ScanSummary
