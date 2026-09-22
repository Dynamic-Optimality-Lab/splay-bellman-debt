"""Pair reachability by BFS from diagonals using our single-tree tables."""
from __future__ import annotations

from collections import deque


def console_log(msg: str) -> None:
    print(msg)


def build_reachability(n: int, tree_count: int, single: dict) -> dict:
    # console.log equivalent [WP2-REACH-01]: BFS start
    console_log(f"[WP2-REACH-01] reachability n={n} start")
    table = single["table"]
    seen: dict[int, bool] = {}
    parent: dict[int, tuple] = {}
    q = deque()
    for t in range(tree_count):
        pid = t * tree_count + t
        seen[pid] = True
        q.append(pid)
    while q:
        pid = q.popleft()
        a = pid // tree_count
        b = pid % tree_count
        for x in range(1, n + 1):
            a2 = table[(a, x)]["after"]
            b2 = table[(b, x)]["after"]
            for mode, nid in ((0, a2 * tree_count + b2), (1, a2 * tree_count + b)):
                if nid not in seen:
                    seen[nid] = True
                    parent[nid] = (pid, mode, x)
                    q.append(nid)
    ids = sorted(seen)
    # console.log equivalent [WP2-REACH-02]: BFS done
    console_log(f"[WP2-REACH-02] reachability n={n} done R={len(ids)}")
    return {"ids": ids, "parent": parent}
