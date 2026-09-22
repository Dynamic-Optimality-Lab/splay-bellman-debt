"""K0 ablation: overcomplete kernel minus one family; necessity witnesses.

Kernel coordinates: groups of scalar feature indices (target-blind).
For each removed group, the lexicographically smallest witness pair with
same weakened kernel but (a) different V_2 [VALUE], (b) primitive
transition mismatch [TRANSITION], or (c) different behavioral class
[BEHAVIOR_CLASS] is recorded. Surviving removals are finite survival only.
Wording COMPONENTWISE_NECESSARY_FINITE; no minimality overclaim.
"""
from __future__ import annotations


def console_log(msg: str) -> None:
    print(msg)


GROUPS = {
    "depth": [0, 1, 2, 3],
    "parent": [4, 5, 6, 7, 8],
    "ancestor": [9, 10, 11, 12, 13],
    "subtree": [14, 15, 16],
    "rank": [17, 18, 19],
    "interval": [20, 21, 22, 23],
    "accesspath": [24, 25, 26, 27, 28],
    "crossing": [29, 30, 31, 32],
    "heavy": [33, 34],
    "inversion": [35, 36],
    "multiscale": [37, 38],
}


def kernel_of(scalars: list[int], drop: str | None) -> tuple:
    skip = set(GROUPS.get(drop, [])) if drop else set()
    return tuple(v for i, v in enumerate(scalars) if i not in skip)


def ablate(n: int, feat_rows: list[dict], V: dict, classes: dict,
           tree_count: int, single: dict, reach_ids: list[int]) -> dict:
    # console.log equivalent [WP3-ABL-01]: ablation start
    console_log(f"[WP3-ABL-01] ablation n={n} start")
    by_state = {r["state_id"]: r["scalars"] for r in feat_rows}
    table = single["table"]
    results = {}
    for g in list(GROUPS) + [None]:
        name = g if g else "K0_full"
        # group states by weakened kernel
        buckets: dict[tuple, list] = {}
        for pid in reach_ids:
            k = kernel_of(by_state[str(pid)], g)
            buckets.setdefault(k, []).append(pid)
        witness = None
        wtype = "FINITE_SUFFICIENT"
        for members in buckets.values():
            if len(members) < 2:
                continue
            members = sorted(members)
            for i in range(len(members)):
                for j in range(i + 1, len(members)):
                    s1, s2 = members[i], members[j]
                    if V[str(s1)] != V[str(s2)]:
                        witness = (s1, s2)
                        wtype = "KERNEL_VALUE_INSUFFICIENT"
                        break
                    # transition mismatch under identity key correspondence
                    a1, b1 = s1 // tree_count, s1 % tree_count
                    a2, b2 = s2 // tree_count, s2 % tree_count
                    mismatch = False
                    for x in range(1, n + 1):
                        r1a = table[(a1, x)]
                        r2a = table[(a2, x)]
                        if r1a["cost"] != r2a["cost"]:
                            mismatch = True
                            break
                        r1b = table[(b1, x)]
                        r2b = table[(b2, x)]
                        if r1b["cost"] != r2b["cost"]:
                            mismatch = True
                            break
                        t1K = r1a["after"] * tree_count + r1b["after"]
                        t2K = r2a["after"] * tree_count + r2b["after"]
                        if kernel_of(by_state[str(t1K)], g) != kernel_of(by_state[str(t2K)], g):
                            mismatch = True
                            break
                    if mismatch:
                        witness = (s1, s2)
                        wtype = "KERNEL_TRANSITION_INSUFFICIENT"
                        break
                    if classes[s1] != classes[s2]:
                        witness = (s1, s2)
                        wtype = "KERNEL_BEHAVIOR_CLASS_INSUFFICIENT"
                        break
                if witness:
                    break
            if witness:
                break
        results[name] = {"type": wtype, "witness": witness,
                         "note": "COMPONENTWISE_NECESSARY_FINITE" if witness else "FINITE_SUFFICIENT"}
    # console.log equivalent [WP3-ABL-02]: ablation done
    console_log(f"[WP3-ABL-02] ablation n={n} done")
    return results
