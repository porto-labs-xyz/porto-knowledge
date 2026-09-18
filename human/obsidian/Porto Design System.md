---
id: doc_porto_design_system_readme_md
type: document
---

# Porto Design System

Porto Design System Release 0.1.0-dev.1, prepared for native Figma implementation. Porto is streaming infrastructure for artists and record labels. This package is the released companion to an editable Figma library. It is deliberately portable: restricted decks, biographies, valuation material and machine-specific source paths are excluded. What is in the release - tokens/porto.tokens.json: primitive and semantic.

## Connected knowledge

- describes: [[Released Porto Design System]] (EXTRACTED)

## Source content

# Porto Design System

Release `0.1.0-dev.1`, prepared for native Figma implementation.

Porto is streaming infrastructure for artists and record labels. This package is the released companion to an editable Figma library. It is deliberately portable: restricted decks, biographies, valuation material and machine-specific source paths are excluded.

## What is in the release

- `tokens/porto.tokens.json`: primitive and semantic tokens for the three expression modes.
- `assets/approved/`: curated approved marks, architectural studies and player artwork.
- `specifications/`: component, chart, accessibility, content and governance rules.
- `templates/`: frame inventory and layout requirements for slides, documents and marketing.
- `examples/`: realistic public-safe briefs and copy.
- `figma/`: import order, release manifest and node-ID registry to fill only after Figma verification.
- `skills/porto-design-system/`: a bounded agent skill for using a released system.

## Release contract

Figma is the editable source for components, variables and layout masters. This repository is the traceable release record. A package change does not update Figma automatically. Each release must name a Figma version, file key, inspected nodes and exported evidence in `figma/release-manifest.json`.

Current status: local package complete for import; native Figma creation is blocked by the account sign-in screen. Do not claim this development release is a Figma library until the Figma fields in the release manifest are verified.

## Reading order

1. `PLAN.md`, then `STATUS.md`.
2. `specifications/foundations.md` and `specifications/components.md`.
3. Select a frame in `templates/` for the required medium.
4. Use the released asset registry, then run `validation/release-checklist.md`.

## Source boundary

Visual direction is derived from the current private deck audit and the live landing source. Product mechanics are verified against `whitepaper/porto-whitepaper.md`, `pips/PIP-5.md` and `pips/PIP-8.md`. The deck is not used as proof of protocol mechanics. Editorial Light is a proposed extension, pending review. Legal Plain is a neutral presentation convention, not legal advice or an agreement template.


