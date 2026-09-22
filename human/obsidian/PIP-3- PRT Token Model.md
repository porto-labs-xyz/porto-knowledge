---
id: doc_pips_pip_3_md
type: document
---

# PIP-3: PRT Token Model

Simple Summary PRT is Porto's native token, implemented as an Aptos-standard Fungible Asset. Unlike a fixed-supply or block-reward-emitted token, PRT is minted only against real, inbound subscription value, and it is the sole unit in which listener demand, node-operator compensation, and rights-holder payouts are denominated. Abstract This PIP specifies the PRT token: its on-chain representation, its issuance.

## Connected knowledge

- describes: [[PRT utility token|PRT utility token]] (EXTRACTED)

## Source content

```
PIP: 3
Title: PRT Fungible Asset & Issuance Standard
Author: Richard Melkonian
Status: Draft
Type: Standards Track (Core)
Created: 2026-09-09
Requires: PIP-1
```

## Simple Summary

PRT is Porto's native token, implemented as an Aptos-standard Fungible Asset. Unlike a fixed-supply or block-reward-emitted token, PRT is minted only against real, inbound subscription value, and it is the sole unit in which listener demand, node-operator compensation, and rights-holder payouts are denominated.

## Abstract

This PIP specifies the PRT token: its on-chain representation, its issuance (minting) mechanism, its redemption/conversion mechanism, its role as the bonding asset for node operator stake, and its gas/fee model. The central design constraint is stated in [PIP-2](./PIP-2.md): PRT must derive its value from network throughput, not from narrative or speculative emission. Every unit of PRT in circulation must be traceable to a real, inbound unit of subscription value at the time it was minted. This PIP defines the mechanism that guarantees that property.

## Motivation

A token whose supply is unrelated to actual usage is vulnerable to the exact criticism Porto must be able to answer cleanly to sophisticated counterparties: "where does the value of the token come from?" Two answers are commonly given by token projects and both are weak on their own:

1. **Fixed/capped supply with speculative demand** — value depends on belief that future demand will outstrip a supply curve unrelated to actual usage. This is a narrative-driven answer.
2. **Block-reward emission** — new tokens are minted on a schedule regardless of usage, diluting holders unless usage growth outpaces emission. This decouples issuance from demand.

