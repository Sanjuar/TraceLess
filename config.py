"""Small environment-backed limits for the local prototype."""

import os

MAX_TEXT_CHARACTERS = int(os.getenv("TRACELESS_MAX_TEXT_CHARACTERS", "50000"))
EVIDENCE_CONTEXT_CHARACTERS = 32
