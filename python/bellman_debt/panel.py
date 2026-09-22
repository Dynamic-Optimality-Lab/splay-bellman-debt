"""Secondary fixed-b robustness panel (5/2, 3, 4): exact solves on required sizes.

Required n=2..5; stretch n=6..7 only if resources permit, else
ROBUSTNESS_PANEL_INCOMPLETE (anchor science unblocked). Values are
diagnostics, never tuning knobs. Monotonicity across b recorded, never assumed.
"""
from __future__ import annotations

from collections import deque


def console_log(msg: str) -> None:
    print(msg)


def solve_U(n: int, tree_count: int, single: dict, reach_ids: list[int], p: int, q: int) -> dict | None:
    # Multi-source shortest scaled slack from diagonals (SLF label-correcting).
    table = single["table"]
    INF = 10 ** 18
    dist = {pid: INF for pid in reach_ids}
    inq = {}
    dq = deque()
    for t in range(tree_count):
        pid = t * tree_count + t
        if pid in dist:
            dist[pid] = 0
            dq.append(pid)
            inq[pid] = True
    # adjacency forward
    adj: dict[int, list] = {pid: [] for pid in reach_ids}
    for pid in reach_ids:
        a = pid // tree_count
        b = pid % tree_count
        for x in range(1, n + 1):
            ra = table[(a, x)]
            rb = table[(b, x)]
            t = ra["after"] * tree_count + rb["after"]
            adj[pid].append((t, p * ra["cost"] - q * rb["cost"]))
            t2 = ra["after"] * tree_count + b
            adj[pid].append((t2, p * ra["cost"]))
    cnt = {pid: 0 for pid in reach_ids}
    while dq:
        u = dq.popleft()
        inq[u] = False
        du = dist[u]
        for v, w in adj[u]:
            if du + w < dist[v]:
                dist[v] = du + w
                cnt[v] += 1
                if cnt[v] > len(reach_ids):
                    return None  # infeasible b (negative cycle)
                if not inq.get(v, False):
                    if dq and dist[v] < dist[dq[0]]:
                        dq.appendleft(v)
                    else:
                        dq.append(v)
                    inq[v] = True
    return dist


def solve_V(n: int, tree_count: int, single: dict, reach_ids: list[int], p: int, q: int, U: dict) -> dict | None:
    # V = -min future slack via reversed graph from super-sink (empty continuation => V>=0).
    table = single["table"]
    INF = 10 ** 18
    # reverse adjacency
    radj: dict[int, list] = {pid: [] for pid in reach_ids}
    for pid in reach_ids:
        a = pid // tree_count
        b = pid % tree_count
        for x in range(1, n + 1):
            ra = table[(a, x)]
            rb = table[(b, x)]
            t = ra["after"] * tree_count + rb["after"]
            radj[t].append((pid, p * ra["cost"] - q * rb["cost"]))
            t2 = ra["after"] * tree_count + b
            radj[t2].append((pid, p * ra["cost"]))
    dist = {pid: 0 for pid in reach_ids}  # super-sink zero init
    inq = {pid: True for pid in reach_ids}
    dq = deque(reach_ids)
    cnt = {pid: 0 for pid in reach_ids}
    while dq:
        u = dq.popleft()
        inq[u] = False
        for v, w in radj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                cnt[v] += 1
                if cnt[v] > len(reach_ids):
                    return None
                if not inq[v]:
                    dq.append(v)
                    inq[v] = True
    V = {pid: -dist[pid] for pid in reach_ids}
    for pid in reach_ids:
        if V[pid] < 0:
            return None
    return V


def run_panel(n: int, tree_count: int, single: dict, reach_ids: list[int]) -> dict:
    # console.log equivalent [WP2-PANEL-01]: panel start
    console_log(f"[WP2-PANEL-01] panel n={n} start")
    out = {}
    for (p, q) in [(5, 2), (3, 1), (4, 1)]:
        U = solve_U(n, tree_count, single, reach_ids, p, q)
        if U is None:
            out[f"{p}/{q}"] = {"feasible": False}
            continue
        V = solve_V(n, tree_count, single, reach_ids, p, q, U)
        if V is None:
            out[f"{p}/{q}"] = {"feasible": False}
            continue
        out[f"{p}/{q}"] = {"feasible": True, "maxU": max(U.values()), "maxV": max(V.values())}
    # console.log equivalent [WP2-PANEL-02]: panel done
    console_log(f"[WP2-PANEL-02] panel n={n} done")
    return out
