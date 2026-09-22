"""Exact development falsification (primary evaluator, RATIONAL branch).

Residuals: E_K = c_B + Phi(t) - Phi(s) - b_H*c_A (KEEP),
           E_D = Phi(t) - Phi(s) - b_H*c_A (DELETE), exact integers.
Correct-b precheck: b_H >= b_n* per certified n (cross-multiplied);
Track-S sandwich V_{bH} <= Phi <= U_{bH} at own b_H (here b_H=2=anchor,
so certified b=2 tables reused byte-consistently). Track-R candidates
are NEVER judged by the pair corridor (BD0-13 bar).
Ordered failure: lexicographically-smallest + maximum positive residual.
"""
from __future__ import annotations

import json
from pathlib import Path

import zstandard as zstd


def console_log(msg: str) -> None:
    print(msg)


PARENT = Path(r"C:\Users\SAIFMA~1\AppData\Local\Temp\opencode\parent_upstream_full")
BNSTAR = {2: (1, 1), 3: (1, 1), 4: (3, 2), 5: (8, 5), 6: (8, 5), 7: (23, 14)}


def bH_feasible(pH: int, qH: int) -> dict:
    recs = {}
    for n, (pn, qn) in BNSTAR.items():
        recs[str(n)] = bool(pH * qn >= pn * qH)
    return recs


def load_VU(n: int) -> tuple[dict, dict]:
    U = {r["pair_id"]: int(r["U_scaled"]) for r in json.loads(
        zstd.ZstdDecompressor().decompress(
            (PARENT / f"artifacts/potentials/n{n}/hypothesis_bH/U.json.zst").read_bytes()).decode())}
    V = {r["pair_id"]: int(r["V_scaled"]) for r in json.loads(
        zstd.ZstdDecompressor().decompress(
            (PARENT / f"artifacts/potentials/n{n}/hypothesis_bH/V.json.zst").read_bytes()).decode())}
    return U, V


def falsify_state_only(hid: str, ns: list[int], repo_root: Path) -> dict:
    # console.log equivalent [WP5-FAL-01]: falsify start
    console_log(f"[WP5-FAL-01] falsify {hid} start ns={ns}")
    import sys
    sys.path.insert(0, str(repo_root / "python"))
    from bellman_debt.splay import single_table
    from bellman_debt.reach import build_reachability
    from structure.trees import build_all
    from mining.synthesize import phi_value
    pH, qH = 2, 1
    feas = bH_feasible(pH, qH)
    assert all(feas.values()), feas
    worst = None
    smallest = None
    checked = 0
    sand_viol = None
    for n in ns:
        single = single_table(n)
        reach = build_reachability(n, len(single["trees"]), single)
        built = build_all(n)
        C = len(single["trees"])
        U, V = load_VU(n)
        table = single["table"]
        for pid in reach["ids"]:
            a = pid // C
            b = pid % C
            phis = phi_value(hid, n, built["data"][a], built["data"][b])
            assert phis >= 0
            if not (V[pid] <= phis <= U[pid]):
                if sand_viol is None:
                    sand_viol = {"n": n, "pid": pid, "V": V[pid], "Phi": phis, "U": U[pid]}
            for x in range(1, n + 1):
                ra = table[(a, x)]
                rb = table[(b, x)]
                ca, cb = ra["cost"], rb["cost"]
                t = ra["after"] * C + rb["after"]
                phit = phi_value(hid, n, built["data"][ra["after"]], built["data"][rb["after"]])
                ek = cb + phit - phis - 2 * ca
                checked += 1
                if ek > 0:
                    if worst is None or ek > worst["residual"]:
                        worst = {"n": n, "mode": "KEEP", "key": x, "source": pid, "target": t,
                                 "residual": ek, "cA": ca, "cB": cb, "Phi_before": phis, "Phi_after": phit}
                    if smallest is None:
                        # traversal order (n, pid, KEEP-before-DELETE, x) is ascending,
                        # so the first violation is the smallest witness.
                        smallest = {"n": n, "mode": "KEEP", "key": x, "source": pid, "target": t,
                                    "residual": ek, "cA": ca, "cB": cb, "Phi_before": phis, "Phi_after": phit}
                t2 = ra["after"] * C + b
                phit2 = phi_value(hid, n, built["data"][ra["after"]], built["data"][b])
                ed = phit2 - phis - 2 * ca
                checked += 1
                if ed > 0:
                    if worst is None or ed > worst["residual"]:
                        worst = {"n": n, "mode": "DELETE", "key": x, "source": pid, "target": t2,
                                 "residual": ed, "cA": ca, "cB": 0, "Phi_before": phis, "Phi_after": phit2}
                    if smallest is None:
                        smallest = {"n": n, "mode": "DELETE", "key": x, "source": pid, "target": t2,
                                    "residual": ed, "cA": ca, "cB": 0, "Phi_before": phis, "Phi_after": phit2}
    # console.log equivalent [WP5-FAL-02]: falsify done
    console_log(f"[WP5-FAL-02] falsify {hid} done checked={checked} worst={worst['residual'] if worst else 0}")
    return {"hypothesis_id": hid, "b_feasible": feas, "sandwich_violation": sand_viol,
            "checked": checked, "worst": worst, "smallest": smallest,
            "verdict": "REJECTED" if (worst or sand_viol) else "SURVIVES_DEV"}


