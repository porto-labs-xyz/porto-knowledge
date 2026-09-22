---
id: concept_london_evidence
type: concept
---

# London delivery evidence (DRAFT)

PROPOSED FOR LONDON 0.1.0. Draft specification, not accepted policy, deployment or runtime evidence.

## Connected knowledge

- informs: [[London USDC settlement (DRAFT)|London USDC settlement (DRAFT)]] (INFERRED)

## Source content

Source: docs/london-0.1.0/06-streaming-delivery-and-attestation.md
## Duration and eligibility

The server records actual response bytes written, status, request interval and verified chunk digest. A successful socket write proves only server-observed delivery, not remote decoding or attention. A node's signed statement is an assertion Porto must validate. Do not describe it as independent proof.

Normalize evidence to completed manifest chunks; deduplicate the union of media intervals per `(listener_internal_id, work_id, session_id)` across ranges, retries and operators. A payable chunk must be completely evidenced by one operator, possibly across that operator's contiguous retries. Do not combine partial delivery by different operators into a payable chunk. Attribute each chunk to the first operator completing it, ordered by the gateway request sequence that completed coverage; duplicates earn zero. A fallback can re-serve the complete chunk if no operator completed it. Reject impossible clock intervals and unauthorised chunks. Cap total credited duration by elapsed authorised lease time plus prebuffer, work duration and approved daily account/work limits. Overlapping sessions cannot increase the account's elapsed-time ceiling.

A session is eligible when approved unique duration reaches `min(30000, floor(work_duration_ms / 2))`, with positive registered duration. If it qualifies, credit its approved unique duration, including the initial threshold interval; if it does not, credit zero. Client playheads/heartbeats affect UX only. Repeated media within a session earns zero additional duration. A new session can qualify again only within the policy's account/work daily cap.

A session crossing midnight is evaluated once at closure; qualifying duration is partitioned by server delivery time across UTC service days and rights versions. No daily slice is published until the session closes or expires. A six-hour session can therefore delay its prior-day inputs, covered by the close watermark below.

Source: docs/london-0.1.0/06-streaming-delivery-and-attestation.md
## Evidence custody

Encrypted raw receipts and signed manifests are immutable with content hashes and retention locks compatible with the approved retention policy. Proposed retention: raw IP/operational access logs 30 days, pseudonymised evidence 180 days, financial/audit records 7 years, subject to D08 professional review before production. Separate identity mappings and destroy them at approved expiry unless under documented legal hold. Never put raw evidence or unsalted listener hashes on-chain. Authorised dispute export includes relevant receipts, grant lineage, hash manifest, policy and allocation versions, with listener identifiers redacted. Access is logged and expires after 15 minutes. A retention lock must not be enabled before legal/privacy review of duration and erasure handling.

See [glossary](glossary.md) for exact state meanings. `CURRENT SOURCE`: PIP-4 §§2,3,5 supplies threshold, server-evidence intent and batching context; London changes the byte accounting, schema and trust boundary.

[London 0.1.0 contents](index.mdx) · [Decision register](17-open-decisions-and-risk-register.md)
