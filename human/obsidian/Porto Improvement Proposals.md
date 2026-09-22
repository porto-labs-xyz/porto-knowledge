---
id: doc_pips_readme_md
type: document
---

# Porto Improvement Proposals

Porto Improvement Proposals (PIPs) PIPs are the design documents for the Porto protocol — Porto Chain, the PRT token, stream accounting, payouts, node operation, and governance — written in an EIP/RFC-style format. See [PIP-1](./PIP-1.md) for the full process, PIP types, and status lifecycle. Start with [PIP-2](./PIP-2.md) for the non-technical overview (the problem, the solution, and how the rest of this series.

## Connected knowledge

No outgoing links.

## Source content

# Porto Improvement Proposals (PIPs)

PIPs are the design documents for the Porto protocol — Porto Chain, the PRT token, stream accounting, payouts, node operation, and governance — written in an EIP/RFC-style format. See [PIP-1](./PIP-1.md) for the full process, PIP types, and status lifecycle.

Start with [PIP-2](./PIP-2.md) for the non-technical overview (the problem, the solution, and how the rest of this series fits together) before reading the Standards Track specifications.

## Index

| PIP | Title | Type | Status |
|---|---|---|---|
| [1](./PIP-1.md) | PIP Purpose, Process, and Format | Meta | Living |
| [2](./PIP-2.md) | Porto Network Overview | Informational | Draft |
| [3](./PIP-3.md) | PRT Fungible Asset & Issuance Standard | Standards Track (Core) | Draft |
| [4](./PIP-4.md) | Stream Accounting & Attestation Protocol | Standards Track (Core) | Draft |
| [5](./PIP-5.md) | Payout Splitter Module | Standards Track (Core) | Draft |
| [6](./PIP-6.md) | Node Operator Registration, Roles & Staking | Standards Track (Core) | Draft |
| [7](./PIP-7.md) | Governance Parameters & Upgrade Process | Standards Track (Core) | Draft |

## Reading order

```
PIP-1  (process)
  └─ PIP-2  (overview — problem, solution, phased rollout)
       ├─ PIP-3  (PRT token: issuance, redemption, gas/fee model)
       ├─ PIP-4  (streaming + on-chain stream accounting; Beta S3 architecture)
       │    └─ PIP-5  (payout splitter — consumes finalized StreamEvents)
       ├─ PIP-6  (node operator staking — secures PIP-4's V1 attestation model)
       └─ PIP-7  (governance — parameters referenced by PIP-3 through PIP-6)
```

## Numbering ranges

See [PIP-1 §Numbering Convention](./PIP-1.md#numbering-convention) for reserved ranges (Meta, Informational, Token, Stream/Attestation, Node/Staking, Governance) for future proposals.

## Status

This series is a working Draft set, compiled from internal product and engineering discussion. Figures, splits, and parameter defaults are subject to revision as the protocol and business model mature — see each PIP's own Status field for its individual state.

## Copyright and licence

Copyright © 2026 Entropy Tech Ltd.

The PIPs are licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/). Porto names, logos, and other trademarks are not licensed under this licence.
