---
id: concept_london_move_storage
type: concept
---

# London Move accounting and storage spike

Current agreed direction: Move owns accounting and payouts, S3 stores audio, one streaming-node role. Table baseline and BigOrderedMap alternative remain research recommendations. Earlier RocksDB and commitment-only detailed specification requires coordinated revision. Local tests are not scale evidence.

## Connected knowledge

- informs: [[London USDC settlement (APPROVED)|London USDC settlement (APPROVED)]] (INFERRED)

## Source content

Source: docs/research/london-move-storage/README.md
## Decision and scope

The product owner agreed to a smaller London architecture: S3 audio, one streaming-node role, a small coordinator and Move-owned accounting/payout state. Artist ownership is an operator attribute, not a node type. This direction supersedes the preceding RocksDB-first implementation priority and hash-only contract choice. The existing London chapters still need a coordinated specification revision; do not implement their RocksDB ledger or commitment-only settlement design as the new target. This spike investigates storage, not that full rewrite.

Recommend starting with `aptos_std::table::Table` for independent accounting records and balances. Benchmark `aptos_framework::big_ordered_map::BigOrderedMap` as the alternative for densely packed records and ordered traversal. Do not introduce both into production until the workload needs both. No custom RocksDB financial authority is needed alongside Move. Backend queues, sessions and rebuildable reporting remain off-chain.

Source: docs/research/london-move-storage/README.md
## What the collections actually offer

| Collection | Verified shape | London fit |
|---|---|---|
| Table | Individual keys stored in separate state items; native keyed access; no enumeration or built-in length | Simplest baseline for independent account, budget and obligation keys; potentially expensive slot-per-entry storage |
| BigOrderedMap | B+ tree spanning storage slots, packed leaf entries, ordered traversal; configurable entry sizes | Candidate for compact accounting records and bounded ordered pages; splits and shared leaves can cause conflicts |
| SmartTable | Linear hashing; current upstream source deprecates it in favour of BigOrderedMap | Do not select for new London code |
| Vector / single-resource map | Contents live together and encounter resource size and read/write costs | Small bounded rights splits/configuration only, not a lifetime stream history |

A set can be represented by a map from an ID to a marker. Accounting normally needs a map from an ID to a record, including amount, state and version. A HashSet by itself does not implement conservation, authorisation, replay prevention or payout correctness. These are contract rules.

Neither map makes one transaction unbounded. BigOrderedMap also has key/value sizing constraints and constructor differences for fixed versus variable-size types. Fixed-size IDs and compact numeric records are a useful starting point. Do not copy `new()` blindly for a variable-size receipt value.

Source: docs/research/london-move-storage/README.md
## Bounded accounting design

Keep current funded budgets, accepted aggregate usage needed for allocation, rights versions, unpaid obligations and replay guards in Move resources. Emit immutable usage-acceptance, allocation and payment events from successful transitions. The contract computes or independently validates allocations from authorised usage and funded amounts; it must not blindly accept a server-provided payout amount.

Use natural partitions such as funding period and opaque accounting bucket. For the user-centric model, preserve the listener-budget boundary without publishing identities or detailed listening timelines. Even opaque identifiers can expose linkable listening patterns. Exact public aggregate granularity and privacy are unresolved design gates, not solved by hashing an email.

Use bounded input batches and bounded settlement pages. A whole day's usage, every beneficiary or the whole map must never be processed in one transaction. For proportional allocation, freeze the denominator and applicable rules before processing pages. Persist a cursor and totals, handle integer remainder deterministically, and reject premature finalisation. Do not independently round each page and accidentally change allocations. A bounded per-budget calculation may be simpler for the pilot; do not quietly change user-centric economics to a global pool.

Separate usage accumulation from payout execution. Independent usage keys do not help if every update also mutates a global total, a global next-ID counter, one day's common record, or the same vault. Common recipients and concurrent withdrawals can also contend. Avoid global mutable counters in the hot path; measure actual storage write sets, including framework resource effects. Shard further only after a benchmark identifies the conflict.

For retries, accept the same stable batch ID and payload digest only once; reject conflicting reuse. Contract-level identity alone does not prevent replaying the same underlying usage under a fresh batch ID. The admission protocol also needs non-overlapping sequence ranges or equivalent provenance checks per reporting lane. In the pilot Porto remains the trusted usage admission authority. Closing a period must permanently reject new submissions to that period before any replay metadata can be retired. Do not delete processed IDs and thereby reopen old payment claims.

Retain unpaid obligations until settled. Pay by an atomic contract transition that checks the obligation and updates payout state with the supported USDC transfer in the same transaction. Asset integration is not exercised by this collection spike. Paid history can be represented by immutable events plus sufficient closed-period/settlement state to reject replay. Do not delete authoritative records while contracts still require them.

Source: docs/research/london-move-storage/README.md
## Executed spike and proof boundary

Result: **PASS, four local Move unit tests**, including exact expected abort codes and module locations for duplicate insertion.

Local unit tests exercise 10000 u64-key/u64-value inserts, reads, updates and removals in each collection, plus duplicate insertion failure. The instruction budget is intentionally raised to 1000000000 for a collection stress check. This is not a realistic single Mainnet transaction, not a concurrency test, and not an end-to-end accounting test. No funds were spent and no contract was deployed.

The test package pins AptosFramework commit `04611dd2cec1f5b7ef21c2cc151e05c587a2ce19`, which matched the framework repository's mainnet branch at observation time. Deployed ABI presence was checked separately; source and ABI checks do not establish byte-for-byte equivalence of deployed code. Upstream comparison also inspected aptos-core commit `b762d569670f9b9ef1a0bcb778c3f3edb944b5ef`.

The installed Aptos CLI 7.10.2 could not parse the current dependency. An isolated official Aptos CLI 9.6.0 binary was used without replacing the installed executable. The local test run used the clean cached framework checkout at the pinned commit; the supplied manifest identifies that same revision portably.

Reproduce with Aptos CLI 9.6.0:

```sh
aptos move test --package-dir research/london-move-storage --instructions 1000000000
```

Run from the docs repository. This package is disposable research, not an application module.

Source: docs/london-0.1.0/index.mdx
## Approved direction: Move accounting, one streaming-node role

The product owner has approved simplifying London to a player, small coordinator, private S3 audio origin, streaming nodes and Move-owned accounting/payout state. Any eligible artist or other participant can operate the same streaming-node software. A real node-to-node cache transfer remains part of the pilot.

The authoritative accounting and payout contract is [Move-owned accounting and payout protocol](09-move-contract-specification.md). It supersedes the preceding RocksDB-first priority and hash-only commitment contract. Where an older chapter conflicts with this protocol, the Move protocol prevails. Do not build the old local financial ledger or commitment-only settlement path.

Start with the [Move storage spike](https://github.com/porto-labs-xyz/docs/blob/main/research/london-move-storage/README.md): Table and BigOrderedMap candidates, bounded accounting, Mainnet limits, local collection tests and explicit remaining benchmark gates. Collection selection is a research recommendation, not a production-scale result. The next specification revision must align accounting, privacy, USDC transfers, APIs and acceptance tests before implementation.

London still excludes PRT, a custom chain and an independent attestor network. Approval of the direction is not deployment, security clearance or observed real payouts.
