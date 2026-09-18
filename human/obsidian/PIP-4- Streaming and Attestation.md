---
id: doc_pips_pip_4_md
type: document
---

# PIP-4: Streaming and Attestation

Simple Summary Every play of a musical work on Porto is served from an audio origin, confirmed by an attestor as actually having been served for a minimum duration, and recorded on-chain as a StreamEvent that becomes the sole trigger for payout. This PIP specifies the on-chain streamaccounting module and, in detail, the Beta-phase streaming architecture: trusted-region, co-located S3 origin storage with a single.

## Connected knowledge

- describes: [[Valid billable play|Valid billable play]] (EXTRACTED)
- describes: [[Playback attestation|Playback attestation]] (EXTRACTED)
- describes: [[Beta-to-Mainnet rollout|Beta-to-Mainnet rollout]] (EXTRACTED)

## Source content

```
PIP: 4
Title: Stream Accounting & Attestation Protocol
Author: Richard Melkonian
Status: Draft
Type: Standards Track (Core)
Created: 2026-09-09
Requires: PIP-1, PIP-3
```

## Simple Summary

Every play of a musical work on Porto is served from an audio origin, confirmed by an attestor as actually having been served for a minimum duration, and recorded on-chain as a `StreamEvent` that becomes the sole trigger for payout. This PIP specifies the on-chain `stream_accounting` module and, in detail, the Beta-phase streaming architecture: trusted-region, co-located S3 origin storage with a single Trusted Attestor, and its migration path to a staked, permissionless, multi-attestor model.

## Abstract

Porto's core claim to artists is that royalties are transparent and auditable because every stream is logged on-chain. That claim is only as strong as the process that turns "a listener pressed play" into an on-chain fact. This PIP specifies that process end to end: how audio is stored and served, what constitutes a valid, billable play, how that play is attested and batched into a transaction, the on-chain schema that records it, and how the trust model of the attestation process evolves from a single centralized attestor (Beta) to a staked, multi-party quorum (Mainnet V1), without changing the on-chain interface that downstream modules ([PIP-5](./PIP-5.md)) depend on.

## Motivation

The problem this PIP solves is stated in [PIP-2](./PIP-2.md): artists cannot currently see how a royalty was calculated, which streams counted, or why the number is what it is. Solving that requires a stream-logging mechanism that is (a) resistant to trivial gaming (skip-spam, bot plays), (b) auditable by any party inspecting chain state, and (c) able to launch in a Beta timeframe without requiring a fully decentralized, staked CDN network to exist first — decentralizing physical content serving is a substantial systems engineering effort in its own right, and gating the entire payout/accounting proof-of-concept on it would conflate two independent problems. This PIP explicitly separates them: centralize serving in Beta, decentralize it later, but make the on-chain accounting interface identical across both phases.

## Specification

### 1. Beta streaming architecture — trusted-region, co-located S3 origin

**Origin storage.** Each registered musical work's audio master is stored as an object in an AWS S3 bucket. Buckets are provisioned per **Trusted Region** — an AWS region selected for physical proximity to Porto's target listener base at each stage of rollout. For the initial Beta (UK go-to-market), the Trusted Region is `eu-west-2` (London). "Trusted" denotes that, during Beta, these buckets and the compute that serves from them are operated directly by Porto Labs under a single, Porto-controlled AWS account — there is no permissionless node operator set yet. This is the explicit, disclosed centralization referenced in [PIP-2](./PIP-2.md) §Rationale.

**Co-location.** The Streaming Gateway (the compute layer that authenticates playback requests and issues access to origin content) is deployed in the same AWS region, and where possible the same Availability Zone, as the S3 bucket it serves from. This eliminates cross-region egress and minimizes time-to-first-byte and rebuffer risk, which matters both for listener experience and because the Streaming Gateway is the component generating server-side duration measurements that anchor payout (§3).

**Access control.** The Streaming Gateway does not expose bucket objects publicly. On a play request, it issues a short-lived, byte-range-scoped, S3 pre-signed `GET` URL:

```
GET https://porto-origin-euw2.s3.eu-west-2.amazonaws.com/{work_id}.flac
    ?X-Amz-Expires=60
    &X-Amz-SignedHeaders=range
    &X-Amz-Signature=...
Range: bytes=0-524287
```

- TTL is capped at 60 seconds, scoped narrowly enough to support adaptive/seek playback via successive range requests without exposing a URL usable to download the full asset well after the listening session.
- Each pre-signed URL is single-purpose (bound to a specific `listener_id` + `work_id` + session token combination validated at issuance time), so a leaked URL has a narrow, time-boxed blast radius.

### 2. Play validity threshold

A play only becomes a billable, on-chain `StreamEvent` once the Streaming Gateway has server-confirmed at least:

```
min(30_000 ms, floor(0.5 * track_duration_ms))
```

