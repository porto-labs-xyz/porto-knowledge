---
id: doc_whitepaper_porto_whitepaper_md
type: document
---

# Porto Whitepaper

Porto: A Network-Owned Infrastructure Layer for Music Distribution v0.1.0 , Draft Richard Melkonian, Porto Labs [redacted-email] This is the canonical Porto whitepaper , the single, in-depth narrative source. Normative technical specifications, written in an EIP/RFC-style format, live separately in the [Porto Improvement Proposal (PIP) series](../pips/README.md) and are referenced throughout this document for.

## Connected knowledge

- describes: [[Artist ownership and control|Artist ownership and control]] (EXTRACTED)
- describes: [[Music distribution network|Music distribution network]] (EXTRACTED)
- describes: [[Beta-to-Mainnet rollout|Beta-to-Mainnet rollout]] (EXTRACTED)

## Source content

# Porto: A Network-Owned Infrastructure Layer for Music Distribution

**v0.1.0 , Draft**
**Richard Melkonian, Porto Labs**
**[redacted-email]**

*This is the canonical Porto whitepaper , the single, in-depth narrative source. Normative technical specifications, written in an EIP/RFC-style format, live separately in the [Porto Improvement Proposal (PIP) series](../pips/README.md) and are referenced throughout this document for readers who want the exact on-chain interfaces.*

---

## Abstract

Music streaming platforms extract roughly 30% of every dollar a stream generates, in exchange for owning the infrastructure that delivers the music: the pipes. Artists and labels have no practical alternative, because building and operating that infrastructure themselves has never been economically accessible. The result is a distribution system defined by three persistent failures , opacity in how royalties are calculated, multi-month delay in paying them out, and a fixed, unaccountable margin taken by the platform regardless of the value it adds.

Porto is decentralized streaming infrastructure that removes the precondition behind all three failures: platform ownership of the delivery layer. Artists, labels, publishers, and independent node operators run the network that caches and serves music. Every play is logged on a purpose-built blockchain, Porto Chain, and settled automatically into an on-chain payout split , currently 70% to rights holders, 25% to node operators, and 5% to the Porto protocol , replacing a 90–180 day intermediary chain with same-epoch, auditable settlement.

Porto is not an NFT project, and it does not tokenize a claim on top of an otherwise unchanged platform. It rebuilds the delivery and settlement infrastructure itself. This paper describes the problem in detail, the architecture of Porto Chain and its native token, PRT, the phased path from a centralized Beta to a permissionless mainnet, and the reasoning behind each major design decision.

---

## 1. Introduction

### 1.1 What Porto is

Porto is streaming infrastructure for artists and record labels. It consists of three layers:

1. **A delivery network** , node operators who cache and serve licensed audio, replacing the centralized CDN a streaming platform would otherwise own.
2. **An accounting layer** , Porto Chain, a purpose-built blockchain that logs every play and executes royalty payouts automatically.
3. **A settlement currency** , PRT, the token in which subscription revenue, node-operator compensation, and rights-holder payouts are all denominated.

Porto's thesis is structural, not cosmetic: the leverage artists lack today is infrastructural. Platforms extract margin because they own the pipes, not because that margin reflects value only they can provide. Give the pipes to the people who make and consume the music, and the margin that used to leave the ecosystem stays inside it.

### 1.2 What Porto is not

Porto is explicitly **not**:

- **An NFT project.** A wave of prior "web3 music" ventures tokenized *ownership* , selling collectible rights or royalty shares as NFTs , without changing how music is actually delivered. The platform still owned the pipes; only a claim on the platform's revenue changed hands. Porto's position is that this never addressed the root cause. Porto does not use NFT modules or standards anywhere in its protocol.
- **A fintech wrapper.** Porto is not a faster or cheaper way to move existing royalty payments through the existing distribution stack. It replaces the stack.
- **A general-purpose blockchain.** Porto Chain is an application-specific chain (an "app-chain") with one job: stream accounting and royalty settlement. It is not a smart contract platform for arbitrary applications.

### 1.3 How to read this document

