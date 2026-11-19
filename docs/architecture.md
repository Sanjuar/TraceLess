# Phase 0/1 architecture

`main.py` creates the FastAPI app and registers the health and versioned text-scan routers. The scan endpoint validates a Pydantic request, calls the in-memory scan service, runs independent regex detectors through a registry, resolves overlaps deterministically, and builds a typed masked response. No raw text is persisted or logged, and no external service is called.

Offsets are Python character offsets into the submitted string. Current detectors match the original text directly, so no lossy normalization step is needed. Confidence is a qualitative label with category-specific caveats, not a probability or identity assertion.
