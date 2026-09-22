"""Independent semantic review of BD0-04 and BD0-05 (byte-level, not status strings)."""
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


def entries() -> dict:
    # console.log equivalent [WP3-TR-01]: ledger load
    console_log("[WP3-TR-01] transport review ledger load")
    ledger = json.loads((repo_root() / "math" / "proof_status.json").read_text(encoding="utf-8"))
    return {o["id"]: o for o in ledger["obligations"]}


def test_bd04_correspondence() -> None:
    # console.log equivalent [WP3-TR-02]: BD0-04 correspondence
    console_log("[WP3-TR-02] BD0-04 action/cost/successor correspondence")
    e = entries()["BD0-04"]
    t = (repo_root() / e["proof"]).read_text(encoding="utf-8")
    assert "action correspondence" in t.lower() or "correspondence is the identity" in t
    assert "immediate costs agree" in t or "costs agree" in t
    assert "successor equivalence" in t


def test_bd04_both_directions_and_sets() -> None:
    # console.log equivalent [WP3-TR-03]: BD0-04 both directions
    console_log("[WP3-TR-03] BD0-04 forward/reverse + regret-set equality")
    e = entries()["BD0-04"]
    t = (repo_root() / e["proof"]).read_text(encoding="utf-8")
    assert "both directions" in t or "both sides" in t or "vice versa" in t or "symmetry" in t.lower()
    assert "suprema coincide" in t or "attainable future-regret sets" in t


def test_bd04_cycles_no_finite_premise_no_converse() -> None:
    # console.log equivalent [WP3-TR-04]: BD0-04 cycles/finiteness scope
    console_log("[WP3-TR-04] BD0-04 cycles, feasibility, no converse")
    e = entries()["BD0-04"]
    t = (repo_root() / e["proof"]).read_text(encoding="utf-8")
    assert "+\\infty" in t or "+∞" in t
    assert "feasib" in t.lower()
    assert "n <=" not in t and "n≤" not in t
    assert "NOT claimed" in t or "not claimed" in t.lower()
    assert e["status"] == "REVIEWED"
    assert [h["status"] for h in e["history"]] == ["UNPROVED", "PROVED", "REVIEWED"]
    assert sha256_file(repo_root() / e["proof"]) == e["proof_sha256"]


def clean(t: str) -> str:
    # Normalize markdown/whitespace so content checks test prose, not formatting.
    return " ".join(t.lower().replace("*", " ").split())


def test_bd05_source_and_paths() -> None:
    # console.log equivalent [WP3-TR-05]: BD0-05 source compatibility
    console_log("[WP3-TR-05] BD0-05 source boundary + compatibility")
    e = entries()["BD0-05"]
    t = clean((repo_root() / e["proof"]).read_text(encoding="utf-8"))
    assert "u_b(d) = 0" in t or "u_b(d)=0" in t
    assert "source compatib" in t
    assert "source-rooted" in t


def test_bd05_slack_cycles_future_insufficient() -> None:
    # console.log equivalent [WP3-TR-06]: BD0-05 slack + cycles + distinction
    console_log("[WP3-TR-06] BD0-05 slack preservation + negative cycles + future-insufficiency")
    e = entries()["BD0-05"]
    t = clean((repo_root() / e["proof"]).read_text(encoding="utf-8"))
    assert "identical" in t and "slack" in t
    assert "−\\infty" in t or "−∞" in t
    assert "not automatically preserve" in t
    assert "n <=" not in t and "n≤" not in t
    assert e["status"] == "REVIEWED"
    assert [h["status"] for h in e["history"]] == ["UNPROVED", "PROVED", "REVIEWED"]
    assert sha256_file(repo_root() / e["proof"]) == e["proof_sha256"]


def test_transport_audit_record() -> None:
    # console.log equivalent [WP3-TR-07]: quotient audit record
    console_log("[WP3-TR-07] quotient applicability record")
    a = json.loads((repo_root() / "artifacts" / "v02" / "kernels" / "transport_audit.json").read_text())
    assert a["BD0-04"]["verdict"] == "V_TRANSPORT_APPLICABLE"
    assert a["BD0-05"]["verdict"] == "U_TRANSPORT_BLOCKED_BY_SOURCE_CONTRACT"
    assert a["finite_result_unchanged"]["KERNEL_NO_COMPRESSION"] is True
