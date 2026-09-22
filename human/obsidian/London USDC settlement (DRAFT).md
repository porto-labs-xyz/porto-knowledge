---
id: concept_london_settlement
type: concept
---

# London USDC settlement (DRAFT)

PROPOSED FOR LONDON 0.1.0. Draft specification, not accepted policy, deployment or runtime evidence.

## Connected knowledge

No outgoing links.

## Source content

Source: docs/london-0.1.0/08-usdc-treasury-and-settlement.md
## Money states and ownership

```text
payment_authorised -> payment_cleared -> net_revenue_available
-> conversion_instructed -> treasury_usdc_confirmed -> listener_period_allocated
-> rights_and_operator_accrued -> onchain_settled -> payout_confirmed
```

Each arrow requires an append-only ledger event, evidence reference, unique business ID and authorised actor. Exceptions branch from every state to `held`, `failed`, `refund_pending`, `reversal_recorded` or `recovery_open`; they never erase history. Payment authorisation is not clearance. Clearance does not eliminate chargeback risk. A conversion quote or broadcast transaction is not a confirmed USDC balance.

Porto owns the treasury funds before settlement. Listener allocations are internal attribution budgets, not customer assets, wallets or redeemable crypto balances. Revenue recognition and liability treatment are D01/D04 professional decisions. This document does not decide their legal or accounting character.

Source: docs/london-0.1.0/08-usdc-treasury-and-settlement.md
## Funded allocation algorithm

D05 must ratify the following proposed method or replace it before production. Let a listener subscription service interval be `[start_ms,end_ms)`. Once its attributable conversion lots are confirmed, assign an immutable integer budget `B` micro-USDC. Allocate B over overlapping UTC days in proportion to service milliseconds, using largest remainder, ties by ascending UTC day. The sum of daily budgets is exactly B. This avoids spending the monthly budget each day. Days before clearance accumulate evidence but cannot settle until funded. A conversion spanning subscriptions uses the same largest-remainder method weighted by approved net GBP, with ties by subscription ID.

After D's evidence watermark, freeze the whole listener-day if any relevant dispute is unresolved. For an unheld day, let `d_w` be accepted unique served duration by work and rights version and `T=sum(d_w)`. If T is zero, leave the day's budget unallocated in a separately tracked reserve; do not silently route it to treasury. D05 must approve eventual unused-budget disposition. Otherwise distribute the day budget in proportion to `d_w` using largest remainder and ties by `(work_id,rights_version)` ascending bytes.

Split each work allocation by ratified rights/operator/treasury basis points summing to 10000, again by largest remainder with tie order rights, operator, treasury. Within rights pool use snapshotted recipient basis points, ties by opaque recipient ID. Within operator pool use accepted unique duration attributed to each serving operator, ties by operator ID. Porto origin fallback uses a separately disclosed operator ID and reward recipient if D06 approves; otherwise hold its operator share pending policy, never redistribute it silently. Rights holders who also operate nodes get two distinct accounting lines.

Aggregate payout lines only after preserving per-listener attribution in the private ledger. Build stable payout IDs and a manifest whose total equals the sum of included unspent budgets. Do not perform monetary arithmetic in floats. Use checked u128 intermediates and checked u64 outputs. Negative adjustments are separate off-chain liabilities.

Synthetic test vector, not approved economics: B=101, two equal days produce 51 and 50. On day one, work durations 1:2 produce 17 and 34. With a test-only 6000/3000/1000 split, 17 produces 10/5/2. All sums conserve exactly. Never use this fixture as production configuration. Existing 70/25/5 is also not pre-approved for London.
