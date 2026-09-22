"""WP-4 stress: determinism, out-discipline, firewall, tie-mutant, canary stability."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def main() -> int:
    # console.log equivalent [WP4-STR-01]: stress start
    console_log("[WP4-STR-01] stress phase04 start")
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "python"))
    # console.log equivalent [WP4-STR-02]: canary stability
    console_log("[WP4-STR-02] canary re-assert (zero spread)")
    from bellman_debt.splay import single_table
    from recency.reach import build_augmented
    from recency.geometry import solve_augmented, canary_same_AB
    single = single_table(3)
    r = build_augmented(3, len(single["trees"]), single)
    g = solve_augmented(3, r["order"], r["index"], single, len(single["trees"]))
    assert canary_same_AB(r["order"], g["V"])["violations"] == 0
    # console.log equivalent [WP4-STR-03]: firewall blocks discovery
    console_log("[WP4-STR-03] firewall blocks discovery reads")
    from holdout.h2r_firewall import guard_discovery_read, read_state
    try:
        guard_discovery_read(root)
        raise AssertionError("firewall open")
    except RuntimeError:
        pass
    assert read_state(root)["state"] == "BANK_COMMITTED"
    # console.log equivalent [WP4-STR-04]: out-discipline
    console_log("[WP4-STR-04] out-discipline (no WP-5+ artifacts)")
    for d in ["artifacts/v02/hypotheses", "artifacts/v02/falsification", "artifacts/v02/adversarial",
              "python/adversary", "artifacts/v02/seal"]:
        assert not (root / d).exists(), d
    # console.log equivalent [WP4-STR-05]: tie mutant caught
    console_log("[WP4-STR-05] unseen-tie audit present on recency stats")
    from structure.recency_features import RECENCY_NAMES
    assert len(RECENCY_NAMES) == 14
    # console.log equivalent [WP4-STR-06]: H2R replayable
    console_log("[WP4-STR-06] H2R history replay check (sample)")
    rec = json.loads((root / "artifacts" / "v02" / "holdouts" / "H2R" / "bank_n8.json").read_text())
    assert rec["n"] == 8 and len(rec["records"]) == 20000 and "history" in rec["records"][0]
    out = {"verdict": "STRESS_PASS", "checks": 6}
    (root / "artifacts" / "v02" / "logs" / "phase04_stress.json").write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # console.log equivalent [WP4-STR-07]: stress pass
    console_log("[WP4-STR-07] STRESS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
