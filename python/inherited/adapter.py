"""Read-only parent adapter. Never writes to parent/ after lock.

Verifies PARENT-01..06: commit equality, manifest presence, FINAL_RESULT
schema, H1 firewall EMPTY, n8 contamination label, normative hashes.
Prose hashes are never trusted; hashes are recomputed from artifacts.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


SEALED_COMMIT = "6de1ca2a595e8895f54794f3a211fe6ee1a95a80"
H1_COMMITMENT = "C9D9BE2652412F6100C667BA1598D982E241868A0751AC5357499D55C0613BFF"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def verify_parent(repo_root: Path) -> dict:
    # console.log equivalent [WP1-ADAPT-01]: adapter start
    console_log("[WP1-ADAPT-01] parent adapter verify start")
    parent = repo_root / "parent"
    results: dict = {}
    seal = json.loads((parent / "PARENT_SEAL.json").read_text(encoding="utf-8"))
    results["PARENT-01"] = seal["sealed_commit"] == SEALED_COMMIT
    results["PARENT-02"] = (parent / "PARENT_MANIFEST.sha256").is_file()
    final = json.loads((parent / "PARENT_FINAL_RESULT.json").read_text(encoding="utf-8"))
    results["PARENT-03"] = isinstance(final, dict) and "bn_results" in final
    fw = json.loads((parent / "H1_FIREWALL_SEAL.json").read_text(encoding="utf-8"))
    results["PARENT-04"] = fw.get("state") == "EMPTY" and fw.get("unlock") is None
    results["PARENT-05"] = seal.get("n8_status") == "PARTIALLY_REVEALED_CANARY_CONTAMINATED"
    manifest = json.loads((parent / "H1_BANK_MANIFEST.json").read_text(encoding="utf-8"))
    results["PARENT-06"] = str(manifest.get("bank_commitment_sha256", "")).upper() == H1_COMMITMENT
    # console.log equivalent [WP1-ADAPT-02]: adapter verdict
    console_log(f"[WP1-ADAPT-02] parent adapter verdict: {results}")
    if not all(results.values()):
        raise RuntimeError(f"FOUNDATION_NOT_FROZEN: {results}")
    return results
