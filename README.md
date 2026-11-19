# TraceLess

TraceLess is a local-first, regex-first prototype for reviewing pasted text for possible personal information exposure. Phase 0 and Phase 1 provide a FastAPI service and an ephemeral text parser. Requests are processed in memory; this milestone has no database, uploads, URL fetching, cloud AI, or breach provider.

## Local setup

Requires Python 3.10 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn main:app --reload
```

The API is at `http://127.0.0.1:8000`; interactive docs are at `/docs` and `/redoc`. Health check: `GET /health`. To change the text limit, export `TRACELESS_MAX_TEXT_CHARACTERS` in the shell before starting the app. `.env.example` documents the optional setting; the application reads process environment variables directly.

## Text scan

`POST /api/v1/scans/text` accepts arbitrary unstructured text (up to 50,000 characters by default):

```json
{
  "text": "Contact alex@example.com or +91 98765 43210. I am 23 years old.",
  "options": {"detect_names": true, "detect_age": true}
}
```

Responses contain a random scan ID, masked findings, character offsets into the original submitted string, sanitized evidence snippets, detector identifiers, caveats, and a summary. Values are always masked; `mask_values: false` is not a reveal mechanism. `persist_scan` is accepted for forward compatibility but has no effect: Phase 1 never stores scan text or results. The service does not log request bodies.

Run the test suite with `pytest -q`.

## Detector limits

- Email detects email-shaped strings; it does not verify ownership or delivery.
- Phone detection requires an international prefix or nearby phone/contact context. It does not validate numbering plans or ownership.
- PAN detection checks format only, not government records.
- Age detection requires a phrase such as “age 24” or “24 years old”; it is an unverified claim.
- Name candidates require contextual phrases/sign-offs and can be false positives.
- Certificate IDs require certificate context because there is no universal format.
- Bank-account-like numbers require account context; no account existence or ownership is checked.

All detectors are heuristic. A missing finding does not establish that no personal information is present. No third-party lookup or network request occurs.