This paper is organized to move from problem, to solution, to mechanism, to execution plan. Section 2 establishes the economics of the problem in detail, with figures. Section 3 introduces the Porto network at a systems level. Sections 4–7 describe the token model, the streaming and attestation architecture, the payout mechanism, and node operator economics , each with enough technical depth to evaluate the design, and each pointing to the corresponding PIP for the exact on-chain specification. Section 8 covers governance. Section 9 lays out the phased rollout from Beta to mainnet. Section 10 covers market positioning, and Section 11 the team. Section 12 concludes.

---

## 2. The Problem

### 2.1 The current royalty chain

An artist today typically distributes through an aggregator , DistroKid, TuneCore, or similar , which places the music on Spotify, Apple Music, and other platforms. Revenue flows in the opposite direction: the platform pays the aggregator, the aggregator pays the label or the artist. Each hop in that chain adds delay and removes visibility. End to end, the chain takes roughly **90 to 180 days** from stream to bank transfer.

The per-stream rate itself is calculated by a formula the platform controls and can change unilaterally, currently averaging **$0.003 to $0.005 per stream** on Spotify. Of every dollar a stream generates, roughly **30%** stays with the platform. The remaining 70% flows through the label and aggregator chain, with each intermediary taking a further cut before anything reaches the artist.

### 2.2 The UK data point

The UK provides a particularly well-documented case. A UK stream generates an average of **£0.011**. Of every **£1** generated by that stream, performers receive roughly **8p** , the rest is absorbed by labels, publishers, and platforms before reaching the person who made the recording. In 2021, a UK Parliamentary inquiry into music streaming concluded that the market needed a complete structural reset. That reset has not happened through regulation, five years on.

### 2.3 What has actually changed over time

It is worth being concrete about the scale of the shift. In the CD and download era, an artist commanding 1M+ monthly streams' worth of listener attention could expect that attention to generate **$10,000 to $40,000 per month**. The same level of attention today, run through the modern streaming and distribution chain, nets the artist **$500 to $1,000 per month** , a reduction of roughly 95%, for a comparable amount of listener engagement. Streaming did not just change the payment mechanism; it collapsed the amount of value that reaches the artist for a given amount of attention.

### 2.4 The problem decomposed

These outcomes are not one problem but three, compounding:

1. **Opacity.** The artist cannot see how their royalty was calculated, which streams counted toward it, or challenge the number if it looks wrong. The calculation happens inside a platform's private systems and is reported, not proven.
2. **Delay.** Revenue generated today arrives, if at all, as a bank transfer three to six months later. For any artist without substantial reserves, this is a cash-flow problem, not merely an inconvenience , it determines whether they can reinvest in their next release, tour, or simply pay rent against work they have already done.
3. **Margin extraction.** The platform takes roughly 30% of every dollar for owning the infrastructure that delivers the stream. The artist has no viable alternative distribution channel, because the platform owns both the audience and the pipes that reach it , there is no competitive market for "who delivers this stream," only a competitive market for "which platform's audience do I want access to," which is not the same thing.

All three are downstream of a single structural fact: **the artist does not own the distribution layer, and therefore has no leverage over any part of how they are paid.** Fixing any one of the three symptoms without addressing infrastructure ownership , a faster payment rail, a clearer royalty statement, a marginally better per-stream rate , does not change the underlying power relationship. Porto is built to change the underlying relationship directly.

---

## 3. The Porto Network

### 3.1 Mission

*We help artists and record labels earn more from streaming by letting them own and run the network that delivers their music, so they earn from distribution, not just plays.*

### 3.2 System overview

Porto has four participant roles and one settlement layer connecting them:

- **Listeners** pay a recurring subscription, priced to undercut incumbent platforms, which converts into PRT behind the scenes.
- **Node operators** run the infrastructure , caching and serving audio, and (once staking is live) participating in consensus , and are compensated in PRT for doing so.
- **Rights holders** (artists, labels, publishers) register their works on-chain and receive automatic, per-stream-attributable payouts.
- **Porto Chain**, the settlement layer, logs every valid play as an on-chain event and executes the payout split without manual intervention.

