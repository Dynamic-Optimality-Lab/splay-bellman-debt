"""Phase-10 gate: debt atoms, creation/repayment screens, scale audit, exhaustion."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def main() -> int:
    # console.log equivalent [WP4-P10-01]: phase10 start
    console_log("[WP4-P10-01] phase10 atoms start")
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "python"))
    from bellman_debt.splay import single_table
    from recency.reach import build_augmented
    from recency.geometry import solve_augmented
    from structure.trees import build_all
    from mining.atoms import atom_vector, ATOM_KINDS, screen_creation, scale_audit
    results = {}
    maxima = {}
    for n in [2, 3, 4]:
        # console.log equivalent [WP4-P10-02]: per-n atoms
        console_log(f"[WP4-P10-02] atoms n={n}")
        single = single_table(n)
        r = build_augmented(n, len(single["trees"]), single)
        g = solve_augmented(n, r["order"], r["index"], single, len(single["trees"]))
        built = build_all(n)
        V = {s: v for s, v in zip(r["order"], g["V"])}
        table = single["table"]
        fam = {}
        for kind in ATOM_KINDS:
            vals = {}
            deltas = []
            cov_create = cov_repay = 0
            tot_create = tot_repay = 0
            mx = 0
            for s in r["order"]:
                a, b, rx, ry = s
                va = atom_vector(kind, n, built["data"][a], built["data"][b], rx, ry)["v"]
                vals[s] = va
                mx = max(mx, abs(va))
            for s in r["order"]:
                a, b, rx, ry = s
                for x in range(1, n + 1):
                    ra = table[(a, x)]
                    # DELETE creation screen
                    d = (ra["after"], b, update_rx(rx, x), ry)
                    tot_create += 1
                    dvd = V[d] - V[s]
                    pred = vals[d] - vals[s]
                    if dvd > 0 and pred == dvd:
                        cov_create += 1
                    # KEEP repayment screen (positive excess only)
                    rb = table[(b, x)]
                    t = (ra["after"], rb["after"], update_rx(rx, x), update_rx(ry, x))
                    Ws = rb["cost"] - 2 * ra["cost"]
                    if Ws > 0:
                        tot_repay += 1
                        if vals[s] - vals[t] >= Ws:
                            cov_repay += 1
            fam[kind] = {"create": [cov_create, tot_create], "repay": [cov_repay, tot_repay]}
            maxima.setdefault(kind, {})[str(n)] = mx
        results[str(n)] = fam
    # family exhaustion: SURVIVING_FORMULA only at 100% both screens, else inconsistent witness
    verdict = {}
    for kind in ATOM_KINDS:
        ok = all(results[str(n)][kind]["create"][0] == results[str(n)][kind]["create"][1] and
                 results[str(n)][kind]["repay"][0] == results[str(n)][kind]["repay"][1] for n in [2, 3, 4])
        verdict[kind] = "SURVIVING_FORMULA" if ok else "DEBT_ATOM_FAMILY_INCONSISTENT"
    out = {"families": results, "verdicts": verdict,
           "scale": {k: scale_audit({n: [v] for n, v in m.items()}) for k, m in maxima.items()},
           "note": "no family required to survive; inconsistent witnesses are results"}
    d = root / "artifacts" / "v02" / "debt_atoms"
    d.mkdir(parents=True, exist_ok=True)
    (d / "recency_atoms.json").write_text(json.dumps(out, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    (root / "artifacts" / "v02" / "logs" / "phase10_gate.json").write_text(
        json.dumps({"phase": "PHASE-10", "verdicts": verdict, "verdict": "DEBT_ATOMS_COMPLETE"}, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    # console.log equivalent [WP4-P10-03]: phase10 done
    console_log("[WP4-P10-03] phase10 done")
    return 0


def update_rx(rx: tuple, x: int) -> tuple:
    return (x,) + tuple(k for k in rx if k != x)


if __name__ == "__main__":
    raise SystemExit(main())
