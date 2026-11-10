---
id: doc_porto_landing_readme_md
type: document
---

# Readme

Kiln by Porto Labs A minimal, responsive stealth landing page for a creative system in development. The page follows the founder-linked Kiln Creative Studios deck, using paper, black, red, yellow, blue and monospaced headings and keeps two conversion paths: the email waitlist and /book/ appointment booking. Current copy, asset provenance and historical context are documented in [CLAUDE.md](CLAUDE.md) and.

## Connected knowledge

No outgoing links.

## Source content

# Kiln by Porto Labs

A minimal, responsive stealth landing page for a creative system in development. The page follows the founder-linked Kiln Creative Studios deck, using paper, black, red, yellow, blue and monospaced headings and keeps two conversion paths: the email waitlist and `/book/` appointment booking.

Current copy, asset provenance and historical context are documented in [CLAUDE.md](CLAUDE.md) and [docs/CONTENT-SOURCES.md](docs/CONTENT-SOURCES.md).

## Preserved version

The previous landing page is retained on `entropy-acs/landing-before-freq-stealth-2026-10-29`, at `b3df6f0`. The Kiln refresh lives on `entropy-acs/kiln-brand`. Existing October assets remain available for historical reference.

## Validation, 10 November 2026

Production build and diff checks passed. Browser review covered desktop and 390px mobile, with no horizontal overflow at 320px. Waitlist navigation, required email validation, conversion destinations and the booking page shell were checked. The signup handler and Calendar URL are unchanged from main. No live signup or appointment was submitted; Calendar availability was not verified.

## Historical validation, 29 October 2026

The production build passed. Browser checks covered 320px and 390px mobile, 768px tablet and desktop layouts, email validation, waitlist navigation and the Google Calendar embed. Controlled checks exercised the actual signup handler with successful, rejected, failed and timed-out requests, plus duplicate-submission prevention. No real email signup or appointment was submitted.

## Setup

```bash
npm install
```

## Development

```bash
npm run develop
```

Site runs at `http://localhost:8000`

## Build

```bash
npm run build
```

## Deploy

Deployment is manual and requires an explicit request. This refresh does not deploy automatically.

```bash
vercel --prod
```
