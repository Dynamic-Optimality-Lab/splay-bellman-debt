"""D/HLD gates at candidate level: eligibility, residuals, counterexamples, firewalls."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_d01_identity() -> None:
    # console.log equivalent [WP5-D-01]: D-01
    console_log("[WP5-D-01] D-01 identity normalization on diagonals")
    sys.path.insert(0, str(root() / "python"))
    from structure.trees import build_all
    from mining.synthesize import phi_value
    built = build_all(4)
    for hid in ("PHI-0001", "PHI-0002"):
        for tid in range(14):
            assert phi_value(hid, 4, built["data"][tid], built["data"][tid]) == 0


def test_d02_nonnegativity() -> None:
    # console.log equivalent [WP5-D-02]: D-02
    console_log("[WP5-D-02] D-02 nonnegativity on dev domain")
    sys.path.insert(0, str(root() / "python"))
    from structure.trees import build_all
    from mining.synthesize import phi_value
    built = build_all(3)
    for hid in ("PHI-0001", "PHI-0002"):
        for a in range(5):
            for b in range(5):
                assert phi_value(hid, 3, built["data"][a], built["data"][b]) >= 0


def test_d03_bH_meta() -> None:
    # console.log equivalent [WP5-D-03]: D-03
    console_log("[WP5-D-03] D-03 one frozen universal b_H per hypothesis")
    for hid in ("PHI-0001", "PHI-0002", "PHI-0003"):
        c = json.loads((root() / "artifacts" / "v02" / "hypotheses" / f"{hid}.eval_contract.json").read_text())
        assert c["b_hypothesis"] == {"p": "2", "q": "1"} and c["b_is_universal_candidate"] is True


def test_d04_wrong_b_canary() -> None:
    # console.log equivalent [WP5-D-04]: D-04
    console_log("[WP5-D-04] D-04 b_H=2 feasible on all certified n")
    g = json.loads((root() / "artifacts" / "v02" / "logs" / "phase11_gate.json").read_text())
    assert g["b_feasible_all_n"] is True


def test_d05_sign_and_zero_tolerance() -> None:
    # console.log equivalent [WP5-D-05]: D-05
    console_log("[WP5-D-05] D-05 exact residuals, no tolerance")
    for hid in ("PHI-0001", "PHI-0002", "PHI-0003"):
        dev = json.loads((root() / "artifacts" / "v02" / "falsification" / hid / "dev.json").read_text())
        assert dev["worst"]["residual"] > 0 and dev["verdict"] == "REJECTED"


def test_d06_smallest_counterexample() -> None:
    # console.log equivalent [WP5-D-06]: D-06
    console_log("[WP5-D-06] D-06 smallest exact counterexamples preserved")
    for hid in ("PHI-0001", "PHI-0002", "PHI-0003"):
        dev = json.loads((root() / "artifacts" / "v02" / "falsification" / hid / "dev.json").read_text())
        assert dev["smallest"] is not None and dev["smallest"]["residual"] > 0


def test_hld01_n8_contaminated() -> None:
    # console.log equivalent [WP5-HLD-01]: HLD-01
    console_log("[WP5-HLD-01] HLD-01 n8 never fresh")
    import json as J
    seal = J.loads((root() / "parent" / "PARENT_SEAL.json").read_text())
    assert seal["n8_status"] == "PARTIALLY_REVEALED_CANARY_CONTAMINATED"


def test_hld02_08_firewalls() -> None:
    # console.log equivalent [WP5-HLD-02]: HLD-02..08
    console_log("[WP5-HLD-02] HLD-02..08 firewalls + set immutability")
    cs = json.loads((root() / "artifacts" / "v02" / "holdouts" / "candidate_set.json").read_text())
    assert cs["set"] == [] and cs["h1"] == "UNREAD" and cs["h2r"] == "UNLOCKED_NEVER" and cs["n8"] == "UNCONTACTED"
    fw = json.loads((root() / "artifacts" / "v02" / "holdouts" / "H2R" / "firewall.json").read_text())
    assert fw["state"] == "BANK_COMMITTED" and fw.get("unlocks", 0) == 0
