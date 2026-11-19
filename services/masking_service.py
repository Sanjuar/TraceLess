from detectors.base import Candidate


def mask_value(candidate: Candidate) -> str:
    value = candidate.value
    if candidate.kind == "email" and "@" in value:
        local, domain = value.rsplit("@", 1)
        if len(local) <= 2:
            masked_local = local[:1] + "*" * max(1, len(local) - 1)
        else:
            masked_local = local[0] + "*" * (len(local) - 2) + local[-1]
        return f"{masked_local}@{domain}"
    if candidate.kind == "phone":
        digits = sum(c.isdigit() for c in value)
        return "*" * max(0, digits - 2) + value[-2:]
    if candidate.kind == "pan_like":
        return value[:2] + "*" * max(0, len(value) - 3) + value[-1:]
    if candidate.kind == "age":
        digits = "".join(c for c in value if c.isdigit())
        return "*" * max(1, len(digits) - 1) + digits[-1:]
    if candidate.kind == "name":
        return (value[:1] or "") + "*" * max(2, len(value) - 1)
    return "*" * max(1, len(value) - 2) + value[-2:]


def sanitized_evidence(text: str, target: Candidate, all_candidates: list[Candidate], context: int = 32) -> str:
    start = max(0, target.start - context)
    end = min(len(text), target.end + context)
    snippet = text[start:end]
    replacements = [c for c in all_candidates if c.start < end and c.end > start]
    for candidate in sorted(replacements, key=lambda c: c.start, reverse=True):
        left, right = max(candidate.start, start) - start, min(candidate.end, end) - start
        masked = mask_value(candidate)
        snippet = snippet[:left] + masked + snippet[right:]
    return snippet