Porto instead ties every mint event directly to a real, contemporaneous inbound payment (a listener's subscription). This produces a token whose supply growth is mechanically bounded by real revenue, and whose price discovery is a function of demand for network access (streaming, publishing) against that revenue-bounded supply — the "utility token" case, made structurally true rather than asserted.

## Specification

### 1. Token identity

| Field | Value |
|---|---|
| Name | Porto |
| Symbol | PRT |
| Decimals | 6 |
| Smallest unit | 1 `microPRT` = 10⁻⁶ PRT |
| Standard | Aptos Fungible Asset (FA) — `0x1::fungible_asset`, object-based, not the legacy `0x1::coin::Coin<T>` standard |

**Rationale for FA over legacy Coin standard:** the FA standard represents PRT holdings as Move `Object`s rather than a generic `Coin<T>` resource, which gives Porto: (a) per-account freeze capability without a separate allowlist module (used for compliance holds, [Security Considerations](#security-considerations)); (b) native support for dispatchable hooks on transfer, which the Redemption Module (§4) and the epoch-settlement logic in [PIP-5](./PIP-5.md) both rely on to trigger atomic conversion at time of payout; and (c) forward compatibility with the Aptos ecosystem's ongoing migration away from the legacy Coin standard, avoiding a future forced migration of Porto's own token.

### 2. Issuance: mint-on-subscription

PRT has no fixed maximum supply and no scheduled block-reward emission. The only path by which new PRT enters circulation is the `treasury::mint_from_subscription` entry function, callable exclusively by the Treasury Module holding the FA `MintRef`.

```move
/// Held only by the Treasury object; never exposed to a user-controlled account.
struct TreasuryCaps has key {
    mint_ref: MintRef,
    burn_ref: BurnRef,
    transfer_ref: TransferRef,
}

/// Conversion rate: microPRT minted per minor unit of settlement currency
/// (e.g. USD cents), scaled by RATE_PRECISION. Updatable only via governance
/// (PIP-7), bounded to a maximum change of MAX_RATE_DELTA_BPS per epoch.
struct ConversionRate has key {
    rate: u128,
    rate_precision: u64,
    last_updated_epoch: u64,
}

/// Called by the off-chain Payment Settlement Service once a listener's
/// subscription payment has cleared and been converted to the Treasury's
/// settlement-currency reserve (see §3). Idempotency_key prevents double-mint
/// on retried webhook delivery from the upstream payment processor.
public entry fun mint_from_subscription(
    treasury_signer: &signer,
    recipient: address,
    settlement_minor_units: u64,
    idempotency_key: vector<u8>,
) acquires TreasuryCaps, ConversionRate, ProcessedPayments {
    // 1. assert idempotency_key not already processed (replay protection)
    // 2. amount = settlement_minor_units * conversion_rate.rate / RATE_PRECISION
    // 3. fungible_asset::mint(&caps.mint_ref, amount) -> FungibleAsset
    // 4. primary_fungible_store::deposit(recipient, fa)
    // 5. emit MintEvent { recipient, settlement_minor_units, prt_amount: amount, idempotency_key }
}
```

Every mint event is 1:1 accounted against a specific, idempotency-keyed inbound payment. There is no discretionary or scheduled minting path in the module. This is the mechanism that makes "value comes from network throughput" a structural property of the token rather than a claim about it.

### 3. Reserve backing (informational, not a peg)

For every `settlement_minor_units` of fiat converted to a mint, the equivalent value in a settlement currency (initially USDC) is held in a Treasury Reserve address. This is **not** a 1:1 redemption peg — PRT is not a stablecoin and does not guarantee redemption of any specific amount of reserve per PRT. The reserve exists to:

- Anchor the initial mint-time exchange rate to real economic activity rather than an arbitrary governance decision, and
- Fund the stable-conversion leg of the two-track payout described in §4.

The `ConversionRate.rate` parameter is the *mint-side* rate (fiat-in → PRT-out) and is distinct from the *market* price of PRT, which floats freely based on secondary-market supply and demand for network access. The two are expected to diverge as the network grows: rising demand to hold/use PRT for access, against a supply that only grows in proportion to subscription revenue, is the intended appreciation mechanism referenced in [PIP-2](./PIP-2.md).

### 4. Redemption: two-track payout

Rights holders receive PRT via the Payout Splitter ([PIP-5](./PIP-5.md)). At the moment of receipt, each rights holder's account-level `RedemptionPreference` is consulted:

```move
struct RedemptionPreference has key {
    stable_bps: u64,   // 0–10000; portion auto-converted to settlement currency
    // remaining (10000 - stable_bps) is retained as PRT
}

/// Invoked atomically within the same transaction as a payout credit.
/// Uses the Price Oracle Module (see §5) to quote a conversion rate at the
/// moment of payout, and executes the conversion leg via the Treasury
/// Reserve rather than a secondary-market swap, avoiding slippage on
/// small, frequent artist payouts.
public(friend) fun apply_redemption_preference(
    recipient: address,
    gross_prt: u64,
) acquires RedemptionPreference, TreasuryCaps { /* ... */ }
```

- **Track 1 — Stable.** `stable_bps` of each payout is converted to settlement currency (e.g. USDC) at the payout-time oracle rate and credited to the rights holder's stable balance. Default for new accounts: `8000` (80%), matching the threshold discussed during product design, but user-configurable from 0 to 10000.
- **Track 2 — Volatile.** The remainder is credited as PRT directly, giving the rights holder direct exposure to network growth.

This lets each participant choose their own risk profile rather than the protocol forcing volatility, or the absence of it, on everyone uniformly.

### 5. Price oracle requirement

The redemption conversion in §4 requires a PRT/settlement-currency price quote at time of payout.

- **Beta:** a single, Porto-operated **Price Attestor** account periodically signs and submits a price observation transaction (`oracle::submit_price`), sourced from Porto's own off-chain order book or a designated reference exchange. This is a disclosed centralization, consistent with the Beta Trusted Attestor model in [PIP-4](./PIP-4.md).
- **Mainnet (V1):** migrates to a decentralized oracle network (e.g., a Pyth-style pull oracle or an equivalent Aptos-native decentralized price feed), specified in a future PIP once selected.

### 6. Gas / fee model

All Porto Chain transactions (stream attestation submission, payout settlement, governance actions) consume gas denominated in `microPRT`. Unlike the mint-on-subscription issuance path, gas fees collected by the protocol are **not re-minted** — they are either burned (via `BurnRef`) or routed to the protocol treasury, per a governance-configurable `GasFeePolicy` parameter ([PIP-7](./PIP-7.md)). This provides a deflationary pressure on circulating PRT that is independent of, and works in the opposite direction to, subscription-driven mint issuance — net supply growth in any period is therefore `mint_volume - gas_burned`, giving governance a lever (via gas price and burn-vs-treasury split) to manage circulating supply growth without touching the mint-from-subscription mechanism itself.

### 7. Staking interplay

PRT is the exclusive bonding asset for node-operator stake, specified in [PIP-6](./PIP-6.md). Bonded PRT is held in a `StakePool` object under `TransferRef`-gated custody and is not freely transferable by the staking account until the unbonding period elapses.

### 8. Interfaces summary

```move
module porto::prt {
    // Issuance
    public entry fun mint_from_subscription(treasury_signer: &signer, recipient: address, settlement_minor_units: u64, idempotency_key: vector<u8>);
    public entry fun set_conversion_rate(governance_signer: &signer, new_rate: u128); // bounded by MAX_RATE_DELTA_BPS

    // Redemption
    public entry fun set_redemption_preference(account: &signer, stable_bps: u64);
    public(friend) fun apply_redemption_preference(recipient: address, gross_prt: u64);

    // Views
    #[view] public fun conversion_rate(): u128;
    #[view] public fun circulating_supply(): u128;
    #[view] public fun reserve_balance(): u64;

    // Events
    struct MintEvent has drop, store { recipient: address, settlement_minor_units: u64, prt_amount: u64, idempotency_key: vector<u8> }
    struct RedeemEvent has drop, store { recipient: address, prt_amount: u64, settlement_amount: u64, oracle_rate: u128 }
    struct GasBurnEvent has drop, store { amount: u64, epoch: u64 }
    struct RateUpdateEvent has drop, store { old_rate: u128, new_rate: u128, epoch: u64 }
}
```

## Rationale

**Why not a fixed supply?** A fixed supply forces PRT's early value entirely onto speculation about future adoption, which is the exact "tokenomics some VCs don't like" concern raised during design. Mint-on-subscription instead lets PRT's supply track realized, not hoped-for, usage from day one.

**Why not block-reward emission for node operators?** Rewarding operators from a separate emission schedule decouples their income from actual demand and dilutes all holders regardless of whether the network is growing. Instead, operator income flows exclusively from the same mint-on-subscription pool that funds rights-holder payouts (see [PIP-5](./PIP-5.md)), meaning operator compensation is mechanically tied to real listener demand, not a separate inflation schedule.

**Why a bounded rate-of-change on the conversion rate?** An unbounded, governance-settable mint rate is a centralization and manipulation risk — governance could mint an arbitrarily large amount of PRT per dollar of inbound revenue, diluting existing holders instantly. `MAX_RATE_DELTA_BPS` per epoch bounds how quickly this parameter can move, giving the market time to react and reducing the blast radius of a compromised or malicious governance action (see [PIP-7](./PIP-7.md)).

**Why gas burn as a separate lever from mint policy?** Keeping issuance (mint-from-subscription) and supply reduction (gas burn) as two independent mechanisms means governance can tune net supply growth via the burn/treasury split without ever touching the mint mechanism that anchors PRT's value to real revenue — a change to one lever cannot be mistaken for, or accidentally become, a change to the other.

## Backwards Compatibility

PRT replaces the `APT` ticker inherited from the underlying Aptos-core fork (on-chain symbol, metadata, gas unit references, CLI defaults, genesis configuration). This is a rename at the chain's genesis and carries no backwards-compatibility burden, since Porto Chain has no prior mainnet history under the `APT` ticker.

## Security Considerations

- **Mint capability custody.** `TreasuryCaps.mint_ref` must never be held by a user-controlled or single-EOA-controlled account. It is held by a governance-gated Treasury object, with the `mint_from_subscription` entry point restricted to the Payment Settlement Service's designated signer only, and rate-limited per epoch to bound the damage of a compromised settlement-service key.
- **Idempotency and double-mint.** `idempotency_key` (derived from the upstream payment processor's transaction ID) is checked against a `ProcessedPayments` set before every mint, preventing replayed webhook deliveries from minting twice against a single payment.
- **Oracle manipulation.** The Beta single-attestor price oracle (§5) is a trust assumption identical in shape to the Beta stream attestor in [PIP-4](./PIP-4.md): a compromised or malicious price attestor could misprice the stable-conversion leg of redemption. Mitigation during Beta: price submissions are bounded to a maximum deviation from the previous observation per submission interval, with anomalous submissions halting the redemption path rather than executing at a bad rate.
- **Rate-of-change governance attack.** See Rationale — `MAX_RATE_DELTA_BPS` is the primary mitigation. A full governance-attack analysis is in [PIP-7](./PIP-7.md) §Security Considerations.
- **Gas-burn accounting drift.** Burned/treasury-routed gas must be reconciled against `circulating_supply()` in the same transaction as collection to prevent a discrepancy between recorded and actual circulating supply.

## Copyright

Copyright © 2026 Entropy Tech Ltd.

This document is licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
Porto names, logos, and other trademarks are not licensed under this license.
