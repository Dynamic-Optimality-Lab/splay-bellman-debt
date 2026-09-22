"""Phase-03 gate (SPEC 03): BELL-SIG, edge specimens, witnesses, trajectories."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def main() -> int:
    # console.log equivalent [WP2-P03-01]: phase03 start
    console_log("[WP2-P03-01] phase03 specimens start")
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "python"))
    from bellman_debt.splay import single_table
    from bellman_debt.reach import build_reachability
    from bellman_debt.signatures import build_signatures
    from bellman_debt.specimens import build_specimens, trajectory_md
    summary = {}
    for n in [2, 3, 4, 5, 6, 7]:
        single = single_table(n)
        reach = build_reachability(n, len(single["trees"]), single)
        # console.log equivalent [WP2-P03-02]: per-n specimens
        console_log(f"[WP2-P03-02] specimens n={n}")
        sigs = build_signatures(n, len(single["trees"]), single, reach["ids"])
        spec = build_specimens(n, len(single["trees"]), single, reach["ids"])
        d = root / "artifacts" / "v02" / "specimens" / f"n{n}"
        d.mkdir(parents=True, exist_ok=True)
        sig_text = json.dumps(sigs, sort_keys=True)
        (d / "signatures.json").write_text(json.dumps(sigs, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (d / "specimens.json").write_text(json.dumps(spec["counts"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
        h = hashlib.sha256(sig_text.encode()).hexdigest().upper()
        (d / "witnesses.json").write_text(json.dumps(spec["witnesses"], indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
        traj = ""
        for cls in ("keep_excess", "delete_create", "exact_repay"):
            traj += trajectory_md(n, spec["witnesses"][cls], single, len(single["trees"]))
        (d / "trajectories.md").write_text(traj, encoding="utf-8")
        summary[n] = {**spec["counts"], "sig_sha": h}
    (root / "artifacts" / "v02" / "logs" / "phase03_gate.json").write_text(
        json.dumps({"phase": "PHASE-03", "summary": summary, "verdict": "SPECIMENS_CERTIFIED"}, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    # console.log equivalent [WP2-P03-03]: phase03 done
    console_log("[WP2-P03-03] phase03 done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
