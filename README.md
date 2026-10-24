# Porto Knowledge

Public, source-grounded organisational knowledge for Porto. It gives people a
linked reading surface and gives agents a deterministic way to locate,
traverse and verify the material that applies to a task.

## Explore it

Open the private [Porto Knowledge Explorer](https://porto-knowledge.r-v-melkonian.chatgpt.site) for a searchable, clickable view of the current graph.

This repository is a knowledge projection, not a second product repository.
The source repositories remain authoritative. Every graph claim records the
source file, revision, classification and hash from which it was built.

## What it provides

- A directed property graph in `graph/knowledge-graph.json` and JSON-LD.
- `knowledge query`, a dependency-free search, route and traversal command for
  agents and scripts.
- A generated Obsidian vault and Graphviz overview for human exploration.
- Impact links: a changed source can identify the documentation, public copy,
  design assets and agent routes that need review.
- A public-safe source boundary. Restricted deck files, legal negotiations,
  biographies, credentials and machine-local paths are deliberately not copied
  here.

## Fast path for agents

```sh
python3 scripts/knowledge.py route marketing-deck
python3 scripts/knowledge.py search "daily artist settlement"
python3 scripts/knowledge.py traverse concept_epoch_settlement --depth 2
python3 scripts/knowledge.py impact pips/PIP-5.md
```

Search and traversal are for orientation. Read the cited source before making
a factual or public-facing claim. `INFERRED` links are navigation aids, never
authority.

## Refreshing

From a checkout beside the Porto workspace:

```sh
python3 scripts/refresh.py --workspace ../porto
python3 scripts/knowledge.py check
```

The refresh has no third-party runtime dependency. It reads only the declared
allowlist in `sources/manifest.json`, writes graph projections, and refuses to
materialise a source marked restricted. CI can refresh the graph from pinned
source revisions with the `PORTO_KNOWLEDGE_SOURCES_TOKEN` organisation secret.

## Source and privacy contract

The manifest is the source allowlist. Add an organisational source by declaring
its authority, owner, classification and materialisation policy first. Do not
add restricted private-deck content, negotiations, personal data, credentials,
or host paths. Private source repositories may contribute metadata only.

## Mandatory source registration and enrichment

For every authorised change to Porto knowledge, implementation, documentation or
operating guidance, complete this workflow before declaring the work finished:

1. **Always query and verify.** Search the graph first, traverse relevant links,
   and read the authoritative source. A missing or stale graph result is a reason
   to inspect the owning repository, not to invent evidence.
2. **Always establish a source.** If the relevant document exists but is missing
   from the graph, register it in `sources/manifest.json`. If no authoritative
   document exists, create a focused document in the owning repository describing
   the change, decision, evidence and unresolved limits, then register it. Reuse
   an appropriate existing source instead of creating duplicate documents. Include
   new source repositories in `repositories` and their documents in `documents`.
   Do not stop at recording a coverage gap when registration is possible within
   the authorised scope.
3. **Always classify before enriching.** Declare source authority, repository
   ownership, privacy classification and materialisation policy. Pin published
   source revisions where required. Private sources remain metadata-only in this
   projection; never copy restricted prose, logs, credentials or personal data.
4. **Always enrich meaning and relationships.** Connect the source to the relevant
   domain, concepts, decisions, implementation and agent routes in maintained
   curation. Add useful source-section pointers and permitted content. Preserve
   provenance and distinguish inferred links, proposed work, tested behaviour and
   deployed evidence. Registration alone is not completed enrichment.
5. **Always refresh and validate.** Run the full workspace enrichment pipeline,
   then verify both the local semantic graph and organisation graph, including
   semantic parity where supported. Never hand-edit generated graph or vault
   files. Confirm the changed source appears with current provenance and the
   correct content/privacy treatment; test search, traversal and `impact` for it.
6. **Always review impact and publish within scope.** Review connected concepts,
   documentation and public copy. Commit and push authorised source and curation
   changes on a scoped branch with a PR; do not merge without authorisation.
   After the registration and source revision are available to the target
   refresh workflow, notify it and verify its result. A dispatch is not proof
   that refresh succeeded, and a branch source is not a merged or deployed change.
7. **Always report unresolved work accurately.** If access, classification or an
   external dependency prevents completion, record the precise gap and report
   the blocked stage. Do not call enrichment complete while source registration,
   required refresh, validation or publication remains unresolved. Resolve the
   gap only after the corresponding checks pass.

In a local Porto workspace, run its `scripts/update-porto-knowledge-graph.sh`
pipeline, which includes organisation refresh and validation, rather than only
regenerating this projection. For this repository's standalone/CI refresh, use
`scripts/refresh.py` followed by `scripts/knowledge.py check`. Then verify the
registered source with `scripts/knowledge.py search`, `traverse` and `impact`.

## Repository layout

- `sources/manifest.json`: source policy and checkout mapping.
- `knowledge/curation.json`: domains, concepts, relations and agent routes.
- `graph/`: generated machine graph, JSON-LD and optional Neo4j Cypher export.
- `human/obsidian/`: generated human-facing notes and map.
- `scripts/`: refresh, query and validation tools.


## Player and style-guide route

Use `python3 scripts/knowledge.py route player-prototype`, then traverse `concept_player_prototype` with `--direction both --depth 2`. Read the returned source documents. The player repository is checked out as `listening-app` in the source workspace. The manifest includes its README, design integration, architecture and contribution workflow, plus the design-system style guide and Figma handoff.

Player concepts include meaningful public-safe descriptions and explicitly selected source-section pointers with revisions. Public source sections may include verified text; private player and design-system sections remain metadata only. Their content is never copied into the public graph. Missing headings in a materialised source stop enrichment. Typed relationships remain INFERRED navigation hints; the source documents establish implementation details and limitations.

Always traverse, enrich and build meaning: record decisions, connect implementation to design guidance, distinguish prototype simulation from network evidence, review impact and pass graph validation. CI refreshes graph, human notes and the explorer from public authoritative checkouts. Private repositories are linked by metadata and pinned revisions without requiring CI credentials.
