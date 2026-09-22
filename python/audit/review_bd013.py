"""Independent audit for BD0-13: byte-level review outside pytest."""
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
    # console.log equivalent [WP4-RAU13-01]: review start
    console_log("[WP4-RAU13-01] BD0-13 audit start")
    ledger = json.loads((root / "math" / "proof_status.json").read_text(encoding="utf-8"))
    e = {o["id"]: o for o in ledger["obligations"]}["BD0-13"]
    text = (root / e["proof"]).read_text(encoding="utf-8")
    out = {
        "exists": (root / e["proof"]).is_file(),
        "sha": sha256_file(root / e["proof"]) == e["proof_sha256"],
        "reviewed": e["status"] == "REVIEWED",
        "lifecycle": [h["status"] for h in e.get("history", [])] == ["UNPROVED", "PROVED", "REVIEWED"],
        "scope_only": "non-implication" in text.lower() or "alone does NOT imply" in text,
        "no_finite_premise": ("n <=" not in text and "n≤" not in text),
    }
    # console.log equivalent [WP4-RAU13-02]: review done
    console_log(f"[WP4-RAU13-02] BD0-13 audit done: {out}")
    assert all(out.values()), out
    return out
