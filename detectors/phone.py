"""International phone detection backed by Google's libphonenumber metadata."""

import re

import phonenumbers
from phonenumbers import PhoneNumberMatcher

from detectors.base import Candidate

PHONE_CONTEXT = re.compile(
    r"(?:phone|mobile|cell|call|tel(?:ephone)?|contact|whatsapp)\s*"
    r"(?:number|no\.?|:|-)?\s*$|^\s*(?:phone|mobile|cell|number|is)\b",
    re.I,
)


def _has_phone_context(text: str, start: int, end: int) -> bool:
    before = text[max(0, start - 36):start]
    after = text[end:min(len(text), end + 24)]
    return bool(PHONE_CONTEXT.search(before) or PHONE_CONTEXT.search(after))


def detect(text: str, default_region: str | None = None) -> list[Candidate]:
    """Find valid phone numbers without guessing a region for national formats.

    International `+` numbers work with no region. National-format numbers are
    considered only when a valid default region is configured. A national
    number must also have phone context or visible phone-style separators so a
    bare sequence of digits is not treated as a phone by default.
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
        formatted = bool(re.search(r"[\s()-]", raw))
        if not explicit_international and not (formatted or _has_phone_context(text, match.start, match.end)):
            continue

        national_digits = phonenumbers.national_significant_number(number)
        region_code = phonenumbers.region_code_for_number(number)
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
                    "reachability or ownership. National-format interpretation used the configured region."
                    if not explicit_international
                    else "Number is valid according to libphonenumber metadata; this does not verify assignment, reachability or ownership."
                ),
                country_code=number.country_code,
                country_region=region_code,
                phone_national_digits=national_digits,
            )
        )

    return found
