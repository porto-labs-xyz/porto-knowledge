#!/usr/bin/env python3
"""Request a refresh after an authoritative Porto source changes."""

import argparse
import json
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("source_path", help="Manifest-declared path, e.g. pips/PIP-5.md")
args = parser.parse_args()
payload = json.dumps({"event_type": "porto-source-changed", "client_payload": {"source_path": args.source_path}})
subprocess.run(["gh", "api", "repos/porto-labs-xyz/porto-knowledge/dispatches", "--method", "POST", "--input", "-"], input=payload, text=True, check=True)
print(f"Requested Porto Knowledge refresh for {args.source_path}.")
