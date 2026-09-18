---
id: doc_pips_pip_6_md
type: document
---

# PIP-6: Node Operations

Simple Summary Specifies the three node operating modes (CDN, Validator, Full), the PRT-denominated staking and unbonding mechanism operators must go through to register, and the slashing conditions that secure the Mainnet V1 multi-attestor model described in [PIP-4](./PIP-4.md). Abstract Node operator staking is load-bearing for two separable things Porto asks of it: (1) skin-in-the-game for participants earning.

## Connected knowledge

- describes: [[Node roles]] (EXTRACTED)
- describes: [[Registration and staking]] (EXTRACTED)

## Source content

```
PIP: 6
Title: Node Operator Registration, Roles & Staking
Author: Richard Melkonian
Status: Draft
Type: Standards Track (Core)
Created: 2026-09-09
Requires: PIP-1, PIP-3, PIP-4
```

## Simple Summary

Specifies the three node operating modes (CDN, Validator, Full), the PRT-denominated staking and unbonding mechanism operators must go through to register, and the slashing conditions that secure the Mainnet V1 multi-attestor model described in [PIP-4](./PIP-4.md).

## Abstract

Node operator staking is load-bearing for two separable things Porto asks of it: (1) skin-in-the-game for participants earning the 25% operator share of every payout ([PIP-5](./PIP-5.md)), and (2) — once the network moves beyond the Beta Trusted Attestor model — the Byzantine-fault-tolerance assumptions of both AptosBFT consensus itself and the `stream_accounting` quorum mechanism. This PIP specifies registration, staking, unbonding, and slashing. It is written as a forward-looking (Mainnet V1) specification; the Beta phase's single Trusted Attestor is explicitly exempt from staking, as noted throughout.

## Motivation

Early design work considered removing staking and delegation modules entirely from the Aptos-core fork underlying Porto Chain, reasoning that Porto does not need a public validator marketplace at MVP stage. This was reversed once it was recognized that staking is load-bearing for AptosBFT consensus itself — removing it would have broken consensus, not merely removed an unused feature. Separately, and independently of the consensus dependency, node-operator staking is also core to Porto's economic model: operators who stake are operators with skin in the game, which is the property that makes the 25% operator share of the payout split defensible as compensation for infrastructure risk rather than a fee for a purely custodial service.

## Specification

### 1. Node modes

```move
module porto::node_registry {

    const MODE_CDN: u8 = 0;        // caches and serves audio; submits stream attestations
    const MODE_VALIDATOR: u8 = 1;  // runs consensus + accounting VM; does not serve audio
    const MODE_FULL: u8 = 2;       // both CDN and Validator; DEFAULT at launch

    struct NodeOperator has key {
        mode: u8,
        stake: u64,                 // bonded microPRT
        region: vector<u8>,
        registered_at_ms: u64,
        unbonding_request: Option<UnbondingRequest>,
        slash_count: u64,
    }

    struct UnbondingRequest has store {
        amount: u64,
        requested_at_ms: u64,       // unbonds after UNBONDING_PERIOD_MS
    }
}
```

All nodes run in `MODE_FULL` by default at launch — operating both the CDN-serving role and the validator/consensus role — rather than allowing operators to specialize into CDN-only or validator-only roles from day one. Specialization is expected post-launch as the operator set grows and geographic/hardware diversity makes splitting the roles economically sensible.

### 2. Registration and staking

```move
/// Bonds `stake_amount` microPRT from the caller's PRT balance into a
/// StakePool object under module-controlled TransferRef, and registers
/// the caller as a node operator in the given mode and region.
public entry fun register_operator(
    operator: &signer,
    mode: u8,
    region: vector<u8>,
    stake_amount: u64,
);
```

Minimum stake is a governance parameter ([PIP-7](./PIP-7.md)) and scales with the operator's claimed serving capacity/region commitment — an operator claiming to serve a high-traffic region posts a higher minimum stake than one serving a low-traffic region, since the potential payout (and therefore potential fraud) exposure scales with claimed capacity.

### 3. Unbonding

