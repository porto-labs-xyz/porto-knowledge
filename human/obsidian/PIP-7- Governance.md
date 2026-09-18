---
id: doc_pips_pip_7_md
type: document
---

# PIP-7: Governance

Simple Summary Specifies the governance-controlled parameter set referenced throughout this PIP series, and the process by which Porto Chain's modules are upgraded — beginning with single-key governance during Beta, with a disclosed, explicit migration path to broader participation. Abstract Multiple PIPs in this series (network split percentages in [PIP-2](./PIP-2.md), the PRT conversion rate and gas-burn policy in.

## Connected knowledge

- describes: [[Governed parameter registry]] (EXTRACTED)

## Source content

```
PIP: 7
Title: Governance Parameters & Upgrade Process
Author: Richard Melkonian
Status: Draft
Type: Standards Track (Core)
Created: 2026-09-09
Requires: PIP-1, PIP-3, PIP-4, PIP-5, PIP-6
```

## Simple Summary

Specifies the governance-controlled parameter set referenced throughout this PIP series, and the process by which Porto Chain's modules are upgraded — beginning with single-key governance during Beta, with a disclosed, explicit migration path to broader participation.

## Abstract

Multiple PIPs in this series (network split percentages in [PIP-2](./PIP-2.md), the PRT conversion rate and gas-burn policy in [PIP-3](./PIP-3.md), attestation quorum size in [PIP-4](./PIP-4.md), epoch length in [PIP-5](./PIP-5.md), staking minimums and slashing severity in [PIP-6](./PIP-6.md)) declare a parameter "governance-configurable" without specifying what governance means procedurally. This PIP is that specification: it enumerates the governed parameter set, defines the upgrade mechanism inherited from Aptos-core's governance module, and specifies Porto's Beta-phase single-key configuration and its planned evolution.

## Motivation

Porto's underlying Aptos-core fork retains its full governance module, unmodified, specifically because governance is how Porto issues protocol upgrades — this was treated as a non-negotiable retention throughout the strip-and-rebrand engineering pass that removed NFT modules and considered (then reversed) removing staking. Having preserved the capability, this PIP defines how it is actually configured and used for Porto's specific parameter set, rather than leaving it as an inherited-but-undocumented capability.

## Specification

### 1. Governed parameter registry

| Parameter | Defined in | Beta default | Bounds |
|---|---|---|---|
| Network split (rights holders / operators / treasury) | [PIP-2](./PIP-2.md) §Revenue split | 70% / 25% / 5% | Must sum to 100%; no single-transaction change permitted, see §3 |
| `ConversionRate.rate` (mint-side, fiat→PRT) | [PIP-3](./PIP-3.md) §2 | Set at Beta launch, disclosed separately | `MAX_RATE_DELTA_BPS` per epoch |
| `DefaultStableRedemptionBps` | [PIP-8](./PIP-8.md) §5 | 8000 bps (80%) | 0–10000 bps; account holders may override |
| `GasFeePolicy` (burn vs. treasury split) | [PIP-3](./PIP-3.md) §6 | 100% burn | 0–100% either direction |
| Attestation quorum size (m-of-n) | [PIP-4](./PIP-4.md) §6 | N/A during Beta (single attestor) | Activated at V1 migration |
| `EPOCH_LENGTH_MS` | [PIP-5](./PIP-5.md) §2 | 86,400,000 (24h) | Minimum bound TBD by gas-cost analysis |
| `MAX_WORKS_PER_EPOCH` | [PIP-5](./PIP-5.md) §5 | 200 | — |
| Minimum stake per mode/region | [PIP-6](./PIP-6.md) §2 | N/A during Beta | — |
| Slashing severity per violation class | [PIP-6](./PIP-6.md) §4 | N/A during Beta | — |
| `UNBONDING_PERIOD_MS` | [PIP-6](./PIP-6.md) §3 | 14 days | — |

### 2. Upgrade mechanism

```move
module porto::governance {
    /// Proposes a parameter change or module upgrade. During Beta, only the
    /// designated single governance signer may successfully propose and
    /// execute; the proposal/voting machinery inherited from Aptos-core
    /// governance is retained in the codebase but its multi-party voting
    /// path is not yet activated (see §3).
    public entry fun propose(proposer: &signer, execution_payload: vector<u8>);
    public entry fun execute(executor: &signer, proposal_id: u64);
}
```

