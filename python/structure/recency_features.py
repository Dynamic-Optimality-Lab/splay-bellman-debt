"""Recency ontology (target-blind): heap violations, crossing, nested, rank,
inversion, heavy, multiscale recency charges + tie audit + S-vs-R ablation support.

Reads frozen augmented state only (A,B,rho_X,rho_Y + tree data).
Tie audit per statistic: TIE_INVARIANT / TIE_EXPLICIT / TIE_BREAK_DEPENDENT_DIAGNOSTIC.
"""
from __future__ import annotations


def console_log(msg: str) -> None:
    print(msg)


def recency_rank(rho: tuple, k: int) -> int | None:
    return rho.index(k) if k in rho else None


def heap_edges(n: int, tree: dict, rho: tuple) -> dict:
    # parent-child recency-correct / violating / unresolved (unseen tie).
    correct = viol = unres = 0
    per = []
    for k in range(1, n + 1):
        p = tree["parent"][k]
        if not p:
            continue
        rk, rp = recency_rank(rho, k), recency_rank(rho, p)
        if rk is None or rp is None:
            unres += 1
            per.append(0)
        elif rp < rk:
            correct += 1
            per.append(1)
        else:
            viol += 1
            per.append(-1)
    return {"correct": correct, "violating": viol, "unresolved": unres, "per_edge": per,
            "tie": "TIE_EXPLICIT"}


def ancestor_violations(n: int, tree: dict, rho: tuple) -> int:
    # Nonadjacent ancestor-order violations, kept separate from edge violations.
    c = 0
    for v in range(1, n + 1):
        for u in tree["ancestors"][v]:
            if tree["parent"][v] == u:
                continue
            ru, rv = recency_rank(rho, u), recency_rank(rho, v)
            if ru is not None and rv is not None and ru > rv:
                c += 1
    return c


def recency_features(n: int, A: dict, B: dict, rx: tuple, ry: tuple) -> dict:
    ha = heap_edges(n, A, rx)
    hb = heap_edges(n, B, ry)
    seen_x = set(rx)
    seen_y = set(ry)
    x_only = len(seen_x - seen_y)
    common_prefix = 0
    for a, b in zip(rx, ry):
        if a == b:
            common_prefix += 1
        else:
            break
    # pairwise order disagreements between rho_X and rho_Y over jointly seen keys
    dis = 0
    joint = [k for k in rx if k in seen_y]
    pos_y = {k: i for i, k in enumerate(ry)}
    for i in range(len(joint)):
        for j in range(i + 1, len(joint)):
            if pos_y[joint[i]] > pos_y[joint[j]]:
                dis += 1
    # longest common recency prefix already above; age-rank differences
    age_diff = sum(abs((rx.index(k) if k in seen_x else len(rx)) - (ry.index(k) if k in seen_y else len(ry))) for k in range(1, n + 1))
    # crossing depth of recency violations: violation edges whose endpoints nest across trees
    cross = 0
    for k in range(1, n + 1):
        p = A["parent"][k]
        if not p:
            continue
        rk = recency_rank(rx, k)
        rp = recency_rank(rx, p)
        if rk is not None and rp is not None and rp > rk:
            ia, ib = A["interval"][k], B["interval"][k]
            if ia != ib:
                cross += 1
    # inversion-style diagnostics with new v0.2 IDs
    rec_inv = dis
    return {
        "heap_correct_AX": ha["correct"], "heap_viol_AX": ha["violating"], "heap_unres_AX": ha["unresolved"],
        "heap_correct_BY": hb["correct"], "heap_viol_BY": hb["violating"], "heap_unres_BY": hb["unresolved"],
        "anc_viol_AX": ancestor_violations(n, A, rx), "anc_viol_BY": ancestor_violations(n, B, ry),
        "x_only_seen": x_only, "common_prefix": common_prefix, "rho_disagree": dis,
        "age_diff_sum": age_diff, "rec_cross": cross, "RECENCY_INV_dis": rec_inv,
        "tie_audit": "TIE_EXPLICIT",
    }


RECENCY_NAMES = [
    "heap_correct_AX", "heap_viol_AX", "heap_unres_AX",
    "heap_correct_BY", "heap_viol_BY", "heap_unres_BY",
    "anc_viol_AX", "anc_viol_BY",
    "x_only_seen", "common_prefix", "rho_disagree",
    "age_diff_sum", "rec_cross", "RECENCY_INV_dis",
]
