# Detector catalog

| Type | Rule | Confidence | Limit |
| --- | --- | --- | --- |
| email | Practical email-shaped regex | high | No mailbox verification |
| phone | Google libphonenumber parsing plus `is_valid_number()`; explicit international calling code required | high | No assignment, reachability or ownership verification; national-format numbers are not guessed |
| pan_like | Indian PAN format | high | Format only; no government validation |
| aadhaar_like | Twelve digits, optionally grouped in fours with spaces | medium | Format only; no UIDAI or government validation |
| age | Age/aged/years-old context, range 0-120 | medium | Unverified text claim |
| name | Name/sign-off context | low | Ambiguous candidate, not identity proof |
| certificate_id | Certificate context plus identifier token | low | Issuer formats vary |
| bank_account_like | Account context plus 9-18 digits | low | No existence or ownership validation |

Phone offsets and evidence spans refer to the original input; phone masking retains only the final two national-number digits. International phone numbers are parsed without a region. The scan API does not interpret national-format numbers without a calling code. The detector's optional `default_region` argument exists only for direct callers that explicitly choose to parse national-format numbers. `country_code` is the calling code and `country_region` is the ISO region code when libphonenumber can determine it.

Patterns are intentionally conservative. Overlaps are resolved by detector priority and source position; contextual certificate/account matches take precedence over an unlabelled Aadhaar-like shape. See `tests/` for synthetic positive, negative, boundary, and false-positive examples.
