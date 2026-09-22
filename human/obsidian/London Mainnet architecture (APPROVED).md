---
id: concept_london_architecture
type: concept
---

# London Mainnet architecture (APPROVED)

APPROVED FOR LONDON 0.1.0. Product-owner-approved implementation scope, not deployment, security clearance or observed pilot evidence.

## Connected knowledge

- uses: [[London delivery evidence (APPROVED)|London delivery evidence (APPROVED)]] (INFERRED)
- requires_review: [[London governance departures (APPROVED)|London governance departures (APPROVED)]] (INFERRED)

## Source content

Source: docs/london-0.1.0/01-executive-architecture.md
## Approved architecture

London is a deliberately small music delivery and accounting network. Porto runs the catalogue, subscriptions, routing, accounting and payout coordination. Artists and other invited parties operate delivery nodes on infrastructure they control. Aptos supplies the external ledger for commitments and USDC transfers.

The shortest complete story is: **pay, listen through a participant node, record, commit, allocate, pay artists and operators, verify**. One bounded peer cache transfer makes the infrastructure experiment concrete without requiring a public peer-discovery network.

```mermaid
flowchart TB
  L[Paying listener] --> P[Porto web player]
  P --> N[Independent delivery node]
  A[Artist-owned node] -->|Authorised cache fill| N
  O[Private Porto origin] -->|Seed and fallback| A
  N -->|Signed receipt| B[Porto backend]
  B --> E[Retained evidence and accounting]
  E -->|Hashes| C[Aptos commitments]
  B -->|Reviewed USDC transfers| R[Artists and operators]
  R --> V[Statements and verifier]
  C --> V
```

Source: docs/london-0.1.0/01-executive-architecture.md
## Smallest implementation

One web application; one modular backend plus workers; PostgreSQL; private origin and evidence object storage; one containerised node package; one append-only Move commitment module; one payment-provider adapter and one treasury conversion adapter. A CLI is sufficient for catalogue import, operator admission, holds, run approval and exports. Do not build an admin product merely to avoid a documented manual operation.

[Contents](index.mdx) · [Implementation plan](16-implementation-plan.md) · [Launch inputs](17-open-decisions-and-risk-register.md)

Source: docs/london-0.1.0/25-node-package-and-pilot.md
## Pilot procedure

1. Invite a small cohort, targeting three to five independently operated nodes, including at least one artist and one unrelated third party. The minimum acceptance boundary is those two ownership categories, not a fabricated recruitment result.
2. Record ownership/control, who pays costs, onboarding time, assistance, licence/participation terms and any subsidy. Give operators a clear exit path.
3. Seed an authorised work onto artist node A. Keep B's selected chunks absent. Run a Porto-authorised A-to-B fill, verify source/destination evidence and ensure B serves at least one eligible real paid-listener session from those filled chunks.
4. Run real paid listening through participant nodes with Porto fallback available. Keep free/test/operator self-test sessions separately labelled and outside demand metrics and payable budgets.
5. Close accounting, anchor evidence, pay both rights and serving operators, deliver statements and have at least one external recipient verify their proof package.
6. Collect actual hosting/egress cost, time, earned reward, subsidy and willingness to continue. Observe at least one offered subscription renewal before claiming renewal evidence. Record the observation window before recruitment.

Source: docs/london-0.1.0/25-node-package-and-pilot.md
## Pilot report

Report invited/activated/retained operators by ownership type; actual peer-filled bytes; eligible independent delivery share versus fallback; successful playback/rebuffer; missing/rejected receipts; cost per eligible served hour; earned rewards versus subsidy and participant cost; cleared paying listeners, repeat listeners and renewal opportunities/outcomes; artist/operator confirmed payments; verifier outcomes; incidents and support effort.

Do not equate a working peer transfer with viable economics, willingness to sign up with retained participation, or subsidies with organic demand. The pilot may correctly conclude that the infrastructure works but participation economics need revision. That is useful evidence, not a reason to rewrite historical results.

[Contents](index.mdx) · [Implementation plan](16-implementation-plan.md) · [Launch inputs](17-open-decisions-and-risk-register.md)
