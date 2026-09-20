#!/usr/bin/env python3
"""Build Porto's private, source-grounded knowledge projections."""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(text):
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def redact(text):
    """Do not turn an internal graph into a directory of personal data or secrets."""
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "[redacted-email]", text)
    text = re.sub(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b", "[redacted-token]", text)
    return text


def git_revision(path):
    try:
        return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def excerpt(text, limit=420):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"[#*_`>|]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[:limit].rsplit(" ", 1)[0] + "."


def selected_section(text, heading):
    """Return an explicitly curated heading and its body, never guessed content."""
    matches = list(re.finditer(r"(?m)^(#{1,6}) +(.+?)\s*$", text))
    for i, match in enumerate(matches):
        if match.group(2).strip() == heading:
            end = next((m.start() for m in matches[i + 1:] if len(m.group(1)) <= len(match.group(1))), len(text))
            return text[match.start():end].strip()
    raise ValueError(f"Curated source heading is missing: {heading}")


def node_id(path):
    return "doc_" + re.sub(r"[^a-z0-9]+", "_", path.lower()).strip("_")


def add_edge(edges, source, relation, target, confidence="EXTRACTED", evidence=None):
    edges.append({"source": source, "relation": relation, "target": target,
                  "confidence": confidence, "evidence": evidence or {}})


def write_human(graph):
    vault = ROOT / "human" / "obsidian"
    vault.mkdir(parents=True, exist_ok=True)
    for old in vault.glob("*.md"):
        old.unlink()
    by_id = {n["id"]: n for n in graph["nodes"]}
    label_counts = {}
    for node in graph["nodes"]:
        key = node["label"].casefold()
        label_counts[key] = label_counts.get(key, 0) + 1
    note_names = {}
    for node in graph["nodes"]:
        safe = re.sub(r"[/:]", "-", node["label"])
        if label_counts[node["label"].casefold()] > 1:
            safe += f" ({node['type']})"
        note_names[node["id"]] = safe
    outgoing = {}
    for edge in graph["edges"]:
        outgoing.setdefault(edge["source"], []).append(edge)
    for node in graph["nodes"]:
        if node["type"] == "document" and not node.get("materialized"):
            content = "Source is restricted metadata only. Read it in its approved location."
        else:
            content = node.get("content") or node.get("description", "")
        links = []
        for edge in outgoing.get(node["id"], []):
            target = by_id[edge["target"]]
            links.append(f"- {edge['relation']}: [[{note_names[target['id']]}|{target['label']}]] ({edge['confidence']})")
        safe = note_names[node["id"]]
        (vault / f"{safe}.md").write_text(
            f"---\nid: {node['id']}\ntype: {node['type']}\n---\n\n# {node['label']}\n\n"
            f"{node.get('description', '')}\n\n## Connected knowledge\n\n"
            f"{'\n'.join(links) or 'No outgoing links.'}\n\n## Source content\n\n{content}\n", encoding="utf-8")
    (ROOT / "human" / "overview.dot").write_text(
        "digraph PortoKnowledge { rankdir=LR; node [shape=box, style=rounded];\n" +
        "\n".join(f'  "{e["source"]}" -> "{e["target"]}" [label="{e["relation"]}"];' for e in graph["edges"]) +
        "\n}\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    manifest, curation = load(ROOT / "sources/manifest.json"), load(ROOT / "knowledge/curation.json")
    repos = {r["id"]: r for r in manifest["repositories"]}
    nodes, edges, missing = [], [], []
    nodes.append({"id": "porto_knowledge", "type": "knowledge_base", "label": "Porto Knowledge",
                  "description": "Private, source-grounded organisational knowledge graph.", "coverage_status": "growing"})
    for key, data in curation["domains"].items():
        nid = f"domain_{key}"
        nodes.append({"id": nid, "type": "domain", "label": data["label"], "description": data["description"]})
        add_edge(edges, "porto_knowledge", "organizes", nid)
    docs = {d["path"]: d for d in manifest["documents"]}
    # Graphify all declared text sources, not just the hand-curated entry
    # points. Curated documents retain their stronger kind and domain mapping.
    default_domains = {"whitepaper": "mission_market", "pips": "governance_process", "docs": "knowledge_ops", "landing": "brand_public", "design-system": "design_system"}
    for repo in repos.values():
        for pattern in repo.get("discover", []):
            for path in (workspace / repo["workspace_path"]).glob(pattern):
                if not path.is_file() or any(part in {".git", "node_modules", "build", ".docusaurus", ".cache"} for part in path.parts):
                    continue
                relative = path.relative_to(workspace).as_posix()
                docs.setdefault(relative, {"path": relative, "source": repo["id"], "domain": default_domains[repo["id"]], "kind": "supporting", "title": path.stem.replace("-", " ").replace("_", " ").title()})
    for doc in sorted(docs.values(), key=lambda item: item["path"]):
        repo = repos[doc["source"]]
        source_path = workspace / doc["path"]
        exists = source_path.exists()
        materialized = bool(repo["materialize"] and exists)
        raw_text = source_path.read_text(encoding="utf-8", errors="replace") if materialized else ""
        text = redact(raw_text)
        if not exists and repo["materialize"]:
            missing.append(doc["path"])
        repo_root = workspace / repo["workspace_path"]
        nodes.append({
            "id": node_id(doc["path"]), "type": "document", "label": doc["title"],
            "description": excerpt(text) if text else f"{doc['kind'].replace('_', ' ')} source. {repo['classification']}.",
            "source_path": doc["path"], "source_repository": doc["source"], "authority": repo["authority"],
            "classification": repo["classification"], "kind": doc["kind"], "materialized": materialized,
            "source_hash": sha(raw_text) if raw_text else None, "source_revision": repo.get("source_revision") or git_revision(repo_root),
            "content": text if materialized else None
        })
        add_edge(edges, f"domain_{doc['domain']}", "contains_source", node_id(doc["path"]), evidence={"source_path": doc["path"]})
    for cid, concept in curation["concepts"].items():
        nodes.append({"id": cid, "type": "concept", "label": concept["label"],
                      "description": concept.get("description", f"{concept['label']} is a curated Porto concept."), "aliases": concept["aliases"],
                      "authority": "source_grounded", "temporal_scope": "verify_source"})
        details = []
        by_path = {n.get("source_path"): n for n in nodes if n["type"] == "document"}
        for path, headings in concept.get("source_sections", {}).items():
            if path not in concept["sources"]:
                raise ValueError(f"Concept section is not connected to its source: {cid}: {path}")
            document = by_path[path]
            if not document.get("materialized"):
                # Preserve a useful source pointer without copying private prose.
                for heading in headings:
                    details.append({"source_path": path, "heading": heading,
                                    "source_hash": None, "source_revision": document["source_revision"],
                                    "authority": document["authority"], "availability": "restricted_metadata_only"})
                continue
            for heading in headings:
                details.append({"source_path": path, "heading": heading,
                                "source_hash": document["source_hash"], "source_revision": document["source_revision"],
                                "authority": document["authority"],
                                "content": selected_section(document["content"], heading)})
        if details:
            nodes[-1]["source_details"] = details
            nodes[-1]["content"] = "\n\n".join(f"Source: {d['source_path']}\n{d.get('content') or (d['heading'] + chr(10) + 'Private source: section pointer only. Read in its approved repository.')}" for d in details)
        add_edge(edges, f"domain_{concept['domain']}", "contains", cid)
        for path in concept["sources"]:
            if path in docs:
                add_edge(edges, node_id(path), "describes", cid, evidence={"source_path": path})
    for source, relation, target in curation["relations"]:
        add_edge(edges, source, relation, target, "INFERRED", {"note": "Curated traversal relation, verify against cited source."})
    for route_id, route in curation["routes"].items():
        nid = f"route_{route_id}"
        nodes.append({"id": nid, "type": "agent_route", "label": route["label"], "description": route["instruction"]})
        add_edge(edges, "domain_knowledge_ops", "provides_route", nid)
        for target in route["start"]:
            add_edge(edges, nid, "starts_with", target)
    graph = {"schema_version": 1, "directed": True, "generated_at": datetime.now(timezone.utc).isoformat(),
             "workspace_fingerprint": sha(str(workspace)), "missing_allowlisted_sources": missing,
             "nodes": nodes, "edges": edges}
    graph_dir = ROOT / "graph"
    graph_dir.mkdir(exist_ok=True)
    (graph_dir / "knowledge-graph.json").write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    jsonld = {"@context": {"id": "@id", "type": "@type", "relation": "https://porto.labs/knowledge/relation"}, "@graph": nodes + edges}
    (graph_dir / "knowledge-graph.jsonld").write_text(json.dumps(jsonld, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    cypher = "\n".join(
        "MERGE (n:Node {id: " + json.dumps(n["id"]) + "}) SET n += " +
        json.dumps({k: v for k, v in n.items() if k != "content"}) + ";"
        for n in nodes
    )
    (graph_dir / "neo4j.cypher").write_text(cypher + "\n", encoding="utf-8")
    write_human(graph)
    # Keep a dependency-free static build alongside the graph. The explorer
    # deliberately loads the same generated JSON that agents query.
    dist = ROOT / "dist"
    (dist / "data").mkdir(parents=True, exist_ok=True)
    explorer = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    # Private Site authentication applies separately to static subrequests.
    # Embed the redacted graph to keep the viewer reliably self-contained.
    safe_graph = json.dumps(graph, ensure_ascii=False).replace("<", "\\u003c")
    explorer = explorer.replace("<!-- GRAPH_DATA -->", f'<script id="graph-data" type="application/json">{safe_graph}</script>')
    (dist / "index.html").write_text(explorer, encoding="utf-8")
    shutil.copy2(graph_dir / "knowledge-graph.json", dist / "data" / "knowledge-graph.json")
    print(f"Built {len(nodes)} nodes and {len(edges)} edges; materialised {sum(1 for n in nodes if n.get('materialized'))} sources.")
    if missing:
        print("Missing allowlisted sources: " + ", ".join(missing))


if __name__ == "__main__":
    main()
