from uuid import uuid4

from detectors.registry import detect_all
from schemas.finding import Finding, ScanResponse, ScanSummary
from schemas.scan import ScanOptions
from services.masking_service import mask_value, sanitized_evidence


def scan_text(text: str, options: ScanOptions) -> ScanResponse:
    candidates = detect_all(
        text,
        detect_names=options.detect_names,
        detect_age=options.detect_age,
    )
    findings = [
        Finding(
            id=str(index),
            type=candidate.kind,
            value_masked=mask_value(candidate),
            confidence=candidate.confidence,
            start_offset=candidate.start,
            end_offset=candidate.end,
            evidence_snippet=sanitized_evidence(text, candidate, candidates),
            detector=candidate.detector,
            notes=candidate.notes,
            country_code=candidate.country_code,
            country_region=candidate.country_region,
        )
        for index, candidate in enumerate(candidates, start=1)
    ]
    # `mask_values=false` cannot reveal values in this privacy-first milestone.
    return ScanResponse(scan_id=str(uuid4()), findings=findings, summary=ScanSummary(total_findings=len(findings)))
