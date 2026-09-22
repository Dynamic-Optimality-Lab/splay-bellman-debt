"""Independent Bellman audit: separate Splay implementation, no discovery imports.

Reads only schemas + frozen parent arrays + contract. Re-derives single-tree
transitions with a dict-based (non-object) Splay core, then rechecks every
Bellman inequality. Import-scan gate: this module must not import
discovery packages (checked per import-statement lines).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import zstandard as zstd


def console_log(msg: str) -> None:
    print(msg)


PARENT = Path(r"C:\Users\SAIFMA~1\AppData\Local\Temp\opencode\parent_upstream_full")


def _shapes(n: int):
    if n == 0:
        return [None]
    out = []
    for l in range(n):
        for ls in _shapes(l):
            for rs in _shapes(n - 1 - l):
                out.append((ls, rs))
    return out


def _ser(s) -> str:
    return "." if s is None else "(" + _ser(s[0]) + _ser(s[1]) + ")"


def _parse(ss: str):
    pos = [0]

    def rec():
        if ss[pos[0]] == ".":
            pos[0] += 1
            return None
        pos[0] += 1
        l = rec()
        r = rec()
        assert ss[pos[0]] == ")"
        pos[0] += 1
        return (l, r)

    return rec()


def _splay_dict(nodes: dict, root_key: int, x: int) -> tuple[int, list[str]]:
    # nodes: key -> {"l":k|None,"r":k|None,"p":k|None}; rotations mutate dict.
    def left(k):
        return nodes[k]["l"]

    def right(k):
        return nodes[k]["r"]

    def par(k):
        return nodes[k]["p"]

    def rot_right(v):
        p = par(v)
        g = par(p)
        b = right(v)
        nodes[v]["r"] = p
        nodes[p]["p"] = v
        nodes[p]["l"] = b
        if b is not None:
            nodes[b]["p"] = p
        nodes[v]["p"] = g
        if g is not None:
            if nodes[g]["l"] == p:
                nodes[g]["l"] = v
            else:
                nodes[g]["r"] = v
        return v if g is None else root_key

    def rot_left(v):
        p = par(v)
        g = par(p)
        b = left(v)
        nodes[v]["l"] = p
        nodes[p]["p"] = v
        nodes[p]["r"] = b
        if b is not None:
            nodes[b]["p"] = p
        nodes[v]["p"] = g
        if g is not None:
            if nodes[g]["l"] == p:
                nodes[g]["l"] = v
            else:
                nodes[g]["r"] = v
        return v if g is None else root_key

    cases = []
    # find path
    path = []
    cur = root_key
    while cur is not None:
        path.append(cur)
        if x == cur:
            break
        cur = left(cur) if x < cur else right(cur)
    v = x
    root = root_key
    while par(v) is not None:
        p = par(v)
        g = par(p)
        if g is None:
            if nodes[p]["l"] == v:
                root = rot_right(v)
            else:
                root = rot_left(v)
            cases.append("ZIG")
        elif nodes[g]["l"] == p and nodes[p]["l"] == v:
            root = rot_right(p)
            root = rot_right(v)
            cases.append("LL")
        elif nodes[g]["r"] == p and nodes[p]["r"] == v:
            root = rot_left(p)
            root = rot_left(v)
            cases.append("RR")
        elif nodes[g]["l"] == p and nodes[p]["r"] == v:
            root = rot_left(v)
            root = rot_right(v)
            cases.append("LR")
        else:
            root = rot_right(v)
            root = rot_left(v)
            cases.append("RL")
    return root, cases


def _tree_nodes(shape, n: int) -> tuple[dict, int]:
    # Assign inorder keys 1..n to shape nodes; return (nodes, root_key).
    nodes: dict[int, dict] = {}
    seq: list = []

    def collect(s):
        if s is None:
            return
        collect(s[0])
        seq.append(s)
        collect(s[1])

    collect(shape)
    key_of = {id(s): i + 1 for i, s in enumerate(seq)}
    for s in seq:
        k = key_of[id(s)]
        nodes[k] = {"l": None, "r": None, "p": None}
    # link children by structure
    def link(s):
        if s is None:
            return None
        k = key_of[id(s)]
        lk = link(s[0])
        rk = link(s[1])
        nodes[k]["l"] = lk
        nodes[k]["r"] = rk
        if lk is not None:
            nodes[lk]["p"] = k
        if rk is not None:
            nodes[rk]["p"] = k
        return k

    root = link(shape)
    return nodes, root


def _cost(nodes: dict, root: int, x: int) -> int:
    d = 0
    cur = root
    while cur != x:
        cur = nodes[cur]["l"] if x < cur else nodes[cur]["r"]
        d += 1
    return d + 1


def _shape_of(nodes: dict, root: int):
    def rec(k):
        if k is None:
            return None
        return (rec(nodes[k]["l"]), rec(nodes[k]["r"]))

    return rec(root)


def audit_n(n: int) -> dict:
    # console.log equivalent [WP2-AUD-01]: audit start
    console_log(f"[WP2-AUD-01] independent audit n={n} start")
    serials = sorted(_ser(s) for s in _shapes(n))
    id_of = {ss: i for i, ss in enumerate(serials)}
    # single table via dict core
    table = {}
    for ss in serials:
        shape = _parse(ss)
        tid = id_of[ss]
        for x in range(1, n + 1):
            nodes, root = _tree_nodes(shape, n)
            c = _cost(nodes, root, x)
            root2, _ = _splay_dict(nodes, root, x)
            after = id_of[_ser(_shape_of(nodes, root2))]
            table[(tid, x)] = (c, after)
    raw = (PARENT / f"artifacts/potentials/n{n}/hypothesis_bH/U.json.zst").read_bytes()
    Urows = json.loads(zstd.ZstdDecompressor().decompress(raw).decode())
    raw = (PARENT / f"artifacts/potentials/n{n}/hypothesis_bH/V.json.zst").read_bytes()
    Vrows = json.loads(zstd.ZstdDecompressor().decompress(raw).decode())
    U = {r["pair_id"]: int(r["U_scaled"]) for r in Urows}
    V = {r["pair_id"]: int(r["V_scaled"]) for r in Vrows}
    C = len(serials)
    pids = [a * C + b for a in range(C) for b in range(C)]
    # reachability filter via BFS on our table
    from collections import deque
    seen = set()
    dq = deque()
    for t in range(C):
        seen.add(t * C + t)
        dq.append(t * C + t)
    while dq:
        pid = dq.popleft()
        a, b = pid // C, pid % C
        for x in range(1, n + 1):
            a2 = table[(a, x)][1]
            b2 = table[(b, x)][1]
            for nid in (a2 * C + b2, a2 * C + b):
                if nid not in seen:
                    seen.add(nid)
                    dq.append(nid)
    for pid in seen:
        assert V[pid] >= 0 and V[pid] <= U[pid], f"audit corridor fail {pid}"
        a, b = pid // C, pid % C
        for x in range(1, n + 1):
            ca, a2 = table[(a, x)]
            cb, b2 = table[(b, x)]
            t = a2 * C + b2
            # scaled residual Ru = Ws + (U[t]-U[s]) <= 0  <=>  cb-2ca + dU <= 0 (q=1)
            assert (cb - 2 * ca) + (U[t] - U[pid]) <= 0, f"U-ineq {pid}"
            assert (cb - 2 * ca) + (V[t] - V[pid]) <= 0, f"V-ineq {pid}"
            t2 = a2 * C + b
            assert (-2 * ca) + (U[t2] - U[pid]) <= 0
            assert (-2 * ca) + (V[t2] - V[pid]) <= 0
    # console.log equivalent [WP2-AUD-02]: audit done
    console_log(f"[WP2-AUD-02] independent audit n={n} done R={len(seen)}")
    return {"n": n, "R": len(seen), "verdict": "PASS"}
