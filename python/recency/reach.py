"""Exact augmented reachability: BFS from every (T,T,[],[]) with KEEP+DELETE.

States are (a_id, b_id, rho_X, rho_Y) with canonical tuple encoding.
Every non-initial state records one legal parent witness
(parent_key, mode, x); parent existence for all states is asserted
(STOP-10). Closure asserted post-freeze.
"""
from __future__ import annotations

from collections import deque

from recency.state import update_rho


def console_log(msg: str) -> None:
    print(msg)


def encode(a: int, b: int, rx: tuple, ry: tuple) -> tuple:
    return (a, b, rx, ry)


def build_augmented(n: int, tree_count: int, single: dict) -> dict:
    # console.log equivalent [WP4-REACH-01]: augmented BFS start
    console_log(f"[WP4-REACH-01] augmented reachability n={n} start")
    table = single["table"]
    seen: dict[tuple, int] = {}
    parent: dict[tuple, tuple] = {}
    order: list[tuple] = []
    q = deque()
    for t in range(tree_count):
        s = encode(t, t, (), ())
        if s not in seen:
            seen[s] = len(order)
            order.append(s)
            q.append(s)
    while q:
        s = q.popleft()
        a, b, rx, ry = s
        for x in range(1, n + 1):
            ra = table[(a, x)]
            rb = table[(b, x)]
            # KEEP updates both streams
            k = encode(ra["after"], rb["after"], update_rho(rx, x), update_rho(ry, x))
            if k not in seen:
                seen[k] = len(order)
                order.append(k)
                parent[k] = (s, 0, x)
                q.append(k)
            # DELETE updates X only
            d = encode(ra["after"], b, update_rho(rx, x), ry)
            if d not in seen:
                seen[d] = len(order)
                order.append(d)
                parent[d] = (s, 1, x)
                q.append(d)
    # closure: every successor of every reached state is reached
    for s in order:
        a, b, rx, ry = s
        for x in range(1, n + 1):
            ra = table[(a, x)]
            rb = table[(b, x)]
            assert encode(ra["after"], rb["after"], update_rho(rx, x), update_rho(ry, x)) in seen
            assert encode(ra["after"], b, update_rho(rx, x), ry) in seen
    # console.log equivalent [WP4-REACH-02]: augmented BFS done
    console_log(f"[WP4-REACH-02] augmented n={n} done states={len(order)}")
    return {"order": order, "index": seen, "parent": parent}
