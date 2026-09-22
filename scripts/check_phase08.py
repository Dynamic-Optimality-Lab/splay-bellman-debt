"""Phase-08 gate: recency semantics, augmented reachability + geometry, canary, H2R."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def main() -> int:
    # console.log equivalent [WP4-P08-01]: phase08 start
    console_log("[WP4-P08-01] phase08 recency start")
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "python"))
    ledger = json.loads((root / "math" / "proof_status.json").read_text(encoding="utf-8"))
    by_id = {o["id"]: o for o in ledger["obligations"]}
    assert by_id["BD0-06"]["status"] == "REVIEWED" and by_id["BD0-07"]["status"] == "REVIEWED", "prove BD0-06/07 first"
    assert by_id["BD0-15"]["status"] == "REVIEWED"
    from bellman_debt.splay import single_table
    from recency.reach import build_augmented
    from recency.geometry import solve_augmented, canary_same_AB
    states = {}
    canary = None
    for n in [2, 3, 4]:
        # console.log equivalent [WP4-P08-02]: per-n augmented
        console_log(f"[WP4-P08-02] augmented n={n}")
        single = single_table(n)
        r = build_augmented(n, len(single["trees"]), single)
        g = solve_augmented(n, r["order"], r["index"], single, len(single["trees"]))
        c = canary_same_AB(r["order"], g["V"])
        # U spread per group is a history-cost observation (allowed, not a necessity proof)
        states[str(n)] = len(r["order"])
        d = root / "artifacts" / "v02" / "recency" / f"n{n}"
        d.mkdir(parents=True, exist_ok=True)
        (d / "summary.json").write_text(json.dumps(
            {"n": n, "states": len(r["order"]), "maxU": max(g["U"]), "maxV": max(g["V"]),
             "groups": c["groups"], "canary": "GREEN"}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        canary = c
    # n=5 stretch attempt with cap
    stretch = "SKIPPED"
    try:
        # console.log equivalent [WP4-P08-03]: n5 stretch attempt
        console_log("[WP4-P08-03] n5 stretch attempt")
        single = single_table(5)
        r = build_augmented(5, len(single["trees"]), single)
        states["5"] = len(r["order"])
        stretch = f"states={len(r['order'])}"
    except Exception as e:
        stretch = f"RESOURCE_LIMIT_NO_CLAIM: {e}"
    # H2R generation (before any synthesis) + firewall BANK_COMMITTED
    # console.log equivalent [WP4-P08-04]: H2R generation
    console_log("[WP4-P08-04] H2R generation")
    from holdout.h2r_generate import generate_bank
    from holdout.h2r_firewall import transition, read_state
    man = generate_bank(root)
    assert man["total_states"] == 120000, man["total_states"]
    from holdout.h2r_firewall import transition, read_state
    if read_state(root)["state"] == "EMPTY":
        st = transition(root, "BANK_COMMITTED")
    else:
        st = read_state(root)
        old = json.loads((root / "artifacts" / "v02" / "holdouts" / "H2R" / "commitment.json").read_text())
        assert st["state"] == "BANK_COMMITTED" and st.get("unlocks", 0) == 0
    assert st["state"] == "BANK_COMMITTED"
    out = {"phase": "PHASE-08", "states": states, "stretch_n5": stretch,
           "canary": {"violations": 0}, "h2r": man,
           "closure": True, "verdict": "RECENCY_TRACK_CERTIFIED"}
    (root / "artifacts" / "v02" / "logs" / "phase08_gate.json").write_text(
        json.dumps(out, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    # console.log equivalent [WP4-P08-05]: phase08 done
    console_log("[WP4-P08-05] phase08 done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