Module code upgrades (as opposed to parameter changes within already-deployed modules) go through the same governance-gated path, using Aptos-core's inherited versioned upgrade capability, unmodified.

### 3. Beta: single-key governance

During Beta, Porto Chain's governance is deliberately configured to single-key control — a single, Porto-controlled signer is the sole account capable of executing governance proposals. This mirrors the MVP build decision to run the chain as a single validator with governance overridden to single-key control, made explicitly to avoid the substantial engineering cost of standing up a full token-weighted or stake-weighted voting system before the accounting and payout loop itself was proven.

This is disclosed centralization, consistent with the Beta Trusted Attestor model in [PIP-4](./PIP-4.md) and the Beta price oracle in [PIP-3](./PIP-3.md) — all three are the same underlying trade-off (ship a centralized bootstrap version of a component whose decentralized version is a larger, separable engineering effort) applied consistently across the protocol, rather than a governance-specific shortcut.

### 4. Migration path

Post-Beta, governance is intended to migrate toward stake-weighted voting, where registered node operators ([PIP-6](./PIP-6.md)) vote on proposals weighted by bonded stake — aligning governance power with the same economic bonding that already secures the attestation and consensus layers, rather than introducing a separate, unrelated governance-token distribution. The precise voting mechanics (quorum thresholds, proposal bonding to prevent spam, timelock between proposal passage and execution) are left to a future PIP once the V1 staking model in [PIP-6](./PIP-6.md) is live and real stake distribution data exists to inform parameter choices.

## Rationale

**Why single-key governance for Beta rather than deferring governance entirely?** Deferring governance entirely (i.e., hardcoding all parameters with no upgrade path) would make correcting an early misconfigured parameter — for example, a mint conversion rate found to be miscalibrated after real usage data arrives — require a full module redeployment rather than a governance transaction. Single-key governance preserves the ability to correct course quickly during Beta while being honest that "governance" during this phase is procedurally equivalent to founder discretion, not decentralized decision-making.

**Why bound `ConversionRate` changes via `MAX_RATE_DELTA_BPS` even under single-key control?** Even a well-intentioned single governance key benefits from a hard, on-chain-enforced rate limit on how fast it can move the mint-side conversion rate: it protects existing PRT holders from a sudden, large repricing of new issuance (whether from error or compromise) regardless of whether the key itself is trusted, since the bound is enforced by the module, not by the operator's discipline.

**Why keep the multi-party voting machinery in the codebase even though it is inactive during Beta?** Retaining Aptos-core's inherited governance/voting module unmodified (rather than stripping it down to only what single-key governance needs) means the eventual migration to stake-weighted voting is a configuration and activation change, not a from-scratch build — consistent with the broader strip-and-rebrand philosophy applied throughout Porto Chain's engineering ([PIP-4](./PIP-4.md) §Motivation) of reusing proven infrastructure wherever the proven version already does what Porto eventually needs.

## Backwards Compatibility

The migration from single-key to stake-weighted governance (§4) is, by construction, a change in *who* can execute a governance proposal, not a change to the `propose`/`execute` interface itself or to any of the governed parameters' semantics — modules and off-chain tooling built against the governance interface during Beta do not require changes at migration time, only the account(s) authorized to call it change.

## Security Considerations

- **Single-key compromise (Beta).** The Beta governance key is the highest-value target in the entire system during this phase — compromise grants control over every governed parameter in §1, including the network split and PRT conversion rate. Mitigated by treating this key with the highest available operational security standard (hardware-backed custody, multi-person operational process for actually triggering a signature even though only one on-chain key exists), independent of the on-chain rate-limit protections in [PIP-3](./PIP-3.md).
- **Parameter bound gaps.** Several parameters in §1 (minimum stake, slashing severity, quorum size) do not yet have specified bounds, since they depend on operational data not yet available before V1 launch. Shipping them as unbounded governance parameters is an accepted, temporary risk during single-key Beta governance and must be resolved with explicit bounds before stake-weighted voting is activated in §4, since unbounded parameters are a materially larger risk once control is distributed across parties with potentially divergent incentives.
- **Governance proposal front-running / MEV.** Not addressed in this PIP; deferred to the future PIP specifying stake-weighted voting mechanics in §4, where timelocked execution between proposal passage and execution is expected to be part of the mitigation.

## Copyright

Copyright © 2026 Entropy Tech Ltd.

This document is licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
Porto names, logos, and other trademarks are not licensed under this license.

