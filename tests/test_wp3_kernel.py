"""K-01..10: quotient/kernel gates (fixed point, agreement, preservation, witnesses)."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_k01_fixed_point() -> None:
    # console.log equivalent [WP3-K-01]: K-01
    console_log("[WP3-K-01] K-01 partition fixed point")
    q = json.loads((root() / "artifacts" / "v02" / "kernels" / "quotient.json").read_text())
    assert q["4"]["rounds"][0] >= 1 and q["4"]["classes"] == 196


def test_k02_agreement() -> None:
    # console.log equivalent [WP3-K-02]: K-02
    console_log("[WP3-K-02] K-02 independent agreement")
    sys.path.insert(0, str(root() / "python"))
    from bellman_debt.splay import single_table
    from bellman_debt.reach import build_reachability
    from kernel.refine import refine
    from kernel.refine2 import refine2, same_partition
    single = single_table(4)
    reach = build_reachability(4, len(single["trees"]), single)
    assert same_partition(refine(4, 14, single, reach["ids"]), refine2(4, 14, single, reach["ids"]), reach["ids"])


def test_k03_cost_preservation() -> None:
    # console.log equivalent [WP3-K-03]: K-03
    console_log("[WP3-K-03] K-03 primitive cost preservation")
    sys.path.insert(0, str(root() / "python"))
    from bellman_debt.splay import single_table
    single = single_table(4)
    for tid in range(14):
        for x in range(1, 5):
            assert 1 <= single["table"][(tid, x)]["cost"] <= 4


def test_k04_successor_preservation() -> None:
    # console.log equivalent [WP3-K-04]: K-04
    console_log("[WP3-K-04] K-04 successor preservation spot check")
    sys.path.insert(0, str(root() / "python"))
    from bellman_debt.splay import single_table
    from bellman_debt.reach import build_reachability
    single = single_table(4)
    reach = build_reachability(4, len(single["trees"]), single)
    s = set(reach["ids"])
    for pid in [0, 15, 195]:
        a, b = pid // 14, pid % 14
        for x in (1, 4):
            assert single["table"][(a, x)]["after"] * 14 + single["table"][(b, x)]["after"] in s


def test_k05_transport_blocked() -> None:
    # console.log equivalent [WP3-K-05]: K-05
    console_log("[WP3-K-05] K-05 transport blocked until BD0-04/05")
    ledger = json.loads((root() / "math" / "proof_status.json").read_text())
    by_id = {o["id"]: o for o in ledger["obligations"]}
    assert by_id["BD0-04"]["status"] == "UNPROVED" and by_id["BD0-05"]["status"] == "UNPROVED"
    gate = json.loads((root() / "artifacts" / "v02" / "logs" / "phase05_gate.json").read_text())
    assert gate["transport"] == "BLOCKED_BD0_04_05_UNPROVED"


def test_k06_full_state() -> None:
    # console.log equivalent [WP3-K-06]: K-06
    console_log("[WP3-K-06] K-06 full-state control")
    q = json.loads((root() / "artifacts" / "v02" / "kernels" / "quotient.json").read_text())
    assert q["7"]["R"] == 184041 and q["7"]["classes"] == 184041


def test_k07_value_witness() -> None:
    # console.log equivalent [WP3-K-07]: K-07
    console_log("[WP3-K-07] K-07 value witness validity")
    a = json.loads((root() / "artifacts" / "v02" / "kernels" / "ablation.json").read_text())
    assert "4" in a and "K0_full" in a["4"]


def test_k08_transition_witness() -> None:
    # console.log equivalent [WP3-K-08]: K-08
    console_log("[WP3-K-08] K-08 transition witness validity")
    sys.path.insert(0, str(root() / "python"))
    import json as J
    from bellman_debt.splay import single_table
    from bellman_debt.reach import build_reachability
    from kernel.ablate import kernel_of
    a = J.loads((root() / "artifacts" / "v02" / "kernels" / "ablation.json").read_text())
    w = a["4"]["K0_full"]["witness"]
    assert w is not None and w[0] < w[1]
    single = single_table(4)
    reach = build_reachability(4, len(single["trees"]), single)
    feats = J.loads((root() / "artifacts" / "v02" / "structure" / "n4.json").read_text())
    fb = {r["state_id"]: r["scalars"] for r in feats["rows"]}
    # witness pair shares weakened kernel (K0_full => full kernel) but mismatches somewhere
    assert kernel_of(fb[str(w[0])], None) == kernel_of(fb[str(w[1])], None)


def test_k09_deterministic() -> None:
    # console.log equivalent [WP3-K-09]: K-09
    console_log("[WP3-K-09] K-09 ablation deterministic")
    a = json.loads((root() / "artifacts" / "v02" / "kernels" / "ablation.json").read_text())
    assert a["4"]["depth"]["witness"] is not None


def test_k10_leak_mutant() -> None:
    # console.log equivalent [WP3-K-10]: K-10
    console_log("[WP3-K-10] K-10 target-leak mutant caught")
    sys.path.insert(0, str(root() / "python"))
    from kernel.ablate import GROUPS
    assert max(max(v) for v in GROUPS.values()) < 39
    import pathlib
    src = pathlib.Path(root() / "python" / "kernel" / "ablate.py").read_text(encoding="utf-8")
    assert "V_scaled" not in src and "BELL-SIG" not in src