def falsify_recency(hid: str, ns: list[int], repo_root: Path) -> dict:
    # console.log equivalent [WP5-FAL-03]: recency falsify start
    console_log(f"[WP5-FAL-03] falsify {hid} (recency) start ns={ns}")
    import sys
    sys.path.insert(0, str(repo_root / "python"))
    from bellman_debt.splay import single_table
    from recency.reach import build_augmented
    from recency.state import update_rho
    from structure.trees import build_all
    from mining.synthesize import phi_value
    worst = None
    smallest = None
    checked = 0
    for n in ns:
        single = single_table(n)
        r = build_augmented(n, len(single["trees"]), single)
        built = build_all(n)
        table = single["table"]
        for s in r["order"]:
            a, b, rx, ry = s
            phis = phi_value(hid, n, built["data"][a], built["data"][b], rx, ry)
            assert phis >= 0
            # identity: synchronized empty-recency states must read 0
            if a == b and rx == () and ry == ():
                assert phis == 0, (hid, s)
            for x in range(1, n + 1):
                ra = table[(a, x)]
                rb = table[(b, x)]
                ca, cb = ra["cost"], rb["cost"]
                k = (ra["after"], rb["after"], update_rho(rx, x), update_rho(ry, x))
                phit = phi_value(hid, n, built["data"][k[0]], built["data"][k[1]], k[2], k[3])
                ek = cb + phit - phis - 2 * ca
                checked += 1
                if ek > 0 and (worst is None or ek > worst["residual"]):
                    worst = {"n": n, "mode": "KEEP", "key": x, "source": list(s),
                             "residual": ek, "cA": ca, "cB": cb}
                d = (ra["after"], b, update_rho(rx, x), ry)
                phit2 = phi_value(hid, n, built["data"][d[0]], built["data"][d[1]], d[2], d[3])
                ed = phit2 - phis - 2 * ca
                checked += 1
                if ed > 0 and (worst is None or ed > worst["residual"]):
                    worst = {"n": n, "mode": "DELETE", "key": x, "source": list(s),
                             "residual": ed, "cA": ca, "cB": 0}
                if (ek > 0 or ed > 0) and smallest is None:
                    smallest = dict(worst)
    # console.log equivalent [WP5-FAL-04]: recency falsify done
    console_log(f"[WP5-FAL-04] falsify {hid} done checked={checked}")
    return {"hypothesis_id": hid, "checked": checked, "worst": worst, "smallest": smallest,
            "verdict": "REJECTED" if worst else "SURVIVES_DEV",
            "note": "pair corridor NOT applied (BD0-13 bar)"}
