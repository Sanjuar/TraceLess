from detectors import age, bank_account, certificate, email, name, pan, phone
from detectors.base import Candidate


def detect_all(text: str, *, detect_names: bool = True, detect_age: bool = True) -> list[Candidate]:
    """Run deterministic detectors and resolve overlaps in a stable priority order."""
    groups = [email.detect(text), phone.detect(text), pan.detect(text)]
    if detect_age:
        groups.append(age.detect(text))
    if detect_names:
        groups.append(name.detect(text))
    groups.extend((certificate.detect(text), bank_account.detect(text)))
    priority = {"email": 0, "phone": 1, "pan_like": 2, "age": 3, "name": 4, "certificate_id": 5, "bank_account_like": 6}
    ordered = sorted((c for group in groups for c in group), key=lambda c: (c.start, priority[c.kind], -(c.end - c.start), c.detector))
    selected: list[Candidate] = []
    for candidate in ordered:
        if any(candidate.start < prior.end and prior.start < candidate.end for prior in selected):
            continue
        selected.append(candidate)
    return sorted(selected, key=lambda c: (c.start, c.end, priority[c.kind], c.detector))
