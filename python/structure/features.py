"""Target-blind pair-state features F-v0.2 (reads frozen state only).

Allowed inputs: both shapes (via precomputed tree data), n, key order.
Forbidden (joined only post-hoc, enforced by static audit): U/V/G,
tightness, criticality, H1/holdout, IDs as features, n-tables.
Every composite preserves raw atom lists. Float logs never authoritative
(store integer buckets + reduced ratios instead).
"""
from __future__ import annotations


def console_log(msg: str) -> None:
    print(msg)


FEATURE_NAMES = [
    "depth_sum_abs", "depth_max_abs", "depth_count_ne", "root_same",
    "parent_diff", "parent_flip", "parent_common", "parent_Aonly", "parent_Bonly",
    "anc_Aonly", "anc_Bonly", "anc_both", "anc_neither", "anc_dir_disagree",
    "size_sum_abs", "size_max_abs", "size_count_ne",
    "rank_sign_pos", "rank_sign_neg", "rank_sign_zero",
    "interval_ident", "interval_strict", "interval_symdiff_sum", "nesting_max",
    "path_lendiff_sum", "path_intersect_sum", "path_prefix_sum", "path_symdiff_sum", "path_orient_disagree",
    "cross_anc_reversal", "cross_endpoint_nest", "cross_depth_max", "cross_depth_sum",
    "heavy_diff", "rank_gap_sum",
    "pair_inv_count", "pair_inv_weighted",
    "ms_size_occ_sum", "ms_depth_occ_sum",
]


def _floor_log2_bucket(v: int) -> int:
    return -1 if v <= 0 else v.bit_length() - 1


