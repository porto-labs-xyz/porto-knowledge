---
id: doc_pips_pip_1_md
type: document
---

# PIP-1: Process

What is a PIP? PIP stands for Porto Improvement Proposal. A PIP is a design document providing information to the Porto community, or describing a new feature for Porto, its Move modules, the Porto Chain protocol, or the Porto network's economic and operational surrounding it. The PIP should provide a concise technical specification of the feature and a rationale for it. The PIP author is responsible for building.

## Connected knowledge

No outgoing links.

## Source content

```
PIP: 1
Title: PIP Purpose, Process, and Format
Author: Richard Melkonian
Status: Living
Type: Meta
Created: 2026-09-09
```

## What is a PIP?

PIP stands for Porto Improvement Proposal. A PIP is a design document providing information to the Porto community, or describing a new feature for Porto, its Move modules, the Porto Chain protocol, or the Porto network's economic and operational surrounding it. The PIP should provide a concise technical specification of the feature and a rationale for it. The PIP author is responsible for building consensus within the community and documenting dissenting opinions.

This numbering scheme and document structure deliberately mirrors the Ethereum Improvement Proposal (EIP) process. Porto Chain is built on a stripped, detached fork of `aptos-core`, and its own protocol documentation borrows the RFC-style discipline of EIP/RFC processes for the same reason it reuses Aptos's consensus engine: this is a solved problem, and reinventing it would waste effort better spent on Porto's actual novelty — the accounting and payout logic described in [PIP-3](./PIP-3.md), [PIP-4](./PIP-4.md), and [PIP-5](./PIP-5.md).

## PIP Rationale

We intend PIPs to be the primary mechanism for proposing new features, for collecting community technical input on an issue, and for documenting the design decisions that have gone into Porto. Because PIPs are maintained as text files in a versioned directory, their revision history is the historical record of the feature proposal.

For Porto implementers, PIPs are a convenient way to track the progress of their implementation. Ideally, each implementation maintainer would list the PIPs that they have implemented. This will give end users a convenient way to know the current status of a given implementation or library.

## PIP Types

There are three types of PIP:

- **Standards Track PIP** describes any change that affects most or all Porto implementations, such as a change to the stream accounting protocol, PRT token mechanics, payout logic, or proposed application standards/conventions used by Porto clients. Standards Track PIPs consist of three parts: a design document, an implementation, and (for changes affecting consensus) an update to the on-chain Move modules. Standards Track PIPs are further broken down into:
  - **Core** — improvements requiring a change to Porto Chain consensus, the stream accounting protocol, the PRT token specification, or anything touching the interoperability of nodes (formerly known as "protocol" PIPs).
  - **Interface** — includes improvements around client API/RPC specifications and standards, and certain language-level standards like method names and streaming-gateway API conventions. The label "interface" aligns with the corresponding Aptos SDK category.
  - **Application** — application-level standards and conventions, including artist/rights-holder metadata conventions, wallet integration patterns, and third-party API conventions.
- **Meta PIP** describes a process surrounding Porto or proposes a change to (or an event in) a process. Meta PIPs are like Standards Track PIPs but apply to areas other than the Porto protocol itself. They may propose an implementation, but not to Porto's codebase; they often require community consensus. Unlike Informational PIPs, they are more than recommendations, and users are typically not free to ignore them. Examples include procedures, guidelines, changes to the decision-making process, and changes to the tools or environment used in Porto development. This document (PIP-1) is a Meta PIP.
- **Informational PIP** describes a Porto design issue, or provides general guidelines or information to the Porto community, but does not propose a new feature. Informational PIPs do not necessarily represent Porto community consensus or a recommendation, so users and implementers are free to ignore Informational PIPs or follow their advice. [PIP-2](./PIP-2.md) (the network overview) is an Informational PIP.

It is highly recommended that a single PIP contain a single key proposal or new idea. The more focused the PIP, the more successful it tends to be.

## PIP Status Terms

- **Idea** — an idea that is pre-draft. This is not tracked within this repository.
- **Draft** — the first formally tracked stage of a PIP in development. A PIP is merged by a PIP editor into this repository once properly formatted.
- **Review** — a PIP author marks a PIP as ready for and requesting peer review.
- **Last Call** — the final review window for a PIP before moving to Final. A PIP editor will assign Last Call status and set a review end date, typically 14 days later.
- **Final** — this PIP represents the final, standard specification. A Final PIP exists in a state of finality and should only be updated to correct errata and add non-normative clarifications.
- **Stagnant** — any PIP in Draft or Review that has been inactive for six months or greater is moved to Stagnant. A PIP may be resurrected from this state by Authors or PIP editors.
- **Withdrawn** — the PIP author(s) have withdrawn the proposed PIP. This state has finality and cannot be resurrected using the same PIP number.
- **Living** — a special status for PIPs designed to be continually updated and not reach a state of finality. This includes, most notably, PIP-1.

## PIP Header Preamble

Each PIP must begin with an RFC-822-style header preamble, preceded and followed by a code fence, containing the following fields in the given order:

- `PIP` — the PIP number.
- `Title` — the PIP title, a few words, not a complete sentence.
- `Author` — a list of the names and, optionally, contact information for all the authors/owners of the PIP.
- `Status` — one of `Draft`, `Review`, `Last Call`, `Final`, `Stagnant`, `Withdrawn`, `Living`.
- `Type` — one of `Standards Track` (`Core`, `Interface`, `Application`), `Meta`, or `Informational`.
- `Created` — the date the PIP was assigned.
- `Requires` (optional) — a PIP number that this PIP depends on.

## Numbering Convention

Porto reserves the following ranges to keep related proposals grouped, in the same spirit as Ethereum's `ERC-20`-style community numbering, but applied prospectively rather than by convention-after-the-fact:

| Range | Reserved for |
|---|---|
| 1–9 | Meta and process |
| 10–19 | Informational / network overview |
| 20–29 | Token standards (PRT and any future fungible/non-fungible standards) |
| 30–39 | Stream accounting, attestation, and content protocols |
| 40–49 | Node operator, staking, and network-role standards |
| 50–59 | Governance and protocol-parameter standards |
| 60+ | Reserved for future use |

The current PIP series does not yet require the full range and is numbered sequentially from PIP-1 for simplicity; the reserved ranges above are declared now so that future proposals can be slotted in without renumbering existing, Final documents.

## Copyright

Copyright © 2026 Entropy Tech Ltd.

This document is licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
Porto names, logos, and other trademarks are not licensed under this license.