```move
public entry fun request_unbond(operator: &signer, amount: u64);
public entry fun withdraw_unbonded(operator: &signer);  // only after UNBONDING_PERIOD_MS elapses
```

A fixed unbonding period (Beta/V1 initial default: 14 days) applies between `request_unbond` and funds becoming withdrawable. This exists specifically to prevent an operator from withdrawing stake immediately before or during a slashing-eligible dispute, preserving the economic backing behind any pending or in-flight attestation the operator has participated in.

### 4. Slashing conditions

| Condition | Description | Detection |
|---|---|---|
| Availability failure | Operator fails to serve content it has attested availability for, on active probing | Periodic synthetic availability probes against registered operators |
| Attestation mismatch | Operator's submitted `StreamEvent` duration disagrees with quorum beyond the tolerance window (V1 multi-attestor model) | `stream_accounting::finalize_batch` quorum check, [PIP-4](./PIP-4.md) §6 |
| Content integrity failure | Operator serves audio whose hash does not match the registered `work_id` | Client/gateway-side hash verification, reported and disputed on-chain |

Slashing parameters (percentage of stake slashed per violation class, and any escalating penalty for repeat `slash_count`) are governance-configurable ([PIP-7](./PIP-7.md)), not hardcoded in this module, so they can be tuned based on observed network behavior without a module upgrade.

### 5. Beta exemption

During Beta, the sole Trusted Attestor account operating under [PIP-4](./PIP-4.md)'s Beta architecture is **not** required to stake or subject to the slashing conditions in §4 — it is a bootstrap-phase, wholly Porto-operated role, and its trust model is disclosed centralization rather than a staking-secured guarantee. This exemption is temporary and is removed as part of the Beta → V1 migration described in [PIP-4](./PIP-4.md) §8, at which point the Trusted Attestor either registers as a staked operator like any other participant or is retired in favor of the permissionless operator set entirely.

## Rationale

**Why keep staking and delegation rather than strip it, as initially considered?** Two independent reasons converge: staking is load-bearing for AptosBFT consensus (removing it breaks consensus, not just an unused feature), and staking is the mechanism that makes the operator payout share ([PIP-5](./PIP-5.md)) compensation for bonded risk rather than an unsecured fee. Both would need to be rebuilt from scratch if removed, at far greater cost than retaining the inherited module and configuring it for Porto's parameters.

**Why capacity/region-scaled minimum stake rather than a flat minimum?** A flat minimum either overprices entry for small, low-traffic regional operators or underprices the fraud/failure exposure of large, high-traffic operators. Scaling the minimum to claimed capacity keeps the economic security roughly proportional to the value at risk from that operator's potential misbehavior.

**Why a fixed unbonding period?** Without one, an operator anticipating a slashing event (e.g., after knowingly serving corrupted content) could withdraw stake before the slash executes, defeating the purpose of bonding entirely.

## Backwards Compatibility

Not applicable — greenfield module, inherited and reconfigured from the underlying Aptos-core staking/delegation modules rather than built from scratch. The specific slashing conditions in §4 are Porto-specific additions on top of the inherited staking primitives.

## Security Considerations

- **Collusion among a minority of quorum attestors.** The V1 multi-attestor tolerance window ([PIP-4](./PIP-4.md) §6) assumes an honest majority among attesting operators for any given work/session. Minimum-stake and slashing parameters must be set high enough that collusion is not economically rational relative to the payout value at stake, a threshold that should be reassessed as real payout volumes are observed.
- **Availability-probe gaming.** An operator could pass synthetic availability probes while failing to serve real listener traffic reliably. Probe design (frequency, realism relative to actual playback request patterns) is an operational security parameter outside this PIP's on-chain specification, to be detailed in a future Interface-track PIP covering the probing service itself.
- **Region self-declaration.** `region` in `NodeOperator` is self-declared at registration. Beta relies on this being accurate for capacity-based minimum stake calculation; a future hardening (post-Beta) should tie region claims to verifiable network-topology evidence rather than pure self-declaration.

## Copyright

Copyright © 2026 Entropy Tech Ltd.

This document is licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
Porto names, logos, and other trademarks are not licensed under this license.

