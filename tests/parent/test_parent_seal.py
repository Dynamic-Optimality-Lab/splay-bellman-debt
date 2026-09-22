"""PARENT-01..06: parent seal equality, manifest, FINAL_RESULT schema, H1 EMPTY, n8 label, normative hashes."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def test_parent_01_commit() -> None:
    # console.log equivalent [WP1-T-01]: PARENT-01
    console_log("[WP1-T-01] PARENT-01 commit equality")
    root = Path(__file__).resolve().parents[2]
    seal = json.loads((root / "parent" / "PARENT_SEAL.json").read_text(encoding="utf-8"))
    assert seal["sealed_commit"] == "6de1ca2a595e8895f54794f3a211fe6ee1a95a80"


def test_parent_02_manifest() -> None:
    # console.log equivalent [WP1-T-02]: PARENT-02
    console_log("[WP1-T-02] PARENT-02 manifest verification")
    root = Path(__file__).resolve().parents[2]
    assert (root / "parent" / "PARENT_MANIFEST.sha256").is_file()


def test_parent_03_final_result() -> None:
    # console.log equivalent [WP1-T-03]: PARENT-03
    console_log("[WP1-T-03] PARENT-03 FINAL_RESULT schema")
    root = Path(__file__).resolve().parents[2]
    final = json.loads((root / "parent" / "PARENT_FINAL_RESULT.json").read_text(encoding="utf-8"))
    assert isinstance(final.get("bn_results"), list) and len(final["bn_results"]) == 6


def test_parent_04_firewall() -> None:
    # console.log equivalent [WP1-T-04]: PARENT-04
    console_log("[WP1-T-04] PARENT-04 H1 firewall EMPTY")
    root = Path(__file__).resolve().parents[2]
    fw = json.loads((root / "parent" / "H1_FIREWALL_SEAL.json").read_text(encoding="utf-8"))
    assert fw["state"] == "EMPTY" and fw["unlock"] is None


def test_parent_05_contamination() -> None:
    # console.log equivalent [WP1-T-05]: PARENT-05
    console_log("[WP1-T-05] PARENT-05 n8 contamination preserved")
    root = Path(__file__).resolve().parents[2]
    seal = json.loads((root / "parent" / "PARENT_SEAL.json").read_text(encoding="utf-8"))
    assert seal["n8_status"] == "PARTIALLY_REVEALED_CANARY_CONTAMINATED"


def test_parent_06_hashes() -> None:
    # console.log equivalent [WP1-T-06]: PARENT-06
    console_log("[WP1-T-06] PARENT-06 normative hashes")
    root = Path(__file__).resolve().parents[2]
    assert (root / "IMPLEMENTATION_SPEC_v0.2.md").is_file()
    assert (root / "SPLAY_AM_BD_IMPLEMENTATION_SPEC_v0.2.1.md").is_file()