of continuous or cumulative served audio for that `(listener_id, work_id)` pair within a single listening session. This mirrors the ~30-second industry threshold used by incumbent platforms, and exists specifically to prevent skip-spam or bot-driven inflation of play counts from translating directly into payout events.

**Server-side, not client-reported, duration.** The Streaming Gateway derives served duration from its own byte-range request logs — the volume of audio bytes actually served for a given `(listener_id, work_id, session)`, converted to a duration via the track's known bitrate — rather than trusting a client-submitted "I listened for N seconds" heartbeat as the sole source of truth. Client heartbeats (§3) are used for real-time UX (e.g., live dashboard ticking) but the value recorded on-chain is reconciled against server-side byte-range records at batch-submission time. This is materially harder to spoof than a client self-report, since it requires actually requesting and receiving the corresponding audio bytes from the origin.

### 3. Client heartbeat and session lifecycle

1. Client requests a playback session for `work_id`; gateway issues `session_token`, validates listener authentication, and opens a `PlaybackSession` record.
2. Client streams audio via successive range-scoped pre-signed URLs, refreshed as needed (each request re-validated against the session).
3. Client emits a heartbeat every 5 seconds during active playback, carrying `session_token` and playhead position, used for gateway-side liveness tracking and real-time dashboard display; **not** treated as authoritative for payout purposes.
4. On session end (track completion, skip, or timeout), the gateway finalizes `served_duration_ms` for that session from its own byte-range logs and checks the threshold in §2.
5. If the threshold is met, the gateway constructs a `StreamEvent` and enqueues it for batch submission (§5).

### 4. On-chain schema

```move
module porto::stream_accounting {

    struct StreamEvent has store, drop, copy {
        work_id: vector<u8>,     // canonical content hash of the registered musical work
        listener_id: address,     // pseudonymous on-chain listener identity
        attestor_id: address,     // node operator submitting the attestation (Beta: the sole Trusted Attestor account)
        duration_ms: u64,         // server-confirmed served duration for this session
        started_at_ms: u64,       // unix epoch millis, session start
        region: vector<u8>,       // origin AWS region code, e.g. b"eu-west-2"
        format: u8,               // enum: 0=FLAC, 1=AAC-256, 2=AAC-128, ... (codec/bitrate class served)
        session_id: vector<u8>,   // gateway-issued session identifier, for audit/dispute correlation
    }

    struct MusicalWork has key {
        work_id: vector<u8>,
        title: vector<u8>,
        isrc: Option<vector<u8>>,
        iswc: Option<vector<u8>>,
        rights_holders: vector<RightsHolderSplit>,   // must sum to 10_000 bps
    }

    struct RightsHolderSplit has store, copy, drop {
        account: address,
        bps: u64,
    }

    /// Submitted by an attestor (Beta: the Trusted Attestor account only;
    /// V1: any staked, registered attestor per PIP-6) as a single transaction
    /// carrying many events, amortizing gas cost across a batch window
    /// (Beta default: 60 seconds or 500 events, whichever first).
    public entry fun submit_batch(attestor: &signer, events: vector<StreamEvent>);

    /// Finalizes a batch after quorum/validity checks (see §6) and forwards
    /// each finalized event to payout_splitter::on_stream_finalized (PIP-5).
    fun finalize_batch(events: vector<StreamEvent>);
}
```

### 5. Attestation submission and batching

The Streaming Gateway does not submit one transaction per play. Instead it accumulates validated `StreamEvent`s and submits them as a single `submit_batch` transaction on a fixed cadence (Beta default: every 60 seconds, or immediately upon reaching 500 buffered events, whichever occurs first). This bounds both the gas cost per play and the on-chain transaction volume at Beta scale, while keeping payout latency low (sub-two-minute, versus the 90–180 day incumbent settlement chain described in [PIP-2](./PIP-2.md)).

### 6. Attestation trust model: Beta vs. Mainnet V1

