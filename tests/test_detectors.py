from detectors.registry import detect_all
from services.masking_service import mask_value


def kinds(text, phone_region=None):
    return [candidate.kind for candidate in detect_all(text, phone_region=phone_region)]


def test_email_pan_age_and_phone_in_unstructured_text():
    text = "Contact alex@example.com or +91 98765 43210. PAN ABCDE1234F; age 23."
    found = detect_all(text)
    assert [item.kind for item in found] == ["email", "phone", "pan_like", "age"]
    assert text[found[0].start:found[0].end] == "alex@example.com"
    assert found[0].confidence == "high"


def test_bare_national_phone_requires_configured_region_and_context():
    assert "phone" not in kinds("Order number 1234567890")
    assert "phone" not in kinds("Call 98765 43210")
    assert "phone" in kinds("Call 98765 43210", phone_region="IN")
    assert "bank_account_like" not in kinds("Order number 1234567890")


def test_contextual_age_bounds_and_name_certificate_bank_candidates():
    assert "age" in kinds("I am 23 years old")
    assert "age" not in kinds("Age 999")
    found = detect_all("My name is Alex Morgan. Certificate ID: CERT-2025-009. Account no: 123456789012")
    assert {item.kind for item in found} == {"name", "certificate_id", "bank_account_like"}


def test_masking_does_not_expose_sensitive_tail_except_limited_suffix():
    email = detect_all("alexandra@example.com")[0]
    assert mask_value(email) == "a*******a@example.com"
    pan = detect_all("ABCDE1234F")[0]
    assert mask_value(pan) == "AB*******F"


def test_false_positive_boundaries():
    assert "email" not in kinds("not-an-email")
    assert "pan_like" not in kinds("XABCDE1234FY")


def test_offsets_remain_original_character_offsets_with_unicode():
    text = "नमस्ते 🙂 alex@example.com"
    found = detect_all(text)
    assert len(found) == 1
    assert text[found[0].start:found[0].end] == "alex@example.com"
