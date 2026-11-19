"""TraceLess local API entry point."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from routers.health import router as health_router
from routers.scans import router as scans_router

app = FastAPI(
    title="TraceLess",
    description="Local-first, regex-first digital footprint text analyzer.",
    version="0.1.0",
)
app.include_router(health_router)
app.include_router(scans_router, prefix="/api/v1")


@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    oversized = any(error.get("type") == "string_too_long" for error in exc.errors())
    status = 413 if oversized else 422
    code = "payload_too_large" if oversized else "invalid_request"
    message = "Text exceeds the configured character limit." if oversized else "Request body is invalid."
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})
