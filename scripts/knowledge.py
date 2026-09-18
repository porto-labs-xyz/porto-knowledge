#!/usr/bin/env python3
"""Deterministic agent retrieval over Porto's generated property graph."""

import argparse
import json
import re
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "graph" / "knowledge-graph.json"


def graph():
    if not GRAPH.exists():
        raise SystemExit("Graph missing. Run scripts/refresh.py --workspace <porto-workspace> first.")
    return json.loads(GRAPH.read_text(encoding="utf-8"))


def words(value):
    return {w for w in re.findall(r"[a-z0-9]+", value.lower()) if len(w) > 1}


def resolve(g, value):
    by_id = {n["id"]: n for n in g["nodes"]}
    if value in by_id:
        return by_id[value]
    found = [n for n in g["nodes"] if n["label"].casefold() == value.casefold()]
    if len(found) == 1:
        return found[0]
    raise SystemExit(f"Unknown or ambiguous node: {value}")


def print_json(value):
    print(json.dumps(value, indent=2, ensure_ascii=False))


def compact(node):
    """Keep query results useful without dumping the whole source corpus."""
    return {key: value for key, value in node.items() if key != "content"}


def search(g, query, limit):
    terms = words(query)
    rows = []
    for n in g["nodes"]:
        haystack = " ".join([n.get("label", ""), n.get("description", ""), " ".join(n.get("aliases", [])), n.get("content") or ""])
        matched = terms & words(haystack)
        if matched:
            score = len(matched) * 10 + (5 if query.casefold() in haystack.casefold() else 0)
            rows.append({"score": score, "id": n["id"], "type": n["type"], "label": n["label"],
                         "source_path": n.get("source_path"), "authority": n.get("authority"),
                         "description": n.get("description")})
    return sorted(rows, key=lambda x: (-x["score"], x["label"]))[:limit]


def traverse(g, start, depth, relation, direction):
    root = resolve(g, start)
    edges = g["edges"]
    queue, seen, result = deque([(root["id"], 0)]), {root["id"]}, []
    while queue:
        current, distance = queue.popleft()
        if distance >= depth:
            continue
        for edge in edges:
            if relation and edge["relation"] != relation:
                continue
            if direction in ("out", "both") and edge["source"] == current:
                nxt = edge["target"]
            elif direction in ("in", "both") and edge["target"] == current:
                nxt = edge["source"]
            else:
                continue
            result.append({**edge, "depth": distance + 1})
            if nxt not in seen:
                seen.add(nxt); queue.append((nxt, distance + 1))
    by_id = {n["id"]: n for n in g["nodes"]}
    return {"start": compact(root), "nodes": [compact(by_id[n]) for n in seen], "edges": result}


def route(g, route_id):
    node = resolve(g, "route_" + route_id if not route_id.startswith("route_") else route_id)
    starts = [e["target"] for e in g["edges"] if e["source"] == node["id"] and e["relation"] == "starts_with"]
    by_id = {n["id"]: n for n in g["nodes"]}
    return {"route": compact(node), "start_nodes": [compact(by_id[n]) for n in starts], "next": "Traverse one or two typed hops, then read cited source documents."}


def impact(g, source_path):
    doc = next((n for n in g["nodes"] if n.get("source_path") == source_path), None)
    if not doc:
        raise SystemExit(f"No declared source: {source_path}")
    result = traverse(g, doc["id"], 3, None, "both")
    result["review_instruction"] = "Review every connected public copy, documentation mirror, design route and concept before publishing the source change."
    return result


def check(g):
    ids = {n["id"] for n in g["nodes"]}
    assert len(ids) == len(g["nodes"]), "duplicate node id"
    assert g.get("directed") is True, "graph must be directed"
    assert all(e["source"] in ids and e["target"] in ids for e in g["edges"]), "orphan edge"
    assert all(n.get("description") for n in g["nodes"]), "description missing"
    assert all(not (n["type"] == "document" and n.get("classification") == "restricted_metadata_only" and n.get("content")) for n in g["nodes"]), "restricted source materialised"
    assert not g.get("missing_allowlisted_sources"), "missing allowlisted source"
    print(f"OK: {len(g['nodes'])} nodes, {len(g['edges'])} directed edges, no restricted content materialised.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("search"); p.add_argument("query"); p.add_argument("--limit", type=int, default=10)
    p = sub.add_parser("traverse"); p.add_argument("node"); p.add_argument("--depth", type=int, default=2); p.add_argument("--relation"); p.add_argument("--direction", choices=("out", "in", "both"), default="out")
    p = sub.add_parser("route"); p.add_argument("route")
    p = sub.add_parser("impact"); p.add_argument("source_path")
    sub.add_parser("check")
    args = parser.parse_args(); g = graph()
    if args.command == "search": result = search(g, args.query, args.limit)
    elif args.command == "traverse": result = traverse(g, args.node, args.depth, args.relation, args.direction)
    elif args.command == "route": result = route(g, args.route)
    elif args.command == "impact": result = impact(g, args.source_path)
    else: return check(g)
    print_json(result)


if __name__ == "__main__":
    main()
