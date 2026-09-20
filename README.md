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
