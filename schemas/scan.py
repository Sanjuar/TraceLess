from pydantic import BaseModel, ConfigDict, Field

from config import MAX_TEXT_CHARACTERS


class ScanOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    detect_names: bool = True
    detect_age: bool = True
    mask_values: bool = True
    # This phase is deliberately ephemeral; persistence is not implemented.
    persist_scan: bool = False


class TextScanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1, max_length=MAX_TEXT_CHARACTERS)
    options: ScanOptions = Field(default_factory=ScanOptions)