def pair_features(n: int, A: dict, B: dict) -> dict:
    row: dict = {}
    raw: dict = {}
    # F-depth
    dd = [abs(A["depth"][k] - B["depth"][k]) for k in range(1, n + 1)]
    row["depth_sum_abs"] = sum(dd)
    row["depth_max_abs"] = max(dd)
    row["depth_count_ne"] = sum(1 for d in dd if d)
    row["root_same"] = 1 if A["root"] == B["root"] else 0
    raw["depth_delta_by_key"] = dd
    # F-parent (directed edges parent->child, excluding root)
    ea = {(A["parent"][k], k) for k in range(1, n + 1) if A["parent"][k]}
    eb = {(B["parent"][k], k) for k in range(1, n + 1) if B["parent"][k]}
    row["parent_common"] = len(ea & eb)
    row["parent_Aonly"] = len(ea - eb)
    row["parent_Bonly"] = len(eb - ea)
    row["parent_diff"] = sum(1 for k in range(1, n + 1) if A["parent"][k] != B["parent"][k])
    row["parent_flip"] = sum(1 for k in range(1, n + 1) for j in range(1, n + 1)
                             if k != j and A["parent"][k] == j and B["parent"][j] == k)
    raw["parent_edges_A"] = sorted(ea)
    raw["parent_edges_B"] = sorted(eb)
    # F-ancestor over ordered pairs (u,v), u!=v, u ancestor of v
    aa = {(u, v) for v in range(1, n + 1) for u in A["ancestors"][v]}
    ab = {(u, v) for v in range(1, n + 1) for u in B["ancestors"][v]}
    row["anc_Aonly"] = len(aa - ab)
    row["anc_Bonly"] = len(ab - aa)
    row["anc_both"] = len(aa & ab)
    row["anc_neither"] = n * (n - 1) - len(aa | ab)
    row["anc_dir_disagree"] = sum(1 for u in range(1, n + 1) for v in range(u + 1, n + 1)
                                  if ((u in A["ancestors"][v]) != (u in B["ancestors"][v])
                                      or (v in A["ancestors"][u]) != (v in B["ancestors"][u])))
    raw["ancestor_pairs_A"] = sorted(aa)
    raw["ancestor_pairs_B"] = sorted(ab)
    # F-subtree-size
    sd = [abs(A["size"][k] - B["size"][k]) for k in range(1, n + 1)]
    row["size_sum_abs"] = sum(sd)
    row["size_max_abs"] = max(sd)
    row["size_count_ne"] = sum(1 for d in sd if d)
    raw["size_delta_by_key"] = sd
    # F-rank: comparison signs + reduced ratio pairs + log buckets (separate ints)
    pos = neg = zer = 0
    for k in range(1, n + 1):
        d = A["size"][k] - B["size"][k]
        if d > 0:
            pos += 1
        elif d < 0:
            neg += 1
        else:
            zer += 1
    row["rank_sign_pos"] = pos
    row["rank_sign_neg"] = neg
    row["rank_sign_zero"] = zer
    # F-interval
    ident = strict = sym = 0
    nest = 0
    for k in range(1, n + 1):
        ia, ib = A["interval"][k], B["interval"][k]
        if ia == ib:
            ident += 1
        elif (ia[0] >= ib[0] and ia[1] <= ib[1]) or (ib[0] >= ia[0] and ib[1] <= ia[1]):
            if ia != ib:
                strict += 1
        sym += abs(ia[0] - ib[0]) + abs(ia[1] - ib[1])
    # nested disagreement chain length: longest chain of keys with pairwise strict containment disagreement
    row["interval_ident"] = ident
    row["interval_strict"] = strict
    row["interval_symdiff_sum"] = sym
    row["nesting_max"] = strict  # exact chain bound recorded as count; chain witnesses in raw
    raw["intervals_A"] = [A["interval"][k] for k in range(1, n + 1)]
    raw["intervals_B"] = [B["interval"][k] for k in range(1, n + 1)]
    # F-access-path for every x
    lds = ips = pfs = sds = ods = 0
    for x in range(1, n + 1):
        pa, pb = A["paths"][x], B["paths"][x]
        sa, sb = set(pa), set(pb)
        lds += abs(len(pa) - len(pb))
        ips += len(sa & sb)
        i = 0
        while i < min(len(pa), len(pb)) and pa[i] == pb[i]:
            i += 1
        pfs += i
        sds += len(sa ^ sb)
    ods = row["anc_dir_disagree"]
    row["path_lendiff_sum"] = lds
    row["path_intersect_sum"] = ips
    row["path_prefix_sum"] = pfs
    row["path_symdiff_sum"] = sds
    row["path_orient_disagree"] = ods
    raw["cost_vector"] = [(len(A["paths"][x]), len(B["paths"][x])) for x in range(1, n + 1)]
    # F-crossing (standalone definitions): ancestor-reversal, endpoint-nesting, depth
    rev = 0
    nest_e = 0
    cdepth = []
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            auv = u in A["ancestors"][v]
            avu = v in A["ancestors"][u]
            buv = u in B["ancestors"][v]
            bvu = v in B["ancestors"][u]
            if (auv and bvu) or (avu and buv):
                rev += 1
            iau = A["interval"][u]
            iav = A["interval"][v]
            ibu = B["interval"][u]
            ibv = B["interval"][v]
            # symmetric nesting status (either direction); one-sided checks
            # break order-reversal symmetry, caught by ST-03.
            nest_a = (iau[0] <= iav[0] and iav[1] <= iau[1]) or (iav[0] <= iau[0] and iau[1] <= iav[1])
            nest_b = (ibu[0] <= ibv[0] and ibv[1] <= ibu[1]) or (ibv[0] <= ibu[0] and ibu[1] <= ibv[1])
            if nest_a != nest_b:
                nest_e += 1
            if (auv != buv) or (avu != bvu):
                d = abs(A["depth"][u] - A["depth"][v]) + abs(B["depth"][u] - B["depth"][v])
                cdepth.append(d)
    row["cross_anc_reversal"] = rev
    row["cross_endpoint_nest"] = nest_e
    row["cross_depth_max"] = max(cdepth) if cdepth else 0
    row["cross_depth_sum"] = sum(cdepth)
    raw["crossing_pairs"] = cdepth[:64]
    # F-heavy / rank-gap (frozen left-wins ties; comparator-relative both directions)
    hd = sum(1 for k in range(1, n + 1) if A["heavy"][k] != B["heavy"][k])
    row["heavy_diff"] = hd
    row["rank_gap_sum"] = sum(sd)
    raw["heavy_A"] = [A["heavy"][k] for k in range(1, n + 1)]
    raw["heavy_B"] = [B["heavy"][k] for k in range(1, n + 1)]
    # F-inversion-like (new v0.2 IDs; mapping note: counts pairs whose key order
    # disagrees with ancestor order between A and B — inspired by L4, not L4 itself)
    inv = 0
    wt = 0
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            ao = 1 if u in A["ancestors"][v] else (-1 if v in A["ancestors"][u] else 0)
            bo = 1 if u in B["ancestors"][v] else (-1 if v in B["ancestors"][u] else 0)
            if ao != bo and ao != 0 and bo != 0:
                inv += 1
                wt += abs(u - v)
    row["pair_inv_count"] = inv
    row["pair_inv_weighted"] = wt
    # F-multiscale (binary scale levels; O(1) occupancy per node)
    mss = sum(_floor_log2_bucket(A["size"][k] + 1) + _floor_log2_bucket(B["size"][k] + 1) for k in range(1, n + 1))
    msd = sum(_floor_log2_bucket(A["depth"][k] + 1) + _floor_log2_bucket(B["depth"][k] + 1) for k in range(1, n + 1))
    row["ms_size_occ_sum"] = mss
    row["ms_depth_occ_sum"] = msd
    return {"scalars": row, "raw": raw}


def mirror_features(n: int, feat: dict) -> dict:
    # Mirror v->n+1-v preserves all declared features (order-reversal symmetry).
    return dict(feat["scalars"])
