"""R-01..12: recency contract gates (exact, no timestamps)."""
from __future__ import annotations

import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def root() -> Path:
    return Path(__file__).resolve().parents[1]


def rec():
    sys.path.insert(0, str(root() / "python"))
    import recency.state as S
    return S


def test_r01_empty_initial() -> None:
    # console.log equivalent [WP4-R-01]: R-01
    console_log("[WP4-R-01] R-01 empty initial")
    S = rec()
    assert S.empty_rho() == ()


def test_r02_update_exact() -> None:
    # console.log equivalent [WP4-R-02]: R-02
    console_log("[WP4-R-02] R-02 update exact")
    S = rec()
    assert S.update_rho((), 2) == (2,)
    assert S.update_rho((2, 1), 3) == (3, 2, 1)


def test_r03_duplicate_front() -> None:
    # console.log equivalent [WP4-R-03]: R-03
    console_log("[WP4-R-03] R-03 duplicate moves to front")
    S = rec()
    assert S.update_rho((3, 2, 1), 2) == (2, 3, 1)


def test_r04_keep_both() -> None:
    # console.log equivalent [WP4-R-04]: R-04
    console_log("[WP4-R-04] R-04 KEEP updates both")
    S = rec()
    assert S.keep_successor((0, 0, (2,), (1,)), 3, 9, 8) == (9, 8, (3, 2), (3, 1))


def test_r05_delete_x_only() -> None:
    # console.log equivalent [WP4-R-05]: R-05
    console_log("[WP4-R-05] R-05 DELETE updates X only")
    S = rec()
    assert S.delete_successor((0, 0, (2,), (1,)), 3, 9) == (9, 0, (3, 2), (1,))


def test_r06_complement() -> None:
    # console.log equivalent [WP4-R-06]: R-06
    console_log("[WP4-R-06] R-06 seen/unseen complement")
    S = rec()
    assert S.unseen_keys((3, 1), 4) == (2, 4)


def test_r07_replay() -> None:
    # console.log equivalent [WP4-R-07]: R-07
    console_log("[WP4-R-07] R-07 relative-order replay")
    S = rec()
    assert S.replay_order([1, 2, 1, 3]) == (3, 1, 2)
    assert S.check_relative_order((3, 1, 2), [1, 2, 1, 3])


def test_r08_parent_witness() -> None:
    # console.log equivalent [WP4-R-08]: R-08
    console_log("[WP4-R-08] R-08 augmented parent witness")
    import json
    g = json.loads((root() / "artifacts" / "v02" / "logs" / "phase08_gate.json").read_text())
    assert g["states"]["2"] == 20 and g["states"]["3"] == 235


def test_r09_closure() -> None:
    # console.log equivalent [WP4-R-09]: R-09
    console_log("[WP4-R-09] R-09 augmented closure asserted")
    import json
    g = json.loads((root() / "artifacts" / "v02" / "logs" / "phase08_gate.json").read_text())
    assert g["closure"] is True


def test_r10_separation_is_canary() -> None:
    # console.log equivalent [WP4-R-10]: R-10
    console_log("[WP4-R-10] R-10 same-pair grouping is canary (zero spread)")
    import json
    g = json.loads((root() / "artifacts" / "v02" / "logs" / "phase08_gate.json").read_text())
    assert g["canary"]["violations"] == 0


def test_r11_tie_audit() -> None:
    # console.log equivalent [WP4-R-11]: R-11
    console_log("[WP4-R-11] R-11 unseen-tie audit present")
    sys.path.insert(0, str(root() / "python"))
    from structure.recency_features import recency_features
    from structure.trees import build_all
    built = build_all(4)
    f = recency_features(4, built["data"][0], built["data"][1], (1,), (2, 1))
    assert f["tie_audit"] == "TIE_EXPLICIT"


def test_r12_independent() -> None:
    # console.log equivalent [WP4-R-12]: R-12
    console_log("[WP4-R-12] R-12 BD0-06/07 REVIEWED")
    import json
    ledger = json.loads((root() / "math" / "proof_status.json").read_text())
    by_id = {o["id"]: o for o in ledger["obligations"]}
    assert by_id["BD0-06"]["status"] == "REVIEWED" and by_id["BD0-07"]["status"] == "REVIEWED"
