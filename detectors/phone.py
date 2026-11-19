import re

from detectors.base import Candidate

# Prefer an explicit international prefix or a nearby phone/contact label.
PATTERN = re.compile(r"(?<!\w)(?:\+\d{1,3}[ .()-]*)?(?:\(?\d{2,5}\)?[ .-]*)?\d(?:[ .()-]*\d){7,12}(?!\w)")
CONTEXT = re.compile(r"(?:phone|mobile|mob|call|tel(?:ephone)?|contact)\s*(?:number|no\.?|:|-)?\s*$", re.I)


def detect(text: str) -> list[Candidate]:
    out = []
    for m in PATTERN.finditer(text):
        raw = m.group()
        digits = sum(ch.isdigit() for ch in raw)
        prefix = text[max(0, m.start() - 24):m.start()]
        explicit_country = raw.lstrip().startswith("+")
        if not 8 <= digits <= 15 or not (explicit_country or CONTEXT.search(prefix)):
            continue
        out.append(Candidate("phone", m.start(), m.end(), raw, "phone_candidate_regex_v1", "medium", "Phone-shaped sequence with country-code or contact context; numbering validity and ownership are not verified."))
    return out