```
      Listener subscription (fiat)
                │
                ▼
      ┌──────────────────┐
      │ Treasury / Mint   │  mints PRT 1:1 against inbound revenue (§5)
      └────────┬──────────┘
               │
               ▼
      ┌────────────────────┐    StreamEvent      ┌─────────────────────────┐
      │ Streaming Gateway    │ ──────────────────▶ │ Stream Accounting        │
      │ (node operators)     │                     │ (on-chain, Porto Chain)  │  (§6)
      └────────────────────┘                       └────────────┬─────────────┘
                                                                  │ finalized event
                                                                  ▼
                                                       ┌─────────────────────┐
                                                       │ Payout Splitter       │  (§7)
                                                       └──────────┬────────────┘
                                     70% rights holders │ 25% operators │ 5% treasury
                                                                  ▼
                                     ┌─────────────────────────────────────────┐
                                     │ Rights-holder & node-operator wallets     │
                                     └─────────────────────────────────────────┘
```

### 3.3 The revenue split

| Recipient | Share | Why |
|---|---|---|
| Rights holders (artists, labels, publishers) | **70%** | The same nominal share rights holders receive today , Porto's change is not to this number, but to everything downstream of it. |
| Node operators | **25%** | Compensation for running the infrastructure that used to be the platform's sole domain and sole profit center. |
| Porto protocol | **5%** | Funds protocol development and operations , a small fraction of the 30% incumbent platforms retain. |

This is the point that most differentiates Porto's pitch from a typical "better royalties" product: **rights holders do not receive a materially larger nominal percentage than they already do.** What changes is where the remaining 30% goes. Today, it disappears into a platform's balance sheet as pure extraction with no path back to the artist, the listener, or anyone who contributed to the network that generated it. Under Porto, only 5% is retained by the protocol; the other 25% is redistributed to the people who operate the network , which can include the artists and superfans themselves. Value that used to leave the ecosystem now compounds within it. An artist who also runs a node earns both their 70% rights-holder share *and* a portion of the 25% operator pool; a superfan who runs a node earns from a network they helped build, not merely one they pay to access.

