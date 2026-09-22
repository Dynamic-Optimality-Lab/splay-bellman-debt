"""Independent audit for BD0-04/05: byte-level review outside pytest."""
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
    # console.log equivalent [WP3-RAU04-01]: review start
    console_log("[WP3-RAU04-01] BD0-04/05 audit start")
    ledger = json.loads((root / "math" / "proof_status.json").read_text(encoding="utf-8"))
    entries = {o["id"]: o for o in ledger["obligations"]}
    out = {}
    for bid in ("BD0-04", "BD0-05"):
        e = entries[bid]
        text = (root / e["proof"]).read_text(encoding="utf-8")
        out[bid] = {
            "exists": (root / e["proof"]).is_file(),
            "sha": sha256_file(root / e["proof"]) == e["proof_sha256"],
            "reviewed": e["status"] == "REVIEWED",
            "lifecycle": [h["status"] for h in e.get("history", [])] == ["UNPROVED", "PROVED", "REVIEWED"],
            "no_finite_premise": ("n <=" not in text and "n≤" not in text),
            "finite_tables_not_premise": ("never a premise" in text or "No finite" in text),
        }
    audit = json.loads((root / "artifacts" / "v02" / "kernels" / "transport_audit.json").read_text())
    out["transport"] = (audit["BD0-04"]["verdict"] == "V_TRANSPORT_APPLICABLE"
                        and audit["BD0-05"]["verdict"] == "U_TRANSPORT_BLOCKED_BY_SOURCE_CONTRACT")
    # console.log equivalent [WP3-RAU04-02]: review done
    console_log(f"[WP3-RAU04-02] BD0-04/05 audit done: {out}")
    for bid in ("BD0-04", "BD0-05"):
        assert all(out[bid].values()), (bid, out[bid])
    assert out["transport"]
    return out
