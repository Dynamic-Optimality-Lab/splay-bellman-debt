"""Clean-room candidate evaluator: independent re-implementation from math text.

Receives only the frozen PHI definition, b_H, and cost/recency contracts.
Imports nothing from discovery (mining/falsify/structure-augmented paths
are asserted absent by scan). Functional tuple-based Splay core, distinct
from object/dict cores. Agreement with the primary evaluator is required.
"""
from __future__ import annotations

import json
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


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


def _ser(s) -> str:
    return "." if s is None else "(" + _ser(s[0]) + _ser(s[1]) + ")"


def _label(shape, keys):
    seq = []

    def collect(s):
        if s is None:
            return
        collect(s[0])
        seq.append(s)
        collect(s[1])

    collect(shape)
    mp = {}
    for i, s in enumerate(seq):
        mp[id(s)] = keys[i]

    def build(s):
        if s is None:
            return None
        return (mp[id(s)], build(s[0]), build(s[1]))

    return build(shape)


def _find(t, x, d=0):
    # returns (cost, path_keys)
    if t is None:
        raise KeyError(x)
    k, l, r = t
    if x == k:
        return d + 1, [k]
    if x < k:
        c, p = _find(l, x, d + 1)
        return c, [k] + p
    c, p = _find(r, x, d + 1)
    return c, [k] + p


def _rot_right(t, v):
    # functional rotations on (key,left,right) tuples by key search
    return _rot(t, v, "R")


def _rot_left(t, v):
    return _rot(t, v, "L")


def _rot(t, v, d):
    if t is None:
        return t
    k, l, r = t
    p = _parent(t, v)
    if p is None:
        return t
    pk, pl, pr = p
    if d == "R":
        # v is left child of p
        vl, vr = _kids(t, v)
        new_p = (pk, vr, pr)
        new_v = (v, vl, new_p)
    else:
        vl, vr = _kids(t, v)
        new_p = (pk, pl, vl)
        new_v = (v, new_p, vr)
    return _replace(t, pk, new_v)


def _kids(t, v):
    n = _get(t, v)
    return n[1], n[2]


def _get(t, v):
    if t is None:
        return None
    k, l, r = t
    if v == k:
        return t
    return _get(l, v) if v < k else _get(r, v)


def _parent(t, v, p=None):
    if t is None:
        return None
    k, l, r = t
    if v == k:
        return p
    return _parent(l, v, t) if v < k else _parent(r, v, t)


def _replace(t, old, new):
    if t is None:
        return None
    if t[0] == old[0]:
        return new
    k, l, r = t
    return (k, _replace(l, old, new), _replace(r, old, new))


def _splay(t, x):
    while True:
        p = _parent(t, x)
        if p is None:
            return t
        g = _parent(t, p[0])
        if g is None:
            t = _rot_right(t, x) if p[1] is not None and p[1][0] == x else _rot_left(t, x)
        elif g[1] is not None and g[1][0] == p[0] and p[1] is not None and p[1][0] == x:
            t = _rot_right(t, p[0])
            t = _rot_right(t, x)
        elif g[2] is not None and g[2][0] == p[0] and p[2] is not None and p[2][0] == x:
            t = _rot_left(t, p[0])
            t = _rot_left(t, x)
        elif g[1] is not None and g[1][0] == p[0]:
            t = _rot_left(t, x)
            t = _rot_right(t, x)
        else:
            t = _rot_right(t, x)
            t = _rot_left(t, x)
    return t


def _depths(t, d=0, out=None):
    if out is None:
        out = {}
    if t is None:
        return out
    out[t[0]] = d
    _depths(t[1], d + 1, out)
    _depths(t[2], d + 1, out)
    return out


def _sizes(t):
    if t is None:
        return {}, 0
    dl, sl = _sizes(t[1])
    dr, sr = _sizes(t[2])
    tot = 1 + sl + sr
    out = {t[0]: tot}
    out.update(dl)
    out.update(dr)
    return out, tot


def phi_clean(hid: str, n: int, tA, tB) -> int:
    if hid == "PHI-0001":
        da, db = _depths(tA), _depths(tB)
        return sum(abs(da[k] - db[k]) for k in range(1, n + 1))
    if hid == "PHI-0002":
        sa, _ = _sizes(tA)
        sb, _ = _sizes(tB)
        return sum(abs(sa[k] - sb[k]) for k in range(1, n + 1))
    raise ValueError(hid)


def evaluate_sample(hid: str, n: int, cases: list) -> dict:
    # cases: list of (shapeA_serial, shapeB_serial, primary_phi_value).
    # Recomputes each value with the independent functional core and asserts equality.
    # console.log equivalent [WP5-CLEAN-01]: clean-room sample
    console_log(f"[WP5-CLEAN-01] clean-room {hid} n={n} cases={len(cases)}")
    agree = 0
    for sa, sb, primary in cases:
        tA = _label(_parse(sa), list(range(1, n + 1)))
        tB = _label(_parse(sb), list(range(1, n + 1)))
        v = phi_clean(hid, n, tA, tB)
        assert v >= 0
        assert v == primary, (hid, sa, sb, v, primary)
        agree += 1
    # console.log equivalent [WP5-CLEAN-02]: clean-room done
    console_log(f"[WP5-CLEAN-02] clean-room {hid} done agree={agree}")
    return {"total": len(cases), "agree": agree}
