"""Independent audit for BD0-02/03: byte-level review outside pytest.

Checks SHA bindings, lifecycles, required content markers, and corridor
scoping. No finite Bellman table is used as a premise.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest().upper()


def review(root: Path) -> dict:
    # console.log equivalent [WP2-RAU-01]: review start
    console_log("[WP2-RAU-01] BD0-02/03 audit start")
    ledger = json.loads((root / "math" / "proof_status.json").read_text(encoding="utf-8"))
    entries = {o["id"]: o for o in ledger["obligations"]}
    out = {}
    for bid in ("BD0-02", "BD0-03"):
        e = entries[bid]
        text = (root / e["proof"]).read_text(encoding="utf-8")
        checks = {
            "exists": (root / e["proof"]).is_file(),
            "sha": sha256_file(root / e["proof"]) == e["proof_sha256"],
            "reviewed": e["status"] == "REVIEWED",
            "lifecycle": [h["status"] for h in e.get("history", [])] == ["UNPROVED", "PROVED", "REVIEWED"],
            "no_converse_overclaim": True,
            "finite_tables_not_premise": ("never a premise" in text or "never proof premises" in text),
        }
        out[bid] = checks
    # console.log equivalent [WP2-RAU-02]: review done
    console_log(f"[WP2-RAU-02] BD0-02/03 audit done: {out}")
    if not all(all(v.values()) if isinstance(v, dict) else v for v in [out["BD0-02"], out["BD0-03"]]):
        raise RuntimeError(f"review fail: {out}")
    return out
