from fastapi import APIRouter

from schemas.finding import ScanResponse
from schemas.scan import TextScanRequest
from services.scan_service import scan_text

router = APIRouter(prefix="/scans", tags=["scans"])


@router.post("/text", response_model=ScanResponse)
def analyze_text(request: TextScanRequest) -> ScanResponse:
    """Analyze pasted text in memory; raw input is not persisted or logged."""
    return scan_text(request.text, request.options)
