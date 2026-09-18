---
id: doc_docs_docs_pips_index_md
type: document
---

# Index

--- id: "index" title: "Porto Improvement Proposals" slug: "/pips" --- Porto Improvement Proposals (PIPs) PIPs are the design documents for the Porto protocol — Porto Chain, the PRT token, stream accounting, payouts, node operation, and governance — written in an EIP/RFC-style format. See [PIP-1](/pips/pip-1) for the full process, PIP types, and status lifecycle. Start with [PIP-2](/pips/pip-2) for the non-technical.

## Connected knowledge

No outgoing links.

## Source content

---
id: "index"
title: "Porto Improvement Proposals"
slug: "/pips"
---

# Porto Improvement Proposals (PIPs)

PIPs are the design documents for the Porto protocol — Porto Chain, the PRT token, stream accounting, payouts, node operation, and governance — written in an EIP/RFC-style format. See [PIP-1](/pips/pip-1) for the full process, PIP types, and status lifecycle.

Start with [PIP-2](/pips/pip-2) for the non-technical overview (the problem, the solution, and how the rest of this series fits together) before reading the Standards Track specifications.

## Index

| PIP | Title | Type | Status |
|---|---|---|---|
| [1](/pips/pip-1) | PIP Purpose, Process, and Format | Meta | Living |
| [2](/pips/pip-2) | Porto Network Overview | Informational | Draft |
| [3](/pips/pip-3) | PRT Fungible Asset & Issuance Standard | Standards Track (Core) | Draft |
| [4](/pips/pip-4) | Stream Accounting & Attestation Protocol | Standards Track (Core) | Draft |
| [5](/pips/pip-5) | Payout Splitter Module | Standards Track (Core) | Draft |
| [6](/pips/pip-6) | Node Operator Registration, Roles & Staking | Standards Track (Core) | Draft |
| [7](/pips/pip-7) | Governance Parameters & Upgrade Process | Standards Track (Core) | Draft |

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

See [PIP-1 §Numbering Convention](/pips/pip-1#numbering-convention) for reserved ranges (Meta, Informational, Token, Stream/Attestation, Node/Staking, Governance) for future proposals.

## Status

This series is a working Draft set, compiled from internal product and engineering discussion. Figures, splits, and parameter defaults are subject to revision as the protocol and business model mature — see each PIP's own Status field for its individual state.

## Copyright and licence

Copyright © 2026 Entropy Tech Ltd.

The PIPs are licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/). Porto names, logos, and other trademarks are not licensed under this licence.

