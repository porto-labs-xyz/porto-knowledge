---
id: doc_pips_pip_5_md
type: document
---

# PIP-5: Listener-Centric Payouts

Simple Summary The payoutsplitter module converts finalized StreamEvents into actual PRT payouts, using a user-centric (listener-attributed) settlement model rather than a platform-wide pro-rata pool, and applies the 70/25/5 network-level split within each listener's own subscription allotment. Abstract This PIP specifies how value moves from a listener's subscription mint to rights holders, node operators, and the.

## Connected knowledge

- describes: [[Epoch settlement|Epoch settlement]] (EXTRACTED)
- describes: [[Multi-party rights-holder splits|Multi-party rights-holder splits]] (EXTRACTED)

## Source content

```
PIP: 5
Title: Payout Splitter Module
Author: Richard Melkonian
Status: Draft
Type: Standards Track (Core)
Created: 2026-09-09
Requires: PIP-1, PIP-3, PIP-4
```

## Simple Summary

The `payout_splitter` module converts finalized `StreamEvent`s into actual PRT payouts, using a **user-centric** (listener-attributed) settlement model rather than a platform-wide pro-rata pool, and applies the 70/25/5 network-level split within each listener's own subscription allotment.

## Abstract

This PIP specifies how value moves from a listener's subscription mint to rights holders, node operators, and the protocol treasury once a `StreamEvent` has been finalized by [PIP-4](./PIP-4.md). It defines the per-listener accrual model, the epoch settlement function, the application of multi-party splits within the rights-holder share, and the interaction with the redemption mechanism specified in [PIP-3](./PIP-3.md).

## Motivation

A naive design would pool all subscription revenue platform-wide and distribute it pro-rata to all works by total stream count across all listeners. This has a well-documented fairness problem in the streaming industry (sometimes called the "pro-rata" model): a listener who exclusively streams independent or niche artists ends up subsidizing plays of the platform's most-streamed works, because their subscription dollars are pooled and redistributed by aggregate popularity rather than by what they personally listened to. Porto instead adopts a **user-centric** model — attributing each listener's subscription value specifically to the works that listener actually streamed, weighted by their own listening time. This is more defensible to artists and auditors (a specific listener's money provably went to the specific work they played) and is directly implementable given Porto's per-listener `StreamEvent` records.

## Specification

### 1. Listener accrual

Each listener's monthly subscription mint (see [PIP-3](./PIP-3.md) §2) is credited to a per-listener accrual balance, not immediately distributed:

```move
module porto::payout_splitter {

    struct ListenerAccrual has key {
        balance: u64,                          // microPRT allotted this epoch, undistributed
        epoch_start_ms: u64,
        work_durations: SimpleMap<vector<u8>, u64>,  // work_id -> cumulative duration_ms this epoch
        total_duration_ms: u64,
    }

    /// Called by stream_accounting::finalize_batch (PIP-4 §4) for every
    /// finalized StreamEvent. Accumulates listening time; does not move
    /// value yet — settlement happens at epoch boundary (§2).
    public(friend) fun on_stream_finalized(event: StreamEvent) acquires ListenerAccrual {
        // work_durations[event.work_id] += event.duration_ms
        // total_duration_ms += event.duration_ms
    }
}
```

Accumulating listening time separately from settling value allows a listener's subscription allotment to be divided proportionally across everything they streamed in the epoch, rather than requiring a payout decision at the moment of each individual play (which would either overpay short/early plays in a session or require knowing the full epoch's listening pattern in advance).

### 2. Epoch settlement

At each epoch boundary (Beta default: **daily**, i.e. `EPOCH_LENGTH_MS = 86_400_000`), or lazily on next access if a listener was inactive, `settle_epoch` distributes that listener's accrued balance across the works they streamed, weighted by listening-time share:

```move
public entry fun settle_epoch(listener: address) acquires ListenerAccrual, MusicalWork {
    let accrual = borrow_global_mut<ListenerAccrual>(listener);
    let n = simple_map::length(&accrual.work_durations);
    let i = 0;
    while (i < n) {
        let (work_id, duration_ms) = /* iterate work_durations */;
        let weight = duration_ms * PRECISION / accrual.total_duration_ms;
        let work_allocation = accrual.balance * weight / PRECISION;
        distribute_for_work(work_id, work_allocation);
        i = i + 1;
    };
    // any rounding dust remaining after integer-division allocation is
    // routed to the protocol treasury (see Security Considerations)
    accrual.balance = 0;
    accrual.work_durations = simple_map::new();
    accrual.total_duration_ms = 0;
}

fun distribute_for_work(work_id: vector<u8>, amount: u64) acquires MusicalWork {
    let work = borrow_global<MusicalWork>(work_address(work_id));
    let rights_holder_pool = amount * 7_000 / 10_000;   // 70%
    let operator_pool      = amount * 2_500 / 10_000;   // 25%
    let treasury_pool      = amount - rights_holder_pool - operator_pool; // remainder = 5% + dust

    // rights_holder_pool distributed pro-rata across work.rights_holders by bps
    // operator_pool credited to the attestor(s) who served this work's plays
    //   this epoch, weighted by their share of served duration for this work
    //   (Beta: 100% to the sole Trusted Attestor; V1: split across the
    //   quorum members who attested, per PIP-6)
    // treasury_pool credited to the protocol treasury account
}
```

