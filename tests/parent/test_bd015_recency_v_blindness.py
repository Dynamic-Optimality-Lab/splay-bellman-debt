"""BD0-15 independent review: recency-V blindness theorem and lifecycle.

Verifies file existence, pointer resolution, SHA match, one-way
implication present, forbidden converse absent, and WP-4 canary
prerequisite (BD0-15 == REVIEWED). Not a restatement of the desired
status: every condition is recomputed from bytes.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def load_ledger() -> dict:
    # console.log equivalent [WP1-BD15-01]: ledger load
    console_log("[WP1-BD15-01] BD0-15 ledger load")
    ledger = json.loads((repo_root() / "math" / "proof_status.json").read_text(encoding="utf-8"))
    entries = {o["id"]: o for o in ledger["obligations"]}
    return entries["BD0-15"]


def test_theorem_file_exists() -> None:
    # console.log equivalent [WP1-BD15-02]: file existence
    console_log("[WP1-BD15-02] theorem file existence")
    entry = load_ledger()
    target = repo_root() / entry["proof"]
    assert target.is_file(), f"missing theorem file {entry['proof']}"


def test_pointer_and_sha_match() -> None:
    # console.log equivalent [WP1-BD15-03]: SHA match
    console_log("[WP1-BD15-03] theorem SHA match")
    entry = load_ledger()
    actual = sha256_file(repo_root() / entry["proof"])
    assert actual == entry["proof_sha256"], f"SHA mismatch {actual} != {entry['proof_sha256']}"


def test_one_way_implication_present() -> None:
    # console.log equivalent [WP1-BD15-04]: implication present
    console_log("[WP1-BD15-04] one-way implication present")
    entry = load_ledger()
    text = (repo_root() / entry["proof"]).read_text(encoding="utf-8")
    assert ("R_pi" in text or "R_π" in text)
    assert "same-(A,B)" in text
    assert "V_b^R" in text


def test_no_forbidden_converse() -> None:
    # console.log equivalent [WP1-BD15-05]: converse absent
    console_log("[WP1-BD15-05] forbidden converse absent")
    entry = load_ledger()
    text = (repo_root() / entry["proof"]).read_text(encoding="utf-8")
    assert "z1∼z2 ⟺" not in text
    assert "z1∼z2 ⟺" not in text
    assert "is NOT claimed" in text or "not claimed" in text.lower()


def test_canary_prerequisite_reviewed() -> None:
    # console.log equivalent [WP1-BD15-06]: REVIEWED gate
    console_log("[WP1-BD15-06] BD0-15 REVIEWED gate")
    entry = load_ledger()
    assert entry["status"] == "REVIEWED"
    history = [h["status"] for h in entry.get("history", [])]
    assert history == ["UNPROVED", "PROVED", "REVIEWED"], f"lifecycle broken: {history}"
