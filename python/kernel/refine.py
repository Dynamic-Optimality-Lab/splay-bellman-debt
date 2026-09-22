"""Behavioral quotient by partition refinement (impl 1, iterative dicts).

Initial signature: primitive immediate data only (track, n, per-x c_A/c_B).
Refinement: new_class = canonical(old_class, [(action, costs, old_class(succ))]).
Target-independent: no U/V/G reads. Stops at exact fixed point.
"""
from __future__ import annotations


def console_log(msg: str) -> None:
    print(msg)


def refine(n: int, tree_count: int, single: dict, reach_ids: list[int]) -> dict:
    # console.log equivalent [WP3-QUO-01]: refine start
    console_log(f"[WP3-QUO-01] quotient n={n} start R={len(reach_ids)}")
    table = single["table"]
    # initial observable: per-x (c_A, c_B) tuple
    sig: dict[int, tuple] = {}
    for pid in reach_ids:
        a = pid // tree_count
        b = pid % tree_count
        obs = []
        for x in range(1, n + 1):
            obs.append((table[(a, x)]["cost"], table[(b, x)]["cost"]))
        sig[pid] = tuple(obs)
    # canonical initial ids
    classes: dict[int, int] = {}
    canon: dict = {}
    for pid in reach_ids:
        if sig[pid] not in canon:
            canon[sig[pid]] = len(canon)
        classes[pid] = canon[sig[pid]]
    rounds = 0
    while True:
        rounds += 1
        keys: dict = {}
        new_classes: dict[int, int] = {}
        for pid in reach_ids:
            a = pid // tree_count
            b = pid % tree_count
            succ = []
            for x in range(1, n + 1):
                ra = table[(a, x)]
                rb = table[(b, x)]
                tK = ra["after"] * tree_count + rb["after"]
                tD = ra["after"] * tree_count + b
                succ.append((x, 0, ra["cost"], rb["cost"], classes[tK]))
                succ.append((x, 1, ra["cost"], 0, classes[tD]))
            key = (classes[pid], tuple(succ))
            if key not in keys:
                keys[key] = len(keys)
            new_classes[pid] = keys[key]
        # partition equality via member sets (class ids may permute)
        old_parts: dict = {}
        new_parts: dict = {}
        for pid in reach_ids:
            old_parts.setdefault(classes[pid], set()).add(pid)
            new_parts.setdefault(new_classes[pid], set()).add(pid)
        if {frozenset(v) for v in old_parts.values()} == {frozenset(v) for v in new_parts.values()}:
            classes = new_classes
            break
        classes = new_classes
        if rounds > 100:
            raise RuntimeError("refinement did not converge")
    # canonicalize by sorted member ids
    parts: dict = {}
    for pid in reach_ids:
        parts.setdefault(classes[pid], []).append(pid)
    ordered = sorted((sorted(v) for v in parts.values()), key=lambda v: v[0])
    final = {}
    for i, members in enumerate(ordered):
        for pid in members:
            final[pid] = i
    # console.log equivalent [WP3-QUO-02]: refine done
    console_log(f"[WP3-QUO-02] quotient n={n} done classes={len(ordered)} rounds={rounds}")
    return {"classes": final, "nclasses": len(ordered), "rounds": rounds}
