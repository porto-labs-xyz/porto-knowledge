---
id: doc_pips_pip_2_md
type: document
---

# PIP-2: Network Architecture

Simple Summary Porto is decentralized streaming infrastructure that replaces the platform-owned delivery layer of music streaming with a network that artists, labels, and node operators own and run themselves, settling royalties transparently and automatically on-chain. Abstract This PIP is informational: it does not specify protocol behavior. It records the problem Porto exists to solve, the shape of the solution,.

## Connected knowledge

- describes: [[Music distribution network]] (EXTRACTED)
- describes: [[Node roles]] (EXTRACTED)

## Source content

```
PIP: 2
Title: Porto Network Overview
Author: Richard Melkonian
Status: Draft
Type: Informational
Created: 2026-09-09
```

## Simple Summary

Porto is decentralized streaming infrastructure that replaces the platform-owned delivery layer of music streaming with a network that artists, labels, and node operators own and run themselves, settling royalties transparently and automatically on-chain.

## Abstract

This PIP is informational: it does not specify protocol behavior. It records the problem Porto exists to solve, the shape of the solution, and how the other PIPs in this series fit together, so that a reader arriving at any single technical PIP has the context needed to evaluate it. Token mechanics are specified normatively in [PIP-3](./PIP-3.md); stream accounting and the Beta streaming architecture in [PIP-4](./PIP-4.md); payout logic in [PIP-5](./PIP-5.md); node operator roles and staking in [PIP-6](./PIP-6.md); governance in [PIP-7](./PIP-7.md).

## Motivation

### How artists get paid today

Artists distribute through aggregators (DistroKid, TuneCore, and similar), who place music on Spotify, Apple Music, and other platforms. The platform pays the aggregator; the aggregator pays the label or artist. That chain takes roughly 90–180 days end to end. The per-stream rate is set unilaterally by the platform and can change at any time — currently around $0.003–$0.005 per stream on Spotify. Of every dollar generated, roughly 30% stays with the platform, with the remaining 70% flowing through the label/aggregator chain, each intermediary taking a cut, before anything reaches the artist.

In the UK specifically: a UK stream generates an average of £0.011, and of every £1 generated, performers receive roughly 8p. A 2021 UK Parliamentary inquiry into music streaming concluded the market needs a complete reset. That reset has not happened through regulation.

For historical context: in the CD/download era, an artist with 1M+ monthly streams' worth of attention could earn $10,000–$40,000/month from that attention. Today, the same attention nets $500–$1,000/month after label, publisher, distributor, and platform cuts.

### The problem has three parts

1. **Opacity.** The artist cannot see how their royalty was calculated, which streams counted, or why the number is what it is.
2. **Delay.** Revenue generated today arrives as a bank transfer in three to six months — a cash-flow problem, not merely an inconvenience.
3. **Margin extraction.** The platform takes roughly 30% for owning the pipes. The artist has no alternative, because the platform owns the audience and the infrastructure that reaches it.

All three are symptoms of one root cause: **the artist does not own the distribution layer, and therefore has no leverage over any of it.**

### Why prior "web3 music" attempts didn't fix this

A wave of NFT-based music projects tokenized *ownership* — selling collectible rights or royalty shares as NFTs — without changing how music is actually delivered. The platform still owns the pipes; only a claim on the platform's revenue changed hands. Porto's position is that this does not address the root cause. Porto explicitly does not use NFT modules or standards ([PIP-4](./PIP-4.md) §Removed Modules) — it rebuilds the delivery and settlement infrastructure itself, rather than tokenizing a claim on top of an unchanged system.

## Specification

This PIP is non-normative. See referenced PIPs for specification text.

### System overview

```
 ┌────────────┐      subscription (fiat)      ┌──────────────────┐
 │  Listener  │ ─────────────────────────────▶ │  Treasury / Mint │
 └────────────┘                                └────────┬──────────┘
       │  stream request                                │ mints PRT (PIP-3)
       ▼                                                 ▼
 ┌────────────────────┐   StreamEvent batch    ┌───────────────────────┐
 │ Streaming Gateway   │ ──────────────────────▶│ stream_accounting     │
 │ (Beta: trusted S3   │                        │ module (PIP-4)        │
 │ co-located buckets) │                        └──────────┬────────────┘
 └────────────────────┘                                    │ finalized event
                                                             ▼
                                                  ┌───────────────────────┐
                                                  │ payout_splitter (PIP-5)│
                                                  └──────────┬────────────┘
                                    70% rights holders │ 25% operators │ 5% treasury
                                                             ▼
                                    ┌────────────────────────────────────┐
                                    │ Rights holder / operator wallets    │
                                    └────────────────────────────────────┘
```