*(An earlier design iteration of this split used 70/15/15 , rights holders/node operators/protocol treasury , before Porto Labs' own company take was separated out explicitly from the general protocol treasury line. 70/25/5 is the current model, and it is the one implemented in [PIP-5](../pips/PIP-5.md).)*

### 3.4 Node roles

Nodes operate in one of three modes:

- **CDN mode** , caches content, serves streams, and submits attestations of what was served.
- **Validator mode** , runs consensus and the accounting virtual machine.
- **Full mode** , both. This is the default for every node at launch; specialization into CDN-only or validator-only roles is expected to emerge later as the operator base diversifies by hardware and geography.

The full technical specification for node registration, staking, and slashing is in [PIP-6](../pips/PIP-6.md).

---

## 4. Porto Chain: An App-Chain, Not a General-Purpose L1

### 4.1 Why an app-chain

Porto Chain is purpose-built for one job , music distribution and rights settlement , rather than designed as a platform for arbitrary smart contracts. This mirrors the approach Hyperliquid took in building its own L1 with a custom consensus mechanism (HyperBFT) tuned specifically for its order-book use case, instead of building an order book on top of a general-purpose chain. Applied to music: the chain's only real job is agreeing on state for stream accounting and payouts. Everything else a general-purpose chain needs to support , arbitrary token launches, NFT marketplaces, DeFi composability , is explicitly out of scope, because supporting it well is a different, harder engineering problem than the one Porto exists to solve, and solving it well would not make Porto's actual product better.

### 4.2 Built on a stripped, detached fork of Aptos

Consensus is the single hardest, easiest-to-subtly-break part of building a blockchain , and it is also a solved, extensively audited problem elsewhere. Rather than spend months building bespoke consensus that showcases nothing unique to Porto, Porto Chain is built on a stripped-down fork of `aptos-core`, pinned at the last stable mainnet release at fork time (`aptos-node-v1.45.5`). This is not an arbitrary choice of base layer: Porto's founding engineering team has direct production experience implementing and debugging AptosBFT consensus at scale, having done so previously in a rollup context. Reusing it lets Porto's own engineering effort concentrate entirely on the layer that is actually novel , stream accounting and payout logic , rather than re-deriving a consensus algorithm the team already understands deeply.

**What is retained, unmodified:**

- The **Move VM** (internally, `AptosMoveVm` , kept as its literal, correct name in the Rust source as a deliberate lineage marker; this is unmodified Aptos code, not Porto's own).
- **AptosBFT consensus**, rebranded to Porto branding only where the change is cosmetic and on-chain/user-facing.
- **Staking and delegation.** Considered for removal early in the process , Porto does not need a public validator marketplace at MVP stage , and then explicitly reinstated once it became clear that staking is load-bearing for AptosBFT consensus itself. Removing it would have broken consensus, not simply removed an unused feature.
- **Governance**, including its versioned upgrade path , this is how Porto issues protocol upgrades.
- **The token standard** that PRT is issued against.
- **CLI and deployment tooling.**
- **The RocksDB storage layer** , chain state *is* the ledger; Porto does not bolt on an external database to fake a ledger for demo purposes.

**What is removed:** NFT-related modules and standards. This is as much a positioning decision as a technical one , Porto is explicitly not an NFT project, and carrying NFT infrastructure in the codebase would misrepresent that.

**Rebrand scope.** The Aptos → Porto rename is deliberately narrow: on-chain module names, addresses, genesis configuration, user-facing CLI output, and branding text are renamed. Internal Rust crate names, file paths, and the `AptosMoveVm` identifier specifically are left as Aptos , because that is what they are. The codebase is honest about its own lineage rather than disguising it, down to the git history itself: rather than keep the code as a GitHub fork (which permanently displays "forked from aptos-labs/aptos-core" and is not a good look in front of investors evaluating engineering originality), the repository was cloned at the pinned stable tag, its git history stripped, and pushed fresh under Porto Labs , with the underlying Apache 2.0 license terms fully respected regardless.

Full technical rationale, module inventory, and the exact rename policy are in the engineering `CLAUDE.md` governing the Porto Chain repository; the resulting on-chain modules are specified across [PIP-3](../pips/PIP-3.md) through [PIP-7](../pips/PIP-7.md).

---

## 5. PRT: Token Model

### 5.1 Design constraint

The hardest question any token project has to answer honestly is: *where does the value of the token come from?* Two common answers are both weak on their own. A fixed, speculative supply asks holders to believe demand will simply outstrip an arbitrary supply curve. A block-reward emission schedule mints new tokens regardless of whether the network is actually being used, diluting holders unless adoption happens to outpace emission. Porto's design constraint is that PRT's value must come from **network throughput** , actual usage , not narrative. This section describes the mechanism that makes that structurally true rather than merely asserted; the full normative specification is [PIP-3](../pips/PIP-3.md).

### 5.2 Issuance: mint-on-subscription

PRT has **no fixed maximum supply and no scheduled emission**. The only way new PRT enters circulation is by being minted 1:1 against a real, inbound subscription payment. A listener pays a recurring monthly subscription , priced to undercut incumbent streaming platforms , and that payment, once cleared, triggers a mint of PRT at the network's current conversion rate. There is no discretionary minting path and no scenario in which PRT is created without a corresponding real payment behind it.

This is the single most load-bearing design decision in the token model: it means total PRT supply growth is *mechanically bounded by real subscription revenue*, not by a schedule or a governance whim. "The more streams the network carries, the more PRT is needed" is not a narrative claim under this design , it is the literal mechanism by which supply grows at all.

An equivalent amount of value, at time of mint, is held in a settlement-currency reserve (initially USDC). This is **not a redemption peg** , PRT is not a stablecoin, and there is no guarantee of 1:1 redemption at any later point. The reserve exists to anchor the *initial* mint-time exchange rate to real economic activity, and to fund the stable-conversion leg of the redemption mechanism described next.

### 5.3 Redemption: a two-track payout for volatility

Token price volatility is a legitimate concern raised repeatedly during Porto's own design process , both from investors who are structurally skeptical of tokenomics, and from artists who need predictable income rather than exposure to a young network's price swings. Porto's answer is not to eliminate volatility, but to make exposure to it optional, per participant:

- **Track 1 , Stable.** A rights holder or node operator can configure a percentage of every payout (default: 80%) to auto-convert to a stablecoin at the moment of payout, at the prevailing oracle rate, funded from the treasury reserve rather than a secondary-market swap , avoiding slippage on what are often small, frequent artist payouts.
- **Track 2 , Volatile.** The remainder is paid directly in PRT, giving the recipient direct exposure to network growth.

Some volatility is arguably a *feature*, not a defect, for the participants most likely to run nodes and promote the network: early participants who hold PRT rather than immediately converting are rewarded if the network grows, which aligns the incentives of exactly the people whose participation the network depends on. But forcing that exposure on every artist , including those who simply need predictable income to plan around , would be a mistake. The two-track model lets each participant choose their own risk profile rather than the protocol choosing for them.

### 5.4 Why utility, not speculation

PRT has utility value if, and only if, it is required to actually use the network: artists must hold or spend PRT to publish, and listeners (directly, or via a platform acting on their behalf) must spend PRT to stream. This ties demand mechanically to usage rather than to belief about future usage. Combined with the supply mechanism in §5.2, PRT's price is a function of demand for network access set against a supply that only grows in proportion to real subscription revenue , which is the cleanest defensible tokenomics story available, and the one Porto is built around rather than merely claiming.

### 5.5 Fees and the deflationary counterweight

Transactions on Porto Chain , stream attestation submission, payout settlement, governance actions , consume gas denominated in PRT. Unlike issuance, collected gas is not re-minted: it is burned, or routed to the protocol treasury, per a governance-configurable policy. This gives the network a deflationary pressure that operates independently of, and in the opposite direction to, subscription-driven issuance. Net supply growth in any period is therefore `mint_volume − gas_burned`, and governance can tune this without ever touching the mint mechanism that anchors PRT's value to real revenue , the two levers are deliberately kept separate so that a change to one cannot be mistaken for a change to the other.

### 5.6 Onboarding friction

Requiring users to hold and spend a token introduces real friction relative to a traditional subscription product. Porto's position is that this is a solved UX problem, not a fundamental blocker: modern embedded-wallet and walletless-login flows let a listener or artist interact with the network without ever directly managing a seed phrase or a manual token transfer during onboarding, deferring the "crypto-native" experience until, or unless, a user actually wants it.

---

## 6. Streaming and Stream Accounting

### 6.1 What has to be proven

Porto's central promise to artists is that royalties are transparent and auditable because every play is logged on-chain. That promise is only as strong as the process turning "a listener pressed play" into an on-chain fact. This section describes that process for Porto's initial Beta phase, and how it evolves toward a fully decentralized model. The full normative specification is [PIP-4](../pips/PIP-4.md).

### 6.2 Beta architecture: trusted, region-co-located S3 origin storage

For the initial Beta, Porto deliberately does not attempt to stand up a permissionless, staked CDN network before proving the accounting and payout loop works. Decentralizing physical content serving is a substantial systems engineering effort in its own right, separate from the problem of proving that a stream reliably becomes a correctly-split, on-time payment. Porto's Beta scope separates these two problems explicitly:

- Each registered musical work's audio master is stored in an **AWS S3 bucket**, provisioned in a **Trusted Region** , an AWS region chosen for physical proximity to the target listener base at each stage of rollout. For the initial UK go-to-market, this is `eu-west-2` (London).
- "Trusted" means that during Beta, these buckets , and the compute that serves from them , are operated directly by Porto Labs under a single, Porto-controlled account. There is no permissionless operator set yet at this phase.
- The **Streaming Gateway**, the service that authenticates playback requests and issues access to origin content, is deployed **co-located** with the origin bucket, in the same region and where possible the same availability zone. This removes cross-region egress and minimizes time-to-first-byte and rebuffer risk , which matters both for listener experience and because the gateway is the component generating the server-side duration measurements that anchor payout (§6.3).
- The gateway never exposes bucket contents publicly. On a play request it issues a short-lived (60-second), byte-range-scoped, pre-signed S3 URL, bound to the specific listener, work, and session , narrowing the blast radius of a leaked URL to a short time window and a specific playback context, rather than granting durable access to the full asset.

This is a disclosed, explicit centralization, not a claim of decentralization the product does not yet deliver. Porto's view is that a gap between a company's marketing claims and its actual mechanism is exactly the kind of thing sophisticated counterparties , investors, auditors, and eventually artists themselves , are trained to look for and penalize. The trust model is versioned and documented (§6.5) rather than left implicit.

### 6.3 What counts as a valid, billable play

A play only becomes a billable, on-chain event once the Streaming Gateway has **server-confirmed** , not client-reported , at least `min(30 seconds, 50% of track duration)` of served audio for that listener/work pair within a session. This mirrors the roughly 30-second threshold used by incumbent platforms and exists specifically to prevent skip-spam or bot-driven inflation of play counts from translating directly into payouts.

Server-side confirmation matters because duration is derived from the volume of audio bytes the gateway actually served , logged from its own byte-range request records , rather than trusted from a client's self-reported "I listened for N seconds" heartbeat. A client heartbeat, sent every five seconds during playback, is used for real-time UX (a live dashboard ticking up during a demo, for instance) but is not the value ultimately recorded on-chain; that value is reconciled against the gateway's own serving logs at the point a session ends. Spoofing this requires actually requesting and receiving the corresponding audio bytes from the origin, which is a materially higher bar than forging a client-side timer.

### 6.4 From a play to an on-chain record

Each valid play becomes a `StreamEvent`: a compact record of the work played, the listener, the attesting operator, the server-confirmed duration, the session start time, the serving region, and the audio format. Rather than submit one on-chain transaction per play , inefficient at any meaningful scale , the gateway batches validated events and submits them together (Beta default: every 60 seconds, or every 500 events, whichever comes first). This keeps gas cost bounded while still settling far faster than the incumbent industry's multi-month cycle: Beta payout latency is measured in minutes, not months.

Each musical work is registered on-chain before any stream can be attested against it, identified by a content hash of its canonical audio master rather than an incrementing database ID , tying its on-chain identity directly to the specific audio file it represents, and making any tampering with the registered master detectable by re-hashing. A registered work also declares its internal rights-holder split (supporting arbitrary multi-party arrangements among co-writers, labels, and publishers), which applies within the network-level 70% rights-holder share described in §3.3.

### 6.5 From one trusted attestor to a decentralized quorum

The Beta trust model , a single Trusted Attestor account, with no cross-checking , is a deliberately temporary bootstrap, not the end state. The migration path to a fully decentralized model is designed into the schema from day one: at mainnet, multiple independent, staked node operators serve the same content and independently submit stream events for the same listening session; the protocol requires **m-of-n matching attestations**, within a governance-set tolerance window, before finalizing an event and releasing payout. Events that fail to reach quorum enter a bounded dispute window rather than paying out.

The important engineering property is that this migration changes only *who* may attest and *how* validity is decided , it does not change the on-chain event schema or the downstream payout interface. No wallet, artist dashboard, or third-party integration built against the Beta chain needs to change when the trust model is upgraded underneath it. Node operator staking and the slashing conditions that secure this quorum model , availability failures, attestation mismatches, and content-integrity failures , are specified in [PIP-6](../pips/PIP-6.md).

---

## 7. Payouts: A User-Centric Settlement Model

### 7.1 Why not a pooled, pro-rata model

A naive design would pool all subscription revenue platform-wide and distribute it pro-rata by total stream count across all works. This has a well-documented fairness problem: a listener who exclusively streams independent or niche artists ends up, in effect, subsidizing plays of the platform's most-streamed works, because their subscription dollars are pooled and redistributed by aggregate popularity rather than by what they personally listened to. This is precisely the kind of quiet unfairness Porto exists to remove, not reproduce in a new form.

### 7.2 The user-centric model

Porto instead attributes each listener's subscription value specifically to the works that listener actually streamed, weighted by their own listening time within a settlement period (Beta default: **daily**). Each listener's monthly subscription mint accrues into a per-listener balance across the period; at the epoch boundary, that balance is distributed across the specific works the listener played, proportional to time spent on each. Only then is the 70/25/5 split (§3.3) applied within each work's allocation, followed by any further multi-party split the work itself declares (§6.4).

This is both fairer and more auditable: a specific listener's specific subscription payment can be traced, epoch by epoch, to the specific works it funded , a materially stronger transparency claim than "your payment went into a pool and came out somewhere." The full settlement algorithm, including rounding/dust handling and gas-bounding for listeners with very broad listening habits, is specified in [PIP-5](../pips/PIP-5.md).

### 7.3 Settlement latency as a design parameter

A daily epoch is short enough to preserve Porto's core value proposition relative to the incumbent 90–180 day settlement chain, while long enough to amortize the on-chain cost of settlement across a meaningful volume of listening per listener. Epoch length is a governance parameter (§8), not a hardcoded constant, and is expected to shorten as infrastructure and gas efficiency improve.

---

## 8. Governance

Multiple parameters described throughout this paper , the revenue split, the PRT conversion rate, the gas-burn policy, the attestation quorum size, epoch length, staking minimums, and slashing severity , are governance-configurable rather than hardcoded, using the governance module retained unmodified from the underlying Aptos-core fork specifically for this purpose (§4.2).

During Beta, governance is deliberately configured as **single-key**: a single, Porto-controlled signer is the sole account able to execute governance actions. This mirrors the same underlying trade-off Porto makes throughout its Beta architecture , the Trusted Attestor model in §6, the centralized price oracle behind stable redemption in §5.3 , ship a disclosed, centralized bootstrap version of a component whose fully decentralized version is a substantial, separable engineering effort, rather than gate the entire product proof-of-concept on solving every decentralization problem simultaneously. Even under single-key control, sensitive parameters like the PRT conversion rate are protected by hard, on-chain-enforced rate limits, so that even a compromised or mistaken governance action cannot reprice the token arbitrarily in a single transaction.

Post-Beta, governance is intended to migrate toward stake-weighted voting , node operators voting on proposals weighted by their bonded stake, aligning governance power with the same economic bonding that already secures the network's attestation and consensus layers, rather than introducing a separate, unrelated governance token. The full parameter registry and migration design are specified in [PIP-7](../pips/PIP-7.md).

---

## 9. Phased Rollout

Porto's build sequencing follows a specific logic, stated plainly: **testnet proves the network. Mainnet proves the economics. Traction proves the market.**

| Phase | Streaming | Attestation | Governance | Token | Goal |
|---|---|---|---|---|---|
| **Beta** | Trusted-region, Porto-operated S3 origin (§6.2) | Single Trusted Attestor | Single-key | Testnet PRT, no monetary value | Prove the loop: a stream reliably becomes a correctly-split, on-time payment. |
| **Mainnet V1** | Staked, permissionless node operators | m-of-n multi-attestor quorum | Stake-weighted (migrating) | Mainnet PRT, reserve-minted | Prove the economics with real value flowing. |

For the Beta demo specifically, no real decentralization or real BFT consensus is required to prove the point that matters: an artist uploads a track, a listener streams it, a payout event fires, and PRT visibly splits between rights holder and node operator in real time, on a live dashboard. The deployment underneath that demo is a single-validator Porto Chain , governance overridden to single-key control, running in single-threaded mode , which gets real consensus finality and real RocksDB-backed chain state "for free," without needing to fake a ledger with an external database. Whatever explorer or dashboard is shown to an audience queries that real chain state directly, which is the entire credibility point of the demonstration: the mechanism being shown is the real mechanism, at small scale, not a mockup of it.

Because testnet PRT carries no monetary value, this phase also carries no volatility exposure or financial-decision pressure for the artists and node operators participating in it , which is precisely appropriate for a phase whose purpose is building trust in the mechanism, not asking participants to take on financial risk in an unproven network.

---

## 10. Market Position

Porto's category depends on the audience:

- **To investors:** music tech infrastructure , or, more precisely, web3 infrastructure applied to media distribution. If forced to pick a single category, it sits under "Infrastructure" rather than "Fintech" or "DeFi."
- **Technically:** an app-chain , a purpose-built L1 with a narrow accounting VM, closer in shape to Hyperliquid than to a general-purpose chain or a dApp built on top of one (§4.1).
- **What Porto actually sells:** CDN and rights-settlement infrastructure. Node operators cache and serve audio; the chain settles royalties. Strip away the blockchain framing, and the product is a distribution network with a built-in clearing house.
- **The market being disrupted:** the platform layer of music streaming distribution , specifically, the layer that currently captures the margin between what a stream generates and what a rights holder actually receives.

Porto's initial go-to-market is the UK, motivated directly by the data in §2.2: an average UK stream generating £0.011, only ~8p of every £1 reaching performers, and a 2021 Parliamentary inquiry that concluded reform was needed but has not materialized through regulation. Porto's approach is to build that reform structurally, by default, rather than wait for it to be legislated.

---

## 11. Team

**Richard Melkonian , Founder**

- **CTO, Inflow Music** (Feb 2021 – May 2022). Architected and built the company's core DeFi contracts in Solidity, along with its front-end application, APIs, and backend infrastructure; built its CI/CD pipeline; managed a team of 15 developers. Results: raised $1.5M, launched successfully on the Flow blockchain, and graduated from the Tachyon accelerator.
- **Protocol Lead, Movement Labs** (Feb 2024 – Feb 2026). Second hire at the company. Instrumental in designing and architecting the M2 rollup, including its settlement, verification, and fraud-prevention systems , including ZKFP, using the Risc0 VM to verify proofs of Aptos Move execution. Implemented and rolled out AptosBFT consensus in production, including rehearsing validator ceremonies and debugging live consensus issues. Built the USDCx Bridge. Led three teams , Engineering, Infrastructure, and Research. Results: a testnet launch peaking at 3 million transactions per day, followed by mainnet launch.
- Also previously associated with **Parity**.

Porto's central technical bet , reusing a battle-tested consensus engine rather than building one from scratch (§4.2) , is a direct extension of this background: the founder has personally implemented and debugged the exact consensus mechanism Porto Chain is built on, in production, at meaningful scale.

**Peter Xan , Head of Growth & A&R**

- Growth and strategy across MediaCom, M&C Saatchi, TBWA\Media Arts Lab and BBH. Founder of Thinning Room, developing artists and creator communities. Independent recording artist.

---

## 12. Conclusion

The pattern behind every failure described in Section 2 , opacity, delay, and margin extraction , is the same: an artist has no leverage over a system they do not own any part of. Porto's answer is not a better royalty statement, a faster payment rail bolted onto the existing chain of intermediaries, or a token that claims ownership without changing delivery. It is a rebuild of the delivery and settlement layer itself, owned and operated by the people who make, distribute, and listen to the music running through it.

The engineering strategy follows the same discipline as the business thesis: reuse what is already proven , Aptos's Move VM and BFT consensus , and spend original effort only where Porto is actually novel, which is the stream accounting and payout logic that makes network ownership mean something concrete in an artist's bank balance. The rollout strategy follows the same discipline again: prove the mechanism centralized and small before decentralizing it at scale, and be explicit at every stage about which parts of the system are already trust-minimized and which are not yet.

Porto's claim is a narrow, falsifiable one: that streams can settle transparently, quickly, and with the extracted margin flowing back into the network instead of out of it , and that this is provable on-chain, not merely promised in a pitch deck.

---

## Appendix: Normative Specifications

This paper is the narrative source. The exact on-chain interfaces, data structures, and parameters referenced throughout are specified normatively in the Porto Improvement Proposal series:

| PIP | Covers |
|---|---|
| [PIP-1](../pips/PIP-1.md) | PIP process itself |
| [PIP-2](../pips/PIP-2.md) | Network overview (informational counterpart to this paper) |
| [PIP-3](../pips/PIP-3.md) | PRT token: issuance, redemption, gas/fee model |
| [PIP-4](../pips/PIP-4.md) | Stream accounting, Beta streaming architecture, attestation |
| [PIP-5](../pips/PIP-5.md) | Payout splitter, user-centric settlement |
| [PIP-6](../pips/PIP-6.md) | Node operator registration, roles, staking, slashing |
| [PIP-7](../pips/PIP-7.md) | Governance parameters and upgrade process |

---

*This document is a working draft (v0.1.0), compiled from internal product, engineering, and go-to-market discussion. It is not a final, audited whitepaper, and figures, splits, and parameter defaults are subject to revision as the protocol and business model mature.*

## Copyright and licence

Copyright © 2026 Entropy Tech Ltd.

This document is licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/). Porto names, logos, and other trademarks are not licensed under this licence.