**Beta.** `submit_batch` accepts submissions only from the single, designated Trusted Attestor account (the Streaming Gateway's signing key). There is no quorum check — a submitted, well-formed batch that passes the validity threshold (§2) is finalized directly. This is a single point of trust, and it is the primary item in [Security Considerations](#security-considerations).

**Mainnet V1 (forward-looking specification; full staking mechanics in [PIP-6](./PIP-6.md)).** Multiple independent, staked node operators serve the same content and independently submit `StreamEvent`s for the same `(listener_id, work_id, session_id)`. `finalize_batch` requires **m-of-n matching attestations** — events whose `duration_ms` values agree within a governance-set tolerance window — before forwarding to `payout_splitter`. Non-matching or insufficiently-attested events enter a bounded dispute window rather than finalizing; no payout is triggered for events that fail to reach quorum. This directly replaces the Beta single-attestor trust assumption with a Byzantine-fault-tolerant one, using the same `StreamEvent` schema and the same downstream `payout_splitter` interface — the migration changes only *who* may call `submit_batch` and *how* `finalize_batch` decides validity, not the shape of the data.

### 7. Musical work registration

Rights holders (or Porto, on their behalf during onboarding) register a `MusicalWork` prior to any stream being attestable against it. `work_id` is a content hash of the canonical audio master plus core metadata, functioning as a content-addressed identifier analogous to a CID, rather than an incrementing database ID — this ties the on-chain identity of a work directly to the specific audio file it represents, and makes tampering with the registered master detectable. `rights_holders` supports arbitrary multi-party splits (co-writers, labels, publishers) that apply *within* the 70% rights-holder share of the network-level split specified in [PIP-5](./PIP-5.md); entries must sum to `10_000` basis points.

### 8. Migration path

| | Beta | Mainnet V1 |
|---|---|---|
| Origin storage | Porto-operated S3, Trusted Region | Staked, permissionless CDN nodes ([PIP-6](./PIP-6.md)) |
| Attestor set | Single Trusted Attestor account | m-of-n staked, registered attestors |
| Finalization rule | Direct (no quorum check) | Quorum agreement within tolerance window |
| `StreamEvent` schema | As specified in §4 | Unchanged |
| `payout_splitter` interface | As specified in [PIP-5](./PIP-5.md) | Unchanged |

Because the on-chain schema and downstream interfaces are stable across this migration, no wallet, artist dashboard, or third-party integration built against the Beta chain needs to change when the attestation trust model is upgraded — only the node-operator registration and quorum logic inside `stream_accounting` changes.

## Rationale

**Why server-confirmed duration instead of client self-report?** A client-reported "seconds listened" value is trivially forgeable by any modified client or script. Deriving duration from the volume of bytes actually requested and served from the origin requires genuinely fetching the audio, which is a materially higher bar for a would-be gamer of the system, and keeps the source of truth inside infrastructure Porto (Beta) or staked, slashable operators (V1) control.

**Why batch attestation instead of one transaction per play?** At meaningful scale, one on-chain transaction per play is gas- and throughput-inefficient. Batching amortizes fixed per-transaction overhead across many plays while keeping the payout latency (batch interval) far below the incumbent settlement timeline, preserving the "real-time-ish" payout experience that differentiates Porto from a 90–180 day royalty chain.

**Why region co-location specifically, rather than a generic global CDN?** At Beta scale with a single target market (UK), a single well-chosen, co-located region minimizes latency for the actual listener base without the operational complexity of a multi-region edge network — that complexity is deferred to the permissionless, geographically-distributed node operator model in V1, where it is inherent to the design rather than an optimization.

**Why content-hash `work_id` rather than a centralized database ID?** A content hash ties the on-chain record to the specific bytes of the registered master, making substitution or corruption of the underlying audio detectable by re-hashing, and gives Porto a natural, collision-resistant identifier that does not depend on any single database being available or trusted.

**Why disclose the Beta trust model explicitly rather than presenting Beta as already decentralized?** See [PIP-2](./PIP-2.md) §Rationale. A gap between claimed and actual decentralization is a specific, well-known failure mode this PIP is written to avoid by construction — the trust model is a first-class, versioned part of the specification (§6), not an implementation detail left undocumented.

## Security Considerations

- **Single Trusted Attestor as a single point of failure/trust (Beta).** A compromised or malicious Trusted Attestor key can submit fabricated `StreamEvent`s, directly triggering fraudulent payouts. Mitigations during Beta: (a) hot/cold key separation, with the batch-submission hot key rate-limited and monitored, and (b) a governance-enforced maximum mint/payout volume per epoch (see [PIP-3](./PIP-3.md) §Security Considerations, [PIP-7](./PIP-7.md)), bounding the damage a single compromised key can cause before intervention.
- **Pre-signed URL leakage or replay.** Mitigated by short TTL (60s), byte-range scoping, and per-session binding — a leaked URL has limited scope and a short window of validity.
- **Sybil listener accounts.** Creating many pseudonymous `listener_id`s to inflate a work's play count is mitigated at Beta scale by account-creation friction and a per-`(listener_id, work_id)` daily play-count rate limit; this is flagged as an area requiring hardening (e.g., proof-of-personhood or stronger session binding) before Mainnet scale.
- **Region/format metadata spoofing.** `region` and `format` fields are set by the attestor at submission time and are informational/analytics fields in the Beta trust model (not payout-determining beyond the base duration calculation); under the V1 quorum model, mismatched `region`/`format` reporting across independent attestors for the same session is itself a signal usable in dispute resolution.
- **Dispute window griefing (V1, forward-looking).** An adversarial minority of attestors could attempt to force disputes on legitimate plays to delay payout. The quorum tolerance window and dispute-resolution parameters (finalized in a future PIP alongside [PIP-6](./PIP-6.md)) must be tuned so that a minority cannot unilaterally block finalization, only trigger review.

## Copyright

Copyright © 2026 Entropy Tech Ltd.

This document is licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
Porto names, logos, and other trademarks are not licensed under this license.

