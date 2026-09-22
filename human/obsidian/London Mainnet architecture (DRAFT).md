---
id: concept_london_architecture
type: concept
---

# London Mainnet architecture (DRAFT)

PROPOSED FOR LONDON 0.1.0. Draft specification, not accepted policy, deployment or runtime evidence.

## Connected knowledge

- uses: [[London delivery evidence (DRAFT)|London delivery evidence (DRAFT)]] (INFERRED)
- requires_review: [[London governance departures (DRAFT)|London governance departures (DRAFT)]] (INFERRED)

## Source content

Source: docs/london-0.1.0/01-executive-architecture.md
## Proposed architecture

Porto owns the music experience, catalogue, private origin, delivery admission, fraud decisions and settlement application. Aptos supplies consensus, ordering, finality and Move execution. Permissioned delivery/cache operators provide a measurable service; they are not Porto validators. Porto's attestation service is the initially trusted authority that accepts signed delivery evidence and commits approved batches.

The proposed public description is:

> Porto operates a music delivery and settlement network. Initial real-money settlement uses proven Mainnet infrastructure while Porto builds toward its own app-chain.

This wording describes the intended model, not evidence of launch. Do not describe it as decentralised consensus, permissionless serving, trustless playback verification or a completed app-chain.

Source: docs/london-0.1.0/01-executive-architecture.md
## Responsibilities and money

A listener pays GBP for access. Cleared revenue becomes Porto company revenue, subject to accounting adjustments, reserves and professional review. A selected provider converts treasury funds to native Aptos USDC. Porto allocates a funded portion to listener periods in its internal ledger. Accepted delivery determines rights-holder and operator accruals. Reviewed daily batches reserve funds on-chain; bounded transfers pay registered recipients. Dashboards distinguish pending evidence, accrual, settlement commitment and confirmed transfer.

Only salted commitments, opaque application identifiers, settlement amounts, states and payout addresses go on-chain. Detailed playback, listener identity, IP, device and provider data stay off-chain. Public addresses and amounts still permit correlation; privacy review is mandatory.
