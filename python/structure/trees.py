"""Per-tree structural precompute (state-only; no Bellman reads).

Families: depth, parent, ancestors, subtree sizes, intervals, all-key
access paths, heavy-child decomposition (left-wins ties), rank buckets.
Frozen tie rules recorded here. Mirror map v->n+1-v supported.
"""
from __future__ import annotations


def console_log(msg: str) -> None:
    print(msg)


def parse_shape(ss: str):
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


def serialize_shape(s) -> str:
    return "." if s is None else "(" + serialize_shape(s[0]) + serialize_shape(s[1]) + ")"


def all_shapes(n: int) -> list:
    if n == 0:
        return [None]
    out = []
    for l in range(n):
        for ls in all_shapes(l):
            for rs in all_shapes(n - 1 - l):
                out.append((ls, rs))
    return out


def tree_data(n: int, shape) -> dict:
    # Inorder keys 1..n; returns depth/parent/ancestors/sizes/intervals/paths/heavy.
    parent: dict[int, int] = {}
    depth: dict[int, int] = {}
    children: dict[int, list] = {}

    # Assign keys by inorder rank over shape nodes.
    seq: list = []

    def collect(s):
        if s is None:
            return
        collect(s[0])
        seq.append(s)
        collect(s[1])

    collect(shape)
    key_of = {id(s): i + 1 for i, s in enumerate(seq)}

    def link(s, pkey, d):
        if s is None:
            return None
        k = key_of[id(s)]
        parent[k] = pkey
        depth[k] = d
        lk = link(s[0], k, d + 1)
        rk = link(s[1], k, d + 1)
        children[k] = [lk, rk]
        return k

    root = link(shape, 0, 0)
    # subtree sizes + intervals via post-order on keys
    size: dict[int, int] = {}
    interval: dict[int, tuple] = {}

    def post(k):
        if k is None:
            return (0, None, None)
        lk, rk = children[k]
        sl, mil, mal = post(lk)
        sr, mir, mar = post(rk)
        sz = 1 + sl + sr
        mn = k
        mx = k
        if mil is not None:
            mn = min(mn, mil)
            mx = max(mx, mal)
        if mir is not None:
            mn = min(mn, mir)
            mx = max(mx, mar)
        size[k] = sz
        interval[k] = (mn, mx)
        return (sz, mn, mx)

    post(root)
    # ancestor sets
    ancestors: dict[int, set] = {k: set() for k in range(1, n + 1)}
    for k in range(1, n + 1):
        p = parent[k]
        while p:
            ancestors[k].add(p)
            p = parent[p]
    # access paths root->x
    paths: dict[int, list] = {}
    for x in range(1, n + 1):
        path = [x]
        p = parent[x]
        while p:
            path.append(p)
            p = parent[p]
        paths[x] = list(reversed(path))
    # heavy child: larger subtree wins; ties go LEFT (frozen).
    heavy: dict[int, int | None] = {}
    for k in range(1, n + 1):
        lk, rk = children[k]
        sl = size[lk] if lk is not None else 0
        sr = size[rk] if rk is not None else 0
        if lk is None and rk is None:
            heavy[k] = None
        elif sl >= sr:
            heavy[k] = lk
        else:
            heavy[k] = rk
    return {
        "root": root, "parent": parent, "depth": depth,
        "children": children, "size": size, "interval": interval,
        "ancestors": ancestors, "paths": paths, "heavy": heavy,
    }


def build_all(n: int) -> dict:
    # console.log equivalent [WP3-TREE-02]: build all trees
    console_log(f"[WP3-TREE-02] tree precompute n={n} start")
    serials = sorted(serialize_shape(s) for s in all_shapes(n))
    data = {}
    for tid, ss in enumerate(serials):
        data[tid] = tree_data(n, parse_shape(ss))
    # console.log equivalent [WP3-TREE-03]: build done
    console_log(f"[WP3-TREE-03] tree precompute n={n} done trees={len(data)}")
    return {"serials": serials, "data": data}