### Revenue split

| Recipient | Share | Role |
|---|---|---|
| Rights holders (artists, labels, publishers) | 70% | Paid automatically per settlement epoch |
| Node operators | 25% | Run streaming/attestation infrastructure per [PIP-4](./PIP-4.md) and [PIP-6](./PIP-6.md) |
| Porto protocol treasury | 5% | Funds protocol development and operations |

This is the network-level split. Within the 70% rights-holder share, individual works may declare arbitrary multi-party splits among collaborators, labels, and publishers — see `MusicalWork.rights_holders` in [PIP-4](./PIP-4.md).

An earlier design iteration used 70/15/15 (rights holders/node operators/protocol treasury) before Porto Labs' own take was separated out explicitly from the protocol treasury line. 70/25/5 is the current, corrected model: it keeps the "the 30% platform tax becomes a 5% protocol fee" claim honest, since Porto Labs' own take (5%) is materially smaller than the 30% currently retained by incumbent platforms, with the difference (25%) redistributed to the people who operate the network rather than extracted by a centralized intermediary.

### Node roles

Nodes run in one of three modes, specified fully in [PIP-6](./PIP-6.md):

- **CDN mode** — caches and serves audio, submits stream attestations.
- **Validator mode** — runs consensus and the accounting VM.
- **Full mode** — both. Default for all nodes at launch.

### Phased rollout

| Phase | Streaming | Attestation trust model | Token | Reference |
|---|---|---|---|---|
| Beta | Trusted-region co-located S3 buckets, Porto-operated | Single Trusted Attestor account | Testnet PRT, no monetary value | [PIP-4](./PIP-4.md) §Beta Architecture |
| V1 (Mainnet, permissionless CDN) | Staked, permissionless node operators | m-of-n multi-attestor quorum | Mainnet PRT, reserve-minted | [PIP-4](./PIP-4.md) §Migration Path, [PIP-6](./PIP-6.md) |

The sequencing is deliberate: **testnet proves the network. Mainnet proves the economics. Traction proves the market.** Beta is scoped to prove the accounting and payout loop — that a stream reliably and auditably becomes a correctly-split, on-time payment — without requiring real decentralization or real consensus to exist yet. Real decentralization of physical serving is a Phase 2 concern layered on top of an already-proven accounting core, not a prerequisite for proving the core.

## Rationale

### Why an app-chain, and why fork Aptos

Porto Chain is purpose-built for one job: music distribution and rights settlement, not a general-purpose smart contract platform. This mirrors Hyperliquid's approach of building a custom L1 with consensus tuned specifically to one application (an order book, in their case) rather than trying to be general-purpose. Porto's founding engineering team has direct production experience implementing and debugging AptosBFT consensus; reusing it is a pragmatic application of that experience rather than an unfamiliar dependency, and it lets engineering effort concentrate on the genuinely novel part of the system — stream accounting and payout logic — rather than on re-deriving a solved, audited consensus algorithm. Full technical rationale is in [PIP-4](./PIP-4.md) and the Porto Chain repository's `CLAUDE.md`.

### Why disclose Beta centralization rather than obscure it

Porto's Beta streaming architecture (single trusted attestor, Porto-operated S3 infrastructure) is explicitly centralized. This PIP series treats that as a disclosed, temporary trust assumption with a defined migration path ([PIP-4](./PIP-4.md) §Migration Path), rather than a permanent design or something to obscure behind decentralization framing the product does not yet deliver. The alternative — claiming decentralization the network does not yet have — creates exactly the kind of gap between a company's marketing claims and its actual mechanism that sophisticated counterparties (investors, auditors, artists) are trained to look for and penalize.

## Backwards Compatibility

Not applicable — Porto is a greenfield protocol.

## Security Considerations

Discussed per-component in [PIP-3](./PIP-3.md), [PIP-4](./PIP-4.md), [PIP-5](./PIP-5.md), [PIP-6](./PIP-6.md), and [PIP-7](./PIP-7.md). The Beta phase's central security consideration is enumerated in [PIP-4](./PIP-4.md) §Security Considerations: a single Trusted Attestor is a single point of failure and trust by design, disclosed rather than hidden, with mitigations (key custody, mint-volume rate limits) specified there.

## Copyright

Copyright © 2026 Entropy Tech Ltd.

This document is licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
Porto names, logos, and other trademarks are not licensed under this license.

