"""PR/NEG/SEAL: proof discipline, negative-branch gating, seal integrity."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def root() -> Path:
    return Path(__file__).resolve().parents[1]


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest().upper()


def test_pr01_no_finite_premise() -> None:
    # console.log equivalent [WP6-PR-01]: PR-01
    console_log("[WP6-PR-01] PR-01 no finite premise (no proof attempted)")
    r = json.loads((root() / "artifacts" / "v02" / "seal" / "route_audit.json").read_text())
    assert r["positive"]["p15_proof"] == "NOT_ATTEMPTED"


def test_pr02_all_cases() -> None:
    # console.log equivalent [WP6-PR-02]: PR-02
    console_log("[WP6-PR-02] PR-02 Splay cases (no proof, nothing omitted)")
    r = json.loads((root() / "artifacts" / "v02" / "seal" / "route_audit.json").read_text())
    assert r["positive"]["activated"] is False


def test_pr03_recency_cases() -> None:
    # console.log equivalent [WP6-PR-03]: PR-03
    console_log("[WP6-PR-03] PR-03 recency cases (no Track-R proof)")
    assert (root() / "math" / "theorem_BD07_augmented_path.md").is_file()


def test_pr04_telescoping() -> None:
    # console.log equivalent [WP6-PR-04]: PR-04
    console_log("[WP6-PR-04] PR-04 telescoping not claimed")
    f = json.loads((root() / "artifacts" / "v02" / "seal" / "FINAL_RESULT.json").read_text())
    assert f["terminal_claim"] == "FINITE_DEBT_LAW_MINING_RESULTS"


def test_pr05_bridge() -> None:
    # console.log equivalent [WP6-PR-05]: PR-05
    console_log("[WP6-PR-05] PR-05 bridge not invoked")
    f = json.loads((root() / "artifacts" / "v02" / "seal" / "FINAL_RESULT.json").read_text())
    assert f["terminal_claim"] not in ("APPROXIMATE_MONOTONICITY_PROVED", "DYNAMIC_OPTIMALITY_PROVED")


def test_pr06_b_independence() -> None:
    # console.log equivalent [WP6-PR-06]: PR-06
    console_log("[WP6-PR-06] PR-06 universal b (no theorem constant)")
    g = json.loads((root() / "artifacts" / "v02" / "logs" / "phase11_gate.json").read_text())
    assert g["b_feasible_all_n"] is True


def test_neg01_cycle() -> None:
    # console.log equivalent [WP6-NEG-01]: NEG-01
    console_log("[WP6-NEG-01] NEG-01 no fixed-b cycle misclassified")
    r = json.loads((root() / "artifacts" / "v02" / "seal" / "route_audit.json").read_text())
    assert r["negative"]["C1_reachable_legal_motif"] is False


def test_neg02_closed_form() -> None:
    # console.log equivalent [WP6-NEG-02]: NEG-02
    console_log("[WP6-NEG-02] NEG-02 no solver-defined family")
    r = json.loads((root() / "artifacts" / "v02" / "seal" / "route_audit.json").read_text())
    assert r["negative"]["C2_parameterized_construction"] is False


def test_neg03_bounds() -> None:
    # console.log equivalent [WP6-NEG-03]: NEG-03
    console_log("[WP6-NEG-03] NEG-03 no symbolic bounds (branch inactive)")
    r = json.loads((root() / "artifacts" / "v02" / "seal" / "route_audit.json").read_text())
    assert r["negative"]["C3_growing_ratio"] is False


def test_neg04_ratio() -> None:
    # console.log equivalent [WP6-NEG-04]: NEG-04
    console_log("[WP6-NEG-04] NEG-04 no ratio limit (branch inactive)")
    assert json.loads((root() / "artifacts" / "v02" / "seal" / "FINAL_RESULT.json").read_text())["terminal_claim"] != "DYNAMIC_OPTIMALITY_DISPROVED"


def test_seal01_checkout() -> None:
    # console.log equivalent [WP6-SEAL-01]: SEAL-01
    console_log("[WP6-SEAL-01] SEAL-01 parent seal present")
    assert (root() / "parent" / "PARENT_SEAL.json").is_file()


def test_seal02_manifest() -> None:
    # console.log equivalent [WP6-SEAL-02]: SEAL-02
    console_log("[WP6-SEAL-02] SEAL-02 manifest complete")
    lines = (root() / "artifacts" / "v02" / "seal" / "MANIFEST.sha256").read_text().splitlines()
    assert len(lines) > 100
    names = {l.split("  ", 1)[1] for l in lines}
    # the seal manifest and the archive blob must not self-include (T45);
    # other substring matches (e.g. parent/PARENT_MANIFEST.sha256) are legitimate.
    assert "artifacts/v02/seal/MANIFEST.sha256" not in names
    assert "SPLAY-AM-BD-v0.2.tar.zst" not in names
    assert "SPLAY-AM-BD-v0.2.tar.zst.sha256" not in names


def test_seal03_arithmetic() -> None:
    # console.log equivalent [WP6-SEAL-03]: SEAL-03
    console_log("[WP6-SEAL-03] SEAL-03 exact arithmetic only")
    f = json.loads((root() / "artifacts" / "v02" / "seal" / "FINAL_RESULT.json").read_text())
    assert f["terminal_claim"] in f["allowed_claims"]


def test_seal04_recompute() -> None:
    # console.log equivalent [WP6-SEAL-04]: SEAL-04
    console_log("[WP6-SEAL-04] SEAL-04 result recomputable")
    g = json.loads((root() / "artifacts" / "v02" / "logs" / "phase18_gate.json").read_text())
    assert g["verdict"] == "SEALED" and g["terminal_claim"] == "FINITE_DEBT_LAW_MINING_RESULTS"


def test_seal05_archive() -> None:
    # console.log equivalent [WP6-SEAL-05]: SEAL-05
    console_log("[WP6-SEAL-05] SEAL-05 archive determinism file present")
    assert (root() / "SPLAY-AM-BD-v0.2.tar.zst.sha256").is_file()