### 3. Multi-party rights-holder splits

Within `rights_holder_pool`, value is further divided according to the `MusicalWork.rights_holders` vector registered in [PIP-4](./PIP-4.md) §7 (e.g., a work co-written by two songwriters and released on a label might declare a 40/40/20 split). This layer is independent of, and sits entirely inside, the network-level 70% share — Porto's protocol never sees or needs to know the semantic reason for a given split (co-writing agreement, label deal terms, etc.), only the on-chain basis-point allocation.

### 4. Interaction with redemption

Each individual credit within `distribute_for_work` (to a rights holder or an operator) immediately invokes `prt::apply_redemption_preference` ([PIP-3](./PIP-3.md) §4) for that recipient, so the stable/volatile split the recipient has configured is applied atomically at the moment of payout, within the same settlement transaction, rather than as a separate downstream step a recipient must remember to trigger.

### 5. Settlement cost bounding

`settle_epoch`'s gas cost scales with the number of distinct works a listener streamed in an epoch. To bound worst-case transaction cost, a `MAX_WORKS_PER_EPOCH` parameter (Beta default: 200) caps the number of distinct works settled in a single `settle_epoch` call; a listener who streamed more distinct works than the cap in one epoch has their settlement processed across multiple transactions (chunked by the client/gateway calling `settle_epoch` iteratively), rather than the module attempting an unbounded loop in one transaction.

## Rationale

**Why user-centric rather than pro-rata pooling?** As described in Motivation, pro-rata pooling systematically transfers value from listeners of niche/independent work to the platform's most popular works, which directly undermines Porto's stated purpose of helping independent artists and labels capture more of the value their own listeners generate. User-centric settlement is also strictly more auditable: a specific listener's specific subscription payment can be traced, epoch by epoch, to the specific works it funded — a materially stronger transparency claim than "your payment went into a pool."

**Why settle at epoch boundaries rather than per-stream?** Per-stream settlement would require knowing, at the moment of an individual play, what fraction of that listener's *entire remaining monthly allotment* this one play should consume — which depends on plays that haven't happened yet within the same period. Batching accrual and settling at a fixed epoch boundary is the natural resolution: it allows proportional, retrospective allocation across everything actually streamed in the period, at the cost of introducing epoch-length latency (bounded, and disclosed, rather than the multi-month latency of the incumbent system it replaces).

**Why daily epochs for Beta?** A daily cadence is short enough to preserve Porto's "not months-later" value proposition relative to the 90–180 day incumbent settlement chain ([PIP-2](./PIP-2.md)), while being long enough to amortize settlement transaction cost across a meaningful number of plays per listener. The epoch length is a governance parameter ([PIP-7](./PIP-7.md)) and may be shortened as gas costs and infrastructure allow.

## Backwards Compatibility

Not applicable — greenfield module. Any future change to the settlement algorithm (e.g., moving from daily to more frequent epochs, or introducing a different weighting function) should be proposed as a new Standards Track PIP referencing this one, since it changes payout amounts for existing participants and therefore warrants the same review rigor as this specification.

## Security Considerations

- **Rounding/dust handling.** Integer division in `distribute_for_work` and the weighting calculation in `settle_epoch` can leave small remainders. All such dust is deterministically routed to the protocol treasury rather than being left unaccounted for or silently dropped, keeping `circulating_supply()` fully reconciled.
- **Replay protection.** `settle_epoch` zeroes `ListenerAccrual` state after distribution; a well-formed settlement transaction cannot be replayed against the same epoch's already-distributed balance.
- **Gas-bounded settlement (griefing via excessive distinct works).** Without `MAX_WORKS_PER_EPOCH` (§5), a listener (or an attacker inflating a target listener's play diversity) could construct a settlement call expensive enough to fail or to be economically irrational to execute, stalling that listener's payouts. The cap, with multi-transaction chunking, bounds this.
- **Dependency on stream_accounting finalization correctness.** `payout_splitter` trusts that any `StreamEvent` reaching `on_stream_finalized` has already passed the validity and (in V1) quorum checks specified in [PIP-4](./PIP-4.md). This module performs no independent verification of play authenticity — that trust boundary is intentional and documented, so that attestation-layer security upgrades (e.g., the Beta→V1 migration) do not require changes here.

## Copyright

Copyright © 2026 Entropy Tech Ltd.

This document is licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
Porto names, logos, and other trademarks are not licensed under this license.
