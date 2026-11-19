# Phase 0/1 privacy and security

Text is processed in memory and discarded after the response. No request body is logged, persisted, or sent to a third party. Responses always mask detected values and sanitize snippets where known findings overlap. This is not a guarantee that arbitrary sensitive text is fully recognized: avoid submitting content you do not have authorization to review.

The text limit defaults to 50,000 characters and can be set using `TRACELESS_MAX_TEXT_CHARACTERS`. Phase 0/1 does not implement authentication, persistence, uploads, external URL fetches, rate limiting, or breach checks. Do not expose this prototype as a multi-user service without those controls.
