# Detector catalog

| Type | Rule | Confidence | Limit |
| --- | --- | --- | --- |
| email | Practical email-shaped regex | high | No mailbox verification |
| phone | Digit candidate plus international prefix or contact context | medium | No numbering-plan or ownership verification |
| pan_like | Indian PAN format | high | Format only; no government validation |
| age | Age/aged/years-old context, range 0-120 | medium | Unverified text claim |
| name | Name/sign-off context | low | Ambiguous candidate, not identity proof |
| certificate_id | Certificate context plus identifier token | low | Issuer formats vary |
| bank_account_like | Account context plus 9-18 digits | low | No existence or ownership validation |

Patterns are intentionally conservative. Overlaps are resolved by detector priority and source position. See `tests/` for synthetic positive, negative, boundary, and false-positive examples.
