import re

from detectors.base import Candidate

PATTERN = re.compile(r"(?<![\w.!#$%&'*+/=?^`{|}~-])[A-Z0-9.!#$%&'*+/=?^`{|}~-]+@[A-Z0-9](?:[A-Z0-9-]*[A-Z0-9])?(?:\.[A-Z0-9](?:[A-Z0-9-]*[A-Z0-9])?)+(?![\w-])", re.I)


def detect(text: str) -> list[Candidate]:
    return [Candidate("email", m.start(), m.end(), m.group(), "email_regex_v1", "high", "Email-shaped text matched; mailbox ownership and deliverability are not verified.") for m in PATTERN.finditer(text)]
