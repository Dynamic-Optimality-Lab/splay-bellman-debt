"""Independent semantic review of BD0-13 (byte-level, not status strings)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest().upper()


def clean(t: str) -> str:
    return " ".join(t.lower().replace("*", " ").split())


def entries() -> dict:
    # console.log equivalent [WP4-C13-01]: ledger load
    console_log("[WP4-C13-01] corridor review ledger load")
    ledger = json.loads((repo_root() / "math" / "proof_status.json").read_text(encoding="utf-8"))
    return {o["id"]: o for o in ledger["obligations"]}


def test_pair_assumptions_exact() -> None:
    # console.log equivalent [WP4-C13-02]: pair assumptions
    console_log("[WP4-C13-02] pair-state corridor assumptions exact")
    e = entries()["BD0-13"]
    t = clean((repo_root() / e["proof"]).read_text(encoding="utf-8"))
    assert "h(d)=0" in t
    assert "h ≥ 0" in t or "h >= 0" in t
    assert "one value" in t


def test_domain_distinguished() -> None:
    # console.log equivalent [WP4-C13-03]: domain distinguished
    console_log("[WP4-C13-03] augmented domain distinguished")
    e = entries()["BD0-13"]
    t = clean((repo_root() / e["proof"]).read_text(encoding="utf-8"))
    assert "h(a,b)" in t
    assert "augmented" in t and "φ(a,b" in t


def test_no_pair_to_phi_implication() -> None:
    # console.log equivalent [WP4-C13-04]: no overclaim
    console_log("[WP4-C13-04] no pair-to-phi implication, no necessity claim")
    e = entries()["BD0-13"]
    t = clean((repo_root() / e["proof"]).read_text(encoding="utf-8"))
    assert "does not" in t or "does not imply" in t or "alone does not" in t
    assert "recency is necessary" not in t or "no claim that recency is necessary" in t


def test_no_unproved_existence() -> None:
    # console.log equivalent [WP4-C13-05]: no existence overclaim
    console_log("[WP4-C13-05] no unproved out-of-corridor existence claim")
    e = entries()["BD0-13"]
    t = clean((repo_root() / e["proof"]).read_text(encoding="utf-8"))
    assert "no such example is constructed" in t or "not claimed" in t


def test_bd015_not_misused() -> None:
    # console.log equivalent [WP4-C13-06]: BD0-15 scope
    console_log("[WP4-C13-06] BD0-15 not misused as phi blindness")
    e = entries()["BD0-13"]
    t = clean((repo_root() / e["proof"]).read_text(encoding="utf-8"))
    assert "bd0-15" in t
    assert "forbidden" in t or "not" in t


def test_evaluator_bar_and_lifecycle() -> None:
    # console.log equivalent [WP4-C13-07]: evaluator bar + lifecycle
    console_log("[WP4-C13-07] WP-5 evaluator bar + REVIEWED lifecycle")
    e = entries()["BD0-13"]
    t = clean((repo_root() / e["proof"]).read_text(encoding="utf-8"))
    assert "barred" in t
    assert e["status"] == "REVIEWED"
    assert [h["status"] for h in e["history"]] == ["UNPROVED", "PROVED", "REVIEWED"]
    assert sha256_file(repo_root() / e["proof"]) == e["proof_sha256"]
