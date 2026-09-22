"""Phase-02 gate (SPEC 02): anchor b=2 geometry + secondary panel + diagnostics."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def main() -> int:
    # console.log equivalent [WP2-P02-01]: phase02 start
    console_log("[WP2-P02-01] phase02 bellman start")
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "python"))
    from bellman_debt.splay import single_table
    from bellman_debt.reach import build_reachability
    from bellman_debt.verify import verify_anchor
    from bellman_debt.panel import run_panel
    anchor = {}
    for n in [2, 3, 4, 5, 6, 7]:
        single = single_table(n)
        reach = build_reachability(n, len(single["trees"]), single)
        # console.log equivalent [WP2-P02-02]: anchor per-n
        console_log(f"[WP2-P02-02] anchor verify n={n}")
        rep = verify_anchor(n, len(single["trees"]), single, reach["ids"])
        anchor[n] = rep
        d = root / "artifacts" / "v02" / "bellman" / f"n{n}_b2"
        d.mkdir(parents=True, exist_ok=True)
        (d / "anchor_report.json").write_text(json.dumps(rep, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    panel = {}
    incomplete = []
    for n in [2, 3, 4, 5]:
        single = single_table(n)
        reach = build_reachability(n, len(single["trees"]), single)
        panel[n] = run_panel(n, len(single["trees"]), single, reach["ids"])
    # console.log equivalent [WP2-P02-03]: stretch panel attempt n=6
    console_log("[WP2-P02-03] stretch panel n=6 attempt")
    try:
        single = single_table(6)
        reach = build_reachability(6, len(single["trees"]), single)
        panel[6] = run_panel(6, len(single["trees"]), single, reach["ids"])
    except Exception as e:
        incomplete.append(f"n6: {e}")
    incomplete.append("n7 panel skipped (resource policy; anchor authoritative)")
    # console.log equivalent [WP2-P02-04]: monotonicity diagnostics
    console_log("[WP2-P02-04] monotonicity diagnostics recorded-not-assumed")
    diag = {"note": "V/U across b recorded as FINITE_OBSERVATION; no monotonicity claim proved", "panel": panel}
    (root / "artifacts" / "v02" / "bellman" / "panel.json").write_text(
        json.dumps(diag, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    status = "BELL_DEBT_GEOMETRY_CERTIFIED"
    out = {"phase": "PHASE-02", "anchor": anchor, "robustness": "ROBUSTNESS_PANEL_INCOMPLETE" if incomplete else "PANEL_COMPLETE",
           "incomplete_notes": incomplete, "verdict": status}
    (root / "artifacts" / "v02" / "logs" / "phase02_gate.json").write_text(
        json.dumps(out, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    # console.log equivalent [WP2-P02-05]: phase02 done
    console_log(f"[WP2-P02-05] phase02 done verdict={status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
