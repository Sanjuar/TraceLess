from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_text_scan_returns_masked_findings_and_offsets():
    text = "Email alex@example.com; call +91 98765 43210."
    response = client.post("/api/v1/scans/text", json={"text": text})
    assert response.status_code == 200
    payload = response.json()
    assert payload["summary"]["total_findings"] == 2
    assert [item["type"] for item in payload["findings"]] == ["email", "phone"]
    assert "alex@example.com" not in response.text
    assert "98765 43210" not in response.text
    for item in payload["findings"]:
        assert text[item["start_offset"]:item["end_offset"]]
        assert item["value_masked"] not in ("alex@example.com", "+91 98765 43210")
        assert item["source"] == "pasted_text"


def test_validation_errors_are_safe_and_oversized_text_is_413():
    invalid = client.post("/api/v1/scans/text", json={"text": ""})
    assert invalid.status_code == 422
    assert "detail" not in invalid.json()
    oversized = client.post("/api/v1/scans/text", json={"text": "x" * 50001})
    assert oversized.status_code == 413
    assert oversized.json()["error"]["code"] == "payload_too_large"


def test_mask_values_false_never_reveals_values():
    response = client.post("/api/v1/scans/text", json={"text": "alex@example.com", "options": {"mask_values": False}})
    assert response.status_code == 200
    assert "alex@example.com" not in response.text


def test_detection_options_can_disable_contextual_categories():
    response = client.post(
        "/api/v1/scans/text",
        json={"text": "My name is Alex. I am 23 years old.", "options": {"detect_names": False, "detect_age": False}},
    )
    assert response.status_code == 200
    assert response.json()["findings"] == []
