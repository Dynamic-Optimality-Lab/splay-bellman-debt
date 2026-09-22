"""Augmented fixed-b geometry at b=2 + SA-01 canary.

U_2^R: multi-source shortest scaled slack from all initial states.
V_2^R: reversed-graph longest future (super-sink zero init).
Canary: group by (A,B), assert zero V-spread; nonzero => RECENCY_V_CANARY_FAIL.
"""
from __future__ import annotations

from collections import deque

from recency.state import update_rho


def console_log(msg: str) -> None:
    print(msg)


def build_edges(order: list[tuple], index: dict, n: int, single: dict) -> tuple[list, list]:
    table = single["table"]
    fwd: list[list] = [[] for _ in order]
    rev: list[list] = [[] for _ in order]
    for i, s in enumerate(order):
        a, b, rx, ry = s
        for x in range(1, n + 1):
            ra = table[(a, x)]
            rb = table[(b, x)]
            k = (ra["after"], rb["after"], update_rho(rx, x), update_rho(ry, x))
            j = index[k]
            w = (rb["cost"], ra["cost"])  # (y, a)
            fwd[i].append((j, w, 0, x))
            rev[j].append((i, w, 0, x))
            d = (ra["after"], b, update_rho(rx, x), ry)
            j2 = index[d]
            w2 = (0, ra["cost"])
            fwd[i].append((j2, w2, 1, x))
            rev[j2].append((i, w2, 1, x))
    return fwd, rev


def solve_augmented(n: int, order: list[tuple], index: dict, single: dict, tree_count: int,
                    p: int = 2, q: int = 1) -> dict:
    # console.log equivalent [WP4-GEO-01]: augmented solve start
    console_log(f"[WP4-GEO-01] augmented b={p}/{q} solve n={n} states={len(order)}")
    fwd, rev = build_edges(order, index, n, single)
    N = len(order)
    INF = 10 ** 18
    # U: multi-source from all true initials (T,T,(),()).
    init = set()
    for t in range(tree_count):
        init.add(index[(t, t, (), ())])
    dist = [INF] * N
    dq = deque()
    inq = [False] * N
    for i in init:
        dist[i] = 0
        dq.append(i)
        inq[i] = True
    cnt = [0] * N
    while dq:
        u = dq.popleft()
        inq[u] = False
        du = dist[u]
        for v, (y, a), mode, x in fwd[u]:
            w = p * a - q * y
            if du + w < dist[v]:
                dist[v] = du + w
                cnt[v] += 1
                if cnt[v] > N:
                    raise RuntimeError("infeasible b (negative slack cycle)")
                if not inq[v]:
                    dq.append(v)
                    inq[v] = True
    U = dist
    # V via reversed graph, super-sink zero init
    dist2 = [0] * N
    dq = deque(range(N))
    inq = [True] * N
    cnt = [0] * N
    while dq:
        u = dq.popleft()
        inq[u] = False
        for v, (y, a), mode, x in rev[u]:
            w = p * a - q * y
            if dist2[u] + w < dist2[v]:
                dist2[v] = dist2[u] + w
                cnt[v] += 1
                if cnt[v] > N:
                    raise RuntimeError("infeasible b (reversed)")
                if not inq[v]:
                    dq.append(v)
                    inq[v] = True
    V = [-d for d in dist2]
    for v in V:
        assert v >= 0
    # console.log equivalent [WP4-GEO-02]: augmented solve done
    console_log(f"[WP4-GEO-02] augmented n={n} done maxU={max(U)} maxV={max(V)}")
    return {"U": U, "V": V, "G": [u - v for u, v in zip(U, V)]}


def canary_same_AB(order: list[tuple], V: list) -> dict:
    # console.log equivalent [WP4-CAN-01]: canary grouping
    console_log("[WP4-CAN-01] SA-01 canary grouping by (A,B)")
    groups: dict = {}
    for i, s in enumerate(order):
        groups.setdefault((s[0], s[1]), []).append(V[i])
    bad = {k: (min(v), max(v)) for k, v in groups.items() if min(v) != max(v)}
    if bad:
        raise RuntimeError(f"RECENCY_V_CANARY_FAIL groups={len(bad)} e.g. {list(bad.items())[:3]}")
    # console.log equivalent [WP4-CAN-02]: canary green
    console_log(f"[WP4-CAN-02] canary green groups={len(groups)}")
    return {"groups": len(groups), "violations": 0}
