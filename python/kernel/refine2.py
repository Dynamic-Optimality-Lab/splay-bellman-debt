"""Independent quotient implementation (impl 2: string-keyed refinement).

Different code path from refine.py (string signatures + sort-based
canonicalization instead of dict/tuple keys). Agreement checked by
sorted-member comparison, not id equality.
"""
from __future__ import annotations


def console_log(msg: str) -> None:
    print(msg)


def refine2(n: int, tree_count: int, single: dict, reach_ids: list[int]) -> dict:
    # console.log equivalent [WP3-QUO2-01]: refine2 start
    console_log(f"[WP3-QUO2-01] quotient2 n={n} start R={len(reach_ids)}")
    table = single["table"]
    cur = {}
    for pid in reach_ids:
        a = pid // tree_count
        b = pid % tree_count
        cur[pid] = "|".join(f"{table[(a, x)]['cost']},{table[(b, x)]['cost']}" for x in range(1, n + 1))
    # normalize to ids
    def norm(mapping):
        vals = sorted(set(mapping.values()))
        idx = {v: i for i, v in enumerate(vals)}
        return {k: idx[v] for k, v in mapping.items()}

    classes = norm(cur)
    rounds = 0
    while True:
        rounds += 1
        nxt = {}
        for pid in reach_ids:
            a = pid // tree_count
            b = pid % tree_count
            parts = [f"C{classes[pid]}"]
            for x in range(1, n + 1):
                ra = table[(a, x)]
                rb = table[(b, x)]
                tK = ra["after"] * tree_count + rb["after"]
                tD = ra["after"] * tree_count + b
                parts.append(f"K{x}:{ra['cost']},{rb['cost']}->{classes[tK]}")
                parts.append(f"D{x}:{ra['cost']},0->{classes[tD]}")
            nxt[pid] = ";".join(parts)
        new_classes = norm(nxt)
        old_parts = {}
        new_parts = {}
        for pid in reach_ids:
            old_parts.setdefault(classes[pid], set()).add(pid)
            new_parts.setdefault(new_classes[pid], set()).add(pid)
        if {frozenset(v) for v in old_parts.values()} == {frozenset(v) for v in new_parts.values()}:
            classes = new_classes
            break
        classes = new_classes
        if rounds > 100:
            raise RuntimeError("refine2 did not converge")
    parts = {}
    for pid in reach_ids:
        parts.setdefault(classes[pid], []).append(pid)
    ordered = sorted((sorted(v) for v in parts.values()), key=lambda v: v[0])
    final = {}
    for i, members in enumerate(ordered):
        for pid in members:
            final[pid] = i
    # console.log equivalent [WP3-QUO2-02]: refine2 done
    console_log(f"[WP3-QUO2-02] quotient2 n={n} done classes={len(ordered)} rounds={rounds}")
    return {"classes": final, "nclasses": len(ordered), "rounds": rounds}


def same_partition(r1: dict, r2: dict, reach_ids: list[int]) -> bool:
    def parts(r):
        d: dict = {}
        for pid in reach_ids:
            d.setdefault(r["classes"][pid], set()).add(pid)
        return {frozenset(v) for v in d.values()}

    return parts(r1) == parts(r2)
