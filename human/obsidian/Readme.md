---
id: doc_porto_landing_readme_md
type: document
---

# Readme

Kiln by Porto Labs The approved Kiln product website, built in the existing Gatsby application. Monument Grotesk, the close-up One introduction, native hardware carousel and a black Atelier interlude introduce private AI hardware and an agent-native OS. Register interest is the primary conversion. No deposits or pre-orders are collected. Development Validation The signup tests use controlled responses and send no.

## Connected knowledge

No outgoing links.

## Source content

# Kiln by Porto Labs

The approved Kiln product website, built in the existing Gatsby application. Monument Grotesk, the close-up One introduction, native hardware carousel and a black Atelier interlude introduce private AI hardware and an agent-native OS. Register interest is the primary conversion. No deposits or pre-orders are collected.

## Development

```sh
npm ci --legacy-peer-deps
npm run develop
```

## Validation

```sh
npm run build
node --test src/lib/*.test.mjs
git diff --check
```

The signup tests use controlled responses and send no real lead. They cover success, duplicate prevention, rejected responses, network failures, timeout and cleanup. The signup endpoint and Calendar destination are preserved from the previous production page. Provider-side delivery has not been verified with a real submission.

## Release

PR #5 targets `porto-labs-xyz/lander:staging`. Richard owns review, merge and the production-domain release. Source provenance and content boundaries are in `docs/CONTENT-SOURCES.md`.

## Structure

- `src/content/*.json`: trusted, versioned editorial markup for Home, About, Hardware, three product pages and Privacy.
- `src/components/MonumentPage.jsx`: Gatsby wrapper and effect lifecycle.
- `src/lib/monument.mjs`: native carousel, keyboard tabs, dialogs and menu.
- `src/lib/monument-arrival.mjs`: scroll-linked One opening and original Little Tilt cue, with reduced-motion and teardown support.
- `src/lib/enquiry-form.mjs`: Formspree registration/contact, explicit marketing consent, duplicate prevention and retry states.
- `src/styles/monument.css`, `product-pages.css`: current design; `booking.css` is scoped to the Calendar shell.
- `static/assets/`: current artwork and webfonts. Older components and assets remain in the repository but are not routed by the current pages.

Current release and integration validation: [release notes](docs/RELEASE-2026-11-14.md). Older motion/performance documents describe the superseded grille-animation implementation.
