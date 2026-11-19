"""International phone detection backed by Google's libphonenumber metadata."""

import phonenumbers
from phonenumbers import PhoneNumberMatcher

from detectors.base import Candidate

PHONE_CONTEXT = ("phone", "mobile", "cell", "call", "telephone", "tel", "contact", "whatsapp")


def _has_phone_context(text: str, start: int, end: int) -> bool:
    before = text[max(0, start - 36):start].lower()
    after = text[end:min(len(text), end + 24)].lower()
    return any(marker in before or marker in after for marker in PHONE_CONTEXT)


def detect(text: str, default_region: str | None = None) -> list[Candidate]:
    """Find libphonenumber-valid international numbers in the original text.

    Explicit `+` country calling codes work without a region. `default_region`
    remains an optional compatibility hook for callers that intentionally want
    national-format parsing; the application API does not set a default region.
    """
    region = default_region.upper() if default_region else None
    if region and region not in phonenumbers.SUPPORTED_REGIONS:
        region = None

    found: list[Candidate] = []
    for match in PhoneNumberMatcher(text, region, leniency=phonenumbers.Leniency.VALID):
        number = match.number
        if not phonenumbers.is_valid_number(number):
            continue

        raw = match.raw_string
        explicit_international = raw.lstrip().startswith("+")
        if not explicit_international:
            # Without an explicit region there is no safe interpretation for a
            # national number. Even with one, require recognizable context or
            # formatting so arbitrary digit sequences are not treated as phones.
            if region is None:
                continue
            formatted = any(separator in raw for separator in " -()\t")
            if not formatted and not _has_phone_context(text, match.start, match.end):
                continue

        national_digits = phonenumbers.national_significant_number(number)
        found.append(
            Candidate(
                kind="phone",
                start=match.start,
                end=match.end,
                value=raw,
                detector="phone_libphonenumber_v1",
                confidence="high",
                notes=(
                    "Number is valid according to libphonenumber metadata; this does not verify assignment, "
                    "reachability or ownership. National-format interpretation used the explicitly supplied region."
                    if not explicit_international
                    else "Number is valid according to libphonenumber metadata; this does not verify assignment, reachability or ownership."
                ),
                country_code=number.country_code,
                country_region=phonenumbers.region_code_for_number(number),
                phone_national_digits=national_digits,
            )
        )

    return found
