from detectors.aadhaar import detect as detect_aadhaar
from detectors.phone import detect as detect_phone
from detectors.registry import detect_all
from schemas.scan import ScanOptions
from services.masking_service import mask_value
from services.scan_service import scan_text


INTERNATIONAL_NUMBERS = [
    ("+91 98765 43210", 91, "IN"),
    ("+1 202-555-0123", 1, "US"),
    ("+44 20 7031 3000", 44, "GB"),
    ("+971 50 123 4567", 971, "AE"),
    ("+1 (416) 555-0123", 1, "CA"),
    ("+61 412 345 678", 61, "AU"),
    ("+49 30 12345678", 49, "DE"),
    ("+65 9123 4567", 65, "SG"),
]


def test_international_phones_cover_eight_regions_and_include_region_metadata():
    for value, calling_code, region in INTERNATIONAL_NUMBERS:
        found = detect_phone(f"Reach me at {value}")
        assert len(found) == 1
        assert found[0].kind == "phone"
        assert found[0].country_code == calling_code
        assert found[0].country_region == region
        assert found[0].detector == "phone_libphonenumber_v1"


def test_phone_masking_only_retains_last_two_national_digits():
    candidate = detect_phone("+44 (0)20 7031 3000")[0]
    masked = mask_value(candidate)
    assert masked == "********00"  # only the final two national-number digits remain
    assert "7031" not in masked
    assert "3000" not in masked


def test_region_is_required_for_national_numbers_and_91_prefix_is_configurable():
    ambiguous = "Call 2025550123"
    assert detect_phone(ambiguous) == []
    assert detect_phone("2025550123") == []
    assert detect_phone(ambiguous, default_region="US")  # nearby call context
    assert detect_phone("202-555-0123", default_region="US")  # formatted national number

    india_prefixed = detect_phone("Call 91 98765 43210", default_region="IN")
    assert len(india_prefixed) == 1
    assert india_prefixed[0].country_code == 91
    assert india_prefixed[0].country_region == "IN"
    assert detect_phone("91 98765 43210") == []  # no region means no country guess


def test_phone_separators_offsets_and_invalid_candidates():
    text = "🙂 Call: +1 (416) 555-0123; backup +61-412-345-678"
    found = detect_phone(text)
    assert len(found) == 2
    assert [text[item.start:item.end] for item in found] == ["+1 (416) 555-0123", "+61-412-345-678"]
    assert detect_phone("Phone: +999 12345 67890") == []
    assert detect_phone("Phone: +1 123 456 7890") == []
    assert detect_phone("National ID: 123-45-6789") == []
    assert detect_phone("+44 123 1234567") == []


def test_same_phone_is_not_duplicated_and_api_evidence_never_contains_full_value():
    text = "Phone: +91-98765-43210"
    findings = detect_all(text)
    phones = [item for item in findings if item.kind == "phone"]
    assert len(phones) == 1
    assert text[phones[0].start:phones[0].end] == "+91-98765-43210"

    response = scan_text(text, ScanOptions())
    phone = next(item for item in response.findings if item.type == "phone")
    assert phone.value_masked == "********10"
    assert "+91-98765-43210" not in phone.evidence_snippet
    assert phone.country_code == 91
    assert phone.country_region == "IN"
    assert phone.source == "pasted_text"


def test_aadhaar_like_accepts_compact_or_four_digit_groups_with_original_offsets():
    for raw in ("123456789012", "1234 5678 9012", "1234\t5678\t9012"):
        text = f"🙂 Aadhaar: {raw}"
        candidates = detect_aadhaar(text)
        assert len(candidates) == 1
        candidate = candidates[0]
        assert text[candidate.start:candidate.end] == raw
        assert candidate.kind == "aadhaar_like"
        assert candidate.detector == "aadhaar_format_regex_v1"
        assert "no UIDAI or government validation" in candidate.notes
        assert mask_value(candidate) == "**********12"


def test_aadhaar_boundaries_reject_short_and_longer_numbers():
    assert detect_aadhaar("12345678901") == []
    assert detect_aadhaar("1234567890123") == []
    assert detect_aadhaar("991234 5678 90123") == []


def test_contextual_identifiers_win_over_overlapping_aadhaar_shape():
    certificate = detect_all("Certificate ID: 123456789012")
    assert len(certificate) == 1
    assert certificate[0].kind == "certificate_id"

    account = detect_all("Account no: 123456789012")
    matching = [item for item in account if item.start == account[0].start]
    assert len(matching) == 1
    assert matching[0].kind == "bank_account_like"
