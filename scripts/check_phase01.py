"""Phase-01 gate (SPEC 01): read-only import + independent reproduction policy.

Loads parent fact rows, rebuilds our single-tree tables + reachability for
n=2..7, asserts counts match, reverifies b_n* certificates structurally
(without rediscovery), writes fact table + gate log.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def main() -> int:
    # console.log equivalent [WP2-P01-01]: phase01 start
    console_log("[WP2-P01-01] phase01 import start")
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "python"))
    from bellman_debt.splay import single_table
    from bellman_debt.reach import build_reachability
    from bellman_debt.import_parent import build_fact_table, EXPECTED_R
    # console.log equivalent [WP2-P01-02]: fact table
    console_log("[WP2-P01-02] building fact table")
    rows = build_fact_table([2, 3, 4, 5, 6, 7])
    for r in rows:
        assert r["R_match"] and r["b_match"] and r["maxU_match"] and r["maxV_match"] and r["forced_match"], r
    out_dir = root / "artifacts" / "v02" / "parent_import"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "fact_table.json").write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # console.log equivalent [WP2-P01-03]: reachability rebuild
    console_log("[WP2-P01-03] rebuilding reachability n=2..7")
    counts = {}
    for n in [2, 3, 4, 5, 6, 7]:
        single = single_table(n)
        assert len(single["table"]) == n * len(single["trees"])
        reach = build_reachability(n, len(single["trees"]), single)
        assert len(reach["ids"]) == EXPECTED_R[n], (n, len(reach["ids"]))
        counts[n] = len(reach["ids"])
    # console.log equivalent [WP2-P01-04]: phase01 done
    console_log(f"[WP2-P01-04] phase01 done counts={counts}")
    (root / "artifacts" / "v02" / "logs" / "phase01_gate.json").write_text(
        json.dumps({"phase": "PHASE-01", "fact_rows": len(rows), "R": counts, "verdict": "IMPORT_VERIFIED"}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
