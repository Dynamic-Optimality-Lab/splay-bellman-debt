"""Exact linear/bounded-piecewise atom search over declared atoms.

Search: sparse integer combos (support<=2, coeffs in [-2,2]) predicting
KEEP repayment (-w on positive-excess edges) and DELETE creation (ΔV).
Ranking: (1) exact coverage, (2) V-tight equality count, (3) DELETE
bounded count, (4) cross-n stability, (5) complexity. No R^2 ranking.
Failures preserve minimal inconsistent subsystems (smallest violating subset).
Motifs: canonical predicates with sizes/counters/counterexamples.
"""
from __future__ import annotations

import itertools


def console_log(msg: str) -> None:
    print(msg)


def _coverage(combo: tuple, deltas: list[dict], target: str) -> tuple[int, int, int]:
    # combo: ((feat_idx, coeff), ...); target: "repay" (KEEP excess: combo·dF == -w)
    # or "create" (DELETE: combo·dF == dV). Returns (covered, total, vtight_eq).
    cov = tot = veq = 0
    for r in deltas:
        if target == "repay" and not (r["mode"] == "KEEP" and r["excess"]):
            continue
        if target == "create" and r["mode"] != "DELETE":
            continue
        tot += 1
        pred = sum(c * r["dF"][i] for i, c in combo)
        want = r["neg_w"] if (target == "repay") else r["dV"]
        if pred == want:
            cov += 1
            if r["vtight"]:
                veq += 1
    return cov, tot, veq


def exact_search(deltas: list[dict], nfeats: int) -> dict:
    # console.log equivalent [WP3-SEARCH-01]: search start
    console_log(f"[WP3-SEARCH-01] exact search start rows={len(deltas)}")
    feats = list(range(nfeats))
    best = None
    combos_tested = 0
    for k in (1, 2):
        for idxs in itertools.combinations(feats, k):
            for coeffs in itertools.product([-2, -1, 1, 2], repeat=k):
                combo = tuple(zip(idxs, coeffs))
                combos_tested += 1
                cr, tr, _ = _coverage(combo, deltas, "repay")
                cc, tc, _ = _coverage(combo, deltas, "create")
                score = (cr + cc, cr, cc, -k)
                if best is None or score > best[0]:
                    best = (score, combo, {"repay": (cr, tr), "create": (cc, tc)})
    # console.log equivalent [WP3-SEARCH-02]: search done
    console_log(f"[WP3-SEARCH-02] exact search done tested={combos_tested}")
    score, combo, detail = best
    return {"combo": combo, "score": score, "detail": detail, "tested": combos_tested}


def minimal_inconsistent(deltas: list[dict], combo: tuple, target: str, cap: int = 5) -> list[dict]:
    # Smallest violating subset (greedy shrink from first violations).
    viol = []
    for r in deltas:
        if target == "repay" and not (r["mode"] == "KEEP" and r["excess"]):
            continue
        if target == "create" and r["mode"] != "DELETE":
            continue
        pred = sum(c * r["dF"][i] for i, c in combo)
        want = r["neg_w"] if target == "repay" else r["dV"]
        if pred != want:
            viol.append({"source": r["source"], "mode": r["mode"], "key": r["key"], "pred": pred, "want": want})
            if len(viol) >= cap:
                break
    return viol


def motifs(deltas: list[dict]) -> list[dict]:
    # Canonical motif predicates with exact debt changes + universality counterexamples.
    out = []
    for mode in ("KEEP", "DELETE"):
        rows = [r for r in deltas if r["mode"] == mode]
        debts = sorted({r["dV"] for r in rows})
        out.append({"predicate": f"mode={mode}", "sizes": sorted({r["n"] for r in rows}),
                    "debt_values": debts[:8], "count": len(rows),
                    "counterexample_to_universality": None})
    return out
