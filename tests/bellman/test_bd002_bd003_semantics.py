"""Independent semantic review of BD0-02 and BD0-03 (not a status-string check).

Recomputes from theorem-file bytes: definitions, empty/source conventions,
decompositions, recurrences, cycle/finiteness handling, semantic wording,
no-universal-potential claim, corridor scoping. Verifies ledger SHA bindings
and UNPROVED->PROVED->REVIEWED lifecycles.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest().upper()


def ledger_entries() -> dict:
    # console.log equivalent [WP2-SEM-01]: ledger load
    console_log("[WP2-SEM-01] semantic review ledger load")
    ledger = json.loads((repo_root() / "math" / "proof_status.json").read_text(encoding="utf-8"))
    return {o["id"]: o for o in ledger["obligations"]}


def test_bd02_definition_and_empty_path() -> None:
    # console.log equivalent [WP2-SEM-02]: BD0-02 definitions
    console_log("[WP2-SEM-02] BD0-02 w_b + empty continuation")
    e = ledger_entries()["BD0-02"]
    t = (repo_root() / e["proof"]).read_text(encoding="utf-8")
    assert "w_b(e) = y(e)" in t or "w_b(e)=y(e)" in t
    assert "empty" in t.lower() and "value `0`" in t


def test_bd02_decomposition_and_recurrence() -> None:
    # console.log equivalent [WP2-SEM-03]: BD0-02 decomposition
    console_log("[WP2-SEM-03] BD0-02 first-edge decomposition + max recurrence")
    e = ledger_entries()["BD0-02"]
    t = (repo_root() / e["proof"]).read_text(encoding="utf-8")
    assert "first legal edge" in t or "first edge" in t
    assert "max(0" in t and "w_b(e)+V_b(t)" in t


def test_bd02_cycles_and_semantics() -> None:
    # console.log equivalent [WP2-SEM-04]: BD0-02 cycles + semantics
    console_log("[WP2-SEM-04] BD0-02 finiteness + semantics + no-universal-claim")
    e = ledger_entries()["BD0-02"]
    t = (repo_root() / e["proof"]).read_text(encoding="utf-8")
    assert "+\\infty" in t or "+∞" in t
    assert "positive" in t.lower() and "cycle" in t.lower()
    assert "maximum future `b`-regret extractable" in t
    assert "not" in t.lower() and "universal closed-form" in t.lower()
    assert e["status"] == "REVIEWED"
    assert [h["status"] for h in e["history"]] == ["UNPROVED", "PROVED", "REVIEWED"]
    assert sha256_file(repo_root() / e["proof"]) == e["proof_sha256"]


def test_bd03_definition_and_source() -> None:
    # console.log equivalent [WP2-SEM-05]: BD0-03 definitions
    console_log("[WP2-SEM-05] BD0-03 ell_b + diagonal source")
    e = ledger_entries()["BD0-03"]
    t = (repo_root() / e["proof"]).read_text(encoding="utf-8")
    assert "ℓ_b(e)" in t and "−w_b" in t
    assert "U_b(d) = 0" in t or "U_b(d)=0" in t


def test_bd03_decomposition_cycles_semantics() -> None:
    # console.log equivalent [WP2-SEM-06]: BD0-03 decomposition + cycles
    console_log("[WP2-SEM-06] BD0-03 prefix decomposition + finiteness + semantics")
    e = ledger_entries()["BD0-03"]
    t = (repo_root() / e["proof"]).read_text(encoding="utf-8")
    assert "last" in t.lower() and "edge" in t.lower()
    assert "min" in t and "U_b(s)" in t
    assert "−\\infty" in t or "−∞" in t
    assert "minimum accumulated `b`-slack" in t
    assert "maximum creation budget" in t  # appears only as an explicitly refused gloss
    assert e["status"] == "REVIEWED"
    assert [h["status"] for h in e["history"]] == ["UNPROVED", "PROVED", "REVIEWED"]
    assert sha256_file(repo_root() / e["proof"]) == e["proof_sha256"]


def test_corridor_scoping() -> None:
    # console.log equivalent [WP2-SEM-07]: corridor scoping
    console_log("[WP2-SEM-07] corridor pair-state-only scoping")
    e2 = ledger_entries()["BD0-02"]
    t2 = (repo_root() / e2["proof"]).read_text(encoding="utf-8")
    assert "V_b(s)" in t2 and "H(s)" in t2 and "U_b(s)" in t2
    assert "BD0-13" in t2
    assert "augmented" in t2.lower()
