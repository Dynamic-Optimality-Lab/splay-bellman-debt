"""D-01..06 (atom side): exact evaluation, residuals, identity, nonnegativity, b_H meta, mutants."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_d01_exact_atom() -> None:
    # console.log equivalent [WP4-D-01]: D-01
    console_log("[WP4-D-01] D-01 exact atom evaluation")
    sys.path.insert(0, str(root() / "python"))
    from structure.trees import build_all
    from mining.atoms import atom_vector, ATOM_KINDS
    built = build_all(4)
    for k in ATOM_KINDS:
        v = atom_vector(k, 4, built["data"][0], built["data"][1], (1,), (2,))
        assert isinstance(v["v"], int) and v["bound"] >= 0


def test_d02_delete_residual() -> None:
    # console.log equivalent [WP4-D-02]: D-02
    console_log("[WP4-D-02] D-02 DELETE creation screen recorded")
    r = json.loads((root() / "artifacts" / "v02" / "debt_atoms" / "recency_atoms.json").read_text())
    assert "D3_recency" in r["families"]["4"]


def test_d03_keep_residual() -> None:
    # console.log equivalent [WP4-D-03]: D-03
    console_log("[WP4-D-03] D-03 KEEP repayment screen recorded")
    r = json.loads((root() / "artifacts" / "v02" / "debt_atoms" / "recency_atoms.json").read_text())
    assert r["families"]["4"]["D5_rank"]["repay"][1] == 3334


def test_d04_identity() -> None:
    # console.log equivalent [WP4-D-04]: D-04
    console_log("[WP4-D-04] D-04 synchronized-zero check")
    sys.path.insert(0, str(root() / "python"))
    from structure.trees import build_all
    from mining.atoms import atom_vector
    built = build_all(4)
    for k in ["D1_node", "D2_edge", "D3_recency", "D5_rank", "D6_mapped"]:
        v = atom_vector(k, 4, built["data"][2], built["data"][2], (), ())
        assert v["v"] == 0, (k, v)


def test_d05_nonnegativity() -> None:
    # console.log equivalent [WP4-D-05]: D-05
    console_log("[WP4-D-05] D-05 atom values are counts (>=0)")
    r = json.loads((root() / "artifacts" / "v02" / "debt_atoms" / "recency_atoms.json").read_text())
    assert set(r["verdicts"]) == {"D1_node", "D2_edge", "D3_recency", "D4_nested", "D5_rank", "D6_mapped", "D7_multiscale"}
    sys.path.insert(0, str(root() / "python"))
    from structure.trees import build_all
    from mining.atoms import atom_vector, ATOM_KINDS
    built = build_all(3)
    for k in ATOM_KINDS:
        assert atom_vector(k, 3, built["data"][0], built["data"][1], (1,), ())["v"] >= 0


def test_d06_scale_audit() -> None:
    # console.log equivalent [WP4-D-06]: D-06
    console_log("[WP4-D-06] D-06 scale audit finite-observation labeled")
    r = json.loads((root() / "artifacts" / "v02" / "debt_atoms" / "recency_atoms.json").read_text())
    assert r["scale"]["D5_rank"]["4"]["note"].startswith("finite observation")
