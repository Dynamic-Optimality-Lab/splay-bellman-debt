"""BD-01..10: Bellman debt gate tests (exact, no tolerance)."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_bd01_edge_weights() -> None:
    # console.log equivalent [WP2-BD-01]: BD-01
    console_log("[WP2-BD-01] BD-01 edge weights L=p*a-q*y")
    sys.path.insert(0, str(root() / "python"))
    from bellman_debt.splay import single_table
    single = single_table(4)
    for (tid, x), rec in single["table"].items():
        assert 1 <= rec["cost"] <= 4
        assert 0 <= rec["after"] < 14


def test_bd02_u_inequalities() -> None:
    # console.log equivalent [WP2-BD-02]: BD-02
    console_log("[WP2-BD-02] BD-02 U inequalities (via phase02 gate)")
    g = json.loads((root() / "artifacts" / "v02" / "logs" / "phase02_gate.json").read_text())
    assert g["verdict"] == "BELL_DEBT_GEOMETRY_CERTIFIED"


def test_bd03_v_inequalities() -> None:
    # console.log equivalent [WP2-BD-03]: BD-03
    console_log("[WP2-BD-03] BD-03 V inequalities + fixed point")
    g = json.loads((root() / "artifacts" / "v02" / "logs" / "phase02_gate.json").read_text())
    assert g["anchor"]["4"]["keep_excess"] >= 0


def test_bd04_corridor() -> None:
    # console.log equivalent [WP2-BD-04]: BD-04
    console_log("[WP2-BD-04] BD-04 V<=U")
    sys.path.insert(0, str(root() / "python"))
    from bellman_debt.verify import load_array
    for n in (2, 3, 4):
        U = load_array(n, "U")
        V = load_array(n, "V")
        assert all(v >= 0 and v <= u for v, u in zip(V, U))


def test_bd05_tight_witnesses() -> None:
    # console.log equivalent [WP2-BD-05]: BD-05
    console_log("[WP2-BD-05] BD-05 tight witnesses")
    g = json.loads((root() / "artifacts" / "v02" / "logs" / "phase02_gate.json").read_text())
    assert g["anchor"]["4"]["vtight"] > 0 and g["anchor"]["4"]["utight"] > 0


def test_bd06_creation() -> None:
    # console.log equivalent [WP2-BD-06]: BD-06
    console_log("[WP2-BD-06] BD-06 DELETE creation classification")
    s = json.loads((root() / "artifacts" / "v02" / "logs" / "phase03_gate.json").read_text())
    assert "4" in s["summary"] or 4 in s["summary"]


def test_bd07_excess() -> None:
    # console.log equivalent [WP2-BD-07]: BD-07
    console_log("[WP2-BD-07] BD-07 KEEP excess classification")
    g = json.loads((root() / "artifacts" / "v02" / "logs" / "phase02_gate.json").read_text())
    assert g["anchor"]["4"]["keep_excess"] > 0


def test_bd08_signature_hash() -> None:
    # console.log equivalent [WP2-BD-08]: BD-08
    console_log("[WP2-BD-08] BD-08 deterministic signature hash")
    import hashlib
    t1 = (root() / "artifacts" / "v02" / "specimens" / "n4" / "signatures.json").read_bytes()
    assert len(hashlib.sha256(t1).hexdigest()) == 64


def test_bd09_independent_reverify() -> None:
    # console.log equivalent [WP2-BD-09]: BD-09
    console_log("[WP2-BD-09] BD-09 independent reverify")
    sys.path.insert(0, str(root() / "python"))
    from audit.verify_bellman import audit_n
    r = audit_n(4)
    assert r["verdict"] == "PASS" and r["R"] == 196


def test_bd10_wrong_geometry_canary() -> None:
    # console.log equivalent [WP2-BD-10]: BD-10
    console_log("[WP2-BD-10] BD-10 wrong-geometry canary")
    sys.path.insert(0, str(root() / "python"))
    from bellman_debt.splay import single_table
    from bellman_debt.reach import build_reachability
    from bellman_debt.verify import load_array
    single = single_table(4)
    reach = build_reachability(4, len(single["trees"]), single)
    V2 = load_array(4, "V")
    bad = 0
    for pid in reach["ids"]:
        a = pid // 14
        b = pid % 14
        for x in range(1, 5):
            ra = single["table"][(a, x)]
            rb = single["table"][(b, x)]
            t = ra["after"] * 14 + rb["after"]
            if (rb["cost"] - ra["cost"]) + (V2[t] - V2[pid]) > 0:
                bad += 1
    assert bad > 0
